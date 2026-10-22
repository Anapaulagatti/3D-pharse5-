"""One independent approved-asset join: Muneum street ↔ station forecourt, native pixels."""
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[1];P=R/'public/assets/gate2';O=P/'seam';S=R/'assets-src/gate2/acceptance';D=R/'docs/gate2/acceptance'
left=Image.open(P/'b/ground.png').convert('RGBA').crop((0,80,1536,800));right=Image.open(P/'station/ground.png').convert('RGBA');assert right.size==(720,720)
# Minimum-error overlap ownership: only original source pixels, no synthesized RGB,
# stretching, feather blur, recoloring or image generation.
a=np.asarray(left)[:,1488:1536,:3].astype(float);b=np.asarray(right)[:,:48,:3].astype(float);cost=np.mean((a-b)**2,axis=2);dp=cost.copy();parents=np.zeros((720,48),dtype=int)
for y in range(1,720):
 for x in range(48):
  lo=max(0,x-1);hi=min(48,x+2);prev=lo+int(np.argmin(dp[y-1,lo:hi]));parents[y,x]=prev;dp[y,x]+=dp[y-1,prev]
seam=[int(np.argmin(dp[-1]))]
for y in range(719,0,-1):seam.append(int(parents[y,seam[-1]]))
seam.reverse();alpha=np.full((720,720),255,dtype='uint8')
for y,x in enumerate(seam):alpha[y,:x]=0
right.putalpha(Image.fromarray(alpha));left.save(O/'street-native-chunk.png');right.save(O/'station-native-chunk.png')
# Register the accepted feet-clearance masks; blockers at benches remain conservative.
lm=Image.open(P/'b/walk.png').convert('L').crop((0,80,1536,800));rm=Image.open(P/'station/walk.png').convert('L');world=Image.new('L',(2208,720));world.paste(lm,(0,0));arr=np.array(world);r=np.asarray(rm);owner=alpha>0;part=arr[:,1488:2208];part[owner]=r[owner];arr[:,1488:2208]=part;world=Image.fromarray(arr)
d=ImageDraw.Draw(world)
for x,y,w,h in [(1488+125,476,100,43),(1488+475,476,115,43)]:d.rectangle((x-8,y-8,x+w+8,y+h+8),fill=0)
world.save(O/'walk.png')
bscene=json.loads((P/'b/scene.json').read_text());objects=[]
for o in bscene['objects']:
 n=dict(o,y=o['y']-80,sortY=o['sortY']-80)
 if o['x']+o['width']>1488:
  im=Image.open(P/o['image']).convert('RGBA');al=np.asarray(im.getchannel('A')).copy()
  for yy in range(im.height):
   wy=int(n['y']+yy)
   if 0<=wy<720:
    for xx in range(im.width):
     wx=int(n['x']+xx)
     if 1488<=wx<2208 and owner[wy,wx-1488]:al[yy,xx]=0
  im.putalpha(Image.fromarray(al));filename='depth-'+o['id']+'.png';im.save(O/filename);n['image']='seam/'+filename
 objects.append(n)
s=dict(id='seam',label='Join proof · Muneum ↔ station',size=[2208,720],spawn=[1288,510],camera=[1500,440],ground='',grounds=[dict(image='seam/street-native-chunk.png',x=0,y=0),dict(image='seam/station-native-chunk.png',x=1488,y=0)],mask='seam/walk.png',objects=objects,targets=[dict(id='commercial',x=1288,y=500,label='Muneum shop frontage'),dict(id='join',x=1520,y=530,label='Street / forecourt join'),dict(id='station',x=1848,y=430,label='Station entrance')],routes=[dict(id='street-to-station',points=[[1288,510],[1430,530],[1580,530],[1848,530],[1848,430]],width=42)],joinScope='Independent approved Muneum and station sources;48px minimum-error binary ownership overlap; source pixels1:1, no new art; one small connection, not full-world integration')
(O/'scene.json').write_text(json.dumps(s,indent=2,ensure_ascii=False)+'\n')
catalog=json.loads((P/'catalog.json').read_text())
for c in catalog:
 if c['id']=='seam':c['label']=s['label']
(P/'catalog.json').write_text(json.dumps(catalog,indent=2,ensure_ascii=False)+'\n')
(S/'small-join-registration.json').write_text(json.dumps(dict(sourceLeft='public/assets/gate2/b/ground.png',sourceLeftCrop=[0,80,1536,800],sourceRight='public/assets/gate2/station/ground.png',rightOrigin=[1488,0],worldSize=[2208,720],overlapWidth=48,binaryOwnershipSeam=seam,sourcePixelsResampled=False,approvedSourcePixelsModified=False,algorithm='Minimize RGB mismatch along one continuous boundary through the native48px overlap; alpha mask only; no RGB generation or feathering',limitation='One native-scale urban street/plaza join; no generalized arbitrary asset seam solver or whole-world kit claim'),indent=2)+'\n')
print('Independent approved Muneum/station join prepared; no art generated')
