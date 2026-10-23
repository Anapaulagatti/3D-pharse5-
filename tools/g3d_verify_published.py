from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen
from PIL import Image
from zipfile import ZipFile
import subprocess,hashlib,json,io,time
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-recovery';commit=subprocess.check_output(['git','rev-parse','checkpoint/g3d-three-pilot-review-20261023^{}'],cwd=R,text=True).strip();base=f'https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/{commit}/docs/gate3-recovery/'
names=['README.md','G3D_SHARED_STYLE_PILOTS_REVIEW.zip']+[n+'-'+k+'-native.png'for n in ['north','south','namsan']for k in ['before','candidate']]+[n+'-comparison-review.jpg'for n in ['north','south','namsan']]
def check(name):
 error=None
 for attempt in range(3):
  try:
   with urlopen(base+name,timeout=55)as r:data=r.read();status=r.status
   assert hashlib.sha256(data).hexdigest()==hashlib.sha256((D/name).read_bytes()).hexdigest(),name
   row={'file':name,'url':base+name,'HTTP':status,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'matchesCommittedFile':True}
   if name.endswith(('.png','.jpg')):
    im=Image.open(io.BytesIO(data));row['dimensions']=list(im.size);im.verify();row['imageDecoded']=True
   if name.endswith('.zip'):
    with ZipFile(io.BytesIO(data))as z:assert z.testzip()is None;row['CRC']='PASS'
   return row
  except Exception as e:error=str(e);time.sleep(2)
 raise RuntimeError(name+': '+str(error))
with ThreadPoolExecutor(max_workers=4)as pool:rows=list(pool.map(check,names))
main=subprocess.check_output(['git','ls-remote','origin','refs/heads/main'],cwd=R,text=True).split()[0];assert main=='33360ed1989e4db9fc3fc4e3686ca385e0b00908'
(D/'published-links.json').write_text(json.dumps({'artifactCommit':commit,'rows':rows,'mainUnchanged':main,'publicSiteDeployed':False,'unifiedArtApproval':'PENDING HUMAN'},indent=2)+'\n')
(D/'NATIVE_LINKS.md').write_text('# Verified immutable G3-D review links\n\nArtifact commit: `'+commit+'`. Files fetched, byte hashes matched, images decoded and ZIP CRC checked. No public site deployment.\n\n'+'\n'.join('- ['+r['file']+']('+r['url']+')'for r in rows)+'\n\nSTOP: unified human artistic approval pending; no full-world propagation.\n')
print('Verified',len(rows),'immutable artifacts; main unchanged')
