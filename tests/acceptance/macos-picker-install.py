# SPDX-License-Identifier: GPL-3.0-or-later
"""Disposable QA image installation only; never a product privileged helper."""
import hashlib
import json
import os
from pathlib import Path
import pwd
import stat
import struct
import subprocess


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    assert os.getuid()==0 and Path('/usr/share/karyo-qa/runtime-probe.exe').is_file()
    assert pwd.getpwnam('win32qa').pw_uid==1001
    folder=Path('/tmp/karyo-macos-gui');row=json.loads((folder/'package.json').read_text())
    release=dict(line.split('=',1) for line in Path('/etc/os-release').read_text().splitlines() if '=' in line)
    for package in row.values():
        assert all(release[key].strip('"')==value for key,value in package['distribution'].items())
        assert digest(folder/package['file'])==package['artifact']['sha256']
    assert row['core']['source']==row['picker']['source']
    assert subprocess.check_output(['dpkg-query','-W','-f=${Version}','karyo-macos-core'],text=True).strip()=='0.1.0-1'
    windows=Path('/usr/share/applications/karyo-mimeapps.list');windows_before=digest(windows)
    owner=subprocess.check_output(['dpkg-query','-S',str(windows)],text=True)
    assert owner.startswith('karyo-win32: ')
    folder_default=subprocess.check_output(['gio','mime','inode/directory'],text=True)
    seed='from pathlib import Path;p=Path("/home/win32qa/.karyo-macos/upgrade-data");p.parent.mkdir(mode=0o700);p.write_text("Existing profile data: Пример\\n");p.chmod(0o600)'
    subprocess.run(['setpriv','--reuid=1001','--regid=1001','--clear-groups','--bounding-set=-all','--no-new-privs',
                    'python3','-I','-B','-c',seed],check=True)
    marker=Path('/home/win32qa/.karyo-macos/upgrade-data')
    def snapshot():
        info=marker.stat();return {'sha256':digest(marker),'mode':stat.S_IMODE(info.st_mode),'uid':info.st_uid,'mtime_ns':info.st_mtime_ns}
    before=snapshot()
    command=['dpkg','--path-include=/usr/share/doc/karyo-macos*','--path-include=/usr/share/doc/karyo-macos*/*','-i',
             str(folder/'core.deb'),str(folder/'picker.deb')]
    subprocess.run(command,check=True)
    for name in ('karyo-macos-core','karyo-macos'):
        verified=subprocess.run(['dpkg','-V',name],capture_output=True,text=True,check=True)
        assert not verified.stdout.strip() and not verified.stderr.strip(),verified
    subprocess.run(['apt-get','check'],check=True)
    assert snapshot()==before and digest(windows)==windows_before
    assert subprocess.check_output(['dpkg-query','-S',str(windows)],text=True)==owner
    assert subprocess.check_output(['gio','mime','inode/directory'],text=True)==folder_default
    subprocess.run(['desktop-file-validate','/usr/share/applications/karyo-macos.desktop'],check=True)
    probe=Path('/usr/share/karyo-qa/Пример literal $().macho')
    probe.write_bytes(struct.pack('<8I',0xFEEDFACF,0x1000007,3,2,0,0,0,0));probe.chmod(0o755)
    assert 'application/x-karyo-mach-o' in subprocess.check_output(['gio','info','-a','standard::content-type',str(probe)],text=True)
    proof={'packages':row,'user_data_unchanged':True,'windows_defaults_unchanged':True,
           'directory_default_unchanged':True,'windows_defaults_sha256':windows_before,'preserved_user_data':before}
    Path('/usr/share/karyo-qa/macos-picker-packages.json').write_text(json.dumps(proof,indent=2)+'\n')


if __name__=='__main__':main()
