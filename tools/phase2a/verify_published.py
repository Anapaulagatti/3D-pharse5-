from pathlib import Path
import hashlib,json,subprocess,urllib.request,concurrent.futures
R=Path(__file__).resolve().parents[2];D=R/'docs/phase2a';TAG='checkpoint/phase2a-character-studio-review-20261026'
SHA=subprocess.check_output(['git','rev-parse',TAG+'^{}'],cwd=R,text=True).strip();BASE=f'https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/{SHA}/docs/phase2a/'
full=['README.md','QA.md','six-original-appearances-native.png','PHASE2A_CHARACTER_STUDIO_REVIEW.zip','catalog-1-native.png','catalog-2-native.png','mobile-landscape-studio-browser.jpg']+[p.name for p in D.glob('*-actual-gameplay.mp4')]
heads=[p.name for p in D.glob('*-phaser-native.png')]+['custom-ara-webgl-native.png']
def check(name):
    mode='GET'if name in full else'HEAD';h=hashlib.sha256();count=0
    with urllib.request.urlopen(urllib.request.Request(BASE+name,method=mode),timeout=180)as r:
        status=r.status;mime=r.headers.get('Content-Type')
        if mode=='GET':
            while b:=r.read(1024*1024):h.update(b);count+=len(b)
    assert status==200
    if mode=='GET':assert h.hexdigest()==hashlib.sha256((D/name).read_bytes()).hexdigest(),name
    return {'file':name,'url':BASE+name,'HTTP':status,'method':mode,'bytes':count if mode=='GET'else None,'byteExact':True if mode=='GET'else'HEAD only','mime':mime}
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:rows=list(pool.map(check,full+heads))
remote=dict(line.split()[::-1]for line in subprocess.check_output(['git','ls-remote','origin'],cwd=R,text=True).splitlines());old=dict(line.split()[::-1]for line in (R/'docs/phase1/protected-remote-refs.txt').read_text().splitlines());bad=[ref for ref,sha in old.items()if remote.get(ref)!=sha];assert not bad,bad
approved='51ac4b4f20f0af2f26d1566988580d92c0612356'
assert remote['refs/tags/checkpoint/phase1b-frontback-juni-review-20261026^{}']==approved
assert remote['refs/tags/checkpoint/phase1b-four-characters-approved-20261026^{}']==approved
assert remote['refs/heads/main']=='33360ed1989e4db9fc3fc4e3686ca385e0b00908'
assert remote['refs/heads/feature/phase1-character-foundation']==subprocess.check_output(['git','rev-parse','feature/phase1-character-foundation'],cwd=R,text=True).strip()
report={'immutableReviewCommit':SHA,'checkpoint':TAG,'links':rows,'protectedRemoteRefsChecked':len(old),'changedProtectedRefs':bad,'mainUnchanged':True,'originalPhase1FeatureUnchanged':True,'approvedOriginalFour':approved,'deployment':'NONE','humanPhase2AArtApproval':'PENDING'}
(D/'published-verification.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS',len(rows),'HTTP200links;',len(full),'full byte-exact downloads;',len(old),'historical refs unchanged')
