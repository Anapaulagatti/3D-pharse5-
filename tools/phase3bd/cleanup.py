"""Evidence-backed active-tree deletion; never rewrites Git history or touches approved closure."""
from pathlib import Path
import json,subprocess,hashlib,sys
from runtime_assets import runtime_names
R=Path(__file__).resolve().parents[2];D=R/'docs/cleanup';baseline=json.loads((R/'docs/phase3bd/BASELINE.json').read_text());closure={'public/'+p for p in runtime_names()};north=json.loads((R/'assets-src/protected-north/protection.json').read_text());northHashes=set(north['nativeImages'].values());files=baseline['files'];removed=[];retained=[]
roots=('docs/v9-world/','docs/v10-city/','assets-src/v9-world/','assets-src/v10-city/','public/assets/v10-city/')
# Exact northern preservation fixture is an authored Gate1 dependency, independent of rejected southern maps.
keep={'docs/v10-city/V10_NORTH.png','assets-src/v10-city/protected-files.json'}
for name,row in files.items():
 if name.startswith(roots) and row['sha256']in northHashes and name.startswith('assets-src/') :keep.add(name)
# Keep a sole original approved northern image even if its only current location is in public legacy storage.
for name,row in files.items():
 if name.startswith('public/assets/v10-city/') and row['sha256']in northHashes:
  if not any(files[n]['sha256']==row['sha256']for n in keep):keep.add(name)
for name,row in files.items():
 if not name.startswith(roots):continue
 reason=None
 if name in closure:reason='APPROVED_ACTIVE: exact canonical runtime manifest dependency'
 elif name in keep:reason='REQUIRED_SOURCE_OR_ROLLBACK: approved historical north native donor / Gate1 comparison reference; NOT runtime'
 elif any(word in Path(name).name.lower()for word in ['provenance','rights','license','safety','input-reference']):reason='REQUIRED_SOURCE_OR_ROLLBACK: original generation/rights evidence retained, no runtime imports'
 if reason:retained.append({'path':name,**row,'classification':reason.split(':')[0],'reason':reason});continue
 removed.append({'path':name,**row,'classification':'CONFIRMED_REJECTED_UNUSED','rejectionEvidence':'Owner Phase3BD Task0 explicit V6–V10 rejection + docs/gate1/GATE1_SOURCE_AND_SKILLS.md excludes old southern inputs','dependencyEvidence':'Canonical runtime closure excludes path; retired legacy bootstrap/build/E2E removed from active inputs; historical snapshots remain in Git'})
for name in ['src/main.ts','src/world/World.ts','src/world/ui.ts','src/world/style.css','v10-city-review.html','tools/review_graphics.py',*subprocess.check_output(['git','ls-files','tools/v10*'],cwd=R,text=True).splitlines()]:
 if name in files:removed.append({'path':name,**files[name],'classification':'CONFIRMED_REJECTED_UNUSED','rejectionEvidence':'Owner Phase3BD Task0; obsolete V10 scene/authoring entrypoint, replaced by current canonical loader','dependencyEvidence':'No import from current src/game/main.ts → src/gate3/main.ts; active tests/build updated to canonical world; historical implementation remains at baseline Git tag'})
assert not closure.intersection(r['path']for r in removed)
q={'schemaVersion':1,'base':baseline['base'],'historyRewritten':False,'canonicalWorld':'public/assets/gate3/palace-cleanup-world/manifest.json','removed':removed,'retained':retained,'removedCount':len(removed),'removedBytes':sum(r['bytes']for r in removed),'scopeNote':'Inventory roots inspected by content/dependency. Other approved Gate1/Gate2/Gate3/character/provenance folders retained; old full maps are not selected or copied by current build. No branch/tag/source-history deletion.'}
(D/'REJECTED_WORLD_CLEANUP_20261103.json').write_text(json.dumps(q,indent=2)+'\n')
for start in range(0,len(removed),100):subprocess.run(['git','rm','--',*[r['path']for r in removed[start:start+100]]],cwd=R,check=True,stdout=subprocess.DEVNULL)
print('git rm',len(removed),'files;',q['removedBytes'],'bytes;',len(retained),'documented source exceptions')
