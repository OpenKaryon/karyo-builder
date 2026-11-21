# SPDX-License-Identifier: GPL-3.0-or-later
import copy
import json
from pathlib import Path
import tempfile
import unittest

from karyo_builder.recipe import load_recipe
from karyo_builder.cli import main


class PackageRecipeTest(unittest.TestCase):
    def setUp(self):
        self.valid = json.loads(
            (Path(__file__).resolve().parents[1] / "examples/ui-foundation.json").read_text())

    def load(self, recipe):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "package.json"
            path.write_text(json.dumps(recipe), encoding="utf-8")
            return load_recipe(path), path.parent

    def test_paths_resolve_from_recipe(self):
        self.valid["source"]["path"] = "sources with spaces"
        recipe, folder = self.load(self.valid)
        self.assertEqual(recipe["source"]["path"], str((folder / "sources with spaces").resolve()))

    def test_source_head_default_and_explicit_tag(self):
        self.valid["source"].pop("revision", None)
        recipe, _ = self.load(self.valid)
        self.assertEqual(recipe["source"]["revision"], "HEAD")
        self.valid["source"]["revision"] = "v0.1.0"
        recipe, _ = self.load(self.valid)
        self.assertEqual(recipe["source"]["revision"], "v0.1.0")

    def test_invalid_contracts(self):
        for section, key, value in (
            ("package", "name", "../escape"),
            ("package", "version", "1\nDepends: injected"),
            ("package", "depends", ["qt6-base-dev\nDescription: injected"]),
            ("package", "architecture", "arm64"),
            ("build", "directory", "../outside"),
            ("build", "directory", "/absolute"),
            ("build", "component", ""),
            ("source", "revision", "HEAD\nother"),
        ):
            with self.subTest(section=section, key=key):
                recipe = copy.deepcopy(self.valid)
                recipe[section][key] = value
                with self.assertRaises(ValueError):
                    self.load(recipe)

    def test_unknown_fields_and_schema(self):
        recipe = copy.deepcopy(self.valid)
        recipe["unexpected"] = True
        with self.assertRaises(ValueError):
            self.load(recipe)
        self.valid["schema"] = True
        with self.assertRaises(ValueError):
            self.load(self.valid)

    def test_missing_recipe_has_clear_failure(self):
        with tempfile.TemporaryDirectory() as temporary:
            result = main_with_args([
                "package", str(Path(temporary) / "absent.json"), "--output", temporary])
            self.assertEqual(result, 1)
            self.assertEqual(list(Path(temporary).iterdir()), [])


def main_with_args(args):
    from unittest.mock import patch
    with patch("sys.argv", ["karyo-builder", *args]):
        return main()


if __name__ == "__main__":
    unittest.main()
