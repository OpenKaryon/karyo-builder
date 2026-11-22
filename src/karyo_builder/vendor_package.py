# SPDX-License-Identifier: GPL-3.0-or-later
"""Build inert optional vendor data packages in a native offline container."""
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import uuid

from . import __version__
from .cli import command, mount, sha256
from .container import validate_target
from .vendor_recipe import capture_recipe


def validate_receipt(result, recipe, staged):
    if (result['package'] != recipe['package'] or result['maintainer_scripts'] != []
            or result['control_files'] != ['control', 'md5sums']):
        raise ValueError('Vendor result changed metadata or contains control hooks')
    if len(result['inputs']) != len(recipe['inputs']): raise ValueError('Vendor input receipt is incomplete')
    expected = set()
    for actual, wanted in zip(result['inputs'], recipe['inputs']):
        if any(actual[key] != wanted[key] for key in ('package', 'version', 'architecture', 'sha256')):
            raise ValueError('Vendor input identity changed')
        if {r['path'] for r in actual['selected']} != set(wanted['files']):
            raise ValueError('Vendor selected files differ from recipe')
        expected.update(wanted['files'])
    expected.update(r['destination'] for r in recipe['licenses'])
    paths = [r['path'] for r in result['payload']]
    if len(set(paths)) != len(paths) or set(paths) != expected:
        raise ValueError('Vendor payload is not the exact declared file selection')
    for record in result['payload']:
        if (not re.fullmatch(r'[a-f0-9]{64}', record['sha256']) or type(record['bytes']) is not int
                or record['bytes'] <= 0 or type(record['mode']) is not int or record['mode'] not in (0o644, 0o755)):
            raise ValueError('Invalid vendor payload receipt')
    by_path = {record['path']: record for record in result['payload']}
    for value in result['inputs']:
        if any(record != by_path[record['path']] for record in value['selected']):
            raise ValueError('Vendor input and final payload receipts disagree')
    for value in recipe['licenses']:
        if by_path[value['destination']]['sha256'] != value['sha256'] or by_path[value['destination']]['mode'] != 0o644:
            raise ValueError('Vendor license differs from the captured input')
    item = result['artifact']; name = item['file']; metadata = recipe['package']
    expected_name = metadata['name']+'_'+metadata['version'].replace(':', '%3a')+'_amd64.deb'
    if name != expected_name: raise ValueError('Vendor artifact filename differs from recipe')
    artifact = staged/name
    if (artifact.is_symlink() or not artifact.is_file() or sha256(artifact) != item['sha256']
            or type(item['bytes']) is not int or artifact.stat().st_size != item['bytes']):
        raise ValueError('Vendor artifact differs from native receipt')
    validate_target('\n'.join(f'{key}={value}' for key, value in result['distribution'].items()))
    return item


def build_vendor_package(args):
    with tempfile.TemporaryDirectory(prefix='karyo-vendor-') as temporary:
        inputs = Path(temporary)/'input'
        recipe, captured, recipe_hash = capture_recipe(args.recipe, inputs)
        module = inputs/'karyo_builder'; module.mkdir(); hashes = {}
        for name in ('__init__.py', 'vendor_container.py', 'vendor_recipe.py', 'recipe.py', 'container.py', 'dependencies.py'):
            shutil.copyfile(Path(__file__).with_name(name), module/name); hashes[name] = sha256(module/name)
        image = json.loads(command(['docker', 'image', 'inspect', args.image]))[0]; image_id = image['Id']
        if image.get('Os') != 'linux' or image.get('Architecture') != 'amd64' or not image_id.startswith('sha256:'):
            raise ValueError('A local immutable Linux amd64 build image is required')
        output = Path(args.output).resolve(); output.mkdir(parents=True, exist_ok=True)
        job = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
        staged = output/('.partial-vendor-'+job); staged.mkdir()
        try:
            invocation = ['docker', 'run', '--rm', '--network=none', '--cpus', str(args.jobs), '--memory=2g',
                '--pids-limit=128', '--cap-drop=ALL', '--security-opt=no-new-privileges',
                '--mount', mount(inputs, '/input'), '--mount', mount(staged, '/output', readonly=False),
                '--workdir=/input', '--env', 'HOME=/tmp/home', '--env', 'LANG=C.UTF-8',
                '--env', 'SOURCE_DATE_EPOCH='+str(recipe['source_date_epoch']), '--env', 'DPKG_DEB_THREADS_MAX='+str(args.jobs),
                '--entrypoint', 'python3', image_id, '-m', 'karyo_builder.vendor_container']
            with (staged/'build.log').open('wb') as log:
                result = subprocess.run(invocation, stdout=log, stderr=subprocess.STDOUT)
            if result.returncode: raise RuntimeError('Vendor repack exited with status '+str(result.returncode))
            receipt = json.loads((staged/'result.json').read_text()); artifact = validate_receipt(receipt, recipe, staged)
            manifest = {'schema': 1, 'kind': 'vendor-package', 'status': 'success', 'builder_version': __version__,
                'recipe_sha256': recipe_hash, 'resolved': recipe, 'captured_inputs': captured, 'runner_sha256': hashes,
                'environment': {'image_id': image_id, 'distribution': receipt['distribution'],
                    'packages_sha256': sha256(staged/'environment.txt')}, 'receipt': receipt,
                'build_log_sha256': sha256(staged/'build.log'),
                'validation': {'input_hashes': 'passed', 'vendor_identity': 'passed', 'maintainer_scripts': 'absent', 'dpkg_deb': 'passed'}}
            (staged/'manifest.json').write_bytes((json.dumps(manifest, indent=2)+'\n').encode())
            (staged/'SHA256SUMS').write_bytes((artifact['sha256']+'  '+artifact['file']+'\n').encode())
            shutil.copyfile(inputs/'original-recipe.json', staged/'original-recipe.json')
            final = output/(recipe['package']['name']+'-'+job)
            if final.parent != output or staged.parent != output: raise ValueError('Vendor output escaped selected directory')
            staged.rename(final)
        except BaseException:
            failed = output/('.failed-vendor-'+job)
            if failed.parent != output or staged.parent != output: raise ValueError('Failed vendor output escaped selected directory')
            staged.rename(failed); print('Failed vendor repack retained at '+str(failed)); raise
    print('Vendor package and build record: '+str(final))
    return 0
