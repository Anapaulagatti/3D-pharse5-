"""One portable canonical runtime ZIP; full-resolution authoring art stays versioned in the review branch."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,hashlib,re,posixpath
from inventory import R,runtime_names
D=R/'docs/phase3a-npc-expansion';O=Path('/tmp/phase3a-exp-review');TAG='checkpoint/phase3a-npc-expansion-20-source-blocked-review-20261028';RAW=f'https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/refs/tags/{TAG}/';files={}
def sha(b):return hashlib.sha256(b).hexdigest()
names=runtime_names()
for n in names:files[n]=(R/'public'/n).read_bytes()
for n in ['index.html','tools/phase3a-npc-expansion/clip-inspector.html']:files[n]=(O/n).read_bytes()
build=json.loads((O/'.vite/manifest.json').read_text())
for row in build.values():
 for n in[row['file']]+row.get('css',[])+row.get('assets',[]):files[n]=(O/n).read_bytes()
files['BUILD_MANIFEST.json']=json.dumps(build,indent=2).encode()
for p in D.rglob('*'):
 if not p.is_file()or'__pycache__'in p.parts:continue
 n=p.name;rel=p.relative_to(D)
 if p.suffix in ['.zip','.webm']or'working'in n or n in ['package-proof.json','package-smoke.json','published-verification.json']:continue
 if rel.parts[0]=='logs'and not(n.startswith('final-')or n=='e2e-results.json'):continue
 if rel.parts[0]=='gameplay':
  if not n.endswith('-juni-context-native.png'):continue
 if rel.parts[0]=='native'and not('greet-'in n and'-0-actual-body-native'in n):continue
 if rel.parts[0]=='before-source':continue
 if n.endswith('-software-webgl-native.png')or(n.startswith('package-')and n.endswith('-phaser-native.png')):continue
 if p.suffix=='.mp4'and rel.parts[0]!='review-clips':continue
 if p.suffix=='.png'and'tooling'in rel.parts:continue
 files[str(p.relative_to(R))]=p.read_bytes()
S=R/'assets-src/npcs/phase3a-npc-expansion'
for p in S.rglob('*'):
 if not p.is_file()or'__pycache__'in p.parts:continue
 # Complete native/layer/rig/pose provenance is small; raw illustrated masters/turnarounds and redundant frames are online in the same immutable ref.
 if p.suffix=='.png'and not any(k in p.parts for k in ['native','layers']):continue
 if'frames'in p.parts or'master-prepared'in p.parts:continue
 files[str(p.relative_to(R))]=p.read_bytes()
for p in(R/'tools/phase3a-npc-expansion').glob('*'):
 if p.is_file()and p.suffix in['.py','.mjs','.html']:
  n=str(p.relative_to(R))
  if n not in files:files[n]=p.read_bytes()
for n in ['tools/phase1b/animate.py','assets-src/characters/phase1b-frontback-juni/juni-motion-template.json','assets-src/characters/phase1/juni-style-reference.png']:
 files[n]=(R/n).read_bytes()
files['start_review.py']=(R/'tools/phase3a-npc-expansion/start_review.py').read_bytes()
for name in ['phaser','zod']:
 p=R/'node_modules'/name/'LICENSE'
 if not p.exists():p=R/'node_modules'/name/'LICENSE.txt'
 if p.exists():files[f'LICENSES/{name}.txt']=p.read_bytes()
files['README.md']=('''# Korean Arena · actual20NPC / requested26 · source-blocked review

Run python3 start_review.py and open the printed local REVIEW.html. No Node/install/network needed to PLAY. Default bind is127.0.0.1;--lan is an explicit private-LAN test option,not a deployment.

Complete frozen canonical world,12approved players,28cosmetics/46variants,14residents with illustrated art and6original cultural visitors. Three approved pilots remain unchanged. Six historical encounters and source-verified real-person index are NOT completed because official sources return proxy403;no placeholder history sprites or unverified biographies are shipped. Final human art approval pending. Physical Android/iPhone/hardwareGPU NOT TESTED. Phase3B LOCKED,no main merge or public deployment.

The source-code checkpoint,full hashes/logs/native evidence and limitations are in docs/phase3a-npc-expansion. This ZIP includes native sources/layers/rigs,actual1:1context crops,17short direct gameplay excerpts and a live native5column Phaser inspector. Full-resolution illustration sources,complete raw-size world PNGs and full videos are versioned in the immutable review ref and linked online;those optional authoring/evidence links are not required to play. The inspector is supplemental atlas playback,not navigation proof. Re-authoring requires the full repository and documented optional tooling/dependencies.
''').encode()
files['REVIEW.html']=b'<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Korean Arena20/26NPC</title><h1>20actualNPC /26requested</h1><p>6historical encounters/indexsourceBLOCKED;human art review pending;physicaldevicesNOTTESTED;Phase3BLOCKED.</p><p><a href="index.html">Enter World / Character Studio</a> | <a href="docs/phase3a-npc-expansion/REVIEW.html">Native evidence and actual gameplay</a> | <a href="tools/phase3a-npc-expansion/clip-inspector.html">Live native Phaser comparison</a> | <a href="docs/phase3a-npc-expansion/QA.md">QA</a></p>'
for n,data in list(files.items()):
 if not n.endswith(('.md','.html')):continue
 def fix(match):
  t=match.group(1)
  if t.startswith(('http:','https:','#','data:','mailto:')):return match.group(0)
  clean=t.split('?')[0].split('#')[0];path=posixpath.normpath(posixpath.join(posixpath.dirname(n),clean)).lstrip('/')
  if path in files:return match.group(0)
  if clean.startswith('/')or clean.startswith('<'):return match.group(0)
  return match.group(0).replace(t,RAW+path)
 text=data.decode();text=re.sub(r'(?:href|src)="([^"]+)"',fix,text);text=re.sub(r'\]\(([^)]+)\)',fix,text);files[n]=text.encode()
files['PACKAGE_SHA256.json']=(json.dumps({n:sha(b)for n,b in sorted(files.items())},indent=2)+'\n').encode();out=D/'PHASE3A_20NPC_SOURCE_BLOCKED_REVIEW.zip'
with ZipFile(out,'w',ZIP_DEFLATED,compresslevel=6)as z:
 for n,b in sorted(files.items()):z.writestr(n,b)
with ZipFile(out)as z:
 assert z.testzip()is None
 for n,h in json.loads(z.read('PACKAGE_SHA256.json')).items():assert sha(z.read(n))==h,n
 for id,h in json.loads((R/'assets-src/characters/phase2c/base-bindings.json').read_text()).items():
  n='assets/juni/juni.png'if id=='juni'else f'assets/characters/{id}/atlas.png';assert sha(z.read(n))==h,id
 for p in(R/'public/assets/npcs/phase3a').rglob('*'):
  if p.is_file():assert z.read(str(p.relative_to(R/'public')))==p.read_bytes()
report={'file':out.name,'bytes':out.stat().st_size,'sha256':sha(out.read_bytes()),'files':len(files),'runtimeAssetFiles':len(names),'actualNPCs':20,'requestedNPCs':26,'historicalNPCs':0,'verifiedIconCards':0,'CRC':'PASS','allFileHashes':'PASS','all12PlayerAtlases':'EXACT','all20NPCBytes':'EXACT','nativeNoResampling':True,'scope':'Complete canonical runtime;curated native/layer/rig/evidence,not full-resolution authoring-source archive','runtime':{n:sha(b)for n,b in files.items()if n.startswith('assets/')or n in['index.html','BUILD_MANIFEST.json','tools/phase3a-npc-expansion/clip-inspector.html']},'includedVideos':sorted(n for n in files if n.endswith('.mp4')),'physicalDevices':'NOT TESTED','humanArtApproval':'PENDING','reference':TAG};(D/'package-proof.json').write_text(json.dumps(report,indent=2)+'\n');print(out.name,out.stat().st_size,'bytes',len(files),'files')
