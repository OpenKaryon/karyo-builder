#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Verify reuse of an actual native Wine prefix in a captured disposable image."""
import argparse,hashlib,json,shutil,subprocess,uuid
from pathlib import Path

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--runtime-acceptance',type=Path,required=True)
    parser.add_argument('--launcher-package',type=Path)
    parser.add_argument('--prefix-arch',choices=('win32','win64'),required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--baseline',action='store_true')
    args=parser.parse_args()
    if args.baseline and (args.launcher_package or args.prefix_arch!='win32'):parser.error('The old-launcher baseline requires a native win32 prefix and no replacement package')
    receipt=args.runtime_acceptance.resolve(strict=True)/'acceptance.json';previous=json.loads(receipt.read_text())
    assert previous['accepted'],'Require previously accepted native runtime'
    image_info=json.loads(subprocess.check_output(['docker','image','inspect',previous['installed_image']],text=True))[0]
    assert image_info['Os']=='linux' and image_info['Architecture']=='amd64'
    output=args.output.resolve();output.mkdir(parents=True,exist_ok=False);actors=output/'actors';actors.mkdir()
    shutil.copyfile(args.source.resolve(strict=True)/'integrations/win32/tests/existing-prefix-acceptance.py',actors/'existing-prefix-acceptance.py')
    identity=uuid.uuid4().hex;image_id=image_info['Id'];package_record=None
    if args.launcher_package:
        folder=args.launcher_package.resolve(strict=True);manifest=folder/'manifest.json';record=json.loads(manifest.read_text())
        assert record['status']=='success' and record['recipe']['resolved']['package']['name']=='karyo-win32'
        binary=folder/record['artifact']['file'];assert digest(binary)==record['artifact']['sha256']
        query=['docker','run','--rm','--network','none','--read-only','--cap-drop','ALL','--security-opt','no-new-privileges','--user','1001:1001',image_id,'cat','/etc/os-release']
        release=dict(line.split('=',1) for line in subprocess.check_output(query,text=True).splitlines() if '=' in line)
        assert all(release[k].strip('"')==v for k,v in record['environment']['distribution'].items()),'Wrong native package base'
        context=output/'image';context.mkdir();shutil.copyfile(binary,context/'karyo-win32.deb')
        base='karyo-prefix-captured:'+identity;tag='karyo-prefix-installed:'+identity
        subprocess.run(['docker','image','tag',image_id,base],check=True)
        dockerfile='ARG BASE\nFROM ${BASE}\nUSER root\nCOPY karyo-win32.deb /tmp/karyo-win32.deb\nRUN echo "'+digest(binary)+'  /tmp/karyo-win32.deb" | sha256sum -c - && dpkg -i /tmp/karyo-win32.deb && dpkg -V karyo-win32\nUSER 1001:1001\n'
        (context/'Dockerfile').write_text(dockerfile)
        with (output/'build.log').open('wb') as log:subprocess.run(['docker','build','--network','none','--build-arg','BASE='+base,'-t',tag,str(context)],stdout=log,stderr=subprocess.STDOUT,check=True,timeout=180)
        image_id=subprocess.check_output(['docker','image','inspect',tag,'--format','{{.Id}}'],text=True).strip()
        package_record={'manifest_sha256':digest(manifest),'source_revision':record['source']['revision'],'sha256':digest(binary)}
    name='karyo-existing-prefix-'+identity
    command=['docker','run','--rm','--name',name,'--network','none','--read-only','--cap-drop','ALL','--security-opt','no-new-privileges','--user','1001:1001','--tmpfs','/tmp:rw,exec,nosuid,nodev,mode=1777','--tmpfs','/home/win32qa:rw,exec,nosuid,nodev,uid=1001,gid=1001,mode=700','--mount','type=bind,src='+str(actors)+',dst=/actors,readonly','--mount','type=bind,src='+str(output)+',dst=/output',image_id,'dbus-run-session','--','python3','-I','-B','/actors/existing-prefix-acceptance.py','--output','/output/native','--prefix-arch',args.prefix_arch]
    if args.baseline:command.append('--baseline')
    try:
        with (output/'native.log').open('wb') as log:code=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,timeout=420).returncode
    except subprocess.TimeoutExpired:code=124
    finally:subprocess.run(['docker','rm','-f',name],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=20)
    report={'runtime_receipt_sha256':digest(receipt),'base_image':image_info['Id'],'installed_image':image_id,'launcher':package_record,'baseline':args.baseline,'prefix_arch':args.prefix_arch,'actor_sha256':digest(actors/'existing-prefix-acceptance.py'),'returncode':code,'accepted':code==0}
    (output/('baseline.json' if args.baseline else 'acceptance.json')).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))
    if code:raise RuntimeError('Actual existing prefix acceptance failed')
if __name__=='__main__':main()
