"""One self-contained playable candidate; untouched native core screenshots included.
Additional original/crop/source evidence links resolve to the immutable review tag.
"""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,re,hashlib,posixpath
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-reconciliation';B=Path('/tmp/g3dr-review');files={}
TAG='checkpoint/g3d-spatial-reconciliation-review-20261024';RAW='https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/refs/tags/'+TAG+'/'
rel='assets/gate3/reconciled-world/manifest.json';m=json.loads((R/'public'/rel).read_text())
for rel in ['assets/gate3/reconciled-world/manifest.json','assets/gate3/reconciled-palace-proposal/manifest.json']:
 m=json.loads((R/'public'/rel).read_text())
 for n in [rel,m['overview']]+[c[k]for c in m['chunks']for k in ['image','mask']]+[o['image']for o in m['objects']]+['assets/juni/juni.png','assets/juni/juni.json','assets/gate3/registration/bakery.png']:
  files[n]=(R/'public'/n).read_bytes()
html=(B/'gate3-review.html').read_text();redirect='<script>if(!new URLSearchParams(location.search).has("scene"))location.replace(location.pathname+"?scene=reconciled-world&worldOnly")</script>';assert '<head>'in html
files['gate3-review.html']=html.replace('<head>','<head>'+redirect,1).encode()
for n in re.findall(r'(?:src|href)="\./([^"]+)"',html):files[n]=(B/n).read_bytes()
core=['palace','academy','culture','transition','retail','station','namsan','amusement','market','jeju-culture']
pngs={n+'-after-native.png'for n in ['palace-compound','station-precinct','jeju-bridge']}
usedJpg=set()
for page in [D/'VISUAL_REVIEW.md',D/'VISUAL_REVIEW.html']:
 usedJpg.update(re.findall(r'([A-Za-z0-9_-]+\.jpg)',page.read_text()))
for p in D.iterdir():
 if not p.is_file()or p.name.startswith(('package-','published-','NATIVE_LINKS')):continue
 if p.suffix in ['.md','.json','.html','.svg']or(p.suffix=='.jpg'and p.name in usedJpg)or p.name in pngs or p.name=='world-traversal-review.mp4':files[str(p.relative_to(R))]=p.read_bytes()
for n in ['KOREAN_ARENA_ART_DIRECTION_BIBLE.md','GATE3_MASTER_DEFECT_REGISTER.md','GATE3_WORLD_ART_DIRECTION_AUDIT.md','assets-src/gate3/approved-station-forecourt.json','assets-src/gate3/production-plan-v3.1-restored.json','docs/current/G3D_SPATIAL_RECONCILIATION.md','package.json','package-lock.json','gate3.vite.config.ts']:
 files[n]=(R/n).read_bytes()
for p in (R/'assets-src/gate3/reconciliation-v1').glob('*.json'):files[str(p.relative_to(R))]=p.read_bytes()
for root in ['src/gate3','src/gate2','src/engine']:
 for p in (R/root).rglob('*'):
  if p.is_file():files[str(p.relative_to(R))]=p.read_bytes()
for p in (R/'tools').glob('g3dr_*'):
 if p.is_file():files[str(p.relative_to(R))]=p.read_bytes()
