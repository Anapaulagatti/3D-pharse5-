"""One self-contained playable candidate; untouched native core screenshots included.
Additional original/crop/source evidence links resolve to the immutable review tag.
"""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,re,hashlib,posixpath,io
from PIL import Image
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-final';B=Path('/tmp/g3final-review');files={}
TAG='checkpoint/g3d-final-surgical-review-20261025';RAW='https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/refs/tags/'+TAG+'/'
rel='assets/gate3/final-world/manifest.json';m=json.loads((R/'public'/rel).read_text())
for rel in ['assets/gate3/'+k+'/manifest.json' for k in ['final-world','final-station-candidate','final-station-ground']]:
 m=json.loads((R/'public'/rel).read_text())
 for n in ([m['farmMetadata']]if'farmMetadata'in m else[])+[rel,m['overview']]+[c[k]for c in m['chunks']for k in ['image','mask']]+[o['image']for o in m['objects']]+[m['contactCollision']['physical']]+['assets/juni/juni.png','assets/juni/juni.json']:
  files[n]=(R/'public'/n).read_bytes()
html=(B/'gate3-review.html').read_text();redirect='<script>if(!new URLSearchParams(location.search).has("scene"))location.replace(location.pathname+"?scene=final-world&worldOnly")</script>';assert '<head>'in html
files['gate3-review.html']=html.replace('<head>','<head>'+redirect,1).encode()
for n in re.findall(r'(?:src|href)="\./([^"]+)"',html):files[n]=(B/n).read_bytes()
core=['palace','academy','culture','transition','retail','station','namsan','amusement','market','jeju-culture']
pngs={'farm-after-native.png','western-house-after-native.png','station-front-station-candidate-native.png','station-independent-source-native.png','western-house-after-crop-1x.png','western-courtyard-after-crop-1x.png'}
pngs.update(q.name for q in D.glob('*-crop-1x.png'))
usedJpg=set()
for page in [D/'VISUAL_REVIEW.md',D/'VISUAL_REVIEW.html']:
 usedJpg.update(re.findall(r'([A-Za-z0-9_-]+\.jpg)',page.read_text()))
for p in D.iterdir():
 if not p.is_file()or p.name.startswith(('package-','published-','NATIVE_LINKS')):continue
 if p.suffix in ['.md','.json','.html','.svg']or(p.suffix=='.jpg'and p.name in usedJpg)or p.name in pngs or p.name in ['world-traversal-review.mp4']:files[str(p.relative_to(R))]=p.read_bytes()
for n in ['KOREAN_ARENA_ART_DIRECTION_BIBLE.md','GATE3_MASTER_DEFECT_REGISTER.md','GATE3_WORLD_ART_DIRECTION_AUDIT.md','assets-src/gate3/approved-station-forecourt.json','assets-src/gate3/production-plan-v3.1-restored.json','docs/current/G3D_FINAL_SURGICAL.md','package.json','package-lock.json','gate3.vite.config.ts']:
 files[n]=(R/n).read_bytes()
for p in (R/'assets-src/gate3/final-surgical-v1').glob('*.json'):files[str(p.relative_to(R))]=p.read_bytes()
for root in ['src/gate3','src/gate2','src/engine']:
 for p in (R/root).rglob('*'):
  if p.is_file():files[str(p.relative_to(R))]=p.read_bytes()
for p in (R/'tools').glob('g3ds_*'):
 if p.is_file():files[str(p.relative_to(R))]=p.read_bytes()
