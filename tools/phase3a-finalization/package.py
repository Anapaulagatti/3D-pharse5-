from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,hashlib,importlib.util,posixpath,re,sys
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a-finalization';O=Path('/tmp/phase3a-finalization-review');TAG='checkpoint/phase3a-26-npc-development-approved-20261029';RAW=f'https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/refs/tags/{TAG}/'
s=importlib.util.spec_from_file_location('inventory',R/'tools/phase3a-npc-expansion/inventory.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def sha(b):return hashlib.sha256(b).hexdigest()
files={n:(R/'public'/n).read_bytes()for n in m.runtime_names()};files['index.html']=(O/'index.html').read_bytes();build=json.loads((O/'.vite/manifest.json').read_text());files['BUILD_MANIFEST.json']=json.dumps(build,indent=2).encode()
for row in build.values():
 for n in[row['file']]+row.get('css',[])+row.get('assets',[]):files[n]=(O/n).read_bytes()
for p in D.rglob('*'):
 if not p.is_file()or p.suffix in['.zip','.webm']or'__pycache__'in p.parts:continue
 if p.name in ['PACKAGE_PROOF.json','package-smoke.json','published-verification.json']:continue
 if p.parent.name=='native'and p.name.endswith('-phaser-native.png'):continue # Full originals remain online;literal native crops local.
 if 'focused'in p.parts or'full-e2e'in p.parts:continue
 files[str(p.relative_to(R))]=p.read_bytes()
for n in ['docs/phase3a/HISTORICAL_NPC_RIGHTS_AND_ALIASES.md','LICENSE','LICENSES.md','assets-src/npcs/phase3a-finalization/identity-presentations.json','assets-src/npcs/phase3a-finalization/release-status.json']:
 files[n]=(R/n).read_bytes()
for p in(R/'public/licenses').glob('*'):
 if p.is_file():files['LICENSES/'+p.name]=p.read_bytes()
files['start_review.py']=b'''from pathlib import Path
from argparse import ArgumentParser
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
import os
p=ArgumentParser();p.add_argument('--port',type=int,default=4450);p.add_argument('--lan',action='store_true');a=p.parse_args();os.chdir(Path(__file__).resolve().parent)
print(f'Open http://127.0.0.1:{a.port}/REVIEW.html',flush=True)
print('26approved development NPCs;facts/commercialrights review pending;physicaldevicesNOTTESTED;Phase3BNOTSTARTED.',flush=True)
ThreadingHTTPServer(('0.0.0.0'if a.lan else'127.0.0.1',a.port),SimpleHTTPRequestHandler).serve_forever()
'''
files['REVIEW.html']=b'<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Phase3A approved26NPC development</title><h1>26NPC approved development baseline</h1><p>Not commercial/legal/hardware certification. No Phase3Bimplementation/publicdeployment.</p><p><a href="index.html">Enter World / original CharacterStudio</a> | <a href="docs/phase3a-finalization/REVIEW.html">Native review / actual ordinary-world archive</a> | <a href="docs/phase3a/HISTORICAL_NPC_RIGHTS_AND_ALIASES.md">Rights and identities</a></p>'
files['README.md']=b"""# Approved 26-NPC development baseline

Extract the ZIP and run python3 start_review.py. Open the printed local REVIEW.html.
No Node installation or network is required for gameplay. --lan is optional private-LAN review, not public deployment.

Ordinary development gameplay registers 26 actors: 14 residents, six original visitors and six educational archive reconstructions. Fresh storage opens the unchanged Character Studio; choose one of the twelve characters and enter the world. Visit palace, bookshop or coast contexts and open the History Archive. No QA/historyArtReview flag is required. At most four actors and four textures are active, with two pending loads; one reconstruction temporarily replaces a host slot.

All approved NPC art, animation, world, players and cosmetics are unchanged. Historical names are retained, with zero fictional replacements. Names are separate from stable IDs. Commercial rights are NOT certified: applicable generation terms, jurisdiction and likeness review remain pending. Unverified biographies and real-person fact cards are excluded. No authentic quotation or completed lesson is invented.

Native crops, an actual ordinary-world gameplay video, rights matrix, QA and handoff are included locally. Optional full-resolution PNG/source links point to the immutable online checkpoint. Physical Android, iPhone and hardware GPU remain NOT TESTED. Existing warnings are retained. Phase 3B is an architectural handoff only; no implementation, main merge or deployment is authorized.
"""
for name,data in list(files.items()):
 if not name.endswith(('.md','.html')):continue
 def fix(match):
  t=match.group(1)
  if t.startswith(('http:','https:','#','data:','mailto:')):return match.group(0)
  clean=t.split('?')[0].split('#')[0];target=posixpath.normpath(posixpath.join(posixpath.dirname(name),clean)).lstrip('/')
  if target in files:return match.group(0)
  return match.group(0).replace(t,RAW+target)
 text=data.decode();text=re.sub(r'(?:href|src)="([^"]+)"',fix,text);text=re.sub(r'\]\(([^)]+)\)',fix,text);files[name]=text.encode()
files['PACKAGE_SHA256.json']=(json.dumps({n:sha(b)for n,b in sorted(files.items())},indent=2)+'\n').encode()
for n,b in files.items():p=O/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
if '--stage-only'in sys.argv:print('STAGED',len(files),'files');raise SystemExit(0)
out=D/'PHASE3A_APPROVED_26NPC_DEVELOPMENT.zip'
with ZipFile(out,'w',ZIP_DEFLATED,compresslevel=6)as z:
 for n,b in sorted(files.items()):z.writestr(n,b)
with ZipFile(out)as z:
 assert z.testzip()is None
 for n,h in json.loads(z.read('PACKAGE_SHA256.json')).items():assert sha(z.read(n))==h,n
 for p in(R/'public/assets/npcs/phase3a').rglob('*'):
  if p.is_file():assert z.read(str(p.relative_to(R/'public')))==p.read_bytes()
assert out.stat().st_size<100*1024*1024
proof={'file':out.name,'bytes':out.stat().st_size,'sha256':sha(out.read_bytes()),'CRC':'PASS','internalSHA256':'PASS','registeredNPCs':26,'approvedNativeCells':2704,'unchangedNPCAssetFiles':104,'fictionalSubstitutions':0,'commercialLegalStatus':'REVIEW_REQUIRED_NOT_CERTIFIED','verifiedHistoricalFacts':0,'physicalDevices':'NOT_TESTED','runtime':{n:sha(b)for n,b in files.items()if n.startswith('assets/')or n=='index.html'},'launch':'See independent extraction smoke,not inferred fromCRC','checkpoint':TAG};(D/'PACKAGE_PROOF.json').write_text(json.dumps(proof,indent=2)+'\n');print(out.name,proof['bytes'],proof['sha256'])
