from pathlib import Path
from urllib.request import urlopen,Request
from zipfile import ZipFile
from io import BytesIO
from PIL import Image
import subprocess,hashlib,json
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-palace-cleanup';S=R/'assets-src/gate3/palace-cleanup-v1';tag='checkpoint/g3d-palace-cleanup-review-20261025';base='https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/refs/tags/'+tag+'/'
old=dict(line.split()[::-1]for line in(S/'protected-remote-refs.txt').read_text().splitlines());now=dict(line.split()[::-1]for line in subprocess.check_output(['git','ls-remote','--heads','--tags','origin'],cwd=R,text=True).splitlines());protected={k:v for k,v in old.items()if k!='refs/heads/art-gate/gate3-full-world'}
for ref,sha in protected.items():assert now.get(ref)==sha,ref
names=['README.md','QA.md','VISUAL_REVIEW.md','VISUAL_REVIEW.html','technical-qa.json','scope-and-collision.json','native-render-qa.json','protected-hashes.json','body-clearance.json','movement-report.json','PALACE_CLEANUP_REVIEW.zip','combined-palace-after-native-1x.png','combined-palace-review.jpg','world-traversal-review.mp4']+[f'{k}-{p}-native-1x.png'for k in ['axis','right-access','facade']for p in ['before','after']]+[f'{k}-before-after-native-board.png'for k in ['axis','right-access','facade']];rows=[]
for n in names:
 p=D/n;url=base+str(p.relative_to(R));req=Request(url,headers={'User-Agent':'Codex-private-review-link-check'})
 with urlopen(req,timeout=60)as response:assert response.status==200;data=response.read()
 assert hashlib.sha256(data).hexdigest()==hashlib.sha256(p.read_bytes()).hexdigest(),n
 if p.suffix=='.png':Image.open(BytesIO(data)).verify()
 if p.suffix=='.zip':
  with ZipFile(BytesIO(data))as z:assert z.testzip()is None
 rows.append({'file':n,'url':url,'HTTP':200,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()});print(n,'PASS')
(D/'published-verification.json').write_text(json.dumps({'files':rows,'protectedPriorRemoteRefsUnchanged':len(protected),'mainUnchanged':now['refs/heads/main'],'noMainMergeOrDeployment':True,'artApproval':'PENDING HUMAN'},indent=2)+'\n')
