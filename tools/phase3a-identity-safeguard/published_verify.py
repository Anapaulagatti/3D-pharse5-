"""Verify immutable GitHub artifact URLs and old-ref preservation after explicit branch publication."""
from pathlib import Path
from urllib.request import urlopen,Request
from concurrent.futures import ThreadPoolExecutor
import json,hashlib,subprocess,datetime
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a-identity-safeguard';tag='checkpoint/phase3a-fictional-identity-safeguard-20261029';raw=f'https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/refs/tags/{tag}/'
paths=['README.md','QA.md','REVIEW.html','PACKAGE_PROOF.json','PROTECTED_AUDIT.json','NATIVE_QA.json','package-smoke.json','package-native-qa.json','PHASE3B_HANDOFF.md','DEPICTION_REVIEW.md','ordinary-world-archive-menu.jpg','roster26-fictional-public-native.png','fictional-archive-actual.mp4']
paths=['docs/phase3a-identity-safeguard/'+p for p in paths]+['AGENTS.md','docs/current/PROJECT_STATE.md','docs/phase3a/HISTORICAL_NPC_RIGHTS_AND_ALIASES.md']
paths += [str(p.relative_to(R)) for p in (D/'native').glob('*')]
proof=json.loads((D/'PACKAGE_PROOF.json').read_text());zipname=str((D/proof['file']).relative_to(R));paths.append(zipname)
def check(path):
 with urlopen(Request(raw+path,method='HEAD'),timeout=45) as response:
  assert response.status==200
  return {'path':path,'status':response.status,'url':raw+path}
with ThreadPoolExecutor(max_workers=6) as pool:rows=list(pool.map(check,sorted(set(paths))))
h=hashlib.sha256();size=0
with urlopen(raw+zipname,timeout=90) as response:
 while True:
  b=response.read(1024*1024)
  if not b:break
  h.update(b);size+=len(b)
assert size==proof['bytes'] and h.hexdigest()==proof['sha256']
def refs(txt):return {line.split('\t')[1]:line.split('\t')[0] for line in txt.strip().splitlines()}
before=refs(Path('/tmp/phase3a-identity-remote-before.txt').read_text());after=refs(subprocess.check_output(['git','ls-remote','origin']).decode());changes=[k for k,v in before.items() if after.get(k)!=v];assert not changes,changes
assert after['refs/heads/main']=='33360ed1989e4db9fc3fc4e3686ca385e0b00908'
commit=subprocess.check_output(['git','rev-parse',tag+'^{}']).decode().strip()
report={'status':'PASS','approvalReference':'8a2dbe6f8077c3263f1280311e3673899f3d37f9','developmentCheckpoint':tag,'checkpointCommit':commit,'checkedAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'URLs':rows,'remoteZIPBytes':size,'remoteZIPSHA256':h.hexdigest(),'oldRemoteRefsUnchanged':len(before),'changedOldRefs':changes,'mainUnchanged':after['refs/heads/main'],'commercialLegalStatus':'REVIEW_REQUIRED_NOT_CERTIFIED','physicalDevices':'NOT_TESTED','phase3BImplementation':False,'mainMerge':False,'publicDeployment':False}
(D/'published-verification.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS',len(rows),'immutable file URLs; full ZIP download SHA256 exact;',len(before),'old refs unchanged; checkpoint',commit)
