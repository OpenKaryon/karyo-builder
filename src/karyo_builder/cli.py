# SPDX-License-Identifier: GPL-3.0-or-later
"""Export a Git revision and build native Debian packages in Docker."""
import argparse
from datetime import datetime, timezone
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tarfile
import tempfile
import uuid

from . import __version__
from .recipe import parse_recipe


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


@dataclass(frozen=True)
class PackageInput:
    path: Path
    recipe: dict
    sha256: str
    source: Path
    reference: str
    revision: str


def resolve_inputs(paths, source_override=None, revision_override=None):
    """Capture recipes and resolve each source reference once before building."""
    inputs = []
    revisions = {}
    names = set()
    for path in paths:
        path = Path(path).resolve(strict=True)
        data = path.read_bytes()
        recipe = parse_recipe(data, path.parent)
        name = recipe["package"]["name"]
        if name in names:
            raise ValueError("A package set needs distinct package names")
        names.add(name)
        source = Path(source_override or recipe["source"]["path"]).resolve(strict=True)
        directory = PurePosixPath(recipe["build"]["directory"]).as_posix()
        recipe["build"]["directory"] = directory
        if inputs and (source != inputs[0].source or directory != inputs[0].recipe["build"]["directory"]):
            raise ValueError("A package set needs one source repository and CMake directory")
        reference = revision_override or recipe["source"]["revision"]
        key = (source, reference)
        if key not in revisions:
            revisions[key] = command(["git", "-C", str(source), "rev-parse", "--verify",
                                      "--end-of-options", f"{reference}^{{commit}}"])
        revision = revisions[key]
        if inputs and revision != inputs[0].revision:
            raise ValueError("A package set needs one resolved source commit")
        inputs.append(PackageInput(path, recipe, hashlib.sha256(data).hexdigest(), source, reference, revision))
    if not inputs:
        raise ValueError("At least one package recipe is required")
    return inputs


def package(args):
    batch = args.stage == "package-set"
    paths = args.recipe if batch else [args.recipe]
    inputs = resolve_inputs(paths, args.source, args.revision)
    source, revision = inputs[0].source, inputs[0].revision
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
            recipes = [dict(item.recipe, source={"path": "/source", "revision": revision}) for item in inputs]
            (input_dir / ("recipes.json" if batch else "recipe.json")).write_text(
                json.dumps(recipes if batch else recipes[0], indent=2) + "\n", encoding="utf-8")
            runner = Path(__file__).with_name("container.py")
            shutil.copyfile(runner, input_dir / "container.py")
            dependency_runner = runner.with_name("dependencies.py")
            shutil.copyfile(dependency_runner, input_dir / "dependencies.py")
            runner_hash = sha256(input_dir / "container.py")
            dependency_hash = sha256(input_dir / "dependencies.py")
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
            environment = {
                "image_id": image_id,
                "packages": json.loads((staged / "environment.json").read_text(encoding="utf-8")),
                "distribution": json.loads((staged / "distribution.json").read_text(encoding="utf-8")),
            }
            source_record = {"revision": revision, "archive_sha256": sha256(archive),
                             "source_date_epoch": source_time}
            records, checksums = [], []
            for item, recipe in zip(inputs, recipes):
                metadata = recipe["package"]
                folder = staged / metadata["name"] if batch else staged
                filename = f'{metadata["name"]}_{metadata["version"].replace(":", "%3a")}_amd64.deb'
                artifact = folder / filename
                if not artifact.is_file():
                    raise RuntimeError("The build did not produce the expected Debian package")
                artifact_hash = sha256(artifact)
                manifest = {
                    "schema": 1, "builder_version": __version__, "status": "success",
                    "source": dict(source_record, reference=item.reference),
                    "recipe": {"sha256": item.sha256, "resolved": recipe},
                    "environment": environment,
                    "runner_sha256": runner_hash,
                    "dependency_runner_sha256": dependency_hash,
                    "dependencies": json.loads((folder / "dependencies.json").read_text(encoding="utf-8")),
                    "artifact": {"file": filename, "sha256": artifact_hash, "bytes": artifact.stat().st_size},
                    "validation": {"ctest": "passed", "dpkg_deb": "passed"},
                }
                if batch:
                    manifest["shared_build_log"] = {"file": "../build.log", "sha256": sha256(staged / "build.log")}
                (folder / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
                (folder / "SHA256SUMS").write_text(f"{artifact_hash}  {filename}\n", encoding="utf-8")
                records.append({"package": metadata["name"], "directory": metadata["name"],
                                "manifest_sha256": sha256(folder / "manifest.json")})
                checksums.append(f'{artifact_hash}  {metadata["name"]}/{filename}')
            if batch:
                manifest = {"schema": 1, "kind": "package-set", "builder_version": __version__,
                            "status": "success", "source": source_record, "environment": environment,
                            "packages": records, "build_log_sha256": sha256(staged / "build.log")}
                (staged / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
                (staged / "SHA256SUMS").write_text("\n".join(checksums) + "\n", encoding="utf-8")
        final = output / f"{'karyo-package-set' if batch else metadata['name']}-{job}"
        if final.parent != output or staged.parent != output:
            raise ValueError("Build result paths must remain in the selected output directory")
        staged.rename(final)
    except BaseException:
        failed = output / f".failed-{job}"
        if staged.parent != output or failed.parent != output:
            raise ValueError("Failed build paths must remain in the output directory")
        staged.rename(failed)
        print(f"Failed build retained at {failed}", file=sys.stderr)
        raise
    print(f"{'Package set' if batch else 'Package'} and build record: {final}")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="stage", required=True)
    for name, help_text in (("package", "Build one package from source HEAD"),
                            ("package-set", "Build/test one source revision and package several components")):
        build = subcommands.add_parser(name, help=help_text)
        if name == "package-set":
            build.add_argument("recipe", nargs="+")
        else:
            build.add_argument("recipe")
        build.add_argument("--source", help="Override the source repository path")
        build.add_argument("--revision", help="Select a Git tag or revision instead of HEAD")
        build.add_argument("--output", required=True)
        build.add_argument("--image", default="karyo-builder:trixie",
                           help="An existing local Docker image (resolved to its immutable ID)")
        build.add_argument("--jobs", type=int, choices=range(1, 9), default=2)
    source_build = subcommands.add_parser("source-package",
        help="Rebuild checksummed Debian quilt source with ordered downstream patches")
    source_build.add_argument("recipe")
    source_build.add_argument("--output", required=True)
    source_build.add_argument("--image", required=True, help="Existing image with native source build dependencies")
    source_build.add_argument("--jobs", type=int, choices=range(1, 9), default=2)
    args = parser.parse_args()
    try:
        if args.stage == "source-package":
            from .source_package import build_source_package
            return build_source_package(args)
        return package(args)
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError, tarfile.TarError) as error:
        detail = error.stderr.strip() if isinstance(error, subprocess.CalledProcessError) and error.stderr else str(error)
        print(f"karyo-builder: {detail}", file=sys.stderr)
        return 1
