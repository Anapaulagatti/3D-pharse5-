from pathlib import Path
from urllib.request import urlopen,Request
from concurrent.futures import ThreadPoolExecutor
import json,hashlib,subprocess,re,time,datetime
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a-final-six';tag='checkpoint/phase3a-26-art-candidates-source-blocked-review-20261028';raw=f'https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/refs/tags/{tag}/';paths=set();missing=[]
for p in list(D.glob('*.md'))+[D/'REVIEW.html']:
 for t in re.findall(r'\]\(([^)]+)\)|(?:href|src)="([^"]+)"',p.read_text()):
  target=next(x for x in t if x)
  if target.startswith(('https:','http:','#','data:')):continue
  target=target.split('?')[0].split('#')[0];q=(p.parent/target).resolve()
  if q.is_file():paths.add(str(q.relative_to(R)))
  else:missing.append({'from':str(p.relative_to(R)),'target':target})
for p in(D/'PLAYABLE_PACKAGE_PROOF.json',D/'package-smoke.json',D/'package-native-qa.json',D/'SOURCE_EVIDENCE.json',D/'ART_PROVENANCE.json',D/'protected-audit.json'):paths.add(str(p.relative_to(R)))
assert not missing,missing
proof=json.loads((D/'PLAYABLE_PACKAGE_PROOF.json').read_text());zipname=str((D/proof['file']).relative_to(R));paths.add(zipname)
def check(path):
 url=raw+path
 for n in range(3):
  try:
   with urlopen(Request(url,method='HEAD'),timeout=30)as r:assert r.status==200;return {'path':path,'url':url,'status':r.status}
  except Exception:
   if n==2:raise
   time.sleep(1)
with ThreadPoolExecutor(max_workers=8)as pool:rows=list(pool.map(check,sorted(paths)))
h=hashlib.sha256();size=0
with urlopen(raw+zipname,timeout=60)as r:
 while True:
  b=r.read(1024*1024)
  if not b:break
  h.update(b);size+=len(b)
assert size==proof['bytes']and h.hexdigest()==proof['sha256']
def refs(txt):return dict(line.split('\t')[::-1]for line in txt.strip().splitlines())
before=refs(Path('/tmp/phase3a-final-six-remote-before.txt').read_text());after=refs(subprocess.check_output(['git','ls-remote','origin']).decode());changes=[k for k,v in before.items()if after.get(k)!=v];assert not changes,changes
report={'status':'PASS','reviewCommit':'831022a8533c1d2126f77724d6eea8aeca2e8e30','tag':tag,'checkedAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewRepositoryURLsChecked':len(rows),'URLs':rows,'fullRemoteZIPBytes':size,'fullRemoteZIPSHA256':h.hexdigest(),'oldRemoteRefsUnchanged':len(before),'changedOldRefs':changes,'mainUnchanged':after['refs/heads/main'],'sourceOfficialURLs':'Still transport-blocked; excluded from review-file availability count,not marked verified','publicSiteDeployment':False}
(D/'published-verification.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS',len(rows),'review-fileURLs,full93MBdownloadSHA,',len(before),'oldrefs unchanged;main',report['mainUnchanged'])
