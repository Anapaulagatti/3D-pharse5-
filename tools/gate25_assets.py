"""Register three approved native sources; derive ownership alpha and local seam foot clearance only."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[1];P=R/'public/assets/gate2';O=P/'district';D=R/'docs/gate25';S=R/'assets-src/gate25'
W,H=3184,1214
sources=[('muneum','b',0,190),('bakery','original',1488,0),('station','station',2464,267)]
ims=[];owners=[];mask=np.zeros((H,W),np.uint8);chunks=[];registration=[];objects=[]
for i,(name,id,x,y) in enumerate(sources):
 im=Image.open(P/id/'ground.png').convert('RGBA');a=np.array(im);alpha=np.full(a.shape[:2],255,np.uint8);h,w=alpha.shape
 if i:
  prev=ims[-1];px,py=sources[i-1][2:];top=max(py,y);bottom=min(py+prev.height,y+h);overlap=px+prev.width-x
  aa=np.array(prev)[top-py:bottom-py,x-px:x-px+overlap,:3].astype(float);bb=a[top-y:bottom-y,:overlap,:3].astype(float)
  cost=np.mean((aa-bb)**2,axis=2);dp=cost.copy();parents=np.zeros(cost.shape,int)
  for row in range(1,len(cost)):
   for col in range(overlap):
    lo=max(0,col-1);hi=min(overlap,col+2);pr=lo+int(np.argmin(dp[row-1,lo:hi]));parents[row,col]=pr;dp[row,col]+=dp[row-1,pr]
  cut=[int(np.argmin(dp[-1]))]
  for row in range(len(cost)-1,0,-1):cut.append(int(parents[row,cut[-1]]))
  cut.reverse()
  for row,col in enumerate(cut):alpha[top-y+row,:col]=0
  registration.append(dict(join=[sources[i-1][0],name],overlapPx=overlap,yRange=[top,bottom],ownership=cut))
 im.putalpha(Image.fromarray(alpha));im.save(O/(name+'.png'));ims.append(im);owners.append((x,y,alpha))
 own=alpha>0;part=mask[y:y+h,x:x+w];raw=np.array(Image.open(P/id/'walk.png').convert('L'));part[own]=raw[own]
 chunks.append(dict(id=name,image='district/'+name+'.png',x=x,y=y,width=w,height=h))
 sc=json.loads((P/id/'scene.json').read_text())
 for ob in sc['objects']:
  n=dict(ob,id='district-'+ob['id'],x=ob['x']+x,y=ob['y']+y,sortY=ob['sortY']+y)
  # Match the ground ownership across source boundaries so no disowned canopy is rendered twice.
  oi=Image.open(P/ob['image']).convert('RGBA');al=np.array(oi.getchannel('A'))
  for xx,yy,owner in owners[1:]:
   for iy in range(oi.height):
    wy=n['y']+iy
    if yy<=wy<yy+owner.shape[0]:
     for ix in range(oi.width):
      wx=n['x']+ix
      if xx<=wx<xx+owner.shape[1] and owner[wy-yy,wx-xx]>0:al[iy,ix]=0
  # Current sources only Muneum has foreground layers; other groups are empty.
  oi.putalpha(Image.fromarray(al));filename=n['id']+'.png';oi.save(O/filename);n['image']='district/'+filename;objects.append(n)
# Re-evaluate all foreground alpha against the final ownership stack, including future chunks.
for ob in objects:
 original=next(o for o in json.loads((P/'b/scene.json').read_text())['objects'] if 'district-'+o['id']==ob['id'])
 oi=Image.open(P/original['image']).convert('RGBA');al=np.array(oi.getchannel('A'))
 for xx,yy,owner in owners[1:]:
  for iy in range(oi.height):
   wy=ob['y']+iy
   if yy<=wy<yy+owner.shape[0]:
    for ix in range(oi.width):
     wx=ob['x']+ix
     if xx<=wx<xx+owner.shape[1] and owner[wy-yy,wx-xx]>0:al[iy,ix]=0
 oi.putalpha(Image.fromarray(al));oi.save(P/ob['image'])
# Extend the former isolated bakery's artificial map-edge clearance only over visible sidewalk.
# Source masks are immutable. Shared crossing band has no new decorative/art pixels.
draw=ImageDraw.Draw(Image.fromarray(mask));walk=Image.fromarray(mask);draw=ImageDraw.Draw(walk)
for x in [1488,2464]:draw.rectangle((x-24,778,x+48,798),fill=255)
# Conservative original bench/bollard restrictions remain; routes cross at y790, away from these.
for x,y,w,h in [(2589,743,100,43),(2939,743,115,43)]:draw.rectangle((x-8,y-8,x+w+8,y+h+8),fill=0)
# Sidewalk route at y810 avoids station benches ending y807.
walk.save(O/'walk.png')
scene=dict(id='district',label='Gate2.5 · Muneum / 오월제과 / station',size=[W,H],spawn=[1200,780],camera=[1200,610],ground='',grounds=chunks,chunkLoading=True,mask='district/walk.png',objects=objects,targets=[dict(id='muneum',x=1288,y=780,label='Muneum street'),dict(id='bakery',x=1998,y=780,label='오월제과 entrance'),dict(id='station',x=2824,y=697,label='Station threshold')],routes=[dict(id='district',points=[[1200,780],[1450,780],[1530,790],[1998,790],[2400,790],[2500,810],[2824,820],[2824,697]],width=16)],limitations='Full native image dimensions kept. Nonwalkable upper/lower areas outside source coverage are technical margins. Source sidewalk/road edge textures are not a production modular pavement kit; local seam material correction may require future authorized art.')
(O/'scene.json').write_text(json.dumps(scene,indent=2,ensure_ascii=False)+'\n')
cat=json.loads((P/'catalog.json').read_text());cat=[x for x in cat if x['id']!='district'];cat.append(dict(id='district',label=scene['label']));(P/'catalog.json').write_text(json.dumps(cat,indent=2,ensure_ascii=False)+'\n')
(S/'district-registration.json').write_text(json.dumps(dict(size=[W,H],chunks=chunks,joins=registration,sourcePixelsResampled=False,newArtworkGenerated=False,technicalMargins='Outside rectangular source coverage; never walkable; not painted extensions',localCollisionAmendment='Seam-only native sidewalk clearance rectangles, leaving original masks unchanged'),indent=2)+'\n')
# Native source proof, not gameplay; the latter must be captured from Phaser.
composite=Image.new('RGBA',(W,H),(32,56,60,255))
for im,(_,_,x,y) in zip(ims,sources):composite.alpha_composite(im,(x,y))
composite.convert('RGB').resize((1592,607)).save(D/'DISTRICT_REGISTRATION.jpg',quality=87)
print('PASS three native chunks registered; no source artwork modified/generated')