files['start_review.py']=b'''from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
import os,argparse
p=argparse.ArgumentParser();p.add_argument('--lan',action='store_true');p.add_argument('--port',type=int,default=4300);a=p.parse_args();os.chdir(Path(__file__).resolve().parent);print(f'Open http://127.0.0.1:{a.port}/');print('Consolidated candidate only. Bakery/P1s open. Physical devices NOT TESTED.');ThreadingHTTPServer(('0.0.0.0'if a.lan else'127.0.0.1',a.port),SimpleHTTPRequestHandler).serve_forever()
'''
files['START_REVIEW.txt']=('Extract completely. Run python3 start_review.py and open http://127.0.0.1:4300/ . No Node needed for playback. --lan is optional only for trusted private Wi-Fi physical review. Final world art acceptance pending; Bakery and P1s remain. No main merge/public deployment. Three original native PNGs and lightweight actual gameplay included. Extra originals/crops/native-resolution video/source masters are immutable repository links. Physical Android/iPhone and hardware performance NOT TESTED. Source reproduction requires the full repository checkout at '+TAG+'; scripts included here document the pipeline, not all historical authoring inputs.\n').encode()
links=''.join(f'<li>{key}: <a href="gate3-review.html?scene=reconciled-world&entry={key}&worldOnly">PLAY</a> · <a href="gate3-review.html?scene=reconciled-world&entry={key}&native&worldOnly">NATIVE framing</a></li>'for key in core)
files['index.html']=('''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>G3-D consolidated recovery review</title><style>body{font:18px/1.5 system-ui;max-width:1100px;margin:2em auto;padding:0 1em;background:#162e31;color:#f4e9d1}a{color:#99e3dd}li{margin:.6em 0}</style><h1>G3-D · spatial and shared-ownership reconciliation candidate</h1><p><strong>Human artistic/spatial approval pending.</strong> Bakery unplaced; tower/ride projections, station strip, inherited routes, full-body clearance and physical-device performance remain open. This is a review world, not an accepted release.</p><p><a href="docs/gate3-reconciliation/VISUAL_REVIEW.html">OPEN VISUAL GALLERY / native originals / actual gameplay / QA</a></p><ul>'''+links+'''</ul><p><a href="docs/gate3-reconciliation/DEVICE_REVIEW.md">Real-device checklist and export</a> · <a href="docs/gate3-reconciliation/COVERAGE.md">Actual coverage</a> · <a href="docs/gate3-reconciliation/README.md">Remaining decisions</a></p><p><a href="gate3-review.html?scene=reconciled-palace-proposal&entry=palace-compound&native&wideNative&worldOnly">PALACE PROPOSAL ONLY — not adopted</a></p><p>WASD/arrows · Shift run · mobile landscape joystick · Scenic/Tour/Return. Original Juni/assets/checkpoints preserved. No main merge, public deployment or unsupported physical-device PASS.</p>''').encode()

# Keep local playable files self-contained; extra evidence/source references use
# immutable raw links rather than missing local files. Original PNGs stay untouched.
def fix_link(n,match):
 href=match.group(1)
 if href.startswith(('http:','https:','#','data:','mailto:')):return match.group(0)
 target=posixpath.normpath(posixpath.join(posixpath.dirname(n),href.split('?')[0].split('#')[0]))
 if target.endswith('G3D_SPATIAL_RECONCILIATION_REVIEW.zip') or (posixpath.basename(target).startswith('package-') and target not in files) or (target not in files and (R/target).is_file()):return match.group(0).replace(href,RAW+target)
 return match.group(0)
for n in list(files):
 if not n.endswith(('.md','.html')):continue
 text=files[n].decode();text=re.sub(r'(?:href|src)="([^"]+)"',lambda match:fix_link(n,match),text);text=re.sub(r'\]\(([^)]+)\)',lambda match:fix_link(n,match),text);files[n]=text.encode()
files['PACKAGE_SHA256.json']=(json.dumps({n:hashlib.sha256(b).hexdigest()for n,b in sorted(files.items())},indent=2)+'\n').encode()
out=D/'G3D_SPATIAL_RECONCILIATION_REVIEW.zip'
with ZipFile(out,'w',ZIP_DEFLATED,compresslevel=9)as z:
 for n,b in sorted(files.items()):z.writestr(n,b)
with ZipFile(out)as z:
 assert z.testzip()is None
 for n,h in json.loads(z.read('PACKAGE_SHA256.json')).items():assert hashlib.sha256(z.read(n)).hexdigest()==h,n
 for n in ['index.html','docs/gate3-reconciliation/VISUAL_REVIEW.html']:
  for href in re.findall(r'(?:href|src)="([^"]+)"',z.read(n).decode()):
   if href.startswith(('http:','https:','#')):continue
   target=posixpath.normpath(posixpath.join(posixpath.dirname(n),href.split('?')[0]));assert target in files,(n,target)
assert out.stat().st_size<100000000,out.stat().st_size
(D/'package-proof.json').write_text(json.dumps({'file':out.name,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'CRC':'PASS','allFileHashes':'PASS','entryAndGalleryLocalLinks':'PASS','nativeCoreScreenshots':'Three untouched native Phaser PNGs: full2048x1280 palace/station and1280x900 bridge; all other originals via immutable links','extraEvidence':'Immutable repository links; no source PNG overwritten','artAcceptance':'PENDING HUMAN','physicalDevices':'NOT TESTED'},indent=2)+'\n');print(out.name,out.stat().st_size,'bytes',len(files),'files')
