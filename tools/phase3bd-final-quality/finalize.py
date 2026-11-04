"""Freeze exact bounded candidate; no publish/approval side effects."""
from pathlib import Path
import json,hashlib,shutil,subprocess
R=Path.cwd();D=R/'docs/phase3bd-final-quality';A=D/'review-assets';O=R/'.cache/phase3bd-final-quality-review';old=R/'.cache/phase3bd-farm-path-final-review';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();build=json.loads((O/'hotfix-build.json').read_text());ref=build['sourceCommit'];evidence=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
assert json.loads((D/'frozen/FARM_QA.json').read_text())['status'].startswith('PASS')
assert json.loads((D/'HANOK_AFTER_QA.json').read_text())['status'].startswith('PASS')
qa=json.loads((D/'QA_RESULT.json').read_text());assert qa['unit']=='PASS213'and qa['e2e']=='PASS73'
# Preserve old immutable snapshot paths; only the new snapshot contains this gallery.
snap=O/'phases/3b-d-final-quality'/ref[:8];assert not snap.exists();snap.mkdir(parents=True)
v=json.loads((O/'version.json').read_text());v.update(phase='Phase3B-D final farming art / western hanok quality',gameCommit=ref,evidenceSourceCommit=evidence,dirty=False,publicExposure='PENDING_EXACT_OWNER_APPROVAL',artisticReview='PENDING_HUMAN_REVIEW',physicalDevices='NOT TESTED',farmBeds=6,farmCells=36)
(O/'version.json').write_text(json.dumps(v,indent=2)+'\n');(O/'qa.json').write_text(json.dumps(qa,indent=2)+'\n');(O/'phase.json').write_text(json.dumps({'phase':v['phase'],'gameRef':ref,'publicExposure':'PENDING_EXACT_OWNER_APPROVAL'},indent=2)+'\n')
p=O/'index.html';s=p.read_text().replace('<a href="#play">','<a href="quality-review/">Farm art + Tây Hanok · mới</a><a href="#play">',1);p.write_text(s)
for name in ['index.html','catalog.json','qa.json','version.json','phase.json','hotfix-build.json','thumbs','play']:
 p=O/name
 if p.is_dir():shutil.copytree(p,snap/name)
 elif p.is_file():shutil.copy2(p,snap/name)
for p in O.iterdir():
 if p.is_file()and p.suffix in['.css','.js','.txt']and p.name not in ['LOCAL_REVIEW.txt']:shutil.copy2(p,snap/p.name)
