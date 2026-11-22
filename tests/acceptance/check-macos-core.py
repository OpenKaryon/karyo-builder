#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Install a captured native core package and exercise its ordinary-user CLI."""
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
    parser.add_argument('--package',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    parent_path=args.runtime_acceptance.resolve(strict=True)/'acceptance.json'
    parent=json.loads(parent_path.read_text());assert parent['accepted']
    assert re.fullmatch(r'sha256:[a-f0-9]{64}',parent['installed_image'])
    actual=json.loads(subprocess.check_output(['docker','image','inspect',parent['installed_image']],text=True))[0]
    assert actual['Id']==parent['installed_image'] and actual['Os']=='linux' and actual['Architecture']=='amd64'
    manifest=args.package.resolve(strict=True)/'manifest.json'
    package=json.loads(manifest.read_text());assert package['status']=='success'
    control=package['recipe']['resolved']['package']
    assert control['name']=='karyo-macos-core' and control['version']=='0.1.0-1' and control['architecture']=='amd64'
    artifact=package['artifact'];assert re.fullmatch(r'[A-Za-z0-9.+_~-]+[.]deb',artifact['file'])
    binary=manifest.parent/artifact['file']
    assert not binary.is_symlink() and binary.stat().st_size==artifact['bytes'] and digest(binary)==artifact['sha256']
    output=args.output.resolve();output.mkdir(parents=True,exist_ok=False)
    context=output/'image';context.mkdir();actors=output/'actors';actors.mkdir()
    actor=args.source.resolve(strict=True)/'integrations/macos/tests/installed-core-acceptance.py'
    shutil.copyfile(actor,actors/actor.name);shutil.copyfile(binary,context/'core.deb')
    metadata={'control':control,'artifact':artifact,'distribution':package['environment']['distribution'],
              'source':package['source'],'manifest_sha256':digest(manifest)}
    (context/'package.json').write_text(json.dumps(metadata,indent=2)+'\n')
    install="""import hashlib,json,struct,subprocess
from pathlib import Path
folder=Path('/tmp/karyo-macos-package');row=json.loads((folder/'package.json').read_text())
release=dict(line.split('=',1) for line in Path('/etc/os-release').read_text().splitlines() if '=' in line)
assert all(release[key].strip('"')==value for key,value in row['distribution'].items())
assert hashlib.sha256((folder/'core.deb').read_bytes()).hexdigest()==row['artifact']['sha256']
subprocess.run(['dpkg','--path-include=/usr/share/doc/karyo-macos-core','--path-include=/usr/share/doc/karyo-macos-core/*','-i',str(folder/'core.deb')],check=True)
r=subprocess.run(['dpkg','-V','karyo-macos-core'],capture_output=True,text=True,check=True)
assert not r.stdout.strip() and not r.stderr.strip()
subprocess.run(['apt-get','check'],check=True)
probe=Path('/usr/share/karyo-qa/macos-inspection-probe');probe.parent.mkdir(parents=True,exist_ok=True)
probe.write_bytes(struct.pack('<8I',0xFEEDFACF,0x1000007,3,2,0,0,0,0));probe.chmod(0o755)
r=subprocess.run(['/usr/bin/karyo-macos','--inspect',str(probe)],capture_output=True,text=True)
assert r.returncode==1 and 'обычного пользователя' in r.stderr
assert not Path('/root/.karyo-macos').exists()
"""
    (context/'install.py').write_text(install)
    token=uuid.uuid4().hex;captured='karyo-macos-core-parent:'+token;tag='karyo-macos-core-installed:'+token
    subprocess.run(['docker','image','tag',actual['Id'],captured],check=True)
    (context/'Dockerfile').write_text('ARG BASE='+captured+'\nFROM ${BASE}\nUSER root\nCOPY core.deb package.json install.py /tmp/karyo-macos-package/\nRUN python3 -I -B /tmp/karyo-macos-package/install.py\nUSER 1001:1001\n')
    report={'base_image':actual['Id'],'parent_receipt_sha256':digest(parent_path),'package':metadata,
        'actor_sha256':digest(actor),'driver_sha256':digest(Path(__file__)),'install_sha256':digest(context/'install.py')}
    (output/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
    with (output/'build.log').open('wb') as log:
        subprocess.run(['docker','build','--network','none','-t',tag,str(context)],check=True,stdout=log,stderr=subprocess.STDOUT,timeout=120)
    installed=subprocess.check_output(['docker','image','inspect',tag,'--format','{{.Id}}'],text=True).strip()
    name='karyo-macos-core-'+token
    try:
        with (output/'native.log').open('wb') as log:
            result=subprocess.run(['docker','run','--rm','--name',name,'--network','none','--read-only',
                '--user','1001:1001','--cap-drop','ALL','--security-opt','no-new-privileges',
                '--tmpfs','/tmp:rw,exec,nosuid,nodev,mode=1777',
                '--tmpfs','/home/win32qa:rw,exec,nosuid,nodev,uid=1001,gid=1001,mode=700',
                '--mount','type=bind,src='+str(actors)+',dst=/actors,readonly',
                '--mount','type=bind,src='+str(output)+',dst=/output',installed,
                'python3','-I','-B','/actors/installed-core-acceptance.py'],stdout=log,stderr=subprocess.STDOUT,timeout=45)
    finally:
        subprocess.run(['docker','rm','-f',name],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=20)
    assert result.returncode==0,'Installed macOS core check failed; see retained native logs'
    native=json.loads((output/'native-acceptance.json').read_text())
    assert native['uid']==1001 and native['package_version']==control['version']
    assert native['accepted'] and native['fixture_only'] and not native['darling_runtime_proven'] and len(native['checks'])==10
    report.update(installed_image=installed,native=native,accepted=True,
        native_receipt_sha256=digest(output/'native-acceptance.json'))
    (output/'acceptance.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'accepted':True,'image':installed,'fixture_only':True}),flush=True)


if __name__=='__main__':main()
