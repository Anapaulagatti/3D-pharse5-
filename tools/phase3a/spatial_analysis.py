from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json
R=Path(__file__).resolve().parents[2];m=json.loads((R/'public/assets/gate3/palace-cleanup-world/manifest.json').read_text());w,h=m['size'];a=np.zeros((h,w),np.uint8)
for c in m['chunks']:a[c['y']:c['y']+c['height'],c['x']:c['x']+c['width']]=np.fromfile(R/'public'/c['mask'],dtype=np.uint8).reshape(c['height'],c['width'])
for s in m['logicalSolids']:
 x,y,ww,hh=s['rect'];a[round(y):round(y+hh),round(x):round(x+ww)]=0
pts={'seoyeon':[2190,940],'daehyun':[1880,960],'minseo':[610,2610],'jiho':[1215,2610],'eunji':[2440,2660],'junho':[2810,2680],'harin':[3960,4120],'seojun':[3770,4400],'nayeon':[570,550],'cheolsu':[500,810],'yejin':[1510,3260],'sungmin':[2320,3280],'donghae':[1630,3860],'soobin':[2840,3760]}
def ok(x,y):return bool((a[y-4:y+5,x-8:x+9]>127).all())
for id,(x,y)in pts.items():
 candidates=[(dx*dx+dy*dy,dx,dy)for dx in range(-100,101,2)for dy in range(-80,81,2)if ok(x+dx,y+dy)];v=min(candidates)if candidates else None;print(id,'target',[x,y],'clear',ok(x,y),'nearest',None if not v else[x+v[1],y+v[2]])
# Native SOURCE-only views; visualization is not gameplay evidence.
for label,cx,cy in [('palace',2050,950),('retail',950,2620),('station',2620,2650),('jeju',3800,4280),('farm',650,550),('namsan',1450,3200),('amusement',2400,3200),('harbor',1670,3820),('ferry',2750,3720)]:
 box=(cx-400,cy-250,cx+400,cy+250);im=Image.new('RGBA',(800,500))
 for c in m['chunks']:
  if c['x']<box[2]and c['x']+c['width']>box[0]and c['y']<box[3]and c['y']+c['height']>box[1]:im.alpha_composite(Image.open(R/'public'/c['image']).convert('RGBA'),(c['x']-box[0],c['y']-box[1]))
 for o in sorted(m['objects'],key=lambda o:o['sortY']):
  if o['x']<box[2]and o['x']+o['width']>box[0]and o['y']<box[3]and o['y']+o['height']>box[1]:im.alpha_composite(Image.open(R/'public'/o['image']).convert('RGBA'),(round(o['x'])-box[0],round(o['y'])-box[1]))
 d=ImageDraw.Draw(im)
 for id,(x,y)in pts.items():
  if box[0]<x<box[2]and box[1]<y<box[3]:d.ellipse((x-box[0]-8,y-box[1]-8,x-box[0]+8,y-box[1]+8),outline='red',width=2);d.text((x-box[0]+10,y-box[1]),id,fill='red')
 im.save('/tmp/phase3a-'+label+'-source-placement.png')
