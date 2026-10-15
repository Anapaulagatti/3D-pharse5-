"""Reset-v2 production export: original generated object masters + independently
code-authored characters, floor tiles and small props. No old art functions reused.
Source PNG/provenance kept intact. Game-size nearest/palette export is explicit.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import json,math,hashlib,random,os
from collections import deque
R=Path(__file__).resolve().parents[1];S=R/'assets-src/reset-v2';O=R/'public-reset/assets/reset-v2';O.mkdir(parents=True,exist_ok=True)
THEMES={
'A':{'name':'Moonletter Garden','vi':'Thư quán ven hồ','role':'Arin · Người đưa thư','mood':'Một góc hanok yên tĩnh, hiên gỗ bên hồ, thư tay và vườn mơ.','source':'object-master.png','rects':[(0,0,615,492),(615,0,1045,492),(1045,0,1536,506),(0,492,615,1024),(615,492,995,1024),(995,506,1536,1024)],'widths':[256,132,144,152,88,148],'spawn':[448,426],'npc':[404,391],'hero':[448,336],'follow':132,'colors':{'soil':'b6b394','shade':'969d83','grass':'8eaa82','grass2':'92ac84','stone':'cabda6','edge':'a69e8b','light':'e0d3b7','wood':'9a7458','accent':'8eaaa0','dark':'445a55'}},
'B':{'name':'Ginkgo Commons','vi':'Quảng trường Ngân Hạnh','role':'Seoha · Học viên thư quán','mood':'Học viện seowon hai tầng, sân đá có trục gặp gỡ và đài phun sách.','source':'object-master-korean.png','rects':[(0,0,780,530),(775,0,1260,580),(1260,0,1536,590),(0,535,624,1024),(575,530,1090,1024),(1090,585,1536,1024)],'widths':[288,144,88,168,124,144],'spawn':[470,426],'npc':[426,392],'hero':[470,326],'follow':138,'colors':{'soil':'9ca58d','shade':'778d83','grass':'7c9985','grass2':'829d88','stone':'c7c5b4','edge':'a5a89b','light':'d9d4c0','wood':'a18b66','accent':'6d8e94','dark':'425961'}},
'C':{'name':'Hanji Afterhours','vi':'Phố xưởng Hanji','role':'Jun · Người biểu diễn','mood':'Phố xưởng lệch tầng, sân khấu nhỏ và quầy lễ hội rực ánh đèn.','source':'object-master.png','rects':[(0,0,656,544),(660,0,1100,548),(1105,0,1536,550),(0,555,565,1024),(575,565,1020,1024),(1025,555,1536,1024)],'widths':[256,144,124,168,140,128],'spawn':[438,420],'npc':[394,392],'hero':[420,340],'follow':136,'colors':{'soil':'b49b8b','shade':'8e8c89','grass':'879c8b','grass2':'8c9f8d','stone':'bc9c8e','edge':'8b8585','light':'d7b8a1','wood':'a17059','accent':'668a8d','dark':'3e555f'}}}
NAMES=['house','tree1','tree2','feature','kiosk','decor']
# Native48x64 hero system. Each role has its own silhouette/outfit, not recolours.
P={'ink':'253241','edge':'414350','hair':'34313e','hairHi':'625163','skin':'efbb91','skinHi':'ffdfb4','skinSh':'bc8270','cheek':'e69586','white':'fff0cd','cream':'d8c8a5','shadow':'746e69','jade':'73a69a','jadeHi':'acd0b6','jadeSh':'456f72','coral':'ce706a','coralHi':'efab8d','coralSh':'914d5b','navy':'3a5069','navyHi':'647b91','navySh':'29394e','gold':'d9ab61','goldHi':'f7db91','goldSh':'9c7849','purple':'876a97','purpleHi':'bc91b1','purpleSh':'614f79','teal':'568c96','tealHi':'8bc2bf','tealSh':'38636e','shoe':'614a46','shoeHi':'b18b70','paper':'f9e2b6','paperSh':'baa38b','rose':'df8799','metal':'a1bdc1'}
class Draw:
 def __init__(self,w,h,p):self.im=Image.new('RGBA',(w,h));self.d=ImageDraw.Draw(self.im);self.p=p
 def c(self,k):return '#'+self.p[k]
 def r(self,b,k):self.d.rectangle(tuple(int(v) for v in b),fill=self.c(k))
 def l(self,pts,k,w=1):self.d.line([(int(x),int(y)) for x,y in pts],fill=self.c(k),width=w)
 def poly(self,pts,k):self.d.polygon([(int(x),int(y)) for x,y in pts],fill=self.c(k))
 def el(self,b,k):self.d.ellipse(tuple(int(v) for v in b),fill=self.c(k))

def character(style,dr,action,f):
 a=Draw(48,64,P);side=dr in ('left','right');back=dr=='up';phase=[0,1,2,1,0,-1,-2,-1][f%8] if action=='walk' else 0
 bob=(-1 if f%4 in (1,2) else 0) if action=='walk' else (1 if action=='idle' and f==2 else 0)
 wave=action=='wave';lift=[0,2,7,10,7,2][f%6] if wave else 0;cy=17+bob
 # Grounded shoes and alternating planted/swing feet; full native frame occupancy.
 for x,s in [(15,phase),(28,-phase)]:
  y=56-(max(0,s));a.r((x,48,x+6,y+4),'navySh' if style=='A' else 'cream');a.r((x-1,y+3,x+7,y+6),'ink');a.r((x,y+3,x+6,y+4),'shoeHi');a.r((x+1,y+5,x+7,y+5),'shoe')
 if style=='A':
  # Long split riding coat, scarf tails, short hanbok-like wrap and messenger bag.
  a.poly([(14,31+bob),(32,31+bob),(39,49),(35,55),(27,53),(23,55),(10,54),(8,49)],'ink')
  a.poly([(15,32+bob),(31,32+bob),(35,50),(27,52),(23,48),(20,53),(11,52)],'jadeSh');a.poly([(15,33+bob),(28,33+bob),(26,47),(19,51),(12,50)],'jade');a.l([(14,35),(12,46),(15,49)],'jadeHi')
  a.poly([(12,30+bob),(35,31+bob),(36,35+bob),(24,37+bob),(12,34+bob)],'coral');a.r((13,31+bob,32,32+bob),'coralHi');a.poly([(30,34),(35,35),(38,43+phase//2),(32,41)],'coralSh')
  a.l([(16,34),(31,45)],'cream',2);a.r((31,41+bob,43,52+bob),'ink');a.r((32,42+bob,42,50+bob),'goldSh');a.r((32,42+bob,42,45+bob),'gold');a.l([(33,43+bob),(37,46+bob),(41,43+bob)],'white');a.r((36,46+bob,38,47+bob),'goldHi')
  a.r((8,36-phase,13,45-phase),'jadeSh');a.r((8,43-phase,12,46-phase),'white');a.r((9,46-phase,12,48-phase),'skin')
  a.r((33,33-lift,38,42-lift),'jade');a.r((33,40-lift,38,43-lift),'white');a.r((34,44-lift,37,46-lift),'skin')
  if wave:a.r((36,35-lift,44,41-lift),'paper');a.l([(36,35-lift),(40,38-lift),(44,35-lift)],'coralSh')
 elif style=='B':
  # Broad academic beret, cropped ivory coat over navy pleats, glasses, held book.
  a.poly([(11,32+bob),(35,32+bob),(42,48),(36,53),(11,53),(5,47)],'ink');a.poly([(12,33+bob),(33,33+bob),(37,49),(11,49),(8,44)],'cream');a.poly([(13,34+bob),(23,36+bob),(22,47),(10,47)],'white');a.l([(29,34),(27,47)],'paperSh');a.r((21,36,25,46),'navy');a.r((22,36,24,38),'gold')
  a.poly([(12,49),(35,49),(38,57),(11,57)],'navySh')
  for x in [14,20,27,33]:a.r((x,50,x+2,56),'navyHi')
  a.r((6,36,11,45),'white');a.r((7,44,11,47),'skin');a.r((34,35-lift,40,45-lift),'cream');a.r((34,43-lift,39,46-lift),'skin')
  a.r((3,40-lift//2,15,52-lift//2),'ink');a.r((4,40-lift//2,14,50-lift//2),'navy');a.r((5,41-lift//2,6,49-lift//2),'gold');a.r((8,43-lift//2,12,44-lift//2),'goldHi');a.r((5,51-lift//2,14,51-lift//2),'paper')
 else:
  # Short open creative jacket, asymmetric bandana and loose cyan trousers.
  a.poly([(12,32+bob),(34,32+bob),(40,45),(33,49),(11,49),(6,44)],'ink');a.r((12,34+bob,34,45),'purpleSh');a.r((14,34+bob,22,44),'purpleHi');a.r((25,34+bob,33,44),'purple');a.r((22,34+bob,26,44),'white');a.l([(22,35),(25,41)],'gold');a.poly([(25,31),(33,31),(35,36),(29,35)],'coral');a.poly([(31,35),(36,35),(40,43+phase//2),(34,41)],'coralHi')
  a.r((11,45,23,56),'tealSh');a.r((25,45,36,56),'teal');a.r((13,46,20,49),'teal');a.r((26,46,33,48),'tealHi');a.r((12,54,22,58),'navySh');a.r((26,54,36,58),'navySh')
  for x,hand in [(6,phase+lift),(35,-phase+lift)]:
   a.r((x,35-hand,x+6,43-hand),'purple');a.r((x,41-hand,x+6,44-hand),'tealHi');a.r((x+1,45-hand,x+5,47-hand),'skin')
  a.r((34,43,41,50),'navySh');a.r((35,44,40,48),'gold');a.r((37,45,39,47),'ink')
  if wave:a.r((3,30-lift,5,37-lift),'goldHi');a.r((1,33-lift,7,34-lift),'white')
 # Head has role-specific contours, side/back identity and expressive open eyes.
 if not side:
  a.poly([(10,cy-10),(16,cy-16),(31,cy-16),(38,cy-10),(39,cy+6),(32,cy+14),(15,cy+14),(9,cy+6)],'ink');a.poly([(12,cy-9),(17,cy-14),(30,cy-14),(36,cy-8),(36,cy+6),(31,cy+12),(16,cy+12),(11,cy+6)],'skin');a.r((15,cy+6,32,cy+10),'skinHi');a.r((10,cy+2,13,cy+6),'skinSh')
 else:
  a.poly([(14,cy-14),(29,cy-15),(37,cy-8),(38,cy),(42,cy+3),(40,cy+7),(34,cy+8),(30,cy+13),(16,cy+12),(11,cy+5)],'ink');a.poly([(17,cy-12),(29,cy-12),(35,cy-7),(35,cy+2),(40,cy+4),(37,cy+6),(31,cy+10),(17,cy+10),(13,cy+4)],'skin');a.l([(20,cy+9),(30,cy+9)],'skinHi',2)
 if back:
  a.poly([(11,cy-12),(17,cy-16),(31,cy-16),(38,cy-9),(38,cy+8),(32,cy+14),(15,cy+13),(9,cy+5)],'hair');a.l([(15,cy-10),(13,cy+5),(18,cy+10)],'hairHi')
  if style=='A':a.r((18,35,31,49),'goldSh');a.r((18,35,31,40),'gold');a.l([(19,36),(24,40),(30,36)],'paper')
  elif style=='B':a.r((14,33,33,48),'navySh');a.r((16,34,31,46),'navy');a.r((18,38,29,40),'gold')
  else:a.r((18,37,30,42),'coralHi');a.r((23,35,25,44),'goldHi')
 else:
  if style=='A':a.poly([(10,cy-9),(14,cy-15),(25,cy-17),(34,cy-13),(37,cy-7),(31,cy-6),(28,cy-10),(23,cy-5),(20,cy-9),(15,cy-3),(13,cy+7),(10,cy+3)],'hair');a.l([(15,cy-11),(21,cy-14),(28,cy-13)],'hairHi',2)
  elif style=='B':a.poly([(10,cy-8),(15,cy-15),(29,cy-16),(36,cy-10),(37,cy-3),(31,cy-3),(26,cy-9),(21,cy-6),(15,cy-5),(12,cy+4),(9,cy+2)],'hair');a.l([(14,cy-9),(23,cy-12),(29,cy-10)],'hairHi')
  else:a.poly([(8,cy-9),(11,cy-16),(18,cy-14),(22,cy-18),(28,cy-14),(35,cy-15),(40,cy-9),(35,cy-3),(32,cy-7),(27,cy-4),(22,cy-8),(15,cy-3),(11,cy+4)],'hair');a.l([(13,cy-11),(21,cy-13),(28,cy-10)],'hairHi',2)
  for x in ([29] if side else [17,30]):
   if action=='idle' and f==1:a.r((x-2,cy+3,x+2,cy+3),'ink')
   else:a.r((x-2,cy+1,x+2,cy+5),'ink');a.r((x-1,cy+1,x,cy+2),'white');a.r((x+1,cy+4,x+1,cy+5),'navyHi')
  if not side:a.r((12,cy+6,16,cy+7),'cheek');a.r((32,cy+6,35,cy+7),'cheek');a.l([(22,cy+8),(24,cy+9),(26,cy+8)],'coralSh')
  if style=='B':
   for x in ([29] if side else [17,30]):a.d.rectangle((x-4,cy-1,x+4,cy+7),outline=a.c('goldSh'))
   if not side:a.r((22,cy+2,25,cy+2),'goldSh')
 hbob=bob+1
 # Headwear gives independent large readable silhouettes.
 if style=='A':a.el((26,0+hbob,37,8+hbob),'hair');a.r((28,1+hbob,34,2+hbob),'hairHi');a.poly([(29,5+hbob),(38,2+hbob),(40,8+hbob),(32,9+hbob)],'paper');a.l([(32,5+hbob),(37,5+hbob)],'gold')
 elif style=='B':a.poly([(5,6+hbob),(12,1+hbob),(32,0+hbob),(42,4+hbob),(43,9+hbob),(35,12+hbob),(9,11+hbob)],'navySh');a.poly([(7,6+hbob),(14,3+hbob),(30,2+hbob),(39,5+hbob),(36,8+hbob),(10,9+hbob)],'navy');a.l([(13,4+hbob),(29,3+hbob)],'navyHi',2);a.r((30,7+hbob,34,9+hbob),'gold')
 else:
  a.poly([(33,5+hbob),(39,0+hbob),(45,2+hbob),(47,9+hbob),(44,18+hbob+phase//2),(39,15+hbob),(40,8+hbob)],'hair');a.l([(40,3+hbob),(44,6+hbob),(43,12+hbob)],'hairHi');a.l([(7,15+hbob),(8,7+hbob),(17,3+hbob),(29,4+hbob),(38,10+hbob)],'metal',2)
  for x in ([10,36] if not side else [14]):a.r((x-3,14+hbob,x+3,24+hbob),'ink');a.r((x-2,15+hbob,x+2,22+hbob),'gold');a.r((x-1,16+hbob,x,20+hbob),'tealHi')
 if dr=='left':return a.im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
 return a.im

def indexed(im,path,maxcol=64):
 alpha=im.getchannel('A').point(lambda x:255 if x>=128 else 0);rgb=im.convert('RGB').quantize(colors=maxcol,dither=Image.Dither.NONE);out=rgb.convert('RGBA');out.putalpha(alpha)
 # Transparent RGB zero; clean deterministic export.
 out.putdata([(r,g,b,a) if a else (0,0,0,0) for r,g,b,a in out.get_flattened_data()]);out.save(path,optimize=True);return out

def tiles(style,c):
 a=Draw(256,128,c);rng=random.Random(441+ord(style))
 for n in range(32):
  x=(n%8)*32;y=(n//8)*32
  if n<4:
   a.r((x,y,x+31,y+31),'grass' if n<3 else 'grass2')
   for _ in range(n%3):
    px=x+rng.randrange(3,28);py=y+rng.randrange(3,28);a.l([(px,py+1),(px+1,py-1),(px+2,py+1)],'shade')
  elif n<12:
   a.r((x,y,x+31,y+31),'edge')
   if style=='A':
    a.poly([(x+2,y+3),(x+16,y+1),(x+30,y+5),(x+29,y+16),(x+18,y+18),(x+2,y+14)],'stone');a.poly([(x+1,y+19),(x+17,y+20),(x+29,y+18),(x+31,y+29),(x+17,y+31),(x+2,y+29)],'stone');a.l([(x+4,y+4),(x+14,y+3)],'light')
   elif style=='B':
    a.r((x+1,y+1,x+30,y+30),'stone');a.l([(x+1,y+1),(x+30,y+1),(x+30,y+28)],'light');a.l([(x+2,y+30),(x+30,y+30)],'shade')
    if n%3==0:a.l([(x+7,y+7),(x+25,y+7)],'light')
   else:
    for row in range(4):
     for col in range(3):
      xx=x+col*14-(7 if row%2 else 0);yy=y+row*8;a.r((max(x,xx),yy+1,min(x+31,xx+12),yy+6),'stone');a.l([(max(x,xx),yy+1),(min(x+31,xx+11),yy+1)],'light')
  elif n<16:
   a.r((x,y,x+31,y+31),'stone');a.r((x,y,x+31,y+5),'edge');a.l([(x,y+1),(x+31,y+1)],'light');a.l([(x,y+6),(x+31,y+6)],'shade')
  elif n<20:
   a.r((x,y,x+31,y+31),'wood')
   for yy in range(y,y+32,8):a.l([(x,yy),(x+31,yy)],'shade');a.l([(x,yy+1),(x+31,yy+1)],'light')
  elif n<24:
   a.r((x,y,x+31,y+31),'accent');a.l([(x+2,y+11),(x+13,y+11)],'light');a.l([(x+18,y+25),(x+28,y+25)],'light');a.l([(x,y),(x+31,y)],'dark')
  else:
   a.r((x,y,x+31,y+31),'soil')
   if n==24:a.poly([(x+16,y+3),(x+29,y+16),(x+16,y+29),(x+3,y+16)],'accent');a.poly([(x+16,y+8),(x+24,y+16),(x+16,y+24),(x+8,y+16)],'stone')
   else:
    for j in range(3):
     xx=x+rng.randrange(3,28);yy=y+rng.randrange(3,28);a.r((xx,yy,xx+2,yy+1),'shade')
 # Restrained stone grain/chips, not screen-wide particle noise.
 rng=random.Random(902+ord(style));pix=a.im.load()
 for yy in range(0,64):
  for xx in range(0,256):
   if rng.random()<.035 and pix[xx,yy][:3]==tuple(bytes.fromhex(c['stone'])):
    base=tuple(bytes.fromhex(c['stone']));d=-7 if (xx+yy)%2 else 5;pix[xx,yy]=tuple(max(0,min(255,v+d)) for v in base)+(255,)
 return a.im

def small(kind,style):
 a=Draw(64,64,P);wood='navy' if style=='B' else 'shoeHi';light='cream' if style=='B' else 'gold';accent={'A':'jade','B':'navy','C':'coral'}[style]
 if kind=='bench':
  for x in (9,48):a.poly([(x,39),(x+5,37),(x+6,54),(x,56)],'ink')
  a.poly([(5,33),(49,27),(60,34),(15,42)],'shoe');a.poly([(15,42),(60,34),(60,39),(15,47)],'shoeHi');a.poly([(5,33),(15,42),(15,47),(5,39)],'ink')
  for yy in (15,22):a.poly([(5,yy),(50,yy-6),(51,yy-1),(6,yy+5)],wood);a.l([(7,yy),(48,yy-5)],light)
  a.r((5,17,8,37),'ink');a.r((50,10,53,33),'ink')
 elif kind in ('planter','shrub'):
  # Smaller coherent planter: substantial front/right planes, rim thickness,
  # varied small leaf clusters and tiny flowers rather than three balloon dots.
  a.poly([(21,39),(39,35),(48,40),(46,54),(31,59),(22,54)],'ink')
  a.poly([(23,42),(32,47),(32,56),(25,52)],'goldSh' if style!='B' else 'navySh')
  a.poly([(32,47),(46,41),(44,52),(32,56)],'shoe' if style!='B' else 'navy')
  for y in (46,50,54):a.l([(33,y),(43,y-3)],'shoeHi' if style!='B' else 'navyHi')
  a.poly([(20,38),(39,33),(49,39),(31,46)],'cream');a.poly([(24,38),(39,35),(45,39),(31,43)],'jadeSh');a.l([(23,40),(31,45),(47,39)],'gold' if style!='B' else 'paper')
  rng=random.Random(46+ord(style))
  for j in range(35):
   x=rng.randrange(21,45);y=rng.randrange(21,40);r=rng.randrange(2,5)
   a.poly([(x-r,y),(x-1,y-r),(x+r,y-1),(x+1,y+r)],'jadeSh');a.l([(x-r+1,y),(x-1,y-r+1),(x+1,y-1)],'jade')
   if j%3==0:a.l([(x-1,y-r+1),(x+1,y-r+1)],'jadeHi')
  for x,y in [(24,24),(35,22),(41,32),(29,34),(37,37)]:
   a.r((x-2,y,x+2,y+1),'paper');a.r((x,y-2,x+1,y+2),'paper');a.r((x,y,x,y),'gold')
 elif kind=='crate':
  a.poly([(6,23),(40,16),(56,26),(20,35)],'gold');a.poly([(20,35),(56,26),(56,53),(20,61)],'shoe');a.poly([(6,23),(20,35),(20,61),(6,49)],'goldSh')
  for y in (34,42,50):a.l([(22,y+2),(54,y-5)],'goldSh')
  a.l([(21,38),(53,52)],'shoeHi',3);a.r((19,10,30,21),'paper');a.l([(19,10),(25,16),(30,10)],'coral')
 elif kind=='lamp':
  a.poly([(24,54),(35,52),(42,57),(31,62),(22,59)],'ink');a.r((29,16,33,57),'shoe');a.r((30,18,31,55),'shoeHi');a.r((19,11,42,16),'navySh');a.r((22,17,39,33),'goldSh');a.r((24,17,36,30),'goldHi');a.r((29,18,33,29),'white');a.r((23,31,38,34),'shoe');a.l([(30,35),(30,41)],'gold')
 elif kind=='sign':
  a.r((28,35,33,59),'shoe');a.poly([(9,13),(46,8),(53,32),(15,39)],'shoe');a.poly([(12,15),(44,11),(49,30),(17,35)],'paper');a.r((23,18,35,27),accent);a.l([(21,19),(30,25),(39,16)],'goldSh',2);a.l([(22,29),(37,26)],'shoe')
 else:
  for x,y in [(16,36),(26,29),(37,33),(43,22)]:a.l([(x,y),(x-2,52)],'jadeSh');a.el((x-4,y-2,x+4,y+3),'coral');a.r((x-2,y-4,x+2,y+5),'coralHi');a.r((x,y,x+1,y+1),'goldHi')
 return a.im

def component_mask(alpha):
 w,h=alpha.size;data=bytearray(alpha.tobytes());best=[]
 for start in range(w*h):
  if data[start]==0:continue
  data[start]=0;q=deque([start]);component=[]
  while q:
   n=q.popleft();component.append(n);x=n%w;y=n//w
   for dy in (-1,0,1):
    for dx in (-1,0,1):
     xx=x+dx;yy=y+dy
     if 0<=xx<w and 0<=yy<h:
      nn=yy*w+xx
      if data[nn]:data[nn]=0;q.append(nn)
  if len(component)>len(best):best=component
 out=bytearray(w*h)
 for n in best:out[n]=255
 return Image.frombytes('L',(w,h),bytes(out))

def export_objects(k,t):
 im=Image.open(S/k/t['source']).convert('RGBA');dest=O/k;dest.mkdir(parents=True,exist_ok=True);meta={}
 for i,(name,rect,width) in enumerate(zip(NAMES,t['rects'],t['widths'])):
  crop=im.crop(rect);alpha=crop.getchannel('A').point(lambda x:255 if x>=144 else 0)
  # Explicit atlas separation polygons for B source layout; preserve original master.
  if k=='B' and name=='tree1':
   mask=ImageDraw.Draw(alpha);mask.rectangle((0,540-rect[1],980-rect[0],crop.height),fill=0)
  alpha=component_mask(alpha);crop.putalpha(alpha);bb=alpha.getbbox();assert bb,(k,name);crop=crop.crop(bb);h=round(crop.height*width/crop.width);source=S/k/(name+'-crop.png');crop.save(source);scaled=crop.resize((width,h),Image.Resampling.NEAREST);img=indexed(scaled,dest/(name+'.png'),128)
  meta[name]={'width':width,'height':h,'source_rect':rect,'trim':bb,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'palette_limit':128,'anchor':[.5,1]}
 return meta

def world(k,t,meta):
 w,h=30,24;rng=random.Random(ord(k));ground=[];border=[]
 for y in range(h):
  for x in range(w):
   if k=='A':road=(11<=x<=17 and 9<=y<=20) or (6<=x<=22 and 13<=y<=15) or (18<=x<=21 and 12<=y<=17)
   elif k=='B':road=(7<=x<=24 and 8<=y<=19) or (13<=x<=16 and y>=5)
   else:
    cx=12+(y-8)//3;road=(cx-3<=x<=cx+4 and y>=8) or (6<=x<=23 and y in (12,13,14))
   n=(5+rng.randrange(7)) if road else 1+rng.randrange(4)
   if k=='B' and road and (x in (8,23) or y in (9,18)):n=25
   if k=='A' and y==21:n=21+(x%3)
   if k=='A' and y==21 and 12<=x<=16:n=17+(x%3)
   ground.append(n);border.append(13 if (k=='A' and y==20 and not 12<=x<=16) else 0)
 hero=t['hero'];props=[{'kind':'house','x':hero[0],'y':hero[1],'id':'hero'}]
 specs={
 'A':[('tree1',244,330),('tree2',672,350),('feature',230,458),('kiosk',620,354),('decor',614,492),('tree1',214,625),('tree2',786,572),('bench',356,526),('bench',520,580),('sign',380,370),('lamp',319,390),('lamp',555,393)],
 'B':[('tree1',235,312),('tree2',746,341),('feature',661,500),('kiosk',266,407),('decor',426,576),('tree2',280,563),('tree1',780,616),('bench',578,565),('sign',541,361),('lamp',346,386),('lamp',585,380)],
 'C':[('tree1',216,336),('tree2',744,350),('feature',650,436),('kiosk',256,526),('decor',628,585),('tree2',204,623),('tree1',800,640),('crate',555,371),('crate',590,390),('sign',346,386),('lamp',316,404),('lamp',539,423)]}
 for i,(kind,x,y) in enumerate(specs[k]):props.append({'kind':kind,'x':x,'y':y,'id':f'{kind}-{i}'})
 # Rich but composed planters and handcrafted story scatter flank walking routes.
 extras={'A':[(326,348),(565,345),(337,500),(538,536),(285,466),(723,452),(390,611),(530,645)],'B':[(345,339),(593,338),(339,513),(603,590),(220,464),(730,483),(402,646),(548,646)],'C':[(308,361),(557,335),(566,470),(364,538),(670,641),(246,434),(484,610),(744,490)]}
 for i,(x,y) in enumerate(extras[k]):props.append({'kind':'planter','x':x,'y':y,'id':f'planter-{i}'})
 for i,(x,y) in enumerate(extras[k][::2]):props.append({'kind':'flowers','x':x+40,'y':y+10,'id':f'flowers-{i}'})
 solid=[]
 for p in props:
  kind=p['kind'];ww=meta[kind]['width'] if kind in meta else 64
  if kind=='house':box=(p['x']-ww*.39,p['y']-48,ww*.78,42)
  elif kind.startswith('tree'):box=(p['x']-12,p['y']-16,24,14)
  elif kind in ('feature','kiosk','decor'):box=(p['x']-ww*.36,p['y']-ww*.23,ww*.72,ww*.21)
  elif kind in ('planter','bench','crate','sign','lamp'):box=(p['x']-13,p['y']-15,26,13)
  else:continue
  solid.append({'id':len(solid)+1,'name':p['id'],'type':'solid','x':round(box[0]),'y':round(box[1]),'width':round(box[2]),'height':round(box[3])})
 if k=='A':
  for x,ww in [(0,384),(544,416)]:solid.append({'id':len(solid)+1,'name':'pond-bank','type':'solid','x':x,'y':672,'width':ww,'height':32})
 layers=[{'id':1,'name':'Ground','type':'tilelayer','width':w,'height':h,'x':0,'y':0,'opacity':1,'visible':True,'data':ground},{'id':2,'name':'Edging','type':'tilelayer','width':w,'height':h,'x':0,'y':0,'opacity':1,'visible':True,'data':border},{'id':3,'name':'Collision','type':'objectgroup','x':0,'y':0,'opacity':1,'visible':False,'objects':solid},{'id':4,'name':'Spawn','type':'objectgroup','x':0,'y':0,'opacity':1,'visible':True,'objects':[{'id':len(solid)+1,'name':'Player','type':'spawn','x':t['spawn'][0],'y':t['spawn'][1],'point':True}]}]
 m={'type':'map','orientation':'orthogonal','renderorder':'right-down','infinite':False,'tilewidth':32,'tileheight':32,'width':w,'height':h,'version':'1.10','tiledversion':'1.12.2','nextlayerid':5,'nextobjectid':len(solid)+2,'layers':layers,'tilesets':[{'firstgid':1,'name':'town','tilewidth':32,'tileheight':32,'tilecount':32,'columns':8,'image':'tiles.png','imagewidth':256,'imageheight':128,'margin':0,'spacing':0}]}
 (S/k/'plaza.tmj').write_text(json.dumps(m,indent=2)+'\n');(O/k/'plaza.json').write_text(json.dumps(m,separators=(',',':')))
 return {'name':t['name'],'vi':t['vi'],'role':t['role'],'mood':t['mood'],'width':960,'height':768,'spawn':t['spawn'],'npc':t['npc'],'follow':t['follow'],'objects':props,'objectMeta':meta,'collisionCount':len(solid),'groundColor':t['colors']['grass'],'mapSha256':hashlib.sha256((O/k/'plaza.json').read_bytes()).hexdigest()}
worlds={}
for k,t in THEMES.items():
 dest=O/k;master=S/k;meta=export_objects(k,t)
 for kind in ['bench','planter','crate','lamp','sign','flowers']:
  indexed(small(kind,k),dest/(kind+'.png'));meta[kind]={'width':64,'height':64,'source':'original code-authored','anchor':[.5,1]}
 indexed(tiles(k,t['colors']),dest/'tiles.png',64)
 atlas=Image.new('RGBA',(512,1024));frames={};i=0
 for dr in ['down','left','right','up']:
  for action,count in [('idle',4),('walk',8),('wave',6)]:
   for f in range(count):
    name=f'{action}-{dr}-{f}';img=indexed(character(k,dr,action,f),master/(name+'.png'),64);x=(i%8)*52+2;y=(i//8)*68+2;atlas.alpha_composite(img,(x,y));frames[name]={'frame':{'x':x,'y':y,'w':48,'h':64},'rotated':False,'trimmed':False,'spriteSourceSize':{'x':0,'y':0,'w':48,'h':64},'sourceSize':{'w':48,'h':64}};i+=1
 atlas.save(dest/'avatar.png',optimize=True);(dest/'avatar.json').write_text(json.dumps({'frames':frames,'meta':{'app':'Original reset-v2 exporter','image':'avatar.png','size':{'w':512,'h':1024},'scale':'1'}},indent=2)+'\n')
 worlds[k]=world(k,t,meta)
 # Contact board uses exact runtime assets, not a different concept rendering.
 board=Image.new('RGBA',(448,448),'#'+t['colors']['grass']);board.alpha_composite(Image.open(dest/'house.png'),(12,10));board.alpha_composite(Image.open(dest/'tree1.png'),(300,12));board.alpha_composite(Image.open(dest/'feature.png'),(262,202))
 for i,dr in enumerate(['down','left','right','up']):board.alpha_composite(character(k,dr,'idle',0).resize((96,128),Image.Resampling.NEAREST),(16+i*108,310))
 board.save(O/f'direction-{k}.png')
(O/'worlds.json').write_text(json.dumps(worlds,ensure_ascii=False,indent=2)+'\n');(S/'worlds.json').write_text(json.dumps(worlds,ensure_ascii=False,indent=2)+'\n')
files=[{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'provenance':'ORIGINAL_NATIVE_IMAGE_GEN_OBJECTS_AND_ORIGINAL_CODE_SPRITES','review':'NOT_APPROVED'} for p in sorted(O.rglob('*')) if p.is_file()]
(S/'manifest.json').write_text(json.dumps({'version':'reset-v2','tile':32,'hero_frame':[48,64],'gameplay_camera':2,'frames_per_direction':{'idle':4,'walk':8,'wave':6},'frames_per_style':72,'source_masters_preserved':True,'export':'Explicit atlas crops, alpha144binary, NEAREST game-size export, <=128colour/object; no source image overwritten','files':files},indent=2)+'\n')
print(json.dumps({'files':len(files),'bytes':sum(p['bytes'] for p in files),'worlds':{k:{'props':len(v['objects']),'collisions':v['collisionCount'],'hero':v['objectMeta']['house']} for k,v in worlds.items()}}))
