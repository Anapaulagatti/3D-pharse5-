"""Private consolidated review + exact export. NEVER publishes or sets approval true."""
from pathlib import Path
import json,hashlib,shutil,sys
R=Path.cwd();D=R/'docs/phase3bd';O=R/sys.argv[1];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old26=R/'.cache/phase3bb-26-exposure-candidate';assert sha(old26/'export-manifest.json')=='db9d4bb68f31c819d79ec95efaad1befce257086e64c41a5c93c2ba6fe7deb2f'
for sub in ['3b-a','3b-b']:
 source=old26/'phases'/sub
 if source.exists() and not (O/'phases'/sub).exists():shutil.copytree(source,O/'phases'/sub)
snap=next((O/'phases/3b-d').iterdir())
# Prior snapshots are byte-identical; current root and current phase get the new consolidated review.
qa=json.loads((D/'QA_RESULT.json').read_text())
for root in [O,snap]:
 out=root/'review';out.mkdir(exist_ok=True)
 for p in D.iterdir():
  if p.is_file() and not p.name.startswith('offline-') and (p.suffix in ['.png','.md','.json'] and p.name not in ['BASELINE.json','PUBLIC_CANDIDATE_PROOF.json','PACKAGE_PROOF.json','HUMAN_DIRECTIVE.md','AUTHORIZED_AMENDMENTS.json','OFFLINE_BROWSER_PROOF.json','DEPLOYMENT_PREPARATION.json','FINAL_DELIVERY.json'] or p.name in ['QA.md','DEFECTS.md','REMAINING_SPATIAL_PROPOSALS.json','HISTORICAL_FAILURES.md','KOREAN_CONTENT_REVIEW.md','NATIVE_RENDERING.json','FULL_REGRESSION_STATS.json','COLLISION_REVIEW.md','RUNTIME_QA.json','TRAVERSAL_QA.json','PROTECTED_AUDIT.json','NAVIGATION_AUDIT.json','COLLISION_AMENDMENTS.json','VIDEO_PROOF.json','QA_RESULT.json','BROWSER_PERFORMANCE.json','ASSET_CONTRACT.json']):shutil.copy2(p,out/p.name)
 (out/'videos').mkdir(exist_ok=True)
 legacy=out/'legacy-quests';legacy.mkdir(exist_ok=True)
 for p in (D/'legacy-quests').rglob('*'):
  if p.is_file() and p.suffix in ['.png','.json','.mp4']:
   target=legacy/p.relative_to(D/'legacy-quests');target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
 cleanup=out/'cleanup';cleanup.mkdir(exist_ok=True)
 for p in (R/'docs/cleanup').glob('*20261103*'):
  if p.is_file():shutil.copy2(p,cleanup/p.name)
 for p in (D/'videos').glob('*.mp4'):shutil.copy2(p,out/'videos'/p.name)
 shutil.copy2(D/'REVIEW.html',out/'index.html')
 p=root/'index.html';text=p.read_text();text=text if 'href="review/"'in text else text.replace('<a href="#play">','<a href="review/">Phase3B-D · nông trại và cửa hàng</a><a href="#play">');p.write_text(text)
 (root/'qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')
 version=json.loads((root/'version.json').read_text());version.update(dirty=False,exposure='PENDING_EXACT_OWNER_PUBLIC_APPROVAL',activeCosmetics=24,retiredHeadEquipment=4,learningMode='LOCAL_DEMO_HUMAN_CONTENT_REVIEW_PENDING');(root/'version.json').write_text(json.dumps(version,indent=2)+'\n')
 (root/'phase.json').write_text(json.dumps({'phase':'Phase3B-D farming/shops/cleanup','slug':'3b-d','gameRef':version['gameCommit'],'publicExposure':'PENDING_EXACT_OWNER_APPROVAL','artisticReview':'PENDING','physicalDevices':'NOT TESTED'},indent=2)+'\n')
 paths=[{'phase':'Phase3B-D candidate','path':('./'if root==snap else str(snap.relative_to(O))+'/'),'sha':version['gameCommit']},{'phase':'Approved Phase3B-B26 rollback','path':('../../3b-b/e48ea63b-e48ea63b/'if root==snap else'phases/3b-b/e48ea63b-e48ea63b/'),'sha':'74235a6e7075b77840d2e9fdf36dce678288cd05'},{'phase':'Approved Contemporary20','path':('../../3b-a/contemporary20-e0f9db0d/'if root==snap else'phases/3b-a/contemporary20-e0f9db0d/'),'sha':'20674e77c1495474115f5cab16a78b7f6b52d8f8'}]
 (root/'history.json').write_text(json.dumps({'snapshots':paths},indent=2)+'\n')
