# SPDX-License-Identifier: GPL-3.0-or-later
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest

from karyo_builder.container import install_maintainer_scripts
from karyo_builder.recipe import parse_recipe


class ScriptRecipeTest(unittest.TestCase):
    def setUp(self):
        self.recipe = json.loads((Path(__file__).resolve().parent / "fixtures/runtime.json").read_text())

    def test_optional_empty_and_explicit_scripts_keep_original_recipe_compatible(self):
        original = parse_recipe(json.dumps(self.recipe).encode(), Path.cwd())
        self.assertNotIn("maintainer_scripts", original["package"])
        self.recipe["package"]["maintainer_scripts"] = {"postinst": "profiles/package/postinst"}
        parsed = parse_recipe(json.dumps(self.recipe).encode(), Path.cwd())
        self.assertEqual(parsed["package"]["maintainer_scripts"], {"postinst": "profiles/package/postinst"})

    def test_unknown_roles_and_script_container_types_are_rejected(self):
        for value in (None, False, [], "postinst", {"triggers": "input"}, {"control": "input"}):
            with self.subTest(value=value):
                self.recipe["package"]["maintainer_scripts"] = value
                with self.assertRaises(ValueError):
                    parse_recipe(json.dumps(self.recipe).encode(), Path.cwd())

    def test_paths_cannot_escape_be_noncanonical_or_encode_inline_shell(self):
        for value in (None, False, "", "/root/postinst", "../postinst", "a/../postinst", "a//postinst", "./script",
                      "-script", "C:/script", "a\\script", "echo done", "a;script", "a\nscript", "x" * 257):
            with self.subTest(value=value):
                self.recipe["package"]["maintainer_scripts"] = {"postinst": value}
                with self.assertRaises(ValueError):
                    parse_recipe(json.dumps(self.recipe).encode(), Path.cwd())


class ScriptStagingTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "source"
        self.source.mkdir()
        self.control = self.root / "DEBIAN"
        self.control.mkdir()
        self.folder = self.source / "hooks"
        self.folder.mkdir()

    def stage(self, scripts):
        return install_maintainer_scripts({"maintainer_scripts": scripts}, self.source, self.control)

    def test_exact_scripts_are_hashed_executable_and_never_executed(self):
        data = b"#!/bin/sh\nset -eu\nexit 73\n"
        (self.folder / "postinst").write_bytes(data)
        records = self.stage({"postinst": "hooks/postinst"})
        self.assertEqual((self.control / "postinst").read_bytes(), data)
        if os.name != "nt":
            self.assertEqual((self.control / "postinst").stat().st_mode & 0o777, 0o755)
        self.assertEqual(records, [{"role": "postinst", "source": "hooks/postinst",
                                   "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}])

    def test_all_inputs_are_checked_before_control_mutation(self):
        (self.folder / "good").write_bytes(b"#!/bin/sh\nexit 0\n")
        (self.folder / "bad").write_bytes(b"#!/usr/bin/env python3\n")
        with self.assertRaises(ValueError):
            self.stage({"postinst": "hooks/good", "prerm": "hooks/bad"})
        self.assertEqual(list(self.control.iterdir()), [])

    def test_only_bounded_utf8_lf_shell_scripts_can_enter_debian_control(self):
        for data in (b"", b"#!/bin/bash\n", b"#!/bin/sh\r\n", b"#!/bin/sh\n\0", b"#!/bin/sh\n\xff",
                     b"#!/bin/sh\n" + b"x" * 65536):
            with self.subTest(data=data[:30]):
                (self.folder / "script").write_bytes(data)
                with self.assertRaises(ValueError):
                    self.stage({"postinst": "hooks/script"})
                self.assertEqual(list(self.control.iterdir()), [])

    def test_existing_control_file_is_never_overwritten(self):
        (self.folder / "script").write_bytes(b"#!/bin/sh\nexit 0\n")
        (self.control / "postinst").write_text("existing")
        with self.assertRaises(FileExistsError):
            self.stage({"postinst": "hooks/script"})
        self.assertEqual((self.control / "postinst").read_text(), "existing")

    def test_directories_hardlinks_and_unknown_roles_fail(self):
        with self.assertRaises(ValueError):
            self.stage({"postinst": "hooks"})
        (self.folder / "script").write_bytes(b"#!/bin/sh\n")
        os.link(self.folder / "script", self.folder / "alias")
        with self.assertRaises(ValueError):
            self.stage({"postinst": "hooks/alias"})
        with self.assertRaises(ValueError):
            self.stage({"other": "hooks/script"})

    @unittest.skipIf(os.name == "nt", "native Linux symlink validation is required separately")
    def test_file_and_parent_symlinks_are_refused_even_inside_source(self):
        (self.folder / "script").write_bytes(b"#!/bin/sh\n")
        (self.folder / "link").symlink_to("script")
        (self.source / "redirect").symlink_to("hooks", target_is_directory=True)
        for relative in ("hooks/link", "redirect/script"):
            with self.subTest(relative=relative), self.assertRaises(ValueError):
                self.stage({"postinst": relative})


if __name__ == "__main__":
    unittest.main()
