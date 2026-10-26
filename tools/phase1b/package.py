"""Portable actual production game + current authored character sources, no legacy demo entry."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,hashlib,posixpath,re
R=Path(__file__).resolve().parents[2];D=R/'docs/phase1b';B=Path('/tmp/phase1b-review');files={};TAG='checkpoint/phase1b-roster-review-20261026';RAW='https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/refs/tags/'+TAG+'/'
m=json.loads((R/'public/assets/gate3/palace-cleanup-world/manifest.json').read_text());names={'assets/gate3/palace-cleanup-world/manifest.json',m['overview'],m['farmMetadata'],m['contactCollision']['physical'],'assets/juni/juni.png','assets/juni/juni.json'}|{c[k]for c in m['chunks']for k in ['image','mask']}|{o['image']for o in m['objects']}
for id in ['haneul','bomi','minjun']:
 for n in ['atlas.png','atlas.json','preview-native.png']:names.add(f'assets/characters/{id}/{n}')
for n in names:files[n]=(R/'public'/n).read_bytes()
files['index.html']=(B/'index.html').read_bytes();build=json.loads((B/'.vite/manifest.json').read_text())
for row in build.values():
 for n in [row['file']]+row.get('css',[])+row.get('assets',[]):files[n]=(B/n).read_bytes()
files['BUILD_MANIFEST.json']=json.dumps(build,indent=2).encode()
for p in (R/'assets-src/characters/phase1b').rglob('*'):
 if p.is_file():files[str(p.relative_to(R))]=p.read_bytes()
for id in ['haneul','bomi','minjun']:files[f'assets-src/characters/phase1/{id}/raw/frame_0000.png']=(R/f'assets-src/characters/phase1/{id}/raw/frame_0000.png').read_bytes()
files['assets-src/characters/phase1/juni-style-reference.png']=(R/'assets-src/characters/phase1/juni-style-reference.png').read_bytes()
for p in D.rglob('*'):
 if not p.is_file()or'initial-attempt'in p.parts or any(x.startswith('forge-qa')for x in p.parts)or'bridges'in p.parts or p.name in ['package-proof.json','published-verification.json','package-final-validation.json']:continue
 if p.suffix in ['.md','.html','.jpg','.json']or p.name.endswith(('-native-crop.png','-sheet-native.png'))or p.name in ['lineup-native-1x.png','lineup-review-4x.png','four-native-gameplay-crops.png','four-gameplay-crops-2x.png','actual-phaser-body-lineup-native.png','walk-four-directions-native-preview.png','walk-four-directions-review-2x-preview.png','run-four-directions-native-preview.png','run-four-directions-review-2x-preview.png']or p.name in ['four-character-gameplay-native-crop-review.mp4','progress-switch-refresh-review.mp4']:files[str(p.relative_to(R))]=p.read_bytes()
for n in ['AGENTS.md','LICENSE','LICENSES.md','docs/current/PROJECT_STATE.md','docs/current/PHASE1B_DIRECTIVE.md','docs/phase1/protected-world.json','docs/phase1/protected-juni.json']:files[n]=(R/n).read_bytes()
for p in (R/'tools/phase1b').glob('*'):
 if p.suffix in ['.py','.mjs']:files[str(p.relative_to(R))]=p.read_bytes()
for package in ['phaser','zod']:
 p=R/'node_modules'/package/'LICENSE'
 if not p.exists():p=R/'node_modules'/package/'LICENSE.txt'
 if p.exists():files[f'LICENSES/{package}.txt']=p.read_bytes()
with ZipFile(R/'docs/gate3-palace-cleanup/PALACE_CLEANUP_REVIEW.zip')as z:files['start_review.py']=z.read('start_review.py')
files['README.md']=b'# Phase1B four-character playable review candidate\n\nRun `python3 start_review.py` and open localhost. Actual production index loads the frozen canonical world, four genuine atlases and original controls. Settings -> Chon nhan vat. WASD/arrows, Shift run, Space wave, C celebrate; mobile landscape joystick. Same-page refresh retains character, position and existing visited markers when browser storage is available. Explicit review-entry navigation keeps its spawn. Open REVIEW.html for QA, native source/crop evidence and actual videos. Large native world readbacks and full recordings use immutable evidence links. All runtime dependencies and character source packs are included offline.\n\nHuman character-art approval PENDING. Auto near/far classification WARNs retained. Physical Android/iPhone and hardware performance NOT TESTED. Canonical world has no interior transition. No Phase2, main merge or public deployment.\n'
files['REVIEW.html']=b'<!doctype html><html lang="vi"><meta charset="utf-8"><title>Phase1B review</title><h1>Four-character playable review candidate</h1><p><a href="index.html">Play actual Phaser game</a> | <a href="docs/phase1b/VISUAL_REVIEW.html">Visual evidence</a> | <a href="docs/phase1b/QA.md">QA</a> | <a href="docs/phase1b/DEVICE_REVIEW.md">Device review</a></p><p>Human artistic approval pending; Phase2 locked.</p></html>'
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
files['PACKAGE_SHA256.json']=(json.dumps({n:hashlib.sha256(b).hexdigest()for n,b in sorted(files.items())},indent=2)+'\n').encode();out=D/'PHASE1B_FOUR_CHARACTER_REVIEW.zip'
with ZipFile(out,'w',ZIP_DEFLATED,compresslevel=9)as z:
 for n,b in sorted(files.items()):z.writestr(n,b)
with ZipFile(out)as z:
 assert z.testzip()is None
 for n,h in json.loads(z.read('PACKAGE_SHA256.json')).items():assert hashlib.sha256(z.read(n)).hexdigest()==h,n
assert out.stat().st_size<100000000,out.stat().st_size
(D/'package-proof.json').write_text(json.dumps({'file':out.name,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'files':len(files),'runtimeFiles':len(names),'CRC':'PASS','allFileHashes':'PASS','playableCharacters':['juni','haneul','bomi','minjun'],'entry':'index.html -> actual canonical palace-cleanup-world, not historical V10 or a mockup','source':'All3new112-frame native sources, raw directionals, masks, joints, clips and provenance included','physicalDevices':'NOT TESTED','humanArtApproval':'PENDING'},indent=2)+'\n');print(out.name,out.stat().st_size,len(files))
