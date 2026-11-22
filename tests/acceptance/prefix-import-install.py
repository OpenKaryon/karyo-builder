#!/usr/bin/python3 -I
# SPDX-License-Identifier: GPL-3.0-or-later
"""Prepare and verify a real package upgrade in a disposable native QA image."""
import hashlib
import json
import os
from pathlib import Path
import subprocess


def main():
    assert os.getuid()==0 and Path('/usr/share/karyo-qa/runtime-probe.exe').is_file()
    folder=Path('/tmp/karyo-prefix-import')
    row=json.loads((folder/'package.json').read_text())
    release=dict(line.split('=',1) for line in Path('/etc/os-release').read_text().splitlines() if '=' in line)
    assert all(release[key].strip('"')==value for key,value in row['distribution'].items())
    package=folder/'karyo-win32.deb'
    assert hashlib.sha256(package.read_bytes()).hexdigest()==row['sha256']
    fields=subprocess.check_output(['dpkg-deb','-f',str(package),'Package','Version','Architecture'],text=True)
    actual=dict(line.split(': ',1) for line in fields.splitlines())
    assert actual=={'Package':'karyo-win32','Version':'0.1.0-2','Architecture':'amd64'}
    before=subprocess.check_output(['dpkg-query','-W','-f=${Version}','karyo-win32'],text=True).strip()
    assert before=='0.1.0-1'
    script=folder/'prefix-upgrade-state.py'
    subprocess.run(['setpriv','--reuid=1001','--regid=1001','--clear-groups',
        '--bounding-set=-all','--no-new-privs','python3','-I','-B',str(script),'--seed'],check=True)
    snapshot=Path('/usr/share/karyo-qa/upgrade-before.json')
    subprocess.run(['python3','-I','-B',str(script),'--snapshot',str(snapshot)],check=True)
    # Minimal container bases may omit documentation globally. Include this
    # package's complete payload explicitly; dpkg -V can report missing files
    # with status zero, so require an empty diagnostic as well.
    subprocess.run(['dpkg','--path-include=/usr/share/doc/karyo-win32',
        '--path-include=/usr/share/doc/karyo-win32/*','-i',str(package)],check=True)
    verified=subprocess.run(['dpkg','-V','karyo-win32'],check=True,capture_output=True,text=True)
    assert not verified.stdout.strip() and not verified.stderr.strip(),verified
    subprocess.run(['apt-get','check'],check=True)
    subprocess.run(['python3','-I','-B',str(script),'--verify',str(snapshot)],check=True)
    archive=Path('/usr/share/karyo-qa/upgrade-home.tar')
    subprocess.run(['tar','--format=pax','-cpf',str(archive),'-C','/home/win32qa','.'],check=True)
    proof={'old_version':before,'new_version':'0.1.0-2','package':row,
        'user_data_unchanged':True,'snapshot_sha256':hashlib.sha256(snapshot.read_bytes()).hexdigest(),
        'backup_sha256':hashlib.sha256(archive.read_bytes()).hexdigest()}
    Path('/usr/share/karyo-qa/upgrade-package.json').write_text(json.dumps(proof,indent=2)+'\n')


if __name__=='__main__':main()
