# SPDX-License-Identifier: GPL-3.0-or-later
"""Validate native probe archive boundaries before any guest extracts it."""
import importlib.util
import io
from pathlib import Path
import struct
import tarfile
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("macos_probe_builder", Path(__file__).with_name("acceptance") / "build-macos-probes.py")
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)

EXECUTABLES = ["karyo-macos-loader-probe", "KaryoCocoaProbe.app/Contents/MacOS/KaryoCocoaProbe",
               "KaryoQtProbe.app/Contents/MacOS/KaryoQtProbe"]
MACHO = struct.pack("<IIII", 0xfeedfacf, 0x01000007, 3, 2) + b"native-probe"


class MacProbeArchive(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.path = Path(self.temporary.name) / "probes.tar.gz"

    def archive(self, extra=(), first=MACHO):
        with tarfile.open(self.path, "w:gz") as archive:
            for index, name in enumerate(EXECUTABLES):
                content = first if index == 0 else MACHO
                member = tarfile.TarInfo("./" + name)
                member.mode = 0o755
                member.size = len(content)
                archive.addfile(member, io.BytesIO(content))
            for member, content in extra:
                archive.addfile(member, io.BytesIO(content) if content is not None else None)

    def test_three_executables_and_contained_bundle_link(self):
        link = tarfile.TarInfo("KaryoQtProbe.app/Contents/Frameworks/Foo.framework/Versions/Current")
        link.type = tarfile.SYMTYPE
        link.linkname = "A"
        link.mode = 0o777
        self.archive([(link, None)])
        records = gate.inspect_archive(self.path)
        self.assertEqual(len(records), 4)
        self.assertTrue(all(item["sha256"] for item in records[:3]))
        self.assertEqual(records[-1]["symlink"], "A")

    def test_host_elf_wrong_cpu_and_dylib_are_not_executable_probes(self):
        for data in (b"\x7fELF" + b"\0" * 24, struct.pack("<IIII", 0xfeedfacf, 0x0100000c, 0, 2),
                     struct.pack("<IIII", 0xfeedfacf, 0x01000007, 3, 6)):
            self.archive(first=data)
            with self.subTest(data=data), self.assertRaisesRegex(ValueError, "Intel64 Mach-O"):
                gate.inspect_archive(self.path)

    def test_unsafe_paths_modes_duplicates_and_links_fail(self):
        for name, mode, kind, target in (
            ("../escape", 0o644, tarfile.REGTYPE, ""),
            ("/absolute", 0o644, tarfile.REGTYPE, ""),
            ("inside//alias", 0o644, tarfile.REGTYPE, ""),
            (EXECUTABLES[0], 0o755, tarfile.REGTYPE, ""),
            ("privileged", 0o4755, tarfile.REGTYPE, ""),
            ("writable", 0o666, tarfile.REGTYPE, ""),
            ("KaryoQtProbe.app/link", 0o777, tarfile.SYMTYPE, "/outside"),
            ("KaryoQtProbe.app/link", 0o777, tarfile.SYMTYPE, "../KaryoCocoaProbe.app"),
            ("alias", 0o644, tarfile.LNKTYPE, EXECUTABLES[0])):
            member = tarfile.TarInfo(name)
            member.mode, member.type, member.linkname = mode, kind, target
            self.archive([(member, b"" if kind == tarfile.REGTYPE else None)])
            with self.subTest(name=name, mode=mode, kind=kind), self.assertRaises(ValueError):
                gate.inspect_archive(self.path)
