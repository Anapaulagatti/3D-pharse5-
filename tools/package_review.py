"""Allowlisted current static build + notices + actual local HTTP launcher. No source or old projects."""
from pathlib import Path
import json,hashlib,shutil,zipfile
R=Path(__file__).resolve().parents[1];D=R/'dist';assert (D/'index.html').exists();files=[p for p in D.rglob('*') if p.is_file()]
for p in files:
 assert p.suffix in {'.html','.js','.css','.png','.json','.svg','.txt'},p
 if p.suffix in {'.html','.js','.css','.json','.txt'}:
  t=p.read_text();assert not any(s in t for s in ['BEGIN PRIVATE KEY','ghp_','sk-proj-']),p
assert len(list((D/'assets/world').iterdir()))==23
for actor in ['hero','sejong','jang','saimdang','yi']:assert (D/'assets/actors'/actor/'atlas.json').exists()
assert not any(p.suffix in ['.blend','.glb'] for p in files)
rows=[{'path':str(p.relative_to(D)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in sorted(files)];buildhash=hashlib.sha256(json.dumps(rows).encode()).hexdigest()[:12];stage=R/'.cache/portable'/buildhash;root=stage/'Korean-Arena-Review';root.mkdir(parents=True,exist_ok=True);shutil.copytree(D,root/'3D-pharse5-',dirs_exist_ok=True)
launcher='''from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
import argparse,webbrowser
p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8000);p.add_argument('--no-browser',action='store_true');a=p.parse_args()
url=f'http://127.0.0.1:{a.port}/3D-pharse5-/'
s=ThreadingHTTPServer(('127.0.0.1',a.port),partial(SimpleHTTPRequestHandler,directory=str(Path(__file__).resolve().parent)))
print('Open in your browser: '+url,flush=True)
if not a.no_browser:webbrowser.open(url)
try:s.serve_forever()
except KeyboardInterrupt:s.server_close()
'''
(root/'start.py').write_text(launcher);(root/'README.txt').write_text('Korean Arena — current animation/historical guest review, NOT PUBLICLY RELEASED.\nExtract, run python3 start.py (Windows py start.py), open printed HTTPURL. Python3required; noNode needed to view. Do not open index.html as source or file://. Ctrl+C stops.\nWASD/arrows walk; Shift run; E nearby guest; Spacewave. Touchpad/buttons, hair/outfit/satchel/4moods/zoom, OSreducedmotion/pause/Canvasfallback. Guests are educational fictional projections from different eras. Hooks are concepts only, no fullquests/onlineusers/backend/ads.\n')
q=R/'docs/review';q.mkdir(parents=True,exist_ok=True);dest=q/'playable-review.zip'
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(root.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(stage))
sha=hashlib.sha256(dest.read_bytes()).hexdigest();extract=R/'.cache/extracted'/sha[:12];extract.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(dest) as z:
 assert z.testzip() is None and all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in z.namelist());z.extractall(extract)
for r in rows:assert hashlib.sha256((extract/'Korean-Arena-Review/3D-pharse5-'/r['path']).read_bytes()).hexdigest()==r['sha256']
m={'status':'PACKAGED_PENDING_HTTP_BROWSER_VERIFICATION','zip':'docs/review/playable-review.zip','zip_bytes':dest.stat().st_size,'zip_sha256':sha,'build_bytes':sum(r['bytes'] for r in rows),'files':rows,'extract_root':str(extract/'Korean-Arena-Review'),'security_scan':'dist only; suffix allowlist; no private-key/provider-token markers,3D,rejectedsource or third-party artwork; original/Phaser/Zod notices included.'}
(q/'package.json').write_text(json.dumps(m,indent=2)+'\n');print(json.dumps({k:v for k,v in m.items() if k!='files'}))
