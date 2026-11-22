# SPDX-License-Identifier: GPL-3.0-or-later
"""Reject ambiguous or changed source inputs before executing any build."""
import copy
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest

from karyo_builder.source_recipe import capture_recipe


class SourceInputsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.original = self.root / "upstream_1.0.orig.tar.gz"
        self.debian = self.root / "upstream_1.0-1.debian.tar.xz"
        self.original.write_bytes(b"opaque archive fixture")
        self.debian.write_bytes(b"opaque packaging fixture")
        self.patch_a = self.root / "first.patch"
        self.patch_b = self.root / "second.patch"
        self.patch_a.write_bytes(b"first patch")
        self.patch_b.write_bytes(b"second patch")
        self.dsc = self.root / "upstream_1.0-1.dsc"
        self.write_dsc()
        self.recipe = {
            "schema": 1,
            "source": {"name": "upstream", "version": "1.0-1",
                       "dsc": self.entry(self.dsc),
                       "archives": [self.entry(self.original), self.entry(self.debian)]},
            "patches": [self.entry(self.patch_a), self.entry(self.patch_b)],
            "build": {"revision": "karyo1", "distribution": "trixie",
                      "maintainer": "Karyo Developers <developers@openkaryon.invalid>",
                      "message": "Reviewed downstream changes.", "binaries": ["upstream"],
                      "source_date_epoch": 1700000000},
        }

    def entry(self, path):
        return {"path": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}

    def write_dsc(self, extra=""):
        checksums = "".join(" " + hashlib.sha256(p.read_bytes()).hexdigest()
                            + f" {p.stat().st_size} {p.name}\n" for p in (self.original, self.debian))
        self.dsc.write_bytes(("Format: 3.0 (quilt)\nSource: upstream\nVersion: 1.0-1\n"
                             + extra + "Checksums-Sha256:\n" + checksums).encode())

    def capture(self, recipe=None, label="captured"):
        path = self.root / (label + ".json")
        path.write_text(json.dumps(recipe or self.recipe), encoding="utf-8")
        return capture_recipe(path, self.root / label)

    def test_capture_is_stable_after_live_files_change_and_keeps_patch_order(self):
        result, digest = self.capture()
        self.original.write_bytes(b"changed after capture")
        self.patch_a.write_bytes(b"changed after capture")
        self.assertEqual((self.root / "captured/sources" / self.original.name).read_bytes(),
                         b"opaque archive fixture")
        self.assertEqual((self.root / "captured/patches/first.patch").read_bytes(), b"first patch")
        self.assertEqual([p["file"] for p in result["patches"]], ["first.patch", "second.patch"])
        self.assertEqual(digest, hashlib.sha256((self.root / "captured.json").read_bytes()).hexdigest())

    def test_native_architecture_is_explicit_and_old_inputs_keep_their_default(self):
        original = copy.deepcopy(self.recipe)
        default, _ = self.capture(label="default-architecture")
        self.assertNotIn("architecture", default["build"])
        self.assertEqual(self.recipe, original)
        for architecture in ("amd64", "i386"):
            recipe = copy.deepcopy(original)
            recipe["build"]["architecture"] = architecture
            captured, _ = self.capture(recipe, "architecture-" + architecture)
            self.assertEqual(captured["build"]["architecture"], architecture)
        for index, architecture in enumerate(("all", "386", "arm64", "", None, [], True)):
            recipe = copy.deepcopy(original)
            recipe["build"]["architecture"] = architecture
            with self.subTest(architecture=architecture), self.assertRaisesRegex(ValueError, "architecture"):
                self.capture(recipe, "invalid-architecture-" + str(index))

    def test_corruption_is_rejected_before_build(self):
        self.original.write_bytes(b"corrupted archive")
        with self.assertRaisesRegex(ValueError, "SHA256 mismatch"):
            self.capture()
        recipe = copy.deepcopy(self.recipe)
        recipe["source"]["archives"][0] = self.entry(self.original)
        with self.assertRaisesRegex(ValueError, "DSC archives"):
            self.capture(recipe, "matching-recipe-stale-dsc")

    def test_identity_format_and_duplicate_headers_are_rejected(self):
        for index, data in enumerate((
                self.dsc.read_bytes().replace(b"Version: 1.0-1", b"Version: 2.0-1"),
                self.dsc.read_bytes().replace(b"3.0 (quilt)", b"3.0 (native)"),
                self.dsc.read_bytes() + b"Source: different\n")):
            self.dsc.write_bytes(data)
            recipe = copy.deepcopy(self.recipe)
            recipe["source"]["dsc"] = self.entry(self.dsc)
            with self.assertRaises(ValueError):
                self.capture(recipe, f"identity-{index}")

    def test_missing_or_extra_archive_is_rejected(self):
        recipe = copy.deepcopy(self.recipe)
        recipe["source"]["archives"].pop()
        with self.assertRaisesRegex(ValueError, "DSC archives"):
            self.capture(recipe)
        extra = self.root / "extra.tar.gz"
        extra.write_bytes(b"not declared")
        recipe["source"]["archives"] = [*self.recipe["source"]["archives"], self.entry(extra)]
        with self.assertRaisesRegex(ValueError, "DSC archives"):
            self.capture(recipe, "extra")

    def test_duplicate_input_names_and_unsafe_patch_names_are_rejected(self):
        recipe = copy.deepcopy(self.recipe)
        recipe["patches"].append(self.entry(self.patch_a))
        with self.assertRaisesRegex(ValueError, "distinct"):
            self.capture(recipe)
        unsafe = self.root / "-option.patch"
        unsafe.write_bytes(b"not an option")
        recipe["patches"] = [self.entry(unsafe)]
        with self.assertRaisesRegex(ValueError, "Unsafe"):
            self.capture(recipe, "unsafe")

    def test_schema_and_metadata_cannot_inject_control_lines_or_options(self):
        cases = []
        for field, value in (("revision", "-option"), ("distribution", "bookworm"),
                             ("maintainer", "Name\nInjected: value"), ("binaries", ["same", "same"]),
                             ("source_date_epoch", True)):
            recipe = copy.deepcopy(self.recipe)
            recipe["build"][field] = value
            cases.append(recipe)
        recipe = copy.deepcopy(self.recipe)
        recipe["source"]["dsc"]["sha256"] = "NOT-A-DIGEST"
        cases.append(recipe)
        recipe = copy.deepcopy(self.recipe)
        recipe["unknown"] = True
        cases.append(recipe)
        for index, recipe in enumerate(cases):
            with self.subTest(index=index), self.assertRaises(ValueError):
                self.capture(recipe, f"bad-{index}")

    def test_clearsigned_control_fields_are_supported_without_claiming_signature_trust(self):
        # This exercises armor parsing only; digest checks do not authenticate a PGP signer.
        self.dsc.write_bytes(b"-----BEGIN PGP SIGNED MESSAGE-----\nHash: SHA256\n\n"
                             + self.dsc.read_bytes() + b"\n-----BEGIN PGP SIGNATURE-----\nfixture\n")
        self.recipe["source"]["dsc"] = self.entry(self.dsc)
        result, _ = self.capture()
        self.assertEqual(result["source"]["version"], "1.0-1")

    def test_symlink_inputs_are_rejected(self):
        link = self.root / "linked.patch"
        try:
            os.symlink(self.patch_a, link)
        except OSError as error:
            self.skipTest("Host does not permit creating symlinks: " + str(error))
        recipe = copy.deepcopy(self.recipe)
        recipe["patches"] = [{"path": link.name, "sha256": self.entry(self.patch_a)["sha256"]}]
        with self.assertRaisesRegex(ValueError, "symlinks"):
            self.capture(recipe)
