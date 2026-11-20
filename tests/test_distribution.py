# SPDX-License-Identifier: GPL-3.0-or-later
import unittest
from karyo_builder.container import validate_target


class DistributionTest(unittest.TestCase):
    def test_supported_release_identities(self):
        for name, version, codename in (("debian", "13", "trixie"), ("ubuntu", "26.04", "resolute")):
            with self.subTest(name=name):
                target = validate_target(f'ID={name}\nVERSION_ID="{version}"\nVERSION_CODENAME={codename}\n')
                self.assertEqual(target["ID"], name)
                self.assertEqual(target["VERSION_ID"], version)

    def test_release_must_match_entire_identity(self):
        for text in (
            "VERSION_CODENAME=trixie", "ID=ubuntu\nVERSION_ID=24.04\nVERSION_CODENAME=noble",
            "ID=debian\nVERSION_ID=12\nVERSION_CODENAME=trixie",
            "ID=other\nVERSION_ID=26.04\nVERSION_CODENAME=resolute",
            "ID=ubuntu\nVERSION_ID=26.04\nVERSION_CODENAME=trixie",
        ):
            with self.subTest(text=text), self.assertRaises(RuntimeError):
                validate_target(text)
