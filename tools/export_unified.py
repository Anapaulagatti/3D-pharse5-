"""Original integer-raster pixel art. No external game pixels, images or paid APIs."""
from pathlib import Path
from PIL import Image, ImageDraw
import math,json,hashlib,random,shutil
R=Path(__file__).resolve().parents[1];S=R/'assets-src/unified-v4';O=R/'public-unified/assets/unified-v4'
S.mkdir(parents=True,exist_ok=True);O.mkdir(parents=True,exist_ok=True)
P={'ink':'#303945','deep':'#263e43','roof0':'#303c53','roof1':'#435875','roof2':'#657c94','roof3':'#91a4ae','wood0':'#533d3c','wood1':'#805643','wood2':'#ad7950','wood3':'#d6a367','cream0':'#b8b79a','cream1':'#ddd2ac','cream2':'#f4e6ba','stone0':'#686f70','stone1':'#88918c','stone2':'#a8ada0','stone3':'#c7c7ae','green0':'#354e42','green1':'#48694a','green2':'#698b50','green3':'#93b360','grass':'#79935f','grass2':'#839d68','grass3':'#708a59','jade0':'#345b61','jade1':'#4c8180','jade2':'#7bb1a1','jade3':'#bad2af','coral0':'#9d5651','coral1':'#ca7865','coral2':'#e5a078','skin0':'#bd8166','skin1':'#e7ad80','skin2':'#f5c89b','hair0':'#343440','hair1':'#51414b','hair2':'#785458','gold':'#e6bf73','white':'#f4e6cc','flower':'#df9f9b'}
def col(v):return P.get(v,v)
def canvas(w,h):return Image.new('RGBA',(w,h))
def rect(d,b,c):d.rectangle(tuple(map(int,b)),fill=col(c))
def poly(d,p,c):d.polygon([(int(x),int(y)) for x,y in p],fill=col(c))
def line(d,p,c,w=1):d.line([(int(x),int(y)) for x,y in p],fill=col(c),width=w)
def save(im,name):
 im.save(S/(name+'.png'));im.save(O/(name+'.png'))
 return im
rng=random.Random(4004)
# Full native pixel tiles: ground variation, mason joints and discrete cluster texture.
tiles=[]
for k in range(16):
 im=canvas(32,32);d=ImageDraw.Draw(im)
 if k<4:
  rect(d,(0,0,31,31),'grass' if k%2==0 else 'grass2')
  for j in range(19):
   x=rng.randrange(1,30);y=rng.randrange(1,30);line(d,[(x,y),(x+1,y-1)],'grass3' if j%2 else 'green2')
 elif k<8:
  rect(d,(0,0,31,31),'stone0')
  for y in range(0,32,8):
   for x in range(-8 if y%16 else 0,32,16):
    rect(d,(x+1,y+1,x+14,y+6),'stone1' if (x+y+k)%3 else 'stone2');line(d,[(x+1,y+1),(x+14,y+1)],'stone2');rect(d,(x+3,y+3,x+4,y+3),'stone0')
 elif k<10:
  rect(d,(0,0,31,31),'wood0')
  for y in range(0,32,8):
   for x in range(-8 if y%16 else 0,32,16):
    rect(d,(x+1,y+1,x+14,y+6),'coral0' if (x+y)%3 else 'wood1');line(d,[(x+1,y+1),(x+14,y+1)],'coral1')
 elif k<12:
  rect(d,(0,0,31,31),'jade0');
  for y in [5,14,24]:line(d,[(2+(y+k)%7,y),(13+(y+k)%8,y)],'jade1')
 elif k==12:
  rect(d,(0,0,31,31),'wood0')
  for x in range(1,32,8):rect(d,(x,0,x+5,31),'wood2');line(d,[(x,0),(x,31)],'wood3')
 else:
  # Transparent curb/flower overlays.
  if k==13:
   rect(d,(0,20,31,27),'stone0');rect(d,(0,19,31,23),'stone3');line(d,[(0,18),(31,18)],'cream2');line(d,[(15,19),(15,25)],'stone1')
  if k==14:
   for x,y in [(5,7),(17,21),(26,10)]:
    line(d,[(x,y+6),(x,y)],'green0');rect(d,(x-2,y,x+2,y+2),'flower');rect(d,(x,y-1,x,y+3),'cream2');rect(d,(x,y+1,x,y+1),'gold')
  if k==15:
   rect(d,(0,0,31,31),'stone0');rect(d,(1,1,30,30),'stone2');line(d,[(1,1),(30,1),(30,29)],'stone3');line(d,[(2,29),(29,29)],'stone1');rect(d,(5,8,7,8),'stone1');rect(d,(22,23,24,23),'stone3')
 tiles.append(im)
