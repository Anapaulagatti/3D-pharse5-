"""Freeze baseline; technical blank-site guide contains NO old station pixels."""
from pathlib import Path
from PIL import Image,ImageDraw
import copy,json,hashlib,subprocess,numpy as np
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate3/station-clean-v1';D=R/'docs/gate3-station-clean'
def wr(p,q):p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
m=json.loads((R/'public/assets/gate3/final-world/manifest.json').read_text());W,H=m['size'];g=Image.new('RGBA',m['size'])
for c in m['chunks']:g.paste(Image.open(R/'public'/c['image']),(c['x'],c['y']))
legacy=[o for o in m['objects']if o['id'].startswith('registration/station')or o['id']in ['alignment/canopy-terminal','residual/station-potted-tree']];assert len(legacy)==6
# All old station-owned ground is purged, not retained through seam masks.
plot=[2274,2140,684,673];extension=[2958,2490,38,208]
mask=Image.new('L',m['size']);dr=ImageDraw.Draw(mask)
for x,y,w,h in [plot,extension]:dr.rectangle((x,y,x+w-1,y+h-1),fill=255)
# Neutral technical placeholder only; never the final clean-site artwork.
# No old visual/ground donors are used for this engineering guide.
g.paste(Image.new('RGBA',g.size,'#b9b3a2'),(0,0),mask)
# Planning-only native vector guide, no old-art pixels copied. Existing road
# alignment/entry are mandatory; final authoring replaces these flat placeholders.
dr=ImageDraw.Draw(g);dr.rectangle((2274,2755,2957,2812),fill='#38424b')
for cy in [2753,2773,2793]:dr.rectangle((2520,cy,2666,cy+10),fill='#e9e2ce')
dr.line((2274,2753,2485,2753),fill='#d6aa45',width=3);dr.line((2710,2753,2957,2753),fill='#d6aa45',width=3)
dr.rectangle((2589,2610,2608,2744),fill='#c5ad5a')

remain=[o for o in m['objects']if o not in legacy]
for o in sorted(remain,key=lambda o:o['sortY']):g.alpha_composite(Image.open(R/'public'/o['image']).convert('RGBA'),(o['x'],o['y']))
g.crop((1920,1920,3456,2944)).save(S/'purged-authoring-guide.png');mask.save(S/'purged-ground-mask.png')
scopes=[{'id':'main-station-lot','rect':plot,'allowed':'Entire old building/source ground/forecourt/road-edge art replaced from fresh ground; preserve non-art road/curb/crosswalk coordinates','maxPixels':684*673},{'id':'old-tree-right-remnant','rect':extension,'allowed':'Remove old potted-tree/halo/shadow pixels past old source edge only','maxPixels':38*208},{'id':'old-canopy-terminal','rect':[2946,2244,82,274],'allowed':'Retire old foreground terminal only; preserve underlying correct platform','maxPixels':82*274}]
wr(S/'scope.json',{'baseline':'e935e2a / final-world','plot':plot,'origin':[1920,1920],'extraGround':extension,'regions':scopes,'legacyObjectsRemoved':legacy,'planning':{'logicalSolids':m['logicalSolids'],'entrance':[2598.5,2610],'districtReservation':[2230,2090,1160,690]},'instruction':'No old station art as authoring reference. This neutral guide is engineering only. Fresh floor then fresh station; old source files remain historical.'})
lock=S/'baseline-lock.json'
if not lock.exists():
 wr(lock,{'HEAD':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'assets':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for root in ['assets-src','public']for p in sorted((R/root).rglob('*'))if p.is_file()and'/station-clean'not in str(p)},'originalManifest':m})
for id in ['station-clean-before','station-clean-site','station-clean-world']:
 q=copy.deepcopy(m);q['id']=id;q['artStatus']='FRESH STATION REBUILD / HUMAN REVIEW PENDING';q['nativeFrames'].update({'station-all':[2680,2480],'station-facade':[2600,2470],'station-top':[2600,2250],'station-east':[2950,2480],'station-base':[2600,2735]});q['reviewEntries'].update({key:[2598.5,2760]for key in ['station-all','station-facade','station-top','station-east','station-base']});wr(R/'public/assets/gate3'/id/'manifest.json',q)
(D/'BASELINE.md').write_text('# Clean rebuild baseline\n\nLatest complete candidate `final-world` at `e935e2a`. Recoverable tag `checkpoint/g3d-before-station-clean-20261025`. New human override retires all prior station-art protection; original files/checkpoints stay immutable in history but are not active donors.\n\nMain lot2274,2140,684,673; old tree extension2958,2490,38,208; old terminal2946,2244,82,274. Same logical footprint2322.5,2380,555,210 and entrance2598.5,2610; neighbors/farm/house/Jeju/road network unchanged. Ground ownership is fresh throughout the lot, no old floor/shadows retained.\n')
print('Removed legacy registry:',[o['id']for o in legacy])
