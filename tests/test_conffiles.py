# SPDX-License-Identifier: GPL-3.0-or-later
from pathlib import Path
import tempfile
import unittest
from karyo_builder.container import write_conffiles


class ConffileTest(unittest.TestCase):
    def test_only_host_configuration_is_registered(self):
        with tempfile.TemporaryDirectory() as directory:
            payload = Path(directory)
            control = payload / "DEBIAN"
            control.mkdir()
            (payload / "etc/pam.d").mkdir(parents=True)
            (payload / "etc/pam.d/karyo-lock").write_text("fixture")
            (payload / "etc/example.conf").write_text("fixture")
            (payload / "usr/share").mkdir(parents=True)
            (payload / "usr/share/example.conf").write_text("data")
            write_conffiles(payload, control)
            self.assertEqual((control / "conffiles").read_text(),
                             "/etc/example.conf\n/etc/pam.d/karyo-lock\n")

    def test_packages_without_configuration_need_no_conffiles(self):
        with tempfile.TemporaryDirectory() as directory:
            payload = Path(directory)
            control = payload / "DEBIAN"
            control.mkdir()
            write_conffiles(payload, control)
            self.assertFalse((control / "conffiles").exists())
