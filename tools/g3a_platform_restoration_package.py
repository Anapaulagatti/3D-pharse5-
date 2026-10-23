from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import re,json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'docs/g3a-platform-restoration';B=Path('/tmp/g3-platform-restoration');files={}
for scene in ['world','district','registration','registration-refined','registration-forecourt','registration-review','registration-working-v3']:
 rel=f'assets/gate3/{scene}/manifest.json';m=json.loads((R/'public'/rel).read_text());names=[rel,m['overview']]+[c[k]for c in m['chunks']for k in ['image','mask']]+[o['image']for o in m['objects']]
 for n in names:files[n]=(R/'public'/n).read_bytes()
for n in ['assets/juni/juni.png','assets/juni/juni.json']:files[n]=(R/'public'/n).read_bytes()
files['gate3-review.html']=(B/'gate3-review.html').read_bytes()
for n in re.findall(r'(?:src|href)="\./([^"]+)"',files['gate3-review.html'].decode()):files[n]=(B/n).read_bytes()
for p in D.iterdir():
 if p.suffix in ['.png','.md','.json']and p.name not in ['package-proof.json','published-links.json']:files[str(p.relative_to(R))]=p.read_bytes()
for n in ['assets-src/gate3/production-plan-v3.1-restored.json','assets-src/gate3/approved-station-forecourt.json','docs/current/G3A_PLATFORM_VISUAL_REJECTION.md']:files[n]=(R/n).read_bytes()
files['index.html']=b'''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Original station-platform restoration</title><style>body{font:18px system-ui;margin:2em;max-width:1000px}li{margin:1em}img{max-width:100%;image-rendering:pixelated}</style><h1>Original station-platform artwork restored</h1><p>Accepted Maru/Namsan/retail preserved. Station transfer BLOCKED. No new connector or collision opening. G3-B BLOCKED.</p><ul><li><a href="gate3-review.html?scene=registration-working-v3&entry=station">Play restored station</a></li><li><a href="gate3-review.html?scene=registration-working-v3&entry=platform">Test blocked transfer from platform</a></li><li><a href="gate3-review.html?scene=registration-working-v3&entry=convenience">Accepted Maru</a></li><li><a href="docs/g3a-platform-restoration/README.md">Evidence and QA</a></li><li><a href="docs/g3a-platform-restoration/COLLISION_PROPOSAL.md">Collision-only proposal</a></li></ul><img src="docs/g3a-platform-restoration/BEFORE_RESTORED_1X.png" alt="Before and restored native comparison"><p>Extract fully; run python3 -m http.server 4292 --bind 127.0.0.1 and open http://127.0.0.1:4292 . Physical devices NOT TESTED; no deployment.</p>'''
files['START_REVIEW.txt']=b'Extract fully. Run python3 -m http.server 4292 --bind 127.0.0.1 in extracted folder. Open http://127.0.0.1:4292 . Review branch only. Station transfer BLOCKED; G3-B BLOCKED; physical devices NOT TESTED.\n'
assert not any(n.endswith('platform-opening-connector.png')or'/registration-working-v3/roof-overhead.png'in n for n in files)
files['PACKAGE_SHA256.json']=(json.dumps({n:hashlib.sha256(b).hexdigest()for n,b in files.items()},indent=2)+'\n').encode()
out=D/'G3A_PLATFORM_RESTORED_REVIEW.zip'
with ZipFile(out,'w',ZIP_DEFLATED,compresslevel=6)as z:
 for n,b in sorted(files.items()):z.writestr(n,b)
with ZipFile(out)as z:
 assert z.testzip()is None
 assert all(hashlib.sha256(z.read(n)).hexdigest()==h for n,h in json.loads(z.read('PACKAGE_SHA256.json')).items())
(D/'package-proof.json').write_text(json.dumps({'file':out.name,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'CRC':'PASS','allFileHashes':'PASS','rejectedConnectorIncluded':False,'stationTransfer':'BLOCKED'},indent=2)+'\n');print(out.name,out.stat().st_size)
