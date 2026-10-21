"""Package only the already-built final-art; never author or rebuild assets."""
import hashlib,json,shutil,zipfile
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'docs/v10-production';C=R/'.cache/v10-final-portable';name='Korean-Arena-V10-Final-Review'
root=C/name
if root.exists():shutil.rmtree(root) # Owned disposable output, never a source directory.
site=root/'site/3D-pharse5-';shutil.copytree(R/'dist',site)
assert not (site/'assets/world').exists(),'Legacy runtime must not ship'
launcher='''"""V10 final-art review — local HTTP launcher (Python 3, no Node required)."""
import argparse,functools,http.server,pathlib,webbrowser
p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8080);p.add_argument('--no-browser',action='store_true');a=p.parse_args()
class Handler(http.server.SimpleHTTPRequestHandler):
 def end_headers(self):
  self.send_header('Cache-Control','no-store');super().end_headers()
directory=pathlib.Path(__file__).resolve().parent/'site'
with http.server.ThreadingHTTPServer(('127.0.0.1',a.port),functools.partial(Handler,directory=str(directory))) as server:
 url=f'http://127.0.0.1:{server.server_port}/3D-pharse5-/v10-city-review.html'
 print('V10 FINAL ART — awaiting visual approval',flush=True);print(url,flush=True)
 if not a.no_browser:webbrowser.open(url)
 try:server.serve_forever()
 except KeyboardInterrupt:pass
'''
(root/'start.py').write_text(launcher)
(root/'README.txt').write_text('V10 PLAYABLE FINAL ART — awaiting final visual approval.\nExtract, enter this folder, run python3 start.py (Windows: py start.py).\nWASD/arrows walk, Shift runs, E interacts; touch joystick on landscape mobile.\nOriginal V10 southern artwork; final visual approval pending. No public deployment.\n')
manifest={str(p.relative_to(site)):hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted(site.rglob('*'))if p.is_file()}
(root/'build-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
dest=D/'V10_FINAL_REVIEW.zip'
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(root.rglob('*')):
        if p.is_file():z.write(p,p.relative_to(C))
proof=dict(bytes=dest.stat().st_size,sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),builtFiles=len(manifest),finalArt=True)
(D/'package.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps(proof))
