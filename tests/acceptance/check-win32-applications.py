#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Freeze optional third-party QA inputs and use an accepted real-shell runtime."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import uuid


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--runtime-acceptance',type=Path,required=True)
    parser.add_argument('--inputs',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    source=args.source.resolve(strict=True)
    receipt_path=args.runtime_acceptance.resolve(strict=True)/'acceptance.json'
    receipt=json.loads(receipt_path.read_text())
    assert receipt['accepted'] and receipt.get('scenario')=='shell-icons' and not receipt['baseline']
    assert re.fullmatch(r'sha256:[0-9a-f]{64}',receipt['installed_image'])
    image=json.loads(subprocess.check_output(['docker','image','inspect',receipt['installed_image']],text=True))[0]
    assert image['Id']==receipt['installed_image'] and image['Os']=='linux' and image['Architecture']=='amd64'
    output=args.output.resolve();output.mkdir(parents=True,exist_ok=False)
    actors=output/'actors';actors.mkdir();inputs=output/'inputs';inputs.mkdir()
    manifest=source/'integrations/win32/tests/third-party-inputs.json'
    data=json.loads(manifest.read_text());assert data['schema']==1
    assert {r['id'] for r in data['inputs']}=={'7zip-32','7zip-64','notepadpp-32','notepadpp-64'}
    for row in data['inputs']:
        assert re.fullmatch(r'[A-Za-z0-9.+_-]+',row['file']) and re.fullmatch(r'[a-f0-9]{64}',row['sha256'])
        p=args.inputs.resolve(strict=True)/row['file']
        assert not p.is_symlink() and p.stat().st_size==row['bytes'] and digest(p)==row['sha256']
        shutil.copyfile(p,inputs/p.name)
        assert digest(inputs/p.name)==row['sha256']
    for name in ('third-party-acceptance.py','window-inspector.c','third-party-inputs.json'):
        shutil.copyfile(source/'integrations/win32/tests'/name,actors/name)
    shutil.copyfile(source/'integrations/compositor/tests/caption-buttons.py',actors/'caption-buttons.py')
    shutil.copyfile(source/'integrations/compositor/tests/foreign-icons-probe.c',actors/'foreign-icons-probe.c')
    shutil.copyfile(source/'shell/protocols/wlr-foreign-toplevel-management-unstable-v1.xml',actors/'wlr-icons.xml')
    report={'runtime_receipt_sha256':digest(receipt_path),'installed_image':image['Id'],
        'inputs':data['inputs'],'actor_inputs':{p.name:digest(p) for p in actors.iterdir()},
        'driver_sha256':digest(Path(__file__)),'native':receipt['native']}
    (output/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
    name='karyo-real-win32-applications-'+uuid.uuid4().hex
    command=['docker','run','--rm','--name',name,'--network','none','--read-only',
        '--cap-drop','ALL','--security-opt','no-new-privileges','--user','1001:1001',
        '--tmpfs','/tmp:rw,exec,nosuid,nodev,mode=1777',
        '--tmpfs','/home/win32qa:rw,exec,nosuid,nodev,uid=1001,gid=1001,mode=700',
        '--mount','type=bind,src='+str(actors)+',dst=/actors,readonly',
        '--mount','type=bind,src='+str(inputs)+',dst=/inputs,readonly',
        '--mount','type=bind,src='+str(output)+',dst=/output',image['Id'],
        'dbus-run-session','--','python3','-I','-B','/actors/third-party-acceptance.py','--output','/output/native']
    try:
        with (output/'native.log').open('wb') as log:
            code=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,timeout=420).returncode
    finally:
        subprocess.run(['docker','rm','-f',name],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=20)
    report['returncode']=code
    assert code==0,'Real application acceptance failed; inspect native.log and retained diagnostics'
    native=json.loads((output/'native/acceptance.json').read_text())
    assert native['accepted'] and native['real_wine_application'] and native['private_pointer'] and native['uid']==1001
    assert {r['program'] for r in native['frames']}=={r['id'] for r in data['inputs']}
    report.update(accepted=True,native_receipt_sha256=digest(output/'native/acceptance.json'))
    (output/'acceptance.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'accepted':True,'image':image['Id'],'programs':len(native['frames'])}),flush=True)


if __name__=='__main__':main()
