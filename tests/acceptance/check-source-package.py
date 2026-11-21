#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Exercise real DSC extraction, ordered patches, upstream tests and native ELF."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from karyo_builder.source_recipe import source_headers


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", required=True)
    parser.add_argument("--distribution", choices=("trixie", "resolute"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve() / ("acceptance-" + uuid.uuid4().hex[:8])
    tree = output / "work/karyo-source-fixture-1.0"
    tree.mkdir(parents=True)
    files = {
        "program.c": '#include <stdio.h>\nint main(void) { puts("source-fixture one"); return 0; }\n',
        "Makefile": ("all: program\nprogram: program.c\n\t$(CC) $(CPPFLAGS) $(CFLAGS) $(LDFLAGS) -o $@ $<\n"
                     "check: program\n\t./program\n\t@echo UPSTREAM-CHECK-RAN\n"
                     "\t@echo 'upstream checks ran' > upstream-tested\n"
                     "install:\n\tinstall -Dm755 program $(DESTDIR)/usr/bin/karyo-source-fixture\n"
                     "\tinstall -Dm644 upstream-tested $(DESTDIR)/usr/share/karyo-source-fixture/test-proof\n"
                     "clean:\n\trm -f program upstream-tested\n"),
        "debian/control": ("Source: karyo-source-fixture\nSection: devel\nPriority: optional\n"
            "Maintainer: Builder QA <qa@openkaryon.invalid>\n"
            "Build-Depends: debhelper-compat (= 13), gcc, make\nStandards-Version: 4.6.2\n"
            "Rules-Requires-Root: no\n\nPackage: karyo-source-fixture\nArchitecture: any\n"
            "Depends: @D@{shlibs:Depends}, @D@{misc:Depends}\nDescription: Public source package fixture\n"
            " Exercises ordered patching and upstream checks.\n"),
        "debian/changelog": ("karyo-source-fixture (1.0-1) unstable; urgency=medium\n\n"
            "  * Public disposable fixture.\n\n -- Builder QA <qa@openkaryon.invalid>  "
            "Tue, 14 Nov 2023 22:13:20 +0000\n"),
        "debian/rules": "#!/usr/bin/make -f\n%:\n\tdh $@\n",
        "debian/source/format": "3.0 (quilt)\n",
        "debian/copyright": ("Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/\n"
            "Upstream-Name: karyo-source-fixture\nSource: Public QA fixture\n\n"
            "Files: *\nCopyright: 2026 Karyo Developers\nLicense: GPL-3+\n"
            " See /usr/share/common-licenses/GPL-3.\n"),
    }
    for name, content in files.items():
        path = tree / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content.replace("@D@", chr(36)).encode())
    shutil.copyfile(ROOT / "LICENSE", tree / "LICENSE")
    prep = r"""
from pathlib import Path
import os,subprocess
work=Path('/fixture/work');tree=work/'karyo-source-fixture-1.0'
os.chmod(tree/'debian/rules',0o755)
subprocess.run(['tar','--sort=name','--mtime=@1700000000','--owner=0','--group=0',
 '--numeric-owner','--exclude=karyo-source-fixture-1.0/debian','-czf',
 'karyo-source-fixture_1.0.orig.tar.gz','karyo-source-fixture-1.0'],cwd=work,check=True)
subprocess.run(['dpkg-source','-b',str(tree)],cwd=work,check=True)
"""
    with (output / "prepare.log").open("wb") as log:
        subprocess.run(["docker", "run", "--rm", "--network=none", "--cap-drop=ALL",
            "--security-opt=no-new-privileges", "--mount",
            "type=bind,source=" + str(output) + ",target=/fixture", "--entrypoint", "python3",
            args.image, "-c", prep], stdout=log, stderr=subprocess.STDOUT, check=True)
    inputs = output / "inputs"
    inputs.mkdir()
    for path in (output / "work").iterdir():
        if path.is_file():
            shutil.copyfile(path, inputs / path.name)
    dsc = next(inputs.glob("*.dsc"))
    headers = source_headers(dsc.read_bytes())
    archives = [inputs / line.split()[2] for line in headers["Checksums-Sha256"].splitlines() if line.strip()]
    def entry(path):
        return {"path": path.name, "sha256": digest(path)}
    patches = []
    for before, after, name in (("one", "two", "first.patch"), ("two", "three", "second.patch")):
        path = inputs / name
        path.write_bytes(('--- a/program.c\n+++ b/program.c\n@@ -1,2 +1,2 @@\n'
            ' #include <stdio.h>\n-int main(void) { puts("source-fixture ' + before
            + '"); return 0; }\n+int main(void) { puts("source-fixture ' + after
            + '"); return 0; }\n').encode())
        patches.append(entry(path))
    recipe = {"schema": 1,
        "source": {"name": "karyo-source-fixture", "version": "1.0-1", "dsc": entry(dsc),
                   "archives": [entry(p) for p in archives]},
        "patches": patches,
        "build": {"revision": "qa1", "distribution": args.distribution,
            "maintainer": "Builder QA <qa@openkaryon.invalid>",
            "message": "Apply ordered public QA patches.", "binaries": ["karyo-source-fixture"],
            "source_date_epoch": 1700000001}}
    environment = dict(os.environ, PYTHONPATH=str(ROOT / "src"))
    def build(spec, label, success):
        path = inputs / (label + ".json")
        path.write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")
        target = output / label
        with (output / (label + ".log")).open("wb") as log:
            result = subprocess.run([sys.executable, "-m", "karyo_builder", "source-package", str(path),
                "--image", args.image, "--output", str(target)], cwd=ROOT, env=environment,
                stdout=log, stderr=subprocess.STDOUT)
        assert (result.returncode == 0) == success, (label, output)
        published = [p for p in target.iterdir() if not p.name.startswith(".")]
        if not success:
            assert not published
            failures = list(target.glob(".failed-source-*"))
            assert len(failures) == 1
            return failures[0]
        assert len(published) == 1
        return published[0]
    result = build(recipe, "valid", True)
    manifest = json.loads((result / "manifest.json").read_text())
    assert manifest["version"] == "1.0-1+qa1"
    assert manifest["environment"]["distribution"]["VERSION_CODENAME"] == args.distribution
    assert manifest["patch_order"] == ["karyo-001-first.patch", "karyo-002-second.patch"]
    for item in manifest["artifacts"]:
        assert digest(result / item["file"]) == item["sha256"]
    assert "UPSTREAM-CHECK-RAN" in (result / "build.log").read_text()
    inspector = r"""
import json,pathlib,subprocess,tempfile
root=pathlib.Path('/input');manifest=json.loads((root/'manifest.json').read_text())
archive=root/manifest['binaries']['karyo-source-fixture']
with tempfile.TemporaryDirectory() as tmp:
 subprocess.run(['dpkg-deb','-x',str(archive),tmp],check=True)
 installed=pathlib.Path(tmp)
 assert subprocess.check_output([str(installed/'usr/bin/karyo-source-fixture')],text=True).strip()=='source-fixture three'
 assert (installed/'usr/share/karyo-source-fixture/test-proof').read_text().strip()=='upstream checks ran'
print('PASS patched native ELF and executed upstream checks as UID65534')
"""
    with (output / "native.log").open("wb") as log:
        subprocess.run(["docker", "run", "--rm", "--network=none", "--read-only",
            "--tmpfs", "/tmp:rw,exec,mode=1777", "--user", "65534:65534", "--cap-drop=ALL",
            "--security-opt=no-new-privileges", "--mount",
            "type=bind,source=" + str(result) + ",target=/input,readonly", "--entrypoint", "python3",
            manifest["environment"]["image_id"], "-c", inspector], stdout=log,
            stderr=subprocess.STDOUT, check=True)
    reversed_recipe = json.loads(json.dumps(recipe))
    reversed_recipe["patches"].reverse()
    failed = build(reversed_recipe, "wrong-order", False)
    assert "FAILED" in (failed / "build.log").read_text() or "does not apply" in (failed / "build.log").read_text()
    wrong_base = json.loads(json.dumps(recipe))
    wrong_base["build"]["distribution"] = "resolute" if args.distribution == "trixie" else "trixie"
    failed = build(wrong_base, "wrong-base", False)
    assert "distribution do not match" in (failed / "build.log").read_text()
    (output / "acceptance.json").write_text(json.dumps({
        "image_id": manifest["environment"]["image_id"], "result": str(result),
        "checks": "DSC/ordered patches/upstream checks/native UID execution/failed patch/foreign base passed"
    }, indent=2) + "\n")
    print("PASS source-package acceptance:", output)


if __name__ == "__main__":
    main()
