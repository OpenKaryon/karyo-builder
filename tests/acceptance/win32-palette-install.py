#!/usr/bin/python3 -I
# SPDX-License-Identifier: GPL-3.0-or-later
"""Install captured native QA packages only inside a disposable image build."""
import hashlib
import json
import os
from pathlib import Path
import subprocess

def main():
    if not hasattr(os, 'getuid') or os.getuid() != 0:
        raise SystemExit('This helper is only for a disposable native image build')
    release = dict((line.split('=', 1) for line in Path('/etc/os-release').read_text().splitlines() if '=' in line))
    rows = json.loads(Path('/tmp/karyo-palette-native/native.json').read_text())
    names = []
    packages = []
    for row in rows:
        assert all((release[key].strip(chr(34)) == value for key, value in row['distribution'].items())), 'Wrong native base'
        artifact = row['artifact']
        path = Path('/tmp/karyo-palette-native') / artifact['file']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == artifact['sha256'], 'Changed native package'
        actual = subprocess.check_output(['dpkg-deb', '-f', str(path), 'Package', 'Version', 'Architecture'], text=True)
        fields = dict((line.split(': ', 1) for line in actual.splitlines()))
        assert fields == {'Package': artifact['package'], 'Version': row['version'], 'Architecture': 'amd64'}, 'Wrong native metadata'
        if row.get('only_if_installed'):
            status = subprocess.run(['dpkg-query', '-W', '-f=${db:Status-Status}', artifact['package']],
                capture_output=True, text=True)
            if status.returncode or status.stdout.strip() in ('not-installed', 'config-files', ''):
                continue
        names.append(artifact['package'])
        packages.append(str(path))
    if json.loads(Path('/tmp/karyo-palette-native/dependency-policy.json').read_text())['check']:
        library = next((row for row in rows if row['artifact']['package'].startswith('libwlroots-')))
        compositor = next((row for row in rows if row['artifact']['package'] == 'labwc'))
        library_name = library['artifact']['package']
        required = library['version']
        installed = subprocess.check_output(['dpkg-query', '-W', '-f=${Version}', library_name], text=True).strip()
        assert installed != required, 'Negative dependency check needs the earlier native runtime'
        comp_path = str(Path('/tmp/karyo-palette-native') / compositor['artifact']['file'])
        depends = subprocess.check_output(['dpkg-deb', '-f', comp_path, 'Depends'], text=True)
        assert library_name + ' (= ' + required + ')' in depends, 'Exact native owner-hints dependency is missing'
        rejected = subprocess.run(['dpkg', '-i', comp_path], capture_output=True, text=True)
        assert rejected.returncode != 0 and library_name in rejected.stderr and (required in rejected.stderr) and ('dependency' in rejected.stderr.lower()), 'Compositor did not reject its earlier library for the expected reason'
        status = subprocess.check_output(['dpkg-query', '-W', '-f=${Status}', 'labwc'], text=True).strip()
        assert status == 'install ok unpacked', 'Unexpected package failure instead of a dependency rejection'
        receipt = Path('/usr/share/karyo-qa/owner-dependency.json')
        receipt.parent.mkdir(parents=True, exist_ok=True)
        receipt.write_text(json.dumps({'accepted': True, 'library': library_name, 'required': required, 'previous': installed, 'rejected_returncode': rejected.returncode, 'compositor_version': compositor['version']}) + chr(10))
    subprocess.run(['dpkg', '-i', *packages], check=True)
    subprocess.run(['dpkg', '-V', *names], check=True)
    subprocess.run(['apt-get', 'check'], check=True)
if __name__ == '__main__':
    main()
