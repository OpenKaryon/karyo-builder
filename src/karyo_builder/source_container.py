# SPDX-License-Identifier: GPL-3.0-or-later
"""Native Debian quilt build runner; executed only in an isolated container."""
from datetime import datetime, timezone
from email.parser import Parser
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

from container import run, validate_target


def main():
    jobs = int(sys.argv[1])
    if not 1 <= jobs <= 8:
        raise ValueError("Invalid job count")
    spec = json.loads(Path("/input/source-recipe.json").read_text())
    source, build = spec["source"], spec["build"]
    distribution = validate_target(Path("/etc/os-release").read_text())
    if distribution["VERSION_CODENAME"] != build["distribution"]:
        raise ValueError("Source recipe and native build distribution do not match")
    output = Path("/output")
    (output / "distribution.json").write_text(json.dumps(distribution, indent=2) + "\n")
    query_format = "-f=" + chr(36) + "{binary:Package}=" + chr(36) + "{Version}\\n"
    packages = run(["dpkg-query", "-W", query_format],
                   text=True, stdout=subprocess.PIPE).stdout.splitlines()
    (output / "environment.json").write_text(json.dumps(sorted(packages), indent=2) + "\n")
    if run(["dpkg", "--print-architecture"], text=True, stdout=subprocess.PIPE).stdout.strip() != "amd64":
        raise ValueError("Source packages require native amd64")
    for group, entries in (("sources", [source["dsc"], *source["archives"]]), ("patches", spec["patches"])):
        for item in entries:
            path = Path("/input") / group / item["file"]
            with path.open("rb") as stream:
                digest = hashlib.file_digest(stream, "sha256").hexdigest()
            if digest != item["sha256"] or path.stat().st_size != item["bytes"]:
                raise ValueError("Captured input changed: " + item["file"])
    work = Path("/tmp/source-build")
    work.mkdir()
    Path("/tmp/home").mkdir(exist_ok=True)
    tree = work / "source"
    run(["dpkg-source", "--require-strong-checksums", "-x", Path("/input/sources") / source["dsc"]["file"], tree], cwd=work)
    def changelog_field(field):
        return run(["dpkg-parsechangelog", "-S", field], cwd=tree,
                   text=True, stdout=subprocess.PIPE).stdout.strip()
    if changelog_field("Source") != source["name"] or changelog_field("Version") != source["version"]:
        raise ValueError("Extracted source identity does not match recipe")
    patch_dir = tree / "debian/patches"
    patch_dir.mkdir(exist_ok=True)
    series = patch_dir / "series"
    previous = series.read_bytes() if series.exists() else b""
    names = []
    for index, item in enumerate(spec["patches"], 1):
        name = f"karyo-{index:03d}-{item['file']}"
        target = patch_dir / name
        if target.exists() or target.is_symlink():
            raise ValueError("Downstream patch already exists in source: " + name)
        shutil.copyfile(Path("/input/patches") / item["file"], target)
        names.append(name)
    if names:
        series.write_bytes(previous.rstrip(b"\n") + (b"\n" if previous else b"")
                           + ("\n".join(names) + "\n").encode())
        run(["quilt", "push", "-a"], cwd=tree,
            env=dict(os.environ, QUILT_PATCHES="debian/patches", QUILT_PATCH_OPTS="--fuzz=0"))
    version = source["version"] + "+" + build["revision"]
    run(["dpkg", "--validate-version", version])
    date = datetime.fromtimestamp(build["source_date_epoch"], timezone.utc).strftime(
        "%a, %d %b %Y %H:%M:%S +0000")
    entry = (f"{source['name']} ({version}) {build['distribution']}; urgency=medium\n\n"
             f"  * {build['message']}\n\n -- {build['maintainer']}  {date}\n\n")
    changelog = tree / "debian/changelog"
    changelog.write_bytes(entry.encode() + changelog.read_bytes())
    run(["dpkg-buildpackage", "-b", "-us", "-uc", "-rfakeroot", f"-j{jobs}"], cwd=tree,
        env=dict(os.environ, DEB_BUILD_OPTIONS=f"parallel={jobs}",
                 SOURCE_DATE_EPOCH=str(build["source_date_epoch"])))
    artifacts, binaries = [], {}
    for path in sorted(work.iterdir()):
        if path.suffix not in {".deb", ".ddeb", ".buildinfo", ".changes"} or not path.is_file():
            continue
        if path.is_symlink():
            raise ValueError("Build artifacts must not be symlinks")
        target = output / path.name
        shutil.copyfile(path, target)
        with target.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        record = {"file": path.name, "sha256": digest, "bytes": target.stat().st_size}
        if path.suffix in {".deb", ".ddeb"}:
            control = Parser().parsestr(run(["dpkg-deb", "--field", path],
                text=True, stdout=subprocess.PIPE).stdout)
            name = control.get("Package")
            if control.get("Version") != version or control.get("Architecture") not in {"amd64", "all"}:
                raise ValueError("Unexpected binary package version/architecture")
            if name in binaries:
                raise ValueError("Duplicate binary package: " + name)
            binaries[name] = record["file"]
            record["package"] = name
        artifacts.append(record)
    if not set(build["binaries"]).issubset(binaries):
        raise ValueError("Build did not produce all declared binary packages")
    if not any(item["file"].endswith(".buildinfo") for item in artifacts) or not any(
            item["file"].endswith(".changes") for item in artifacts):
        raise ValueError("Build is missing its native buildinfo or changes record")
    (output / "result.json").write_text(json.dumps({
        "version": version, "binaries": binaries, "artifacts": artifacts,
        "patch_order": names}, indent=2) + "\n")


if __name__ == "__main__":
    main()
