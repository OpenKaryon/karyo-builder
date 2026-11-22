#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Install captured native packages and exercise actual caption pixels/pointer."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import uuid


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--runtime-acceptance', type=Path, required=True)
    parser.add_argument('--compositor-package', type=Path, required=True)
    parser.add_argument('--wlroots-package', type=Path, required=True)
    parser.add_argument('--win32-package', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--baseline', action='store_true')
    parser.add_argument('--scenario', choices=('caption-buttons', 'rounded-frames'), default='caption-buttons')
    args = parser.parse_args()
    source = args.source.resolve(strict=True)
    previous_path = args.runtime_acceptance.resolve(strict=True) / 'acceptance.json'
    previous = json.loads(previous_path.read_text())
    assert previous.get('accepted') is True and re.fullmatch(r'sha256:[a-f0-9]{64}', previous.get('installed_image', ''))
    info = json.loads(subprocess.check_output(['docker', 'image', 'inspect', previous['installed_image']], text=True))[0]
    assert info['Os'] == 'linux' and info['Architecture'] == 'amd64'
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    context = output / 'image'
    context.mkdir()
    actors = output / 'actors'
    actors.mkdir()
    actor = actors / (args.scenario + '.py')
    shutil.copyfile(source / 'integrations/compositor/tests' / actor.name, actor)
    if args.scenario != 'caption-buttons':
        shutil.copyfile(source / 'integrations/compositor/tests/caption-buttons.py', actors / 'caption-buttons.py')
    rows = []

    def capture(folder, name, *, native=True, optional=False):
        folder = folder.resolve(strict=True)
        manifest = json.loads((folder / 'manifest.json').read_text())
        assert manifest['status'] == 'success'
        if native:
            assert manifest['kind'] == 'source-package'
            filename = manifest['binaries'][name]
            row = next(row for row in manifest['artifacts'] if row['file'] == filename and row.get('package') == name)
            assert row.get('architecture') == 'amd64'
            version = manifest['version']
        else:
            package = manifest['recipe']['resolved']['package']
            assert package['name'] == name and package['architecture'] == 'amd64'
            row = {**manifest['artifact'], 'package':name, 'architecture':'amd64'}
            filename = row['file']
            version = package['version']
        assert re.fullmatch(r'[A-Za-z0-9.+_~%-]+[.]deb', filename), filename
        path = folder / filename
        assert not path.is_symlink() and path.stat().st_size == row['bytes'] and digest(path) == row['sha256']
        assert not (context / filename).exists(), 'Aliased native artifact'
        shutil.copyfile(path, context / filename)
        rows.append({'distribution':manifest['environment']['distribution'], 'artifact':row,
            'version':version, 'only_if_installed':optional, 'manifest_sha256':digest(folder / 'manifest.json')})

    capture(args.compositor_package, 'labwc')
    library = json.loads((args.wlroots_package / 'manifest.json').read_text())
    names = [n for n in library['binaries'] if re.fullmatch(r'libwlroots-0[.](18|19)', n)]
    assert len(names) == 1
    capture(args.wlroots_package, names[0])
    if names[0] + '-dev' in library['binaries']:
        capture(args.wlroots_package, names[0] + '-dev', optional=True)
    capture(args.win32_package, 'karyo-win32', native=False)
    assert all(row['distribution'] == rows[0]['distribution'] for row in rows)
    (context / 'native.json').write_text(json.dumps(rows, indent=2) + '\n')
    (context / 'dependency-policy.json').write_text('{"check": false}\n')
    shutil.copyfile(Path(__file__).with_name('win32-palette-install.py'), context / 'install-native.py')
    assets = {p.name:digest(p) for p in (source / 'integrations/win32/theme').glob('*.svg')}
    assert set(assets) == {'close.svg', 'close_hover.svg', 'iconify.svg', 'max.svg', 'max_toggled.svg'}
    (context / 'assets.json').write_text(json.dumps(assets, sort_keys=True) + '\n')
    verify = "import hashlib,json,pathlib; expected=json.loads(pathlib.Path('/tmp/karyo-palette-native/assets.json').read_text()); folder=pathlib.Path('/usr/share/themes/Karyo-Windows/labwc'); assert {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.glob('*.svg')}==expected"
    identity = uuid.uuid4().hex
    captured = 'karyo-caption-buttons-captured:' + identity
    tag = 'karyo-caption-buttons-package:' + identity
    subprocess.run(['docker', 'image', 'tag', info['Id'], captured], check=True)
    lines = ['ARG BASE=karyo-caption-buttons-captured:unset', 'FROM ${BASE}', 'USER root',
        'COPY *.deb native.json dependency-policy.json assets.json install-native.py /tmp/karyo-palette-native/',
        'RUN python3 -I -B /tmp/karyo-palette-native/install-native.py',
        'RUN python3 -I -c ' + shlex.quote(verify), 'USER 1001:1001']
    (context / 'Dockerfile').write_text('\n'.join(lines) + '\n')
    with (output / 'build.log').open('wb') as log:
        subprocess.run(['docker', 'build', '--network', 'none', '--build-arg', 'BASE=' + captured,
            '-t', tag, str(context)], check=True, stdout=log, stderr=subprocess.STDOUT, timeout=180)
    image = subprocess.check_output(['docker', 'image', 'inspect', tag, '--format', '{{.Id}}'], text=True).strip()
    report = {'base_image':info['Id'], 'installed_image':image, 'native':rows, 'assets':assets,
        'actor_sha256':digest(actor), 'driver_sha256':digest(Path(__file__)),
        'runtime_receipt_sha256':digest(previous_path), 'baseline':args.baseline,
        'scenario':args.scenario, 'actor_inputs':{p.name:digest(p) for p in actors.iterdir()}}
    (output / 'progress.json').write_text(json.dumps(report, indent=2) + '\n')
    name = 'karyo-caption-buttons-' + identity
    command = ['docker', 'run', '--rm', '--name', name, '--network', 'none', '--read-only',
        '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges', '--user', '1001:1001',
        '--tmpfs', '/tmp:rw,exec,nosuid,nodev,mode=1777',
        '--tmpfs', '/home/win32qa:rw,exec,nosuid,nodev,uid=1001,gid=1001,mode=700',
        '--mount', 'type=bind,src=' + str(actors) + ',dst=/actors,readonly',
        '--mount', 'type=bind,src=' + str(output) + ',dst=/output', image,
        'dbus-run-session', '--', 'python3', '-I', '-B', '/actors/' + actor.name, '--output', '/output/native']
    if args.baseline:
        command.append('--baseline')
    try:
        with (output / 'native.log').open('wb') as log:
            code = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, timeout=120).returncode
    finally:
        subprocess.run(['docker', 'rm', '-f', name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=20)
    report['returncode'] = code
    assert code == 0, 'Caption checks failed; inspect retained native.log'
    native = json.loads((output / 'native/acceptance.json').read_text())
    assert native['accepted'] and native['baseline'] == args.baseline and native['uid'] == 1001
    report['accepted'] = True
    report['native_receipt_sha256'] = digest(output / 'native/acceptance.json')
    (output / ('baseline.json' if args.baseline else 'acceptance.json')).write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'accepted':True, 'baseline':args.baseline, 'image':image}), flush=True)


if __name__ == '__main__':
    main()
