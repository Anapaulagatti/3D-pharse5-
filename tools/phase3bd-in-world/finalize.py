"""Private exact candidate only; no approval or publication side effects."""
from pathlib import Path
import json,hashlib,shutil,sys
R=Path.cwd();D=R/'docs/phase3bd-in-world';O=R/sys.argv[1];old=R/'.cache/rollback-artifact';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(old/'export-manifest.json')=='543ccd32deb9f37efaf3dd5c8ce48886db95f329657a63ba9c29c4f47b3d49b0'
for sub in (old/'phases').iterdir():
 if not (O/'phases'/sub.name).exists():shutil.copytree(sub,O/'phases'/sub.name)
snap=next((O/'phases/3b-d-in-world').iterdir());qa=json.loads((D/'QA_RESULT.json').read_text());assert qa['checks'].get('currentE2ECoverage','').startswith('PASS') and qa['checks']['actualWorldGameplay'].startswith('PASS') and qa['checks']['mobileLandscape'].startswith('PASS')
for root in [O,snap]:
 out=root/'review';out.mkdir(exist_ok=True)
 excluded={'BASELINE.json','HUMAN_DIRECTIVE.md','AUTHORIZED_AMENDMENTS.json','PUBLIC_CANDIDATE_PROOF.json','PACKAGE_PROOF.json','FINAL_DELIVERY.json','OFFLINE_BROWSER_PROOF.json','DEPLOYMENT_PREPARATION.json','RECOVERY.md'}
 for p in D.iterdir():
  if p.is_file()and p.suffix in ['.png','.jpg','.md','.json']and p.name not in excluded:shutil.copy2(p,out/p.name)
 (out/'videos').mkdir(exist_ok=True)
 for p in (D/'videos').glob('*.mp4'):shutil.copy2(p,out/'videos'/p.name)
 shutil.copy2(D/'REVIEW.html',out/'index.html');p=root/'index.html';s=p.read_text();s=s.replace('<a href="#play">','<a href="review/">Phase3BD · tương tác trong thế giới</a><a href="#play">',1);p.write_text(s)
 (root/'qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n');v=json.loads((root/'version.json').read_text());assert not v['dirty'],'Source must be committed before compile';v.update(exposure='PENDING_EXACT_OWNER_PUBLIC_APPROVAL',activeCosmetics=24,learningMode='LOCAL_DEMO_HUMAN_CONTENT_REVIEW_PENDING');(root/'version.json').write_text(json.dumps(v,indent=2)+'\n')
 (root/'phase.json').write_text(json.dumps({'phase':'Phase3BD physical world gameplay','slug':'3b-d-in-world','gameRef':v['gameCommit'],'publicExposure':'PENDING_EXACT_OWNER_APPROVAL','artisticReview':'PENDING','physicalDevices':'NOT TESTED'},indent=2)+'\n')
 oldhist=json.loads((old/'history.json').read_text())['snapshots'];hist=[{'phase':'Phase3BD physical gameplay candidate','path':'./'if root==snap else str(snap.relative_to(O))+'/','sha':v['gameCommit']}]
 for h in oldhist:
  row={**h};row['path']=('../../'+h['path'].removeprefix('phases/'))if root==snap else h['path'];hist.append(row)
 (root/'history.json').write_text(json.dumps({'snapshots':hist},indent=2)+'\n')
shutil.copy2(R/'tools/phase3bd/start-review.py',O/'start-review.py');(O/'LOCAL_REVIEW.txt').write_text('PRIVATE Phase3BD physical gameplay. Unzip then python3 start-review.py\nOpen http://127.0.0.1:4483/review/ . No npm/internet. Python3 required.\nExact new public approval PENDING; oldfff156b6/543ccd32 retained as rollback.\nPhysical devices NOT TESTED. Human Korean content review PENDING.\n')
prior=json.loads((old/'export-manifest.json').read_text());byHash={r['sha256']:r for r in prior['files']}
def manifest(root):
 rows=[]
 for p in sorted(root.rglob('*')):
  if not p.is_file()or p==root/'export-manifest.json'or '.git'in p.relative_to(root).parts:continue
  digest=sha(p);oldrow=byHash.get(digest);n=str(p.relative_to(root));row={'filename':n,'sha256':digest,'bytes':p.stat().st_size,'publicPreviewDecision':'PENDING_EXACT_OWNER_APPROVAL','commercialRelease':'NOT_CERTIFIED'}
  if oldrow:row.update(evidence='Byte-identical to prior owner-approved Phase3BD preview manifest',priorManifestSHA256='543ccd32deb9f37efaf3dd5c8ce48886db95f329657a63ba9c29c4f47b3d49b0',priorFilename=oldrow['filename'],category=oldrow.get('category','prior-approved-identical-byte'))
  else:row.update(evidence='Project-authored physical interaction/UI code,8original native tool props, QA metadata or silent project Phaser recording; no new third-party image/font/audio',category='original-project-code-content-review',risk='Human gameplay/art review and exact new public exposure approval PENDING; Korean educational review pending')
  if n.endswith(('farming/interaction-tools.png','farming/interaction-tools.json')):row.update(origin='assets-src/farming/phase3bd-in-world/PROVENANCE.json',category='original-hand-authored-native-tool-pixels')
  rows.append(row)
 return {'schemaVersion':1,'profile':'phase3bd-in-world26','scope':'PRIVATE:26fictionalNPC/12players/24cosmetics;physical farming,3corequests,existing2economyquests,contextualshop,compactHUD. Exact exposure PENDING. Prior snapshots byte-exact.','gameCommit':v['gameCommit'],'portalCommit':v['portalCommit'],'files':rows}
(snap/'export-manifest.json').write_text(json.dumps(manifest(snap),ensure_ascii=False,indent=2)+'\n');(O/'export-manifest.json').write_text(json.dumps(manifest(O),ensure_ascii=False,indent=2)+'\n')
for p in (old/'phases').rglob('*'):
 if p.is_file():assert sha(p)==sha(O/'phases'/p.relative_to(old/'phases')),str(p)
proof={'manifestSHA256':sha(O/'export-manifest.json'),'files':len(manifest(O)['files']),'candidate':str(O.relative_to(R)),'sourceCommit':v['gameCommit'],'publicApproval':'PENDING','publicRollbackArtifact':'fff156b6e15584855f1585de5a03d21b3022cdbc','publicRollbackManifestSHA256':'543ccd32deb9f37efaf3dd5c8ce48886db95f329657a63ba9c29c4f47b3d49b0','priorSnapshotsByteExact':True,'canonicalApprovedArtChanges':0};(D/'PUBLIC_CANDIDATE_PROOF.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps(proof,indent=2))
