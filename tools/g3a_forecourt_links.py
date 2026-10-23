from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen
from PIL import Image
import json,hashlib,io,time
R=Path(__file__).resolve().parents[1];D=R/'docs/g3a-forecourt-audit';commit='9975319ff74fc8f60afef5a02e54797e2e43088a';base=f'https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/{commit}/docs/g3a-forecourt-audit/'
rois=['entrance-ground','tactile-strip','left-planter-pavement','right-planter-pavement'];names=[f'{name}-{phase}-1x.png'for name in rois for phase in ['before','after','original-recovery-reference']]+['NATIVE_1X_COMPARISON.png','NATIVE_RECOVERY_REFERENCE_NOT_APPLIED.png']
def fetch(name):
 for attempt in range(4):
  try:
   with urlopen(base+name,timeout=30)as r:data=r.read();status=r.status;mime=r.headers.get('content-type')
   break
  except Exception:
   if attempt==3:raise
   time.sleep(2*(attempt+1))
 assert data==(D/name).read_bytes()
 with Image.open(io.BytesIO(data))as im:size=list(im.size);im.verify()
 return {'name':name,'url':base+name,'httpStatus':status,'mime':mime,'dimensions':size,'sha256':hashlib.sha256(data).hexdigest(),'matchesCommittedBytes':True}
with ThreadPoolExecutor(max_workers=4)as pool:rows=list(pool.map(fetch,names))
(D/'published-links.json').write_text(json.dumps({'status':'PASS','commit':commit,'downloads':rows,'visualRepairApplied':False,'forecourtVisualStatus':'FAIL / OPEN'},indent=2)+'\n')
lines=['# Verified direct native1x evidence','', 'Every PNG below was downloaded from its immutable GitHub raw URL, decoded and matched to committed bytes. Before/after refers to this audit: no source repair was applied, and these pairs remain identical. Earlier native source is a reference only, not a repaired gameplay image.','', '| Area | Before audit | After audit / unchanged | Earlier source / NOT applied |','|---|---|---|---|']
for name in rois:
 lines.append(f'| {name} | [PNG]({base}{name}-before-1x.png) | [PNG]({base}{name}-after-1x.png) | [PNG]({base}{name}-original-recovery-reference-1x.png) |')
lines+=['',f'[Source/before/after native contact sheet]({base}NATIVE_1X_COMPARISON.png).',f'[Current versus earlier crisp native source — NOT applied]({base}NATIVE_RECOVERY_REFERENCE_NOT_APPLIED.png).','','[Download verification](published-links.json). Forecourt softness remains FAIL/open; G3-B blocked.']
(D/'NATIVE_LINKS.md').write_text('\n'.join(lines)+'\n');print('PASS',len(rows),'immutable native PNG downloads / exact bytes / decode')