G=snap/'quality-review';shutil.copytree(A,G)
# An immutable gallery is stored once, instead of duplicating 35MB of native/video evidence.
rootG=O/'quality-review';rootG.mkdir();html=(G/'index.html').read_text();relative=str(G.relative_to(O))+'/'
(rootG/'index.html').write_text(html.replace('<head>','<head><base href="../'+relative+'">')if'<head>'in html else html.replace('<meta charset=',f'<base href="../{relative}"><meta charset=',1))
shutil.copy2(D/'QA.md',G/'QA.md')
linkbase='https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/'+evidence+'/'
(G/'ORIGINAL_SOURCE_LINKS.json').write_text(json.dumps({'evidenceSourceCommit':evidence,'fullNativeOriginals':[{'path':str(p.relative_to(R)),'sha256':sha(p),'url':linkbase+str(p.relative_to(R))}for p in (D/'frozen').glob('*-native.png')],'fullQA':[{'path':str(D.relative_to(R))+'/frozen/FARM_QA.json','url':linkbase+str(D.relative_to(R))+'/frozen/FARM_QA.json'}],'note':'Original native PNGs preserved unchanged in source checkpoint; published selected nativePNG re-encoded losslessly, matching exactRGBApixels; all crop evidence is original1:1pixel scale'},indent=2)+'\n')
hist=json.loads((old/'history.json').read_text())['snapshots'];(O/'history.json').write_text(json.dumps({'snapshots':[{'phase':v['phase'],'sha':ref,'path':str(snap.relative_to(O))+'/'}]+hist},indent=2)+'\n');(snap/'history.json').write_text(json.dumps({'snapshots':[{'phase':v['phase'],'sha':ref,'path':'./'}]},indent=2)+'\n');v['archived']=True;(snap/'version.json').write_text(json.dumps(v,indent=2)+'\n')
p=snap/'index.html';s=p.read_text().replace('href="farm-path-review/"','href="../../../farm-path-review/"').replace('href="review/"','href="../../../review/"');p.write_text(s)
(O/'start-review.py').write_text((R/'tools/phase3bd/start-review.py').read_text().replace('/review/','/quality-review/'))
(O/'LOCAL_REVIEW.txt').write_text('PRIVATE REVIEW. Unzip; python3 start-review.py; open http://127.0.0.1:4483/quality-review/ . No npm/network needed for game, cropped evidence and movies. Original full native source links optionally require network. New exact manifest approval PENDING.\n')
prev=json.loads((old/'export-manifest.json').read_text());previous={r['sha256']:r for r in prev['files']}
def manifest(root):
 rows=[]
 for p in sorted(root.rglob('*')):
  if not p.is_file()or p==root/'export-manifest.json'or'.git'in p.relative_to(root).parts:continue
  n=str(p.relative_to(root));digest=sha(p);row={'filename':n,'sha256':digest,'bytes':p.stat().st_size,'publicPreviewDecision':'PENDING_EXACT_OWNER_APPROVAL','commercialRelease':'NOT_CERTIFIED'};prior=previous.get(digest)
  if prior:row.update(category='prior-approved-identical-byte',priorManifestSHA256='d170ee180c4743ab8bee4b4a952c7bf1b7f69c2c8083e1b2eb84cf6846beea58',priorFilename=prior['filename'])
  else:row.update(category='original-native-crop-components-gameplay-code-or-actual-review-evidence',provenance='assets-src/farming/phase3bd-final-quality/PROVENANCE.json; originalbuiltinimagegen source+native finish.26NPC/12players/24cosmetics/worldoriginals unchanged',rights='No new third-party reference assets, fonts, voices, logos or paid-service calls; new exact exposure approval pending')
  rows.append(row)
 return {'schemaVersion':1,'profile':'phase3bd-final-quality26','gameCommit':ref,'portalCommit':prev['portalCommit'],'scope':'PRIVATE REVIEW: bounded native per-cell farm art + western-hanok mask; no production/art acceptance inferred','files':rows}
(snap/'export-manifest.json').write_text(json.dumps(manifest(snap),indent=2)+'\n');m=manifest(O);(O/'export-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
for p in(old/'phases').rglob('*'):
 if p.is_file():assert sha(p)==sha(O/'phases'/p.relative_to(old/'phases')),str(p)
size=sum(r['bytes']for r in m['files'])+(O/'export-manifest.json').stat().st_size;assert size<1_000_000_000,('Pages budget exceeded; do not silently delete approved history',size)
q={'status':'READY_FOR_OWNER_REVIEW; NOT_DEPLOYED','sourceBuildCommit':ref,'evidenceSourceCommit':evidence,'manifestSHA256':sha(O/'export-manifest.json'),'files':len(m['files']),'siteBytes':size,'pagesBudgetBytes':1_000_000_000,'candidate':str(O.relative_to(R)),'allOldSnapshotFilesByteExact':True,'galleryStoredOnce':True,'rollbackArtifact':'5b5ce278596520efd520f6af63266e57c49c3fd8','rollbackManifest':'d170ee180c4743ab8bee4b4a952c7bf1b7f69c2c8083e1b2eb84cf6846beea58','publicExposure':'PENDING_EXACT_OWNER_APPROVAL'};(D/'CANDIDATE_PROOF.json').write_text(json.dumps(q,indent=2)+'\n');print(json.dumps(q,indent=2))
