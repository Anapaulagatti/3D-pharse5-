from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,hashlib,importlib.util,posixpath,re,sys
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a-identity-safeguard';O=Path('/tmp/phase3a-identity-review');TAG='checkpoint/phase3a-fictional-identity-safeguard-20261029';RAW=f'https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/refs/tags/{TAG}/'
s=importlib.util.spec_from_file_location('inventory',R/'tools/phase3a-npc-expansion/inventory.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def sha(b):return hashlib.sha256(b).hexdigest()
files={n:(R/'public'/n).read_bytes() for n in m.runtime_names()};files['index.html']=(O/'index.html').read_bytes();build=json.loads((O/'.vite/manifest.json').read_text());files['BUILD_MANIFEST.json']=json.dumps(build,indent=2).encode()
for row in build.values():
 for n in [row['file']]+row.get('css',[])+row.get('assets',[]):files[n]=(O/n).read_bytes()
for p in D.rglob('*'):
 if not p.is_file() or p.suffix in ['.zip','.webm'] or '__pycache__' in p.parts:continue
 if p.name in ['PACKAGE_PROOF.json','package-smoke.json','published-verification.json','BASELINE.json']:continue
 if p.suffix=='.log' or p.parent.name.startswith(('full-e2e','focused')):continue
 if p.parent.name=='native' and p.name.endswith('-phaser-native.png'):continue
 files[str(p.relative_to(R))]=p.read_bytes()
for n in ['docs/phase3a/HISTORICAL_NPC_RIGHTS_AND_ALIASES.md','LICENSE','LICENSES.md','assets-src/npcs/phase3a-finalization/identity-presentations.json','assets-src/npcs/phase3a-finalization/release-status.json']:
 files[n]=(R/n).read_bytes()
for p in (R/'public/licenses').glob('*'):
 if p.is_file():files['LICENSES/'+p.name]=p.read_bytes()
files['start_review.py']=b'''from pathlib import Path
from argparse import ArgumentParser
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
import os
p=ArgumentParser();p.add_argument('--port',type=int,default=4460);p.add_argument('--lan',action='store_true');a=p.parse_args();os.chdir(Path(__file__).resolve().parent)
print(f'Open http://127.0.0.1:{a.port}/REVIEW.html',flush=True)
ThreadingHTTPServer(('0.0.0.0' if a.lan else '127.0.0.1',a.port),SimpleHTTPRequestHandler).serve_forever()
'''
files['REVIEW.html']=b'<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>26 NPC development review</title><h1>26 NPCs: six fictional archive identities</h1><p>Approved art unchanged. Commercial rights unverified; physical devices not tested.</p><p><a href="index.html">Enter World</a> | <a href="docs/phase3a-identity-safeguard/REVIEW.html">Current names, native gallery and actual video</a></p>'
files['README.md']=b'''# Fictional identity safeguard review
Extract and run python3 start_review.py; open the printed local REVIEW.html.
No Node installation or network is needed for gameplay. --lan is optional private-LAN review.
The ordinary development world has 26 unique NPCs. Six archive inhabitants are fictional, not actual historical people. Approved artwork, animation, IDs, navigation, world, players and cosmetics are unchanged. Choose a character in the original Character Studio if using fresh storage.
Use the contextual cultural archive near palace, bookshop or coast. QA-entry links only position the player at existing review approaches; they do not unlock the roster.
Native crops and actual gameplay video are local. Optional full native originals are linked to the immutable online checkpoint. Rights and provenance documents are internal review material, not the fictional characters' biographies.
Commercial depiction rights remain unverified. Renaming is not legal clearance. Historical factual biographies stay disabled. Physical Android/iPhone/hardware GPU remain NOT TESTED. Phase 3B has not started. No main merge or public deployment.
'''
for name,data in list(files.items()):
 if not name.endswith(('.md','.html')):continue
 def fix(match):
  t=match.group(1)
  if t.startswith(('http:','https:','#','data:','mailto:')):return match.group(0)
  target=posixpath.normpath(posixpath.join(posixpath.dirname(name),t.split('?')[0].split('#')[0])).lstrip('/')
  return match.group(0) if target in files else match.group(0).replace(t,RAW+target)
 text=re.sub(r'(?:href|src)="([^"]+)"',fix,data.decode());files[name]=re.sub(r'\]\(([^)]+)\)',fix,text).encode()
files['PACKAGE_SHA256.json']=(json.dumps({n:sha(b) for n,b in sorted(files.items())},indent=2)+'\n').encode()
for n,b in files.items():p=O/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
if '--stage-only' in sys.argv:print('STAGED',len(files),'files');raise SystemExit(0)
out=D/'PHASE3A_FICTIONAL_IDENTITIES_REVIEW.zip'
with ZipFile(out,'w',ZIP_DEFLATED,compresslevel=6) as z:
 for n,b in sorted(files.items()):z.writestr(n,b)
with ZipFile(out) as z:
 assert z.testzip() is None
 for n,h in json.loads(z.read('PACKAGE_SHA256.json')).items():assert sha(z.read(n))==h,n
 for p in (R/'public/assets/npcs/phase3a').rglob('*'):
  if p.is_file():assert z.read(str(p.relative_to(R/'public')))==p.read_bytes()
assert out.stat().st_size<100*1024*1024
proof={'file':out.name,'bytes':out.stat().st_size,'sha256':sha(out.read_bytes()),'CRC':'PASS','internalSHA256':'PASS','registeredNPCs':26,'fictionalArchiveIdentities':6,'artChanges':0,'commercialRights':'UNVERIFIED_NOT_CERTIFIED','physicalDevices':'NOT_TESTED','runtime':{n:sha(b) for n,b in files.items() if n.startswith('assets/') or n=='index.html'},'launch':'NOT YET TESTED: see later independent extraction smoke','checkpoint':TAG};(D/'PACKAGE_PROOF.json').write_text(json.dumps(proof,indent=2)+'\n');print(out.name,proof['bytes'],proof['sha256'])
