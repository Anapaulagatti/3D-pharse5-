from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,re,hashlib
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-recovery';B=Path('/tmp/g3d-recovery');files={}
for scene in ['production','recovery-before','recovery-pilots']:
 rel=f'assets/gate3/{scene}/manifest.json';m=json.loads((R/'public'/rel).read_text())
 for n in [rel,m['overview']]+[c[k]for c in m['chunks']for k in ['image','mask']]+[o['image']for o in m['objects']]:files[n]=(R/'public'/n).read_bytes()
for n in ['assets/juni/juni.png','assets/juni/juni.json','assets/gate3/registration/bakery.png']:files[n]=(R/'public'/n).read_bytes()
files['gate3-review.html']=(B/'gate3-review.html').read_bytes()
for n in re.findall(r'(?:src|href)="\./([^"]+)"',files['gate3-review.html'].decode()):files[n]=(B/n).read_bytes()
for p in D.iterdir():
 if p.suffix not in ['.png','.jpg','.json','.md','.html','.mp4']:continue
 if p.suffix=='.mp4'and not p.name.endswith('-review.mp4'):continue
 if p.suffix=='.png' and p.name not in [n+'-'+state+'-native.png'for n in ['north','south','namsan']for state in ['before','candidate']]+[n+'-comparison-0-1x.png'for n in ['north','south','namsan']]:continue
 if p.name in ['package-proof.json','package-smoke.json','published-links.json','NATIVE_LINKS.md']:continue
 files[str(p.relative_to(R))]=p.read_bytes()
for n in ['KOREAN_ARENA_ART_DIRECTION_BIBLE.md','GATE3_WORLD_ART_DIRECTION_AUDIT.md','GATE3_MASTER_DEFECT_REGISTER.md','assets-src/gate3/approved-station-forecourt.json','assets-src/gate3/production-plan-v3.1-restored.json','docs/gate3-world/DEVICE_REVIEW.md','docs/current/G3D_ART_RECOVERY_AUTHORIZATION.md','docs/world-gate1/style-bible.html','package.json','package-lock.json','gate3.vite.config.ts']:
 files[n]=(R/n).read_bytes()
for p in (R/'assets-src/gate3/recovery').glob('*.json'):files[str(p.relative_to(R))]=p.read_bytes()
for p in (R/'assets-src/gate3/recovery').glob('approved-material-*.png'):files[str(p.relative_to(R))]=p.read_bytes()
files['assets-src/gate3/recovery/canonical-native-board.png']=(R/'assets-src/gate3/recovery/canonical-native-board.png').read_bytes()
for root in ['src/gate3','src/gate2','src/engine']:
 for p in (R/root).rglob('*'):
  if p.is_file():files[str(p.relative_to(R))]=p.read_bytes()
