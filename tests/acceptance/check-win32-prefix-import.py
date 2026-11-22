#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Upgrade an accepted Wine desktop with real pre-existing user data, then import."""
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
    parser.add_argument('--launcher-package',type=Path,required=True)
    parser.add_argument('--inputs',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--prepared-upgrade',type=Path,help='Reuse a verified immutable upgrade image; rerun all application checks.')
    args=parser.parse_args();source=args.source.resolve(strict=True)
    receipt_path=args.runtime_acceptance.resolve(strict=True)/'acceptance.json'
    previous=json.loads(receipt_path.read_text());assert previous['accepted']
    assert re.fullmatch(r'sha256:[a-f0-9]{64}',previous['installed_image'])
    base=json.loads(subprocess.check_output(['docker','image','inspect',previous['installed_image']],text=True))[0]
    assert base['Id']==previous['installed_image'] and base['Os']=='linux' and base['Architecture']=='amd64'
    output=args.output.resolve();output.mkdir(parents=True,exist_ok=False)
    context=output/'image';context.mkdir();actors=output/'actors';actors.mkdir();inputs=output/'inputs';inputs.mkdir()
    folder=args.launcher_package.resolve(strict=True);manifest_path=folder/'manifest.json'
    package=json.loads(manifest_path.read_text());assert package['status']=='success'
    metadata=package['recipe']['resolved']['package']
    assert metadata['name']=='karyo-win32' and metadata['version']=='0.1.0-2' and metadata['architecture']=='amd64'
    artifact=package['artifact'];assert re.fullmatch(r'[A-Za-z0-9.+_~-]+[.]deb',artifact['file'])
    binary=folder/artifact['file'];assert not binary.is_symlink() and binary.stat().st_size==artifact['bytes'] and digest(binary)==artifact['sha256']
    shutil.copyfile(binary,context/'karyo-win32.deb')
    row={'sha256':artifact['sha256'],'distribution':package['environment']['distribution'],
        'source_revision':package['source']['revision'],'manifest_sha256':digest(manifest_path)}
    (context/'package.json').write_text(json.dumps(row,indent=2)+'\n')
    checks=source/'integrations/win32/tests'
    for name in ('prefix-import-acceptance.py','prefix-upgrade-state.py'):
        shutil.copyfile(checks/name,actors/name)
    shutil.copyfile(checks/'prefix-upgrade-state.py',context/'prefix-upgrade-state.py')
    fixture=checks/'fixtures/legacy-win32-v012.py'
    assert hashlib.sha256(fixture.read_bytes().split(b'\n',2)[2]).hexdigest()=='e98f0c5ca047b611a7421d7a10f8ee00d20d7f53187964bba9c1b62ed1e855fb'
    shutil.copyfile(fixture,actors/fixture.name)
    for name in ('caption-buttons.py','foreign-icons-probe.c'):
        shutil.copyfile(source/'integrations/compositor/tests'/name,actors/name)
    shutil.copyfile(source/'shell/protocols/wlr-foreign-toplevel-management-unstable-v1.xml',actors/'wlr-icons.xml')
    selected=next(row for row in json.loads((checks/'third-party-inputs.json').read_text())['inputs'] if row['id']=='7zip-64')
    installer=args.inputs.resolve(strict=True)/selected['file']
    assert installer.stat().st_size==selected['bytes'] and digest(installer)==selected['sha256']
    shutil.copyfile(installer,inputs/installer.name)
    shutil.copyfile(Path(__file__).with_name('prefix-import-install.py'),context/'install.py')
    token=uuid.uuid4().hex;captured='karyo-prefix-upgrade-parent:'+token;tag='karyo-prefix-upgrade-installed:'+token
    subprocess.run(['docker','image','tag',base['Id'],captured],check=True)
    dockerfile='ARG BASE='+captured+'\nFROM ${BASE}\nUSER root\nCOPY karyo-win32.deb package.json prefix-upgrade-state.py install.py /tmp/karyo-prefix-import/\nRUN python3 -I -B /tmp/karyo-prefix-import/install.py\nUSER 1001:1001\n'
    (context/'Dockerfile').write_text(dockerfile)
    report={'base_image':base['Id'],'runtime_receipt_sha256':digest(receipt_path),
        'launcher':row,'input':selected,'actor_inputs':{p.name:digest(p) for p in actors.iterdir()},
        'driver_sha256':digest(Path(__file__)),'install_helper_sha256':digest(context/'install.py')}
    (output/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
    prepared=None
    if args.prepared_upgrade:
        prepared_path=args.prepared_upgrade.resolve(strict=True)/'acceptance.json'
        prepared=json.loads(prepared_path.read_text())
        assert prepared['accepted'] and prepared['base_image']==base['Id']
        assert prepared['launcher']==row and prepared['install_helper_sha256']==report['install_helper_sha256']
        assert re.fullmatch(r'sha256:[a-f0-9]{64}',prepared['installed_image'])
        image=prepared['installed_image']
        actual=json.loads(subprocess.check_output(['docker','image','inspect',image],text=True))[0]
        assert actual['Id']==image and actual['Os']=='linux' and actual['Architecture']=='amd64'
        report['prepared_upgrade_receipt_sha256']=digest(prepared_path)
    else:
        with (output/'build.log').open('wb') as log:
            subprocess.run(['docker','build','--network','none','--build-arg','BASE='+captured,
                '-t',tag,str(context)],check=True,stdout=log,stderr=subprocess.STDOUT,timeout=360)
        image=subprocess.check_output(['docker','image','inspect',tag,'--format','{{.Id}}'],text=True).strip()
    proof=json.loads(subprocess.check_output(['docker','run','--rm','--network','none','--read-only',
        '--cap-drop','ALL','--security-opt','no-new-privileges','--user','1001:1001',image,
        'cat','/usr/share/karyo-qa/upgrade-package.json'],text=True))
    if prepared is not None:assert proof==prepared['upgrade']
    assert proof['package']==row
    assert proof['user_data_unchanged'] and proof['old_version']=='0.1.0-1' and proof['new_version']=='0.1.0-2'
    report.update(installed_image=image,upgrade=proof)
    (output/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
    name='karyo-prefix-import-'+token
    command=['docker','run','--rm','--name',name,'--network','none','--read-only','--cap-drop','ALL',
        '--security-opt','no-new-privileges','--user','1001:1001',
        '--tmpfs','/tmp:rw,exec,nosuid,nodev,mode=1777',
        '--tmpfs','/home/win32qa:rw,exec,nosuid,nodev,uid=1001,gid=1001,mode=700',
        '--mount','type=bind,src='+str(actors)+',dst=/actors,readonly',
        '--mount','type=bind,src='+str(inputs)+',dst=/inputs,readonly',
        '--mount','type=bind,src='+str(output)+',dst=/output',image,
        'dbus-run-session','--','python3','-I','-B','/actors/prefix-import-acceptance.py','--output','/output/native']
    try:
        with (output/'native.log').open('wb') as log:
            code=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,timeout=420).returncode
    finally:
        subprocess.run(['docker','rm','-f',name],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=20)
    report['returncode']=code
    assert code==0,'Actual import acceptance failed; inspect retained build/native logs'
    native=json.loads((output/'native/acceptance.json').read_text())
    assert native['accepted'] and native['uid']==1001 and native['real_wine_application'] and not native['private_pointer']
    assert len(native['frames'])==4
    report.update(accepted=True,native_receipt_sha256=digest(output/'native/acceptance.json'))
    (output/'acceptance.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'accepted':True,'image':image,'stages':len(native['frames'])}),flush=True)


if __name__=='__main__':main()
