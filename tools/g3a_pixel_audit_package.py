"""Build a new audit package; never overwrite a prior review archive."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import hashlib,json,re
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3a-pixel-audit';B=Path('/tmp/g3-pixel-fixed');old=R/'docs/gate3a-corrections/G3A_TARGETED_REVIEW.zip'
files={}
with ZipFile(old)as z:
 for n in z.namelist():
  if n.startswith(('assets/','approved-prototype/'))and not re.match(r'assets/review-[^/]+\.(js|css)$',n):files[n]=z.read(n)
 files['DEVICE_CHECKLIST.md']=z.read('DEVICE_CHECKLIST.md')
html=(B/'gate3-review.html').read_bytes();files['gate3-review.html']=html
for n in re.findall(r'(?:src|href)="\./([^"]+)"',html.decode()):files[n]=(B/n).read_bytes()
files['index.html']=b'''<!doctype html><meta charset="utf-8"><title>G3-A pixel-fidelity audit</title><h1>Pixel-fidelity review / human acceptance pending</h1><p>Canvas implicit resizing and half-CSS-pixel centering corrected. Remaining source softness is documented. No G3-B authorization.</p><ul><li><a href="gate3-review.html?scene=district&entry=station">District / WebGL</a></li><li><a href="gate3-review.html?scene=district&entry=station&renderer=canvas">District / corrected Canvas</a></li><li><a href="gate3-review.html?scene=district&entry=station&native">Native station frontage</a></li><li><a href="gate3-review.html?scene=district&entry=alley">Walk and inspect the passages</a></li><li><a href="gate3-review.html?scene=registration&entry=station&native">Existing station registration candidate</a></li><li><a href="gate3-review.html?scene=world&entry=jeju">Jeju / existing scenic tour</a></li><li><a href="review-data/SOURCE_BEFORE_AFTER.png">Source / before / after</a></li><li><a href="review-data/CANVAS_BEFORE_AFTER.png">Canvas correction comparison</a></li><li><a href="review-data/REPORT.md">Diagnosis</a></li><li><a href="DEVICE_CHECKLIST.md">Physical device handoff / NOT TESTED</a></li></ul>'''
files['START_REVIEW.txt']=b'Extract the entire archive. Run python3 -m http.server 4281 --bind 127.0.0.1 and open http://127.0.0.1:4281/ . Original source art unchanged. G3-B remains blocked; human visual review pending. Native pixel evaluation: downloaded PNG at100% zoom. Physical devices NOT TESTED. No public deployment.\n'
for p in D.iterdir():
 if p.name in ['package-proof.json','package-smoke.json']:continue
 if p.name.startswith('after-')and p.name.endswith(('-native.png','-stationary.png','-moving.png')):continue
 if p.suffix in ['.md','.json'] or p.name in ['SOURCE_BEFORE_AFTER.png','CANVAS_BEFORE_AFTER.png','STATIONARY_COMPARISON.png','MOVING_COMPARISON.png','before-auto-odd-display.png','after-auto-odd-display.png','after-auto-half-zoom-odd-backing.png','after-auto-tour-moving-backing.png'] or (p.suffix=='.png' and ('-native' in p.name or '-stationary' in p.name or '-moving' in p.name or '-station-pivot-backing' in p.name or '-1x' in p.name)):
  files['review-data/'+p.name]=p.read_bytes()
files['BUILD_SOURCES_SHA256.json']=(json.dumps({str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in (R/'src/gate3').rglob('*')if p.is_file()},indent=2)+'\n').encode()
files['PACKAGE_SHA256.json']=(json.dumps({n:hashlib.sha256(b).hexdigest()for n,b in sorted(files.items())},indent=2)+'\n').encode()
out=D/'G3A_PIXEL_CRISP_REVIEW.zip'
with ZipFile(out,'w',ZIP_DEFLATED,compresslevel=6)as z:
 for n,b in sorted(files.items()):z.writestr(n,b)
with ZipFile(out)as z:
 assert z.testzip()is None
 for n,h in json.loads(z.read('PACKAGE_SHA256.json')).items():assert hashlib.sha256(z.read(n)).hexdigest()==h,n
 for n in [n for n in files if n.startswith('assets/')and not re.match(r'assets/review-',n)]:
  with ZipFile(old)as oz:assert z.read(n)==oz.read(n),n
(D/'package-proof.json').write_text(json.dumps({'file':out.name,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'CRC':'PASS','fileHashes':'PASS','allAssetBytesUnchanged':'PASS'},indent=2)+'\n')
print(out.name,out.stat().st_size)
