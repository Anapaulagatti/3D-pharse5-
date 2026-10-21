"""Static allowlist ZIP, preserved repository subpath and local HTTP launcher."""
from pathlib import Path
import json,hashlib,zipfile,subprocess
R=Path(__file__).resolve().parents[1];D=R/'dist';Q=R/'docs/v9-world';Q.mkdir(exist_ok=True);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
launcher='''#!/usr/bin/env python3
from pathlib import Path
import argparse,functools,http.server,webbrowser
p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8765);p.add_argument('--no-browser',action='store_true');a=p.parse_args();root=Path(__file__).resolve().parent
class Handler(http.server.SimpleHTTPRequestHandler):
 def do_GET(self):
  if self.path=='/favicon.ico':self.send_response(204);self.end_headers();return
  super().do_GET()
url=f'http://localhost:{a.port}/3D-pharse5-/v9-world-review.html'
with http.server.ThreadingHTTPServer(('127.0.0.1',a.port),functools.partial(Handler,directory=str(root)))as server:
 print('Open in a web browser:',url,flush=True)
 if not a.no_browser:webbrowser.open(url)
 try:server.serve_forever()
 except KeyboardInterrupt:pass
'''
readme='''KOREAN ARENA — V9 REVIEW CANDIDATE (USER ART APPROVAL PENDING)

1. Extract this whole ZIP, retaining its directory structure.
2. Install/use Python3. Open a terminal inside Korean-Arena-V9-World-Review.
3. Run: python start.py (Windows can use: py start.py)
4. Open http://localhost:8765/3D-pharse5-/v9-world-review.html in a browser.

Alternative: python -m http.server 8765 from this same folder, then open the same URL.
Do not double-click index.html or use a raw source-code viewer; the bundled app needs HTTP.
No Node, API key, login, remote service or paid dependency is required for this static package.

WASD/arrows or joystick move; hold Shift/Run to run; E/Explore interacts.
Emote menu: Wave/Celebrate. Ferry: walk onto the landing, Explore, then confirm the trip.
Settings: reduced motion follows OS preference, native1x/2x zoom and Canvas compatibility.
Mobile: landscape; controls stay available and portrait orientation pauses the game.
This is a fictional learning-tour geography, not a real mainland/Jeju route reconstruction.
No public deployment or map-lock approval is implied.
'''
rows=[];files=[]
for p in sorted(D.rglob('*')):
 if not p.is_file():continue
 rel=p.relative_to(D).as_posix()
 if rel in ['index.html','v9-world-review.html']or rel.startswith(('assets/','licenses/')):
  assert p.suffix not in ['.map','.env','.blend','.glb','.gltf'],rel
  files.append((p,'3D-pharse5-/'+rel));rows.append({'file':'3D-pharse5-/'+rel,'sha256':sha(p),'bytes':p.stat().st_size})
assert {'3D-pharse5-/index.html','3D-pharse5-/v9-world-review.html'}<={r['file']for r in rows}
manifest={'candidate':'Korean Arena V9 — new southern world, art review pending','sourceCheckpoint':head,'branch':'rebuild/pixel-social-rpg-v3','world':[4352,6144],'base':'/3D-pharse5-/','distribution':'Static review package only, no automatic deployment','files':rows}
root='Korean-Arena-V9-World-Review/'
with zipfile.ZipFile(Q/'playable-review.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
 for p,name in files:z.write(p,root+name)
 z.writestr(root+'start.py',launcher);z.writestr(root+'README.txt',readme);z.writestr(root+'REVIEW_MANIFEST.json',json.dumps(manifest,indent=2)+'\n')
 for name in ['LICENSE','LICENSES.md']:z.write(R/name,root+name)
proof={'sha256':sha(Q/'playable-review.zip'),'bytes':(Q/'playable-review.zip').stat().st_size,'files':len(rows)+5,'sourceCheckpoint':head,'allowlist':['index.html','v9-world-review.html','assets/**','licenses/**','start.py','README.txt','LICENSE','LICENSES.md','REVIEW_MANIFEST.json'],'httpVerified':False};(Q/'package.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps(proof))
