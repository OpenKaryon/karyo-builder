#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Freeze a Win32 caption fixture and run it in a captured accepted native image."""
import argparse,hashlib,json,re,shutil,subprocess,uuid
from pathlib import Path

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def rendered_buttons(folder,previous,source,baseline):
    # Only the frozen own palette producer can justify these exact colors/sizes.
    from PIL import Image
    fixture=source/'integrations/win32/tests'
    assert previous['producer_source_sha256']==digest(fixture/'palette-probe.c')
    assert previous['actor_sha256']==digest(fixture/'palette-acceptance.py')
    assert previous['cases'],'An accepted real palette matrix is required'
    records=[]
    for case in previous['cases']:
        label=case['stage']
        assert re.fullmatch(r'pe(?:32|64)-[0-9]+',label) and case['returncode']==0
        frame=folder/label/'restored-0.png'
        with Image.open(frame) as captured:
            image=captured.convert('RGB')
        pixels=image.load()
        remaining={(x,y) for y in range(image.height) for x in range(image.width) if pixels[x,y]==(196,43,28)}
        components=[]
        while remaining:
            point=remaining.pop();seen={point};queue=[point]
            while queue:
                x,y=queue.pop()
                for candidate in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                    if candidate in remaining:
                        remaining.remove(candidate);seen.add(candidate);queue.append(candidate)
            left=min(x for x,y in seen);right=max(x for x,y in seen)
            top=min(y for x,y in seen);bottom=max(y for x,y in seen)
            white=sum(pixels[x,y]==(255,255,255) for x in range(left,right+1) for y in range(top,bottom+1))
            components.append({'red':len(seen),'white':white,'width':right-left+1,'height':bottom-top+1,'left':left,'top':top})
        if baseline:
            assert not components,'Baseline already renders the patched red button'
        else:
            assert len(components)==4 and all(c['red']==108 and c['white']==13 and c['width']==c['height']==11 for c in components),'Four filled red/white tool buttons were not actually rendered'
        records.append({'case':label,'frame_sha256':digest(frame),'components':sorted(components,key=lambda c:(c['top'],c['left']))})
    return records

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--runtime-acceptance',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--baseline',action='store_true')
    args=parser.parse_args()
    receipt=args.runtime_acceptance.resolve(strict=True)/'acceptance.json'
    previous=json.loads(receipt.read_text());assert previous['accepted'],'Runtime acceptance must pass first'
    frames=rendered_buttons(receipt.parent,previous,args.source.resolve(strict=True),args.baseline)
    info=json.loads(subprocess.check_output(['docker','image','inspect',previous['installed_image']],text=True))[0]
    assert info['Os']=='linux' and info['Architecture']=='amd64'
    output=args.output.resolve();output.mkdir(parents=True,exist_ok=False)
    context=output/'image';context.mkdir();actors=output/'actors';actors.mkdir()
    fixture=args.source.resolve(strict=True)/'integrations/win32/tests'
    shutil.copyfile(fixture/'caption-probe.c',context/'caption-probe.c')
    shutil.copyfile(fixture/'caption-acceptance.py',actors/'caption-acceptance.py')
    identity=uuid.uuid4().hex;base='karyo-caption-captured:'+identity;image='karyo-caption-qa:'+identity
    subprocess.run(['docker','image','tag',info['Id'],base],check=True)
    lines=['ARG BASE','FROM ${BASE}','USER root','COPY caption-probe.c /usr/share/karyo-qa/']
    for bits,compiler,suffix in [(32,'i686','32'),(64,'x86_64','')]:
        lines.append(f'RUN {compiler}-w64-mingw32-gcc -std=c11 -Wall -Wextra -Werror -municode /usr/share/karyo-qa/caption-probe.c -lgdi32 -o /usr/share/karyo-qa/caption-probe{suffix}.exe')
    lines.append('USER 1001:1001');(context/'Dockerfile').write_text('\n'.join(lines)+'\n')
    with (output/'build.log').open('wb') as log:
        subprocess.run(['docker','build','--network','none','--build-arg','BASE='+base,'-t',image,str(context)],stdout=log,stderr=subprocess.STDOUT,check=True,timeout=180)
    image_id=subprocess.check_output(['docker','image','inspect',image,'--format','{{.Id}}'],text=True).strip()
    report={'runtime_receipt_sha256':digest(receipt),'base_image':info['Id'],'installed_image':image_id,'baseline':args.baseline,'rendered_frames':frames,'source_sha256':digest(context/'caption-probe.c'),'actor_sha256':digest(actors/'caption-acceptance.py'),'cases':[]}
    for bits in [32,64]:
        label='pe'+str(bits);name='karyo-caption-'+identity+'-'+label
        command=['docker','run','--rm','--name',name,'--network','none','--read-only','--cap-drop','ALL','--security-opt','no-new-privileges','--user','1001:1001','--tmpfs','/tmp:rw,exec,nosuid,nodev,mode=1777','--tmpfs','/home/win32qa:rw,exec,nosuid,nodev,uid=1001,gid=1001,mode=700','--mount','type=bind,src='+str(actors)+',dst=/actors,readonly','--mount','type=bind,src='+str(output)+',dst=/output',image_id,'dbus-run-session','--','python3','-I','-B','/actors/caption-acceptance.py','--output','/output/'+label,'--bits',str(bits)]
        if args.baseline:command.append('--baseline')
        try:
            with (output/(label+'.log')).open('wb') as log:
                result=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,timeout=240)
            code=result.returncode
        except subprocess.TimeoutExpired:code=124
        finally:subprocess.run(['docker','rm','-f',name],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=20)
        report['cases'].append({'stage':label,'returncode':code})
        (output/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
        print(label,code,flush=True)
    report['accepted']=all(row['returncode']==0 for row in report['cases'])
    if not report['accepted']:raise RuntimeError('Caption acceptance failed; inspect retained observations')
    (output/('baseline.json' if args.baseline else 'acceptance.json')).write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
