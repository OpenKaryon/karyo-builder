# SPDX-License-Identifier: GPL-3.0-or-later
"""Package-stage runner, invoked only inside the selected Debian-family container."""
import argparse
import json
import os
from pathlib import Path
import shlex
import subprocess

if __package__:
    from .dependencies import discover
else:
    from dependencies import discover


def run(args, **kwargs):
    print("+ " + shlex.join(map(str, args)), flush=True)
    return subprocess.run(list(map(str, args)), check=True, **kwargs)


def write_conffiles(payload, control_dir):
    paths = sorted(
        "/" + path.relative_to(payload).as_posix()
        for path in (payload / "etc").rglob("*")
        if path.is_file() and not path.is_symlink()
    )
    if any("\n" in path or "\r" in path for path in paths):
        raise ValueError("Debian conffile paths must not contain line breaks")
    if paths:
        (control_dir / "conffiles").write_text("\n".join(paths) + "\n", encoding="utf-8")


def validate_target(text):
    """Reject a different base before configuring native packages."""
    release = {}
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        words = shlex.split(value)
        release[key] = words[0] if len(words) == 1 else ""
    identity = (release.get("ID"), release.get("VERSION_ID"), release.get("VERSION_CODENAME"))
    if identity not in {("debian", "13", "trixie"), ("ubuntu", "26.04", "resolute")}:
        raise RuntimeError("Package stage requires Debian 13 (trixie) or Ubuntu 26.04 (resolute)")
    return {key: release[key] for key in ("ID", "VERSION_ID", "VERSION_CODENAME")}


def claim_payload(payload, package_name, owners):
    """Reject colliding files or file/directory prefixes before publishing a set."""
    for path in sorted(payload.rglob("*")):
        relative = path.relative_to(payload).as_posix()
        directory = path.is_dir() and not path.is_symlink()
        if relative in owners:
            previous, was_directory = owners[relative]
            if not directory or not was_directory:
                raise ValueError(f"Package payload collision: {relative} ({previous}, {package_name})")
        else:
            owners[relative] = (package_name, directory)


def build_package(recipe, build, output, architecture, owners):
    metadata = recipe["package"]
    payload = build / "debian" / metadata["name"]
    output.mkdir(parents=True, exist_ok=True)
    install_env = dict(os.environ, DESTDIR=str(payload))
    run(["cmake", "--install", build, "--component", recipe["build"]["component"]], env=install_env)
    if not payload.exists() or not any(path.is_file() for path in payload.rglob("*")):
        raise RuntimeError("The selected install component produced no files")
    claim_payload(payload, metadata["name"], owners)
    control_dir = payload / "DEBIAN"
    if control_dir.exists():
        raise RuntimeError("The CMake component must not supply Debian control files")
    control_dir.mkdir()
    write_conffiles(payload, control_dir)
    dependencies = list(dict.fromkeys(metadata["depends"] + discover(payload, build, metadata["name"])))
    (output / "dependencies.json").write_text(
        json.dumps(dependencies, indent=2) + "\n", encoding="utf-8")
    control = [
        f'Package: {metadata["name"]}', f'Version: {metadata["version"]}',
        f'Architecture: {architecture}', f'Section: {metadata["section"]}',
        "Priority: optional", f'Maintainer: {metadata["maintainer"]}',
        f'Description: {metadata["description"]}',
    ]
    if dependencies:
        control.append("Depends: " + ", ".join(dependencies))
    (control_dir / "control").write_text("\n".join(control) + "\n", encoding="utf-8")
    control_dir.chmod(0o755)
    (control_dir / "control").chmod(0o644)
    filename = f'{metadata["name"]}_{metadata["version"].replace(":", "%3a")}_{architecture}.deb'
    artifact = output / filename
    run(["dpkg-deb", "--build", "--root-owner-group", payload, artifact])
    run(["dpkg-deb", "--info", artifact])
    run(["dpkg-deb", "--contents", artifact])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jobs", type=int, required=True)
    args = parser.parse_args()
    batch = Path("/input/recipes.json").is_file()
    recipes = json.loads(Path("/input/recipes.json" if batch else "/input/recipe.json").read_text(encoding="utf-8"))
    if not batch:
        recipes = [recipes]
    if not recipes or len({r["package"]["name"] for r in recipes}) != len(recipes):
        raise ValueError("A package set needs distinct package names")
    if len({r["build"]["directory"] for r in recipes}) != 1:
        raise ValueError("A package set needs one CMake source directory")
    distribution = validate_target(Path("/etc/os-release").read_text())
    Path("/output/distribution.json").write_text(json.dumps(distribution, indent=2) + "\n", encoding="utf-8")
    architecture = subprocess.check_output(["dpkg", "--print-architecture"], text=True).strip()
    for recipe in recipes:
        if architecture != recipe["package"]["architecture"]:
            raise RuntimeError("Package and container architectures differ")
        run(["dpkg", "--validate-version", recipe["package"]["version"]])
    source = (Path("/source") / recipes[0]["build"]["directory"]).resolve()
    if not source.is_relative_to("/source") or not (source / "CMakeLists.txt").is_file():
        raise ValueError("The selected build directory has no CMakeLists.txt")
    Path("/tmp/home").mkdir()
    build = Path("/tmp/build")
    run(["cmake", "-S", source, "-B", build, "-G", "Ninja",
         "-DCMAKE_BUILD_TYPE=Release", "-DCMAKE_INSTALL_PREFIX=/usr",
         "-DCMAKE_INSTALL_LIBDIR=lib/x86_64-linux-gnu",
         "-DCMAKE_INSTALL_SYSCONFDIR=/etc", "-DBUILD_TESTING=ON"])
    run(["cmake", "--build", build, "--parallel", args.jobs])
    run(["ctest", "--test-dir", build, "--no-tests=error", "--output-on-failure"])
    owners = {}
    for recipe in recipes:
        output = Path("/output") / recipe["package"]["name"] if batch else Path("/output")
        build_package(recipe, build, output, architecture, owners)
    inventory = subprocess.check_output(
        ["dpkg-query", "-W", "-f", "${binary:Package}=${Version}\n"], text=True)
    Path("/output/environment.json").write_text(
        json.dumps(inventory.splitlines(), indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
