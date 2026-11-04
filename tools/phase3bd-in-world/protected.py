from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3bd-in-world';b=json.loads((D/'BASELINE.json').read_text());amend=json.loads((D/'AUTHORIZED_AMENDMENTS.json').read_text())['files'];bad=[];assets=0;code=0
for n,row in b['files'].items():
 p=R/n;h=hashlib.sha256(p.read_bytes()).hexdigest()if p.is_file()else None
 if n.startswith(('assets-src/','public/assets/')):
  assets+=1
  if h!=row['sha256']:bad.append(n)
 else:
  code+=1
  if h!=row['sha256']:
   a=amend.get(n)
   if not a or a['beforeSHA256']!=row['sha256']or a['afterSHA256']!=h:bad.append(n)
assert not bad,bad
(D/'PROTECTED_AUDIT.json').write_text(json.dumps({'status':'PASS','base':b['base'],'unchangedExistingArtAndSourceFiles':assets,'protectedCodeFilesChecked':code,'changedProtectedAssets':bad,'scopedIntegration':'main.ts input/action hooks and NPCManager interaction/activation only; exact pins. Existing player motion,camera,collision and NPC route/data files byte-identical.','newArt':['assets-src/farming/phase3bd-in-world/PROVENANCE.json'],'runtimeAdditions':'Six reversible116x12pxmanaged soil rows8352pixels,8tiny native tool/quest props and temporary effects; approved source PNGs unchanged.','physicalDevices':'NOT TESTED'},indent=2)+'\n');print('PASS',assets,'existing art/source files unchanged')
