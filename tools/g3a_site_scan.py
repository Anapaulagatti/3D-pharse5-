"""Conservative 10px-grid site screening, not a visual approval or universal fit proof."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json
R=Path(__file__).resolve().parents[1];p=json.loads((R/'assets-src/gate25/world-plan-v1.json').read_text());W,H=p['size'];step=10
# Entire visual envelope must avoid protected source rectangles and all approved public path corridors.
mask=Image.new('L',(W,H));d=ImageDraw.Draw(mask)
for b in p['buildings']:
 x,y,w,h=b['rect'];d.rectangle((x,y,x+w-1,y+h-1),fill=255)
for f in p['facadeReserves']:
 x,y,w,h=f['rect'];d.rectangle((x,y,x+w-1,y+h-1),fill=255)
d.rectangle((640,650,2175,1673),fill=255)
for path in p['paths']:d.line([tuple(v)for v in path['points']],fill=255,width=path['width'],joint='curve')
a=np.pad((np.array(mask)>0).astype(np.int32),((1,0),(1,0))).cumsum(0).cumsum(1)
land=Image.new('L',(W,H));ld=ImageDraw.Draw(land)
for x,y,w,h in p['land']:ld.rectangle((x+16,y+16,x+w-17,y+h-17),fill=255)
l=np.pad((np.array(land)==0).astype(np.int32),((1,0),(1,0))).cumsum(0).cumsum(1)
def count(s,x,y,w,h):return int(s[y+h,x+w]-s[y,x+w]-s[y+h,x]+s[y,x])
landfits=0;clean=[]
for y in range(2400,H-442,step):
 for x in range(190,W-902,step):
  if count(l,x,y,875,442):continue
  landfits+=1
  # Native image origin contact(-27,-310), size905x763; no resizing.
  if not count(a,x-27,y-310,905,763):clean.append([x,y,875,442])
proof={'method':'Conservative 10px origin grid, contact inside approved land with16px shore inset; full905x763 visual rectangle excludes protected building/facade rectangles, native northern sample and all approved path widths; modern envelope starts south of2090','candidateContactPositionsOnLand':landfits,'zeroConflictConservativeSites':clean,'limitation':'Rectangular visual envelopes include transparent/context pixels; this does not prove no alternative exists under different visual easements. It screens clean existing-land sites only; visual approval still required.'}
(R/'docs/g3a-spatial-review/site-scan.json').write_text(json.dumps(proof,indent=2)+'\n');print(landfits,'land-valid origins;',len(clean),'clean sites')
