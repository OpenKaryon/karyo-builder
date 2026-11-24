#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Positive native package modes: default, selected tests and explicit build-only."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    output = Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    fixture = root / "tests/fixtures/runtime.json"
    documentation = root / "tests/fixtures/runtime-doc.json"
    cases = {}
    for mode, flags in (("default", []), ("selected", ["--test-regex", "^runtime-fixture$"]),
                        ("build-only", ["--build-only"])):
        target = output / mode
        batch = mode == "build-only"
        command = [sys.executable, "-B", "-m", "karyo_builder",
                   "package-set" if batch else "package", str(fixture)]
        if batch:
            command.append(str(documentation))
        command += ["--source", str(root), "--output", str(target),
                    "--image", args.image, "--jobs", "2", *flags]
        with (output / (mode + ".log")).open("xb") as log:
            result = subprocess.run(command, cwd=root,
                env=dict(os.environ, PYTHONPATH=str(root / "src")), stdout=log, stderr=subprocess.STDOUT)
        result.check_returncode()
        folders = [p for p in target.iterdir() if p.is_dir() and not p.name.startswith(".")]
        assert len(folders) == 1
        folder = folders[0]
        manifest = json.loads((folder / "manifest.json").read_bytes())
        log = (folder / "build.log").read_text()
        assert log.count("+ cmake --build ") == 1
        assert log.count("+ ctest ") == (0 if batch else 1)
        assert ("-DBUILD_TESTING=OFF" in log) == batch
        records = manifest["packages"] if batch else [{"directory": "."}]
        items = []
        for row in records:
            location = folder / row["directory"]
            item = json.loads((location / "manifest.json").read_bytes())
            if batch:
                assert digest(location / "manifest.json") == row["manifest_sha256"]
                assert item["shared_build_log"]["sha256"] == digest(folder / "build.log")
            expected = {"ctest": "not-run" if batch else "passed",
                        "ctest_scope": "none" if batch else ("selected" if mode == "selected" else "all"),
                        "ctest_regex": "^runtime-fixture$" if mode == "selected" else None,
                        "dpkg_deb": "passed"}
            assert item["validation"] == expected
            assert item["runner_sha256"] == digest(root / "src/karyo_builder/container.py")
            artifact = location / item["artifact"]["file"]
            assert artifact.stat().st_size == item["artifact"]["bytes"]
            assert digest(artifact) == item["artifact"]["sha256"]
            dependencies = item["dependencies"]
            if item["recipe"]["resolved"]["package"]["name"].endswith("-doc"):
                assert dependencies == []
            else:
                assert any(value.startswith("libqt6core") for value in dependencies)
            items.append({"directory": row["directory"], "artifact": item["artifact"],
                          "validation": expected, "dependencies": dependencies})
        cases[mode] = {"directory": str(folder), "manifest_sha256": digest(folder / "manifest.json"),
                       "items": items}

    # Execute the actual build-only ELF normally; this is separate runtime evidence.
    batch = Path(cases["build-only"]["directory"])
    image = json.loads((batch / "manifest.json").read_bytes())["environment"]["image_id"]
    code = r'''import json,pathlib,subprocess,tempfile
root=pathlib.Path('/input');manifest=json.loads((root/'manifest.json').read_bytes())
with tempfile.TemporaryDirectory() as temporary:
 for row in manifest['packages']:
  folder=root/row['directory'];item=json.loads((folder/'manifest.json').read_bytes())
  control=pathlib.Path(temporary)/row['package'];payload=control/'payload'
  subprocess.run(['dpkg-deb','--control',str(folder/item['artifact']['file']),str(control)],check=True)
  subprocess.run(['dpkg-deb','--extract',str(folder/item['artifact']['file']),str(payload)],check=True)
  if row['package'].endswith('-doc'):
   assert not (control/'conffiles').exists()
   assert (payload/'usr/share/doc/karyo-builder-runtime-doc/example.conf').is_file()
  else:
   assert '/etc/karyo-builder-runtime-check/example.conf' in (control/'conffiles').read_text()
   version=subprocess.check_output([str(payload/'usr/bin/runtime-fixture')],text=True).strip()
   assert version.startswith('6.'),version
print('Ordinary native ELF execution and per-component conffiles passed')
'''
    command = ["docker", "run", "--rm", "--network=none", "--read-only",
               "--user=65534:65534", "--cap-drop=ALL", "--security-opt=no-new-privileges",
               "--tmpfs", "/tmp:rw,exec,size=128m,mode=1777",
               "--mount", "type=bind,source=" + str(batch) + ",target=/input,readonly",
               "--entrypoint", "python3", image, "-c", code]
    with (output / "native-execution.log").open("xb") as log:
        result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT)
    result.check_returncode()
    record = {"image_id": image, "cases": cases, "native_build_only_ELF_executed": True,
              "ordinary_positive_only": True, "security_or_shared_unit_suites_executed": False}
    (output / "result.json").write_text(json.dumps(record, indent=2) + "\n")
    print("PASS ordinary package validation modes: " + str(output))


if __name__ == "__main__":
    main()
