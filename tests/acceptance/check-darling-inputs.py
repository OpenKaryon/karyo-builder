#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Join real pinned source, Swift recovery, patch and native SDK evidence."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def equivalent_patch_results(first, second):
    # Native distributions legitimately ship different quilt/patch versions.
    # Preserve those in each receipt; compare the complete source/result proof.
    tools = {"gnu_patch_version", "quilt_version"}
    for record in (first, second):
        if not all(isinstance(record.get(key), str) and record[key] for key in tools):
            return False
    return ({key: value for key, value in first.items() if key not in tools}
            == {key: value for key, value in second.items() if key not in tools})


def digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def bind(path, target, readonly=True):
    path = str(Path(path).resolve(strict=True))
    if "," in path:
        raise ValueError("Docker bind paths cannot contain commas")
    return "type=bind,source=" + path + ",target=" + target + (",readonly" if readonly else "")


def image(reference):
    data = json.loads(subprocess.check_output(["docker", "image", "inspect", reference], text=True))[0]
    if data.get("Os") != "linux" or data.get("Architecture") != "amd64" or not data.get("Id", "").startswith("sha256:"):
        raise ValueError("A local immutable Linux amd64 SDK image is required")
    return data["Id"]


def check(args):
    inventory, complete, recipe, archive = (Path(value).resolve(strict=True)
        for value in (args.inventory, args.complete, args.de_source, args.archive))
    recipe = recipe / "integrations/macos/runtime"
    source, ready = read(inventory / "manifest.json"), read(complete / "manifest.json")
    if source.get("build_ready") is not False or ready.get("build_ready") is not True:
        raise ValueError("Expected an unresolved inventory and a fully materialized snapshot")
    for key in ("source", "modules", "source_date_epoch", "members", "external_symlinks", "recipe_sha256", "exporter_sha256"):
        if source.get(key) != ready.get(key):
            raise ValueError("Materialization changed source identity: " + key)
    expected = [{k: v for k, v in item.items() if k != "materialized"} for item in source["lfs"]]
    actual = [{k: v for k, v in item.items() if k != "materialized"} for item in ready["lfs"]]
    if len(expected) != 44 or actual != expected or not all(item["materialized"] for item in ready["lfs"]):
        raise ValueError("Materialized Swift identities differ from the complete inventory")
    expected_patches = len(read(recipe / "patches/series.json")["patches"])
    if not 21 <= expected_patches <= 64:
        raise ValueError("Unexpected reviewed patch count")
    output = Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    actor = Path(__file__).with_name("darling-sdk-smoke.py")
    results = {}
    for base, reference in (("debian", args.debian_image), ("ubuntu", args.ubuntu_image)):
        image_id = image(reference)
        folder = output / base
        folder.mkdir()
        common = ["docker", "run", "--rm", "--network=none", "--read-only", "--cpus=2", "--memory=2g",
                  "--pids-limit=128", "--cap-drop=ALL", "--security-opt=no-new-privileges", "--user=65534:65534",
                  "--tmpfs", "/tmp:rw,exec,nosuid,nodev,size=256m,mode=1777", "--env", "HOME=/tmp",
                  "--mount", bind(recipe, "/recipe"), "--mount", bind(inventory, "/inventory"),
                  "--mount", bind(complete, "/complete"), "--mount", bind(archive, "/archive.deb"),
                  "--mount", bind(actor, "/sdk.py"), "--mount", bind(folder, "/output", False),
                  "--entrypoint", "python3", image_id, "-B"]
        def run(label, command):
            log = folder / (label + ".log")
            with log.open("wb") as stream:
                result = subprocess.run(common + command, stdout=stream, stderr=subprocess.STDOUT)
            if result.returncode:
                raise ValueError(base + " " + label + " failed; see " + str(log))
            return log
        print("Checking pinned Darling inputs on " + base, flush=True)
        sdk = read(run("sdk", ["/sdk.py"]))
        if sdk["distribution"]["ID"] != base:
            raise ValueError("SDK distribution differs from its selected native base")
        if not args.source_only:
            run("unit", ["-m", "unittest", "discover", "-s", "/recipe/tests", "-v"])
        run("swift", ["/recipe/prepare_swift.py", "/inventory", "--archive", "/archive.deb",
                      "--objects", "/output/objects", "--output", "/output/swift-provenance"])
        run("patches", ["/recipe/verify_patches.py", "/complete", "--output", "/output/patch-stack.json"])
        swift, patches = read(folder / "swift-provenance/provenance.json"), read(folder / "patch-stack.json")
        if (swift["status"] != "verified" or swift["native_linux_binaries"] or swift["compiled_from_source"]
                or patches["status"] != "verified" or patches["source_mutated"] or patches.get("quilt_zero_fuzz") is not True
                or len(patches["forward"]) != expected_patches or len(patches["reverse"]) != expected_patches):
            raise ValueError("Incomplete native source preparation evidence")
        results[base] = {"image_id": image_id, "sdk": sdk, "swift": swift, "patches": patches,
                         "logs": {path.name: digest(path) for path in sorted(folder.glob("*.log"))}}
    if results["debian"]["swift"] != results["ubuntu"]["swift"] or not equivalent_patch_results(results["debian"]["patches"], results["ubuntu"]["patches"]):
        raise ValueError("Native bases disagree about fixed runtime inputs")
    record = {"schema": 1, "kind": "darling-source-preparation", "status": "verified",
              "inventory": {"manifest_sha256": digest(inventory / "manifest.json"), "archive": source["archive"]},
              "complete": {"manifest_sha256": digest(complete / "manifest.json"), "archive": ready["archive"],
                           "build_ready": True, "modules": len(ready["modules"]), "members": ready["members"]},
              "native": results, "driver_sha256": digest(Path(__file__)),
              "unit_tests_executed": not args.source_only,
              "engine_compiled": False, "engine_installed": False, "mac_application_executed": False}
    (output / "acceptance.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print("Verified source preparation on both bases: " + str(output), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("inventory", "complete", "de-source", "archive", "output", "debian-image", "ubuntu-image"):
        parser.add_argument("--" + name, required=True)
    parser.add_argument("--source-only", action="store_true",
                        help="Verify native SDK, Swift inputs and patch application without running the unit suite")
    try:
        check(parser.parse_args())
        return 0
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print("Darling input acceptance: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
