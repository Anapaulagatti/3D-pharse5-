from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,hashlib,posixpath,re
R=Path(__file__).resolve().parents[2];D=R/'docs/phase2b-motion';B=Path('/tmp/phase2b-motion-review');TAG='checkpoint/phase2b-motion-corrected-review-20261027';RAW=f'https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/refs/tags/{TAG}/';files={}
m=json.loads((R/'public/assets/gate3/palace-cleanup-world/manifest.json').read_text());names={'assets/gate3/palace-cleanup-world/manifest.json',m['overview'],m['farmMetadata'],m['contactCollision']['physical'],'assets/juni/juni.png','assets/juni/juni.json','assets/character-studio/juni-preview.png'}|{c[k]for c in m['chunks']for k in ['image','mask']}|{o['image']for o in m['objects']}
for id in ['haneul','bomi','minjun','ara','doyun','sori','jiwon','nari','taeyang','yuna','hyunwoo']:
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
 if not p.is_file():continue
 name=p.name
 include=p.suffix in ['.md','.html','.jpg','.gif']
 if p.suffix=='.mp4':include=True
 if p.suffix=='.png':include=any(k in name for k in ['before-after-native','foot-guide-native','actual-contact-native','-actual-native','candidate-native'])or name=='sori-world-gameplay-native-crop.png'
 if p.suffix=='.json':include=p.stat().st_size<1200000 and not any(k in name for k in ['working','package-proof','published','failure'])
 if include:
  content=Path('/tmp/phase2b-motion-compact-videos')/name if name.endswith('-actual-gameplay.mp4') else p
  files[str(p.relative_to(R))]=content.read_bytes()
for p in list((D/'recovery-logs').glob('*.log'))+list((D/'recovery-e2e').glob('*.json')):
 if p.is_file():files[str(p.relative_to(R))]=p.read_bytes()
for n in ['docs/phase2b/FORGE_WARNINGS.md','docs/phase2b/forge-warnings.json','docs/phase2b/DEVICE_REVIEW.md']:
 files[n]=(R/n).read_bytes()
for n in ['AGENTS.md','LICENSE','LICENSES.md','docs/current/PROJECT_STATE.md','docs/phase2b/approved-six.json','docs/phase2b/approved-identity-records.json','assets-src/characters/phase2a/cosmetics/catalog.json']:files[n]=(R/n).read_bytes()
files['start_review.py']=(R/'tools/phase2b/start_review.py').read_bytes()
for name in ['phaser','zod']:
 p=R/'node_modules'/name/'LICENSE'
 if not p.exists():p=R/'node_modules'/name/'LICENSE.txt'
 if p.exists():files[f'LICENSES/{name}.txt']=p.read_bytes()
files['README.md']=b"# Phase2B motion correction review\n\nRun python3 start_review.py and open REVIEW.html. Actual compiled Phaser world,12 playable characters,10 approved cosmetics. Six corrected motion packs only: front/back/right walk/run and related starts/stops. Approved six, left clips, UI, world, collision, camera, persistence unchanged.\n\nReview contains6 Juni comparison videos, native before/after sheets, source-only animated previews, actual contact annotations and all6 full unretimed gameplay videos. Packaged gameplay videos are lighter compression derivatives with identical dimensions,frame counts,timing. Original MP4 recordings and exhaustive native captures remain linked to the recoverable review checkpoint. Comparison videos use actual game-frame captures phase-aligned at normal gait timing; they are separate from the raw gameplay recordings.\n\nTechnical checks do not grant artistic acceptance. Human motion review pending. Physical devices NOT TESTED. Phase2C LOCKED. No merge or public deployment.\n"
files['REVIEW.html']=b'<!doctype html><meta charset="utf-8"><title>Motion correction review</title><h1>Korean Arena Phase2B motion correction</h1><p><a href="index.html">Play actual Phaser world</a> | <a href="docs/phase2b-motion/REVIEW.html">Six synchronized comparisons + native evidence</a> | <a href="docs/phase2b-motion/QA.md">QA</a></p><p>Human motion approval pending. Phase2C LOCKED. Real devices NOT TESTED.</p>'
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
files['PACKAGE_SHA256.json']=(json.dumps({n:hashlib.sha256(b).hexdigest()for n,b in sorted(files.items())},indent=2)+'\n').encode();out=D/'PHASE2B_MOTION_CORRECTION_REVIEW.zip'
with ZipFile(out,'w',ZIP_DEFLATED,compresslevel=6)as z:
 for n,b in sorted(files.items()):z.writestr(n,b)
with ZipFile(out)as z:
 assert z.testzip()is None
 for n,h in json.loads(z.read('PACKAGE_SHA256.json')).items():assert hashlib.sha256(z.read(n)).hexdigest()==h,n
 for id in ['juni','haneul','bomi','minjun','ara','doyun','sori','jiwon','nari','taeyang','yuna','hyunwoo']:
  n='assets/juni/juni.png'if id=='juni'else f'assets/characters/{id}/atlas.png';assert z.read(n)==(R/'public'/n).read_bytes()
assert out.stat().st_size<100000000,out.stat().st_size
(D/'package-proof.json').write_text(json.dumps({'file':out.name,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'files':len(files),'runtimeFiles':len(names),'CRC':'PASS','allFileHashes':'PASS','allTwelveCurrentAtlasesExact':'PASS','sourceCheckpoint':TAG,'entry':'Actual compiled index.html -> frozen canonical palace-cleanup-world; Character Studio extends existing manager/controller','humanPhase2BApproval':'PENDING','physicalDevices':'NOT TESTED'},indent=2)+'\n');print(out.name,out.stat().st_size,'bytes',len(files),'files')
