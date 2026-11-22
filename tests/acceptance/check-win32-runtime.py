#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Install native DEBs and test native Wine in disposable, nonprivileged containers.

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
    parser.add_argument('--wine-package-directory',type=Path,help='Optional successful native Wine source-package output')
    parser.add_argument('--baseline-menus',action='store_true',help='Require observed unpatched DIALOG menus; incompatible with a patched Wine package')
    parser.add_argument('--pe32',action='store_true',help='Also compile and run own PE32/MSI32; image needs native i686 MinGW')
    args=parser.parse_args()
    if args.baseline_menus and args.wine_package_directory:parser.error('Baseline and patched Wine modes are distinct')
    source=args.source.resolve(strict=True);package=args.package_directory.resolve(strict=True)
    compositor=args.compositor.resolve(strict=True);output=args.output.resolve()
    output.mkdir(parents=True,exist_ok=False)
    manifest=json.loads((package/'manifest.json').read_text())
    assert manifest['status']=='success' and manifest['recipe']['resolved']['package']['name']=='karyo-win32'
    binary=package/manifest['artifact']['file'];assert sha(binary)==manifest['artifact']['sha256']
    fixture=source/'integrations/win32/tests';context=output/'image';context.mkdir()
    actors=output/'actors';actors.mkdir()
    for name in ('qt-dialogs.py','account-acceptance.py','runtime-acceptance.py','menu-acceptance.py'):
        shutil.copyfile(fixture/name,actors/name)
    for name in ('runtime-probe.c','runtime-probe.wxs','probe.rc','installed.Dockerfile'):
        shutil.copyfile(fixture/name,context/name)
    shutil.copyfile(binary,context/'karyo-win32.deb');shutil.copyfile(compositor,context/'labwc.deb')
    template=(context/'installed.Dockerfile').read_text()
    additions=[];wine_record=None
    if args.wine_package_directory:
        wine_folder=args.wine_package_directory.resolve(strict=True)
        wine=json.loads((wine_folder/'manifest.json').read_text())
        assert wine['status']=='success' and wine['kind']=='source-package' and wine['input']['source']['name']=='wine'
        assert wine['environment']['distribution']==manifest['environment']['distribution'],'Native package distributions differ'
        assert subprocess.check_output(['docker','image','inspect',args.qa_image,'--format','{{.Id}}'],text=True).strip()==wine['environment']['image_id'],'Use the captured native Wine build image'
        selected={};native=context/'native-wine';native.mkdir()
        required={'libwine','wine','wine64','fonts-wine'}
        for name in sorted(required|{'wine64-preloader','wine-common'}):
            if name not in wine['binaries']:
                assert name not in required,'Required native Wine package missing'
                continue
            filename=wine['binaries'][name]
            assert Path(filename).name==filename and '/' not in filename and chr(92) not in filename and not any(c.isspace() for c in filename),'Unsafe package filename'
            path=wine_folder/filename;assert not path.is_symlink()
            artifact=next(item for item in wine['artifacts'] if item['file']==filename and item.get('package')==name)
            assert path.stat().st_size==artifact['bytes'] and sha(path)==artifact['sha256'],'Changed native Wine package'
            shutil.copyfile(path,native/filename);selected[name]=artifact
        (native/'SHA256SUMS').write_text(''.join(item['sha256']+'  '+item['file']+'\n' for item in selected.values()))
        additions.append('COPY native-wine/ /tmp/native-wine/\nRUN cd /tmp/native-wine && sha256sum -c SHA256SUMS && dpkg -i ./*.deb && dpkg -V '+' '.join(selected)+' && rm -rf /tmp/native-wine\n')
        wine_record={'version':wine['version'],'manifest_sha256':sha(wine_folder/'manifest.json'),'runtime_artifacts':selected,'source_image':wine['environment']['image_id']}
    if wine_record or args.baseline_menus:
        for name in ('menu-probe.c','pointer-probe.c','menu.Dockerfile'):
            shutil.copyfile(fixture/name,context/name)
        (context/'protocols').mkdir()
        shutil.copyfile(fixture/'protocols/wlr-virtual-pointer-unstable-v1.xml',context/'protocols/wlr-virtual-pointer-unstable-v1.xml')
        menu=(context/'menu.Dockerfile').read_text().split('USER root\n',1)[1].rsplit('USER 1001:1001',1)[0]
        additions.append(menu)
    if args.pe32:
        wix=(context/'runtime-probe.wxs').read_text().replace('Platform="x64"','Platform="x86"').replace('Win64="yes"','Win64="no"').replace('Source="runtime-probe.exe"','Source="runtime-probe32.exe"')
        (context/'runtime-probe32.wxs').write_text(wix)
        additions.append('COPY runtime-probe32.wxs /usr/share/karyo-qa/\nRUN cd /usr/share/karyo-qa && i686-w64-mingw32-windres probe.rc probe-resource32.o && i686-w64-mingw32-gcc -std=c11 -Wall -Wextra -Werror -municode runtime-probe.c probe-resource32.o -lgdi32 -o runtime-probe32.exe && wixl -a x86 -o runtime-probe32.msi runtime-probe32.wxs\n')
    if args.pe32 and (wine_record or args.baseline_menus):additions.append('RUN i686-w64-mingw32-gcc -std=c11 -Wall -Wextra -Werror -municode /usr/share/karyo-qa/menu-probe.c -o /usr/share/karyo-qa/menu-probe32.exe\n')
    assert template.count('USER 1001:1001')==1
    (context/'installed.Dockerfile').write_text(template.replace('USER 1001:1001',''.join(additions)+'USER 1001:1001'))
    identity=uuid.uuid4().hex
    captured_image='karyo-win32-captured:'+identity
    qa_image_id=subprocess.check_output(['docker','image','inspect',args.qa_image,'--format','{{.Id}}'],text=True).strip()
    subprocess.run(['docker','image','tag',qa_image_id,captured_image],check=True)
    tag='karyo-win32-acceptance:'+identity
    execute(['docker','build','--network','none','--build-arg','QA_IMAGE='+captured_image,
             '--build-arg','WIN32_SHA256='+sha(binary),'--build-arg','COMPOSITOR_SHA256='+sha(compositor),
             '-f',str(context/'installed.Dockerfile'),'-t',tag,str(context)],output/'image-build.log',300)
    image=subprocess.check_output(['docker','image','inspect',tag,'--format','{{.Id}}'],text=True).strip()
    report={'source_revision':manifest['source']['revision'],'package_sha256':sha(binary),
            'compositor_sha256':sha(compositor),'qa_image':args.qa_image,'installed_image':image,'qa_image_id':qa_image_id,'native_wine':wine_record,'menu_baseline':args.baseline_menus,'cases':[]}
    stages=[('qt','1001','qt-dialogs.py',['--installed']),
                                  ('account','1002','account-acceptance.py',[]),
                                  ('engine','1001','runtime-acceptance.py',['--output','/output/engine'])]
    menu_args=['--baseline'] if args.baseline_menus else []
    if wine_record or args.baseline_menus:
        stages.extend([('menu-keys','1001','menu-acceptance.py',[*menu_args,'--output','/output/menu-keys']),('menu-mouse','1001','menu-acceptance.py',[*menu_args,'--mouse','--output','/output/menu-mouse'])])
    if args.pe32:
        stages.append(('engine32','1001','runtime-acceptance.py',['--bits','32','--output','/output/engine32']))
        if wine_record or args.baseline_menus:stages.extend([('menu32-keys','1001','menu-acceptance.py',[*menu_args,'--bits','32','--output','/output/menu32-keys']),('menu32-mouse','1001','menu-acceptance.py',[*menu_args,'--bits','32','--mouse','--output','/output/menu32-mouse'])])
    for stage,user,script,extra in stages:
        account='win32qa' if user=='1001' else 'workqa'
        command=['docker','run','--rm','--network','none','--read-only','--cap-drop','ALL',
                 '--security-opt','no-new-privileges','--user',user+':'+user,
                 '--tmpfs','/tmp:rw,exec,nosuid,nodev,mode=1777',
                 '--tmpfs','/home/'+account+':rw,exec,nosuid,nodev,uid='+user+',gid='+user+',mode=700',
                 '--mount','type=bind,src='+str(actors)+',dst=/actors,readonly',
                 '--mount','type=bind,src='+str(output)+',dst=/output','-e','QT_QPA_PLATFORM=offscreen',
                 '-e','XDG_CACHE_HOME=/tmp/qa-cache',tag,'dbus-run-session','--','python3','-I','-B',
                 '/actors/'+script,*extra]
        execute(command,output/(stage+'.log'),360)
        report['cases'].append(stage)
        (output/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
    report['actors']={p.name:sha(p) for p in actors.iterdir()}
    report['build_inputs']={str(p.relative_to(context)):sha(p) for p in context.rglob('*') if p.is_file() and p.suffix!='.deb'}
    report['accepted']=True
    (output/'acceptance.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))


if __name__=='__main__':main()
