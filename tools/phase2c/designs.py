"""Authored native Korean fashion designs. Raster ownership comes from APPROVED
poses, not an old body renderer. Coordinates are head/torso registered, never screen
accessories. No base art is exported. Palettes/material panels and contour recipes
are versioned source artwork; every claimed pairing gets its own112/144 cells.
"""
from core import *
import colorsys,sys
from PIL import ImageDraw
IDS=['juni','haneul','bomi','minjun','ara','doyun','sori','jiwon','nari','taeyang','yuna','hyunwoo']
PAIRS=[['juni','sori'],['haneul','jiwon'],['bomi','nari'],['minjun','taeyang'],['ara','yuna'],['doyun','hyunwoo']]
NAMES={
 'hairstyle':[('classic-bob','Tóc bob Hàn cổ điển','Korean Classic Bob','클래식 단발'),('soft-waves','Tóc gợn sóng mềm','Soft Wavy Hair','부드러운 웨이브'),('traditional-braid','Tóc tết truyền thống','Traditional Braided Hair','전통 땋은머리'),('layered-cut','Tóc tỉa tầng hiện đại','Modern Layered Cut','레이어드 컷'),('high-ponytail','Tóc đuôi ngựa cao','High Ponytail','하이 포니테일'),('side-part','Tóc ngắn rẽ ngôi','Side-Part Short Hair','짧은 가르마 머리')],
 'outfit':[('daily-hanbok','Hanbok thường ngày','Modern Daily Hanbok','생활 한복'),('festival-hanbok','Hanbok lễ hội','Traditional Festival Hanbok','축제 한복'),('campus','Phong cách sân trường','Korean Campus Fashion','캠퍼스 룩'),('seoul-streetwear','Dạo phố Seoul','Seoul Streetwear','서울 스트리트웨어'),('jeju-explorer','Khám phá Jeju','Jeju Explorer Outfit','제주 탐험복'),('garden-workwear','Bộ làm vườn','Korean Farm & Garden Outfit','정원 작업복')],
 'accessory':[('hair-ornament','Nơ cài tóc truyền thống','Traditional Hair Ornament','전통 머리 장식'),('backpack','Ba lô dạo chơi','Casual Backpack','캐주얼 배낭'),('round-glasses','Kính tròn','Round Glasses','동그란 안경'),('fashion-cap','Mũ lưỡi trai Hàn','Korean Fashion Cap','패션 볼캡'),('crossbody','Túi đeo chéo nhỏ','Small Crossbody Bag','작은 크로스백'),('garden-hat','Mũ làm vườn','Gardening Hat','정원 모자')]}
T=json.loads((R/'assets-src/characters/phase1b-frontback-juni/juni-motion-template.json').read_text())['clips']
def viewof(name,base,frames):
 parts=name.split('-')
 if len(parts)>2:return parts[1]
 # Juni's turn cells are real authored intermediate views, not new directions.
 a=np.array(base)[24:45,32:65];scores=[]
 for v in ['front','back','left','right']:
  b=np.array(frames['idle-'+v+'-0'])[24:45,32:65];scores.append((np.abs(a.astype(int)-b.astype(int)).mean(),v))
 return min(scores)[1]
def registration(im,reference):
 a=np.array(im);b=np.array(reference);best=(1e9,0,0)
 for dy in range(-3,4):
  for dx in range(-3,4):
   aa=a[24+dy:43+dy,38+dx:59+dx,:3];bb=b[24:43,38:59,:3];mask=(np.array(reference)[24:43,38:59,3]>0)
   score=np.abs(aa.astype(float)-bb.astype(float))[mask].mean()
   if score<best[0]:best=(score,dx,dy)
 return best[1:]
def shifted(im,dx,dy):
 out=Image.new('RGBA',(96,112));out.alpha_composite(im,(dx,dy));return out

def skincolors(frames):
 a=np.array(frames['idle-front-0']);colors=a[33:44,40:57,:3].reshape(-1,3).astype(int);return {tuple(x)for x in colors if x[0]>95 and x[0]-x[1]>16 and x[1]-x[2]>7}
