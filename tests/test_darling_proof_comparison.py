# SPDX-License-Identifier: GPL-3.0-or-later
"""Compare actual patch effects while retaining native tool versions separately."""
import copy
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("darling_input_gate", Path(__file__).with_name("acceptance") / "check-darling-inputs.py")
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


class NativeProofComparison(unittest.TestCase):
    def test_native_tool_versions_can_differ_but_every_source_effect_must_match(self):
        first = {"quilt_version": "0.68", "gnu_patch_version": "GNU patch 2.8", "quilt_zero_fuzz": True,
                 "archive": {"sha256": "original"}, "patches": [{"file": "fix.patch", "sha256": "patch"}],
                 "files": [{"path": "source.c", "sha256": "pristine", "matches_pristine": True}],
                 "forward": ["fix.patch"], "reverse": ["fix.patch"]}
        second = copy.deepcopy(first)
        second["quilt_version"] = "0.69"
        self.assertTrue(gate.equivalent_patch_results(first, second))
        for key, value in (("quilt_zero_fuzz", False), ("archive", {"sha256": "changed"}),
                           ("patches", [{"file": "fix.patch", "sha256": "changed"}]),
                           ("files", [{"path": "source.c", "sha256": "changed", "matches_pristine": True}]),
                           ("forward", [])):
            changed = copy.deepcopy(second)
            changed[key] = value
            with self.subTest(key=key):
                self.assertFalse(gate.equivalent_patch_results(first, changed))
        second.pop("quilt_version")
        self.assertFalse(gate.equivalent_patch_results(first, second))
