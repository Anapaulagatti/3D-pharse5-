"""Allowlisted current static build + notices + actual local HTTP launcher. No source or old projects."""
from pathlib import Path
import json,hashlib,shutil,zipfile,argparse
ap=argparse.ArgumentParser();ap.add_argument('--review-dir',default='docs/review');ap.add_argument('--entry',choices=['','character-review.html','plaza-review.html','district-review.html'],default='');ap.add_argument('--folder',choices=['Korean-Arena-Review','Korean-Arena-Character-Review','Korean-Arena-Gwanghwamun-Review','Korean-Arena-Juni-Animation-Review','Korean-Arena-Living-Seoul-Review'],default='Korean-Arena-Review');a=ap.parse_args()
R=Path(__file__).resolve().parents[1];D=R/'dist';assert (D/'index.html').exists();files=[p for p in D.rglob('*') if p.is_file()]
for p in files:
 assert p.suffix in {'.html','.js','.css','.png','.json','.svg','.txt'},p
 if p.suffix in {'.html','.js','.css','.json','.txt'}:
  t=p.read_text();assert not any(s in t for s in ['BEGIN PRIVATE KEY','ghp_','sk-proj-']),p
assert len(list((D/'assets/world').iterdir()))==23
for actor in ['hero','sejong','jang','saimdang','yi']:assert (D/'assets/actors'/actor/'atlas.json').exists()
assert not any(p.suffix in ['.blend','.glb'] for p in files)
rows=[{'path':str(p.relative_to(D)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in sorted(files)];buildhash=hashlib.sha256(json.dumps(rows).encode()).hexdigest()[:12];stage=R/'.cache/portable'/buildhash;root=stage/a.folder;root.mkdir(parents=True,exist_ok=True);shutil.copytree(D,root/'3D-pharse5-',dirs_exist_ok=True)
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
launcher=launcher.replace("/3D-pharse5-/'",f"/3D-pharse5-/{a.entry}'")
(root/'start.py').write_text(launcher);(root/'README.txt').write_text(('Korean Arena — THREE STATIC CHARACTER CONCEPTS, A/B/C. NOT APPROVED OR PUBLICLY RELEASED.\nChoose front/back/left/right and 1x native / 2x gameplay camera. These are static direction drawings, not action animations. The current game is preserved and linked separately; its old actors have been rejected and await a future approved replacement.\n' if a.entry else 'Korean Arena — current animation/historical guest review, NOT PUBLICLY RELEASED.\nWASD/arrows walk; Shift run; E nearby guest; Space wave.\n')+'Extract, run python3 start.py (Windows py start.py), open printed HTTP URL. Python 3 required; no Node needed to view. Do not open HTML as source or file://. Ctrl+C stops. No online users, paid services or ads.\n')
if a.entry=='plaza-review.html':(root/'README.txt').write_text('KOREAN ARENA — GWANGHWAMUN PLAZA ART REVIEW, NOT A PUBLIC RELEASE.\nThree original plaza concepts; recommended B/Ginkgo Commons is playable in Phaser. Juni/B is provisional; Bori/A and Nari/C remain future avatar styles. Juni has144genuine image-generated frames:4way idle/walk/run/start/stop,8orientation turn and front wave/celebration/social gestures. No mirrored or rigid-bounce substitute.\nExtract, run python3 start.py (Windows py start.py), open the printed HTTP URL ending /3D-pharse5-/plaza-review.html. Python3 required; no Node needed to view. Do not open file:// or the HTML source viewer.\nWASD/arrows move, Shift/run accelerates, E/click explores landmarks. Camera1x/2x/3x, evening, pause, reduced-motion and mobile touch available. Use the brand link to open the preserved previous town. The gallery below the game is generated concept art, not engine captures. No server account, API, ads or multiplayer. Ctrl+C stops. Stop for visual approval; other districts and new NPCs are not produced. Side idle/small gesture motion remains a visual-review item; physical phone performance is unmeasured.\n')
if a.entry=='district-review.html':(root/'README.txt').write_text('KOREAN ARENA - LIVING SEOUL FIRST CONNECTED SLICE / VISUAL REVIEW, NOT PUBLIC RELEASE.\nOutdoor2048x768 preserves the approved plaza and Juni, adds book alley, Academy court and lazy-loaded768x576reading room. Future districts and new animated historical guests are NOT included yet.\nExtract this entire folder. Run python3 start.py (Windows: py start.py). Python3required, noNode needed. Open printed HTTP URL ending /3D-pharse5-/district-review.html; do not open file:// or source viewer. Ctrl+C stops server.\nWASD/arrows walk, Shift/run accelerates; E or Explore near Academy doorway enters/exits. Cross the old bridge and follow the eastern book alley. In room, approach central desk and E for3letter-name matching activity. Wrong answers retry; completion saves locally when browser storage permits. Use close button to resume. Camera1x/2x/3x, evening, reduced-motion and touch supported. No accounts, paid providers, ads or multiplayer. Brand link preserves old town; plaza-review.html preserves earlier plaza.\nMap density/material edges and new architecture remain visual-review items. Mobile is emulated, physical-phoneFPS is unmeasured. No website deployment.\n')
q=R/a.review_dir;assert q.resolve().is_relative_to((R/'docs').resolve());q.mkdir(parents=True,exist_ok=True);dest=q/'playable-review.zip'
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(root.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(stage))
sha=hashlib.sha256(dest.read_bytes()).hexdigest();extract=R/'.cache/extracted'/sha[:12];extract.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(dest) as z:
 assert z.testzip() is None and all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in z.namelist());z.extractall(extract)
for r in rows:assert hashlib.sha256((extract/a.folder/'3D-pharse5-'/r['path']).read_bytes()).hexdigest()==r['sha256']
m={'status':'PACKAGED_PENDING_HTTP_BROWSER_VERIFICATION','zip':str(dest.relative_to(R)),'zip_bytes':dest.stat().st_size,'zip_sha256':sha,'build_bytes':sum(r['bytes'] for r in rows),'files':rows,'extract_root':str(extract/a.folder),'entry':a.entry,'security_scan':'dist only; suffix allowlist; no private-key/provider-token markers,3D or authoring sources; original/Phaser/Zod notices included. Current working game actors deliberately retained pending replacement approval.'}
(q/'package.json').write_text(json.dumps(m,indent=2)+'\n');print(json.dumps({k:v for k,v in m.items() if k!='files'}))