for p in (R/'tools').glob('g3d_*'):files[str(p.relative_to(R))]=p.read_bytes()
# Native recordings/large authoring masters remain immutable repository evidence rather than duplicated in ZIP.
raw='https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/refs/tags/checkpoint/g3d-three-pilot-review-20261023/docs/gate3-recovery/'
n='docs/gate3-recovery/README.md';text=files[n].decode()
for name in ['north','south','namsan']:text=text.replace(']('+name+'-traversal.webm)',']('+raw+name+'-traversal.webm)')
files[n]=text.encode()
files['start_review.py']=b'''from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
import os,argparse
p=argparse.ArgumentParser();p.add_argument('--lan',action='store_true');p.add_argument('--port',type=int,default=4296);a=p.parse_args();os.chdir(Path(__file__).resolve().parent);print(f'Open http://127.0.0.1:{a.port}/');print('Human art approval pending; physical devices NOT TESTED.');ThreadingHTTPServer(('0.0.0.0'if a.lan else'127.0.0.1',a.port),SimpleHTTPRequestHandler).serve_forever()
'''
files['START_REVIEW.txt']=b'Extract completely. Run python3 start_review.py and open http://127.0.0.1:4296/ . Node is not required. --lan is optional for trusted private Wi-Fi physical-device review. Shared art system has NOT been human-approved. Full-world propagation is BLOCKED. No public deployment. Native PNGs and review gameplay included; native WebM/source masters preserved in the repository. Physical devices and hardware WebGL performance NOT TESTED. Stop after review.\n'
links=''.join(f'<li>{title}: <a href="gate3-review.html?scene=recovery-pilots&entry={n}&pilotsOnly">PLAY candidate</a> · <a href="gate3-review.html?scene=recovery-before&entry={n}&native&pilotsOnly">matched BEFORE</a> · <a href="gate3-review.html?scene=recovery-pilots&entry={n}&native&pilotsOnly">candidate native framing</a></li>'for n,title in [('north','A Historical North'),('south','B Modern South'),('namsan','C Namsan')])
files['index.html']=('''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>G3-D shared art recovery review</title><style>body{font:18px/1.5 system-ui;max-width:1100px;margin:2em auto;padding:0 1em;background:#152b2c;color:#f5ecd7}a{color:#a5e9e5}li{margin:1em 0}</style><h1>G3-D: three pilots of one shared style system</h1><p><strong>Human artistic approval pending. Full-world propagation blocked.</strong> Original engine/prototype/source art preserved. Missing palace continuation, outer-region joins, attraction/station projection, Bakery placement and full navigation/performance/device acceptance remain open.</p><p><a href="docs/gate3-recovery/VISUAL_REVIEW.html">OPEN VISUAL GALLERY · lightweight comparisons / original native PNGs / actual gameplay</a></p><ul>'''+links+'''</ul><p><a href="docs/gate3-recovery/README.md">QA report and limitations</a> · <a href="KOREAN_ARENA_ART_DIRECTION_BIBLE.md">Art Bible</a> · <a href="GATE3_WORLD_ART_DIRECTION_AUDIT.md">Ten-region audit</a> · <a href="docs/gate3-world/DEVICE_REVIEW.md">Real-device checklist</a></p><p>WASD/arrows, Shift run, Follow/Scenic/Overview and tour. The rest of the world in these scenes remains the REJECTED history baseline. Physical Android/iPhone and hardware WebGL NOT TESTED. No merge/deployment or full-world correction authorized.</p>''').encode()
# Missing large native references link to immutable repository evidence, not broken local paths.
import posixpath
rawroot='https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/refs/tags/checkpoint/g3d-three-pilot-review-20261023/'
for n in list(files):
 if not n.endswith(('.md','.html')):continue
 text=files[n].decode()
 def fix(match):
  href=match.group(1)
  if href.startswith(('http:','https:','#','data:')):return match.group(0)
  target=posixpath.normpath(posixpath.join(posixpath.dirname(n),href.split('?')[0].split('#')[0]))
  if target not in files and (R/target).is_file():return match.group(0).replace(href,rawroot+target)
  return match.group(0)
 text=re.sub(r'(?:href|src)="([^"]+)"',fix,text);text=re.sub(r'\]\(([^)]+)\)',fix,text);files[n]=text.encode()

files['PACKAGE_SHA256.json']=(json.dumps({n:hashlib.sha256(b).hexdigest()for n,b in sorted(files.items())},indent=2)+'\n').encode()
out=D/'G3D_SHARED_STYLE_PILOTS_REVIEW.zip'
with ZipFile(out,'w',ZIP_DEFLATED,compresslevel=9)as z:
 for n,b in sorted(files.items()):z.writestr(n,b)
with ZipFile(out)as z:
 assert z.testzip()is None
 for n,h in json.loads(z.read('PACKAGE_SHA256.json')).items():assert hashlib.sha256(z.read(n)).hexdigest()==h,n
 for path in ['index.html','docs/gate3-recovery/VISUAL_REVIEW.html']:
  for href in re.findall(r'(?:href|src)="([^"]+)"',z.read(path).decode()):
   if href.startswith(('http:','https:','#')):continue
   import posixpath
   target=posixpath.normpath(posixpath.join(posixpath.dirname(path),href.split('?')[0]));assert target in files,(path,target)
assert out.stat().st_size<100000000,out.stat().st_size
(D/'package-proof.json').write_text(json.dumps({'file':out.name,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'CRC':'PASS','allFileHashes':'PASS','entryAndGalleryLinks':'PASS','sourceMasters':'Repository preserved; authoring prompts,calibration and ownership metadata included','nativeWebM':'Repository preserved; smaller MP4 review copies included','artApproval':'PENDING HUMAN','physicalDevices':'NOT TESTED'},indent=2)+'\n');print(out.name,out.stat().st_size,'bytes',len(files),'files')
