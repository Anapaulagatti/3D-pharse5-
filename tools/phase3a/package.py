"""Dependency-complete local Phaser review; original assets are read-only."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import json, hashlib, posixpath, re
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a';O=Path('/tmp/phase3a-review');TAG='checkpoint/phase3a-living-npc-world-review-20261027';RAW=f'https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/refs/tags/{TAG}/';files={}
def sha(b):return hashlib.sha256(b).hexdigest()
m=json.loads((R/'public/assets/gate3/palace-cleanup-world/manifest.json').read_text());names={'assets/gate3/palace-cleanup-world/manifest.json',m['overview'],m['farmMetadata'],m['contactCollision']['physical'],'assets/juni/juni.png','assets/juni/juni.json','assets/character-studio/juni-preview.png'}|{c[k]for c in m['chunks']for k in ['image','mask']}|{o['image']for o in m['objects']}
B=json.loads((R/'assets-src/characters/phase2c/base-bindings.json').read_text())
for id in B:
 if id!='juni':
  for n in ['atlas.png','atlas.json','preview-native.png']:names.add(f'assets/characters/{id}/{n}')
for stem in ['assets/cosmetics/phase2c','assets/npcs/phase3a']:
 for p in (R/'public'/stem).rglob('*'):
  if p.is_file():names.add(str(p.relative_to(R/'public')))
for n in names:files[n]=(R/'public'/n).read_bytes()
files['index.html']=(O/'index.html').read_bytes();build=json.loads((O/'.vite/manifest.json').read_text())
for row in build.values():
 for n in [row['file']]+row.get('css',[])+row.get('assets',[]):files[n]=(O/n).read_bytes()
files['BUILD_MANIFEST.json']=json.dumps(build,indent=2).encode()
for p in D.rglob('*'):
 if not p.is_file():continue
 n=p.name
 if p.suffix in ['.webm','.zip']or'working'in n or n in ['package-proof.json','package-smoke.json','published-verification.json','approved-main.ts.txt']:continue
 if p.suffix=='.mp4'and(p.parent.name!='gameplay'):continue
 if n=='npc-placement-map-review.png'or(p.parent.name=='gameplay'and p.suffix=='.jpg'):continue
 if p.suffix=='.png'and(n.endswith('-phaser-native.png')or p.parent.name=='pilot' or(p.parent.name=='gameplay'and not n.endswith('-body-native.png'))or n.endswith('-software-webgl-native.png')):continue
 if p.suffix in ['.md','.html','.jpg','.png','.mp4','.json','.log']and(p.suffix!='.json'or p.stat().st_size<1500000):files[str(p.relative_to(R))]=p.read_bytes()
for n in ['AGENTS.md','LICENSE','LICENSES.md','docs/current/PROJECT_STATE.md','assets-src/npcs/phase3a/registry.json','assets-src/npcs/phase3a/dialogues.json']:files[n]=(R/n).read_bytes()
files['start_review.py']=(R/'tools/phase3a/start_review.py').read_bytes()
for name in ['phaser','zod']:
 p=R/'node_modules'/name/'LICENSE'
 if not p.exists():p=R/'node_modules'/name/'LICENSE.txt'
 if p.exists():files[f'LICENSES/{name}.txt']=p.read_bytes()
files['README.md']=b'# Korean Arena Phase3A Living NPC World\n\nRun python3 start_review.py and open http://127.0.0.1:4378/REVIEW.html. Actual local compiled Phaser with canonical frozen world,12original players,28cosmetics and14newresidents. No Node,install or network required to play. --lan explicitly opts into your own LAN only.\n\nAll14resident gameplay videos,native crops and review sheets included. Large full traversal/stability videos and native scene PNGs resolve online at the immutable review tag. Native PNGs are pixel authority.\n\nHuman artistic/linguistic approval PENDING. Physical devices and hardwareGPU NOT TESTED. Phase3B locked. No main merge/public deployment.\n'
files['REVIEW.html']=b'<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Phase3A NPC World</title><h1>Korean Arena Phase3A</h1><p><a href="index.html">Play actual Phaser</a> | <a href="docs/phase3a/REVIEW.html">Native gallery and gameplay videos</a> | <a href="docs/phase3a/QA.md">QA</a> | <a href="docs/phase3a/DEVICE_REVIEW.html">Device checklist/export</a></p><p>Human artistic approval pending. Physical devices NOT TESTED. Phase3B locked.</p>'
for n,data in list(files.items()):
 if not n.endswith(('.md','.html')):continue
 def fix(match):
  t=match.group(1)
  if t.startswith(('http:','https:','#','data:','mailto:')):return match.group(0)
  clean=t.split('?')[0].split('#')[0];path=posixpath.normpath(posixpath.join(posixpath.dirname(n),clean)).lstrip('/')
  if path in files:return match.group(0)
  return match.group(0).replace(t,RAW+path)
 text=data.decode();text=re.sub(r'(?:href|src)="([^"]+)"',fix,text);text=re.sub(r'\]\(([^)]+)\)',fix,text);files[n]=text.encode()
files['PACKAGE_SHA256.json']=(json.dumps({n:sha(b)for n,b in sorted(files.items())},indent=2)+'\n').encode();out=D/'PHASE3A_LIVING_NPC_WORLD_REVIEW.zip'
with ZipFile(out,'w',ZIP_DEFLATED,compresslevel=6)as z:
 for n,b in sorted(files.items()):z.writestr(n,b)
with ZipFile(out)as z:
 assert z.testzip()is None
 for n,h in json.loads(z.read('PACKAGE_SHA256.json')).items():assert sha(z.read(n))==h,n
 for id,h in B.items():
  n='assets/juni/juni.png'if id=='juni'else f'assets/characters/{id}/atlas.png';assert sha(z.read(n))==h,id
 for p in(R/'public/assets/npcs/phase3a').rglob('*'):
  if p.is_file():assert z.read(str(p.relative_to(R/'public')))==p.read_bytes()
assert out.stat().st_size<100000000,out.stat().st_size
report={'file':out.name,'bytes':out.stat().st_size,'sha256':sha(out.read_bytes()),'files':len(files),'runtimeFiles':len(names),'CRC':'PASS','allFileHashes':'PASS','all12ApprovedAtlasesExact':'PASS','all14NPCAssetsExact':'PASS','relativePortableBuild':True,'runtime':{n:sha(b)for n,b in files.items()if n.startswith('assets/')or n in ['index.html','BUILD_MANIFEST.json']},'includedVideos':sorted(n for n in files if n.endswith('.mp4')),'sourceCheckpoint':TAG,'physicalDevices':'NOT TESTED','humanArtApproval':'PENDING'};(D/'package-proof.json').write_text(json.dumps(report,indent=2)+'\n');print(out.name,out.stat().st_size,'bytes',len(files),'files')
