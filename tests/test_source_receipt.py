# SPDX-License-Identifier: GPL-3.0-or-later
"""Reject inconsistent native build receipts before publishing them."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from karyo_builder.source_package import validate_receipt, validate_source_image


class SourceReceiptTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.spec = {"source": {"version": "1.0-1"},
                     "patches": [{"file": "one.patch"}, {"file": "two.patch"}],
                     "build": {"revision": "qa1", "binaries": ["fixture"], "distribution": "trixie"}}
        (self.root / "distribution.json").write_text(json.dumps({
            "ID": "debian", "VERSION_ID": "13", "VERSION_CODENAME": "trixie"}))
        artifacts = []
        for name in ("fixture.deb", "fixture.buildinfo", "fixture.changes"):
            data = ("fixture " + name).encode()
            (self.root / name).write_bytes(data)
            record = {"file": name, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
            if name.endswith(".deb"):
                record["package"] = "fixture"
            artifacts.append(record)
        self.receipt = {"version": "1.0-1+qa1", "patch_order": ["karyo-001-one.patch", "karyo-002-two.patch"],
                        "binaries": {"fixture": "fixture.deb"}, "artifacts": artifacts}

    def test_complete_receipt_matches_captured_recipe(self):
        artifacts, distro = validate_receipt(self.receipt, self.spec, self.root)
        self.assertEqual(artifacts, self.receipt["artifacts"])
        self.assertEqual(distro["ID"], "debian")

    def test_native_i386_receipt_cannot_substitute_amd64_packages(self):
        self.spec["build"]["architecture"] = "i386"
        with self.assertRaisesRegex(ValueError, "architecture"):
            validate_receipt(self.receipt, self.spec, self.root)
        self.receipt["architecture"] = "i386"
        with self.assertRaisesRegex(ValueError, "architecture"):
            validate_receipt(self.receipt, self.spec, self.root)
        self.receipt["artifacts"][0]["architecture"] = "amd64"
        with self.assertRaisesRegex(ValueError, "architecture"):
            validate_receipt(self.receipt, self.spec, self.root)
        self.receipt["artifacts"][0]["architecture"] = "i386"
        validate_receipt(self.receipt, self.spec, self.root)
        self.receipt["artifacts"][0]["architecture"] = "all"
        validate_receipt(self.receipt, self.spec, self.root)

    def test_source_image_must_match_native_recipe_architecture(self):
        image = {"Id": "sha256:" + "a" * 64, "Os": "linux", "Architecture": "386"}
        self.assertEqual(validate_source_image(image, "i386"), image["Id"])
        for architecture in ("amd64", "arm64", "all"):
            with self.subTest(architecture=architecture), self.assertRaises(ValueError):
                validate_source_image(image, architecture)
        image["Architecture"] = "amd64"
        self.assertEqual(validate_source_image(image, "amd64"), image["Id"])
        image["Os"] = "windows"
        with self.assertRaises(ValueError):validate_source_image(image, "amd64")

    def test_inconsistent_receipts_are_rejected(self):
        variants = []
        for key, value in (("version", "2.0-1+qa1"), ("patch_order", []),
                           ("binaries", {"fixture": "different.deb"})):
            item = copy.deepcopy(self.receipt)
            item[key] = value
            variants.append(item)
        item = copy.deepcopy(self.receipt)
        item["artifacts"].append(item["artifacts"][0])
        variants.append(item)
        item = copy.deepcopy(self.receipt)
        item["artifacts"].pop()
        variants.append(item)
        item = copy.deepcopy(self.receipt)
        item["artifacts"][0]["file"] = "../fixture.deb"
        variants.append(item)
        item = copy.deepcopy(self.receipt)
        item["artifacts"][1]["package"] = "invented"
        variants.append(item)
        for item in variants:
            with self.subTest(item=item), self.assertRaises(ValueError):
                validate_receipt(item, self.spec, self.root)

    def test_modified_artifact_is_rejected(self):
        (self.root / "fixture.deb").write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            validate_receipt(self.receipt, self.spec, self.root)

    def test_foreign_distribution_receipt_is_rejected(self):
        (self.root / "distribution.json").write_text(json.dumps({
            "ID": "ubuntu", "VERSION_ID": "26.04", "VERSION_CODENAME": "resolute"}))
        with self.assertRaisesRegex(ValueError, "different distribution"):
            validate_receipt(self.receipt, self.spec, self.root)
