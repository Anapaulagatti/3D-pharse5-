from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,hashlib,re,posixpath
R=Path(__file__).resolve().parents[2];D=R/'docs/phase2b-motion/walk-front';base=R/'docs/phase2b-motion/PHASE2B_MOTION_CORRECTION_REVIEW.zip';TAG='checkpoint/phase2b-walkfront-hotfix-review-20261027';RAW=f'https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/refs/tags/{TAG}/';files={}
# Compiled engine is identical: every src/config/lockfile is frozen by the audit.
with ZipFile(base)as z:
 for n in z.namelist():
  if n.startswith(('assets/','LICENSES/'))or n in ['index.html','BUILD_MANIFEST.json','LICENSE','LICENSES.md','start_review.py']:files[n]=z.read(n)
for id in ['ara','doyun','sori','jiwon','nari','taeyang','yuna','hyunwoo']:
 n=f'assets/characters/{id}/atlas.png';files[n]=(R/'public'/n).read_bytes()
for p in D.iterdir():
 if not p.is_file():continue
 n=p.name;include=p.suffix in ['.md','.html','.gif','.mp4']
 if p.suffix=='.json':include=p.stat().st_size<1300000 and not any(x in n for x in ['working','package-proof','published','failure'])
 if p.suffix=='.png':include=any(x in n for x in ['source-native','source-2x','actual-native','cosmetic-native'])
 if include:files[str(p.relative_to(R))]=p.read_bytes()
for p in(D/'logs').glob('*.log'):files[str(p.relative_to(R))]=p.read_bytes()
for name in ['WALK_FRONT_FIX.md','QA.md','VISUAL_REVIEW.md']:files[f'docs/phase2b-motion/{name}']=(R/f'docs/phase2b-motion/{name}').read_bytes()
files['README.md']=b'# Walk-front-only hotfix review\n\nRun python3 start_review.py, then open REVIEW.html. Actual compiled Phaser engine and frozen approved world;12 playable characters. Only64 walk-front frames for Ara,Doyun,Sori,Jiwon,Nari,Taeyang,Yuna,Hyunwoo changed. Walk-right is human-approved and byte-identical. No other animation or runtime edit.\n\nIncludes8 unretimed gameplay videos,8 phase-aligned actual Phaser comparisons with Juni,source-only before/after sheets and native gameplay evidence. Human front-walk approval pending. Phase2C locked. Real devices NOT TESTED.\n'
files['REVIEW.html']=b'<!doctype html><meta charset="utf-8"><h1>Walk-front hotfix review</h1><p><a href="index.html?entry=transition">Play actual Phaser</a> | <a href="docs/phase2b-motion/walk-front/REVIEW.html">Visual review</a> | <a href="docs/phase2b-motion/WALK_FRONT_FIX.md">Scope and QA</a></p><p>Human walk-front review pending. Approved walk-right unchanged. Phase2C LOCKED.</p>'
for n,data in list(files.items()):
 if not n.endswith(('.md','.html')):continue
 def fix(match):
  t=match.group(1)
  if t.startswith(('http:','https:','#','data:','mailto:')):return match.group(0)
  clean=t.split('?')[0].split('#')[0];path=posixpath.normpath(posixpath.join(posixpath.dirname(n),clean))
  if path in files:return match.group(0)
  # Old review evidence remains at its immutable historical source checkpoint.
  prefix=RAW if path.startswith('docs/phase2b-motion/walk-front/')or path.endswith('WALK_FRONT_FIX.md')else'https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/cc27eda7410336d434f7c47bc2455b0faf1f8856/'
  return match.group(0).replace(t,prefix+path)
 text=data.decode();text=re.sub(r'(?:href|src)="([^"]+)"',fix,text);text=re.sub(r'\]\(([^)]+)\)',fix,text);files[n]=text.encode()
files['PACKAGE_SHA256.json']=json.dumps({n:hashlib.sha256(b).hexdigest()for n,b in sorted(files.items())},indent=2).encode();out=D/'WALK_FRONT_HOTFIX_REVIEW.zip'
with ZipFile(out,'w',ZIP_DEFLATED,compresslevel=6)as z:
 for n,b in sorted(files.items()):z.writestr(n,b)
with ZipFile(out)as z:
 assert z.testzip()is None
 for n,h in json.loads(z.read('PACKAGE_SHA256.json')).items():assert hashlib.sha256(z.read(n)).hexdigest()==h,n
 for id in ['juni','haneul','bomi','minjun','ara','doyun','sori','jiwon','nari','taeyang','yuna','hyunwoo']:
  n='assets/juni/juni.png'if id=='juni'else f'assets/characters/{id}/atlas.png';assert z.read(n)==(R/'public'/n).read_bytes()
assert out.stat().st_size<100000000
(D/'package-proof.json').write_text(json.dumps({'file':out.name,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'CRC':'PASS','allFileHashes':'PASS','allTwelveAtlasesExact':'PASS','compiledEngine':'Unchanged cc27eda production bundle; source/config/lockfile match hotfix freeze. Only8 atlas PNG runtime assets changed.','videos':16,'humanWalkFrontReview':'PENDING','walkRight':'APPROVED UNCHANGED'},indent=2)+'\n');print(out.name,out.stat().st_size,'bytes')
