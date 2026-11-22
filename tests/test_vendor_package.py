# SPDX-License-Identifier: GPL-3.0-or-later
import copy
import hashlib
import io
import json
import os
from pathlib import Path
import tarfile
import tempfile
import unittest

from karyo_builder.vendor_container import select_members
from karyo_builder.vendor_recipe import capture_recipe, validate_recipe
from karyo_builder.vendor_package import validate_receipt


def spec():
    return {'schema': 1, 'package': {'name': 'karyo-vendor-test', 'version': '1.0-1', 'architecture': 'amd64',
        'maintainer': 'Karyo <test@example.invalid>', 'description': 'Inert fixture', 'section': 'net', 'depends': [],
        'provides': ['vendor-test (= 1.0)'], 'conflicts': ['vendor-test']},
        'inputs': [{'path': 'test.deb', 'sha256': 'a'*64, 'package': 'vendor-test', 'version': '1.0',
                    'architecture': 'amd64', 'files': ['usr/bin/vendor-test']}],
        'licenses': [{'path': 'LICENSE', 'sha256': 'b'*64, 'destination': 'usr/share/doc/karyo-vendor-test/LICENSE.vendor'}],
        'source_date_epoch': 0}


class VendorRecipeTest(unittest.TestCase):
    def test_exact_files_and_control_relationships(self):
        validate_recipe(spec())

    def test_hooks_unknown_fields_duplicate_destinations_and_missing_licenses_fail(self):
        cases = []
        item = spec(); item['package']['maintainer_scripts'] = {'postinst': 'install'}; cases.append(item)
        item = spec(); item['licenses'] = []; cases.append(item)
        item = spec(); item['inputs'][0]['files'] *= 2; cases.append(item)
        item = spec(); item['inputs'].append(copy.deepcopy(item['inputs'][0])); cases.append(item)
        item = spec(); item['source_date_epoch'] = False; cases.append(item)
        item = spec(); item['inputs'][0]['sha256'] = 'A'*64; cases.append(item)
        item = spec(); item['inputs'][0]['architecture'] = 'all'; cases.append(item)
        item = spec(); item['package']['conflicts'] = ['x\nPostinst: command']; cases.append(item)
        for value in cases:
            with self.subTest(value=value), self.assertRaises(ValueError): validate_recipe(value)

    def test_activation_control_and_escape_paths_are_not_payload(self):
        for path in ('/usr/bin/tool', '../usr/bin/tool', 'usr/bin/../tool', 'usr//bin/tool', 'usr/bin/x\\y',
                     'DEBIAN/postinst', 'etc/xdg/autostart/tool.desktop', 'usr/lib/systemd/system/tool.service',
                     'usr/share/applications/tool.desktop', 'usr/share/polkit-1/actions/tool.policy', 'usr/share/dbus-1/services/tool.service'):
            with self.subTest(path=path):
                value = spec(); value['inputs'][0]['files'] = [path]
                with self.assertRaises(ValueError): validate_recipe(value)
        value = spec(); value['licenses'][0]['destination'] = 'usr/share/doc/other/LICENSE'
        with self.assertRaises(ValueError): validate_recipe(value)

    def test_capture_hashes_private_copies_and_rejects_mismatch_links_or_duplicate_json(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); data = b'captured deb data'; license = b'License text\n'
            (root/'test.deb').write_bytes(data); (root/'LICENSE').write_bytes(license)
            value = spec(); value['inputs'][0]['sha256'] = hashlib.sha256(data).hexdigest()
            value['licenses'][0]['sha256'] = hashlib.sha256(license).hexdigest()
            recipe = root/'recipe.json'; recipe.write_bytes(json.dumps(value).encode())
            resolved, captured, digest = capture_recipe(recipe, root/'input')
            self.assertEqual((root/'input/inputs-0.deb').read_bytes(), data)
            self.assertEqual(captured[0]['sha256'], value['inputs'][0]['sha256'])
            self.assertEqual(resolved['inputs'][0]['path'], '/input/inputs-0.deb')
            self.assertEqual(digest, hashlib.sha256(recipe.read_bytes()).hexdigest())
            (root/'test.deb').write_bytes(b'changed')
            with self.assertRaises(ValueError): capture_recipe(recipe, root/'changed')
            recipe.write_bytes(b'{"schema":1,"schema":1}')
            with self.assertRaises(ValueError): capture_recipe(recipe, root/'duplicate')
            (root/'test.deb').write_bytes(data); os.link(root/'test.deb', root/'alias.deb')
            recipe.write_bytes(json.dumps(value).encode())
            with self.assertRaises(ValueError): capture_recipe(recipe, root/'hardlinked')

    @unittest.skipIf(os.name == 'nt', 'native symlink fixture')
    def test_parent_symlink_is_not_captured(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); (root/'real').mkdir(); (root/'alias').symlink_to(root/'real', target_is_directory=True)
            value = spec(); value['inputs'][0]['path'] = 'alias/input.deb'
            (root/'real/input.deb').write_bytes(b'x'); value['inputs'][0]['sha256'] = hashlib.sha256(b'x').hexdigest()
            (root/'recipe.json').write_text(json.dumps(value))
            with self.assertRaises(ValueError): capture_recipe(root/'recipe.json', root/'input')


