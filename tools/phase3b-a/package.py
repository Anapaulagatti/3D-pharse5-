from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,hashlib,importlib.util,re,posixpath,sys
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3b-a';O=Path('/tmp/phase3ba-private-review');TAG='checkpoint/phase3b-a-daily-life-private-review-20261029';RAW=f'https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/refs/tags/{TAG}/'
spec=importlib.util.spec_from_file_location('inventory',R/'tools/phase3a-npc-expansion/inventory.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def sha(b):return hashlib.sha256(b).hexdigest()
files={n:(R/'public'/n).read_bytes()for n in m.runtime_names()};files['index.html']=(O/'index.html').read_bytes();manifest=json.loads((O/'.vite/manifest.json').read_text());files['BUILD_MANIFEST.json']=json.dumps(manifest,indent=2).encode()
assert b'private-review' in files['index.html']
for row in manifest.values():
 for n in [row['file']]+row.get('css',[])+row.get('assets',[]):files[n]=(O/n).read_bytes()
for p in D.rglob('*'):
 if not p.is_file()or p.suffix in ['.zip','.webm','.log']or'__pycache__'in p.parts:continue
 if p.name in ['BASELINE.json','PACKAGE_PROOF.json','package-smoke.json','package-native-qa.json','published-verification.json','ACTUAL_PHASER_EVIDENCE.json']:continue
 if p.parent.name not in ['phase3b-a','native','media']:continue
 if p.parent.name=='native'and p.name.endswith('-phaser-native.png'):continue
 files[str(p.relative_to(R))]=p.read_bytes()
for n in ['LICENSE','LICENSES.md','assets-src/rights/npc-inventory.json','assets-src/npcs/daily-life/schedules.json','assets-src/npcs/daily-life/visitor-windows.json','assets-src/npcs/phase3a-finalization/identity-presentations.json','docs/phase3a/HISTORICAL_NPC_RIGHTS_AND_ALIASES.md']:
 files[n]=(R/n).read_bytes()
for p in(R/'public/licenses').glob('*'):
 if p.is_file():files['LICENSES/'+p.name]=p.read_bytes()
files['start_review.py']=b'''from pathlib import Path
from argparse import ArgumentParser
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
import os
p=ArgumentParser();p.add_argument('--port',type=int,default=4480);p.add_argument('--lan',action='store_true');a=p.parse_args();os.chdir(Path(__file__).resolve().parent)
print(f'PRIVATE REVIEW ONLY: http://127.0.0.1:{a.port}/REVIEW.html',flush=True)
print('Commercial rights blocked; physical devices NOT TESTED; no deployment authorized.',flush=True)
ThreadingHTTPServer(('0.0.0.0'if a.lan else'127.0.0.1',a.port),SimpleHTTPRequestHandler).serve_forever()
'''
files['REVIEW.html']=b'<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Phase3B-A private review</title><h1>PRIVATE REVIEW: NPC daily life</h1><p>26 NPCs; approved art unchanged. Commercial rights BLOCKED_PENDING_REVIEW; physical devices NOT TESTED.</p><p><a href="index.html">Enter World / original Character Studio</a> | <a href="docs/phase3b-a/REVIEW.html">Native scenes and actual videos</a> | <a href="docs/phase3b-a/README.md">Review guide</a></p>'
files['README.md']=b'''# Phase 3B-A PRIVATE REVIEW
Extract and run python3 start_review.py. Open the printed localhost REVIEW.html.
No Node/install/network is required for gameplay. --lan is explicit private-LAN review, not public deployment.
Fresh storage uses the unchanged 12-character Studio. Choose a character and Enter World. The world has 20 present-day schedule identities and six selected fictional era-story inhabitants (26 stable IDs). Caps remain 4 actors / 4 textures / 2 pending loads.
The normal day lasts 30 real minutes. Use a QA approach link and Settings clock controls for acceleration. A review link can inspect a visitor outside its normal window; this is not ordinary eligibility. Source artwork, avatars, cosmetics, map and collision remain unchanged.
Native crops, actual videos and rights/QA documents are local. Full native originals, verbose source evidence and historical provenance links are optional online checkpoint files.
All26commercial publications remain blocked pending creation/account terms and independent IP review. Fictional names or AI generation do not grant clearance. This is a technical review, not legal certification. Physical Android/iPhone/hardware GPU NOT TESTED; measured browser outliers remain documented.
No shops/farming gameplay/economy/learning rewards/ads/multiplayer or Phase3B-B/C/D. No main merge or public deployment.
'''
for name,data in list(files.items()):
 if not name.endswith(('.md','.html')):continue
 def fix(match):
  t=match.group(1)
  if t.startswith(('https:','http:','#','data:','mailto:')):return match.group(0)
  target=posixpath.normpath(posixpath.join(posixpath.dirname(name),t.split('?')[0].split('#')[0])).lstrip('/')
  return match.group(0)if target in files else match.group(0).replace(t,RAW+target)
 text=re.sub(r'(?:href|src)="([^"]+)"',fix,data.decode());files[name]=re.sub(r'\]\(([^)]+)\)',fix,text).encode()
files['PACKAGE_SHA256.json']=(json.dumps({n:sha(b)for n,b in sorted(files.items())},indent=2)+'\n').encode()
for n,b in files.items():p=O/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
if '--stage-only'in sys.argv:print('STAGED',len(files),'files');raise SystemExit(0)
out=D/'PHASE3BA_PRIVATE_REVIEW.zip'
with ZipFile(out,'w',ZIP_DEFLATED,compresslevel=6)as z:
 for n,b in sorted(files.items()):z.writestr(n,b)
with ZipFile(out)as z:
 assert z.testzip()is None
 for n,h in json.loads(z.read('PACKAGE_SHA256.json')).items():assert sha(z.read(n))==h,n
 for p in(R/'public/assets/npcs/phase3a').rglob('*'):
  if p.is_file():assert z.read(str(p.relative_to(R/'public')))==p.read_bytes()
assert out.stat().st_size<100*1024*1024,out.stat().st_size
proof={'file':out.name,'bytes':out.stat().st_size,'sha256':sha(out.read_bytes()),'CRC':'PASS','internalSHA256':'PASS','profile':'PRIVATE_REVIEW_ONLY','registeredNPCs':26,'presentDaySchedules':20,'archiveStorySchedules':6,'approvedNativeCells':2704,'artChanges':0,'commercialPublication':'BLOCKED_PENDING_REVIEW','publicGateProof':'RELEASE_GATE_PROOF.json','physicalDevices':'NOT_TESTED','runtime':{n:sha(b)for n,b in files.items()if n.startswith('assets/')or n=='index.html'},'launch':'Pending independent extraction, not inferred from CRC','checkpoint':TAG};(D/'PACKAGE_PROOF.json').write_text(json.dumps(proof,indent=2)+'\n');print(out.name,proof['bytes'],proof['sha256'])