files['start_review.py']=b'''from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
import os,argparse
p=argparse.ArgumentParser();p.add_argument('--lan',action='store_true');p.add_argument('--port',type=int,default=4300);a=p.parse_args();os.chdir(Path(__file__).resolve().parent);print(f'Open http://127.0.0.1:{a.port}/');print('Consolidated candidate only. Bakery/P1s open. Physical devices NOT TESTED.');ThreadingHTTPServer(('0.0.0.0'if a.lan else'127.0.0.1',a.port),SimpleHTTPRequestHandler).serve_forever()
'''
files['START_REVIEW.txt']=('Extract completely. Run python3 start_review.py and open http://127.0.0.1:4300/ . No Node needed for playback. --lan is optional only for trusted private Wi-Fi physical review. Final world art acceptance pending; Bakery and P1s remain. No main merge/public deployment. Three untouched core native PNGs, original-resolution house/courtyard/pose crops and standalone station source and lightweight actual gameplay included. Extra originals/crops/native-resolution video/source masters are immutable repository links. Physical Android/iPhone and hardware performance NOT TESTED. Source reproduction requires the full repository checkout at '+TAG+'; scripts included here document the pipeline, not all historical authoring inputs.\n').encode()
core+=['farm','western-house','western-courtyard','house-court','station-precinct','station-upper','station-front','station-right','bridge-mainland','bridge-island','bridge-full','coast-middle','palace-entrance','retail-block']
links=''.join(f'<li>{key}: <a href="gate3-review.html?scene=final-world&entry={key}&worldOnly">PLAY MAIN</a> · <a href="gate3-review.html?scene=final-world&entry={key}&native&worldOnly">NATIVE frame</a></li>'for key in core)
files['index.html']=('''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>G3-D surgical review</title><style>body{font:18px/1.5 system-ui;max-width:1100px;margin:2em auto;padding:0 1em;background:#162e31;color:#f4e9d1}a{color:#99e3dd}li{margin:.6em 0}</style><h1>Final G3-D surgical candidate</h1><p><strong>Human artistic acceptance pending. MAIN retains OLD station.</strong> House/garden, compact six-plot NW farm, local landing/asphalt joins only. The new station remains a separate pending candidate. Original sources/Juni/scale/protected environments remain exact outside authorized masks. Bakery unplaced, platform8px strip, bridge complete stop/turn contact, inherited routes/projections and physical hardware tests remain open.</p><p><a href="docs/gate3-final/VISUAL_REVIEW.html">OPEN VISUAL GALLERY / native originals / actual gameplay / QA</a></p><p><a href="gate3-review.html?scene=final-station-candidate&entry=station&worldOnly">PLAY NEW STATION CANDIDATE — not adopted</a> · <a href="gate3-review.html?scene=final-station-candidate&entry=station-precinct&native&wideNative&worldOnly">NEW station native precinct</a> · <a href="gate3-review.html?scene=final-station-ground&entry=station-precinct&native&wideNative&worldOnly">GROUND STAGE — old/new architecture removed</a></p><ul>'''+links+'''</ul><p><a href="docs/gate3-final/FARM_PLOTS.json">Six plot metadata</a> · <a href="docs/gate3-final/DEVICE_REVIEW.md">Device checklist/export</a> · <a href="docs/gate3-final/QA.md">Honest PASS/FAIL/NOT TESTED</a> · <a href="docs/gate3-final/README.md">Remaining decisions</a></p><p>Original WASD/arrows · Shift run · mobile landscape joystick · Scenic/Tour/Return. No farming inventory/timers/economy/quests implemented. No main merge/public deployment or unsupported physical-device PASS.</p>''').encode()

# Keep local playable files self-contained; extra evidence/source references use
# immutable raw links rather than missing local files. Original PNGs stay untouched. Offline JPEG copies are max900px/quality68; full review copies remain in repository.
def fix_link(n,match):
 href=match.group(1)
 if href.startswith(('http:','https:','#','data:','mailto:')):return match.group(0)
 target=posixpath.normpath(posixpath.join(posixpath.dirname(n),href.split('?')[0].split('#')[0]))
 if target.endswith('G3D_FINAL_SURGICAL_REVIEW.zip') or (posixpath.basename(target).startswith('package-') and target not in files) or (target not in files and (R/target).is_file()):return match.group(0).replace(href,RAW+target)
 return match.group(0)
for n in list(files):
 if not n.endswith(('.md','.html')):continue
 text=files[n].decode();text=re.sub(r'(?:href|src)="([^"]+)"',lambda match:fix_link(n,match),text);text=re.sub(r'\]\(([^)]+)\)',lambda match:fix_link(n,match),text);files[n]=text.encode()
# Extra-light offline JPEG derivatives only. Native PNGs and original gallery files unchanged.
for n in list(files):
 if n.endswith('.jpg'):
  im=Image.open(io.BytesIO(files[n])).convert('RGB')
  if im.width>900:im=im.resize((900,round(im.height*900/im.width)),Image.Resampling.NEAREST)
  outJpg=io.BytesIO();im.save(outJpg,format='JPEG',quality=68,optimize=True);files[n]=outJpg.getvalue()
files['PACKAGE_SHA256.json']=(json.dumps({n:hashlib.sha256(b).hexdigest()for n,b in sorted(files.items())},indent=2)+'\n').encode()
out=D/'G3D_FINAL_SURGICAL_REVIEW.zip'
with ZipFile(out,'w',ZIP_DEFLATED,compresslevel=9)as z:
 for n,b in sorted(files.items()):z.writestr(n,b)
with ZipFile(out)as z:
 assert z.testzip()is None
 for n,h in json.loads(z.read('PACKAGE_SHA256.json')).items():assert hashlib.sha256(z.read(n)).hexdigest()==h,n
 for n in ['index.html','docs/gate3-final/VISUAL_REVIEW.html','docs/gate3-final/README.md','docs/gate3-final/DEVICE_REVIEW.md']:
  for href in re.findall(r'(?:href|src)="([^"]+)"',z.read(n).decode())+re.findall(r'\]\(([^)]+)\)',z.read(n).decode()):
   if href.startswith(('http:','https:','#')):continue
   target=posixpath.normpath(posixpath.join(posixpath.dirname(n),href.split('?')[0]));assert target in files,(n,target)
assert out.stat().st_size<100000000,out.stat().st_size
(D/'package-proof.json').write_text(json.dumps({'file':out.name,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'CRC':'PASS','allFileHashes':'PASS','entryAndGalleryLocalLinks':'PASS','nativeCoreScreenshots':'Three untouched native1280x900 Phaser PNGs: farm, western house, NEW station candidate; original house/courtyard/pose crops, standalone SOURCE PNG. Other originals via immutable links','extraEvidence':'Immutable repository links; no source PNG overwritten','artAcceptance':'PENDING HUMAN','physicalDevices':'NOT TESTED'},indent=2)+'\n');print(out.name,out.stat().st_size,'bytes',len(files),'files')
