from pathlib import Path
from urllib.request import Request,urlopen
from PIL import Image
from io import BytesIO
from zipfile import ZipFile
import json,hashlib,subprocess
R=Path(__file__).resolve().parents[1];D=R/'docs/phase1';tag='checkpoint/phase1-foundation-review-20261026';base='https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/refs/tags/'+tag+'/'
refs=lambda text:dict(line.split()[::-1]for line in text.splitlines());old=refs((D/'protected-remote-refs.txt').read_text());now=refs(subprocess.check_output(['git','ls-remote','--heads','--tags','origin'],cwd=R,text=True))
for key,value in old.items():assert now.get(key)==value,key
assert now['refs/tags/checkpoint/world-art-approved-phase1-20261026']=='a183b1a69f08571acea1a35b4d70185ad95a2257';assert now['refs/heads/archive/world-art-approved-phase1-20261026']=='a183b1a69f08571acea1a35b4d70185ad95a2257'
paths=['docs/phase1/'+n for n in ['README.md','QA.md','QA.json','VISUAL_REVIEW.md','selection-desktop.jpg','selection-mobile-landscape.jpg','PHASE1_FOUNDATION_REVIEW.zip','selection-juni-gameplay-review.mp4','preservation-qa.json','character-art-status.json','package-proof.json','package-smoke.json','palace-front-local-webgl-after-native-1x.png','station-all-webgl-after-native-1x.png','bridge-a-full-webgl-after-native-1x.png','bridge-regression/world-traversal-review.mp4','bridge-regression/body-clearance.json']]+['docs/current/PROJECT_STATE.md','docs/current/CLEANUP_MANIFEST.md','assets-src/characters/phase1/run-manifest.json'];rows=[]
for name in paths:
 p=R/name;url=base+name
 with urlopen(Request(url,headers={'User-Agent':'Codex-phase1-review-verifier'}),timeout=60)as response:assert response.status==200;data=response.read()
 assert hashlib.sha256(data).hexdigest()==hashlib.sha256(p.read_bytes()).hexdigest(),name
 if p.suffix in ['.jpg','.png']:Image.open(BytesIO(data)).verify()
 if p.suffix=='.zip':
  with ZipFile(BytesIO(data))as z:assert z.testzip()is None
 rows.append({'path':name,'url':url,'HTTP':200,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()});print(name,'PASS',flush=True)
(D/'published-verification.json').write_text(json.dumps({'files':rows,'allPriorRemoteRefsUnchanged':len(old),'mainUnchanged':now['refs/heads/main'],'artistBaselineExact':now['refs/tags/checkpoint/world-art-approved-phase1-20261026'],'phase1Acceptance':'INCOMPLETE_ROSTER','noMainMergeOrPublicDeployment':True},indent=2)+'\n')
