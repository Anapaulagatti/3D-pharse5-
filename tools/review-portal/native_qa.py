"""Inspect actual portal-build Phaser pixels against immutable approved cells."""
from pathlib import Path
from PIL import Image
import json,numpy as np
R=Path.cwd();D=R/'docs/review-portal';q=json.loads((D/'PORTAL_SMOKE.json').read_text());assert q['status']=='PASS';rows=[];images={};objects=json.loads((R/'public/assets/gate3/palace-cleanup-world/manifest.json').read_text())['objects']
for row in q['rows']:
 if 'native'not in row:continue
 a=row['native'];id=row['check'];s=a['sprite'];cx,cy=a['camera']['scroll'];assert a['matched']and a['camera']['zoom']==1 and s['scale']==[1,1]and s['sampling']==1;assert all(float(n).is_integer()for n in [s['x'],s['y'],cx,cy]);r=R/'public/assets/npcs/phase3a'/id;f=json.loads((r/'atlas.json').read_text())['frames'][a['actualFrame']]['frame'];source=np.array(Image.open(r/'atlas.png').convert('RGBA').crop((f['x'],f['y'],f['x']+96,f['y']+112)));x,y=int(s['x']-48-cx),int(s['y']-100-cy);actual=Image.open(R/'.cache/review-native'/f'{id}.png').convert('RGB').crop((x,y,x+96,y+112));actual_array=np.array(actual);diff=(source[:,:,3]==255)&np.any(actual_array!=source[:,:,:3],axis=2);owned=0
 for py,px in zip(*np.where(diff)):
  wx,wy=int(px+s['x']-48),int(py+s['y']-100);owners=[]
  for o in objects:
   if o['sortY']>s['depth']and o['x']<=wx<o['x']+o['width']and o['y']<=wy<o['y']+o['height']:
    if o['image']not in images:images[o['image']]=Image.open(R/'public'/o['image']).convert('RGBA')
    pixel=images[o['image']].getpixel((int(wx-o['x']),int(wy-o['y'])))
    if pixel[3]==255 and pixel[:3]==actual.getpixel((int(px),int(py))):owners.append(o['id'])
  assert owners,('Unexplained pixel mismatch',id,int(px),int(py));owned+=1
 rows.append({'id':id,'frame':a['actualFrame'],'opaquePixels':int((source[:,:,3]==255).sum()),'unexplainedMismatch':0,'foregroundOwnedPixels':owned,'integerNativeNearest':True})
assert len(rows)==26
(D/'NATIVE_QA.json').write_text(json.dumps({'status':'PASS','actualActors':26,'rows':rows,'physicalDevices':'NOT_TESTED'},indent=2)+'\n');print('26 native Phaser readbacks PASS')
