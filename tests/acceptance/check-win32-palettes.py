#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Exercise real Wine owned palettes in a captured, disposable native runtime."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import uuid


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def execute(command, log, timeout):
    with log.open("wb") as stream:
        result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT, timeout=timeout)
    if result.returncode:
        raise RuntimeError(f"QA preparation failed; see {log}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--runtime-acceptance", type=Path, required=True)
    parser.add_argument("--compositor-package", type=Path, required=True)
    parser.add_argument("--wlroots-package", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--bits", type=int, choices=(32, 64), nargs="+", default=[32, 64])
    parser.add_argument("--repeats", type=int, choices=range(1, 11), default=2)
    parser.add_argument("--owner", choices=("mapped", "unmapped"), default="mapped")
    parser.add_argument("--baseline", action="store_true", help="Observe old stacking; not positive acceptance")
    parser.add_argument("--trace-wayland", action="store_true")
    parser.add_argument("--rounded-frames", action="store_true", help="Require actual Wine main/tool rounded corners")
    parser.add_argument("--verify-library-dependency", action="store_true", help="Require rejection of the compositor alone before installing its matching native library")
    args = parser.parse_args()
    if args.verify_library_dependency and not args.wlroots_package:
        parser.error("Dependency rejection needs a matching native wlroots package")
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    runtime_path = args.runtime_acceptance.resolve(strict=True) / "acceptance.json"
    runtime = json.loads(runtime_path.read_text())
    if runtime.get("accepted") is not True or not re.fullmatch(r"sha256:[a-f0-9]{64}", runtime.get("installed_image", "")):
        raise ValueError("A successful captured native runtime acceptance is required")
    base = json.loads(subprocess.check_output(["docker", "image", "inspect", runtime["installed_image"]], text=True))[0]
    if base["Os"] != "linux" or base["Architecture"] != "amd64":
        raise ValueError("Use a native Linux amd64 runtime")
    context = output / "image"
    context.mkdir()
    actors = output / "actors"
    actors.mkdir()
    fixture = args.source.resolve(strict=True) / "integrations/win32/tests"
    shutil.copyfile(fixture / "palette-acceptance.py", actors / "palette-acceptance.py")
    shutil.copyfile(fixture / "palette-probe.c", context / "palette-probe.c")
    shutil.copyfile(runtime_path, output / "runtime-acceptance.json")
    native = []
    selected = [(args.compositor_package, "labwc")]
    if args.wlroots_package:
        library = json.loads((args.wlroots_package / "manifest.json").read_text())
        names = [name for name in library["binaries"] if re.fullmatch(r"libwlroots-0[.](18|19)", name)]
        if len(names) != 1:
            raise ValueError("One supported native wlroots runtime is required")
        selected.append((args.wlroots_package, names[0]))
        # Preserve an existing native SDK instead of leaving its exact runtime
        # dependency broken. Runtime-only images do not gain a new SDK.
        if names[0] + '-dev' in library['binaries']:
            selected.append((args.wlroots_package, names[0] + '-dev'))
    for folder, package_name in selected:
        folder = folder.resolve(strict=True)
        spec = json.loads((folder / "manifest.json").read_text())
        if spec.get("status") != "success" or spec.get("kind") != "source-package":
            raise ValueError("Use successful native source-package output")
        name = spec["binaries"][package_name]
        if not re.fullmatch(r"[A-Za-z0-9+_.~%-]+[.]deb", name):
            raise ValueError("Unsafe native package filename")
        path = folder / name
        artifact = next(row for row in spec["artifacts"] if row["file"] == name and row.get("package") == package_name)
        if artifact.get("architecture", spec.get("architecture", "amd64")) != "amd64" or path.is_symlink() or path.stat().st_size != artifact["bytes"] or digest(path) != artifact["sha256"]:
            raise ValueError("Changed or non-native package artifact")
        shutil.copyfile(path, context / name)
        native.append({"manifest_sha256": digest(folder / "manifest.json"), "distribution": spec["environment"]["distribution"], "artifact": artifact, "version": spec["version"], "only_if_installed": package_name.endswith('-dev')})
    (context / "native.json").write_text(json.dumps(native, indent=2) + "\n")
    (context / "dependency-policy.json").write_text(json.dumps({"check": args.verify_library_dependency}) + "\n")
    shutil.copyfile(Path(__file__).with_name("win32-palette-install.py"), context / "install-native.py")
    identity = uuid.uuid4().hex
    captured = "karyo-palette-captured:" + identity
    subprocess.run(["docker", "image", "tag", base["Id"], captured], check=True)
    lines = ["ARG BASE=karyo-palette-captured:unset", "FROM ${BASE}", "USER root", "COPY *.deb native.json dependency-policy.json install-native.py /tmp/karyo-palette-native/", "RUN python3 -I -B /tmp/karyo-palette-native/install-native.py", "COPY palette-probe.c /usr/share/karyo-qa/"]
    for bits in sorted(set(args.bits)):
        compiler = "i686" if bits == 32 else "x86_64"
        suffix = "32" if bits == 32 else ""
        lines.append(f"RUN {compiler}-w64-mingw32-gcc -std=c11 -Wall -Wextra -Werror -municode /usr/share/karyo-qa/palette-probe.c -lgdi32 -o /usr/share/karyo-qa/palette-probe{suffix}.exe")
    lines.append("USER 1001:1001")
    (context / "Dockerfile").write_text("\n".join(lines) + "\n")
    tag = "karyo-palette-acceptance:" + identity
    execute(["docker", "build", "--network", "none", "--build-arg", "BASE=" + captured, "-t", tag, str(context)], output / "build.log", 240)
    image = subprocess.check_output(["docker", "image", "inspect", tag, "--format", "{{.Id}}"], text=True).strip()
    report = {"runtime_acceptance_sha256": digest(runtime_path), "base_image": base["Id"], "installed_image": image, "native": native, "owner": args.owner, "baseline": args.baseline, "actor_sha256": digest(actors / "palette-acceptance.py"), "producer_source_sha256": digest(context / "palette-probe.c"), "cases": []}
    if args.verify_library_dependency:
        command = ["docker", "run", "--rm", "--network", "none", "--read-only", "--cap-drop", "ALL", "--security-opt", "no-new-privileges", "--user", "1001:1001", image, "python3", "-I", "-c", "from pathlib import Path; print(Path('/usr/share/karyo-qa/owner-dependency.json').read_text())"]
        report["owner_dependency"] = json.loads(subprocess.check_output(command, text=True))
        assert report["owner_dependency"]["accepted"]
    (output / "progress.json").write_text(json.dumps(report, indent=2) + "\n")
    for iteration in range(args.repeats):
        for bits in sorted(set(args.bits)):
            label = f"pe{bits}-{iteration}"
            name = "karyo-palette-" + identity + "-" + label
            command = ["docker", "run", "--rm", "--name", name, "--network", "none", "--read-only", "--cap-drop", "ALL", "--security-opt", "no-new-privileges", "--user", "1001:1001", "--tmpfs", "/tmp:rw,exec,nosuid,nodev,mode=1777", "--tmpfs", "/home/win32qa:rw,exec,nosuid,nodev,uid=1001,gid=1001,mode=700", "--mount", "type=bind,src=" + str(actors) + ",dst=/actors,readonly", "--mount", "type=bind,src=" + str(output) + ",dst=/output", image, "dbus-run-session", "--", "python3", "-I", "-B", "/actors/palette-acceptance.py", "--output", "/output/" + label, "--bits", str(bits)]
            for flag, enabled in [("--mapped-owner", args.owner == "mapped"), ("--baseline", args.baseline), ("--trace-wayland", args.trace_wayland), ("--rounded-frames", args.rounded_frames)]:
                if enabled:
                    command.append(flag)
            try:
                with (output / (label + ".log")).open("wb") as stream:
                    result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT, timeout=240)
                code = result.returncode
            except subprocess.TimeoutExpired:
                code = 124
            finally:
                subprocess.run(["docker", "rm", "-f", name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=20)
            report["cases"].append({"stage": label, "returncode": code})
            (output / "progress.json").write_text(json.dumps(report, indent=2) + "\n")
            print(label, code, flush=True)
    report["accepted"] = all(row["returncode"] == 0 for row in report["cases"])
    report["build_inputs"] = {p.name: digest(p) for p in context.iterdir() if p.is_file() and p.suffix != ".deb"}
    if not report["accepted"]:
        raise RuntimeError("Real Wine palette acceptance failed; inspect preserved case logs")
    (output / ("baseline.json" if args.baseline else "acceptance.json")).write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
