"""Fetch immutable review artifacts and verify their exact bytes before publishing links."""
from pathlib import Path
from urllib.request import urlopen,Request
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from PIL import Image
from zipfile import ZipFile
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[1];D=R/'docs/g3a-forecourt-restoration';commit=subprocess.check_output(['git','rev-parse','checkpoint/g3a-native-forecourt-candidate-20261023^{}'],cwd=R,text=True).strip();base=f'https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/{commit}/docs/g3a-forecourt-restoration/'
names=['SOURCE_CURRENT_RESTORED_1X.png','before-auto-native.png','after-auto-native.png','station-with-juni-1x.png','entrance-ground-comparison-1x.png','tactile-strip-comparison-1x.png','left-planter-pavement-comparison-1x.png','right-planter-pavement-comparison-1x.png','forecourt-walk.mp4','G3A_FORECOURT_RESTORATION.zip','QA.md','README.md']
def check(n):
 url=base+n
 with urlopen(Request(url,headers={'User-Agent':'Native-forecourt-review-verification'}),timeout=90)as res:
  data=res.read();status=res.status;ctype=res.headers.get('Content-Type')
 expected=(D/n).read_bytes();assert data==expected,n
 row={'file':n,'url':url,'http':status,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'exactCommittedBytes':True,'contentType':ctype}
 if n.endswith('.png'):
  im=Image.open(BytesIO(data));row['size']=im.size;im.verify()
 if n.endswith('.zip'):
  with ZipFile(BytesIO(data))as z:assert z.testzip()is None
 return row
with ThreadPoolExecutor(max_workers=4)as pool:rows=list(pool.map(check,names))
(D/'published-links.json').write_text(json.dumps({'immutableEvidenceCommit':commit,'verified':rows,'G3B':'BLOCKED'},indent=2)+'\n')
md='# Verified direct native review links\n\nActual repair candidate, human visual approval PENDING. G3-B BLOCKED. All links below returnedHTTP200 and exactly matched the committed bytes. PNGs decoded and ZIP CRC passed. No public site was deployed.\n\n'
for r in rows:md+=f'- [{r["file"]}]({r["url"]}) — {r["bytes"]:,}bytes\n'
md+='\nRecoverable checkpoint: `checkpoint/g3a-native-forecourt-candidate-20261023` at `'+commit+'`. Prior checkpoints unchanged.\n'
(D/'NATIVE_LINKS.md').write_text(md);print('PASS',len(rows),'downloaded immutable artifacts; PNG decode and ZIP CRC; commit',commit)
