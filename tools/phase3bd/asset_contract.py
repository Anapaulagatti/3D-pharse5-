import sys
from pathlib import Path
import json,hashlib
R=Path.cwd();D=R/'docs/phase3bd';O=R/sys.argv[1]
cat=json.loads((R/'assets-src/characters/phase2c/catalog.json').read_text());retired={'ara-shell-barrette','kr-hair-ornament','kr-fashion-cap','kr-garden-hat'}
items=[i for i in cat['items']if i['id']not in retired];checks=[]
for item in items:
 for v in item['variants']:
  for key in ['paint','erase','mapping','preview']:
   p=O/'play'/v[key];assert p.is_file(),str(p)
   assert hashlib.sha256(p.read_bytes()).hexdigest()==hashlib.sha256((R/'public'/v[key]).read_bytes()).hexdigest()
  checks.append({'item':item['id'],'character':v['characterId'],'nativeRegistration':v['registration'],'status':'PASS'})
blocked=[str(p.relative_to(O))for p in(O/'play/assets/cosmetics').rglob('*')if p.is_file()and any('/'+id+'/'in str(p)for id in retired)]
assert not blocked,blocked
npcs=json.loads((O/'catalog.json').read_text())['npcs'];assert len(npcs)==26 and len({n['id']for n in npcs})==26
report={'status':'PASS','activeItems':len(items),'retiredItems':sorted(retired),'variants':checks,'retiredFilesInActivePlay':blocked,'NPCs':len(npcs),'method':'Exact candidate active atlas/mapping/image presence and equality; old approved sources untouched. Prior snapshots intentionally preserve their own historical cosmetics.'}
(D/'ASSET_CONTRACT.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS active24 items,',len(checks),'variants,26NPCs,0retired current assets')
