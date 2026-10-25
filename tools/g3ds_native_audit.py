"""Actual Phaser native ground readback and matched out-of-scope frame comparison."""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-final'
def rd(p):return json.loads((R/p).read_text())
cap=rd('docs/gate3-final/native-captures.json');assert not cap['errors'];cache={};ground={};regions=rd('docs/gate3-final/REGION_TARGETS.json')['regions']
for row in cap['rows']:
 id=row['scene']
 if id not in cache:
  m=rd('public/assets/gate3/'+id+'/manifest.json');cache[id]=m;g=Image.new('RGBA',m['size'])
  for c in m['chunks']:g.paste(Image.open(R/'public'/c['image']),(c['x'],c['y']))
  ground[id]=g
result=[];total=0
for row in cap['rows']:
 a=row['audit'];s=row['state'];cam=a['camera'];assert cam['zoom']==1,row['name'];sx,sy=cam['scroll'];assert sx==round(sx)and sy==round(sy);sx,sy=round(sx),round(sy);shot=Image.open(D/(row['name']+'.png')).convert('RGB');w,h=shot.size;expected=ground[row['scene']].crop((sx,sy,sx+w,sy+h)).convert('RGB');eligible=np.ones((h,w),bool)
 # Whole actual foreground object masks, not arbitrary broad crop exclusions.
 for layer in a['layers']:
  if not layer['key'].startswith('f/')or not layer['visible']or layer['alpha']<=0:continue
  o=next(o for o in cache[row['scene']]['objects']if 'f/'+o['id']==layer['key']);assert layer['scale']==[1,1];assert all(float(v).is_integer()for v in layer['position']);assert layer['scaleMode']==1
  x,y=layer['position'];im=Image.open(R/'public'/o['image']).convert('RGBA');mask=im.getchannel('A');lx=max(sx,int(x));ly=max(sy,int(y));rx=min(sx+w,int(x)+im.width);ry=min(sy+h,int(y)+im.height)
  if lx<rx and ly<ry:eligible[ly-sy:ry-sy,lx-sx:rx-sx]&=np.array(mask.crop((lx-x,ly-y,rx-x,ry-y)))==0
 cx,cy=round(s['x'])-sx,round(s['y'])-sy;x1=max(0,cx-50);x2=min(w,cx+50);y1=max(0,cy-102);y2=min(h,cy+14);eligible[y1:y2,x1:x2]=False
 diff=np.any(np.array(shot)!=np.array(expected),2)&eligible;assert not np.any(diff),(row['name'],int(diff.sum()));total+=int(eligible.sum());result.append({'frame':row['name'],'eligibleNativeGroundPixels':int(eligible.sum()),'mismatchPixels':int(diff.sum()),'zoom':1,'integerCamera':True,'nativeForegroundScale':True,'nearest':True})
pairs=[]
for after in [r for r in cap['rows']if r['phase']in ['after','station-candidate','station-ground']]:
 before=next(r for r in cap['rows']if r['phase']=='before'and r['entry']==after['entry']);assert after['audit']['camera']==before['audit']['camera'],after['name'];assert [after['state'][k]for k in ['x','y']]==[before['state'][k]for k in ['x','y']]
 a=Image.open(D/(before['name']+'.png')).convert('RGB');b=Image.open(D/(after['name']+'.png')).convert('RGB');w,h=a.size;sx,sy=map(round,after['audit']['camera']['scroll']);allow=Image.new('L',(w,h));dr=ImageDraw.Draw(allow)
 for q in regions:
  x,y,rw,rh=q['rect'];dr.rectangle((x-sx,y-sy,x+rw-1-sx,y+rh-1-sy),fill=255)
 for row in [before,after]:
  cx,cy=round(row['state']['x'])-sx,round(row['state']['y'])-sy;dr.rectangle((cx-50,cy-102,cx+50,cy+14),fill=255)
 diff=np.any(np.array(a)!=np.array(b),2);outside=diff&(np.array(allow)==0);assert not np.any(outside),(after['name'],int(outside.sum()));pairs.append({'before':before['name'],'candidate':after['name'],'cameraAndReviewPose':'EXACT MATCH','unexpectedOutsideScopePixels':0,'dynamicActorExcluded':'96x112 native sprite plus2px guard only'})
(D/'native-render-qa.json').write_text(json.dumps({'status':'PASS','frames':result,'pairs':pairs,'eligiblePixels':total,'nativePixelMismatches':0,'outOfScopeNativeFramePixels':0,'sourcePivotPolicy':'Original station anchor.5 unchanged; isolated600x423 candidate image pivot32.5,15 expresses native crop translation with exact integer raster origin2281,2181. No source resampling.','physicalDevices':'NOT TESTED','artAcceptance':'PENDING HUMAN'},indent=2)+'\n');print('Native Phaser PASS',len(result),'frames',len(pairs),'matched pairs',total,'pixels;0 mismatches/out-of-scope')
