from pathlib import Path
import hashlib,json,subprocess,urllib.request,concurrent.futures
R=Path(__file__).resolve().parents[2];D=R/'docs/phase1b-frontback-juni';SHA='51ac4b4f20f0af2f26d1566988580d92c0612356';BASE=f'https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/{SHA}/docs/phase1b-frontback-juni/'
full=['README.md','QA.md','juni-reference-native.png','PHASE1B_FRONTBACK_JUNI_REVIEW.zip']+[f'{id}-corrected-native.png'for id in ['haneul','bomi','minjun']]+[f'juni-vs-{id}-motion.png'for id in ['haneul','bomi','minjun']]+[f'actual-comparison-{clip}.mp4'for clip in ['walk-front','walk-back','run-front','run-back']]
heads=[p.name for p in D.glob('*-phaser-native.png')]
def check(name):
 mode='GET'if name in full else'HEAD';h=hashlib.sha256();req=urllib.request.Request(BASE+name,method=mode)
 with urllib.request.urlopen(req,timeout=120)as r:
  status=r.status;mime=r.headers.get('Content-Type');count=0
  if mode=='GET':
   while b:=r.read(1024*1024):h.update(b);count+=len(b)
 assert status==200
 if mode=='GET':assert h.hexdigest()==hashlib.sha256((D/name).read_bytes()).hexdigest(),name
 return {'file':name,'url':BASE+name,'HTTP':status,'method':mode,'bytes':count if mode=='GET'else None,'byteExact':True if mode=='GET'else'HEAD only','mime':mime}
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:rows=list(pool.map(check,full+heads))
remote=dict(line.split()[::-1]for line in subprocess.check_output(['git','ls-remote','origin'],cwd=R,text=True).splitlines())
old=dict(line.split()[::-1]for line in (R/'docs/phase1/protected-remote-refs.txt').read_text().splitlines());bad=[ref for ref,sha in old.items()if remote.get(ref)!=sha];assert not bad,bad
assert remote['refs/tags/checkpoint/phase1b-frontback-juni-review-20261026^{}']==SHA
assert remote['refs/heads/main']=='33360ed1989e4db9fc3fc4e3686ca385e0b00908'
report={'immutableReviewCommit':SHA,'checkpoint':'checkpoint/phase1b-frontback-juni-review-20261026','links':rows,'protectedRemoteRefsChecked':len(old),'changedProtectedRefs':bad,'mainUnchanged':True,'deployment':'NONE','humanMotionApproval':'PENDING'}
(D/'published-verification.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS',len(rows),'HTTP200links;',len(full),'full byte-exact downloads;',len(old),'protected remote refs unchanged')
