"""Read-only published-review verification; no site deployment."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen
from PIL import Image
import subprocess,hashlib,json,io,zipfile
R=Path(__file__).resolve().parents[1];D=R/'docs/gate2';ref=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip();base=f'https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/{ref}/docs/gate2/'
files=['GATE2_REVIEW.md','MUNEUM_SIDE_BY_SIDE_1X.png','TRANSITION_NATIVE_1X.png','STATION_NATIVE_1X.png']+[f'{id}_{kind}'for id in ['A','B','C']for kind in ['NATIVE_1X.png','PLAYABLE.zip','GAMEPLAY.mp4']]
def check(name):
 with urlopen(base+name,timeout=60)as r:status=r.status;data=r.read()
 local=(D/name).read_bytes();assert status==200 and hashlib.sha256(data).digest()==hashlib.sha256(local).digest(),name
 row=dict(path='docs/gate2/'+name,httpStatus=status,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),matchesCommittedFile=True,url=base+name)
 if name.endswith('.png'):
  with Image.open(io.BytesIO(data))as im:row['decodedSize']=im.size;im.verify()
 if name.endswith('.zip'):
  with zipfile.ZipFile(io.BytesIO(data))as z:assert z.testzip()is None;row['zipCRC']='PASS'
 print(name,'PASS',flush=True);return row
with ThreadPoolExecutor(max_workers=3)as pool:rows=list(pool.map(check,files))
refs=subprocess.check_output(['git','ls-remote','origin','refs/heads/main','refs/heads/art-gate/final-gate1-world','refs/heads/art-gate/gate2-three-slices'],cwd=R,text=True)
assert '33360ed1989e4db9fc3fc4e3686ca385e0b00908\trefs/heads/main'in refs
assert 'e0a5c0aeff1a2980042983e6091abff11b987fad\trefs/heads/art-gate/final-gate1-world'in refs
(D/'published-verification.json').write_text(json.dumps(dict(reviewCommit=ref,verification='Independent raw GitHub GET + SHA256; PNG decode; ZIP CRC. Actual local gameplay MP4 hashes match published bytes.',files=rows,remoteRefs=refs,gate3='LOCKED',merged=False,deployed=False),indent=2)+'\n')
