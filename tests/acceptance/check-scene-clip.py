#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Exercise native scene masks with an old-header binary and real renderer pixels."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import uuid


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')


def build(context, base, tag, log):
    with log.open('wb') as stream:
        subprocess.run(['docker', 'build', '--network', 'none', '--build-arg',
                        'BASE=' + base, '-t', tag, str(context)], stdout=stream,
                       stderr=subprocess.STDOUT, check=True, timeout=180)
    return subprocess.check_output(['docker', 'image', 'inspect', tag,
                                    '--format', '{{.Id}}'], text=True).strip()


def run(image, command, mount=None):
    name = 'karyo-scene-clip-run-' + uuid.uuid4().hex
    args = ['docker', 'run', '--rm', '--name', name, '--network', 'none', '--read-only',
            '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges',
            '--cpus', '2', '--memory', '2g', '--pids-limit', '128',
            '--user', '1001:1001', '--tmpfs', '/tmp:rw,nosuid,nodev,mode=1777']
    if mount:
        args.extend(['--mount', 'type=bind,src=' + str(mount) + ',dst=/output'])
    try:
        return subprocess.run([*args, image, *command], stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, timeout=90)
    finally:
        subprocess.run(['docker', 'rm', '-f', name], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, timeout=20)


def metadata(image, abi):
    code = r"""from pathlib import Path
import hashlib,json,re,subprocess
root=Path(subprocess.check_output(['pkg-config','--variable=libdir',ABI],text=True).strip())
lib=root/('lib'+ABI+'.so')
exports=subprocess.check_output(['nm','-D','--defined-only','--format=posix',str(lib)],text=True)
dynamic=subprocess.check_output(['readelf','-d',str(lib)],text=True)
name=re.search(r'Library soname: \[(.*?)\]',dynamic)
assert name
binary=Path('/usr/local/libexec/karyo-qa/scene-clip-probe')
print(json.dumps({'soname':name[1],'exports':sorted({line.split()[0] for line in exports.splitlines()}),'library_sha256':hashlib.sha256(lib.read_bytes()).hexdigest(),'probe_sha256':hashlib.sha256(binary.read_bytes()).hexdigest()}))
""".replace('ABI', repr(abi))
    result = run(image, ['python3', '-I', '-B', '-c', code])
    require(result.returncode == 0, result.stdout.decode(errors='replace'))
    return json.loads(result.stdout)


