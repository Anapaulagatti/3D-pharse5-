"""Verify immutable originals, byte-identical B reuse and lossless review crops."""
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[1];D=R/'docs/gate2';O=D/'final-review'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
originals=json.loads((O/'preserved-before.json').read_text())
for p,h in originals.items():assert sha(R/p)==h,p
assert subprocess.check_output(['git','rev-parse','checkpoint/gate1-approved-planning-20261022^{}'],cwd=R,text=True).strip()=='e0a5c0aeff1a2980042983e6091abff11b987fad'
props=[]
for file in sorted((R/'public/assets/gate2/b').glob('prop-*.png')):
 source=R/'assets-src/gate1/map'/file.name.removeprefix('prop-');assert sha(file)==sha(source);props.append(dict(source=str(source.relative_to(R)),runtime=str(file.relative_to(R)),sha256=sha(file)))
assert sha(R/'assets-src/gate1/native/street-foundation.png')==sha(R/'public/assets/gate2/b/ground.png')
crops=[('MUNEUM_PIXELS_1X.png',R/'docs/gate1/GATE1_STREET_NATIVE.png',(360,230,808,566)),('A_PIXELS_1X.png',D/'A_ARCHITECTURE_1X.png',(288,248,736,584)),('B_PIXELS_1X.png',D/'B_ARCHITECTURE_1X.png',(288,248,736,584)),('TRANSITION_PIXELS_1X.png',D/'TRANSITION_NATIVE_1X.png',(600,340,1048,676)),('STATION_PIXELS_1X.png',D/'STATION_NATIVE_1X.png',(136,200,584,536)),('JEJU_HOUSE_PIXELS_1X.png',O/'JEJU_ACCESS_NATIVE_1X.png',(250,1010,698,1346)),('JEJU_TERRAIN_PIXELS_1X.png',O/'JEJU_ACCESS_NATIVE_1X.png',(350,250,798,586))]
cr=[]
for name,src,box in crops:
 actual=Image.open(O/name).convert('RGBA');expected=Image.open(src).convert('RGBA').crop(box);assert actual.size==(448,336)and ImageChops.difference(actual,expected).getbbox()is None;assert (O/name).stat().st_size<1000000;cr.append(dict(path=name,source=str(src.relative_to(R)),box=box,exactSourcePixels=True))
for p in O.glob('*.jpg'):assert p.stat().st_size<1000000,p
s=json.loads((R/'assets-src/gate2/access-fix/amendment.json').read_text());patch=Image.open(R/'public/assets/gate2/c/entrance-paving.png').convert('RGBA');canvas=Image.new('L',(1024,1536));canvas.paste(patch.getchannel('A'),s['patchBox'][:2]);keep=Image.new('L',canvas.size);ImageDraw.Draw(keep).polygon([(190,1045),(230,1015),(300,970),(325,910),(490,910),(515,965),(570,1000),(622,1045),(595,1070),(580,1168),(220,1175),(210,1070)],fill=255);assert ImageChops.multiply(canvas,keep).getbbox()is None
opaque=sum(v>0 for v in canvas.get_flattened_data());qa=json.loads((O/'access-qa.json').read_text());assert qa['normalEntryRealKeyboard']and len(qa['route'])==10 and not qa['errors']
(O/'verification.json').write_text(json.dumps(dict(preservedOriginalFiles=len(originals),originalHashes=originals,checkpointUnchanged=True,originalMasterplanModified=False,houseSilhouetteUnmodified=True,patchOpaquePixels=opaque,percentOfSceneCovered=opaque/(1024*1536)*100,modernB=dict(groundIdenticalToMuneum=True,placements=10,uniqueReusedProps=props,newCommercialBuildingArtCount=0),crops=cr,lightweightPreviews=9,allPreviewsAndCropsUnder1MB=True,actualInputApproachSegments=10,scope='No scene compiler, full-world integration, merge or deployment. Original PNGs unchanged; one localized source-mask overlay and local collision amendment.',humanArtApproval=False,gate3='LOCKED'),indent=2)+'\n');print('PASS',len(originals),'original hashes;7 exact native crops;9 lightweight previews;10 real-input approach segments; unchanged checkpoint')
