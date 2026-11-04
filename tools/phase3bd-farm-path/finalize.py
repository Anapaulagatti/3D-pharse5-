"""Freeze one candidate, preserving all prior snapshots and canonical source art."""
from pathlib import Path
import shutil,json,hashlib,subprocess
R=Path.cwd();D=R/'docs/phase3bd-farm-path';O=R/'.cache/phase3bd-farm-path-final-review';old=R/'.cache/physical-review-candidate';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();build=json.loads((O/'hotfix-build.json').read_text());ref=build['sourceCommit']
G=O/'farm-path-review';G.mkdir(exist_ok=True)
for p in D.iterdir():
 if p.is_file() and p.suffix in ['.png','.md','.html','.json'] and p.name not in ['BASELINE.json','AUTHORIZED_AMENDMENTS.json','PACKAGE_PROOF.json','CANDIDATE_PROOF.json','FINAL_DELIVERY.json','OFFLINE_BROWSER_PROOF.json']:
  shutil.copy2(p,G/p.name)
(G/'videos').mkdir(exist_ok=True)
for p in (D/'videos').glob('*.mp4'):shutil.copy2(p,G/'videos'/p.name)
(O/'start-review.py').write_text((R/'tools/phase3bd/start-review.py').read_text().replace('/review/', '/farm-path-review/'))
(O/'LOCAL_REVIEW.txt').write_text('Unzip; python3 start-review.py; open http://127.0.0.1:4483/farm-path-review/ . No npm or internet. Public exposure of this NEW manifest PENDING. Rollback9fce709a; earlierfff156b6 retained.\n')
(O/'qa.json').write_text(json.dumps(json.loads((D/'QA_RESULT.json').read_text()),ensure_ascii=False,indent=2)+'\n')
v=json.loads((O/'version.json').read_text());v.update(gameCommit=ref,phase='Phase3BD farming lifecycle + narrow-path hotfix',dirty=False,publicExposure='PENDING_EXACT_MANIFEST_APPROVAL',physicalDevices='NOT TESTED',activeCosmetics=24);(O/'version.json').write_text(json.dumps(v,indent=2)+'\n')
(O/'phase.json').write_text(json.dumps({'phase':v['phase'],'gameRef':ref,'publicExposure':'PENDING_EXACT_MANIFEST_APPROVAL','physicalDevices':'NOT TESTED'},indent=2)+'\n')
p=O/'index.html';s=p.read_text();s=s.replace('<a href="#play">','<a href="farm-path-review/">Farm lifecycle + paths</a><a href="#play">',1);p.write_text(s)
snap=O/'phases/3b-d-farm-path'/ref[:8];assert not snap.exists();snap.mkdir(parents=True)
for name in ['index.html','style.css','app.js','catalog.json','qa.json','version.json','phase.json','history.json','hotfix-build.json','play','farm-path-review','thumbs','THIRD_PARTY_NOTICES.txt']:
 p=O/name
 if p.is_dir():shutil.copytree(p,snap/name)
 elif p.is_file():shutil.copy2(p,snap/name)
# Include any other actual portal root resources, never arbitrary private source files.
for p in O.iterdir():
 if p.is_file() and p.suffix in ['.css','.js'] and not(snap/p.name).exists():shutil.copy2(p,snap/p.name)
history=json.loads((old/'history.json').read_text())['snapshots'];(O/'history.json').write_text(json.dumps({'snapshots':[{'phase':v['phase'],'sha':ref,'path':str(snap.relative_to(O))+'/'}]+history},indent=2)+'\n');(snap/'history.json').write_text(json.dumps({'snapshots':[{'phase':v['phase'],'sha':ref,'path':'./'}]},indent=2)+'\n')
v['archived']=True;(snap/'version.json').write_text(json.dumps(v,indent=2)+'\n')
oldm=json.loads((old/'export-manifest.json').read_text());previous={r['sha256']:r for r in oldm['files']}
def manifest(root):
 rows=[]
 for p in sorted(root.rglob('*')):
  if not p.is_file() or p==root/'export-manifest.json' or '.git' in p.relative_to(root).parts:continue
  n=str(p.relative_to(root));h=sha(p);prior=previous.get(h);row={'filename':n,'sha256':h,'bytes':p.stat().st_size,'publicPreviewDecision':'PENDING_EXACT_MANIFEST_APPROVAL','commercialRelease':'NOT_CERTIFIED'}
  if prior:row.update(category='prior-approved-identical-byte',priorManifestSHA256='17306fc4c2a3f958e29a2256eb1ddbb722658917863269907554ecd005f69183',priorFilename=prior['filename'])
  else:row.update(category='original-project-hotfix-code-native-crops-or-gameplay-evidence',evidence='Original native pixel patterns and soil; approved world and actors unchanged; actual silent Phaser captures; no added third-party media',specificConcern='No identified copied work/likeness in additive crops; exact public owner manifest approval remains pending')
  rows.append(row)
 return {'schemaVersion':1,'profile':'phase3bd-farm-path26','gameCommit':ref,'portalCommit':oldm['portalCommit'],'scope':'PRIVATE REVIEW: same26fictional NPC/12players/24cosmetics; native farming stages and localized path correction. No production exposure approval invented.','files':rows}
(snap/'export-manifest.json').write_text(json.dumps(manifest(snap),indent=2)+'\n');(O/'export-manifest.json').write_text(json.dumps(manifest(O),indent=2)+'\n')
for p in (old/'phases').rglob('*'):
 if p.is_file():assert sha(p)==sha(O/'phases'/p.relative_to(old/'phases')),str(p)
q={'status':'READY_FOR_EXACT_OWNER_REVIEW; NOT DEPLOYED','sourceCommit':ref,'manifestSHA256':sha(O/'export-manifest.json'),'files':len(manifest(O)['files']),'candidate':str(O.relative_to(R)),'rollbackArtifact':'9fce709ab87698ed078fd2a545a8a696a5a104f6','earlierPublicRollback':'fff156b6e15584855f1585de5a03d21b3022cdbc','historicalSnapshotsByteExact':True,'originalArtChanges':0,'publicExposure':'PENDING_EXACT_MANIFEST_APPROVAL'}
(D/'CANDIDATE_PROOF.json').write_text(json.dumps(q,indent=2)+'\n');print(json.dumps(q,indent=2))
