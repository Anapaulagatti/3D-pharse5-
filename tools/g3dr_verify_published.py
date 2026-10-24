"""Verify immutable remote evidence bytes, not merely a GitHub file-view URL."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen,Request
import json,hashlib,io
from PIL import Image
from zipfile import ZipFile
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-reconciliation';tag='checkpoint/g3d-spatial-reconciliation-review-20261024';base='https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/refs/tags/'+tag+'/'
paths=[p for p in D.glob('*-native.png')]+[D/'palace-runtime-registration-overlay.png',D/'palace-approved-graybox-native.png',D/'VISUAL_REVIEW.md',D/'VISUAL_REVIEW.html',D/'G3D_SPATIAL_RECONCILIATION_REVIEW.zip']
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
