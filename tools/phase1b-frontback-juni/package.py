from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import hashlib,json
R=Path(__file__).resolve().parents[2];D=R/'docs/phase1b-frontback-juni';out=D/'PHASE1B_FRONTBACK_JUNI_REVIEW.zip';files={}
with ZipFile(R/'docs/phase1b/PHASE1B_FOUR_CHARACTER_REVIEW.zip')as old:
 for n in old.namelist():
  if n.startswith('docs/phase1b/')or n in ['PACKAGE_SHA256.json','README.md','REVIEW.html']:continue
  files[n]=old.read(n)
for id in ['haneul','bomi','minjun']:files[f'assets/characters/{id}/atlas.png']=(R/f'public/assets/characters/{id}/atlas.png').read_bytes()
for folder in ['assets-src/characters/phase1b-frontback-juni','tools/phase1b-frontback-juni','docs/phase1b-frontback-juni']:
 for p in (R/folder).rglob('*'):
  if not p.is_file()or p.suffix in ['.zip','.webm','.pyc']or p.name.endswith('-phaser-native.png')or '__pycache__'in p.parts or p.name in ['package-proof.json','published-verification.json']:continue
  files[str(p.relative_to(R))]=p.read_bytes()
for n in ['AGENTS.md','docs/current/PROJECT_STATE.md','docs/current/PHASE1B_FRONTBACK_DIRECTIVE.md']:files[n]=(R/n).read_bytes()
files['README.md']=b'# Corrected front/back Juni-motion review\n\nRun python3 start_review.py; open REVIEW.html. Current candidate replaces only32 atlas frame rectangles per Haneul/Bomi/Minjun. All other frames/runtime/world assets unchanged. Human motion approval pending; Phase2 locked.\n'
files['REVIEW.html']=b'<!doctype html><meta charset="utf-8"><h1>Focused front/back correction</h1><p><a href="index.html">Play actual Phaser world</a> | <a href="docs/phase1b-frontback-juni/REVIEW.html">Visual review, comparisons and gameplay videos</a> | <a href="docs/phase1b-frontback-juni/QA.md">QA</a></p><p>Human motion acceptance pending. Phase2 locked. Physical devices NOT TESTED.</p>'
# Full native screenshots remain in the immutable review checkpoint; compact native crops stay offline.
for n,data in list(files.items()):
 if n.endswith('.html'):
  text=data.decode()
  import re
  text=re.sub(r'(href=\")([^\"]+-phaser-native.png)(\")',lambda m:m[1]+'https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/refs/tags/checkpoint/phase1b-frontback-juni-review-20261026/docs/phase1b-frontback-juni/'+m[2]+m[3],text)
  files[n]=text.encode()
files['PACKAGE_SHA256.json']=(json.dumps({n:hashlib.sha256(b).hexdigest()for n,b in sorted(files.items())},indent=2)+'\n').encode()
with ZipFile(out,'w',ZIP_DEFLATED,compresslevel=6)as z:
 for n,b in sorted(files.items()):z.writestr(n,b)
with ZipFile(out)as z:
 assert z.testzip()is None
 for n,h in json.loads(z.read('PACKAGE_SHA256.json')).items():assert hashlib.sha256(z.read(n)).hexdigest()==h,n
assert out.stat().st_size<100000000
(D/'package-proof.json').write_text(json.dumps({'file':out.name,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'CRC':'PASS','allHashes':'PASS','files':len(files),'basis':'Accepted portable Phase1B compiled runtime; only three atlas PNGs patched to the new candidate. No source runtime change; original world/resources and own layered character sources retained. New sources, QA, native evidence and videos included.','humanMotionAcceptance':'PENDING'},indent=2)+'\n');print(out.stat().st_size,len(files))