def skinmask(im,colors):
 a=np.array(im);mask=np.zeros(a.shape[:2],bool)
 for c in colors:mask|=np.all(a[:,:,:3]==c,2)
 yy,xx=np.indices(mask.shape);return mask&(((xx<44)|(xx>54))|(yy<54))&(yy<80)&(a[:,:,3]>0)

def feet(id,name,im):
 a=np.array(im);yy,xx=np.indices(a.shape[:2]);mask=np.zeros((112,96),bool);bits=name.split('-');action=bits[0];i=int(bits[-1]);v=bits[1]if len(bits)>2 else'front'
 if v in ['front','back']and action in ['walk','run']:
  guidepath=R/f'assets-src/characters/phase2b-walkfront/{id}/guide.json';poses=[]
  if guidepath.exists()and name.startswith('walk-front'):poses=next(r['landmarks']for r in json.loads(guidepath.read_text())['poses']if r['frame']==name);soles=[p['sole']for p in poses]
  else:soles=T[action+'-'+v][i]['soleScreenLR']
  for x,y in soles:mask|=(abs(xx-x)<=8)&(yy>=y-7)&(yy<=y+1)
 else:
  # Shoe pixels retain contact, approved outlines and their source material.
  bright=(a[:,:,0]>135)&(a[:,:,1]>115)&(a[:,:,2]>90)&(yy>=80)&(a[:,:,3]>0)
  for dy in range(-2,3):
   for dx in range(-2,3):mask|=np.roll(bright,(dy,dx),(0,1))
  mask|=yy>=93
 return mask&(a[:,:,3]>0)