class VendorTarTest(unittest.TestCase):
    def archive(self, entries):
        data = io.BytesIO()
        with tarfile.open(fileobj=data, mode='w') as archive:
            for name, kind, mode, contents in entries:
                info = tarfile.TarInfo(name); info.type = kind; info.mode = mode
                if kind == tarfile.REGTYPE: info.size = len(contents)
                else: info.linkname = '../../escape'
                archive.addfile(info, io.BytesIO(contents) if kind == tarfile.REGTYPE else None)
        data.seek(0); return tarfile.open(fileobj=data, mode='r')

    def test_only_selected_regular_files_are_copied_not_hooks_or_parent_links(self):
        entries = [('usr', tarfile.SYMTYPE, 0o777, b''), ('../escape', tarfile.REGTYPE, 0o644, b'outside'),
                   ('./usr/bin/vendor-test', tarfile.REGTYPE, 0o755, b'binary'),
                   ('etc/xdg/autostart/x.desktop', tarfile.REGTYPE, 0o644, b'activation')]
        with tempfile.TemporaryDirectory() as temp, self.archive(entries) as archive:
            result = select_members(archive, Path(temp), ['usr/bin/vendor-test'])
            self.assertEqual((Path(temp)/'usr/bin/vendor-test').read_bytes(), b'binary')
            self.assertFalse((Path(temp)/'etc').exists())
            self.assertEqual(result[0]['sha256'], hashlib.sha256(b'binary').hexdigest())
            self.assertEqual(result[0]['mode'], 0o755)

    def test_selected_symlink_hardlink_fifo_privileged_writable_empty_or_duplicate_fail(self):
        path = 'usr/bin/vendor-test'
        cases = [[(path, kind, 0o755, b'')] for kind in (tarfile.SYMTYPE, tarfile.LNKTYPE, tarfile.FIFOTYPE)]
        cases += [[(path, tarfile.REGTYPE, mode, b'x')] for mode in (0o4755, 0o2755, 0o1777, 0o775)]
        cases += [[(path, tarfile.REGTYPE, 0o644, b'')], [(path, tarfile.REGTYPE, 0o755, b'x')]*2, []]
        for entries in cases:
            with self.subTest(entries=entries), tempfile.TemporaryDirectory() as temp, self.archive(entries) as archive:
                with self.assertRaises(ValueError): select_members(archive, Path(temp), [path])

    def test_direct_selection_still_rejects_escape_paths(self):
        with tempfile.TemporaryDirectory() as temp, self.archive([]) as archive:
            with self.assertRaises(ValueError): select_members(archive, Path(temp), ['../escape'])


class VendorReceiptTest(unittest.TestCase):
    def test_native_receipt_cannot_add_files_hooks_change_inputs_or_lose_license(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); recipe = spec(); artifact = root/'karyo-vendor-test_1.0-1_amd64.deb'; artifact.write_bytes(b'package')
            binary = {'path': 'usr/bin/vendor-test', 'bytes': 6, 'sha256': 'c'*64, 'mode': 0o755}
            license = {'path': recipe['licenses'][0]['destination'], 'bytes': 12, 'sha256': 'b'*64, 'mode': 0o644}
            value = {'package': recipe['package'], 'maintainer_scripts': [], 'control_files': ['control', 'md5sums'],
                'inputs': [{'package': 'vendor-test', 'version': '1.0', 'architecture': 'amd64', 'sha256': 'a'*64, 'selected': [binary]}],
                'payload': [binary, license], 'artifact': {'file': artifact.name, 'bytes': 7, 'sha256': hashlib.sha256(b'package').hexdigest()},
                'distribution': {'ID': 'debian', 'VERSION_ID': '13', 'VERSION_CODENAME': 'trixie'}}
            validate_receipt(value, recipe, root)
            changed = []
            item = copy.deepcopy(value); item['maintainer_scripts'] = ['postinst']; changed.append(item)
            item = copy.deepcopy(value); item['control_files'].append('triggers'); changed.append(item)
            item = copy.deepcopy(value); item['inputs'][0]['version'] = '2.0'; changed.append(item)
            item = copy.deepcopy(value); item['payload'].append(dict(binary, path='usr/bin/extra')); changed.append(item)
            item = copy.deepcopy(value); item['payload'][1]['sha256'] = 'd'*64; changed.append(item)
            item = copy.deepcopy(value); item['artifact']['file'] = '../escaped.deb'; changed.append(item)
            item = copy.deepcopy(value); item['artifact']['sha256'] = 'd'*64; changed.append(item)
            for item in changed:
                with self.subTest(item=item), self.assertRaises(ValueError): validate_receipt(item, recipe, root)