shutil.copy2(R/'tools/phase3bd/start-review.py',O/'start-review.py')
(O/'LOCAL_REVIEW.txt').write_text('Private Phase3BD farm/shop/cleanup candidate. Unzip then run: python3 start-review.py\nOpen http://127.0.0.1:4483/review/ . No npm or internet required.\nNo new public exposure approval; current production/review Pages is unchanged.\nPhysical Android/iPhone NOT TESTED.\n')
# Old generation/rights evidence is inherited only for unchanged bytes. New code/content/masks are separately authored.
previous=json.loads((old26/'export-manifest.json').read_text());byHash={r['sha256']:r for r in previous['files']}
def manifest(root):
 rows=[]
 for p in sorted(root.rglob('*')):
  if not p.is_file()or p==root/'export-manifest.json'or '.git'in p.relative_to(root).parts:continue
  digest=sha(p);prior=byHash.get(digest);name=str(p.relative_to(root));npcId=next((n['id']for n in json.loads((O/'catalog.json').read_text())['npcs'] if '/'+n['id']+'/'in '/'+name or Path(name).stem==n['id']), None)
  row={'npcId':npcId,'filename':name,'sha256':digest,'bytes':p.stat().st_size,'publicPreviewDecision':'PENDING_EXACT_OWNER_APPROVAL','commercialRelease':'NOT_CERTIFIED'}
  if prior:row.update(evidence='Byte-identical to previously approved26 exposure record',priorManifestSHA256='db9d4bb68f31c819d79ec95efaad1befce257086e64c41a5c93c2ba6fe7deb2f',priorFilename=prior['filename'])
  else:row.update(evidence='Original project code, native hand-authored crop pixels, exact approved Jeju crop for postcard, beginner questions, gameplay evidence and review metadata; no new third-party images, fonts or voice',risk='Korean educational review pending; exact new public exposure NOT approved')
  if name.endswith(('farming/crops.png','farming/crops.json')):row.update(origin='assets-src/farming/phase3bd/PROVENANCE.json',category='new-original-native-crop-art')
  elif name.endswith('farming/postcard.png'):row.update(origin='assets-src/farming/phase3bd/POSTCARD_PROVENANCE.json',category='approved-source-native-crop-no-resampling')
  elif name.endswith('.mp4'):row.update(origin='Actual project Phaser browser recording; VIDEO_PROOF.json',category='original-silent-gameplay-review')
  elif prior:row['category']=prior.get('category','prior-approved-identical-byte')
  else:row['category']='original-project-code-content-or-review-evidence'
  rows.append(row)
 return {'schemaVersion':1,'profile':'phase3bd-farm26','scope':'Private Phase3BD candidate;26 fictionalNPC/world/12players/24activecosmetics/5quests/6plots/2crops/shop/localdemo/inventory; old approved snapshots retained. Not public or commercial clearance.','gameCommit':version['gameCommit'],'portalCommit':version['portalCommit'],'files':rows}
(snap/'export-manifest.json').write_text(json.dumps(manifest(snap),ensure_ascii=False,indent=2)+'\n');(O/'export-manifest.json').write_text(json.dumps(manifest(O),ensure_ascii=False,indent=2)+'\n')
# Enforce exact prior snapshot preservation.
for sub in ['3b-a','3b-b']:
 for p in (old26/'phases'/sub).rglob('*'):
  if p.is_file():assert sha(p)==sha(O/'phases'/sub/p.relative_to(old26/'phases'/sub)),str(p)
proof={'manifestSHA256':sha(O/'export-manifest.json'),'files':len(manifest(O)['files']),'candidate':str(O.relative_to(R)),'sourceCommit':version['gameCommit'],'publicApproval':'PENDING','publicRollbackArtifact':'74235a6e7075b77840d2e9fdf36dce678288cd05','developmentRollbackArtifact':'b0164331134d5ea9ebce306fc3b16a19b9565744','priorSnapshotsByteExact':True,'canonicalApprovedAssetChanges':0}
(D/'PUBLIC_CANDIDATE_PROOF.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps(proof,indent=2))