HAIR_PALETTES=[[(35,22,22),(57,32,28),(85,48,35),(113,68,44),(139,87,53),(158,105,66),(177,126,81)],[(36,22,27),(62,34,36),(88,50,43),(116,68,50),(143,91,63),(163,112,81),(180,135,100)],[(26,22,29),(45,32,40),(66,44,46),(86,59,55),(107,76,65),(131,96,78),(153,118,95)],[(16,25,35),(26,38,52),(39,51,65),(53,64,76),(70,80,92),(89,98,107),(111,118,122)],[(30,21,28),(51,31,35),(77,44,43),(104,60,48),(127,79,56),(149,101,70),(170,122,86)],[(18,22,28),(30,34,41),(43,46,53),(56,58,65),(72,74,78),(91,92,94),(111,111,110)]]
def hairstyle(style,v,base,reference):
 dx,dy=registration(base,reference);mask=Image.new('1',(96,112));dr=ImageDraw.Draw(mask)
 # Individually authored contours, with different frontal/rear/profile topology.
 if style==0:poly=[(34,27),(39,23),(49,22),(58,25),(62,31),(63,43),(60,47),(55,47),(53,41),(42,41),(40,47),(34,46),(32,40),(32,32)]
 elif style==1:poly=[(34,27),(40,23),(51,23),(58,26),(62,32),(61,36),(65,40),(63,45),(66,49),(62,53),(57,52),(55,47),(40,47),(37,53),(31,51),(30,46),(33,42),(30,38),(32,32)]
 elif style==2:poly=[(34,28),(40,24),(49,23),(57,26),(61,31),(61,39),(57,45),(53,46),(42,46),(36,43),(33,37)]
 elif style==3:poly=[(31,31),(34,27),(39,25),(42,22),(48,24),(54,22),(56,26),(62,28),(61,33),(64,36),(60,41),(58,44),(54,40),(41,42),(35,44),(35,40),(31,37),(33,34)]
 elif style==4:poly=[(33,30),(37,26),(43,24),(53,24),(59,28),(61,34),(59,42),(55,45),(39,45),(34,40),(32,35)]
 else:poly=[(33,30),(37,26),(46,23),(54,24),(60,28),(62,34),(60,41),(57,43),(54,39),(39,40),(36,44),(33,40)]
 if v in ['left','right']:
  # True profile silhouette; crown volume and visible sideburn shift together.
  sign=-1 if v=='left'else 1;poly=[(x+sign*2,y)for x,y in poly]
 dr.polygon(poly,fill=1)
 if style==2 and v=='back':dr.polygon([(44,40),(53,40),(55,47),(51,51),(54,55),(50,59),(51,63),(46,65),(44,61),(46,56),(43,51)],fill=1)
 if style==4:
  tail=[(54,26),(61,25),(64,30),(64,41),(61,46),(63,53),(60,60),(55,64),(53,59),(56,52),(55,44),(53,36)]if v!='back'else[(45,25),(54,25),(57,31),(56,42),(59,49),(55,57),(54,63),(48,65),(46,61),(48,53),(45,44),(44,34)]
  dr.polygon(tail,fill=1);dr.ellipse((51,22,59,29),fill=1)
 arr=np.array(mask);out=Image.new('RGBA',(96,112));p=np.array(out);pal=HAIR_PALETTES[style]
 for y,x in zip(*np.where(arr)):
  edge=not(0<x<95 and 0<y<111 and arr[y-1,x]and arr[y+1,x]and arr[y,x-1]and arr[y,x+1]);light=max(0,1-((x-42)/24)**2-((y-29)/26)**2);strand=((x*3+y*2+style)%9==0);shade=0 if edge else max(1,min(6,round(light*4.5)+1+(1 if strand and x<53 else 0)));p[y,x]=[*pal[shade],255]
 out=Image.fromarray(p);d=ImageDraw.Draw(out)
 if v!='back':
  # Deliberate fringe placement remains above the approved eye line.
  for k in range(5):
   x=37+k*4;d.line((x,27+(k%2),x-2+(style%3),32),fill=(*pal[2+k%3],255))
  if style in [2,5]:d.line((47 if style==2 else 52,25,46 if style==2 else 50,31),fill=(*pal[5],255))
 else:
  for x in range(37,59,4):d.line((x,29,x+1,43),fill=(*pal[2+(x//4)%3],255))
 if style==2 and v=='back':
  for y in range(46,62,4):d.line((46,y,51,y+3),fill=(*pal[4],255));d.line((51,y,46,y+3),fill=(*pal[1],255))
  d.polygon([(45,61),(50,62),(54,60),(54,65),(50,64),(45,66)],fill=(157,67,64,255));d.point((49,62),fill=(239,177,118,255))
 if style==4:d.rectangle((53 if v!='back'else 46,25,60 if v!='back'else 54,27),fill=(176,79,65,255))
 out=shifted(out,dx,dy);a=np.array(base);ref=np.array(shifted(reference,dx,dy));yy,xx=np.indices(a.shape[:2]);headregion=(yy<47)&(xx>=27+dx)&(xx<=69+dx);erase=headregion&(a[:,:,3]>0)
 face={'front':(40,33,56,44),'back':None,'left':(35,33,50,44),'right':(46,33,61,44)}[v];preserve=np.zeros((112,96),bool)
 if face:
  x0,y0,x1,y1=face;preserve[y0+dy:y1+dy,x0+dx:x1+dx]=True;preserve[43+dy:47+dy,41+dx:55+dx]=True
 # Raised hands/sleeves outside the resting head silhouette remain foreground.
 foreground=(a[:,:,3]>0)&(ref[:,:,3]==0)&(yy<47);p=np.array(out);p[preserve|foreground]=0;erase&=~(preserve|foreground)
 if v!='back':p[(yy>=47)&(a[:,:,3]>0)]=0
 out=Image.fromarray(p);e=np.zeros_like(a);e[erase]=255;return out,Image.fromarray(e)

CLOTH=[((83,140,154),(217,203,170),(240,228,194)),((143,64,77),(49,116,121),(237,217,170)),((45,67,102),(171,148,114),(234,222,183)),((59,70,78),(68,78,96),(189,98,76)),((103,155,142),(129,108,80),(235,213,162)),((226,211,169),(75,104,122),(137,164,157))]
def outfit(style,id,name,base,frames):
 a=np.array(base);yy,xx=np.indices(a.shape[:2]);v=viewof(name,base,frames);dx,dy=registration(base,frames['idle-'+v+'-0']);protect=skinmask(base,skincolors(frames))|feet(id,name,base);mask=(a[:,:,3]>0)&(yy>=47+dy)&~protect
 neck=(xx>=43+dx)&(xx<=53+dx)&(yy<51+dy);mask&=~neck
 p=a.copy();top,bottom,trim=CLOTH[style];lum=a[:,:,:3].astype(float)@np.array([.299,.587,.114]);active=lum[mask];lo,hi=(np.percentile(active,[5,95])if len(active)else[0,255]);strength=np.clip((lum-lo)/max(35,hi-lo),0,1);factor=.46+.72*(np.round(strength*5)/5)
 for ch in range(3):p[:,:,ch][mask]=np.clip((np.where(yy<67+dy,top[ch],bottom[ch])*factor)[mask],0,255).astype('uint8')
 material=Image.fromarray(p);design=Image.new('RGBA',(96,112));d=ImageDraw.Draw(design);x=48+dx;y=dy
 def line(points,c,w=1):d.line([(int(a+dx),int(b+y))for a,b in points],fill=(*c,255),width=w)
 def rect(box,c):d.rectangle((box[0]+dx,box[1]+y,box[2]+dx,box[3]+y),fill=(*c,255))
 if style in [0,1]:
  if v=='front':
   line([(41,49),(50,60),(55,50)],trim,2);line([(42,50),(49,59)],tuple(int(c*.58)for c in trim));rect((39,62,57,63),trim);d.polygon([(51+dx,58+y),(57+dx,57+y),(56+dx,61+y),(51+dx,60+y)],fill=(*trim,255));line([(53,60),(52,67),(55,69)],trim)
  elif v=='back':line([(40,50),(48,53),(56,50)],trim,2);line([(48,53),(48,63)],tuple(int(c*.75)for c in top))
  else:line([(46,49),(49,54),(49,63)],trim,2)
  if style==1:
   # Authored chima panels, animated by current native foot/waist phase.
   hem=89+y;left=35+dx;right=62+dx
   if v in ['left','right']:left=36+dx;right=60+dx
   skirt=Image.new('RGBA',(96,112));sd=ImageDraw.Draw(skirt);sd.polygon([(41+dx,64+y),(55+dx,64+y),(right,hem-1),(left,hem)],fill=(*bottom,255))
   for i in range(6):
    tx=42+dx+i*2;bx=left+2+i*(right-left-4)//5;sd.line((tx,66+y,bx,hem-1),fill=(*tuple(max(0,int(c*(.68 if i%2 else 1.16)))for c in bottom),255))
   sd.line((left+1,hem-1,right-1,hem-2),fill=(*trim,255));s=np.array(skirt);s[protect]=0;material.alpha_composite(Image.fromarray(s));line([(54,64),(55,73)],(206,161,69));rect((54,72,56,75),(207,162,68))
 elif style==2:
  if v=='front':rect((45,50,51,66),trim);line([(41,49),(45,59),(43,64)],(25,40,68),2);line([(55,49),(51,59),(54,65)],(24,40,66),2);rect((53,55,55,58),(209,166,74));rect((40,66,56,68),trim);line([(40,67),(56,67)],(92,113,148))
  elif v=='back':rect((41,53,55,56),trim);line([(43,58),(53,58)],trim);rect((39,67,57,69),trim)
  else:line([(49,50),(47,60),(48,67)],trim,2);rect((42,67,54,69),trim)
 elif style==3:
  if v=='front':rect((45,49,51,67),trim);line([(48,50),(48,69)],(31,39,50));line([(44,49),(43,55)],(211,204,171));line([(52,49),(53,55)],(211,204,171));rect((40,58,44,62),(109,131,142));rect((52,64,57,66),(140,76,64))
  elif v=='back':d.ellipse((39+dx,48+y,57+dx,57+y),outline=(24,33,44,255),width=2);rect((41,60,55,64),(132,80,66));line([(43,62),(53,62)],trim)
  else:line([(46,50),(49,56),(48,69)],(24,32,42),2);rect((43,60,49,63),trim)
 elif style==4:
  if v=='front':line([(48,49),(48,69)],(42,91,88));rect((40,55,45,62),(207,195,159));rect((51,55,56,62),(207,195,159));line([(41,57),(44,57)],(104,105,87));line([(52,57),(55,57)],(104,105,87));rect((40,66,56,68),(76,112,101));rect((47,66,49,68),trim)
  elif v=='back':line([(39,54),(57,54)],trim,2);rect((43,58,53,61),(78,119,110));rect((42,67,54,68),trim)
  else:line([(46,51),(49,55),(49,69)],trim);rect((43,57,49,63),(207,195,159))
 else:
  if v=='front':
   d.polygon([(43+dx,51+y),(53+dx,51+y),(55+dx,63+y),(60+dx,82+y),(37+dx,82+y),(41+dx,63+y)],fill=(82,123,132,255));line([(43,51),(41,60)],trim);line([(53,51),(55,60)],trim);rect((41,69,54,76),(133,167,160));line([(42,70),(53,70)],trim);line([(48,70),(48,76)],(61,96,107));line([(38,81),(59,81)],trim)
  elif v=='back':line([(42,50),(54,66)],(79,116,126),2);line([(54,50),(42,66)],(79,116,126),2);rect((40,66,56,68),(79,116,126));line([(48,67),(44,71)],trim);line([(48,67),(53,71)],trim)
  else:line([(47,50),(47,64),(52,80)],(79,116,126),2);rect((47,66,53,77),(79,116,126))
 # Garment seams follow native cloth ownership; no detached screen-space props.
 de=np.array(design);de[~mask]=0;material.alpha_composite(Image.fromarray(de));desired=np.array(material);desired[protect]=a[protect];desired[:47]=a[:47];return diff(base,Image.fromarray(desired))

def accessory(style,v,base,reference,colors):
 dx,dy=registration(base,reference);p=Image.new('RGBA',(96,112));d=ImageDraw.Draw(p);erase=Image.new('RGBA',(96,112));e=ImageDraw.Draw(erase)
 if style==0:
  x=55 if v in ['front','left']else 41;y=31
  d.polygon([(x-5,y-2),(x,y),(x-5,y+3),(x-7,y+1)],fill=(166,61,70,255));d.polygon([(x,y),(x+5,y-3),(x+6,y),(x+4,y+3)],fill=(194,80,83,255));d.rectangle((x-1,y-1,x+1,y+1),fill=(226,184,91,255));d.point((x,y-1),fill=(255,226,152,255));d.line((x,y+2,x-2,y+7),fill=(157,61,71,255))
 elif style==1:
  if v=='back':
   d.rounded_rectangle((38,51,57,72),radius=4,fill=(63,112,117,255),outline=(29,65,78,255));d.line((40,54,42,52,53,52),fill=(139,185,172,255));d.rounded_rectangle((41,63,54,70),radius=2,fill=(87,143,140,255),outline=(39,83,92,255));d.rectangle((46,56,49,58),fill=(226,196,137,255));d.line((42,64,53,64),fill=(151,188,167,255))
  elif v=='front':
   d.line((40,50,39,64,42,69),fill=(39,78,87,255),width=3);d.line((55,50,57,64,54,69),fill=(39,78,87,255),width=3);d.line((40,51,40,64),fill=(128,170,153,255));d.line((55,51,56,64),fill=(128,170,153,255))
  else:
   x=51 if v=='left'else 33;d.rounded_rectangle((x,52,x+12,72),radius=3,fill=(63,112,117,255),outline=(29,65,78,255));d.line((x+2,55,x+9,55),fill=(139,185,172,255));d.rectangle((x+3,63,x+9,69),fill=(87,143,140,255));d.line((x+3,53,x+3,69),fill=(43,84,94,255))
 elif style==2:
  if v=='front':
   for x in [40,50]:d.rounded_rectangle((x,34,x+6,39),radius=2,outline=(58,46,40,255));d.line((46,36,50,36),fill=(58,46,40,255));d.point((41,34),fill=(205,186,140,255));d.point((51,34),fill=(205,186,140,255))
  elif v!='back':
   x=36 if v=='left'else 53;d.rounded_rectangle((x,34,x+6,39),radius=2,outline=(58,46,40,255));d.line((x+5 if v=='left'else x-7,35,x+13 if v=='left'else x,35),fill=(69,55,43,255))
 elif style in [3,5]:
  e.rectangle((27,18,69,33),fill=(255,255,255,255));cloth=(51,70,86,255)if style==3 else(206,174,105,255);edge=(27,43,60,255)if style==3 else(120,93,53,255);light=(103,126,141,255)if style==3 else(244,216,151,255)
  d.polygon([(33,29),(35,25),(41,22),(53,22),(60,26),(62,30),(60,33),(34,33)],fill=cloth,outline=edge);d.line((37,26,42,24,52,24),fill=light);d.line((48,23,49,30),fill=edge)
  if style==5:
   d.ellipse((29,28,66,35),fill=cloth,outline=edge);d.line((32,30,40,29,57,29,63,31),fill=light);d.rectangle((34,28,60,30),fill=(81,113,105,255))
   for x in range(36,61,4):d.line((x,25,x-1,28),fill=light)
  elif v=='back':d.rectangle((43,29,53,32),fill=edge);d.rectangle((46,30,51,30),fill=(188,145,88,255))
  else:
   bx=28 if v=='left'else 53 if v=='right'else 34;bw=17 if v!='front'else 29;d.polygon([(bx,30),(bx+bw,30),(bx+bw+2,32),(bx+1,34)],fill=edge);d.line((bx+2,31,bx+bw,31),fill=light)
 elif style==4:
  if v in ['front','back']:
   d.line((41,49,57,68),fill=(59,74,81,255),width=2);d.line((42,50,57,67),fill=(188,163,115,255));d.rounded_rectangle((53,65,63,76),radius=2,fill=(63,84,98,255),outline=(31,49,66,255));d.rectangle((54,66,62,69),fill=(103,127,133,255));d.point((58,69),fill=(224,186,104,255));d.line((55,73,61,73),fill=(138,155,144,255))
  else:
   x=49 if v=='left'else 38;d.line((48,50,x+4,68),fill=(183,158,112,255),width=2);d.rounded_rectangle((x,65,x+10,76),radius=2,fill=(63,84,98,255),outline=(31,49,66,255));d.line((x+2,68,x+8,68),fill=(140,156,143,255))
 p=shifted(p,dx,dy);erase=shifted(erase,dx,dy);a=np.array(p);protect=skinmask(base,colors);yy,xx=np.indices(protect.shape)
 if style in [1,4]:a[protect& (yy>=47)]=0
 # Hat brim never hides the approved eyes; glasses deliberately overlay rims.
 if style in [3,5]:a[(yy>=34+dy)&(xx>=39+dx)&(xx<=57+dx)]=0
 p=Image.fromarray(a);return p,erase

def make(category,style,targets):
 spec=NAMES[category][style];itemid='kr-'+spec[0];variants=[];previews=[]
 for id in targets:
  frames=load(id);patches={};colors=skincolors(frames)
  for name,base in frames.items():
   v=viewof(name,base,frames);ref=frames['idle-'+v+'-0']
   patch=hairstyle(style,v,base,ref)if category=='hairstyle'else outfit(style,id,name,base,frames)if category=='outfit'else accessory(style,v,base,ref,colors);patches[name]=patch
  preview=apply(frames['idle-front-0'],patches['idle-front-0']);variants.append(save(itemid,id,patches,preview,'Authored native Korean fashion contours/material construction in tools/phase2c/designs.py; approved frame ownership and foot-contact masks'));previews.append((id,frames,patches))
  board=Image.new('RGBA',(768,528),(28,30,38));dr=ImageDraw.Draw(board)
  for row,k in enumerate(['walk-front','walk-back','walk-right','run-front']):
   for i in range(8):board.alpha_composite(apply(frames[f'{k}-{i}'],patches[f'{k}-{i}']),(i*96,row*132+20))
   dr.text((3,row*132+2),itemid+' '+id+' '+k,fill='white')
  board.save(D/f'{itemid}-{id}-native.png')
 return {'id':itemid,'name':dict(zip(['vi','en','ko'],spec[1:])),'category':category,'compatibility':{'characterIds':targets},'variants':variants,'availability':{'status':'free-review','reason':'Native authored directional variant; current approved base pose binding; human Phase2C art review pending','acquisition':{'kind':'free-review'}}}
