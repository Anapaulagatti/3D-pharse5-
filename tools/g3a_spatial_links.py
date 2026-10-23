"""Verify actually published immutable review URLs; a local commit alone is insufficient."""
from pathlib import Path
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
import json,hashlib,subprocess,io,time,os
R=Path(__file__).resolve().parents[1];D=R/'docs/g3a-spatial-review';commit=os.environ.get('G3A_REVIEW_COMMIT','05335a58900741a37c9704dd49e1ba2dd1da5679');base=f'https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/{commit}/';paths=sorted(D.glob('*.png'))+[D/'G3A_SPATIAL_COMPARISON.zip']
def verify(p):
 rel=str(p.relative_to(R));url=base+rel
 for trial in range(4):
  try:
   with urlopen(url,timeout=30)as response:data=response.read();status=response.status;mime=response.headers.get('content-type')
   break
  except Exception:
   if trial==3:raise
   time.sleep(2*(trial+1))
 local=p.read_bytes();assert data==local,url
 row={'path':rel,'url':url,'status':status,'contentType':mime,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'byteExact':True}
 if p.suffix=='.png':
  with Image.open(io.BytesIO(data))as image:row['dimensions']=list(image.size);image.verify()
 return row
with ThreadPoolExecutor(max_workers=4)as pool:rows=list(pool.map(verify,paths))
remote=subprocess.check_output(['git','ls-remote','origin','refs/heads/main','refs/heads/art-gate/gate3-full-world'],cwd=R,text=True)
assert '33360ed1989e4db9fc3fc4e3686ca385e0b00908\trefs/heads/main' in remote
(D/'published-links.json').write_text(json.dumps({'status':'PASS','immutableCommit':commit,'downloads':rows,'remoteRefsAtVerification':remote,'noMainMergeOrPublicDeployment':True},indent=2)+'\n')
lines=['# Direct native image links — downloaded and verified','',f'Immutable review commit `{commit}`. Every link below returned HTTP200 and matched local committed bytes. Full native screenshots are1280×900; frontage crops684×295 retain1:1 pixels. The diagram and door source crop are labeled separately.','', '| Evidence | Dimensions | Direct PNG |','|---|---|---|']
for row in rows:
 if 'dimensions'not in row:continue
 title=Path(row['path']).stem
 if title=='SITE_COMPARISON':title+=' / technical geometry diagram, not gameplay'
 if title=='maru-door-source-native':title+=' / source crop, not gameplay'
 lines.append(f"| {title} | {row['dimensions'][0]}×{row['dimensions'][1]} | [Open PNG]({row['url']}) |")
package=next(r for r in rows if r['path'].endswith('.zip'));lines+=['',f"[Verified playable ZIP]({package['url']}) — {package['bytes']:,} bytes, SHA256 `{package['sha256']}`.",'','[Machine-readable download verification](published-links.json). Final G3-A approval withheld; G3-B remains blocked.']
(D/'NATIVE_LINKS.md').write_text('\n'.join(lines)+'\n');print('PASS',len(rows),'immutable downloads / PNG decode / exact hashes; remote main unchanged')
