"""Single portable art-review package, not a source-verified history release."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import importlib.util,json,hashlib,posixpath,re,sys
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a-final-six';O=Path('/tmp/phase3a-history-review');TAG='checkpoint/phase3a-26-art-candidates-source-blocked-review-20261028';RAW=f'https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/refs/tags/{TAG}/'
spec=importlib.util.spec_from_file_location('inventory',R/'tools/phase3a-npc-expansion/inventory.py');inv=importlib.util.module_from_spec(spec);spec.loader.exec_module(inv)
def sha(b):return hashlib.sha256(b).hexdigest()
files={n:(R/'public'/n).read_bytes()for n in inv.runtime_names()}
for n in ['index.html','tools/phase3a-final-six/clip-inspector.html']:files[n]=(O/n).read_bytes()
build=json.loads((O/'.vite/manifest.json').read_text())
for row in build.values():
 for n in[row['file']]+row.get('css',[])+row.get('assets',[]):files[n]=(O/n).read_bytes()
files['BUILD_MANIFEST.json']=json.dumps(build,indent=2).encode()
for p in D.rglob('*'):
 if not p.is_file()or'__pycache__'in p.parts:continue
 n=p.name;rel=p.relative_to(D)
 if n=='boundary-traversal-actual.mp4':continue # Full unique traversal remains versioned/linked online, not duplicated into portable runtime
 if p.suffix in ['.zip','.webm']or'working'in n or n in ['PLAYABLE_PACKAGE_PROOF.json','package-smoke.json','published-verification.json']:continue
 if rel.parts[0]=='tooling':
  if p.suffix=='.png':continue
  if not(n.startswith(('final-','current-'))or n in ['doctor.json','diagnostics.log','portable-build.log','sheet-qc.json']):continue
  if n=='final-e2e.log':continue # obsolete intentionally interrupted run
 if rel.parts[0]=='gameplay':
  if n.endswith('-actual.mp4'):continue # Full originals stay versioned; portable continuous native crops below
  if not(n.endswith(('-context-native.png','-review.jpg','-notice.jpg','-vocabulary.jpg','-actual.mp4'))):continue
 if n.endswith('-software-webgl-native.png'):continue
 if n.endswith('-pilot-native.png'):continue
 files[str(p.relative_to(R))]=p.read_bytes()
S=R/'assets-src/npcs/phase3a-final-six'
for p in S.rglob('*'):
 if not p.is_file()or'__pycache__'in p.parts:continue
 if'frames'in p.parts or'master-prepared'in p.parts or'master-job'in p.parts:continue
 if p.suffix=='.png'and not any(v in p.parts for v in ['native','layers']):continue
 files[str(p.relative_to(R))]=p.read_bytes()
for p in(R/'tools/phase3a-final-six').glob('*'):
 if p.is_file()and p.suffix in ['.py','.mjs','.html']:
  key=str(p.relative_to(R))
  if key not in files:files[key]=p.read_bytes()
files['start_review.py']=b'''from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from argparse import ArgumentParser
import os
p=ArgumentParser();p.add_argument('--port',type=int,default=4416);p.add_argument('--lan',action='store_true');a=p.parse_args();os.chdir(Path(__file__).resolve().parent)
print(f'Open http://127.0.0.1:{a.port}/REVIEW.html',flush=True)
print('20productionNPCs /26ARTcandidateIDs. Historicalfacts/costumesUNVERIFIED;physicaldevicesNOTTESTED;Phase3BLOCKED.',flush=True)
ThreadingHTTPServer(('0.0.0.0'if a.lan else'127.0.0.1',a.port),SimpleHTTPRequestHandler).serve_forever()
'''
files['README.md']=b'''# Korean Arena:26actor ART REVIEW / historical sources BLOCKED
Run python3 start_review.py, then open the printed local REVIEW.html. No Node/install/network is required to PLAY. --lan is an explicit private-LAN device-review option,not public deployment.
Normal world has14residents+6original visitors=20. Review links activate an actual26-definition catalog with6independently illustrated104-cell historical art actors,one reconstruction at a time. Historical facts/costumes are UNVERIFIED and production historicalArchiveCount is0. Neutral KO/VI art-review narration/vocabulary is not a finished sourced biography.0/6real-person fact cards. Do not call this final verified26NPCacceptance.
The frozen world,12players,28cosmetics/46variants and20NPCart remain unchanged. Fresh installation may show the original Character Studio first:select a character and Enter World,then use review links. Existing WASD/arrows/Shift/E/mobile joystick remain.
Native context PNG crops/readable previews/livePhaser inspector/six actual continuous native-crop gameplay videos are local. Full1280x900originals remain versioned; REVIEW_CLIP_PROVENANCE.json records time/crop with no spatial resize. Optional full native world PNGs,original high-resolution illustrations,every source frame and complete diagnostic archives are safely versioned in the immutable review ref and linked online;they are not required to play. Authoring reproduction requires the full repository and optional pinned tooling/dependencies. No source illustration is presented as gameplay. Physical Android/iPhone/hardwareGPU NOTTESTED. Phase3B/mainmerge/deployment remain locked.
'''
files['REVIEW.html']=b'<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Korean Arena historical art review</title><h1>26actor ART REVIEW /20production NPCs</h1><p>Historical facts/costumes UNVERIFIED. Not final verified26NPCacceptance. Physical devices NOTTESTED.</p><p><a href="docs/phase3a-final-six/REVIEW.html">Six historical art actors,gameplay,source gate and review links</a> | <a href="index.html">Enter World / Character Studio</a> | <a href="tools/phase3a-final-six/clip-inspector.html">Live native Phaser comparison</a> | <a href="docs/phase3a-final-six/QA.md">QA</a></p>'
for name in ['phaser','zod']:
 for p in [R/'node_modules'/name/'LICENSE',R/'node_modules'/name/'LICENSE.txt']:
  if p.exists():files[f'LICENSES/{name}.txt']=p.read_bytes();break
# Map repository public links to actual local runtime assets. Optional original
# sources/evidence omitted from the portable copy link to the immutable ref.
for n,data in list(files.items()):
 if not n.endswith(('.md','.html')):continue
 def fix(match):
  t=match.group(1)
  if t.startswith(('http:','https:','#','data:','mailto:')):return match.group(0)
  clean=t.split('?')[0].split('#')[0];target=posixpath.normpath(posixpath.join(posixpath.dirname(n),clean)).lstrip('/')
  if target in files:return match.group(0)
  if target.startswith('docs/phase3a-final-six/gameplay/')and target.endswith('-actual.mp4'):
   crop=target.replace('/gameplay/','/review-clips/').replace('-actual.mp4','-native-crop.mp4')
   if crop in files:return match.group(0).replace(t,posixpath.relpath(crop,posixpath.dirname(n)or'.'))
  if target.startswith('public/')and target[7:]in files:
   local=posixpath.relpath(target[7:],posixpath.dirname(n)or'.');return match.group(0).replace(t,local)
  if clean.startswith(('/','<')):return match.group(0)
  return match.group(0).replace(t,RAW+target)
 text=data.decode();text=re.sub(r'(?:href|src)="([^"]+)"',fix,text);text=re.sub(r'\]\(([^)]+)\)',fix,text);files[n]=text.encode()
files['PACKAGE_SHA256.json']=(json.dumps({n:sha(b)for n,b in sorted(files.items())},indent=2)+'\n').encode()
for n,b in files.items():p=O/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
if '--stage-only'in sys.argv:print('STAGED',len(files),'files;noZIPcreated');raise SystemExit(0)
out=D/'PHASE3A_26_ACTOR_ART_REVIEW_SOURCE_BLOCKED.zip'
with ZipFile(out,'w',ZIP_DEFLATED,compresslevel=6)as z:
 for n,b in sorted(files.items()):z.writestr(n,b)
with ZipFile(out)as z:
 assert z.testzip()is None
 for n,h in json.loads(z.read('PACKAGE_SHA256.json')).items():assert sha(z.read(n))==h,n
 for p in(R/'public/assets/npcs/phase3a').rglob('*'):
  if p.is_file():assert z.read(str(p.relative_to(R/'public')))==p.read_bytes()
 for id,h in json.loads((R/'assets-src/characters/phase2c/base-bindings.json').read_text()).items():
  n='assets/juni/juni.png'if id=='juni'else f'assets/characters/{id}/atlas.png';assert sha(z.read(n))==h,id
report={'file':out.name,'bytes':out.stat().st_size,'sha256':sha(out.read_bytes()),'files':len(files),'runtimeAssetFiles':len(inv.runtime_names()),'reviewActorIDs':26,'normalProductionActors':20,'newHistoricalArtCandidates':6,'verifiedProductionHistoricalActors':0,'verifiedModernIconCards':0,'CRC':'PASS','internalHashes':'PASS','all26NPCBytes':'EXACT','all12PlayerAtlases':'EXACT','runtime':{n:sha(b)for n,b in files.items()if n.startswith('assets/')or n in ['index.html','tools/phase3a-final-six/clip-inspector.html']},'includedActualVideos':sorted(n for n in files if n.endswith('.mp4')),'nativeContextCrops':'1:1; full unmodified native screenshots retained online','physicalDevices':'NOT TESTED','humanSixArtApproval':'PENDING','sourceVerification':'BLOCKED','checkpoint':TAG,'launchSmoke':'See independent extraction report; not inferred from CRC'}
(D/'PLAYABLE_PACKAGE_PROOF.json').write_text(json.dumps(report,indent=2)+'\n');print(out.name,report['bytes'],'bytes SHA256',report['sha256'])
