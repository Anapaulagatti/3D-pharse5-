"""Package the isolated reviewed candidate; no site publication or old file changes."""
from pathlib import Path
import json,hashlib,zipfile,shutil
root=Path(__file__).resolve().parents[2];src=root/'showcase-v0.6';out=root/'downloads/v0.6';out.mkdir(exist_ok=True)
info=json.loads((src/'build-info.json').read_text());data=(src/'index.html').read_bytes();assert len(data)==info['bytes'] and hashlib.sha256(data).hexdigest()==info['sha256']
records=[]
for suffix,names,prefix in [('view',['index.html','start.py','START_WINDOWS.cmd','README.md','build-info.json'],'Playful-Hangeul-Town-v0.6-prototype/'),('static',['index.html','.nojekyll'],'')]:
    dst=out/f'playful-hangeul-town-v0.6-prototype-{suffix}.zip'
    with zipfile.ZipFile(dst,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in names:z.write(src/name,prefix+name)
    with zipfile.ZipFile(dst) as z:
        assert z.testzip() is None
        for name in z.namelist():assert not Path(name).is_absolute() and '..' not in Path(name).parts
        assert z.read(prefix+'index.html')==data
    records.append({'file':dst.name,'bytes':dst.stat().st_size,'sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'files':names})
(out/'prototype-package-manifest.json').write_text(json.dumps({'version':'0.6-prototype','public_release':'NOT_AUTHORIZED','html_sha256':info['sha256'],'packages':records},indent=2)+'\n')
# Disposable, strict two-file static repository subpath for internal real-browser QA.
stage=Path('/tmp/town-v06-static-review/3D-pharse5-');stage.mkdir(parents=True,exist_ok=True)
for name in ['index.html','.nojekyll']:shutil.copyfile(src/name,stage/name)
assert sorted(p.name for p in stage.iterdir())==['.nojekyll','index.html']
# Safely extract complete viewing package for its actual included launcher check.
target=Path('/tmp/town-v06-extracted-review');target.mkdir(exist_ok=True)
with zipfile.ZipFile(out/'playful-hangeul-town-v0.6-prototype-view.zip') as z:z.extractall(target)
assert (target/'Playful-Hangeul-Town-v0.6-prototype/index.html').read_bytes()==data
print(json.dumps(records,indent=2))
