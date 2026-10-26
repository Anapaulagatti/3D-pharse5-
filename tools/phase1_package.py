from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,hashlib,re,posixpath
R=Path(__file__).resolve().parents[1];D=R/'docs/phase1';B=Path('/tmp/phase1-review');files={};TAG='checkpoint/phase1-foundation-review-20261026';RAW='https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/refs/tags/'+TAG+'/'
m=json.loads((R/'public/assets/gate3/palace-cleanup-world/manifest.json').read_text());names={'assets/gate3/palace-cleanup-world/manifest.json',m['overview'],m['farmMetadata'],m['contactCollision']['physical'],'assets/juni/juni.png','assets/juni/juni.json'}|{c[k]for c in m['chunks']for k in ['image','mask']}|{o['image']for o in m['objects']}|{f'assets/characters/{id}/preview.png'for id in ['haneul','bomi','minjun']}
for name in names:files[name]=(R/'public'/name).read_bytes()
files['index.html']=(B/'index.html').read_bytes();manifest=json.loads((B/'.vite/manifest.json').read_text())
for row in manifest.values():
 for name in [row['file']]+row.get('css',[])+row.get('assets',[]):files[name]=(B/name).read_bytes()
files['BUILD_MANIFEST.json']=json.dumps(manifest,indent=2).encode()
for p in D.rglob('*'):
 if not p.is_file()or 'initial-attempt'in p.parts or p.name.startswith(('package-','published-','e2e-initial')):continue
 if p.suffix in ['.md','.html','.json','.jpg']or p.name.endswith('-native-crop.png')or p.name.endswith('-native-comparison.png')or p.name in ['selection-juni-gameplay-review.mp4']:files[str(p.relative_to(R))]=p.read_bytes()
for n in ['AGENTS.md','LICENSE','LICENSES.md','docs/current/PROJECT_STATE.md','docs/current/PHASE1_DIRECTIVE.md','docs/current/CLEANUP_MANIFEST.md'] :files[n]=(R/n).read_bytes()
for package in ['phaser','zod']:
 p=R/'node_modules'/package/'LICENSE'
 if not p.exists():p=R/'node_modules'/package/'LICENSE.txt'
 if p.exists():files[f'LICENSES/{package}.txt']=p.read_bytes()
with ZipFile(R/'docs/gate3-palace-cleanup/PALACE_CLEANUP_REVIEW.zip')as z:files['start_review.py']=z.read('start_review.py')
files['REVIEW.html']=b'<!doctype html><html><head><meta charset="utf-8"><title>Phase1 review</title></head><body><h1>Phase1 technical foundation / roster incomplete</h1><p>Only Juni playable. Haneul, Bomi, Minjun remain incomplete references.</p><p><a href="index.html">Play actual game</a> | <a href="docs/phase1/VISUAL_REVIEW.html">Visual evidence</a> | <a href="docs/phase1/QA.md">QA</a> | <a href="docs/phase1/DEVICE_REVIEW.md">Device checklist</a></p></body></html>'
files['README.md']=b'# Phase1 technical review / roster INCOMPLETE\n\nRun `python3 start_review.py`, open localhost. Default index is the actual approved world and character selector. Juni is complete; three new references are NOT playable. No account, Phase2 or deployment. Open REVIEW.html for native evidence/QA/device checklist. WASD/arrows, Shift, E, Space wave, C celebrate, mobile joystick retained. Settings -> character selection preserves current location. Actual phones/hardware NOT TESTED.\n'
for n,data in list(files.items()):
 if not n.endswith(('.md','.html')):continue
 text=data.decode()
 def fix(match):
  target=match.group(1)
  if target.startswith(('http:','https:','#','data:','mailto:'))or'?'in target:return match.group(0)
  path=posixpath.normpath(posixpath.join(posixpath.dirname(n),target)).lstrip('/')
  if path in files:return match.group(0)
  return match.group(0).replace(target,RAW+path)
 text=re.sub(r'(?:href|src)="([^"]+)"',fix,text);text=re.sub(r'\]\(([^)]+)\)',fix,text);files[n]=text.encode()
files['PACKAGE_SHA256.json']=(json.dumps({n:hashlib.sha256(b).hexdigest()for n,b in sorted(files.items())},indent=2)+'\n').encode();out=D/'PHASE1_FOUNDATION_REVIEW.zip'
with ZipFile(out,'w',ZIP_DEFLATED,compresslevel=9)as z:
 for n,b in sorted(files.items()):z.writestr(n,b)
with ZipFile(out)as z:
 assert z.testzip()is None
 for n,h in json.loads(z.read('PACKAGE_SHA256.json')).items():assert hashlib.sha256(z.read(n)).hexdigest()==h,n
assert out.stat().st_size<100000000
(D/'package-proof.json').write_text(json.dumps({'file':out.name,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'CRC':'PASS','allFileHashes':'PASS','canonicalWorld':'palace-cleanup-world','playableCharacters':['juni'],'incompleteCharacters':['haneul','bomi','minjun'],'entry':'index.html -> actual production game, not review mockup/V10','runtime':'All runtime JS/CSS/art/atlas/collision offline; large native frames use explicit immutable links','physicalDevices':'NOT TESTED','phase1Acceptance':'INCOMPLETE_ROSTER'},indent=2)+'\n');print(out.name,out.stat().st_size,len(files))
