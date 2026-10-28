"""Verify exact review ref, native/media/document URLs and full remote ZIP checksum."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request,urllib.parse,json,hashlib,subprocess,re,time
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a-npc-expansion';TAG='checkpoint/phase3a-npc-expansion-20-source-blocked-review-20261028';RAW='https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/refs/tags/'+TAG+'/'
def refs(s):return {line.split()[1]:line.split()[0]for line in s.splitlines()if line.strip()}
before=refs(Path('/tmp/phase3a-exp-remote-before.txt').read_text());after=refs(subprocess.check_output(['git','ls-remote','origin'],cwd=R,text=True));assert all(after.get(n)==h for n,h in before.items()),'Historical remote ref changed';assert after['refs/heads/main']=='33360ed1989e4db9fc3fc4e3686ca385e0b00908'
commit=subprocess.check_output(['git','rev-parse',TAG+'^{commit}'],cwd=R,text=True).strip();assert after['refs/tags/'+TAG+'^{}']==commit
paths=set()
for n in ['README.md','ART_PIPELINE.md','STYLE_BIBLE.md','NPC_ROSTER_26.md','HISTORY_FACT_CHECK.md','MODERN_RIGHTS_MATRIX.md','MODERN_KOREAN_ICONS_FACT_SHEETS.md','DIALOGUES_KO_VI.md','PERFORMANCE.md','QA.md','PROTECTED_AUDIT.md','REVIEW.html']:
 p=D/n;paths.add(str(p.relative_to(R)))
 for row in re.findall(r'(?:href|src)="([^"]+)"|\]\(([^)]+)\)',p.read_text()):
  u=next(x for x in row if x)
  if u.startswith(('http:','https:','#','data:')):continue
  target=(p.parent/urllib.parse.unquote(u.split('#')[0].split('?')[0])).resolve();assert target.is_file(),str(target);paths.add(str(target.relative_to(R)))
paths.add('docs/phase3a-npc-expansion/PHASE3A_20NPC_SOURCE_BLOCKED_REVIEW.zip')
def check(n):
 url=RAW+urllib.parse.quote(n,safe='/')
 for attempt in range(4):
  try:
   with urllib.request.urlopen(urllib.request.Request(url,method='HEAD'),timeout=60)as q:assert q.status==200;return {'file':n,'url':url,'status':q.status}
  except Exception:
   if attempt==3:raise
   time.sleep(1+attempt)
with ThreadPoolExecutor(max_workers=8)as pool:rows=list(pool.map(check,sorted(paths)))
proof=json.loads((D/'package-proof.json').read_text());url=RAW+'docs/phase3a-npc-expansion/'+proof['file'];h=hashlib.sha256();size=0
with urllib.request.urlopen(url,timeout=120)as response:
 while True:
  chunk=response.read(1024*1024)
  if not chunk:break
  size+=len(chunk);h.update(chunk)
assert size==proof['bytes']and h.hexdigest()==proof['sha256']
report={'status':'PASS','reviewCommit':commit,'reviewCheckpoint':TAG,'reviewBranch':'feature/phase3a-npc-expansion','checkedPublishedURLs':len(rows),'URLs':rows,'fullRemoteZIPDownload':{'bytes':size,'sha256':h.hexdigest(),'matchesLocal':'PASS'},'allHistoricalRemoteRefsUnchanged':len(before),'mainUnchanged':after['refs/heads/main'],'physicalDevices':'NOT TESTED','humanArtApproval':'PENDING','Phase3B':'LOCKED','actualNPCs':20,'requestedNPCs':26,'historicalNPCs':0,'verifiedRealPersonCards':0,'incompleteReason':'Official-source proxy CONNECT403,even after network grant;no fabricated source validation'};(D/'published-verification.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS',len(rows),'published URLs;full remote ZIP checksum;all',len(before),'oldrefs unchanged;main unchanged',commit)
