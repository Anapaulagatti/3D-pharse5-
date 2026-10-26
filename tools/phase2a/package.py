from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,hashlib,posixpath,re
R=Path(__file__).resolve().parents[2];D=R/'docs/phase2a';B=Path('/tmp/phase2a-review');TAG='checkpoint/phase2a-character-studio-review-20261026';RAW=f'https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/refs/tags/{TAG}/';files={}
m=json.loads((R/'public/assets/gate3/palace-cleanup-world/manifest.json').read_text());names={'assets/gate3/palace-cleanup-world/manifest.json',m['overview'],m['farmMetadata'],m['contactCollision']['physical'],'assets/juni/juni.png','assets/juni/juni.json','assets/character-studio/juni-preview.png'}|{c[k]for c in m['chunks']for k in ['image','mask']}|{o['image']for o in m['objects']}
for id in ['haneul','bomi','minjun','ara','doyun']:
 for n in ['atlas.png','atlas.json','preview-native.png']:names.add(f'assets/characters/{id}/{n}')
for p in (R/'public/assets/cosmetics').rglob('*'):
 if p.is_file():names.add(str(p.relative_to(R/'public')))
for n in names:files[n]=(R/'public'/n).read_bytes()
files['index.html']=(B/'index.html').read_bytes();build=json.loads((B/'.vite/manifest.json').read_text())
for row in build.values():
 for n in [row['file']]+row.get('css',[])+row.get('assets',[]):files[n]=(B/n).read_bytes()
files['BUILD_MANIFEST.json']=json.dumps(build,indent=2).encode()
# Compact native originals/crops and real videos; large full readbacks and all
# original master/layer/frame sources stay recoverable at the immutable checkpoint.
for p in D.iterdir():
 if p.suffix=='.mp4' and p.name not in ['ara-default-actual-gameplay.mp4','doyun-default-actual-gameplay.mp4']:continue
 if not p.is_file()or p.name in ['package-proof.json','published-verification.json','actual-gameplay-working.json']or p.suffix in ['.zip','.webm','.log']:continue
 if p.suffix in ['.md','.html','.jpg','.mp4']or(p.suffix=='.json'and p.stat().st_size<500000)or(p.suffix=='.png'and p.stat().st_size<900000)or p.name in ['native-pixel-qa.json','original4-native-pixel-qa.json','source-provenance.json','validation.json','composition-qa.json','persistence-evidence.json','memory-stability.json']:files[str(p.relative_to(R))]=p.read_bytes()
for n in ['AGENTS.md','LICENSE','LICENSES.md','docs/current/PROJECT_STATE.md','docs/phase2a/approved-four-characters.json','docs/phase2a/approved-identity-records.json','assets-src/characters/phase2a/cosmetics/catalog.json']:files[n]=(R/n).read_bytes()
files['start_review.py']=(R/'tools/phase2a/start_review.py').read_bytes()
for name in ['phaser','zod']:
 p=R/'node_modules'/name/'LICENSE'
 if not p.exists():p=R/'node_modules'/name/'LICENSE.txt'
 if p.exists():files[f'LICENSES/{name}.txt']=p.read_bytes()
files['README.md']=b'# Korean Arena Phase2A Character Studio\n\nRun python3 start_review.py and open REVIEW.html. This is the actual compiled Phaser game with the frozen canonical world, six playable characters and native-frame cosmetics. The game runs locally/offline; full authoring sources and large native evidence are linked to the immutable source checkpoint.\n\nFour original identities are human-approved and unchanged. Ara/Doyun and cosmetics are review candidates with native/technical validation, awaiting human Phase2A approval. Physical Android/iPhone and hardware performance NOT TESTED. No Phase2B, main merge or public deployment.\n'
files['REVIEW.html']=b'<!doctype html><meta charset="utf-8"><title>Phase2A review</title><h1>Korean Arena Character Studio</h1><p><a href="index.html">Play actual six-character Phaser world</a> | <a href="docs/phase2a/REVIEW.html">Visual review and gameplay evidence</a> | <a href="docs/phase2a/QA.md">QA</a> | <a href="docs/phase2a/DEVICE_REVIEW.md">Device handoff</a></p><p>Human Phase2A approval pending. Phase2B locked.</p>'
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
files['PACKAGE_SHA256.json']=(json.dumps({n:hashlib.sha256(b).hexdigest()for n,b in sorted(files.items())},indent=2)+'\n').encode();out=D/'PHASE2A_CHARACTER_STUDIO_REVIEW.zip'
with ZipFile(out,'w',ZIP_DEFLATED,compresslevel=6)as z:
 for n,b in sorted(files.items()):z.writestr(n,b)
with ZipFile(out)as z:
 assert z.testzip()is None
 for n,h in json.loads(z.read('PACKAGE_SHA256.json')).items():assert hashlib.sha256(z.read(n)).hexdigest()==h,n
 for id in ['juni','haneul','bomi','minjun','ara','doyun']:
  n='assets/juni/juni.png'if id=='juni'else f'assets/characters/{id}/atlas.png';assert z.read(n)==(R/'public'/n).read_bytes()
assert out.stat().st_size<100000000,out.stat().st_size
(D/'package-proof.json').write_text(json.dumps({'file':out.name,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'files':len(files),'runtimeFiles':len(names),'CRC':'PASS','allFileHashes':'PASS','allSixCurrentAtlasesExact':'PASS','sourceCheckpoint':TAG,'entry':'Actual compiled index.html -> frozen canonical palace-cleanup-world; Character Studio extends existing manager/controller','humanPhase2AApproval':'PENDING','physicalDevices':'NOT TESTED'},indent=2)+'\n');print(out.name,out.stat().st_size,'bytes',len(files),'files')
