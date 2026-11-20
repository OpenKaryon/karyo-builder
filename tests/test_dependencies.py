# SPDX-License-Identifier: GPL-3.0-or-later
from pathlib import Path
import tempfile
import unittest

from karyo_builder.dependencies import discover


class DependencyDiscoveryTest(unittest.TestCase):
    def test_data_and_static_objects_do_not_add_runtime_dependencies(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "file.txt").write_text("plain text")
            (root / "library.a").write_bytes(b"!<arch>\n")
            header = bytearray(20)
            header[:6] = b"\x7fELF\x02\x01"
            header[16:18] = (1).to_bytes(2, "little")
            header[18:20] = (62).to_bytes(2, "little")
            (root / "object.o").write_bytes(header)
            self.assertEqual(discover(root, root, "fixture"), [])

    def test_wrong_machine_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            header = bytearray(20)
            header[:6] = b"\x7fELF\x02\x01"
            header[16:18] = (3).to_bytes(2, "little")
            header[18:20] = (183).to_bytes(2, "little")
            (root / "foreign.so").write_bytes(header)
            with self.assertRaisesRegex(RuntimeError, "Unsupported ELF architecture"):
                discover(root, root, "fixture")
