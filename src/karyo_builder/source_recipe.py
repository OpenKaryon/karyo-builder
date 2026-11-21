# SPDX-License-Identifier: GPL-3.0-or-later
"""Capture a checksummed Debian quilt source and ordered downstream patches."""
from email.parser import Parser
import hashlib
import json
from pathlib import Path
import re
import shutil

from .recipe import fields, text


def source_headers(data):
    """Read control fields, including clearsigned DSCs; do not claim PGP verification."""
    value = data.decode("utf-8").replace("\r\n", "\n")
    if value.startswith("-----BEGIN PGP SIGNED MESSAGE-----"):
        _, separator, value = value.partition("\n\n")
        if not separator:
            raise ValueError("Invalid clearsigned source control file")
        value = value.split("\n-----BEGIN PGP SIGNATURE-----", 1)[0]
        value = "\n".join(line[2:] if line.startswith("- ") else line for line in value.splitlines())
    return Parser().parsestr(value)


def validate_recipe(recipe):
    fields(recipe, ("schema", "source", "patches", "build"), "source recipe")
    if type(recipe["schema"]) is not int or recipe["schema"] != 1:
        raise ValueError("Only source-package recipe schema 1 is supported")
    source = recipe["source"]
    fields(source, ("name", "version", "dsc", "archives"), "source")
    for key in ("name", "version"):
        text(source[key], "source." + key)
    if not re.fullmatch(r"[a-z0-9][a-z0-9+.-]+", source["name"]):
        raise ValueError("Invalid source package name")
    if not re.fullmatch(r"[0-9][A-Za-z0-9.+:~\-]*", source["version"]):
        raise ValueError("Invalid source package version")
    if not isinstance(source["archives"], list) or not source["archives"]:
        raise ValueError("Source archives must be a non-empty list")
    if not isinstance(recipe["patches"], list):
        raise ValueError("Patches must be an ordered list")
    for item in [source["dsc"], *source["archives"], *recipe["patches"]]:
        fields(item, ("path", "sha256"), "input file")
        text(item["path"], "input path")
        if not isinstance(item["sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", item["sha256"]):
            raise ValueError("Each input needs a lowercase SHA256")
    build = recipe["build"]
    fields(build, ("revision", "distribution", "maintainer", "message", "binaries",
                   "source_date_epoch"), "source build")
    for key in ("revision", "distribution", "maintainer", "message"):
        text(build[key], "build." + key)
    if not re.fullmatch(r"[a-z0-9][a-z0-9.+~]*", build["revision"]):
        raise ValueError("Invalid downstream revision suffix")
    if build["distribution"] not in {"trixie", "resolute"}:
        raise ValueError("Only trixie and resolute source targets are supported")
    if not re.fullmatch(r"[^<>]+ <[^<>\s@]+@[^<>\s@]+>", build["maintainer"]):
        raise ValueError("Maintainer must include a name and email")
    binaries = build["binaries"]
    if not isinstance(binaries, list) or not binaries or any(
            not isinstance(name, str) or not re.fullmatch(r"[a-z0-9][a-z0-9+.-]+", name)
            for name in binaries) or len(set(binaries)) != len(binaries):
        raise ValueError("Expected binaries must be distinct Debian package names")
    epoch = build["source_date_epoch"]
    if type(epoch) is not int or not 0 <= epoch <= 253402300799:
        raise ValueError("source_date_epoch must be supported non-negative Unix seconds")


def capture_recipe(path, destination):
    path = Path(path).resolve(strict=True)
    raw = path.read_bytes()
    recipe = json.loads(raw.decode("utf-8"))
    validate_recipe(recipe)
    destination = Path(destination)
    destination.mkdir()
    (destination / "original-recipe.json").write_bytes(raw)

    def capture(entries, group, suffix):
        folder = destination / group
        folder.mkdir(exist_ok=True)
        seen, result = set(), []
        for item in entries:
            source = path.parent / item["path"]
            if source.is_symlink() or not source.is_file():
                raise ValueError("Inputs must be ordinary files, not symlinks")
            name = source.name
            if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9.+~_%\-]*" + suffix, name):
                raise ValueError("Unsafe or unsupported input filename: " + name)
            if name in seen:
                raise ValueError("Input filenames must be distinct within each group")
            seen.add(name)
            target = folder / name
            with source.open("rb") as reader, target.open("xb") as writer:
                shutil.copyfileobj(reader, writer)
            with target.open("rb") as reader:
                digest = hashlib.file_digest(reader, "sha256").hexdigest()
            if digest != item["sha256"]:
                raise ValueError("Input SHA256 mismatch: " + name)
            result.append({"file": name, "sha256": digest, "bytes": target.stat().st_size})
        return result

    source = recipe["source"]
    captured_dsc = capture([source["dsc"]], "sources", r"\.dsc")[0]
    captured_archives = capture(source["archives"], "sources", r"\.tar\.(?:xz|gz|bz2|zst)")
    if captured_dsc["file"] in {item["file"] for item in captured_archives}:
        raise ValueError("Source control and archive names must be distinct")
    patches = capture(recipe["patches"], "patches", r"\.patch")
    headers = source_headers((destination / "sources" / captured_dsc["file"]).read_bytes())
    if any(len(headers.get_all(name, [])) != 1
           for name in ("Format", "Source", "Version", "Checksums-Sha256")):
        raise ValueError("DSC identity and checksum fields must appear exactly once")
    if headers.get("Format") != "3.0 (quilt)":
        raise ValueError("The source-package stage requires 3.0 (quilt)")
    if headers.get("Source") != source["name"] or headers.get("Version") != source["version"]:
        raise ValueError("DSC identity does not match the selected source")
    declared = {}
    for line in headers.get("Checksums-Sha256", "").splitlines():
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) != 3:
            raise ValueError("Invalid DSC SHA256 entry")
        digest, size, name = parts
        if name in declared or not size.isdecimal():
            raise ValueError("Duplicate or invalid DSC archive entry")
        declared[name] = (digest, int(size))
    actual = {item["file"]: (item["sha256"], item["bytes"]) for item in captured_archives}
    if declared != actual:
        raise ValueError("DSC archives must exactly match the captured names, sizes and SHA256s")
    resolved = {
        "schema": 1,
        "source": {"name": source["name"], "version": source["version"],
                   "dsc": captured_dsc, "archives": captured_archives},
        "patches": patches, "build": recipe["build"],
    }
    (destination / "source-recipe.json").write_text(
        json.dumps(resolved, indent=2) + "\n", encoding="utf-8")
    return resolved, hashlib.sha256(raw).hexdigest()
