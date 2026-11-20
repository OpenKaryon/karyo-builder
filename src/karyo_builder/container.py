# SPDX-License-Identifier: GPL-3.0-or-later
"""Package-stage runner, invoked only inside the selected Debian container."""
import argparse
import json
import os
from pathlib import Path
import shlex
import subprocess

from dependencies import discover


def run(args, **kwargs):
    print("+ " + shlex.join(map(str, args)), flush=True)
    return subprocess.run(list(map(str, args)), check=True, **kwargs)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jobs", type=int, required=True)
    args = parser.parse_args()
    recipe = json.loads(Path("/input/recipe.json").read_text(encoding="utf-8"))
    metadata = recipe["package"]
    distribution = Path("/etc/os-release").read_text()
    if 'VERSION_CODENAME=trixie' not in distribution:
        raise RuntimeError("This package stage requires Debian 13 (trixie)")
    architecture = subprocess.check_output(["dpkg", "--print-architecture"], text=True).strip()
    if architecture != metadata["architecture"]:
        raise RuntimeError("Package and container architectures differ")
    run(["dpkg", "--validate-version", metadata["version"]])
    source = (Path("/source") / recipe["build"]["directory"]).resolve()
    if not source.is_relative_to("/source") or not (source / "CMakeLists.txt").is_file():
        raise ValueError("The selected build directory has no CMakeLists.txt")
    Path("/tmp/home").mkdir()
    build = Path("/tmp/build")
    payload = build / "debian" / metadata["name"]
    run(["cmake", "-S", source, "-B", build, "-G", "Ninja",
         "-DCMAKE_BUILD_TYPE=Release", "-DCMAKE_INSTALL_PREFIX=/usr",
         "-DCMAKE_INSTALL_LIBDIR=lib/x86_64-linux-gnu", "-DBUILD_TESTING=ON"])
    run(["cmake", "--build", build, "--parallel", args.jobs])
    run(["ctest", "--test-dir", build, "--no-tests=error", "--output-on-failure"])
    install_env = dict(os.environ, DESTDIR=str(payload))
    run(["cmake", "--install", build, "--component", recipe["build"]["component"]], env=install_env)
    if not payload.exists() or not any(path.is_file() for path in payload.rglob("*")):
        raise RuntimeError("The selected install component produced no files")
    control_dir = payload / "DEBIAN"
    if control_dir.exists():
        raise RuntimeError("The CMake component must not supply Debian control files")
    control_dir.mkdir()
    dependencies = list(dict.fromkeys(metadata["depends"] + discover(payload, build, metadata["name"])))
    Path("/output/dependencies.json").write_text(
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
    artifact = Path("/output") / filename
    run(["dpkg-deb", "--build", "--root-owner-group", payload, artifact])
    run(["dpkg-deb", "--info", artifact])
    run(["dpkg-deb", "--contents", artifact])
    inventory = subprocess.check_output(
        ["dpkg-query", "-W", "-f", "${binary:Package}=${Version}\n"], text=True)
    # Preserve the exact installed build dependencies, including toolchain versions.
    Path("/output/environment.json").write_text(
        json.dumps(inventory.splitlines(), indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
