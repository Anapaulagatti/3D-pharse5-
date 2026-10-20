"""Offline final-map lock: exact geometry/art/coast plus pixel-locality checks.

Pillow and stdlib only. Does not author artwork or require Forge/NumPy/Git.
"""
from pathlib import Path
from PIL import Image, ImageChops
import hashlib
import json

R=Path(__file__).resolve().parents[1]
S=R/'assets-src/final-map-lock'
P=R/'assets-src/v6-restructure/map'

def read(p):return json.loads(p.read_text())
def sha(p):
    with p.open('rb')as f:return hashlib.file_digest(f,'sha256').hexdigest()
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()

proof=read(S/'preservation.json');receipt=read(S/'processing.json')
bundle=read(P/'outdoor-bundle.json')
for key,expected in proof['geometryHashes'].items():
    assert digest(bundle[key])==expected,('Approved world/architecture/physics changed',key)
for name,expected in proof['files'].items():
    assert sha(R/name)==expected,('Approved art/runtime changed',name)
assert sha(P/'land-mask.png')==proof['landHash']
assert sha(P/'walk-mask.png')==proof['walkHash']
assert sha(R/'assets-src/v6-path-fix/path-network.json')==proof['priorPathSpecSha256']
assert sha(R/'assets-src/v6-path-fix/edit-mask.png')==proof['priorPathEditMaskSha256']
assert receipt['inputRGBSha256']==proof['baselineGroundRGBSha256'],'Polish must start from the exact approved palette-finished ground'
ground=Image.open(P/'ground-native.png').convert('RGB')
mask=Image.open(S/'edit-mask.png').convert('L')
assert ground.size==mask.size==(4352,5312)
assert mask.crop((0,0,4352,2240)).getbbox()is None
assert ImageChops.subtract(mask,Image.open(R/'assets-src/v6-path-fix/edit-mask.png').convert('L')).getbbox()is None
bits=mask.tobytes();pixels=ground.tobytes();assert set(bits)<={0,255}
changed=bits.count(255)
assert changed==receipt['changedPixels'] and 0<changed<4352*5312*.08
assert hashlib.sha256(pixels).hexdigest()==receipt['outputRGBSha256']
outside=hashlib.sha256()
for y in range(5312):
    row=bits[y*4352:(y+1)*4352];pos=0
    while pos<4352:
        start=row.find(b'\0',pos)
        if start<0:break
        end=row.find(b'\xff',start)
        if end<0:end=4352
        outside.update(pixels[(y*4352+start)*3:(y*4352+end)*3]);pos=end
assert outside.hexdigest()==receipt['outsideEditMaskRGBSha256'],'Unapproved ground pixel changed'
assert receipt['resampling']=='none'
report={'status':'PASS','baseline':proof['baselineCommit'],'world':[4352,5312],'placementsExact':len(bundle['objects']),'collisionRectanglesExact':len(bundle['collision']['solids']),'originalPropImagesExact':len(bundle['props']),'protectedRuntimeFiles':len(proof['files']),'routeNetworkExact':True,'coastAndWalkMasksExact':True,'northernGroundExact':True,'outsideSurgicalMaskExact':True,'changedGroundPixels':changed,'worldFraction':changed/(4352*5312),'resampling':'none','geometrySectionsExact':list(proof['geometryHashes'])}
out=R/'docs/final-map-lock/quality/preservation.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
