"""Exact allowlisted static V7 runtime, licenses and an HTTP launcher. No authoring secrets."""
from pathlib import Path
import json,hashlib,shutil,zipfile
R=Path(__file__).resolve().parents[1];D=R/'dist';Q=R/'docs/v7-world';name='Korean-Arena-V7-World-Review'
files=[p for p in D.rglob('*')if p.is_file()and(str(p.relative_to(D)).startswith(('assets/','review/v7-world/','review/juni-animation/','review/living-seoul/room/'))or str(p.relative_to(D))=='review/gwanghwamun/leaf.png'or p.name in ['index.html','v7-world-review.html']or p.suffix=='.txt')]
assert any(p.name=='v7-world-review.html'for p in files)
for p in files:
 assert p.suffix in {'.html','.js','.css','.png','.json','.svg','.txt'},p
 if p.suffix in {'.html','.js','.css','.json','.txt'}:
  t=p.read_text();assert not any(k in t for k in ['BEGIN PRIVATE KEY','ghp_','sk-proj-','AKIA']),p
 assert not any(k in p.parts for k in ['.git','.aws','.env','assets-src','source-blend'])
rows=[{'path':str(p.relative_to(D)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}for p in sorted(files)];build=hashlib.sha256(json.dumps(rows).encode()).hexdigest()[:16];stage=R/'.cache/v7-portable'/build;root=stage/name;root.mkdir(parents=True,exist_ok=True)
for p in files:
 dest=root/'3D-pharse5-'/p.relative_to(D);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
(root/'start.py').write_text('''from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
import argparse,webbrowser
p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8000);p.add_argument('--no-browser',action='store_true');p.add_argument('--canvas',action='store_true');p.add_argument('--lan',action='store_true');a=p.parse_args()
path='/3D-pharse5-/v7-world-review.html'+('?renderer=canvas'if a.canvas else '')
url=f'http://127.0.0.1:{a.port}'+path
server=ThreadingHTTPServer(('0.0.0.0'if a.lan else '127.0.0.1',a.port),partial(SimpleHTTPRequestHandler,directory=str(Path(__file__).resolve().parent)))
print('Open: '+url,flush=True)
if a.lan:print('Same-WiFi phone: http://YOUR_COMPUTER_LAN_IP:'+str(a.port)+path,flush=True)
if not a.no_browser:webbrowser.open(url)
try:server.serve_forever()
except KeyboardInterrupt:server.server_close()
''')
(root/'README.txt').write_text('''KOREAN ARENA — V7 LIVING KOREA RECONSTRUCTION / USER VISUAL REVIEW, NOT PUBLIC RELEASE.
Extract ENTIRE Korean-Arena-V7-World-Review folder. Python3 required; no Node/account/API.
Run python3 start.py (Windows: py start.py), then open printed HTTP URL.
Never file:// or HTML source viewer. Ctrl+C stops. Optional --canvas, --lan for same-WiFi phone; manually rotate landscape.
WASD/arrows, Shift run, E Explore, Space wave; landscape joystick+Run+Explore/Talk/Emote. Portrait pauses, OS reduced-motion respected.
Follow unchanged palace/Academy north through warm threshold to station gardens/frontage, real central rail crossing/platform stair. West boulevard enters Namsan winding park; east promenade reaches centered amusement arch. Short coastal bridge crosses real inlet. Terminal→narrow boarding pier→Explore→confirm ferry to Jeju; northern island landing returns. Explore original Academy reading room/Hangul desk, basalt discovery, landmarks.
4352x5312, original native landmark images/Juni144frames preserved. New clean route/site graph, modern station/commercial plots, independent park campuses, real shore and island routes. Fictional educational geography; not historical reconstruction. Train/rides static scenic art, not minigames.
This package contains current V7 and retained base-town brand link only; older reviews, editable sources, archived3D and all recovery points remain in Git repository, not included here.
No paid API/backend/accounts/ads/multiplayer/public deployment. Actual physical phones/Safari/GPU unmeasured. STOP for user's visual approval.
''')
expected={Path('start.py'),Path('README.txt')}|{Path('3D-pharse5-')/r['path']for r in rows};assert {p.relative_to(root)for p in root.rglob('*')if p.is_file()}==expected
out=Q/'playable-review.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
 for p in sorted(root.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(stage))
assert out.stat().st_size<100_000_000
j={'status':'PACKAGED_PENDING_HTTP_BROWSER_VERIFICATION','zip':str(out.relative_to(R)),'zip_bytes':out.stat().st_size,'zip_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'files':rows,'entry':'v7-world-review.html','folder':name,'security_scan':'allowlisted static runtime suffixes; no token/private-key markers, authoring/3D/private paths; original license notices included; actual HTTP tests required'}
(Q/'package.json').write_text(json.dumps(j,indent=2)+'\n');print(json.dumps({k:v for k,v in j.items()if k!='files'}))
