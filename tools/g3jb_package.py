"""Single private playable world, native proof crops, review movie and device handoff."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,re,hashlib,posixpath
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-jeju-bridges';B=Path('/tmp/g3jb-review');files={};TAG='checkpoint/g3d-jeju-two-bridges-review-20261025';RAW='https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/refs/tags/'+TAG+'/'
rel='assets/gate3/jeju-bridges-world/manifest.json';m=json.loads((R/'public'/rel).read_text())
for n in [rel,m['overview'],m['farmMetadata'],m['contactCollision']['physical']]+[c[k]for c in m['chunks']for k in ['image','mask']]+[o['image']for o in m['objects']]+['assets/juni/juni.png','assets/juni/juni.json']:files[n]=(R/'public'/n).read_bytes()
text=(B/'gate3-review.html').read_text();redirect='<script>if(!new URLSearchParams(location.search).has("scene"))location.replace(location.pathname+"?scene=jeju-bridges-world&entry=bridge-a-full&worldOnly")</script>';files['gate3-review.html']=text.replace('<head>','<head>'+redirect,1).encode()
for n in re.findall(r'(?:src|href)="(?:\./|/)?(assets/[^\"]+)"',text):files[n]=(B/n).read_bytes()
for p in D.iterdir():
 if not p.is_file()or p.name.startswith(('package-','published-','initial-','NATIVE_LINKS')):continue
 if p.suffix in ['.md','.json','.html']or p.suffix=='.jpg'or p.name.endswith(('-crop-1x.png','-detail-1x.png'))or p.name=='world-traversal-review.mp4':files[str(p.relative_to(R))]=p.read_bytes()
for n in ['KOREAN_ARENA_ART_DIRECTION_BIBLE.md','GATE3_MASTER_DEFECT_REGISTER.md','AGENTS.md','docs/current/G3D_STATION_APPROVAL_JEJU_BRIDGES.md','assets-src/gate3/approved-fresh-hanbit.json']:files[n]=(R/n).read_bytes()
for p in (R/'tools').glob('g3jb_*'):
 if p.is_file():files[str(p.relative_to(R))]=p.read_bytes()
for p in (R/'assets-src/gate3/jeju-bridges-v1').glob('*.json'):files[str(p.relative_to(R))]=p.read_bytes()
with ZipFile(R/'docs/gate3-station-clean/HANBIT_CLEAN_REBUILD_REVIEW.zip')as z:files['start_review.py']=z.read('start_review.py')
entries=['bridge-a-full','bridge-b-full','station-all','palace','academy','culture','transition','retail','station','namsan','amusement','market','jeju-culture']
links=''.join(f'<li><a href="gate3-review.html?scene=jeju-bridges-world&entry={e}&worldOnly">{e}</a></li>'for e in entries)
files['index.html']=f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Two Jeju crossings review</title></head><body><h1>Two Jeju crossings / Hanbit approved and locked</h1><p>Private review only. Bridge human artistic acceptance pending. Physical Android/iPhone NOT TESTED.</p><ul>{links}</ul><p><a href="docs/gate3-jeju-bridges/VISUAL_REVIEW.html">Before/after native evidence and gameplay</a> · <a href="docs/gate3-jeju-bridges/QA.md">QA</a> · <a href="docs/gate3-jeju-bridges/DEVICE_REVIEW.md">Physical device checklist/export workflow</a></p></body></html>'.encode()
files['README.md']=b'# Private two-bridge review\n\nRun `python3 start_review.py`, open the localhost URL. Original WASD/arrows, Shift run, mobile joystick, E explore, Scenic/Tour/Return and report export preserved. Native art remains1:1. Physical devices/hardware performance NOT TESTED. Human bridge art approval pending. No public site deployed.\n'
# Keep small native crops offline. Unmodified full frames and source masters use
# explicit immutable links, never silently downscaled stand-ins.
for n,data in list(files.items()):
 if not n.endswith(('.md','.html')):continue
 text=data.decode()
 if n.endswith('.html')and'<head>'in text:text=text.replace('<head>','<head><link rel="icon" href="data:,">',1)
 def resolve(match):
  target=match.group(1)
  if target.startswith(('http:','https:','#','data:','mailto:'))or '?'in target:return match.group(0)
  path=posixpath.normpath(posixpath.join(posixpath.dirname(n),target)).lstrip('/')
  if path in files:return match.group(0)
  return match.group(0).replace(target,RAW+path)
 text=re.sub(r'(?:href|src)="([^"]+)"',resolve,text);text=re.sub(r'\]\(([^)]+)\)',resolve,text);files[n]=text.encode()
assert not re.search(r'(?:src|href)="https?[^"]+\.(?:js|css)"',files['gate3-review.html'].decode()),'Runtime dependencies must be offline local files'
files['PACKAGE_SHA256.json']=(json.dumps({n:hashlib.sha256(b).hexdigest()for n,b in sorted(files.items())},indent=2)+'\n').encode();out=D/'JEJU_TWO_BRIDGES_REVIEW.zip'
with ZipFile(out,'w',ZIP_DEFLATED,compresslevel=9)as z:
 for n,b in sorted(files.items()):z.writestr(n,b)
with ZipFile(out)as z:
 assert z.testzip()is None
 for n,h in json.loads(z.read('PACKAGE_SHA256.json')).items():assert hashlib.sha256(z.read(n)).hexdigest()==h,n
assert out.stat().st_size<100000000,out.stat().st_size
(D/'package-proof.json').write_text(json.dumps({'file':out.name,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'CRC':'PASS','allFileHashes':'PASS','runtimeScenes':['jeju-bridges-world'],'nativeEvidence':'Untouched1:1 original Phaser crops offline; full native PNGs via immutable links. No resized substitutes.','artAcceptance':'PENDING HUMAN','physicalDevices':'NOT TESTED'},indent=2)+'\n');print(out.name,out.stat().st_size,'bytes',len(files),'files')
