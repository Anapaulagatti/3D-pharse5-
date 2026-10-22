"""Read-only verification of review downloads at an immutable production-source commit."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from zipfile import ZipFile
from PIL import Image
import json,hashlib,io,urllib.request,subprocess,tempfile
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3a';commit=subprocess.check_output(['git','rev-parse','checkpoint/gate3a-foundation-review-20261022^{}'],cwd=R,text=True).strip()
base=f'https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/{commit}/docs/gate3a/'
manifest=json.loads((D/'ARTIFACT_SHA256.json').read_text())
def verify(item):
 name,want=item
 with urllib.request.urlopen(base+name,timeout=120) as response:data=response.read()
 h=hashlib.sha256(data).hexdigest();assert h==want,name
 row={'file':name,'bytes':len(data),'sha256':h,'status':'PASS'}
 if name.endswith(('.png','.jpg')):
  with Image.open(io.BytesIO(data)) as im:row['dimensions']=im.size;im.verify()
 if name.endswith('.zip'):
  with ZipFile(io.BytesIO(data)) as z:
   assert z.testzip() is None
   checks=json.loads(z.read('PACKAGE_SHA256.json'))
   for f,v in checks.items():assert hashlib.sha256(z.read(f)).hexdigest()==v,f
   assert hashlib.sha256(z.read('approved-prototype/GATE25_APPROVED.zip')).hexdigest()==json.loads((D/'package-proof.json').read_text())['originalPrototypeSha256']
   row['archiveCRC']='PASS';row['packageFilesSha256']='PASS';row['approvedNestedPrototype']='PASS'
 if name.endswith('.mp4'):
  with tempfile.NamedTemporaryFile(suffix='.mp4',dir='/tmp') as t:
   t.write(data);t.flush();row['video']=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_name,width,height','-of','json',t.name]))
 return row
with ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(verify,manifest.items()))
refnames=['refs/heads/main','refs/heads/art-gate/gate2-three-slices','refs/heads/art-gate/final-gate1-world','refs/heads/art-gate/gate3-full-world','refs/tags/checkpoint/gate25-final-approved-20261022^{}','refs/tags/checkpoint/gate25-refinement-approved-20261022^{}','refs/tags/checkpoint/gate1-approved-planning-20261022^{}','refs/tags/checkpoint/gate3a-foundation-review-20261022^{}']
refs=dict(line.split()[::-1] for line in subprocess.check_output(['git','ls-remote','origin',*refnames],cwd=R,text=True).splitlines())
assert refs[refnames[0]]=='33360ed1989e4db9fc3fc4e3686ca385e0b00908'
assert refs[refnames[1]]=='01f4f954771595061d31cf2e8f53d49ce52910a0'
assert refs[refnames[2]]=='e0a5c0aeff1a2980042983e6091abff11b987fad'
assert refs[refnames[4]]==refs[refnames[1]]
assert refs[refnames[5]]=='868aa60acce297253c555f994ecac60276a830b3'
assert refs[refnames[6]]==refs[refnames[2]]
assert refs[refnames[7]]==commit
(D/'published-verification.json').write_text(json.dumps({'verifiedCommit':commit,'baseUrl':base,'downloadedArtifacts':rows,'remoteRefs':refs,'mainMerged':False,'publicSiteDeployed':False},indent=2)+'\n')
print('Verified immutable downloads:',len(rows),'commit:',commit)
