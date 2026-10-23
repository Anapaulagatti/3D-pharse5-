from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,re,hashlib
R=Path(__file__).resolve().parents[1];D=R/'docs/g3a-forecourt-restoration';B=Path('/tmp/g3-forecourt-restoration');files={}
for scene in ['world','district','registration','registration-refined','registration-forecourt']:
 rel=f'assets/gate3/{scene}/manifest.json';m=json.loads((R/'public'/rel).read_text());names=[rel,m['overview']]+[n for c in m['chunks']for n in [c['image'],c['mask']]]+[o['image']for o in m['objects']]
 for n in names:files[n]=(R/'public'/n).read_bytes()
for n in ['assets/juni/juni.png','assets/juni/juni.json']:files[n]=(R/'public'/n).read_bytes()
files['gate3-review.html']=(B/'gate3-review.html').read_bytes()
for n in re.findall(r'(?:src|href)="\./([^"]+)"',files['gate3-review.html'].decode()):files[n]=(B/n).read_bytes()
for p in D.iterdir():
 if p.suffix in ['.md','.png','.json','.mp4']and p.name not in ['package-proof.json','package-smoke.json','published-links.json','NATIVE_LINKS.md']:files[str(p.relative_to(R))]=p.read_bytes()
for root in ['assets-src/gate3/forecourt-restoration','src/gate3']:
 for p in (R/root).rglob('*'):
  if p.is_file():files[str(p.relative_to(R))]=p.read_bytes()
for n in ['tools/g3a_restore_forecourt.py','tools/g3a_restoration_capture.mjs','tools/g3a_restoration_proof.py','tools/g3a_restoration_package.py','tools/g3a_restoration_smoke.mjs','docs/gate3a-corrections/DEVICE_CHECKLIST.md']:files[n]=(R/n).read_bytes()
files['index.html']='''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Station native-ground restoration candidate</title><style>body{font:18px system-ui;max-width:900px;margin:2em auto;padding:0 1em;background:#17242e;color:#fff}a{color:#a9ddff}li{margin:1em 0}img{max-width:100%;image-rendering:pixelated}video{max-width:100%}</style><h1>Station forecourt restoration candidate</h1><p>Actual native ground repair; human visual approval PENDING. G3-B BLOCKED. Approved default assets unchanged. No public deployment.</p><ul><li><a href="gate3-review.html?scene=registration-forecourt&entry=station">PLAY restored candidate (follow camera)</a></li><li><a href="gate3-review.html?scene=registration-refined&entry=station">PLAY unchanged before comparison</a></li><li><a href="gate3-review.html?scene=registration-forecourt&entry=station&native&pixelAudit">Restored fixed native1:1 frame</a></li><li><a href="gate3-review.html?scene=registration-refined&entry=station&native&pixelAudit">Before fixed native1:1 frame</a></li><li><a href="gate3-review.html?scene=registration-forecourt&entry=station&native&pixelAudit&renderer=canvas">Restored Canvas fallback native1:1</a></li><li><a href="docs/g3a-forecourt-restoration/SOURCE_CURRENT_RESTORED_1X.png">Source / current / restored at same native scale</a></li><li><a href="docs/g3a-forecourt-restoration/before-auto-native.png">Before native Phaser PNG</a></li><li><a href="docs/g3a-forecourt-restoration/after-auto-native.png">After native Phaser PNG</a></li><li><a href="docs/g3a-forecourt-restoration/station-with-juni-1x.png">Station frontage with Juni</a></li><li><a href="docs/g3a-forecourt-restoration/forecourt-walk.mp4">Actual walking video</a></li><li><a href="docs/g3a-forecourt-restoration/QA.md">QA and remaining visual issues</a></li><li><a href="docs/gate3a-corrections/DEVICE_CHECKLIST.md">Physical device checklist: NOT TESTED</a></li></ul><p>WASD/arrows, Shift run; existing mobile joystick. Lossless PNGs are pixel evidence; compressed video is traversal evidence. Source and masks included for provenance.</p><img src="docs/g3a-forecourt-restoration/SOURCE_CURRENT_RESTORED_1X.png" alt="Native1:1 comparisons"><video controls preload="metadata" src="docs/g3a-forecourt-restoration/forecourt-walk.mp4"></video>'''.encode()
files['START_REVIEW.txt']=b'Extract all files. Run python3 -m http.server 4286 --bind 127.0.0.1 inside the extracted folder. Open http://127.0.0.1:4286/ . Candidate-only repair; comparison retained. No public deployment. Physical devices NOT TESTED. Human visual approval required; G3-B BLOCKED.\n'
files['BUILD_SOURCES_SHA256.json']=(json.dumps({str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in (R/'src/gate3').rglob('*')if p.is_file()},indent=2)+'\n').encode()
files['PACKAGE_SHA256.json']=(json.dumps({n:hashlib.sha256(b).hexdigest()for n,b in sorted(files.items())},indent=2)+'\n').encode()
out=D/'G3A_FORECOURT_RESTORATION.zip'
with ZipFile(out,'w',ZIP_DEFLATED,compresslevel=6)as z:
 for n,b in sorted(files.items()):z.writestr(n,b)
with ZipFile(out)as z:
 assert z.testzip()is None
 for n,h in json.loads(z.read('PACKAGE_SHA256.json')).items():assert hashlib.sha256(z.read(n)).hexdigest()==h,n
 for n in re.findall(r'href="([^"]+)"',z.read('index.html').decode()):assert n.split('?')[0]in files,n
(D/'package-proof.json').write_text(json.dumps({'file':out.name,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'CRC':'PASS','allFileHashes':'PASS','indexLinks':'PASS','candidateOnly':True,'G3B':'BLOCKED'},indent=2)+'\n');print(out.name,out.stat().st_size)
