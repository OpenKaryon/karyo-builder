# SPDX-License-Identifier: GPL-3.0-or-later
"""Build captured distribution source packages without a network or host APT."""
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import uuid

from . import __version__
from .cli import command, mount, sha256
from .source_recipe import capture_recipe


def validate_source_image(image, architecture):
    expected = {"amd64": "amd64", "i386": "386"}.get(architecture)
    if (expected is None or image.get("Os") != "linux" or image.get("Architecture") != expected
            or not str(image.get("Id", "")).startswith("sha256:")):
        raise ValueError("A local immutable Linux image matching the recipe architecture is required")
    return image["Id"]


def validate_receipt(receipt, spec, staged):
    """Check native records against captured inputs before publishing output."""
    architecture = spec["build"].get("architecture", "amd64")
    if receipt.get("architecture", "amd64") != architecture:
        raise ValueError("Native source receipt architecture does not match the recipe")
    if receipt["version"] != spec["source"]["version"] + "+" + spec["build"]["revision"]:
        raise ValueError("Native source build returned a different version")
    expected_order = [f"karyo-{index:03d}-{item['file']}"
                      for index, item in enumerate(spec["patches"], 1)]
    if receipt["patch_order"] != expected_order:
        raise ValueError("Native source build returned a different patch order")
    artifacts = receipt["artifacts"]
    if not artifacts:
        raise ValueError("Native source build returned no artifacts")
    names, binaries = set(), {}
    for item in artifacts:
        name = item["file"]
        if (Path(name).name != name or "/" in name or "\\" in name
                or name in names or Path(name).suffix not in {".deb", ".ddeb", ".buildinfo", ".changes"}):
            raise ValueError("Artifacts must have distinct simple native filenames")
        names.add(name)
        path = staged / name
        if path.is_symlink() or not path.is_file() or sha256(path) != item["sha256"]:
            raise ValueError("Native source artifact hash mismatch: " + name)
        if type(item["bytes"]) is not int or path.stat().st_size != item["bytes"]:
            raise ValueError("Native source artifact size mismatch")
        if Path(name).suffix in {".deb", ".ddeb"}:
            if item.get("architecture", "amd64" if architecture == "amd64" else None) not in {architecture, "all"}:
                raise ValueError("Binary package architecture differs from native source target")
            package = item["package"]
            if package in binaries:
                raise ValueError("Duplicate binary package in native receipt")
            binaries[package] = name
        elif "package" in item:
            raise ValueError("Non-package artifact cannot claim a binary package")
    if binaries != receipt["binaries"] or not set(spec["build"]["binaries"]).issubset(binaries):
        raise ValueError("Native source build returned incomplete binary selection")
    if not {".buildinfo", ".changes"}.issubset({Path(name).suffix for name in names}):
        raise ValueError("Native source build is missing its buildinfo or changes record")
    distribution = json.loads((staged / "distribution.json").read_text())
    from .container import validate_target
    identity = validate_target("\n".join(f"{key}={value}" for key, value in distribution.items()))
    if identity["VERSION_CODENAME"] != spec["build"]["distribution"]:
        raise ValueError("Native source receipt has a different distribution")
    return artifacts, distribution


def build_source_package(args):
    with tempfile.TemporaryDirectory(prefix="karyo-dsc-") as temporary:
        inputs = Path(temporary) / "input"
        spec, recipe_hash = capture_recipe(args.recipe, inputs)
        runner_hashes = {}
        for name in ("source_container.py", "container.py", "dependencies.py"):
            shutil.copyfile(Path(__file__).with_name(name), inputs / name)
            runner_hashes[name] = sha256(inputs / name)
        image = json.loads(command(["docker", "image", "inspect", args.image]))[0]
        architecture = spec["build"].get("architecture", "amd64")
        image_id = validate_source_image(image, architecture)
        output = Path(args.output).resolve()
        output.mkdir(parents=True, exist_ok=True)
        job = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
        staged = output / (".partial-source-" + job)
        staged.mkdir()
        try:
            shutil.copyfile(inputs / "original-recipe.json", staged / "original-recipe.json")
            (staged / "resolved-input.json").write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")
            invocation = [
                "docker", "run", "--rm", "--network=none",
                "--platform=linux/" + ("386" if architecture == "i386" else "amd64"),
                "--cpus", str(args.jobs),
                "--memory=4g", "--pids-limit=512", "--cap-drop=ALL",
                "--security-opt=no-new-privileges",
                "--mount", mount(inputs, "/input"),
                "--mount", mount(staged, "/output", readonly=False),
                "--env", "HOME=/tmp/home", "--env", "LANG=C.UTF-8", "--env", "TERM=dumb",
                "--entrypoint", "python3", image_id, "/input/source_container.py", str(args.jobs),
            ]
            with (staged / "build.log").open("wb") as log:
                result = subprocess.run(invocation, stdout=log, stderr=subprocess.STDOUT)
            if result.returncode:
                raise RuntimeError(f"Native source package build exited with status {result.returncode}")
            receipt = json.loads((staged / "result.json").read_text(encoding="utf-8"))
            artifacts, distribution = validate_receipt(receipt, spec, staged)
            manifest = {
                "schema": 1, "kind": "source-package", "status": "success",
                "builder_version": __version__, "architecture": architecture, "recipe_sha256": recipe_hash, "input": spec,
                "environment": {"image_id": image_id,
                    "distribution": distribution,
                    "packages": json.loads((staged / "environment.json").read_text())},
                "runner_sha256": runner_hashes, "build_log_sha256": sha256(staged / "build.log"),
                "version": receipt["version"], "patch_order": receipt["patch_order"],
                "binaries": receipt["binaries"], "artifacts": artifacts,
            }
            (staged / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
            (staged / "SHA256SUMS").write_text(
                "".join(f"{item['sha256']}  {item['file']}\n" for item in artifacts), encoding="utf-8")
            final = output / ("karyo-source-package-" + job)
            if final.parent != output or staged.parent != output:
                raise ValueError("Build output escaped its selected directory")
            staged.rename(final)
        except BaseException:
            failed = output / (".failed-source-" + job)
            if failed.parent != output or staged.parent != output:
                raise ValueError("Failed build output escaped its selected directory")
            staged.rename(failed)
            print(f"Failed source build retained at {failed}")
            raise
    print(f"Native source packages and build record: {final}")
    return 0
