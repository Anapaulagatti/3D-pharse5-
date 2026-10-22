"""Verify published review files at an immutable review-branch commit; no deployment."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen
from urllib.parse import quote
from PIL import Image
import json,hashlib,subprocess,zipfile,io,time
R=Path(__file__).resolve().parents[1];D=R/'docs/gate25-station-planters';commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip();C=R/'.cache/gate25-station-planters/downloaded';C.mkdir(parents=True,exist_ok=True)
files=sorted(p for p in D.iterdir()if p.is_file()and p.name!='published-verification.json')
def check(p):
 path=str(p.relative_to(R));url='https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/'+commit+'/'+quote(path)
 for attempt in range(3):
  try:
   with urlopen(url,timeout=45)as response:data=response.read();status=response.status
   break
  except Exception:
   if attempt==2:raise
   time.sleep(1)
 actual=hashlib.sha256(data).hexdigest();assert actual==hashlib.sha256(p.read_bytes()).hexdigest(),path
 row=dict(path=path,url=url,status=status,bytes=len(data),sha256=actual,localEqualsRemote=True)
 if p.suffix.lower()in ['.png','.jpg']:
  with Image.open(io.BytesIO(data))as im:im.load();row['decodedDimensions']=im.size
 if p.suffix=='.mp4':
  target=C/p.name;target.write_bytes(data);info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_name,width,height','-of','json',str(target)],text=True));assert float(info['format']['duration'])>1;row['video']=info
 if p.suffix=='.zip':
  with zipfile.ZipFile(io.BytesIO(data))as z:
   assert z.testzip()is None;manifest=json.loads(z.read('MANIFEST.json'))
   for f in manifest:assert hashlib.sha256(z.read(f['path'])).hexdigest()==f['sha256'],f['path']
   row['crc']='PASS';row['manifestFiles']=len(manifest);row['manifestAllHashes']='PASS'
 return row
with ThreadPoolExecutor(max_workers=6)as pool:rows=list(pool.map(check,files))
refs=subprocess.check_output(['git','ls-remote','origin','refs/heads/main','refs/heads/art-gate/gate2-three-slices','refs/heads/art-gate/final-gate1-world','refs/tags/checkpoint/gate1-approved-planning-20261022^{}','refs/tags/checkpoint/gate25-refinement-approved-20261022','refs/tags/checkpoint/gate25-refinement-approved-20261022^{}'],cwd=R,text=True)
heads={line.split()[1]:line.split()[0]for line in refs.splitlines()};assert heads['refs/heads/main']=='33360ed1989e4db9fc3fc4e3686ca385e0b00908';assert heads['refs/heads/art-gate/final-gate1-world']==heads['refs/tags/checkpoint/gate1-approved-planning-20261022^{}']=='e0a5c0aeff1a2980042983e6091abff11b987fad';assert heads['refs/heads/art-gate/gate2-three-slices']==commit
assert heads['refs/tags/checkpoint/gate25-refinement-approved-20261022^{}']=='868aa60acce297253c555f994ecac60276a830b3'
assert heads['refs/tags/checkpoint/gate25-refinement-approved-20261022']=='529317c8afb1a23541252dbe68a9e51f38178d78'
(D/'published-verification.json').write_text(json.dumps(dict(reviewCommit=commit,filesVerified=len(rows),allBytesIdentical=True,protectedRefs=heads,files=rows,note='Raw repository file retrieval only; no public site deployment. Latest Gate2.5 is NOT fully approved; targeted planter quality awaits direct human review; physical Android Chrome/iPhone Safari remain NOT TESTED. Gate3 locked.'),indent=2)+'\n');print('PASS published review files',len(rows),'/ SHA / decoded images / actual videos / ZIP CRC + manifest / protected remote refs')
