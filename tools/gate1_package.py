"""Package ONLY the stored Gate1 production build and approved shared actor dependencies."""
import json,hashlib,shutil,zipfile
from pathlib import Path
R=Path(__file__).resolve().parents[1];C=R/'.cache/gate1/package';D=R/'docs/gate1';root=C/'Korean-Arena-Gate1';site=root/'site/3D-pharse5-'
if root.exists():shutil.rmtree(root)
shutil.copytree(R/'dist-gate1',site)
for sub in ['gate1','juni','actors/hero']:
 dest=site/'assets'/sub
 if dest.exists():shutil.rmtree(dest)
 shutil.copytree(R/'public/assets'/sub,dest)
shared=site/'assets/shared';shared.mkdir(parents=True,exist_ok=True);shutil.copy2(R/'public/assets/shared/leaf.png',shared/'leaf.png')
# Keep a complete exact portable build for verification; no graybox/rejected south is shipped.
for sub in ['world','v10-city','v9-world']:assert not(site/'assets'/sub).exists()
(root/'start.py').write_text('''import argparse,functools,http.server,pathlib,webbrowser
p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8080);p.add_argument('--no-browser',action='store_true');a=p.parse_args()
class Handler(http.server.SimpleHTTPRequestHandler):
 def end_headers(self):self.send_header('Cache-Control','no-store');super().end_headers()
base=pathlib.Path(__file__).resolve().parent/'site'
with http.server.ThreadingHTTPServer(('127.0.0.1',a.port),functools.partial(Handler,directory=str(base)))as server:
 url=f'http://127.0.0.1:{server.server_port}/3D-pharse5-/gate1-street.html';print(url,flush=True)
 if not a.no_browser:webbrowser.open(url)
 try:server.serve_forever()
 except KeyboardInterrupt:pass
''')
(root/'README.txt').write_text('KOREAN ARENA — GATE1 VISUAL SAMPLE, USER APPROVAL PENDING\nExtract and run python3 start.py (Windows: py start.py). Python3 required, no Node needed.\nWASD/arrows walk, Shift runs, E opens a venue card, Space greets. Landscape mobile has joystick and interaction button.\nFour new original buildings, one continuous sidewalk and public gathering court. No full-world rebuild or deployment.\nDefault1x camera follows Juni; add ?overview to the printed URL for the complete native1536x1024 scene (large display recommended).\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();manifest={str(p.relative_to(site)):sha(p)for p in sorted(site.rglob('*'))if p.is_file()};(root/'build-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
# Exact same files under dist-gate1 for byte-equality verification.
for sub in ['gate1','juni','actors/hero']:
 dest=R/'dist-gate1/assets'/sub
 if dest.exists():shutil.rmtree(dest)
 shutil.copytree(site/'assets'/sub,dest)
out=R/'dist-gate1/assets/shared';out.mkdir(exist_ok=True);shutil.copy2(shared/'leaf.png',out/'leaf.png')
zipfile_path=D/'GATE1_PLAYABLE.zip'
with zipfile.ZipFile(zipfile_path,'w',zipfile.ZIP_DEFLATED)as z:
 for p in sorted(root.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(C))
proof=dict(bytes=zipfile_path.stat().st_size,sha256=sha(zipfile_path),files=len(manifest),fullWorldIncluded=False,userVisualApproval='PENDING');(D/'package.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps(proof))
