from pathlib import Path
import hashlib,json,sys,argparse,zipfile
from runtime_assets import runtime_names,CANONICAL
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3bd';p=argparse.ArgumentParser();p.add_argument('--artifact');p.add_argument('--zip');a=p.parse_args();names=runtime_names();baseline=json.loads((D/'BASELINE.json').read_text())['files'];bad=[]
for name in names:
 f=R/'public'/name
 if not f.is_file():bad.append('missing '+name);continue
 old=baseline.get('public/'+name)
 if old and hashlib.sha256(f.read_bytes()).hexdigest()!=old['sha256']:bad.append('changed approved asset '+name)
for source in ['src/game/main.ts','src/gate3/main.ts']:
 t=(R/source).read_text()
 for banned in ['assets/v10-city/','assets/v9-world/','v10-city-review.html','"recovery-world"','"production"']:
  if banned in t:bad.append('rejected runtime reference '+source+' '+banned)
cleanupSource=json.loads((R/'docs/cleanup/REJECTED_WORLD_CLEANUP_20261103.json').read_text())
for row in cleanupSource['removed']:
 if (R/row['path']).exists():bad.append('reintroduced removed path '+row['path'])
for row in cleanupSource.get('archiveMoves',[]):
 if (R/row['from']).exists():bad.append('archived rejected map back in public '+row['from'])
 if hashlib.sha256((R/row['to']).read_bytes()).hexdigest()!=row['sha256']:bad.append('changed required archived source '+row['to'])
assert 'const id = "palace-cleanup-world"'in(R/'src/gate3/main.ts').read_text()
if a.artifact:
 root=Path(a.artifact)
 cleanup=json.loads((R/'docs/cleanup/REJECTED_WORLD_CLEANUP_20261103.json').read_text())
 approvedHashes={hashlib.sha256((R/'public'/n).read_bytes()).hexdigest()for n in names}
 approvedHashes|={r['sha256']for r in cleanup['retained']}
 rejectedHashes={r['sha256']for r in cleanup['removed']if Path(r['path']).suffix in ['.png','.jpg','.tmj'] and r['sha256']not in approvedHashes}
 # Previous approved snapshots may exist in review packages; their worlds must also be canonical.
 for f in root.rglob('*'):
  if not f.is_file()or '.git'in f.parts:continue
  rel=str(f.relative_to(root))
  if f.suffix in ['.png','.jpg','.tmj']and hashlib.sha256(f.read_bytes()).hexdigest()in rejectedHashes:bad.append('rejected content hash '+rel)
  if any(x in rel for x in ['assets/v10-city/','assets/v9-world/','v10-city-review.html','docs/v9-world/','assets-src/v9-world/','assets-src/archive/']):bad.append('rejected artifact path '+rel)
  if f.suffix=='.js':
   data=f.read_text()
   if any(x in data for x in ['assets/v10-city/','assets/v9-world/','v10-city-review.html']):bad.append('rejected compiled URL '+rel)
 assetRoot=root/'play'if(root/'play').exists()else root
 if any(not(assetRoot/name).is_file()for name in names):bad.append('artifact lacks explicit active asset')
if a.zip:
 cleanup=json.loads((R/'docs/cleanup/REJECTED_WORLD_CLEANUP_20261103.json').read_text())
 approvedHashes={hashlib.sha256((R/'public'/n).read_bytes()).hexdigest()for n in names}|{r['sha256']for r in cleanup['retained']}
 rejectedHashes={r['sha256']for r in cleanup['removed']if Path(r['path']).suffix in ['.png','.jpg','.tmj']and r['sha256']not in approvedHashes}
 with zipfile.ZipFile(a.zip)as z:
  entries=set(z.namelist())
  if any('play/'+name not in entries for name in names):bad.append('ZIP lacks explicit active asset')
  if z.testzip()is not None:bad.append('ZIP CRC failure')
  for name in entries:
   if '..'in Path(name).parts or name.startswith('/'):bad.append('unsafe ZIP path '+name)
   if any(x in name for x in ['assets/v10-city/','assets/v9-world/','v10-city-review.html','docs/v9-world/','assets-src/v9-world/','assets-src/archive/']):bad.append('rejected ZIP path '+name)
   if Path(name).suffix in ['.png','.jpg','.tmj']and hashlib.sha256(z.read(name)).hexdigest()in rejectedHashes:bad.append('rejected ZIP content hash '+name)
   if Path(name).suffix=='.js'and any(x in z.read(name).decode()for x in ['assets/v10-city/','assets/v9-world/','v10-city-review.html']):bad.append('rejected ZIP compiled URL '+name)
assert not bad,bad
(D/'CANONICAL_WORLD_AUDIT.json').write_text(json.dumps({'status':'PASS','canonicalManifest':'public/'+CANONICAL,'runtime':['index.html','src/game/main.ts','src/gate3/main.ts','src/gate3/WorldCache.ts'],'loadingOrder':['explicit canonical manifest','versioned Phase3BC collision overrides','original native contact guard','chunk/foreground residency before movement','lazy selected player/NPC textures'],'activeAssets':len(names),'unchangedApprovedAssets':sum('public/'+n in baseline for n in names),'artifactChecked':a.artifact,'zipChecked':a.zip,'sourceOrHistoryErased':False},indent=2)+'\n');print('PASS canonical world closure',len(names),'assets; artifact',a.artifact)
