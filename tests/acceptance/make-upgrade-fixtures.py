#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Create acceptance-only package upgrades with unchanged executable payloads."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile


def run(*args):
    return subprocess.check_output(args, text=True).strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--version", default="0.1.0-2")
    args = parser.parse_args()
    run("dpkg", "--validate-version", args.version)
    packages = sorted(args.source.glob("karyo-*.deb"))
    if not packages:
        raise ValueError("No Karyo runtime packages supplied")
    names = {run("dpkg-deb", "-f", str(path), "Package") for path in packages}
    args.output.mkdir(parents=True, exist_ok=True)
    records = []
    for package in packages:
        name = run("dpkg-deb", "-f", str(package), "Package")
        original_version = run("dpkg-deb", "-f", str(package), "Version")
        architecture = run("dpkg-deb", "-f", str(package), "Architecture")
        subprocess.run(["dpkg", "--compare-versions", args.version, "gt", original_version], check=True)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            run("dpkg-deb", "-R", str(package), str(root))
            control = root / "DEBIAN/control"
            text = re.sub(r"(?m)^Version: .+$", "Version: " + args.version, control.read_text())
            text = re.sub(r"(karyo-[a-z0-9+.-]+) \(= [^)]+\)",
                          lambda m: m[1] + " (= " + args.version + ")" if m[1] in names else m[0], text)
            control.write_text(text)
            policy = root / "etc/pam.d/karyo-lock"
            if policy.exists():
                with policy.open("a") as stream:
                    stream.write("\n# Acceptance fixture: changed shipped default, same PAM behavior.\n")
            checksums = root / "DEBIAN/md5sums"
            if policy.exists() and checksums.exists():
                checksum = hashlib.md5(policy.read_bytes(), usedforsecurity=False).hexdigest()
                checksums.write_text(re.sub(r"(?m)^\S+  etc/pam.d/karyo-lock$",
                                           checksum + "  etc/pam.d/karyo-lock", checksums.read_text()))
            artifact = args.output / f"{name}_{args.version}_{architecture}.deb"
            run("dpkg-deb", "--build", "--root-owner-group", str(root), str(artifact))
        records.append({"package": name, "original_version": original_version,
                        "fixture_version": args.version,
                        "original_sha256": hashlib.sha256(package.read_bytes()).hexdigest(),
                        "fixture_sha256": hashlib.sha256(artifact.read_bytes()).hexdigest()})
    (args.output / "fixtures.json").write_text(json.dumps(records, indent=2) + "\n")
    print(f"Created {len(records)} acceptance-only upgrades; executable payloads unchanged")


if __name__ == "__main__":
    main()