def matrix(image, folder, mode):
    folder.mkdir()
    rows = []
    for scale in (1, 2):
        for transform in (0, 1):
            label = f'scale{scale}-transform{transform}'
            case = folder / label
            case.mkdir()
            command = ['/usr/local/libexec/karyo-qa/scene-clip-probe', '/output',
                       str(scale), str(transform), mode]
            result = run(image, command, case)
            (case / 'native.log').write_bytes(result.stdout)
            records = [json.loads(line) for line in result.stdout.decode(errors='replace').splitlines()
                       if line.startswith('{')]
            require(result.returncode == 0, 'Native scene case failed: ' + str(case))
            require(records and records[-1].get('accepted') is True,
                    'Missing complete native acceptance: ' + label)
            require(records[-1]['baseline'] == (mode == 'baseline'), 'Wrong native case mode')
            stages = [row for row in records if 'stage' in row]
            require(len(stages) == records[-1]['phases'], 'Missing native stages')
            require(all(row['pixel_errors'] == row['input_errors'] == 0 for row in stages),
                    'Actual pixel or input mismatch')
            names = {row['stage']: row for row in stages}
            required = {'unclipped', 'disabled-child', 'enabled-child', 'destroyed-child'}
            if mode == 'positive':
                required.update({'copied-child-clip', 'complex-hole', 'restore-corners',
                                 'nested-parent-clip', 'moved-nested-clips', 'clear-parent',
                                 'reparented-clip', 'reparented-back', 'empty-child', 'clear-child',
                                 'mask-before-hide'})
            require(required <= names.keys(), 'Missing required scene lifecycle stages')
            if scale == 1 and transform == 0:
                require(names['scanout-unclipped']['sampled'] and
                        names['scanout-unclipped']['direct_scanout'], 'No real baseline scanout path')
                if mode == 'positive':
                    require(names['scanout-clipped']['sampled'] and
                            not names['scanout-clipped']['direct_scanout'], 'Clipped node was scanned out')
                    require(names['scanout-cleared']['sampled'] and
                            names['scanout-cleared']['direct_scanout'], 'Clearing clip did not restore scanout')
            frames = {p.name: digest(p) for p in case.glob('*.ppm')}
            require(required <= {p.stem for p in case.glob('*.ppm')}, 'Missing actual output frames')
            receipt = {'case': label, 'abi': records[0]['abi'], 'result': records[-1],
                       'frames': frames, 'native_log_sha256': digest(case / 'native.log')}
            save(case / 'acceptance.json', receipt)
            rows.append(receipt)
            save(folder / 'progress.json', {'cases': rows})
            print(mode, label, records[-1]['phases'], flush=True)
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--package-directory', type=Path, required=True)
    parser.add_argument('--sdk-image', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    folder = args.package_directory.resolve(strict=True)
    manifest_path = folder / 'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    require(manifest['kind'] == 'source-package' and manifest['status'] == 'success' and
            manifest['architecture'] == 'amd64',
            'Require a successful native amd64 source build')
    libraries = [name for name in manifest['binaries']
                 if re.fullmatch(r'libwlroots-0[.](18|19)', name)]
    require(len(libraries) == 1, 'Require exactly one supported native library')
    package = libraries[0]
    abi = package.removeprefix('lib')
    sdk = json.loads(subprocess.check_output(['docker', 'image', 'inspect',
                                             args.sdk_image], text=True))[0]
    require(sdk['Os'] == 'linux' and sdk['Architecture'] == 'amd64', 'Native Linux amd64 SDK required')
    require(sdk['Id'] == manifest['environment']['image_id'], 'Use the captured native SDK image')
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    before_context = output / 'before-image'
    before_context.mkdir()
    source = args.source.resolve(strict=True) / 'integrations/compositor/tests/scene-clip-probe.c'
    copied_source = before_context / source.name
    shutil.copyfile(source, copied_source)
    producer = copied_source.read_text()
    abi_function = producer[producer.index('static void abi(void)'):producer.index('int main(')]
    abi_source = ('// SPDX-License-Identifier: GPL-3.0-or-later\n#define _POSIX_C_SOURCE 200809L\n#include <stdio.h>\n'
                  '#include <stddef.h>\n#include <wlr/types/wlr_scene.h>\n' + abi_function +
                  'int main(void) { abi(); return 0; }\n')
    (before_context / 'abi.c').write_text(abi_source)
    identity = uuid.uuid4().hex
    sdk_tag = 'karyo-scene-clip-sdk:' + identity
    subprocess.run(['docker', 'image', 'tag', sdk['Id'], sdk_tag], check=True)
    flags = '$(pkg-config --cflags --libs ' + abi + ' pixman-1 wayland-server libdrm) -lm -ldl'
    dockerfile = ('ARG BASE=karyo-scene-clip-captured:unset\nFROM ${BASE}\nUSER root\n'
                  'COPY scene-clip-probe.c abi.c /usr/share/karyo-qa/\n'
                  'RUN mkdir -p /usr/local/libexec/karyo-qa && '
                  'cc -std=c11 -Wall -Wextra -Werror -DWLR_USE_UNSTABLE '
                  '/usr/share/karyo-qa/scene-clip-probe.c '
                  '-o /usr/local/libexec/karyo-qa/scene-clip-probe ' + flags + '\n'
                  'USER 1001:1001\n')
    (before_context / 'Dockerfile').write_text(dockerfile)
    before = build(before_context, sdk_tag, 'karyo-scene-clip-before:' + identity,
                   output / 'before-build.log')
    before_meta = metadata(before, abi)
    baseline = matrix(before, output / 'baseline', 'baseline')
    context = output / 'after-image'
    context.mkdir()
    selected = []
    for name in (package, package + '-dev'):
        filename = manifest['binaries'][name]
        require(re.fullmatch(r'[A-Za-z0-9+_.~%-]+[.]deb', filename), 'Unsafe native filename')
        artifact = next(row for row in manifest['artifacts'] if row['file'] == filename)
        path = folder / filename
        require(path.is_file() and not path.is_symlink() and
                artifact.get('package') == name and artifact.get('architecture') == 'amd64' and
                path.stat().st_size == artifact['bytes'] and digest(path) == artifact['sha256'],
                'Changed, aliased or non-native artifact')
        shutil.copyfile(path, context / filename)
        selected.append(filename)
    checks = ''.join(digest(context / name) + '  ' + name + '\n' for name in selected)
    (context / 'SHA256SUMS').write_text(checks)
    lines = ['ARG BASE=karyo-scene-clip-captured:unset', 'FROM ${BASE}', 'USER root']
    lines.extend('COPY ' + name + ' /tmp/scene-clip/' for name in [*selected, 'SHA256SUMS'])
    lines.append('RUN cd /tmp/scene-clip && sha256sum -c SHA256SUMS && dpkg -i ./*.deb && '
                 'dpkg -V ' + package + ' ' + package + '-dev && apt-get check && '
                 'cc -std=c11 -Wall -Wextra -Werror -DWLR_USE_UNSTABLE /usr/share/karyo-qa/abi.c '
                 '-o /usr/local/libexec/karyo-qa/scene-abi $(pkg-config --cflags --libs ' + abi + ')')
    lines.append('USER 1001:1001')
    (context / 'Dockerfile').write_text('\n'.join(lines) + '\n')
    after = build(context, 'karyo-scene-clip-before:' + identity,
                  'karyo-scene-clip-after:' + identity, output / 'after-build.log')
    after_meta = metadata(after, abi)
    require(after_meta['probe_sha256'] == before_meta['probe_sha256'], 'Old-header binary changed')
    require(after_meta['soname'] == before_meta['soname'], 'Native SONAME changed')
    require(set(after_meta['exports']) == set(before_meta['exports']) | {'wlr_scene_node_set_clip_region'},
            'Old exports changed or unexpected symbols were added')
    require('wlr_scene_node_set_clip_region' not in before_meta['exports'], 'Baseline already has clip API')
    abi_result = run(after, ['/usr/local/libexec/karyo-qa/scene-abi'])
    require(abi_result.returncode == 0, 'New-header ABI probe failed')
    new_abi = json.loads(abi_result.stdout)['abi']
    require(all(row['abi'] == new_abi for row in baseline), 'Public structure layout changed')
    positive = matrix(after, output / 'positive', 'positive')
    require(all(row['abi'] == new_abi for row in positive), 'Old binary observed incompatible ABI')
    report = {'accepted': True, 'source_sha256': digest(copied_source),
              'native_manifest_sha256': digest(manifest_path), 'version': manifest['version'],
              'sdk_image': sdk['Id'], 'before_image': before, 'installed_image': after,
              'before': before_meta, 'after': after_meta, 'new_header_abi': new_abi,
              'baseline': baseline, 'positive': positive}
    save(output / 'acceptance.json', report)
    print('accepted', manifest['version'], flush=True)


if __name__ == '__main__':
    main()
