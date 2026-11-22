# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline native data-only vendor repack; upstream scripts are inspected, not run."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tarfile

if __package__:
    from .container import validate_target
    from .vendor_recipe import validate_recipe, payload_path
else:
    from container import validate_target
    from karyo_builder.vendor_recipe import validate_recipe, payload_path

MAX_PAYLOAD = 256 * 1024 * 1024


def digest(path):
    with Path(path).open('rb') as stream: return hashlib.file_digest(stream, 'sha256').hexdigest()


def select_members(archive, payload, selected):
    """Copy only exact regular files into fresh directories; never extract links."""
    selected = {payload_path(value) for value in selected}; seen = set(); records = []; total = 0
    for member in archive:
        name = member.name.removeprefix('./')
        if name not in selected: continue
        if name in seen or not member.isreg() or member.mode & 0o7022:
            raise ValueError('Selected vendor files must be unique ordinary non-writable files')
        seen.add(name); total += member.size
        if not 0 < member.size <= MAX_PAYLOAD or total > MAX_PAYLOAD:
            raise ValueError('Selected vendor payload is too large or empty')
        target = payload/name; target.parent.mkdir(parents=True, exist_ok=True)
        mode = 0o755 if member.mode & 0o111 else 0o644
        with archive.extractfile(member) as reader, target.open('xb') as writer:
            remaining = member.size
            while remaining:
                data = reader.read(min(1024 * 1024, remaining))
                if not data: raise ValueError('Truncated vendor payload')
                writer.write(data); remaining -= len(data)
        target.chmod(mode)
        records.append({'path': name, 'bytes': member.size, 'sha256': digest(target), 'mode': mode})
    if seen != selected: raise ValueError('Vendor archive is missing selected payload files')
    return records


def native_tar(package, role, callback):
    with subprocess.Popen(['dpkg-deb', role, str(package)], stdout=subprocess.PIPE) as process:
        try:
            with tarfile.open(fileobj=process.stdout, mode='r|') as archive: result = callback(archive)
            # Drain input so dpkg-deb completes even after the tar end marker.
            while process.stdout.read(1024 * 1024): pass
            if process.wait() != 0: raise RuntimeError('Cannot read vendor Debian archive')
            return result
        except BaseException:
            process.kill(); process.wait(); raise


def control_inventory(archive):
    records = []
    for member in archive:
        name = member.name.removeprefix('./')
        if member.isdir(): continue
        value = {'path': name, 'bytes': member.size, 'type': member.type.decode('ascii', 'replace')}
        if member.isreg():
            if member.size > 1024 * 1024: raise ValueError('Vendor control file is too large')
            value['sha256'] = hashlib.sha256(archive.extractfile(member).read()).hexdigest()
        records.append(value)
    return records


def main():
    recipe = json.loads(Path('/input/vendor-recipe.json').read_text()); validate_recipe(recipe)
    distribution = validate_target(Path('/etc/os-release').read_text())
    assert subprocess.check_output(['dpkg', '--print-architecture'], text=True).strip() == 'amd64'
    payload = Path('/tmp/vendor-payload'); payload.mkdir()
    inputs = []; files = []
    for item in recipe['inputs']:
        path = Path(item['path'])
        if digest(path) != item['sha256']: raise ValueError('Captured vendor DEB hash changed')
        actual = {key: subprocess.check_output(['dpkg-deb', '--field', str(path), field], text=True).strip()
                  for key, field in (('package', 'Package'), ('version', 'Version'), ('architecture', 'Architecture'))}
        if any(actual[key] != item[key] for key in actual): raise ValueError('Vendor DEB identity differs from recipe')
        control = native_tar(path, '--ctrl-tarfile', control_inventory)
        extracted = native_tar(path, '--fsys-tarfile', lambda archive: select_members(archive, payload, item['files']))
        files.extend(extracted); inputs.append(dict(actual, sha256=item['sha256'], control_omitted=control, selected=extracted))
    for item in recipe['licenses']:
        path = Path(item['path'])
        if digest(path) != item['sha256']: raise ValueError('Captured license hash changed')
        target = payload/item['destination']; target.parent.mkdir(parents=True, exist_ok=True)
        with path.open('rb') as reader, target.open('xb') as writer: writer.write(reader.read())
        target.chmod(0o644)
        files.append({'path': item['destination'], 'bytes': path.stat().st_size, 'sha256': item['sha256'], 'mode': 0o644})
    metadata = recipe['package']; control_dir = payload/'DEBIAN'; control_dir.mkdir()
    control = [f'Package: {metadata["name"]}', f'Version: {metadata["version"]}', 'Architecture: amd64',
        f'Section: {metadata["section"]}', 'Priority: optional', f'Maintainer: {metadata["maintainer"]}',
        f'Description: {metadata["description"]}']
    for key in ('depends', 'provides', 'conflicts'):
        if metadata.get(key): control.append(key.capitalize()+': '+', '.join(metadata[key]))
    (control_dir/'control').write_text('\n'.join(control)+'\n')
    checksums = []
    for record in sorted(files, key=lambda r: r['path']):
        with (payload/record['path']).open('rb') as stream: value = hashlib.file_digest(stream, lambda: hashlib.md5(usedforsecurity=False)).hexdigest()
        checksums.append(value+'  '+record['path'])
    (control_dir/'md5sums').write_text('\n'.join(checksums)+'\n')
    epoch = recipe['source_date_epoch']
    for path in [*payload.rglob('*'), payload]: os.utime(path, (epoch, epoch))
    filename = metadata['name']+'_'+metadata['version'].replace(':', '%3a')+'_amd64.deb'
    artifact = Path('/output')/filename
    subprocess.run(['dpkg-deb', '--build', '--root-owner-group', str(payload), str(artifact)], check=True)
    control_files = native_tar(artifact, '--ctrl-tarfile', control_inventory)
    if sorted(r['path'] for r in control_files) != ['control', 'md5sums']:
        raise ValueError('Repacked output unexpectedly contains control hooks')
    subprocess.run(['dpkg-deb', '--info', str(artifact)], check=True)
    subprocess.run(['dpkg-deb', '--contents', str(artifact)], check=True)
    result = {'package': metadata, 'artifact': {'file': filename, 'bytes': artifact.stat().st_size, 'sha256': digest(artifact)},
              'inputs': inputs, 'payload': sorted(files, key=lambda r: r['path']), 'maintainer_scripts': [],
              'control_files': ['control', 'md5sums'], 'distribution': distribution}
    Path('/output/result.json').write_text(json.dumps(result, indent=2)+'\n')
    environment = subprocess.check_output(['dpkg-query', '-W', '-f=${binary:Package}=${Version}\n'], text=True)
    Path('/output/environment.txt').write_text(environment)


if __name__ == '__main__': main()
