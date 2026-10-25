"""Verify immutable remote evidence bytes, not merely a GitHub file-view URL."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen,Request
import json,hashlib,io,subprocess
from PIL import Image
from zipfile import ZipFile
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-final';tag='checkpoint/g3d-final-surgical-review-20261025';base='https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/refs/tags/'+tag+'/'
paths=list(D.glob('*.png'))+list(D.glob('*.jpg'))+[D/n for n in ['VISUAL_REVIEW.md','VISUAL_REVIEW.html','README.md','QA.md','G3D_FINAL_SURGICAL_REVIEW.zip','world-traversal-native.mp4','world-traversal-review.mp4']]
def verify(p):
 rel=str(p.relative_to(R));url=base+rel
 with urlopen(Request(url,headers={'User-Agent':'G3D-review-evidence-verification'}),timeout=180)as response:data=response.read();status=response.status
 expected=hashlib.sha256(p.read_bytes()).hexdigest();actual=hashlib.sha256(data).hexdigest();assert status==200 and expected==actual,rel
 row={'path':rel,'url':url,'HTTP':status,'bytes':len(data),'sha256':actual,'localBytesMatch':True}
 if p.suffix=='.png':
  im=Image.open(io.BytesIO(data));im.load();row['decodedSize']=list(im.size)
 if p.suffix=='.zip':
  with ZipFile(io.BytesIO(data))as z:assert z.testzip()is None;row['CRC']='PASS'
 return row
with ThreadPoolExecutor(max_workers=4)as pool:rows=list(pool.map(verify,paths))
(D/'published-verification.json').write_text(json.dumps({'immutableArtifactTag':tag,'files':rows,'status':'PASS_HTTP200_SHA256_DECODE_AND_ZIP_CRC','limits':'HTTP/hash verification is accessibility/preservation, not artistic approval. No site deployed.'},indent=2)+'\n')
print('Published evidence verified:',len(rows),'HTTP200 / SHA256; PNG decode and ZIP CRC PASS')

prior=json.loads((D/'remote-protection-before.json').read_text())['refs']
now={line.split()[1]:line.split()[0]for line in subprocess.check_output(['git','ls-remote','origin','refs/tags/*','refs/heads/main','refs/heads/art-gate/gate3-full-world'],text=True).splitlines()}
for ref,h in prior.items():
 if ref!='refs/heads/art-gate/gate3-full-world':assert now[ref]==h,ref
p=D/'published-verification.json';q=json.loads(p.read_text());q['existingRemoteProtectedRefsUnchanged']=True;q['oldProtectedRefCount']=len(prior)-1;q['mainCommit']=now['refs/heads/main'];q['reviewBranchArtifactCommit']=now['refs/heads/art-gate/gate3-full-world'];q['noMainMergeOrDeployment']=True;p.write_text(json.dumps(q,indent=2)+'\n')
