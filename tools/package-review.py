"""Allowlisted static review package. Never includes old release/source/private data."""
from pathlib import Path
import json,hashlib,zipfile,shutil,gzip
R=Path(__file__).resolve().parents[1];dist=R/'dist';assert (dist/'index.html').exists()
assert not any(p.suffix in ('.blend','.glb') for p in dist.rglob('*'))
assert not any(s in (R/'package.json').read_text() for s in ['"three"','@react-three','"react"','gltfjsx'])
files=[p for p in dist.rglob('*') if p.is_file()];approved_suffixes={'.html','.js','.css','.png','.json','.svg','.txt'}
for p in files:
 assert p.suffix in approved_suffixes,p
 if p.suffix in {'.html','.js','.css','.json','.txt'}:
  t=p.read_text();assert 'BEGIN PRIVATE KEY' not in t and 'ghp_' not in t and 'sk-proj-' not in t,p
stage=R/'.cache/portable-review';stage.mkdir(parents=True,exist_ok=True);root=stage/'Hangeul-Pixel-Town-Gate2';root.mkdir(exist_ok=True);shutil.copytree(dist,root/'3D-pharse5-',dirs_exist_ok=True)
launcher='''"""Run locally: python3 start.py (Windows: py start.py)."""
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from pathlib import Path
import argparse,webbrowser
p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8000);p.add_argument('--no-browser',action='store_true');a=p.parse_args()
url=f'http://127.0.0.1:{a.port}/3D-pharse5-/'
server=ThreadingHTTPServer(('127.0.0.1',a.port),partial(SimpleHTTPRequestHandler,directory=str(Path(__file__).resolve().parent)))
print('Open in your web browser: '+url,flush=True)
if not a.no_browser:webbrowser.open(url)
try:server.serve_forever()
except KeyboardInterrupt:server.server_close()
'''
(root/'start.py').write_text(launcher)
(root/'README.txt').write_text('''KOREAN ARENA — Hangeul Pixel Town, Gate2 ART REVIEW ONLY\nUnzip, open a terminal in this directory, run python3 start.py (Windows: py start.py). Open the HTTP address printed. Do not open HTML in a source-text viewer or move the 3D-pharse5- directory. Python3 required; Node/npm not needed for viewing. Stop server with Ctrl+C.\nWASD/arrows walk; Shift run; E near Mira; Space wave. Buttons/touch pad also available. A/B/C style selector and1x/2x/3x zoom; OS reduced motion respected. No real online players, learning quest, ads, cloud services or paid content.\nOriginal editable source is in repository branch rebuild/pixel-social-rpg-v3. This static package excludes old3D sources/releases. Public website remains v0.5 until separately approved replacement.\n''')
(R/'downloads/pixel-v3.1').mkdir(parents=True,exist_ok=True);dest=R/'downloads/pixel-v3.1/hangeul-pixel-town-gate2-review.zip'
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for f in sorted(root.rglob('*')):
  if f.is_file():z.write(f,f.relative_to(stage))
extract=Path('/tmp/pixel-extracted-review');extract.mkdir(exist_ok=True)
with zipfile.ZipFile(dest) as z:
 assert all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in z.namelist());assert z.testzip() is None;z.extractall(extract)
rows=[{'path':str(p.relative_to(dist)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(files)]
for row in rows:assert hashlib.sha256((extract/'Hangeul-Pixel-Town-Gate2/3D-pharse5-'/row['path']).read_bytes()).hexdigest()==row['sha256']
js=[p for p in files if p.suffix=='.js'];manifest={'status':'PACKAGED_NOT_PUBLICLY_DEPLOYED','zip':str(dest.relative_to(R)),'zip_bytes':dest.stat().st_size,'zip_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'build_bytes':sum(p.stat().st_size for p in files),'js_raw_bytes':sum(p.stat().st_size for p in js),'js_theoretical_gzip_bytes':sum(len(gzip.compress(p.read_bytes())) for p in js),'gzip_note':'Computed compression, not measured network transfer','files':rows,'public_v05_unchanged_sha256':'082c661b5da2b4c8e66e81b2f52405ef460947bfeff27e2fd6fe771b2e3c716f','scan':'Allowlisted dist-only files; no private key/provider-token markers or3D assets. Original assets MIT; dependency license files included.'}
(R/'downloads/pixel-v3.1/package-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps({k:v for k,v in manifest.items() if k!='files'}))
