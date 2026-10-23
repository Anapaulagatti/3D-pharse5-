from pathlib import Path
from urllib.request import urlopen,Request
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from zipfile import ZipFile
from PIL import Image
import json,hashlib,subprocess
R=Path(__file__).resolve().parents[1];D=R/'docs/g3a-controlled-finalization';sha=subprocess.check_output(['git','rev-parse','checkpoint/g3a-working-v3-review-20261023^{}'],cwd=R,text=True).strip();base=f'https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/{sha}/'
paths=['assets-src/gate3/production-plan-v3-working.json']+['docs/g3a-controlled-finalization/'+n for n in ['README.md','PLAN_DIFF.md','plan-diff.json','route-validation.json','protected-assets.json','WORKING_V3_PLANNING_BOARD.png','PLATFORM_BEFORE_AFTER_1X.png','PLATFORM_OWNERSHIP_OVERLAY.png','before-station-native.png','after-station-native.png','platform-traversal.mp4','G3A_WORKING_V3_REVIEW.zip']]
def check(p):
 with urlopen(Request(base+p,headers={'User-Agent':'G3-A-native-review-verification'}),timeout=90)as r:data=r.read();status=r.status
 assert data==(R/p).read_bytes(),p
 v={'path':p,'url':base+p,'http':status,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'matchesCommittedBytes':True}
 if p.endswith('.png'):
  im=Image.open(BytesIO(data));v['size']=im.size;im.verify()
 if p.endswith('.zip'):
  with ZipFile(BytesIO(data))as z:assert z.testzip()is None
 return v
with ThreadPoolExecutor(max_workers=4)as pool:rows=list(pool.map(check,paths))
(D/'published-links.json').write_text(json.dumps({'evidenceCommit':sha,'verified':rows,'finalG3A':'PENDING','stationTransfer':'BLOCKED','G3B':'BLOCKED'},indent=2)+'\n')
text='# Verified direct review downloads\n\nAll artifacts below were downloaded from immutable commit URLs and matched the committed bytes. PNG decoding and ZIP CRC passed. Final G3-A pending, station transfer BLOCKED, G3-B BLOCKED.\n\n'
for row in rows:text+=f'- [{Path(row["path"]).name}]({row["url"]}) — HTTP {row["http"]}, {row["bytes"]:,} bytes\n'
text+='\nReview checkpoint: `checkpoint/g3a-working-v3-review-20261023` at `'+sha+'`. The protected station-forecourt approval checkpoint and all earlier tags remain unchanged.\n';(D/'NATIVE_LINKS.md').write_text(text);print('PASS',len(rows),'downloaded immutable review artifacts:',sha)
