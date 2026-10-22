"""Private local acceptance build package; no deployment or asset generation."""
from pathlib import Path
import shutil,json,hashlib,zipfile
R=Path(__file__).resolve().parents[1];root=R/'.cache/gate2/acceptance/package';D=R/'docs/gate2/acceptance'
if root.exists():shutil.rmtree(root)
app=root/'3D-pharse5-';shutil.copytree(R/'dist-gate2',app);shutil.copytree(R/'public/assets/gate2',app/'assets/gate2');shutil.copytree(R/'public/assets/juni',app/'assets/juni')
(root/'start.py').write_text('''from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
import os,sys
os.chdir(Path(__file__).resolve().parent)
port=int(sys.argv[1]) if len(sys.argv)>1 else 8064
print(f"Open http://127.0.0.1:{port}/3D-pharse5-/gate2-review.html?scene=original",flush=True)
ThreadingHTTPServer(("127.0.0.1",port),SimpleHTTPRequestHandler).serve_forever()
''')
(root/'README.txt').write_text('''Gate2 acceptance review only / Gate3 locked / human artistic approval pending
Run python3 start.py then open the local URL printed. No dependencies to install.
Select Original for the ONE new bakery; Station for exact-fit entrance; Join proof for Muneum/station; Jeju fit for the CANDIDATE technical graybox registration. A/B/C/transition retain their source art.
WASD/arrows move; Shift runs; E explores; Space greets.
Mobile landscape: joystick, Run, Explore. Scenic freezes player control; drag/pinch to look. Full scene shows current Juni, landmarks and previous follow viewport. Return to Juni restores native gameplay. Reduced views are not native1:1 art evidence.
Options (...) contains Pause and OPTIONAL Landmark moments, off by default. Movement or Skip cancels the showcase; reduced motion suppresses it.
No ferry gameplay, full-world production, public deployment or main merge.
The approved masterplan/checkpoint and source images are unchanged. Fit candidate and judgments require human review. No physical-device performance certification.
''')
manifest=[dict(path=str(p.relative_to(root)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())for p in sorted(root.rglob('*'))if p.is_file()];(root/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
out=R/'docs/gate2/ACCEPTANCE_PLAYABLE.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,6)as z:
 for p in sorted(root.rglob('*')):
  if p.is_file():z.write(p,str(p.relative_to(root)))
with zipfile.ZipFile(out)as z:
 assert z.testzip()is None;extracted=R/'.cache/gate2/acceptance/extracted'
 if extracted.exists():shutil.rmtree(extracted)
 z.extractall(extracted)
for f in json.loads((extracted/'MANIFEST.json').read_text()):assert hashlib.sha256((extracted/f['path']).read_bytes()).hexdigest()==f['sha256']
(D/'package.json').write_text(json.dumps(dict(path='docs/gate2/ACCEPTANCE_PLAYABLE.zip',bytes=out.stat().st_size,sha256=hashlib.sha256(out.read_bytes()).hexdigest(),zipCRC='PASS',extractedManifestHashes='PASS',scenes=json.loads((app/'assets/gate2/catalog.json').read_text())),indent=2)+'\n');print('PASS acceptance ZIP and extracted hashes')