at=canvas(256,64)
for i,im in enumerate(tiles):at.alpha_composite(im,((i%8)*32,(i//8)*32))
save(at,'tiles')
# Modular house bay kit, reused by every town building.
def wallbay(kind='window'):
 im=canvas(32,48);d=ImageDraw.Draw(im);rect(d,(0,0,31,47),'wood0');rect(d,(3,2,28,43),'cream1');rect(d,(3,2,28,7),'wood1');rect(d,(3,8,5,43),'cream0');rect(d,(0,0,3,47),'wood1');line(d,[(1,1),(1,47)],'wood3');rect(d,(28,0,31,47),'wood1');rect(d,(4,39,27,44),'wood2')
 if kind=='door':
  rect(d,(7,9,25,45),'deep');rect(d,(9,10,23,43),'wood1');rect(d,(11,12,21,30),'wood0')
  for x in [12,16,20]:line(d,[(x,13),(x,29)],'wood3')
  for y in [17,23,29]:line(d,[(11,y),(21,y)],'wood2')
  rect(d,(20,34,21,35),'gold');rect(d,(9,45,24,47),'stone3')
 else:
  rect(d,(7,12,25,34),'wood0');rect(d,(9,14,23,31),'jade0');poly(d,[(9,14),(21,14),(9,26)],'jade2')
  for x in [10,16,22]:line(d,[(x,14),(x,31)],'wood2')
  for y in [18,24,30]:line(d,[(9,y),(23,y)],'wood2')
  rect(d,(6,34,26,36),'wood3')
 return im
mods={k:wallbay(k) for k in ['window','door']}
for k,im in mods.items():im.save(S/('module-'+k+'.png'))
def building(name,bays=4,awning=False,sign='mail'):
 w=bays*32+32;im=canvas(w,144);d=ImageDraw.Draw(im)
 # foundation + visible side wall, left lighting, shaded right return.
 poly(d,[(12,80),(w-20,80),(w-8,89),(w-8,132),(12,132)],'stone0');rect(d,(12,124,w-20,131),'stone2');line(d,[(12,124),(w-20,124)],'stone3')
 for x in range(15,w-20,16):line(d,[(x,126),(x,131)],'stone1')
 poly(d,[(w-24,70),(w-9,80),(w-9,125),(w-24,121)],'wood0')
 for y in range(82,122,8):line(d,[(w-22,y),(w-10,y+6)],'wood1')
 for i in range(bays):im.alpha_composite(mods['door' if i==bays//2 else 'window'],(12+i*32,76))
 d=ImageDraw.Draw(im);rect(d,(10,74,w-18,81),'wood0');rect(d,(10,72,w-18,75),'wood3')
 # Long ridge, shallow curved Korean hipped roof; two visible planes and lifted corners.
 l=w//3;r=w-l
 poly(d,[(0,65),(l,19),(r,19),(w-2,65),(w-7,77),(8,78)],'roof0')
 poly(d,[(4,63),(l,23),(r,23),(w-6,63),(w-15,70),(15,70)],'roof1')
 poly(d,[(r,23),(w-6,63),(w-15,70),(r-3,55)],'roof0')
 for row in range(8):
  y=26+row*5; left=int(l*(1-row/9));right=int(r+(w-r-9)*row/9)
  for x in range(left+3,right-2,7):
   slant=round((x-w/2)/(w/2)*2)
   poly(d,[(x,y),(x+4,y),(x+4+slant,y+3),(x+slant,y+4)],'roof2')
   line(d,[(x,y),(x+4,y)],'roof3');line(d,[(x+4,y+1),(x+4+slant,y+4)],'roof0')
 line(d,[(2,66),(14,70),(w//2,72),(w-15,70),(w-3,65)],'roof2',2)
 line(d,[(4,70),(15,74),(w//2,76),(w-15,73),(w-4,68)],'roof3')
 line(d,[(l-3,20),(r+3,20)],'roof3',3);line(d,[(l-3,24),(r+4,24)],'roof0')
 for x in range(l,r+1,9):rect(d,(x,17,x+3,20),'roof2');rect(d,(x,17,x+2,17),'roof3')
 for x,y in [(2,65),(l-3,19),(r+3,19),(w-3,64)]:
  poly(d,[(x-3,y+2),(x,y-5),(x+4,y+3)],'roof0');rect(d,(x,y-3,x+1,y-1),'gold')
 for x in range(13,w-20,16):
  rect(d,(x,77,x+4,82),'wood1');rect(d,(x-2,77,x+7,78),'wood3')
 # Threshold steps and recessed sign under eave.
 cx=12+(bays//2)*32+16
 for y,ex in [(132,18),(136,22),(140,25)]:rect(d,(cx-ex,y,cx+ex,y+3),'stone1');line(d,[(cx-ex,y),(cx+ex,y)],'stone3')
 rect(d,(cx-23,81,cx+23,94),'wood0');rect(d,(cx-21,83,cx+21,92),'wood2');rect(d,(cx-19,84,cx+19,90),'cream1')
 if sign=='mail':poly(d,[(cx-7,84),(cx+7,84),(cx+7,90),(cx-7,90)],'jade0');line(d,[(cx-7,84),(cx,88),(cx+7,84)],'cream2')
 elif sign=='cafe':rect(d,(cx-5,84,cx+3,89),'coral0');line(d,[(cx+4,85),(cx+6,85),(cx+6,88),(cx+4,88)],'wood0');line(d,[(cx-6,90),(cx+6,90)],'wood0')
 else:line(d,[(cx-7,84),(cx-7,90),(cx,88),(cx+7,90),(cx+7,84),(cx,86),(cx-7,84)],'jade0')
 if awning:
  for x in range(13,w-20,10):poly(d,[(x,99),(x+9,99),(x+13,111),(x+3,111)],'coral1' if x%20<10 else 'cream2')
  line(d,[(15,112),(w-17,112)],'wood0',2)
 return save(im,name)
building('courier',4,False,'mail');building('cafe',4,True,'cafe');building('hanok',5,False,'book');building('academy',4,False,'book')
# Tree silhouette built from overlapping pixel leaf lobes, never smooth ellipses.
def tree(name,variant):
 im=canvas(80,104);d=ImageDraw.Draw(im)
 poly(d,[(32,99),(37,67),(31,48),(39,46),(43,68),(51,59),(54,63),(44,77),(46,96),(56,101)],'wood0');line(d,[(39,63),(40,94),(36,99)],'wood2',2);line(d,[(43,72),(52,62)],'wood1',2)
 clusters=[(30,28,21),(51,33,22),(19,45,18),(42,51,24),(61,51,16),(39,15,16)]
 ramps=['coral0','coral1','flower','cream2'] if variant==2 else ['green0','green1','green2','green3']
 if variant==1:
  clusters=[(40,15,13),(39,31,20),(39,50,28),(39,67,29)]
 for i,(cx,cy,r) in enumerate(clusters):
  pts=[(cx-r,cy+3),(cx-r+3,cy-r//2),(cx-r//2,cy-r+3),(cx+1,cy-r),(cx+r-5,cy-r//2),(cx+r,cy+3),(cx+r-4,cy+r//2),(cx+5,cy+r//2+4),(cx-r//2,cy+r//2+2)]
  poly(d,pts,ramps[0]);poly(d,[(x,y-3) for x,y in pts[:-1]],ramps[1])
  # Lit leaf masses follow the canopy volume; small stepped clusters, not random noise.
  poly(d,[(cx-r+6,cy),(cx-r+8,cy-8),(cx-5,cy-r+6),(cx+3,cy-r+4),(cx+8,cy-9),(cx+4,cy-3),(cx-4,cy+1)],ramps[2])
  for j in range(17):
   x=cx+rng.randrange(-r+5,r-4);y=cy+rng.randrange(-r+4,max(-r+5,r//2))
   if (x-cx)**2+(y-cy)**2<r*r*.70:
    c=ramps[3 if y<cy-4 and j%3==0 else 2]
    poly(d,[(x,y+2),(x+1,y),(x+4,y),(x+5,y+2),(x+3,y+4),(x,y+3)],c)
    if j%3==0:line(d,[(x+2,y+1),(x+4,y+1)],ramps[3])
 save(im,name)
for n,v in [('tree',0),('pine',1),('plum',2)]:tree(n,v)
# Coherent native props: depth and edge treatment share the same ramps.
def prop(name,w,h):
 im=canvas(w,h);d=ImageDraw.Draw(im)
 if name=='fountain':
  poly(d,[(4,29),(w//2,17),(w-4,29),(w-4,44),(w//2,55),(4,44)],'stone0');poly(d,[(4,28),(w//2,14),(w-4,28),(w//2,43)],'stone3');poly(d,[(10,28),(w//2,19),(w-10,28),(w//2,37)],'jade0');line(d,[(17,28),(w//2,23),(w-17,28)],'jade2',2)
  rect(d,(w//2-4,6,w//2+4,29),'stone1');poly(d,[(w//2-12,7),(w//2,1),(w//2+12,7),(w//2,14)],'gold');line(d,[(w//2,3),(w//2,17)],'cream2',2)
  for x in [12,w-15]:line(d,[(w//2,16),(x,23),(x,29)],'jade3')
 elif name=='bench':
  for y in [9,15,23]:rect(d,(2,y,w-3,y+4),'wood0');rect(d,(2,y,w-4,y+2),'wood2');line(d,[(3,y),(w-5,y)],'wood3')
  for x in [6,w-9]:rect(d,(x,13,x+3,h-1),'deep')
 elif name=='lantern':
  rect(d,(14,14,17,h-3),'wood0');rect(d,(13,h-5,19,h-1),'stone0');rect(d,(7,10,24,28),'wood0');rect(d,(9,12,22,26),'gold');rect(d,(11,13,14,25),'cream2');line(d,[(16,12),(16,27)],'wood2');poly(d,[(4,10),(16,4),(27,10)],'roof1');line(d,[(5,10),(26,10)],'roof3')
 elif name in ['board','portal','puzzle','outfit']:
  for x in [7,w-11]:rect(d,(x,17,x+3,h-1),'wood0');rect(d,(x,18,x+1,h-3),'wood2')
  rect(d,(2,9,w-3,h-13),'wood0');rect(d,(5,12,w-6,h-16),'wood2');rect(d,(7,14,w-8,h-18),'cream1');poly(d,[(0,9),(w//2,1),(w-1,9)],'roof1');line(d,[(1,9),(w-2,9)],'roof3')
  if name=='board':
   for x,y in [(10,17),(25,20),(16,28)]:rect(d,(x,y,x+9,y+10),'white');line(d,[(x+2,y+3),(x+7,y+3)],'wood1')
  elif name=='puzzle':
   for x,y in [(12,19),(24,19),(12,29),(24,29)]:rect(d,(x,y,x+8,y+7),'jade0');line(d,[(x+2,y+2),(x+6,y+2),(x+6,y+5)],'gold')
  elif name=='outfit':poly(d,[(18,17),(12,20),(10,26),(15,28),(16,36),(29,36),(30,28),(35,26),(31,20),(26,17),(23,21)],'coral0');line(d,[(22,22),(22,34)],'gold')
  else:poly(d,[(21,16),(30,25),(21,34),(12,25)],'jade0');line(d,[(16,20),(26,30)],'gold',2)
 elif name=='stall':
  for x in [5,w-8]:rect(d,(x,12,x+3,h-2),'wood0')
  rect(d,(3,31,w-4,h-7),'wood1');rect(d,(2,29,w-3,33),'wood3');rect(d,(6,36,w-7,h-9),'wood2')
  for x in range(0,w-5,8):poly(d,[(x+3,3),(x+10,3),(x+7,20),(x,20)],'jade1' if x%16 else 'cream1')
  line(d,[(0,21),(w-5,21)],'wood0',2)
  for x in range(9,w-8,11):rect(d,(x,24,x+6,28),'coral1');rect(d,(x+2,22,x+5,25),'gold')
 elif name=='gardenbed':
  poly(d,[(2,23),(w-8,19),(w-2,29),(w-7,h-2),(8,h-1),(2,33)],'stone0');poly(d,[(2,22),(w-8,18),(w-2,27),(w-8,33),(8,36),(2,30)],'stone3');poly(d,[(8,23),(w-11,21),(w-8,27),(w-12,30),(10,32)],'wood0')
  for x in range(10,w-9,8):
   y=16+(x%13)//3
   poly(d,[(x-5,y+10),(x-6,y+3),(x-2,y-2),(x+4,y-3),(x+8,y+3),(x+7,y+10)],'green0');poly(d,[(x-4,y+5),(x-3,y),(x+3,y-1),(x+6,y+4),(x+2,y+7)],'green2');rect(d,(x,y,x+2,y+2),'green3')
   rect(d,(x+1,y-4,x+4,y-2),'flower');rect(d,(x+2,y-3,x+3,y-2),'cream2')
 elif name=='parcel':
  for x,y in [(2,15),(15,8)]:
   rect(d,(x,y,x+13,y+15),'wood0');rect(d,(x+1,y+1,x+12,y+13),'wood2');rect(d,(x+5,y+1,x+7,y+13),'cream1');line(d,[(x+1,y+1),(x+12,y+1)],'wood3');rect(d,(x+8,y+4,x+10,y+7),'white')
 elif name=='table':
  for x in [11,33]:rect(d,(x,18,x+3,31),'wood0')
  poly(d,[(2,13),(23,3),(45,13),(45,20),(23,28),(2,20)],'wood0');poly(d,[(3,12),(23,4),(44,12),(23,21)],'wood2');line(d,[(4,12),(23,5),(43,12)],'wood3');rect(d,(19,8,25,14),'cream2');rect(d,(20,8,24,10),'wood1');rect(d,(29,13,35,15),'gold')
 elif name=='planter':
  poly(d,[(2,16),(w-3,16),(w-6,h-1),(6,h-1)],'wood0');rect(d,(4,17,w-5,21),'wood3');rect(d,(7,22,w-8,h-3),'wood2')
  for x in [6,14,22]:line(d,[(x,16),(x+2,6)],'green0',2);rect(d,(x,5,x+5,9),'green2');rect(d,(x+2,2,x+4,5),'flower');rect(d,(x+2,4,x+3,5),'cream2')
 save(im,name)
for n,w,h in [('gardenbed',64,40),('parcel',32,32),('table',48,32),('fountain',80,56),('bench',48,32),('lantern',32,64),('board',48,56),('portal',48,56),('puzzle',48,56),('outfit',48,56),('stall',64,56),('planter',32,32)]:prop(n,w,h)
# Avatar anatomy/registration shared by all skin, clothing, hair and accessory layers.
ACTIONS={'idle':4,'walk':8,'run':8,'wave':6,'celebrate':8,'pose':4};DIRS=['down','left','right','up'];NAMES=[f'{a}-{d}-{i}' for d in DIRS for a,n in ACTIONS.items() for i in range(n)]
LAYERS=['body','outfit0','outfit1','hair0','hair1','satchel'];atlases={k:canvas(512,1024) for k in LAYERS};frames={}
for idx,key in enumerate(NAMES):
 a,dr,ii=key.split('-');i=int(ii);phase=i*math.pi/4
 walk=a=='walk';run=a=='run';dy=([0,0,-1,0][i] if a=='idle' else [0,-1,-2,-1,0,-1,-2,-1][i] if run else int(round(math.sin(phase))) if walk else -2 if a=='celebrate' and i in [2,3,6] else 0)
 lean=(2 if dr=='right' else -2 if dr=='left' else 0) if run else 0
 hx=16+lean;hy=12+dy;stride=([0,2,3,2,0,-2,-3,-2][i] if walk else [0,4,5,3,0,-4,-5,-3][i] if run else 0)
 ims={k:canvas(32,48) for k in LAYERS};ds={k:ImageDraw.Draw(v) for k,v in ims.items()};d=ds['body'];side=dr in ['left','right']
 # Separate planted walk and airborne running silhouettes; shoulders lean at run.
 for sign in [-1,1]:
  fx=16+sign*4+(stride if side and sign==1 else -stride if side else 0);fy=43+(sign*stride//2 if not side else (-3 if run and i%4==2 else 0))
  rect(d,(fx-2,32+dy,fx+2,min(45,fy)),'roof0');rect(d,(fx-3,min(44,fy),fx+3,min(46,fy+2)),'deep');line(d,[(fx-2,min(44,fy)),(fx+2,min(44,fy))],'roof2')
 # Face silhouette has the same pixel density as architecture.
 poly(d,[(hx-6,hy-5),(hx+5,hy-5),(hx+8,hy-1),(hx+8,hy+8),(hx+4,hy+12),(hx-4,hy+12),(hx-8,hy+8),(hx-8,hy-1)],'ink');rect(d,(hx-6,hy-3,hx+6,hy+7),'skin1');rect(d,(hx-4,hy+8,hx+4,hy+10),'skin1');rect(d,(hx-5,hy-2,hx+3,hy+6),'skin2')
 if dr!='up':
  eyes=[hx-3,hx+4] if dr=='down' else [hx-4] if dr=='left' else [hx+4]
  for x in eyes:
   if a=='idle' and i==1:line(d,[(x-1,hy+3),(x+1,hy+3)],'ink')
   else:rect(d,(x,hy+1,x+1,hy+4),'ink');rect(d,(x,hy+1,x,hy+1),'white')
  rect(d,(hx-1 if dr=='down' else hx-4 if dr=='left' else hx+4,hy+7,hx+1 if dr=='down' else hx-3 if dr=='left' else hx+5,hy+7),'skin0')
 # Hands/arms and clothing: actual per-pose anatomy rather than a recolour atlas.
 left=(8,30+dy+stride//2);right=(24,30+dy-stride//2)
 if a=='wave':right=(26,20+dy-[0,2,6,4,6,0][i])
 if a=='celebrate':left=(6,17+dy-(i%2)*2);right=(26,17+dy-(i%2)*2)
 if a=='pose':left=(7,31+dy);right=(24,24+dy)
 for x,y in [left,right]:rect(d,(x-2,y-2,x+2,y+3),'skin0');rect(d,(x-1,y-2,x+1,y+1),'skin2')
 for outfit in [0,1]:
  dd=ds[f'outfit{outfit}'];c0,c1,c2=('jade0','jade1','jade2') if outfit==0 else ('roof0','roof1','roof2')
  poly(dd,[(11+lean,23+dy),(21+lean,23+dy),(24,34+dy),(22,38+dy),(10,38+dy),(8,34+dy)],c0);rect(dd,(12+lean,24+dy,20+lean,35+dy),c1);rect(dd,(12+lean,24+dy,14+lean,34+dy),c2)
  for x,y in [left,right]:line(dd,[(11 if x<16 else 21,25+dy),(x,y-3)],c0,5);line(dd,[(12 if x<16 else 20,25+dy),(x,y-3)],c1,3)
  if outfit==0:poly(dd,[(11+lean,23+dy),(16+lean,27+dy),(22+lean,23+dy),(21+lean,26+dy),(16+lean,30+dy)],'coral1');rect(dd,(18+lean,27+dy,20+lean,34+dy),'coral0')
  else:rect(dd,(15+lean,24+dy,17+lean,36+dy),'cream1');poly(dd,[(11+lean,24+dy),(15+lean,25+dy),(13+lean,29+dy)],'cream2');rect(dd,(19+lean,29+dy,21+lean,32+dy),'gold')
 for h in [0,1]:
  dd=ds[f'hair{h}'];poly(dd,[(hx-9,hy),(hx-8,hy-5),(hx-4,hy-8),(hx+4,hy-8),(hx+8,hy-5),(hx+9,hy+2),(hx+6,hy+1),(hx+5,hy-2),(hx-3,hy-1),(hx-7,hy+3)],'hair0');line(dd,[(hx-6,hy-5),(hx-2,hy-6),(hx+4,hy-5)],'hair2',2)
  if h==0:
   for xx,yy in [(-6,-2),(-2,-3),(3,-2)]:poly(dd,[(hx+xx,hy+yy),(hx+xx+4,hy+yy),(hx+xx+1,hy+yy+4)],'hair1')
  else:
   rect(dd,(hx-9,hy,hx-7,hy+11),'hair0');rect(dd,(hx+7,hy,hx+9,hy+11),'hair0');rect(dd,(hx+7,hy-6,hx+11,hy-2),'hair1');rect(dd,(hx+8,hy-6,hx+10,hy-5),'coral1')
  if dr=='up':rect(dd,(hx-7,hy-2,hx+7,hy+8),'hair0');line(dd,[(hx-4,hy-2),(hx-4,hy+6)],'hair1');rect(dd,(hx-5,hy+9,hx+5,hy+11),'hair1')
 dd=ds['satchel'];line(dd,[(10+lean,24+dy),(23,35+dy)],'wood0',2);rect(dd,(21,32+dy,28,39+dy),'wood0');rect(dd,(22,33+dy,27,37+dy),'wood2');rect(dd,(24,34+dy,25,35+dy),'gold')
 x=(idx%14)*36+2;y=(idx//14)*52+2;frames[key]={'frame':{'x':x,'y':y,'w':32,'h':48},'rotated':False,'trimmed':False,'spriteSourceSize':{'x':0,'y':0,'w':32,'h':48},'sourceSize':{'w':32,'h':48}}
 for k,im in ims.items():
  p=S/'avatar'/k;p.mkdir(parents=True,exist_ok=True);im.save(p/(key+'.png'));atlases[k].alpha_composite(im,(x,y))
for k,im in atlases.items():save(im,k)
(S/'avatar.json').write_text(json.dumps({'frames':frames,'meta':{'app':'Korean Arena native layered raster pipeline','size':{'w':512,'h':1024},'scale':'1'}},indent=2)+'\n');shutil.copy2(S/'avatar.json',O/'avatar.json')
# One original Central Plaza; source Tiled objects are authoritative for physics/landmarks.
W,H=32,24;ground=[];edge=[]
for y in range(H):
 for x in range(W):
  road=(12<=x<=19 or 11<=y<=17);plaza=8<=x<=23 and 9<=y<=18
  water=(2<=x<=6 and 17<=y<=20)
  inlay=plaza and ((x in [8,23] and y%3!=0) or (y in [9,18] and x%3!=0) or (12<=x<=19 and y in [12,15] and x in [12,13,18,19]))
  ground.append(11+(x+y)%2 if water else 9 if inlay else 16 if plaza else 5+(x*7+y*3)%4 if road else 1+(x*3+y*7)%4)
  edge.append(14 if (y in [10,18] and 7<=x<=24) else 15 if ((x*13+y*17)%37==0 and not road and not plaza and not water) else 0)
objects=[]
def add(kind,x,y,w,h,label='',collide=True):objects.append({'id':len(objects)+1,'kind':kind,'x':x,'y':y,'width':w,'height':h,'label':label,'collide':collide})
# Buildings stand on separate garden plots with walkable doors and social-facing entrances.
add('hanok',504,280,160,28,'Nhà văn hóa');add('courier',330,414,128,28,'Trạm thư');add('cafe',694,414,128,28,'Café Dal');add('academy',797,666,128,28,'TOPIK · Chưa mở')
add('fountain',512,470,64,25,'Giếng thư')
for k,x,y,label in [('board',410,427,'Bảng chuyện'),('puzzle',615,427,'Ghép âm · Gate 3'),('outfit',233,586,'Góc trang phục'),('portal',655,663,'PvP · Chưa mở'),('stall',340,650,'Quầy chợ')]:add(k,x,y,40 if k!='stall' else 54,14,label)
for x,y in [(135,268),(310,241),(686,245),(903,282),(115,504),(890,511),(148,685),(457,708),(598,724),(927,708),(73,371)]:add('tree' if x%3 else 'pine',x,y,24,16)
for x,y in [(376,268),(643,274),(95,607)]:add('plum',x,y,24,16)
for x,y in [(390,482),(631,482),(400,588),(601,588)]:add('bench',x,y,42,12)
for x,y in [(352,414),(672,414),(352,581),(675,581),(200,684),(850,677)]:add('lantern',x,y,14,10)
for x,y in [(270,419),(755,420),(448,310),(560,310),(315,555),(704,555),(760,660),(854,660),(296,651)]:add('planter',x,y,26,12)
for x,y in [(266,448),(282,463),(305,448)]:add('parcel',x,y,24,14)
for x,y in [(732,454),(755,492)]:add('table',x,y,40,16)
for x,y in [(696,468),(784,465),(704,510)]:add('planter',x,y,26,12)
for x,y in [(315,218),(285,246),(881,265),(917,230),(101,483),(125,451),(879,547),(900,571),(121,702)]:add('tree' if x%2 else 'pine',x,y,24,16)
for x,y in [(317,527),(705,542),(402,315),(622,315)]:add('gardenbed',x,y,54,20)
collisions=[{'id':i+1,'name':p['kind'],'type':'solid','x':p['x']-p['width']/2,'y':p['y']-p['height'],'width':p['width'],'height':p['height'],'rotation':0,'visible':True} for i,p in enumerate(objects) if p['collide']]
# Water is bounded, while board/plaza/café/courier all remain reachable around footprints.
collisions.append({'id':len(collisions)+1,'name':'pond','type':'solid','x':64,'y':544,'width':160,'height':128,'rotation':0,'visible':True})
mapdata={'type':'map','version':'1.10','tiledversion':'1.11.2','orientation':'orthogonal','renderorder':'right-down','width':W,'height':H,'tilewidth':32,'tileheight':32,'infinite':False,'layers':[{'id':1,'name':'Ground','type':'tilelayer','width':W,'height':H,'x':0,'y':0,'opacity':1,'visible':True,'data':ground},{'id':2,'name':'Edging','type':'tilelayer','width':W,'height':H,'x':0,'y':0,'opacity':1,'visible':True,'data':edge},{'id':3,'name':'Collision','type':'objectgroup','objects':collisions}],'tilesets':[{'firstgid':1,'name':'town','tilewidth':32,'tileheight':32,'tilecount':16,'columns':8,'image':'tiles.png','imagewidth':256,'imageheight':64,'margin':0,'spacing':0}]}
(S/'plaza.json').write_text(json.dumps(mapdata,indent=2)+'\n');shutil.copy2(S/'plaza.json',O/'plaza.json')
world={'width':1024,'height':768,'spawn':[512,560],'npc':[462,524],'follow':132,'objects':objects,'mapSha256':hashlib.sha256((O/'plaza.json').read_bytes()).hexdigest(),'role':'Ari · Người giữ những lá thư','mood':'Một quảng trường chung, những câu chuyện còn bỏ ngỏ.','vi':'Living Pixel Seoul'}
(S/'world.json').write_text(json.dumps(world,ensure_ascii=False,indent=2)+'\n')
# Native outfit source board, explicitly source-only; gameplay proof captured separately.
board=Image.new('RGBA',(512,144),col('cream1'));dd=ImageDraw.Draw(board)
for j,(h,o) in enumerate([(0,0),(1,0),(0,1),(1,1)]):
 for di,dr in enumerate(DIRS):
  key=f'idle-{dr}-0';n=NAMES.index(key);x=(n%14)*36+2;y=(n//14)*52+2
  for layer in ['body',f'outfit{o}',f'hair{h}','satchel']:board.alpha_composite(atlases[layer].crop((x,y,x+32,y+48)),(j*128+di*32,36))
 dd.text((j*128+4,16),f'H{h+1} / O{o+1}',fill=col('ink'))
board.save(S/'outfit-source.png')
manifest={'original':True,'provenance':'Entire active kit is deterministic native integer raster code; no extracted/copied reference game pixels or downsampled image masters.','palette':P,'seed':4004,'actions':ACTIONS,'directions':DIRS,'layers':LAYERS,'frame_count':len(NAMES),'source_grid':1,'tile':32,'sprite':[32,48],'objects':len(objects),'colliders':len(collisions),'files':[{'path':str(p.relative_to(O)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in sorted(O.iterdir()) if p.is_file()]}
(S/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('Exported one native pixel kit:',len(NAMES),'frames/layer;',len(objects),'props;',len(collisions),'colliders')
