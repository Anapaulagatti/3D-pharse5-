from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,numpy as np
R=Path(__file__).resolve().parents[1];D=R/'docs/gate25';old=json.loads((R/'assets-src/world-gate1/plan.json').read_text());new=json.loads((R/'assets-src/gate25/world-plan-v1.json').read_text())
font=lambda n:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',n)
# Planning diagram explicitly identified, never passed off as gameplay.
board=Image.new('RGB',(1300,850),'#173c49');dr=ImageDraw.Draw(board);dr.text((18,10),'VERSIONED WORKING MASTERPLAN / PLANNING DIAGRAM / not gameplay',font=font(20),fill='#f3e9d0')
for side,plan,label in [(0,old,'Immutable approved Gate1 /4096x4608'),(650,new,'Gate2.5 working V1 /4352x4864')]:
 scale=.15;origin=(side+12,80)
 def rect(r,color,outline=None):
  x,y,w,h=r;dr.rectangle((origin[0]+x*scale,origin[1]+y*scale,origin[0]+(x+w)*scale,origin[1]+(y+h)*scale),fill=color,outline=outline)
 dr.text((side+14,48),label,font=font(17),fill='#f3e9d0')
 rect([0,0,*plan['size']],'#245e70','#ffe0a0')
 for r in plan['land']:rect(r,'#547764')
 for b in plan['buildings']:rect(b['rect'],'#bba37c')
 for path in plan['paths']:
  dr.line([(origin[0]+x*scale,origin[1]+y*scale)for x,y in path['points']],fill='#d9c7a2',width=max(1,int(path['width']*scale)))
 if side:rect(new['gate2LocalizedFit']['nativeFrame'],None,'#ffbc65')
 dr.text((side+20,810),'North, mainland, SW Namsan and SE amusement stay fixed',font=font(15),fill='#f3e9d0')
board.save(D/'WORKING_MASTERPLAN.jpg',quality=89,optimize=True)
# Local exact alignment diagram at a legible scale, over native artwork and actual collision mask.
scene=json.loads((R/'public/assets/gate2/jeju25/scene.json').read_text());base=Image.new('RGBA',tuple(scene['size']),(37,83,99,255))
for g in scene['grounds']:base.alpha_composite(Image.open(R/'public/assets/gate2'/g['image']).convert('RGBA'),(g['x'],g['y']))
for e in scene.get('engineering',[]):
 draw=ImageDraw.Draw(base);color='#74877e'
 if e.get('rect'):
  x,y,w,h=e['rect'];draw.rectangle((x,y,x+w,y+h),fill=color)
 if e.get('points'):draw.line([tuple(p)for p in e['points']],fill=color,width=e.get('width',4))
mask=np.array(Image.open(R/'public/assets/gate2'/scene['mask']).convert('L'));overlay=np.zeros((*mask.shape,4),dtype=np.uint8);overlay[mask>127]=[80,245,145,95];base=Image.alpha_composite(base,Image.fromarray(overlay))
for name,box,points in [('BRIDGE_COLLISION',(650,280,1280,650),[('Mainland3160,3480',810,380),('Endpoint3180,3560',830,460)]),('FERRY_COLLISION',(80,780,1200,1110),[('Mainland2560,4100',210,1000),('Island3180,4020',830,920)])]:
 crop=base.crop(box).convert('RGB');draw=ImageDraw.Draw(crop)
 for label,x,y in points:
  x-=box[0];y-=box[1];draw.ellipse((x-7,y-7,x+7,y+7),fill='#ffcd60');draw.text((max(2,min(crop.width-220,x+10)),max(2,y-30)),label,font=font(15),fill='#ffffff',stroke_width=2,stroke_fill='#20383c')
 canvas=Image.new('RGB',(crop.width,crop.height+54),'#20383c');canvas.paste(crop,(0,54));draw=ImageDraw.Draw(canvas);draw.text((10,8),'Collision overlay / green = walkable feet / technical shore',font=font(16),fill='#f3e9d0');draw.text((10,30),'No ferry gameplay; water crossing blocked',font=font(14),fill='#f3e9d0');canvas.save(D/(name+'.jpg'),quality=87,optimize=True)
# Exact, independently checked geometry invariants.
for b in old['buildings']:
 if b['id']!='jeju-culture':assert b==next(x for x in new['buildings']if x['id']==b['id']),b['id']
assert old['land'][0]==new['land'][0];assert old['station']==new['station'];assert new['size']==[4352,4864];assert new['gate2LocalizedFit']['nativeFrame']==[3180,3200,1024,1536]
assert mask[920,830]>127 and mask[1000,210]>127
for x,y in [(520,960),(500,1400),(1900,1600)]:assert mask[y,x]==0
# Endpoint continuity using exact pixel mask, not just reservations.
for x,y in [(810,380),(830,460),(850,460)]:assert mask[y,x]>127,(x,y)
protected=json.loads((D/'protected-before.json').read_text());exceptions=['public/assets/gate2/catalog.json']
for name,h in protected.items():
 if name not in exceptions:assert hashlib.sha256((R/name).read_bytes()).hexdigest()==h,name
(D/'plan-and-preservation.json').write_text(json.dumps(dict(approvedGate1Unchanged=True,protectedFiles=len(protected),allowedChangedFiles=exceptions,northAndMainlandBuildingsUnchanged=True,stationReservationUnchanged=True,expandedCanvas=new['size'],nativeJejuFrame=new['gate2LocalizedFit']['nativeFrame'],bridgeEndpointsWalkable=True,ferryBoardingWalkable=True,seaSamplesBlocked=True,newArtCalls=0,originalArtworkAndJuniUnchanged=True),indent=2)+'\n')
print('PASS working amendment, protected source, bridge and ferry collision checks')
