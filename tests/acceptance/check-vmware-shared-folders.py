#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Verify packaged HGFS in a named disposable kernel VM using real host files."""
import argparse
import hashlib
import ipaddress
import json
from pathlib import Path
import subprocess
import uuid


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def validate_native_package(manifest, base):
    distribution = {'debian': {'ID':'debian','VERSION_ID':'13','VERSION_CODENAME':'trixie'},
                    'ubuntu': {'ID':'ubuntu','VERSION_ID':'26.04','VERSION_CODENAME':'resolute'}}
    metadata = manifest['recipe']['resolved']['package']
    if (manifest.get('status')!='success' or manifest['validation'].get('ctest')!='passed'
            or manifest['validation'].get('dpkg_deb')!='passed'
            or metadata.get('name')!='karyo-vmware-shared-folders' or metadata.get('architecture')!='amd64'
            or manifest['environment'].get('distribution')!=distribution[base]):
        raise ValueError('Expected a successful HGFS package from the selected native base')


def restore_host(vix, vmx, share, added, enabled, changed):
    errors=[]
    actions=[]
    if added:actions.append(('removeSharedFolder',vmx,share))
    if enabled:actions.append(('disableSharedFolders',vmx))
    if changed:actions.append(('writeVariable',vmx,'runtimeConfig','isolation.tools.hgfs.disable','TRUE'))
    for action in actions:
        try:
            call=vix(*action,check=False)
            if call.returncode:errors.append(str(action[0])+' exited '+str(call.returncode))
        except (OSError,subprocess.SubprocessError) as error:
            errors.append(str(action[0])+': '+str(error))
    restored=False
    try:
        call=vix('readVariable',vmx,'runtimeConfig','isolation.tools.hgfs.disable',check=False)
        restored=call.returncode==0 and call.stdout.strip()=='TRUE'
        if not restored:errors.append('The disabled runtime flag was not restored')
    except (OSError,subprocess.SubprocessError) as error:
        errors.append('readVariable: '+str(error))
    return {'runtime_restored':restored,'errors':errors}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('base','vmx','ssh-host','ssh-key','known-hosts','vmrun','package-output','de-source','output'):
        parser.add_argument('--'+name,required=True,choices=('debian','ubuntu') if name=='base' else None)
    args=parser.parse_args()
    address=str(ipaddress.ip_address(args.ssh_host))
    vmx=Path(args.vmx).resolve(strict=True)
    vmrun=Path(args.vmrun).resolve(strict=True)
    key=Path(args.ssh_key).resolve(strict=True)
    known=Path(args.known_hosts).resolve(strict=True)
    package_output=Path(args.package_output).resolve(strict=True)
    source=Path(args.de_source).resolve(strict=True)
    actor=source/'integrations/vmware/shared-folders/tests/installed-service.py'
    manifest=json.loads((package_output/'manifest.json').read_text())
    validate_native_package(manifest,args.base)
    package=package_output/manifest['artifact']['file']
    if package.parent!=package_output or not package.is_file() or digest(package)!=manifest['artifact']['sha256']:
        raise ValueError('Native package identity changed')
    if vmx.suffix.lower()!='.vmx' or not actor.is_file() or actor.is_symlink():
        raise ValueError('Expected a VMX and product-owned native actor')
    tag='karyo-hgfs-service-'+uuid.uuid4().hex[:10]
    output=Path(args.output).resolve()/tag
    output.mkdir(parents=True,exist_ok=False)
    (output/'host.txt').write_text('System HGFS: Привет!\n',encoding='utf-8')
    events=[];logs={};added=enabled=changed=False
    ssh_options=['-i',str(key),'-o','IdentityAgent=none','-o','IdentitiesOnly=yes','-o','BatchMode=yes',
                 '-o','ConnectTimeout=5','-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(known)]
    host='qaadmin@'+address
    scp_host='qaadmin@'+('['+address+']' if ':' in address else address)
    remote='/home/qaadmin/'+tag
    spec={'base':args.base,'share':tag,'package':remote+'.deb',
          'package_sha256':digest(package),'source':manifest['source']['revision']}
    (output/'spec.json').write_text(json.dumps(spec,indent=2)+'\n')
    result={'schema':1,'kind':'native-vmware-hgfs-service','accepted':False,'base':args.base,
            'package':{'sha256':digest(package),'source_revision':manifest['source']['revision'],
                       'manifest_sha256':digest(package_output/'manifest.json')},
            'actor_sha256':digest(actor),'driver_sha256':digest(Path(__file__)),'events':events}

    def vix(*values,check=True):
        call=subprocess.run([str(vmrun),*map(str,values)],capture_output=True,text=True,errors='replace',timeout=30)
        events.append({'command':str(values[0]),'exit':call.returncode,'stdout':call.stdout,'stderr':call.stderr})
        if check and call.returncode:
            raise RuntimeError('VMware CLI failed: '+str(values[0]))
        return call

    def copy(path,suffix):
        subprocess.run(['scp',*ssh_options,str(path),scp_host+':'+remote+suffix],check=True,timeout=60)

    def phase(label,check=True):
        # All remote arguments are generated ASCII names, not shell input from a
        # caller. The source actor independently checks the fixed QA hostname/UID.
        command='sudo -n /usr/bin/python3 -I '+remote+'-actor.py --spec '+remote+'-spec.json --phase '+label
        log=output/(label+'.log')
        with log.open('wb') as stream:
            call=subprocess.run(['ssh',*ssh_options,host,command],stdout=stream,stderr=subprocess.STDOUT,timeout=180)
        logs[label]={'exit':call.returncode,'sha256':digest(log)}
        print(args.base,label,call.returncode,flush=True)
        if check and call.returncode:
            raise RuntimeError('Native HGFS phase failed: '+str(log))
        return log.read_text()

    try:
        guest_ip=vix('getGuestIPAddress',vmx).stdout.strip()
        if guest_ip!=address:
            raise ValueError('VMware target and SSH guest differ')
        original=vix('readVariable',vmx,'runtimeConfig','isolation.tools.hgfs.disable').stdout.strip()
        if original!='TRUE':
            raise ValueError('QA HGFS must initially be disabled')
        if vix('readVariable',vmx,'runtimeConfig','sharedFolder.maxNum').stdout.strip()!='0':
            raise ValueError('Disposable QA guest must not have other configured host shares')
        copy(package,'.deb');copy(actor,'-actor.py');copy(output/'spec.json','-spec.json')
        # Check copied actor integrity before allowing its root test operations.
        expected=digest(actor)
        verify='test "$(sha256sum '+remote+'-actor.py | cut -d " " -f 1)" = "'+expected+'"'
        subprocess.run(['ssh',*ssh_options,host,verify],check=True,timeout=20)
        text=phase('install-disabled')
        if 'PASS_DISABLED_HOST_SKIPPED' not in text:
            raise ValueError('Absent disabled-host evidence')
        vix('writeVariable',vmx,'runtimeConfig','isolation.tools.hgfs.disable','FALSE');changed=True
        vix('enableSharedFolders',vmx,'runtime');enabled=True
        vix('addSharedFolder',vmx,tag,output);added=True
        text=phase('service-native')
        for marker in ('NATIVE_OWNED_FUSE_WORKER','PASS_REPLACEMENT','READY_DISCONNECTED_PURGE'):
            if marker not in text:
                raise ValueError('Absent native service evidence: '+marker)
        if (output/'guest.txt').read_text()!='Native service: Привет!\n':
            raise ValueError('No real ordinary-user guest-to-host payload')
        vix('removeSharedFolder',vmx,tag);added=False
        vix('disableSharedFolders',vmx);enabled=False
        vix('writeVariable',vmx,'runtimeConfig','isolation.tools.hgfs.disable',original);changed=False
        text=phase('purge-disconnected')
        if 'PASS_DISCONNECTED_PURGE_GLOBAL_STATE_PRESERVED' not in text:
            raise ValueError('Absent native disconnected-purge evidence')
        if ((output/'guest.txt').read_text()!='Native service: Привет!\n'
                or (output/'host.txt').read_text()!='System HGFS: Привет!\n'):
            raise ValueError('Package removal changed host payloads')
        result.update(accepted=True,ordinary_bidirectional=True,private_mount_inheritance=True,
            same_type_replacement_preserved=True,administrator_disable_preserved=True,
            disconnected_purge=True,global_account_pam_dm_shell_root_tools_preserved=True)
    except BaseException as error:
        result['error']=str(error)
        raise
    finally:
        try:
            phase('cleanup-stop',check=False)
            if logs['cleanup-stop']['exit']!=0:
                result['accepted']=False
        except (OSError,subprocess.SubprocessError) as error:
            result.update(accepted=False,cleanup_guest_error=str(error))
        cleanup=restore_host(vix,vmx,tag,added,enabled,changed)
        result['runtime_restored']=cleanup['runtime_restored']
        if cleanup['errors']:
            result.update(accepted=False,cleanup_host_errors=cleanup['errors'])
        result['logs']=logs
        (output/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print('Evidence: '+str(output),flush=True)
    if not result['accepted']:
        raise RuntimeError('Native HGFS acceptance did not complete')


if __name__=='__main__':
    main()
