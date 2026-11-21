#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Build real native single/set fixtures and reject colliding component payloads."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import uuid

ROOT = Path(__file__).resolve().parents[2]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve() / ("acceptance-" + uuid.uuid4().hex[:8])
    output.mkdir(parents=True)
    environment = dict(os.environ, PYTHONPATH=str(ROOT / "src"))
    with tempfile.TemporaryDirectory(prefix="karyo-set-") as temporary:
        temporary = Path(temporary)
        source = temporary / "source"
        shutil.copytree(ROOT / "tests/fixtures/runtime", source)
        hooks = temporary / "hooks"
        hooks.mkdir()
        git = ["git", "-C", str(source), "-c", "user.name=Builder QA",
               "-c", "user.email=qa@openkaryon.invalid", "-c", "core.hooksPath=" + str(hooks)]
        subprocess.run(git + ["init", "-q", "--initial-branch=main", "--template=" + str(hooks)], check=True)
        subprocess.run(git + ["add", "."], check=True)
        subprocess.run(git + ["commit", "--no-gpg-sign", "-qm", "Disposable native package-set fixture",
            "-m", "Keep a Qt Core executable and independent documentation component in one test source snapshot.",
            "-m", "Exercise native dependencies, conffiles and payload ownership without importing workstation data.",
            "-m", "Co-Authored-By: Codex <noreply@openai.com>"], check=True)
        revision = subprocess.check_output(git + ["rev-parse", "HEAD"], text=True).strip()
        # Recipes select '.' in the copied fixture repository; production recipes stay unchanged.
        recipes = []
        for name in ("runtime", "runtime-doc"):
            recipe = json.loads((ROOT / f"tests/fixtures/{name}.json").read_text())
            recipe["source"] = {"path": str(source)}
            recipe["build"]["directory"] = "."
            path = temporary / (name + ".json")
            path.write_text(json.dumps(recipe), encoding="utf-8")
            recipes.append(path)

        def build(stage, paths, label, success=True):
            target = output / label
            with (output / (label + ".log")).open("wb") as log:
                result = subprocess.run([sys.executable, "-m", "karyo_builder", stage,
                    *map(str, paths), "--image", args.image, "--output", str(target)],
                    cwd=ROOT, env=environment, stdout=log, stderr=subprocess.STDOUT)
            if success:
                assert result.returncode == 0, (label, output)
                published = [p for p in target.iterdir() if not p.name.startswith(".")]
                assert len(published) == 1, published
                return published[0]
            assert result.returncode != 0, label
            assert not [p for p in target.iterdir() if not p.name.startswith(".")], target
            failures = list(target.glob(".failed-*"))
            assert len(failures) == 1
            assert "Package payload collision" in (failures[0] / "build.log").read_text()

        single = build("package", [recipes[0]], "single")
        single_manifest = json.loads((single / "manifest.json").read_text())
        assert single_manifest["source"]["revision"] == revision
        assert digest(single / single_manifest["artifact"]["file"]) == single_manifest["artifact"]["sha256"]
        batch = build("package-set", recipes, "set")
        manifest = json.loads((batch / "manifest.json").read_text())
        assert manifest["kind"] == "package-set" and manifest["source"]["revision"] == revision
        assert len(manifest["packages"]) == 2
        for record in manifest["packages"]:
            folder = batch / record["directory"]
            assert digest(folder / "manifest.json") == record["manifest_sha256"]
            item = json.loads((folder / "manifest.json").read_text())
            assert item["source"]["revision"] == revision
            assert digest(folder / item["artifact"]["file"]) == item["artifact"]["sha256"]
            assert item["shared_build_log"]["sha256"] == digest(batch / "build.log")
            if record["package"].endswith("-doc"):
                assert item["dependencies"] == []
            else:
                assert any(dep.startswith("libqt6core") for dep in item["dependencies"])
        log = (batch / "build.log").read_text()
        assert log.count("+ cmake --build ") == 1
        assert log.count("+ ctest ") == 1
        inspector = r"""
import json,pathlib,subprocess,tempfile
root=pathlib.Path('/input')
manifest=json.loads((root/'manifest.json').read_text())
with tempfile.TemporaryDirectory() as tmp:
 for record in manifest['packages']:
  folder=root/record['directory']; item=json.loads((folder/'manifest.json').read_text())
  archive=folder/item['artifact']['file']; control=pathlib.Path(tmp)/record['package']
  subprocess.run(['dpkg-deb','-e',str(archive),str(control)],check=True)
  if record['package'].endswith('-doc'):
   assert not (control/'conffiles').exists()
  else:
   assert '/etc/karyo-builder-runtime-check/example.conf' in (control/'conffiles').read_text()
   installed=pathlib.Path(tmp)/'installed'
   subprocess.run(['dpkg-deb','-x',str(archive),str(installed)],check=True)
   version=subprocess.check_output([str(installed/'usr/bin/runtime-fixture')],text=True).strip()
   assert version.startswith('6.'),version
print('PASS native ELF execution, per-package conffiles and metadata')
"""
        subprocess.run(["docker", "run", "--rm", "--network=none", "--read-only", "--tmpfs", "/tmp:rw,exec,mode=1777",
            "--user", "65534:65534", "--cap-drop=ALL", "--security-opt=no-new-privileges",
            "--mount", "type=bind,source=" + str(batch) + ",target=/input,readonly", "--entrypoint", "python3",
            manifest["environment"]["image_id"], "-c", inspector], check=True)
        collision = json.loads(recipes[1].read_text())
        collision["build"]["component"] = "runtime"
        bad = temporary / "collision.json"
        bad.write_text(json.dumps(collision), encoding="utf-8")
        build("package-set", [recipes[0], bad], "collision", success=False)
        report = {"image": args.image, "revision": revision, "single": str(single),
                  "package_set": str(batch), "checks": "single/set/native/collision passed"}
        (output / "acceptance.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print("PASS package-set acceptance:", output)


if __name__ == "__main__":
    main()
