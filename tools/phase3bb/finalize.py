"""Freeze a new private exact-payload candidate and retain the previously approved snapshot."""
from pathlib import Path
import json,hashlib,shutil,sys,datetime
R=Path.cwd();O=Path(sys.argv[1]).resolve();D=R/'docs/phase3bb-hotfix';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert O.is_relative_to(R/'.cache');old=json.loads((O/'export-manifest.json').read_text());version=json.loads((O/'version.json').read_text());snap=next((O/'phases/3b-b').iterdir());assert snap.is_dir()
previous=R/'.cache/exposure20-private/phases/3b-a/contemporary20-e0f9db0d';target=O/'phases/3b-a/contemporary20-e0f9db0d';assert sha(previous/'export-manifest.json')=='9abfcea015e3da66df25a56ab9a872d62bfd7bcdc1984894a69cd829829f1215';shutil.copytree(previous,target)
qa=json.loads((D/'runtime26/LIVE_QA.json').read_text());assert qa['status'].startswith('PASS PRIVATE LOCAL 26')and len(qa['actors'])==26
# Lightweight current evidence only. Historical images/source masters remain private.
names=['REVIEW.html','QA.md','MOVEMENT_ROOT_CAUSE.md','RIGHTS_AND_SIX.md','ROSTER26-native.png','ROSTER26.json','PROTECTED_AUDIT.json','COSMETIC_QA.json','HAIR_REPAIR.json','CAMERA_REGRESSION.json','MOVEMENT_MATRIX.json','hair-before-native.png','hair-after-native.png','before/gameplay.mp4','after/gameplay.mp4','juni-custom-gameplay.mp4','minjun-custom-gameplay.mp4','doyun-custom-gameplay.mp4','sori-custom-gameplay.mp4']
names +=[str(p.relative_to(D))for p in(D/'head-variants').glob('*.png')]
for root in [O,snap]:
 for name in names:
  p=root/'hotfix'/('index.html'if name=='REVIEW.html'else name);p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(D/name,p)
 (root/'qa.json').write_text(json.dumps({'status':'PASS LOCAL TARGETED QA; FULL REGRESSION SEE HOTFIX REPORT','summary':'26 real NPC approaches, KO/VI dialogues, return controls, daily-life clock, 1509 initial asset URLs and mobile touch passed; no console/resource errors. Actual reduced-motion camera lead before60px/after0px. Four customized character input/persistence matrix and protected9119-file audit passed. Native art acceptance/public exposure pending; physical devices NOT TESTED. Full E2E status and retained warnings are recorded in hotfix/QA.md.'},ensure_ascii=False,indent=2)+'\n')
 h=[{'phase':'Phase3B-B hotfix full26 candidate','sha':version['gameCommit'],'path':('./'if root==snap else str(snap.relative_to(O))+'/')},{'phase':'Approved Phase3B-A Contemporary20','sha':'20674e77c1495474115f5cab16a78b7f6b52d8f8','path':('../../3b-a/contemporary20-e0f9db0d/'if root==snap else 'phases/3b-a/contemporary20-e0f9db0d/')}]
 (root/'history.json').write_text(json.dumps({'snapshots':h},ensure_ascii=False,indent=2)+'\n')
 p=root/'index.html';s=p.read_text().replace('<a href="#play">','<a href="hotfix/">Hotfix · trước/sau</a><a href="#play">');p.write_text(s)
 (root/'phase.json').write_text(json.dumps({'phase':'Phase3B-B targeted hotfix','slug':'3b-b','gameRef':version['gameCommit'],'artisticReview':'PENDING','publicExposure':'PENDING_EXACT_OWNER_APPROVAL'},indent=2)+'\n')
version.update(dirty=False,sourceSnapshotNote='Source commit pins implemented code. QA/review packaging is a separately hashed exact export.',exposure='PENDING_EXACT_OWNER_PUBLIC_APPROVAL')
(O/'version.json').write_text(json.dumps(version,indent=2)+'\n');(snap/'version.json').write_text(json.dumps({**version,'archived':True,'currentPath':'../../../'},indent=2)+'\n')
base={r['filename']:r for r in old['files']};snapRel=str(snap.relative_to(O))+'/'
def manifest(root):
 files=[]
 for p in sorted(root.rglob('*')):
  if not p.is_file()or p==root/'export-manifest.json':continue
  rel=str(p.relative_to(root));key=rel[len(snapRel):]if rel.startswith(snapRel)else rel;x=dict(base.get(key,{}));x.update(filename=rel,sha256=sha(p),bytes=p.stat().st_size)
  if rel.startswith('phases/3b-a/'):x.update(origin='Byte-identical prior approved Contemporary20 snapshot',category='previous-approved-snapshot')
  elif key.startswith('hotfix/'):x.update(origin='docs/phase3bb-hotfix/'+key[len('hotfix/'):],category='new-phase-gameplay-evidence'if p.suffix=='.mp4'else'new-phase-review-evidence')
  elif 'assets/cosmetics/phase3bb/'in rel:x.update(origin='tools/phase3bb/repair_hair.py; own original native patch finishing',category='new-native-head-cosmetic')
  files.append(x)
 return{**old,'profile':'phase3bb-fictional26','scope':'PRIVATE exact Phase3B-B hotfix candidate. 26 fictional identities; prior20 approved snapshot retained unchanged. New exact owner public exposure decision PENDING. No legal/commercial clearance implied.','files':files}
(snap/'export-manifest.json').write_text(json.dumps(manifest(snap),ensure_ascii=False,indent=2)+'\n');(O/'export-manifest.json').write_text(json.dumps(manifest(O),ensure_ascii=False,indent=2)+'\n')
proof={'candidate':str(O.relative_to(R)),'manifestSHA256':sha(O/'export-manifest.json'),'files':len(manifest(O)['files']),'sourceCommit':version['gameCommit'],'npcIds':[n['id']for n in json.loads((O/'catalog.json').read_text())['npcs']],'snapshots':{str((p/'export-manifest.json').relative_to(O)):sha(p/'export-manifest.json')for p in [snap,target]},'existing20SnapshotByteExact':True,'publicDecision':'PENDING','physicalDevices':'NOT TESTED'}
(D/'PUBLIC_CANDIDATE_PROOF.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps(proof,indent=2))
