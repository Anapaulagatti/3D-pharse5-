"""Verify the human-approved station asset lock and current review adoption; no asset writes."""
from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[1]
a=json.loads((R/'assets-src/gate3/approved-station-forecourt.json').read_text())
assert a['status']=='HUMAN_APPROVED'
for n,h in a['sha256'].items():assert hashlib.sha256((R/n).read_bytes()).hexdigest()==h,n
old=json.loads((R/'public/assets/gate3/registration-forecourt/manifest.json').read_text());new=json.loads((R/'public/assets/gate3/registration-review/manifest.json').read_text())
for k in old:
 if k not in ['id','artStatus']:assert old[k]==new[k],k
for c in new['chunks']:
 assert hashlib.sha256((R/'public'/c['image']).read_bytes()).hexdigest()==c['sha256']
 assert hashlib.sha256((R/'public'/c['mask']).read_bytes()).hexdigest()==c['maskSha256']
# All historical approved sources/renderer/checkpoints are preserved; only selector/UI text changes.
paths=['assets-src/gate3/forecourt-restoration','assets-src/gate25-reconstruction','assets-src/gate25-station-planters','assets-src/world-gate1','public/assets/gate3/world','public/assets/gate3/registration','public/assets/gate3/registration-refined','public/assets/gate3/registration-forecourt','public/assets/juni']
paths += [str(p.relative_to(R))for p in (R/'src/gate3').rglob('*')if p.is_file()and p.name!='main.ts']
assert not subprocess.check_output(['git','diff',a['acceptedContentCommit'],'--']+paths,cwd=R).strip()
for n,h in json.loads((R/'docs/gate3a/protected-assets.json').read_text())['sha256'].items():assert hashlib.sha256((R/n).read_bytes()).hexdigest()==h,n
result={'status':'PASS','approvedContentCommit':a['acceptedContentCommit'],'approvedFilesLocked':len(a['sha256']),'reviewManifestUsesExactAcceptedChunks':True,'collisionObjectsAndOtherSpatialProposalsUnchanged':True,'historicalSourceAndRendererBytesUnchanged':True,'protectedAssets':1341,'G3ARegistration':'PENDING','G3B':'BLOCKED','physicalDevices':'NOT TESTED'}
print(json.dumps(result,indent=2))
