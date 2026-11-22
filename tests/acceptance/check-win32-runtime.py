#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Install native DEBs and test Wine64 in disposable, nonprivileged containers.

Requires a prepared native integrations/win32/environments QA image. No personal
prefix, network, current display or current D-Bus session is forwarded.
"""
import argparse,hashlib,json,shutil,subprocess,uuid
from pathlib import Path


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def execute(args,log,timeout):
    with log.open('wb') as stream:
        result=subprocess.run(args,stdout=stream,stderr=subprocess.STDOUT,timeout=timeout)
    if result.returncode:raise RuntimeError(f'QA command failed ({result.returncode}); see {log}')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--package-directory',type=Path,required=True)
    parser.add_argument('--compositor',type=Path,required=True)
    parser.add_argument('--qa-image',required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    source=args.source.resolve(strict=True);package=args.package_directory.resolve(strict=True)
    compositor=args.compositor.resolve(strict=True);output=args.output.resolve()
    output.mkdir(parents=True,exist_ok=False)
    manifest=json.loads((package/'manifest.json').read_text())
    assert manifest['status']=='success' and manifest['recipe']['resolved']['package']['name']=='karyo-win32'
    binary=package/manifest['artifact']['file'];assert sha(binary)==manifest['artifact']['sha256']
    fixture=source/'integrations/win32/tests';context=output/'image';context.mkdir()
    for name in ('runtime-probe.c','runtime-probe.wxs','probe.rc','installed.Dockerfile'):
        shutil.copyfile(fixture/name,context/name)
    shutil.copyfile(binary,context/'karyo-win32.deb');shutil.copyfile(compositor,context/'labwc.deb')
    tag='karyo-win32-acceptance:'+uuid.uuid4().hex
    execute(['docker','build','--network','none','--build-arg','QA_IMAGE='+args.qa_image,
             '--build-arg','WIN32_SHA256='+sha(binary),'--build-arg','COMPOSITOR_SHA256='+sha(compositor),
             '-f',str(context/'installed.Dockerfile'),'-t',tag,str(context)],output/'image-build.log',300)
    image=subprocess.check_output(['docker','image','inspect',tag,'--format','{{.Id}}'],text=True).strip()
    report={'source_revision':manifest['source']['revision'],'package_sha256':sha(binary),
            'compositor_sha256':sha(compositor),'qa_image':args.qa_image,'installed_image':image,'cases':[]}
    for stage,user,script,extra in [('qt','1001','qt-dialogs.py',['--installed']),
                                  ('account','1002','account-acceptance.py',[]),
                                  ('engine','1001','runtime-acceptance.py',['--output','/output/engine'])]:
        account='win32qa' if user=='1001' else 'workqa'
        command=['docker','run','--rm','--network','none','--read-only','--cap-drop','ALL',
                 '--security-opt','no-new-privileges','--user',user+':'+user,
                 '--tmpfs','/tmp:rw,exec,nosuid,nodev,mode=1777',
                 '--tmpfs','/home/'+account+':rw,exec,nosuid,nodev,uid='+user+',gid='+user+',mode=700',
                 '--mount','type=bind,src='+str(source)+',dst=/source,readonly',
                 '--mount','type=bind,src='+str(output)+',dst=/output','-e','QT_QPA_PLATFORM=offscreen',
                 '-e','XDG_CACHE_HOME=/tmp/qa-cache',tag,'dbus-run-session','--','python3','-I','-B',
                 '/source/integrations/win32/tests/'+script,*extra]
        execute(command,output/(stage+'.log'),360)
        report['cases'].append(stage)
        (output/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
    report['actors']={p.name:sha(p) for p in fixture.iterdir() if p.is_file() and p.suffix in ('.py','.c','.wxs','.rc','.Dockerfile')}
    report['accepted']=True
    (output/'acceptance.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))


if __name__=='__main__':main()
