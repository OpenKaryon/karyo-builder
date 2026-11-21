# SPDX-License-Identifier: GPL-3.0-or-later
"""Version 1 of the native Debian package-stage input contract."""
import json
import re
from pathlib import Path


def fields(value, expected, location):
    if not isinstance(value, dict) or set(value) != set(expected):
        raise ValueError(f"{location} must contain exactly: {', '.join(expected)}")


def text(value, location):
    if not isinstance(value, str) or not value.strip() or any(
        character in value for character in "\r\n\0"
    ):
        raise ValueError(f"{location} must be non-empty text on one line")
    return value


def load_recipe(path):
    path = Path(path).resolve(strict=True)
    return parse_recipe(path.read_bytes(), path.parent)


def parse_recipe(data, directory):
    """Validate an already captured UTF-8 recipe against its original directory."""
    recipe = json.loads(data.decode("utf-8"))
    fields(recipe, ("schema", "source", "package", "build"), "recipe")
    if type(recipe["schema"]) is not int or recipe["schema"] != 1:
        raise ValueError("Only package recipe schema 1 is supported")
    source = recipe["source"]
    if isinstance(source, dict):
        source.setdefault("revision", "HEAD")
    fields(source, ("path", "revision"), "source")
    text(source["path"], "source.path")
    text(source["revision"], "source.revision")
    source["path"] = str((Path(directory) / source["path"]).resolve())
    package = recipe["package"]
    fields(package, ("name", "version", "architecture", "maintainer", "description",
                     "section", "depends"), "package")
    for key in ("name", "version", "architecture", "maintainer", "description", "section"):
        text(package[key], f"package.{key}")
    if not re.fullmatch(r"[a-z0-9][a-z0-9+.-]+", package["name"]):
        raise ValueError("Invalid Debian package name")
    if not re.fullmatch(r"[0-9][A-Za-z0-9.+:~\-]*", package["version"]):
        raise ValueError("Invalid Debian package version")
    if package["architecture"] != "amd64":
        raise ValueError("The first package stage supports amd64")
    if not re.fullmatch(r"[a-z0-9][a-z0-9+./-]*", package["section"]):
        raise ValueError("Invalid Debian section")
    if not isinstance(package["depends"], list):
        raise ValueError("package.depends must be a list")
    for dependency in package["depends"]:
        text(dependency, "package.depends entry")
    fields(recipe["build"], ("directory", "component"), "build")
    directory = text(recipe["build"]["directory"], "build.directory")
    if directory.startswith(("/", "\\")) or "\\" in directory or ":" in directory or ".." in directory.split("/"):
        raise ValueError("build.directory must remain inside the source tree")
    text(recipe["build"]["component"], "build.component")
    return recipe
