# SPDX-License-Identifier: GPL-3.0-or-later
"""Export a Git revision and build one native Debian package in Docker."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import uuid

from . import __version__
from .recipe import load_recipe


def command(args, **kwargs):
    return subprocess.run(args, check=True, capture_output=True, text=True, **kwargs).stdout.strip()


def sha256(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def mount(path, destination, readonly=True):
    value = str(Path(path).resolve())
    if "," in value:
        raise ValueError("Docker bind paths containing commas are not supported")
    suffix = ",readonly" if readonly else ""
    return f"type=bind,source={value},target={destination}{suffix}"


def package(args):
    recipe_path = Path(args.recipe).resolve(strict=True)
    recipe = load_recipe(recipe_path)
    source = Path(args.source or recipe["source"]["path"]).resolve(strict=True)
    revision_name = args.revision or recipe["source"]["revision"]
    revision = command(["git", "-C", str(source), "rev-parse", "--verify",
                        "--end-of-options", f"{revision_name}^{{commit}}"])
    source_time = int(command(["git", "-C", str(source), "show", "-s", "--format=%ct", revision]))
    tree = command(["git", "-C", str(source), "ls-tree", "-r", revision])
    if any(line.startswith("160000 ") for line in tree.splitlines()):
        raise ValueError("Submodule source export is not supported by package stage 1")
    image = json.loads(command(["docker", "image", "inspect", args.image]))[0]
    if image.get("Os") != "linux" or image.get("Architecture") != "amd64":
        raise ValueError("A local Linux amd64 build image is required")
    image_id = image["Id"]
    if not image_id.startswith("sha256:"):
        raise ValueError("Docker did not provide an immutable image ID")
    output = Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    job = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    staged = output / f".partial-{job}"
    staged.mkdir()
    try:
        with tempfile.TemporaryDirectory(prefix="karyo-source-") as temporary:
            temporary = Path(temporary)
            archive = temporary / "source.tar"
            command(["git", "-C", str(source), "archive", "--format=tar",
                     f"--output={archive}", revision])
            exported = temporary / "source"
            exported.mkdir()
            with tarfile.open(archive) as tar:
                tar.extractall(exported, filter="data")
            input_dir = temporary / "input"
            input_dir.mkdir()
            recipe["source"] = {"path": "/source", "revision": revision}
            (input_dir / "recipe.json").write_text(
                json.dumps(recipe, indent=2) + "\n", encoding="utf-8")
            runner = Path(__file__).with_name("container.py")
            shutil.copyfile(runner, input_dir / "container.py")
            dependency_runner = runner.with_name("dependencies.py")
            shutil.copyfile(dependency_runner, input_dir / "dependencies.py")
            invocation = [
                "docker", "run", "--rm", "--network=none", "--cpus", str(args.jobs),
                "--memory=4g", "--pids-limit=512", "--cap-drop=ALL",
                "--security-opt=no-new-privileges",
                "--mount", mount(exported, "/source"),
                "--mount", mount(input_dir, "/input"),
                "--mount", mount(staged, "/output", readonly=False),
                "--env", f"SOURCE_DATE_EPOCH={source_time}",
                "--env", "LANG=C.UTF-8", "--env", "HOME=/tmp/home",
                "--env", "QT_QPA_PLATFORM=offscreen",
                "--entrypoint", "python3", image_id, "/input/container.py",
                "--jobs", str(args.jobs),
            ]
            with (staged / "build.log").open("wb") as log:
                result = subprocess.run(invocation, stdout=log, stderr=subprocess.STDOUT)
            if result.returncode:
                raise RuntimeError(f"Package build exited with status {result.returncode}")
            metadata = recipe["package"]
            filename = f'{metadata["name"]}_{metadata["version"].replace(":", "%3a")}_amd64.deb'
            artifact = staged / filename
            if not artifact.is_file():
                raise RuntimeError("The build did not produce the expected Debian package")
            environment = json.loads((staged / "environment.json").read_text(encoding="utf-8"))
            manifest = {
                "schema": 1, "builder_version": __version__, "status": "success",
                "source": {"reference": revision_name, "revision": revision, "archive_sha256": sha256(archive),
                           "source_date_epoch": source_time},
                "recipe": {"sha256": sha256(recipe_path), "resolved": recipe},
                "environment": {"image_id": image_id, "packages": environment},
                "runner_sha256": sha256(runner),
                "dependency_runner_sha256": sha256(dependency_runner),
                "dependencies": json.loads((staged / "dependencies.json").read_text(encoding="utf-8")),
                "artifact": {"file": filename, "sha256": sha256(artifact),
                             "bytes": artifact.stat().st_size},
                "validation": {"ctest": "passed", "dpkg_deb": "passed"},
            }
            (staged / "manifest.json").write_text(
                json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
            (staged / "SHA256SUMS").write_text(
                f'{sha256(artifact)}  {filename}\n', encoding="utf-8")
        final = output / f"{metadata['name']}-{job}"
        staged.rename(final)
    except BaseException:
        failed = output / f".failed-{job}"
        staged.rename(failed)
        print(f"Failed build retained at {failed}", file=sys.stderr)
        raise
    print(f"Package and build record: {final}")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="stage", required=True)
    build = subcommands.add_parser("package", help="Build one package from the source repository HEAD")
    build.add_argument("recipe")
    build.add_argument("--source", help="Override the source repository path")
    build.add_argument("--revision", help="Select a Git tag or revision instead of HEAD")
    build.add_argument("--output", required=True)
    build.add_argument("--image", default="karyo-builder:trixie",
                       help="An existing local Docker image (resolved to its immutable ID)")
    build.add_argument("--jobs", type=int, choices=range(1, 9), default=2)
    args = parser.parse_args()
    try:
        return package(args)
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError, tarfile.TarError) as error:
        detail = error.stderr.strip() if isinstance(error, subprocess.CalledProcessError) and error.stderr else str(error)
        print(f"karyo-builder: {detail}", file=sys.stderr)
        return 1
