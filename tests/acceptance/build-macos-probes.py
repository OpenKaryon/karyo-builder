#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Compile actual Mac CLI/Cocoa/Qt probes with a local external cross SDK."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import posixpath
import struct
import subprocess
import tarfile
import uuid


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def bind(path, target):
    text = str(path)
    if "," in text:
        raise ValueError("Docker bind paths cannot contain commas")
    return "type=bind,source=" + text + ",target=" + target


def inspect_archive(path, executables=None):
    if executables is None:
        executables = {"karyo-macos-loader-probe", "KaryoCocoaProbe.app/Contents/MacOS/KaryoCocoaProbe",
                       "KaryoQtProbe.app/Contents/MacOS/KaryoQtProbe"}
    found, seen, records = set(), set(), []
    with tarfile.open(path, "r:gz") as archive:
        for member in archive:
            name = member.name.removeprefix("./")
            if not name or name == ".":
                continue
            parts = PurePosixPath(name).parts
            if (name in seen or name.startswith("/") or "\\" in name or ".." in parts
                    or not (member.isdir() or member.isfile() or member.issym())
                    or PurePosixPath(name).as_posix() != name
                    or member.mode & 0o7000 or (not member.issym() and member.mode & 0o022)):
                raise ValueError("Unsafe Mac probe archive member: " + name)
            seen.add(name)
            record = {"path": name, "mode": member.mode}
            if member.issym():
                resolved = posixpath.normpath(posixpath.join(posixpath.dirname(name), member.linkname))
                if (member.linkname.startswith("/") or resolved in (".", "..")
                        or resolved.startswith("../") or "\\" in member.linkname
                        or resolved.split("/", 1)[0] != parts[0]):
                    raise ValueError("Escaping bundle link: " + name)
                record["symlink"] = member.linkname
            if member.isfile():
                stream = archive.extractfile(member)
                head = stream.read(16)
                value = hashlib.sha256(head)
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    value.update(block)
                record.update(sha256=value.hexdigest(), bytes=member.size)
                if name in executables:
                    if (len(head) != 16 or struct.unpack("<IIII", head)[:2] != (0xfeedfacf, 0x01000007)
                            or struct.unpack("<IIII", head)[3] != 2 or not member.mode & 0o111):
                        raise ValueError("Probe is not an executable Intel64 Mach-O: " + name)
                    found.add(name)
            records.append(record)
    if found != executables:
        raise ValueError("Required real Mac executables are missing: " + ", ".join(sorted(executables - found)))
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--de-source", required=True)
    parser.add_argument("--image", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--suite", choices=("applications", "cocoa-properties", "iosurface"), default="applications")
    args = parser.parse_args()
    source = Path(args.de_source).resolve(strict=True)
    standalone = args.suite != "applications"
    probes = source / "integrations/macos/tests" / (args.suite if standalone else "probes")
    files = sorted(probes.iterdir())
    if not files or any(not path.is_file() or path.is_symlink() for path in files):
        raise ValueError("Expected regular product-owned probe sources")
    image = json.loads(subprocess.check_output(["docker", "image", "inspect", args.image], text=True))[0]
    if image.get("Os") != "linux" or image.get("Architecture") != "amd64":
        raise ValueError("A local Linux amd64 cross SDK image is required")
    image_id = image["Id"]
    parent = Path(args.output).resolve()
    if parent.is_relative_to(probes):
        raise ValueError("Output must be outside probe sources")
    parent.mkdir(parents=True, exist_ok=True)
    output = parent / ("macos-probes-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8])
    output.mkdir()
    inputs = {path.name: digest(path) for path in files}
    revision = subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"], text=True).strip()
    dirty = bool(subprocess.check_output(["git", "-C", str(source), "status", "--porcelain", "--", str(probes)], text=True).strip())
    container = "karyo-macos-probes-" + uuid.uuid4().hex
    command = ["docker", "run", "--rm", "--name", container, "--network=none", "--read-only", "--cpus=2", "--memory=2g",
        "--pids-limit=256", "--cap-drop=ALL", "--security-opt=no-new-privileges", "--user=65534:65534",
        "--tmpfs", "/tmp:rw,exec,nosuid,nodev,size=768m,mode=1777", "--env", "HOME=/tmp",
        "--mount", bind(probes, "/input") + ",readonly", "--mount", bind(output, "/output"),
        "--entrypoint", "/bin/sh", image_id, "/input/build.sh"]
    inputs_record = {"source_revision": revision, "source_dirty": dirty, "inputs": inputs,
                     "toolchain_image": image_id, "driver_sha256": digest(Path(__file__))}
    (output / "inputs.json").write_text(json.dumps(inputs_record, indent=2) + "\n", encoding="utf-8")
    with (output / "build.log").open("wb") as log:
        try:
            result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, timeout=600)
        except subprocess.TimeoutExpired:
            subprocess.run(["docker", "rm", "--force", container], capture_output=True, timeout=30)
            raise
    if result.returncode:
        raise RuntimeError("Mac cross compilation failed; see " + str(output / "build.log"))
    executables = {"cocoa-properties": {"karyo-macos-window-properties-probe", "karyo-macos-menu-view-probe"},
                   "iosurface": {"karyo-macos-iosurface-matching", "karyo-macos-iosurface-probe", "karyo-macos-iosurface-lifecycle",
                                 "karyo-macos-iosurface-layer", "karyo-macos-iosurface-tree",
                                 "karyo-macos-iosurface-backing-view"}}.get(args.suite)
    members = inspect_archive(output / "probes.tar.gz", executables)
    if inputs != {path.name: digest(path) for path in files}:
        raise ValueError("Source inputs changed while building")
    log_names = ("build.log", "compiler-version.txt") if standalone else (
        "build.log", "qmake-query.txt", "compiler-version.txt")
    record = {"schema": 1, "kind": "real-macos-probes", "suite": args.suite,
        "target": "macos-x86_64", "compiled": True,
        "runtime_tested": False, "source_revision": revision, "source_dirty": dirty, "inputs": inputs,
        "toolchain_image": image_id, "driver_sha256": digest(Path(__file__)), "members": members,
        "archive": {"file": "probes.tar.gz", "sha256": digest(output / "probes.tar.gz")},
        "logs": {name: digest(output / name) for name in log_names}}
    (output / "manifest.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print("Compiled real Intel Mach-O probes; not yet runtime-tested: " + str(output))


if __name__ == "__main__":
    main()
