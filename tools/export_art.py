"""Original code-authored pixel art. Integer raster geometry; no image resampling.
Edit palette/layout.json and these named component functions, then export.
Indexed PNG masters remain editable in any pixel editor. MIT project artwork.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import json, math, hashlib, random
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'public/assets'; SRC=ROOT/'assets-src'; OUT.mkdir(parents=True,exist_ok=True); SRC.mkdir(exist_ok=True)
BASE={'outline':'343c51','woodDark':'705254','wood':'aa7661','woodLight':'d8a47b','cream':'fff0cd','paper':'e8d7b0','stoneDark':'9daaa0','stone':'c8cab2','stoneLight':'e5dfc3','jadeDark':'477b6b','jade':'77ac86','jadeLight':'b6d2a0','grassDark':'82a17a','grass':'abc291','grassLight':'c4d3a5','roofDark':'34495c','roof':'506b77','roofLight':'81959b','coralDark':'ac5e66','coral':'e68d86','coralLight':'ffc1a4','goldDark':'bf874f','gold':'e7b66e','goldLight':'ffe4a2','skinDark':'c88e73','skin':'efbb90','skinLight':'ffe0b6','hair':'3d3946','hairLight':'645161','waterDark':'578c9c','water':'82b4bc','waterLight':'c0e3d5'}
STYLES={'A':{'name':'Celadon Morning','description':'Thanh thoát · ngói lam · vườn mơ','colors':{},'hair':'bob'},'B':{'name':'Coral Courier','description':'Ấm áp · người đưa thư · mái ngói cong','colors':{'wood':'a97159','woodLight':'d9a077','coral':'ed9385','jade':'7fab8c'},'hair':'bun'},'C':{'name':'Indigo Festival','description':'Chàm sâu · đèn mật ong · phố lễ hội','colors':{'grass':'a2b3a3','grassDark':'798f8f','grassLight':'bbccba','roof':'415578','roofDark':'303b5b','roofLight':'7281a2','wood':'957b75','woodLight':'c1a290','coral':'a7a0ce','coralDark':'77789f','coralLight':'d8b9d6'},'hair':'cap'}}
for s in STYLES.values():s['palette']={**BASE,**s['colors']}
if (SRC/'directions.json').exists():STYLES=json.loads((SRC/'directions.json').read_text())
else:(SRC/'directions.json').write_text(json.dumps(STYLES,ensure_ascii=False,indent=2)+'\n')
layout={'tile':32,'width':24,'height':18,'spawn':[384,355],'house':[384,274],'npc':[430,320],'props':[{'kind':'tree','x':170,'y':208},{'kind':'tree','x':612,'y':218},{'kind':'tree','x':100,'y':420},{'kind':'tree','x':650,'y':465},{'kind':'market','x':588,'y':345},{'kind':'bench','x':196,'y':370},{'kind':'bench','x':566,'y':440},{'kind':'lamp','x':270,'y':318},{'kind':'lamp','x':494,'y':318},{'kind':'mailbox','x':332,'y':315},{'kind':'bridge','x':384,'y':559}]}
if (SRC/'layout.json').exists():layout=json.loads((SRC/'layout.json').read_text())
else:(SRC/'layout.json').write_text(json.dumps(layout,indent=2)+'\n')
class Art:
 def __init__(self,w,h,p):self.im=Image.new('RGBA',(w,h)); self.d=ImageDraw.Draw(self.im);self.p=p
 def c(self,k):return '#'+self.p[k]
 def rect(self,box,k):self.d.rectangle(tuple(map(int,box)),fill=self.c(k))
 def poly(self,pts,k):self.d.polygon([(int(x),int(y)) for x,y in pts],fill=self.c(k))
 def line(self,pts,k,width=1):self.d.line([(int(x),int(y)) for x,y in pts],fill=self.c(k),width=width)
 def ellipse(self,box,k):self.d.ellipse(tuple(map(int,box)),fill=self.c(k))
 def paste(self,im,x,y):self.im.alpha_composite(im,(int(x),int(y)))

def roof(a,x,y,w,h):
 # Curved gabled silhouette; staggered ceramic courses, stepped eaves, ridge end finials.
 pts=[(x+9,y+h-17),(x+28,y+h-30),(x+w//2,y),(x+w-28,y+h-30),(x+w-9,y+h-17),(x+w,y+h-23),(x+w-2,y+h-10),(x+w-18,y+h-3),(x+18,y+h-3),(x+2,y+h-10),(x,y+h-23)]
 a.poly(pts,'outline'); inner=[(x+12,y+h-18),(x+31,y+h-29),(x+w//2,y+5),(x+w-31,y+h-29),(x+w-12,y+h-18),(x+w-5,y+h-15),(x+w-20,y+h-7),(x+20,y+h-7),(x+5,y+h-15)];a.poly(inner,'roofDark')
 for row in range(5):
  yy=y+16+row*8; half=int((yy-y)/max(1,h-25)*(w/2-26)); left=x+w//2-half;right=x+w//2+half
  for xx in range(left+(row%2)*4,right,9):
   a.rect((xx,yy,min(xx+6,right),yy+4),'roof');a.line([(xx,yy),(min(xx+5,right),yy)],'roofLight');a.line([(xx+2,yy+2),(xx+2,yy+4)],'roofDark')
 # front course unifies roof and detailed cylindrical end caps
 for xx in range(x+20,x+w-18,9):
  yy=y+h-13;a.rect((xx,yy,xx+6,yy+5),'roof');a.line([(xx+1,yy),(xx+5,yy)],'roofLight');a.rect((xx+2,yy+2,xx+4,yy+4),'roofDark')
 a.line([(x+19,y+h-5),(x+w-19,y+h-5)],'jadeDark',2);a.line([(x+23,y+h-4),(x+w-23,y+h-4)],'jadeLight')
 a.rect((x+w//2-3,y-3,x+w//2+3,y+8),'roofLight');a.rect((x+w//2-2,y-5,x+w//2+2,y-2),'gold');a.rect((x+w//2-8,y+7,x+w//2+8,y+9),'roofLight')

def house(p,style):
 a=Art(224,208,p)
 a.poly([(17,191),(207,191),(216,202),(207,207),(17,207),(8,202)],'stoneDark')
 a.rect((21,123,203,193),'woodDark');a.rect((25,126,199,178),'paper')
 for xx in (29,83,137,191):
  a.rect((xx,119,xx+5,186),'woodDark');a.rect((xx+1,121,xx+2,181),'woodLight');a.rect((xx-3,174,xx+8,182),'wood')
 for xx in (39,146):
  a.rect((xx,133,xx+37,167),'wood');a.rect((xx+3,136,xx+34,163),'cream')
  for ix in range(xx+5,xx+34,7):a.line([(ix,137),(ix,162)],'wood',2)
  for iy in (143,151,159):a.line([(xx+4,iy),(xx+34,iy)],'wood',2)
 a.rect((93,132,130,183),'outline');a.rect((97,135,126,180),'wood');a.rect((99,137,124,170),'paper')
 for xx in (102,109,117,123):a.line([(xx,139),(xx,168)],'woodDark')
 for yy in (145,153,162):a.line([(100,yy),(124,yy)],'woodDark')
 a.rect((118,169,120,172),'goldLight')
 a.rect((24,120,200,127),'woodDark');a.rect((25,122,198,124),'woodLight')
 for xx in range(32,192,18):
  a.rect((xx,127,xx+8,130),'jadeDark');a.rect((xx+2,127,xx+5,127),'coral')
 # broad raised timber porch with individual joints
 a.rect((22,180,202,188),'wood');a.line([(22,180),(202,180)],'woodLight')
 for xx in range(27,202,12):a.line([(xx,181),(xx,188)],'woodDark')
 for y,w in [(188,44),(192,50),(196,58)]:
  a.rect((112-w//2,y,112+w//2,y+3),'stone');a.line([(112-w//2,y),(112+w//2,y)],'stoneLight')
 # letter-mark plaque, roof annex, ornamental colored timber joinery
 a.rect((88,115,135,130),'outline');a.rect((90,117,133,128),'woodLight');a.rect((104,118,119,126),'cream');a.line([(104,118),(111,123),(119,118)],'coralDark')
 roof(a,5,35,214,87)
 if style=='B':roof(a,55,14,114,45)
 elif style=='A':
  a.rect((91,43,132,48),'roofLight');a.rect((104,36,119,45),'gold');a.rect((107,34,116,36),'cream')
 else:
  roof(a,67,18,90,42)
  for x in range(51,180,16):
   a.line([(x,123),(x,132)],'woodDark');a.poly([(x-4,132),(x+4,132),(x+3,143),(x,146),(x-3,143)],'gold');a.rect((x,134,x,141),'cream')
 for x in (36,180):
  a.rect((x,130,x+1,135),'woodDark');a.rect((x-6,136,x+7,149),'coralDark');a.rect((x-5,138,x+6,147),'coral');a.rect((x-2,138,x+1,147),'goldLight');a.rect((x-5,134,x+6,136),'gold');a.line([(x,150),(x,156)],'gold')
 for x in (18,199):
  a.rect((x,183,x+7,190),'coralDark');a.rect((x+1,181,x+6,185),'woodLight');a.ellipse((x-2,169,x+10,181),'jadeDark');a.ellipse((x-1,166,x+9,178),'jade');a.rect((x+3,167,x+5,172),'jadeLight')
 return a.im

def char(p,direction,frame,action,style):
 p={**p,'coral':p['jade'],'coralDark':p['jadeDark'],'coralLight':p['jadeLight']} if style=='bob' else p
 a=Art(48,64,p);side=direction in ('left','right');back=direction=='up'; swing=[0,1,2,0,-1,-2][frame%6] if action in ('walk','run') else 0
 bob=1 if action in ('walk','run') and frame%3==1 else 0;cy=24+bob
 # anchored feet/offset legs, rich small garments, face and hair clusters
 a.ellipse((14,56,34,59),'stoneDark')
 for x,k in [(17,swing),(27,-swing)]:
  yy=48+(abs(k) if k<0 else 0);a.rect((x,44,x+5,yy+5),'paper');a.rect((x,yy+4,x+6,yy+7),'outline');a.rect((x+1,yy+4,x+5,yy+4),'woodLight')
 a.poly([(15,36+bob),(32,36+bob),(34,45),(28,48),(18,48),(13,44)],'coralDark');a.rect((16,37+bob,31,44),'coral');a.line([(17,38+bob),(23,43),(29,37+bob)],'cream',2);a.line([(23,43),(28,44)],'goldLight')
 # sleeves swing in opposition; gesture anticipates then waves
 arm= -6 if action=='wave' and frame%4 in (1,2) else swing
 for x,off in [(11,arm),(32,-swing)]:
  a.rect((x,37+off,x+4,43+off),'coral');a.rect((x,42+off,x+4,44+off),'cream');a.rect((x+1,45+off,x+3,47+off),'skin')
 a.line([(18,35),(30,45)],'woodDark',2);a.rect((28,41,35,49),'jadeDark');a.rect((29,41,35,47),'jade');a.rect((29,42,34,44),'cream');a.line([(29,42),(32,45),(34,42)],'wood')
 # tiny side silhouette and back hairstyle, distinct directional drawings
 a.poly([(14,cy-12),(19,cy-17),(30,cy-17),(35,cy-11),(36,cy+1),(31,cy+10),(18,cy+10),(12,cy+3),(12,cy-6)],'outline')
 a.poly([(15,cy-10),(20,cy-14),(29,cy-14),(33,cy-9),(34,cy+3),(29,cy+8),(19,cy+8),(14,cy+2)],'skin');a.rect((17,cy+4,30,cy+6),'skinLight');a.rect((14,cy+1,16,cy+4),'skinDark')
 if back:
  a.poly([(14,cy-12),(20,cy-16),(29,cy-16),(35,cy-9),(35,cy+7),(31,cy+11),(17,cy+10),(13,cy+5)],'hair');a.line([(17,cy-10),(17,cy+3)],'hairLight');a.line([(30,cy-10),(31,cy+3)],'hairLight')
 else:
  a.poly([(13,cy-8),(16,cy-13),(21,cy-16),(30,cy-15),(34,cy-10),(34,cy-2),(31,cy-1),(29,cy-7),(25,cy-3),(22,cy-7),(18,cy-3),(16,cy-2),(15,cy+5),(12,cy+2)],'hair')
  a.line([(16,cy-9),(21,cy-12),(28,cy-12)],'hairLight',2)
  eyes=[(21,cy),(29,cy)] if not side else [(29,cy)]
  for x,y in eyes:
   if action=='idle' and frame==1:a.rect((x-1,y+1,x+2,y+1),'outline')
   else:a.rect((x-1,y,x+2,y+3),'outline');a.rect((x,y,x,y),'cream')
  if not side:
   a.rect((18,cy+4,20,cy+5),'coral');a.rect((30,cy+4,32,cy+5),'coral');a.rect((25,cy+5,26,cy+5),'woodDark')
  else:a.rect((34,cy+1,35,cy+3),'skinLight');a.rect((28,cy+5,30,cy+5),'woodDark')
 if style=='bun':
  a.ellipse((10,cy-16,18,cy-8),'hair');a.rect((12,cy-16,16,cy-15),'hairLight');a.poly([(15,cy-13),(22,cy-17),(23,cy-13),(17,cy-11)],'cream');a.rect((19,cy-15,21,cy-14),'gold')
 elif style=='cap':
  a.poly([(13,cy-9),(18,cy-17),(29,cy-18),(35,cy-10)],'jadeDark');a.rect((14,cy-10,35,cy-8),'jade');a.rect((20,cy-15,28,cy-14),'jadeLight');a.rect((28,cy-9,38,cy-7),'jadeDark')
 else:a.rect((32,cy-8,35,cy+8),'hair');a.rect((30,cy-8,35,cy-6),'coral')
 if direction=='left':return a.im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
 return a.im

def prop(p,kind):
 sizes={'tree':(96,128),'lamp':(32,80),'mailbox':(40,56),'bench':(72,40),'market':(112,112),'bridge':(112,64),'flowers':(32,32),'fence':(64,32)};a=Art(*sizes[kind],p)
 if kind=='tree':
  a.ellipse((10,108,85,123),'grassDark');a.poly([(44,116),(49,75),(35,57),(42,52),(53,71),(66,50),(71,56),(57,82),(56,115)],'woodDark');a.line([(51,111),(52,75),(65,57)],'wood',3)
  for x,y,r in [(22,55,22),(56,31,25),(70,57,22),(38,39,27),(38,70,26)]:
   a.ellipse((x-r,y-r,x+r,y+r),'coralDark');a.ellipse((x-r+2,y-r,x+r-2,y+r-5),'coral');a.ellipse((x-r+4,y-r+1,x+r-6,y+2),'coralLight')
  for x,y in [(28,19),(62,18),(13,44),(36,47),(69,49),(46,64),(20,62),(59,78)]:
   a.rect((x,y,x+4,y+4),'cream');a.rect((x-2,y+1,x+6,y+3),'coralLight');a.rect((x+1,y+1,x+2,y+2),'gold')
 elif kind=='lamp':
  a.ellipse((5,72,28,77),'stoneDark');a.rect((14,21,17,74),'woodDark');a.rect((15,23,15,71),'woodLight');a.rect((5,70,26,74),'stone');a.rect((4,13,28,18),'roofDark');a.rect((7,19,25,37),'coralDark');a.rect((9,19,23,34),'gold');a.rect((12,20,19,33),'goldLight');a.line([(11,19),(11,34)],'coralDark');a.line([(21,19),(21,34)],'coralDark');a.rect((7,35,25,38),'wood');a.line([(16,39),(16,45)],'gold')
 elif kind=='mailbox':
  a.ellipse((5,49,35,54),'stoneDark');a.rect((12,30,27,49),'woodDark');a.rect((15,31,23,49),'wood');a.poly([(5,13),(10,7),(31,7),(35,13),(35,36),(5,36)],'jadeDark');a.rect((7,15,33,34),'jade');a.rect((11,19,29,21),'outline');a.rect((13,27,27,32),'cream');a.line([(13,27),(20,31),(27,27)],'coralDark');a.line([(10,9),(29,9)],'jadeLight');a.rect((35,8,36,25),'woodDark');a.rect((36,9,39,15),'coral')
 elif kind=='bench':
  a.ellipse((3,29,69,38),'grassDark');a.rect((9,21,14,34),'woodDark');a.rect((57,21,62,34),'woodDark')
  for yy in (7,13,20):a.rect((6,yy,66,yy+4),'wood');a.line([(6,yy),(66,yy)],'woodLight')
  a.rect((4,10,7,26),'woodDark');a.rect((64,10,67,26),'woodDark')
 elif kind=='market':
  a.rect((11,37,17,103),'woodDark');a.rect((94,37,100,103),'woodDark');a.rect((15,76,95,101),'wood');a.line([(16,77),(95,77)],'woodLight',2)
  for x in range(20,95,14):a.line([(x,82),(x,99)],'woodDark')
  a.poly([(6,38),(21,16),(89,16),(106,38),(102,49),(9,49)],'woodDark')
  for x in range(10,104,12):
   a.poly([(x,39),(max(x,22),18),(min(x+10,89),18),(x+10,39),(x+9,47),(x+1,47)],'cream' if x%24==10 else 'coral')
  a.line([(23,15),(88,15)],'woodLight',2)
  for x in (28,49,73):
   a.rect((x-7,67,x+9,76),'woodDark');a.rect((x-8,65,x+10,68),'gold')
   for fx in (x-4,x+3):a.ellipse((fx,55,fx+6,65),'coral');a.rect((fx+2,54,fx+4,55),'jadeDark')
  a.rect((42,86,68,96),'paper');a.rect((46,89,63,90),'woodDark')
 elif kind=='bridge':
  a.rect((5,16,106,60),'woodDark')
  for x in range(7,106,9):a.rect((x,18,x+6,58),'wood');a.line([(x,18),(x+6,18)],'woodLight')
  for y in (9,48):
   a.rect((4,y,107,y+4),'woodLight');a.rect((4,y+4,107,y+6),'woodDark')
   for x in (3,28,82,105):a.rect((x,y-8,x+4,y+15),'woodDark');a.rect((x+1,y-8,x+3,y-6),'gold')
 elif kind=='fence':
  a.rect((0,13,63,16),'woodLight');a.rect((0,22,63,24),'wood')
  for x in (1,20,40,59):a.rect((x,6,x+3,31),'wood');a.rect((x+1,6,x+2,7),'woodLight')
 else:
  for x,y in [(5,18),(13,24),(22,16),(17,8)]:
   a.line([(x,y),(x,y+7)],'jadeDark');a.rect((x-3,y-2,x+3,y+2),'coral');a.rect((x-1,y-4,x+1,y+4),'coralLight');a.rect((x,y,x,y),'gold')
 return a.im

def tiles(p):
 im=Image.new('RGBA',(256,64));rng=random.Random(71)
 for n in range(16):
  a=Art(32,32,p)
  if n<4:
   a.rect((0,0,31,31),'grass')
   for k in range([0,1,2,1][n]):
    x=rng.randrange(3,26);y=rng.randrange(3,26);a.line([(x,y+2),(x,y),(x+1,y+1),(x+2,y-1)],'grassDark' if n%2 else 'grassLight')
  elif n<10:
   a.rect((0,0,31,31),'stoneDark');a.rect((1,1,30,14),'stone');a.rect((1,17,14,30),'stone');a.rect((17,17,30,30),'stone');a.line([(2,1),(29,1)],'stoneLight');a.line([(2,17),(12,17)],'stoneLight');a.line([(18,17),(29,17)],'stoneLight');
   if n==8:a.line([(9,3),(7,7),(9,10)],'stoneDark')
  elif n<13:
   a.rect((0,0,31,31),'water');a.rect((0,0,31,3),'waterDark');a.line([(3,13),(10,13)],'waterLight');a.line([(18,24),(28,24)],'waterLight')
  elif n==13:
   a.rect((0,0,31,31),'woodDark')
   for yy in range(1,32,8):a.rect((0,yy,31,yy+5),'wood');a.line([(0,yy),(31,yy)],'woodLight')
  elif n==14:
   a.rect((0,0,31,31),'grass');a.ellipse((1,4,30,27),'grassDark');a.ellipse((3,2,28,22),'jadeDark');a.ellipse((5,2,26,18),'jade');a.line([(9,5),(19,5)],'jadeLight',2)
  else:
   a.rect((0,0,31,31),'stoneDark');a.rect((0,0,31,25),'stone');a.line([(0,1),(31,1)],'stoneLight',2)
  im.alpha_composite(a.im,((n%8)*32,(n//8)*32))
 return im

def indexed(im,path):
 # No interpolation/dither; exact <= 32 palette + transparent index.
 rgba=im.convert('RGBA');opaque=sorted(set(rgba.get_flattened_data())-{(0,0,0,0)});assert len(opaque)<=32,(path,len(opaque))
 rgb=[(0,0,0)]+[v[:3] for v in opaque];lookup={v:i+1 for i,v in enumerate(opaque)};out=Image.new('P',im.size);out.putpalette([c for v in rgb for c in v]+[0]*(768-len(rgb)*3));out.putdata([0 if v[3]==0 else lookup[v] for v in rgba.get_flattened_data()]);out.info['transparency']=0;out.save(path,optimize=True)

def make_map():
 if (SRC/'plaza.tmj').exists():
  m=json.loads((SRC/'plaza.tmj').read_text());(OUT/'plaza.json').write_text(json.dumps(m,separators=(',',':')));return m
 w,h=layout['width'],layout['height'];rng=random.Random(43);ground=[];overlay=[]
 for y in range(h):
  for x in range(w):
   road=(8<=x<=15 and 8<=y<=15) or (5<=x<=19 and 10<=y<=12) or (10<=x<=13 and y>=5)
   tile=5+rng.randrange(5) if road else 1+rng.randrange(4)
   if y==16:tile=11+(x%3)
   if y==15 and not 10<=x<=13:tile=16
   ground.append(tile);overlay.append(15 if (x in (1,22) and y in (2,3,6,7,10,11,13)) else 0)
 objs=[{'id':1,'name':'PostOffice','type':'solid','x':288,'y':209,'width':192,'height':48},{'id':2,'name':'StreamLeft','type':'solid','x':0,'y':512,'width':330,'height':32},{'id':3,'name':'StreamRight','type':'solid','x':439,'y':512,'width':329,'height':32}]
 oid=4
 for p in layout['props']:
  if p['kind'] in ('tree','market','bench','mailbox','lamp'):
   sz={'tree':(26,14),'market':(80,24),'bench':(62,18),'mailbox':(26,18),'lamp':(12,8)}[p['kind']];objs.append({'id':oid,'name':p['kind'],'type':'solid','x':p['x']-sz[0]/2,'y':p['y']-sz[1],'width':sz[0],'height':sz[1]});oid+=1
 m={'compressionlevel':-1,'type':'map','orientation':'orthogonal','renderorder':'right-down','infinite':False,'tilewidth':32,'tileheight':32,'width':w,'height':h,'version':'1.10','tiledversion':'1.12.2','nextlayerid':5,'nextobjectid':oid+2,'layers':[{'id':1,'name':'Ground','type':'tilelayer','width':w,'height':h,'x':0,'y':0,'opacity':1,'visible':True,'data':ground},{'id':2,'name':'GardenBorders','type':'tilelayer','width':w,'height':h,'x':0,'y':0,'opacity':1,'visible':True,'data':overlay},{'id':3,'name':'Collision','type':'objectgroup','x':0,'y':0,'opacity':1,'visible':False,'objects':objs},{'id':4,'name':'Spawn','type':'objectgroup','x':0,'y':0,'opacity':1,'visible':True,'objects':[{'id':oid,'name':'Player','type':'spawn','x':layout['spawn'][0],'y':layout['spawn'][1],'point':True}]}],'tilesets':[{'firstgid':1,'name':'town','tilewidth':32,'tileheight':32,'tilecount':16,'columns':8,'image':'tiles.png','imagewidth':256,'imageheight':64,'margin':0,'spacing':0}]}
 (SRC/'plaza.tmj').write_text(json.dumps(m,indent=2)+'\n');(OUT/'plaza.json').write_text(json.dumps(m,separators=(',',':')))
 return m

manifest=[]
for key,s in STYLES.items():
 p=s['palette'];dest=OUT/key;master=SRC/key;dest.mkdir(exist_ok=True);master.mkdir(exist_ok=True);frames={};atlas=Image.new('RGBA',(512,512));pos=0
 def pack(name,im):
  global pos
  x=(pos%8)*64;y=(pos//8)*68;assert y+im.height<512
  atlas.alpha_composite(im,(x+2,y+2));frames[name]={'frame':{'x':x+2,'y':y+2,'w':im.width,'h':im.height},'rotated':False,'trimmed':False,'spriteSourceSize':{'x':0,'y':0,'w':im.width,'h':im.height},'sourceSize':{'w':im.width,'h':im.height}};indexed(im,master/(name+'.png'));pos+=1
 for dr in ('down','left','right','up'):
  for action,n in [('idle',2),('walk',6),('wave',4)]:
   for f in range(n):pack(f'{action}-{dr}-{f}',char(p,dr,f,action,s['hair']))
 atlas.save(dest/'avatar.png',optimize=True);(dest/'avatar.json').write_text(json.dumps({'frames':frames,'meta':{'app':'Original Hangeul Pixel Town exporter','version':'1','image':'avatar.png','format':'RGBA8888','size':{'w':512,'h':512},'scale':'1'}},indent=2))
 imgs={'house':house(p,key),'tiles':tiles(p),**{k:prop(p,k) for k in ['tree','lamp','mailbox','bench','market','bridge','flowers','fence']}}
 for name,im in imgs.items():indexed(im,master/(name+'.png'));im.save(dest/(name+'.png'),optimize=True)
 # contact sheet, exact integer enlargement separate from runtime source.
 sheet=Image.new('RGBA',(320,384),'#'+p['grass']);sheet.alpha_composite(imgs['house'],(48,10));sheet.alpha_composite(imgs['tree'],(2,160));sheet.alpha_composite(imgs['market'],(202,180));sheet.alpha_composite(imgs['mailbox'],(140,240));sheet.alpha_composite(imgs['lamp'],(179,214));sheet.alpha_composite(imgs['bench'],(72,263))
 for i,dr in enumerate(('down','left','right','up')):
  sheet.alpha_composite(char(p,dr,0,'idle',s['hair']),(24+i*70,314))
 sheet.convert('RGB').save(OUT/f'direction-{key}.png')
make_map()
for f in sorted(OUT.rglob('*')):
 if f.is_file():manifest.append({'path':str(f.relative_to(ROOT)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'license':'MIT','provenance':'ORIGINAL_CODE_AUTHORED','author':'Korean Arena Studio','status':'REVIEW_CANDIDATE_NOT_APPROVED'})
(SRC/'manifest.json').write_text(json.dumps({'tile_unit':32,'avatar_canvas':[48,64],'native_avatar_height':49,'atlas_gutter':2,'palette_max':32,'resampling':'none (nearest only in review enlargement)','styles':list(STYLES),'assets':manifest},indent=2)+'\n')
print(json.dumps({'files':len(manifest),'bytes':sum(a['bytes'] for a in manifest),'styles':list(STYLES)}))
