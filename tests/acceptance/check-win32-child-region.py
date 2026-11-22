#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Compile and exercise real Win32 child regions in accepted native QA images."""
import argparse,hashlib,json,shutil,subprocess,uuid
from pathlib import Path

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--runtime-acceptance',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--bits',type=int,nargs='+',choices=(32,64),default=[32,64])
    parser.add_argument('--dpis',type=int,nargs='+',choices=(96,192),default=[96,192])
    parser.add_argument('--baseline',action='store_true')
    parser.add_argument('--baseline-matrix',type=Path)
    args=parser.parse_args()
    if args.baseline==bool(args.baseline_matrix):parser.error('Choose baseline observation or a matching accepted baseline matrix')
    previous_path=args.runtime_acceptance.resolve(strict=True)/'acceptance.json';previous=json.loads(previous_path.read_text());assert previous['accepted']
    image_info=json.loads(subprocess.check_output(['docker','image','inspect',previous['installed_image']],text=True))[0]
    assert image_info['Os']=='linux' and image_info['Architecture']=='amd64'
    output=args.output.resolve();output.mkdir(parents=True,exist_ok=False);context=output/'image';context.mkdir();actors=output/'actors';actors.mkdir()
    fixture=args.source.resolve(strict=True)/'integrations/win32/tests'
    shutil.copyfile(fixture/'child-region-probe.c',context/'child-region-probe.c')
    shutil.copyfile(fixture/'child-region-acceptance.py',actors/'child-region-acceptance.py')
    baseline_folder=None;baseline_rows={}
    if args.baseline_matrix:
        baseline_folder=args.baseline_matrix.resolve(strict=True);baseline=json.loads((baseline_folder/'acceptance.json').read_text())
        assert baseline['accepted'] and baseline['baseline']
        assert baseline['actor_sha256']==digest(actors/'child-region-acceptance.py') and baseline['source_sha256']==digest(context/'child-region-probe.c')
        baseline_rows={row['stage']:row for row in baseline['cases']}
    identity=uuid.uuid4().hex;base='karyo-child-region-captured:'+identity;image='karyo-child-region-qa:'+identity
    subprocess.run(['docker','image','tag',image_info['Id'],base],check=True)
    lines=['ARG BASE=karyo-captured:unset','FROM ${BASE}','USER root','COPY child-region-probe.c /usr/share/karyo-qa/']
    for bits in sorted(set(args.bits)):
        compiler='i686' if bits==32 else 'x86_64';suffix='32' if bits==32 else ''
        lines.append(f'RUN {compiler}-w64-mingw32-gcc -std=c11 -Wall -Wextra -Werror -municode /usr/share/karyo-qa/child-region-probe.c -lgdi32 -o /usr/share/karyo-qa/child-region-probe{suffix}.exe')
    lines.append('USER 1001:1001');(context/'Dockerfile').write_text('\n'.join(lines)+'\n')
    with (output/'build.log').open('wb') as log:
        subprocess.run(['docker','build','--network','none','--build-arg','BASE='+base,'-t',image,str(context)],stdout=log,stderr=subprocess.STDOUT,check=True,timeout=180)
    image_id=subprocess.check_output(['docker','image','inspect',image,'--format','{{.Id}}'],text=True).strip()
    report={'runtime_receipt_sha256':digest(previous_path),'base_image':image_info['Id'],'installed_image':image_id,'baseline':args.baseline,'actor_sha256':digest(actors/'child-region-acceptance.py'),'source_sha256':digest(context/'child-region-probe.c'),'cases':[]}
    for bits in sorted(set(args.bits)):
        for dpi in sorted(set(args.dpis)):
            label=f'pe{bits}-dpi{dpi}';name='karyo-child-region-'+identity+'-'+label
            command=['docker','run','--rm','--name',name,'--network','none','--read-only','--cap-drop','ALL','--security-opt','no-new-privileges','--cpus','2','--memory','3g','--pids-limit','512','--user','1001:1001','--tmpfs','/tmp:rw,exec,nosuid,nodev,mode=1777','--tmpfs','/home/win32qa:rw,exec,nosuid,nodev,uid=1001,gid=1001,mode=700','--mount','type=bind,src='+str(actors)+',dst=/actors,readonly','--mount','type=bind,src='+str(output)+',dst=/output',image_id,'dbus-run-session','--','python3','-I','-B','/actors/child-region-acceptance.py','--output','/output/'+label,'--bits',str(bits),'--dpi',str(dpi)]
            if args.baseline:command.append('--baseline')
            else:
                row=baseline_rows[label];path=baseline_folder/label/'acceptance.json'
                assert row['returncode']==0 and digest(path)==row['native_receipt_sha256']
                copied=actors/('baseline-'+label+'.json');shutil.copyfile(path,copied)
                command.extend(['--baseline-file','/actors/'+copied.name])
            try:
                with (output/(label+'.log')).open('wb') as log:code=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,timeout=480).returncode
            except subprocess.TimeoutExpired:code=124
            finally:subprocess.run(['docker','rm','-f',name],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=20)
            native=output/label/'acceptance.json'
            report['cases'].append({'stage':label,'returncode':code,'native_receipt_sha256':digest(native) if native.exists() else None})
            (output/'progress.json').write_text(json.dumps(report,indent=2)+'\n');print(label,code,flush=True)
            if code:raise RuntimeError('Actual child-region acceptance failed; inspect captured stages')
    report['accepted']=True;(output/'acceptance.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
