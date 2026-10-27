"""Portable requested-only runtime and compact review evidence. Never rebuilds approved art."""
from core import *
from zipfile import ZipFile,ZIP_DEFLATED
import posixpath,re
O=Path('/tmp/phase2c-review');TAG='checkpoint/phase2c-fashion-studio-review-20261027';RAW=f'https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/refs/tags/{TAG}/';files={}
m=json.loads((R/'public/assets/gate3/palace-cleanup-world/manifest.json').read_text());names={'assets/gate3/palace-cleanup-world/manifest.json',m['overview'],m['farmMetadata'],m['contactCollision']['physical'],'assets/juni/juni.png','assets/juni/juni.json','assets/character-studio/juni-preview.png'}|{c[k]for c in m['chunks']for k in ['image','mask']}|{o['image']for o in m['objects']}
for id in list(B)[1:]:
 for n in ['atlas.png','atlas.json','preview-native.png']:names.add(f'assets/characters/{id}/{n}')
for p in P.rglob('*'):
 if p.is_file():names.add(str(p.relative_to(R/'public')))
for n in names:files[n]=(R/'public'/n).read_bytes()
files['index.html']=(O/'index.html').read_bytes();build=json.loads((O/'.vite/manifest.json').read_text())
for row in build.values():
 for n in [row['file']]+row.get('css',[])+row.get('assets',[]):files[n]=(O/n).read_bytes()
files['BUILD_MANIFEST.json']=json.dumps(build,indent=2).encode()
selectedVideos={'fashion-juni-actual-gameplay.mp4','fashion-sori-actual-gameplay.mp4','juni-default-actual-gameplay.mp4','sori-default-actual-gameplay.mp4','studio-session-actual.mp4'}
for p in D.rglob('*'):
 if not p.is_file():continue
 n=p.name
 if p.suffix in ['.webm','.zip']or'working'in n or n in ['package-proof.json','package-smoke.json','published-verification.json','curated-capture.json','actual-gameplay.json','first-run-results.json']:continue
 if p.suffix=='.mp4'and n not in selectedVideos:continue
 if n.endswith('-phaser-native.png'):continue
 if p.suffix=='.png':
  if p.parent.name in ['foundation','pilot']:continue
  if p.parent.name=='gameplay'and not n.endswith('-actual-native-sheet.png'):continue
  if n=='custom-ara-webgl-native.png':continue
 if p.suffix in ['.md','.html','.jpg','.mp4','.png','.json','.log']and(p.suffix!='.json'or p.stat().st_size<1500000):files[str(p.relative_to(R))]=p.read_bytes()
for n in ['AGENTS.md','LICENSE','LICENSES.md','docs/current/PROJECT_STATE.md','assets-src/characters/phase2c/catalog.json','assets-src/characters/phase2c/base-bindings.json']:files[n]=(R/n).read_bytes()
files['start_review.py']=(R/'tools/phase2c/start_review.py').read_bytes()
for name in ['phaser','zod']:
 p=R/'node_modules'/name/'LICENSE'
 if not p.exists():p=R/'node_modules'/name/'LICENSE.txt'
 if p.exists():files[f'LICENSES/{name}.txt']=p.read_bytes()
files['README.md']=b'# Korean Arena Phase2C Fashion Studio review\n\nRun python3 start_review.py and open http://127.0.0.1:4342/REVIEW.html. Actual portable compiled Phaser plus canonical frozen world,12approved original actors,28free review cosmetics and12curatedlooks. No Node/install/network needed to play.\n\nFive representative actual videos and native crops/sheets are included. Other per-character videos and large full-native captures link to the immutable checkpoint and require network. PNGs are pixel authority; videos are timing evidence.\n\nTECHNICAL PASS - ARTISTIC APPROVAL PENDING. Physical devices NOT TESTED. Phase3 locked. No main merge/public deployment. See docs/phase2c/DEVICE_REVIEW.html for local report export; --lan is explicit opt-in on your own network.\n'
files['REVIEW.html']=b'<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Phase2C Fashion Studio</title><h1>Korean Arena Phase2C</h1><p><a href="index.html">Play actual Phaser</a> | <a href="docs/phase2c/REVIEW.html">Visual gallery and gameplay videos</a> | <a href="docs/phase2c/QA.md">QA</a> | <a href="docs/phase2c/DEVICE_REVIEW.html">Physical-device checklist/export</a></p><p>TECHNICAL PASS - ARTISTIC APPROVAL PENDING. Phase3 locked. Physical devices NOT TESTED.</p>'
# Preserve local links where included; omitted evidence resolves at the review tag.
for n,data in list(files.items()):
 if not n.endswith(('.md','.html')):continue
 def fix(match):
  t=match.group(1)
  if t.startswith(('http:','https:','#','data:','mailto:')):return match.group(0)
  clean=t.split('?')[0].split('#')[0];path=posixpath.normpath(posixpath.join(posixpath.dirname(n),clean)).lstrip('/')
  if path in files:return match.group(0)
  return match.group(0).replace(t,RAW+path)
 text=data.decode();text=re.sub(r'(?:href|src)="([^"]+)"',fix,text);text=re.sub(r'\]\(([^)]+)\)',fix,text);files[n]=text.encode()
files['PACKAGE_SHA256.json']=(json.dumps({n:hashlib.sha256(b).hexdigest()for n,b in sorted(files.items())},indent=2)+'\n').encode();out=D/'PHASE2C_FASHION_STUDIO_REVIEW.zip'
with ZipFile(out,'w',ZIP_DEFLATED,compresslevel=6)as z:
 for n,b in sorted(files.items()):z.writestr(n,b)
with ZipFile(out)as z:
 assert z.testzip()is None
 for n,h in json.loads(z.read('PACKAGE_SHA256.json')).items():assert hashlib.sha256(z.read(n)).hexdigest()==h,n
 for id,h in B.items():
  n='assets/juni/juni.png'if id=='juni'else f'assets/characters/{id}/atlas.png';assert hashlib.sha256(z.read(n)).hexdigest()==h,id
assert out.stat().st_size<100000000,out.stat().st_size
report={'file':out.name,'bytes':out.stat().st_size,'sha256':sha(out),'files':len(files),'runtimeFiles':len(names),'CRC':'PASS','allFileHashes':'PASS','all12ApprovedAtlasesExact':'PASS','relativePortableBuild':True,'runtime':{n:hashlib.sha256(b).hexdigest()for n,b in files.items()if n.startswith('assets/')or n in ['index.html','BUILD_MANIFEST.json']},'includedVideos':sorted(selectedVideos),'sourceCheckpoint':TAG,'physicalDevices':'NOT TESTED','humanArtApproval':'PENDING'};(D/'package-proof.json').write_text(json.dumps(report,indent=2)+'\n');print(out.name,out.stat().st_size,'bytes',len(files),'files')
