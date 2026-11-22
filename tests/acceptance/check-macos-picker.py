#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Install native macOS components and exercise the actual Wayland/MIME frontend."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import uuid


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def package(folder,name,versions,context,filename):
    manifest=folder.resolve(strict=True)/'manifest.json';row=json.loads(manifest.read_text())
    assert row['status']=='success'
    control=row['recipe']['resolved']['package']
    assert control['name']==name and control['version'] in versions and control['architecture']=='amd64'
    artifact=row['artifact'];assert re.fullmatch(r'[A-Za-z0-9.+_~-]+[.]deb',artifact['file'])
    binary=manifest.parent/artifact['file']
    assert not binary.is_symlink() and binary.stat().st_size==artifact['bytes'] and digest(binary)==artifact['sha256']
    shutil.copyfile(binary,context/filename)
    return {'control':control,'artifact':artifact,'source':row['source'],'distribution':row['environment']['distribution'],
            'manifest_sha256':digest(manifest),'file':filename}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('source','runtime-acceptance','core-package','picker-package','output'):
        parser.add_argument('--'+name,type=Path,required=True)
    args=parser.parse_args();source=args.source.resolve(strict=True)
    parent_path=args.runtime_acceptance.resolve(strict=True)/'acceptance.json'
    parent=json.loads(parent_path.read_text());assert parent['accepted']
    assert re.fullmatch(r'sha256:[a-f0-9]{64}',parent['installed_image'])
    image=json.loads(subprocess.check_output(['docker','image','inspect',parent['installed_image']],text=True))[0]
    assert image['Id']==parent['installed_image'] and image['Os']=='linux' and image['Architecture']=='amd64'
    output=args.output.resolve();output.mkdir(parents=True,exist_ok=False)
    context=output/'image';context.mkdir();actors=output/'actors';actors.mkdir()
    packages={'core':package(args.core_package,'karyo-macos-core',('0.1.0-2',),context,'core.deb'),
              'picker':package(args.picker_package,'karyo-macos',('0.1.0-1','0.1.0-2'),context,'picker.deb')}
    assert packages['core']['source']==packages['picker']['source']
    assert packages['core']['distribution']==packages['picker']['distribution']
    (context/'package.json').write_text(json.dumps(packages,indent=2)+'\n')
    for name in ('installed-picker-acceptance.py','window-action-probe.c'):
        shutil.copyfile(source/'integrations/macos/tests'/name,actors/name)
    shutil.copyfile(source/'integrations/compositor/tests/caption-buttons.py',actors/'caption-buttons.py')
    shutil.copyfile(source/'shell/protocols/wlr-foreign-toplevel-management-unstable-v1.xml',actors/'wlr-icons.xml')
    shutil.copyfile(Path(__file__).with_name('macos-picker-install.py'),context/'install.py')
    token=uuid.uuid4().hex;captured='karyo-macos-picker-parent:'+token;tag='karyo-macos-picker-installed:'+token
    subprocess.run(['docker','image','tag',image['Id'],captured],check=True)
    (context/'Dockerfile').write_text('ARG BASE='+captured+'\nFROM ${BASE}\nUSER root\nCOPY core.deb picker.deb package.json install.py /tmp/karyo-macos-gui/\nRUN python3 -I -B /tmp/karyo-macos-gui/install.py\nUSER 1001:1001\n')
    report={'base_image':image['Id'],'parent_receipt_sha256':digest(parent_path),'packages':packages,
        'actor_inputs':{p.name:digest(p) for p in actors.iterdir()},'driver_sha256':digest(Path(__file__)),
        'install_helper_sha256':digest(context/'install.py')}
    (output/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
    with (output/'build.log').open('wb') as log:
        subprocess.run(['docker','build','--network','none','-t',tag,str(context)],check=True,stdout=log,stderr=subprocess.STDOUT,timeout=180)
    installed=subprocess.check_output(['docker','image','inspect',tag,'--format','{{.Id}}'],text=True).strip()
    proof=json.loads(subprocess.check_output(['docker','run','--rm','--network','none','--read-only','--user','1001:1001',
        '--cap-drop','ALL','--security-opt','no-new-privileges',installed,'cat','/usr/share/karyo-qa/macos-picker-packages.json'],text=True))
    assert proof['packages']==packages and proof['user_data_unchanged'] and proof['windows_defaults_unchanged'] and proof['directory_default_unchanged']
    report.update(installed_image=installed,install_proof=proof)
    (output/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
    name='karyo-macos-picker-'+token
    try:
        with (output/'native.log').open('wb') as log:
            result=subprocess.run(['docker','run','--rm','--name',name,'--network','none','--read-only','--user','1001:1001',
                '--cap-drop','ALL','--security-opt','no-new-privileges','--tmpfs','/tmp:rw,exec,nosuid,nodev,mode=1777',
                '--tmpfs','/home/win32qa:rw,exec,nosuid,nodev,uid=1001,gid=1001,mode=700',
                '--mount','type=bind,src='+str(actors)+',dst=/actors,readonly',
                '--mount','type=bind,src='+str(output)+',dst=/output',installed,'dbus-run-session','--',
                'python3','-I','-B','/actors/installed-picker-acceptance.py','--output','/output/native'],
                stdout=log,stderr=subprocess.STDOUT,timeout=180)
    finally:
        subprocess.run(['docker','rm','-f',name],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=20)
    assert result.returncode==0,'Installed Wayland macOS picker gate failed; inspect retained logs'
    native=json.loads((output/'native/acceptance.json').read_text())
    assert native['accepted'] and native['uid']==1001 and not native['private_pointer'] and not native['real_wine_application']
    assert len(native['frames'])==5 and native['frames'][-1]['fixture_only'] and not native['frames'][-1]['darling_runtime_proven']
    report.update(accepted=True,fixture_only=True,darling_runtime_proven=False,
        native_receipt_sha256=digest(output/'native/acceptance.json'))
    (output/'acceptance.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'accepted':True,'image':installed,'native_wayland':True,'fixture_only':True}),flush=True)


if __name__=='__main__':main()
