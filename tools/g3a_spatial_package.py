from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,re,hashlib
R=Path(__file__).resolve().parents[1];D=R/'docs/g3a-spatial-review';B=Path('/tmp/g3-spatial-review');files={}
for kind in ['world','district','registration','registration-refined']:
 rel=f'assets/gate3/{kind}/manifest.json';m=json.loads((R/'public'/rel).read_text());names=[rel,m['overview']]+[p for c in m['chunks']for p in [c['image'],c['mask']]]+[o['image']for o in m['objects']]
 for n in names:files[n]=(R/'public'/n).read_bytes()
for n in ['assets/juni/juni.png','assets/juni/juni.json']:files[n]=(R/'public'/n).read_bytes()
html=(B/'gate3-review.html').read_bytes();files['gate3-review.html']=html
for n in re.findall(r'(?:src|href)="\./([^"]+)"',html.decode()):files[n]=(B/n).read_bytes()
for p in D.iterdir():
 if p.suffix in ['.md','.json','.png']and p.name not in ['package-proof.json','published-links.json','package-smoke.json']:files['docs/g3a-spatial-review/'+p.name]=p.read_bytes()
for n in ['docs/gate3a-pixel-audit/REPORT.md','docs/gate3a-corrections/DEVICE_CHECKLIST.md']:files[n]=(R/n).read_bytes()
files['index.html']=b'''<!doctype html><meta charset="utf-8"><title>G3-A targeted spatial comparison</title><h1>G3-A comparison / final approval withheld</h1><p>Q1 requires explicit additional land and pacing approval. Maru requires allocation and a local scenic-loop amendment. No approved masterplan modification or G3-B authorization.</p><ul><li><a href="gate3-review.html?scene=registration-refined&entry=bakery">Q1 southwest quay bakery</a></li><li><a href="gate3-review.html?scene=registration&entry=bakery">W0 waterfront bakery / rejected preferred site</a></li><li><a href="gate3-review.html?scene=registration-refined&entry=convenience">Revised Maru / glass-door approach</a></li><li><a href="gate3-review.html?scene=registration&entry=convenience">Original Maru reference</a></li><li><a href="gate3-review.html?scene=registration-refined&entry=namsan">Candidate western Namsan loop</a></li><li><a href="gate3-review.html?scene=registration-refined&entry=station">Protected station</a></li><li><a href="gate3-review.html?scene=world">Unchanged approved default world foundation</a></li><li><a href="gate3-review.html?scene=district&entry=station&renderer=canvas&native">Corrected Canvas district native1:1</a></li><li><a href="docs/g3a-spatial-review/REGISTRATION.md">Exact comparison and conflicts</a></li><li><a href="docs/g3a-spatial-review/QA.md">PASS/FAIL report</a></li><li><a href="docs/g3a-spatial-review/SITE_COMPARISON.png">Technical spatial overlay</a></li><li><a href="docs/g3a-spatial-review/bakery-quay-1x.png">Native bakery screenshot</a></li><li><a href="docs/g3a-spatial-review/maru-revised-1x.png">Native Maru screenshot</a></li><li><a href="docs/gate3a-corrections/DEVICE_CHECKLIST.md">Physical device checklist / NOT TESTED</a></li></ul>'''
files['START_REVIEW.txt']=b'Extract all files. Run python3 -m http.server 4284 --bind 127.0.0.1 and open http://127.0.0.1:4284/ . Local/private review only. Source art unchanged. Original masterplan not amended. G3-B blocked; final spatial approval withheld. Full native PNGs are in docs/g3a-spatial-review. Physical Android/iPhone NOT TESTED. No public deployment.\n'
files['BUILD_SOURCES_SHA256.json']=(json.dumps({str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in (R/'src/gate3').rglob('*')if p.is_file()},indent=2)+'\n').encode()
files['PACKAGE_SHA256.json']=(json.dumps({n:hashlib.sha256(b).hexdigest()for n,b in sorted(files.items())},indent=2)+'\n').encode()
out=D/'G3A_SPATIAL_COMPARISON.zip'
with ZipFile(out,'w',ZIP_DEFLATED,compresslevel=6)as z:
 for n,b in sorted(files.items()):z.writestr(n,b)
with ZipFile(out)as z:
 assert z.testzip()is None
 for n,h in json.loads(z.read('PACKAGE_SHA256.json')).items():assert hashlib.sha256(z.read(n)).hexdigest()==h,n
 for n in re.findall(r'href="([^"]+)"',z.read('index.html').decode()):assert n.split('?')[0]in files,n
(D/'package-proof.json').write_text(json.dumps({'file':out.name,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'CRC':'PASS','allFileHashes':'PASS','indexLinks':'PASS'},indent=2)+'\n');print(out.name,out.stat().st_size)
