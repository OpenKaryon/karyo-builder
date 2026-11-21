# SPDX-License-Identifier: GPL-3.0-or-later
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from karyo_builder.cli import resolve_inputs
from karyo_builder.container import claim_payload


class PackageSetInputsTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.source = self.root / "sources with spaces"
        self.source.mkdir()
        self.hooks = self.root / "empty-hooks"
        self.hooks.mkdir()
        self.git("init", "-q", "--initial-branch=main", "--template=" + str(self.hooks))
        (self.source / "source.txt").write_text("first source\n")
        self.commit()
        self.git("tag", "--no-sign", "fixture-v1")
        self.template = json.loads((Path(__file__).resolve().parent / "fixtures/runtime.json").read_text())
        self.template["source"] = {"path": str(self.source)}
        self.template["build"]["directory"] = "."

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.source), "-c", "user.name=Builder QA",
            "-c", "user.email=qa@openkaryon.invalid", "-c", "core.hooksPath=" + str(self.hooks),
            *args], text=True, stderr=subprocess.STDOUT).strip()

    def commit(self):
        self.git("add", "source.txt")
        self.git("commit", "--no-gpg-sign", "-qm", "Disposable package-set fixture",
                 "-m", "Co-Authored-By: Codex <noreply@openai.com>")

    def recipe(self, name, *, reference=None, directory=".", source=None):
        recipe = json.loads(json.dumps(self.template))
        recipe["package"]["name"] = name
        recipe["build"]["directory"] = directory
        if reference is not None:
            recipe["source"]["revision"] = reference
        if source is not None:
            recipe["source"]["path"] = str(source)
        path = self.root / (name + ".json")
        path.write_text(json.dumps(recipe), encoding="utf-8")
        return path

    def test_same_commit_references_and_captured_recipe_hash(self):
        first = self.recipe("fixture-one")
        second = self.recipe("fixture-two", reference="fixture-v1", directory="./.")
        original = first.read_bytes()
        items = resolve_inputs([first, second])
        self.assertEqual(items[0].revision, self.git("rev-parse", "HEAD"))
        self.assertEqual(items[0].revision, items[1].revision)
        self.assertEqual(items[0].sha256, hashlib.sha256(original).hexdigest())
        first.write_text("changed after input resolution")
        self.assertEqual(items[0].recipe["package"]["name"], "fixture-one")
        self.assertEqual(items[0].sha256, hashlib.sha256(original).hexdigest())
        self.assertEqual(items[1].recipe["build"]["directory"], ".")

    def test_one_head_snapshot_even_if_the_reference_moves(self):
        paths = [self.recipe("fixture-one"), self.recipe("fixture-two")]
        with patch("karyo_builder.cli.command", side_effect=["first-head", "later-head"]) as resolver:
            items = resolve_inputs(paths)
        self.assertEqual([item.revision for item in items], ["first-head", "first-head"])
        self.assertEqual(resolver.call_count, 1)

    def test_distinct_commits_are_rejected_or_explicitly_overridden(self):
        paths = [self.recipe("fixture-one"), self.recipe("fixture-two", reference="fixture-v1")]
        (self.source / "source.txt").write_text("second source\n")
        self.commit()
        with self.assertRaisesRegex(ValueError, "one resolved source commit"):
            resolve_inputs(paths)
        items = resolve_inputs(paths, revision_override="fixture-v1")
        self.assertEqual(items[0].revision, items[1].revision)
        self.assertEqual(items[0].revision, self.git("rev-parse", "fixture-v1"))

    def test_incompatible_sets_fail_before_building(self):
        first = self.recipe("fixture-one")
        for other in (self.recipe("fixture-two", directory="subdir"),
                      self.recipe("fixture-three", source=self.root)):
            with self.assertRaisesRegex(ValueError, "one source repository and CMake directory"):
                resolve_inputs([first, other])
        with self.assertRaisesRegex(ValueError, "distinct package names"):
            resolve_inputs([first, first])
        with self.assertRaisesRegex(ValueError, "At least one"):
            resolve_inputs([])


class PackageOwnershipTest(unittest.TestCase):
    def test_shared_directories_are_allowed_but_duplicate_files_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            one, two = root / "one", root / "two"
            for payload, name in ((one, "one"), (two, "two")):
                (payload / "usr/bin").mkdir(parents=True)
                (payload / "usr/bin" / name).write_text("own payload")
            owners = {}
            claim_payload(one, "one", owners)
            claim_payload(two, "two", owners)
            (two / "usr/bin/one").write_text("even identical data must not have two owners")
            with self.assertRaisesRegex(ValueError, "payload collision"):
                claim_payload(two, "two", {key: value for key, value in owners.items() if value[0] == "one"})

    def test_file_directory_prefix_collisions_are_rejected_in_both_orders(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            one, two = root / "one", root / "two"
            (one / "usr").mkdir(parents=True)
            (one / "usr/shared").write_text("regular file")
            (two / "usr/shared").mkdir(parents=True)
            (two / "usr/shared/nested").write_text("nested payload")
            for first, second in ((one, two), (two, one)):
                owners = {}
                claim_payload(first, "first", owners)
                with self.assertRaisesRegex(ValueError, "payload collision"):
                    claim_payload(second, "second", owners)


if __name__ == "__main__":
    unittest.main()
