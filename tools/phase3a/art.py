"""Own native NPC construction. Approved sprites supply motion landmarks ONLY, never face/costume pixels."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,math,hashlib,sys
import numpy as np
R=Path(__file__).resolve().parents[2];S=R/'assets-src/npcs/phase3a';P=R/'public/assets/npcs/phase3a';D=R/'docs/phase3a';T=json.loads((R/'assets-src/characters/phase1b-frontback-juni/juni-motion-template.json').read_text())['clips']
K=[[[43,78],[49,84]],[[45,83],[50,76]],[[44,84],[50,73]],[[44,74],[49,84]],[[43,78],[49,84]],[[45,84],[51,76]],[[44,84],[50,75]],[[43,77],[49,84]]]
SPECS=[
('seoyeon','서연','Seoyeon','palace','Hướng dẫn văn hóa','hanbok','bun','#80637b','#d8cead','#363b34','#e3b38d','book'),
('daehyun','대현','Daehyun','palace','Lính gác cung điện','guard','guardhat','#a04544','#3e526d','#242a2b','#c99b75','salute'),
('minseo','민서','Minseo','modern','Barista','apron','ponytail','#94b5a2','#675148','#563c31','#e7bda0','cup'),
('jiho','지호','Jiho','modern','Nhân viên hiệu sách','cardigan','sidepart','#53687a','#dfccb0','#30373c','#d2a487','book'),
('eunji','은지','Eunji','station','Nhân viên ga','uniform','staffcap','#3f586d','#d2c6a8','#302e32','#e4b7a0','ticket'),
('junho','준호','Junho','station','Người đi làm','jacket','tousled','#68726a','#c0a581','#443a33','#d5ad87','schedule'),
('harin','하린','Harin','jeju','Người chăm vườn quýt','vest','softwaves','#d28f48','#e1ce9c','#655039','#dcaf7f','tangerine'),
('seojun','서준','Seojun','jeju','Chủ nhà văn hóa','jeogori','lowtie','#aaa181','#536c69','#282f2d','#c59d7b','present'),
('nayeon','나연','Nayeon','farm','Nông dân','gardener','kerchief','#67765d','#b7aa7b','#827867','#d0aa88','leaf'),
('cheolsu','철수','Cheolsu','farm','Chuyên gia hạt giống','workvest','flatcap','#9d7052','#d4bd89','#605344','#bf9774','seed'),
('yejin','예진','Yejin','nature-leisure','Hướng dẫn Namsan','windbreaker','shortbob','#d2c38a','#547d7a','#3e3531','#e8b799','map'),
('sungmin','성민','Sungmin','nature-leisure','Nhân viên khu vui chơi','staffvest','visor','#d97859','#485f78','#493e39','#dab08d','ticket'),
('donghae','동해','Donghae','coast','Ngư dân','fisher','fishercap','#526d81','#9b9b82','#6b6258','#b98d6e','rope'),
('soobin','수빈','Soobin','coast','Nhân viên bến phà','blazer','braid','#d1cbb7','#65848e','#684b3b','#d5a07b','clipboard')]

def rgb(c):return tuple(bytes.fromhex(c.lstrip('#')))
def tone(c,t):return tuple(max(0,min(255,round(v*t)))for v in rgb(c))
def surface(im,poly,c,shade=1):
 mask=Image.new('L',im.size);ImageDraw.Draw(mask).polygon(poly,fill=255);a=np.array(im);m=np.array(mask)>0;ys,xs=np.where(m)
 if len(xs)==0:return
 lo,hi=xs.min(),xs.max();yy=ys.min()
 # Quantized native material, upper-left light, sparse coherent fibre clusters.
 light=(1.14-(xs-lo)/max(1,hi-lo)*.29-(ys-yy)*.0015);grain=((xs//2*7+ys//3*11)%19==0)*.06;steps=np.round((light+grain)*12)/12*shade
 a[ys,xs,:3]=np.clip(np.array(rgb(c))[None,:]*steps[:,None],0,255).astype(np.uint8);a[ys,xs,3]=255;im.paste(Image.fromarray(a));ImageDraw.Draw(im).line(poly+[poly[0]],fill=tone(c,.58),width=1)
def line(im,points,c,width=1):ImageDraw.Draw(im).line(points,fill=c,width=width)
def limb(im,a,b,width,c,far=False):
 a,b=np.array(a,float),np.array(b,float);v=b-a;length=np.linalg.norm(v)
 if length<.1:return
 n=np.array([-v[1],v[0]])/length*width/2;poly=[tuple(np.round(p).astype(int))for p in [a+n,b+n,b-n,a-n]];surface(im,poly,c,.8 if far else 1);line(im,[tuple(np.round(a+n*.5).astype(int)),tuple(np.round(b+n*.5).astype(int))],tone(c,1.12 if not far else .85))
def shoe(im,sole,c,view,lift,far=False):
 x,y=map(round,sole);sign=-1 if view=='left'else 1;w=7 if view in ['front','back']else 10;hh=5 if lift<3 else 7
 if view in ['front','back']:
  w=7 if lift<3 else 5;poly=[(x-w//2+1,y-hh),(x+w//2-1,y-hh),(x+w//2+1,y-2),(x+w//2,y),(x-w//2,y),(x-w//2-1,y-2)]
 else:poly=[(x-4*sign,y-hh),(x+2*sign,y-hh),(x+6*sign,y-2),(x+6*sign,y),(x-4*sign,y)]
 surface(im,poly,c,.8 if far else 1);line(im,[(min(p[0]for p in poly)+1,y-1),(max(p[0]for p in poly)-1,y-1)],'#c3b491');line(im,[(x-2,y-hh+2),(x+2,y-hh+2)],tone(c,1.5))
def face(im,s,view,dx,dy,i,gesture):
 id,ko,vi,zone,job,cloth,hair,main,accent,hc,skin,prop=s;d=ImageDraw.Draw(im);variant=SPECS.index(s);cx=48+dx;top=15+dy+(variant%3-1);hw=12+(variant%3);front=view=='front';back=view=='back';profile=not front and not back;sign=-1 if view=='left'else 1
 if profile:hw=10;cx+=sign
 # Own editable native head contours, no face pixels imported from any approved actor.
 poly=[(cx-hw+4,top+4),(cx-hw+1,top+10),(cx-hw+2,top+22),(cx-6,top+30),(cx+5,top+31),(cx+hw-1,top+24),(cx+hw,top+11),(cx+hw-4,top+5)]
 surface(im,poly,skin);d=ImageDraw.Draw(im)
 if not back:
  d.rectangle((cx-hw,top+15,cx-hw+2,top+20),fill=tone(skin,.83));d.rectangle((cx+hw-1,top+15,cx+hw+1,top+20),fill=tone(skin,.72))
  ey=top+17;spread=5+(variant%2);eyes=[cx-spread,cx+spread]if front else[cx+sign*5]
  for ex in eyes:
   if gesture and i in [2,6]:d.line((ex-1,ey+1,ex+2,ey+1),fill='#3b2c2b')
   else:d.rectangle((ex-1,ey,ex+1,ey+3),fill='#392c2b');d.point((ex-1,ey),fill='#fbebc9');d.point((ex,ey+2),fill='#886e48')
   d.line((ex-2,ey-3,ex+2,ey-4 if variant%2 else ey-3),fill=tone(hc,.8))
  nx=cx if front else cx+sign*9;
  if profile:d.polygon([(cx+sign*9,top+17),(cx+sign*13,top+21),(cx+sign*9,top+23)],fill=skin,outline=tone(skin,.8))
  d.point((nx,ey+5),fill=tone(skin,.66));d.point((nx-1,ey+4),fill=tone(skin,1.12));d.line((cx-2+sign*int(profile),top+25,cx+2+sign*int(profile),top+25),fill='#935e53');d.point((cx+1,top+26),fill=tone(skin,1.1));d.point((cx-8,top+23),fill='#cb8e76');d.point((cx+8,top+23),fill='#bb816b')
  if id in ['cheolsu','donghae']:d.line((cx-3,top+23,cx+3,top+23),fill=tone(hc,.9));d.point((cx,top+24),fill=hc)
 # Directional own hair silhouettes; back carries crown and neckline details.
 if back:poly=[(cx-hw-1,top+6),(cx-hw+3,top),(cx+hw-4,top-1),(cx+hw+1,top+5),(cx+hw,top+23),(cx+7,top+29),(cx-7,top+28),(cx-hw-2,top+22)]
 else:poly=[(cx-hw-1,top+8),(cx-hw+2,top+2),(cx-3,top-1),(cx+hw-4,top+1),(cx+hw+1,top+8),(cx+hw,top+19),(cx+hw-3,top+23),(cx+hw-3,top+9),(cx+3,top+8),(cx-2,top+12),(cx-6,top+10),(cx-hw+3,top+21),(cx-hw,top+24)]
 if profile:poly=[(cx+sign*9,top+7),(cx-sign*2,top),(cx-sign*8,top+2),(cx-sign*10,top+9),(cx-sign*10,top+25),(cx-sign*5,top+28),(cx-sign*2,top+19),(cx+sign*3,top+13),(cx+sign*7,top+12)]
 surface(im,poly,hc);d=ImageDraw.Draw(im)
 for k in range(-hw+4,hw-2,3):d.line((cx+k,top+4,cx+k-2,top+9+(k%3)),fill=tone(hc,1.25))
 if hair in ['bun','lowtie']:
  bx=cx+(0 if back else -sign*(hw-2) if profile else -hw+1);d.ellipse((bx-5,top-4,bx+5,top+5),fill=tone(hc,.85),outline=tone(hc,.5));d.line((bx-3,top-2,bx+2,top-3),fill=tone(hc,1.45));d.line((bx-4,top+3,bx+4,top+3),fill='#bca975')
 if hair in ['ponytail','braid','softwaves','shortbob','tousled']:
  xx=(cx-sign*(hw-2))if profile else(cx-hw+1 if hair!='braid'else cx+hw-2);length={'ponytail':20,'braid':26,'softwaves':11,'shortbob':8,'tousled':3}[hair];d.polygon([(xx-2,top+16),(xx+4,top+16),(xx+6,top+27),(xx+3,top+25+length),(xx-2,top+20+length),(xx-4,top+23)],fill=tone(hc,.92))
  for yy in range(top+21,top+20+length,3):d.line((xx-1,yy,xx+3,yy+1),fill=tone(hc,1.3))
  d.rectangle((xx-2,top+19,xx+3,top+20),fill=accent)
 if hair=='sidepart':d.polygon([(cx+2,top+2),(cx+hw-2,top+7),(cx+hw,top+14),(cx+4,top+12),(cx-2,top+15)],fill=tone(hc,1.04))
 if hair in ['guardhat','staffcap','flatcap','fishercap','visor','kerchief']:
  hat=main if hair!='kerchief'else accent
  if hair=='guardhat':d.rectangle((cx-8,top-8,cx+8,top+4),fill='#323c40',outline='#20292c');d.line((cx-19,top+4,cx+19,top+4),fill='#253132',width=3);d.line((cx-13,top+3,cx+12,top+3),fill='#ad9566');d.rectangle((cx-3,top-6,cx+2,top-4),fill='#c3a574')
  else:
   d.polygon([(cx-hw-1,top+7),(cx-hw+2,top+1),(cx+hw-4,top),(cx+hw+1,top+7)],fill=tone(hat,.95),outline=tone(hat,.5));d.line((cx-hw-2,top+8,cx+hw+3,top+8),fill=tone(hat,.65),width=3);d.line((cx-hw+1,top+5,cx+hw-2,top+5),fill=tone(accent,1.1))
   if hair=='staffcap':d.rectangle((cx-2,top+3,cx+2,top+5),fill='#dec484')
 if id=='jiho'and not back:
  for ex in ([cx-5,cx+5]if front else[cx+sign*5]):d.rectangle((ex-3,top+16,ex+3,top+21),outline='#bcb292');
  if front:d.line((cx-2,top+18,cx+2,top+18),fill='#bcb292')

def frame(s,view,action,i):
 im=Image.new('RGBA',(96,112));id,ko,vi,zone,job,cloth,hair,main,accent,hc,skin,prop=s;profile=view in ['left','right'];sign=-1 if view=='left'else 1;phase=i/8;t=phase*math.tau;dx=0;dy=0;hands=[];soles=[]
 if action=='walk'and not profile:
  p=T['walk-'+view][i];dx=p['bodyDeltaX'];dy=p['bodyDeltaY'];soles=p['soleScreenLR'];hands=p['handScreenLR']
 elif action=='walk':
  dy=round(-abs(math.sin(t)));soles=[]
  for off in [.5,0]:
   q=(phase+off)%1;x=11-44*q if q<=.5 else -11+22*((q-.5)*2)**2*(3-2*(q-.5)*2);lift=0 if q<=.5 else round(math.sin(math.pi*(q-.5)*2)*7);soles.append([48+sign*round(x),98-lift])
  hands=[[48-sign*round(math.cos(t)*6),70+dy],[48+sign*round(math.cos(t)*6),70+dy]]
 else:
  dy=-int(i%4 in [1,2]);soles=[[42,98],[54,98]]if not profile else[[46,98],[50,98]];hands=[[34,70+dy],[62,70+dy]]if not profile else[[46-sign*4,70+dy],[50+sign*2,70+dy]]
  if action=='greet':hands[1]=[63+round(math.sin(t)*3),37+round(math.cos(t)*3)]if not profile else[48+sign*(13+round(math.sin(t)*2)),40+round(math.cos(t)*3)]
  if action=='activity':hands=[[43+round(math.sin(t)*2),59+dy],[54+round(math.cos(t)*3),57+round(math.sin(t)*2)]]if not profile else[[48+sign*7,59],[48+sign*(12+round(math.cos(t)*2)),58+round(math.sin(t)*3)]]
 # Own limbs with native joints and current Juni phase contacts; no borrowed anatomy pixels.
 legorder=sorted(range(2),key=lambda j:soles[j][1])if not profile else[0,1]
 for j in legorder:
  h=[44+j*8+dx,69+dy]if not profile else[48,69+dy];sole=soles[j];k=K[i][j]if action=='walk'and view=='front'else[round((h[0]+sole[0])/2)+(0 if not profile else sign*3),round((h[1]+sole[1])/2)];a=[sole[0],sole[1]-4];limb(im,h,k,9,accent,j==0 and profile);limb(im,k,a,7,accent,j==0 and profile);shoe(im,sole,'#505049'if cloth not in ['guard','hanbok']else'#53545b',view,98-sole[1],j==0 and profile)
 arms=[]
 for j in range(2):
  arm=Image.new('RGBA',(96,112));shoulder=[38+j*20+dx,50+dy]if not profile else[47+j*2,50+dy];hand=hands[j];elbow=[round((shoulder[0]+hand[0])/2)+(-3 if j==0 else 3),round((shoulder[1]+hand[1])/2)+2];limb(arm,shoulder,elbow,8,main,j==0 and profile);limb(arm,elbow,hand,6,main,j==0 and profile);d=ImageDraw.Draw(arm);d.ellipse((hand[0]-2,hand[1]-2,hand[0]+2,hand[1]+3),fill=skin,outline=tone(skin,.7));d.point((hand[0]-1,hand[1]-1),fill=tone(skin,1.12));arms.append(arm)
 im.alpha_composite(arms[0]);cx=48+dx;long=cloth in ['hanbok','guard'];bottom=87 if long else 71
 torso=[(cx-10,48+dy),(cx+9,48+dy),(cx+12,55+dy),(cx+11,bottom+dy),(cx-12,bottom+dy),(cx-12,56+dy)]if not profile else[(cx-7,48+dy),(cx+7,48+dy),(cx+9,bottom+dy),(cx-8,bottom+dy)]
 surface(im,torso,main);d=ImageDraw.Draw(im)
 # Construction: collars, directional seams and role-specific garments.
 if view!='back':
  d.polygon([(cx-7,48+dy),(cx,54+dy),(cx+7,48+dy),(cx+4,58+dy),(cx-4,58+dy)],fill=accent);d.line((cx-6,48+dy,cx+1,57+dy),fill=tone(accent,1.3));d.line((cx,57+dy,cx,bottom-2+dy),fill=tone(main,.7))
  for y in range(60,bottom-2,6):d.point((cx+2,y+dy),fill='#c5b688')
  d.line((cx-8,62+dy,cx-3,62+dy),fill=tone(main,1.35));d.line((cx+5,62+dy,cx+9,62+dy),fill=tone(main,1.3))
 else:d.line((cx,52+dy,cx,bottom-2+dy),fill=tone(main,.83));d.line((cx-8,55+dy,cx+8,55+dy),fill=tone(main,1.18))
 if cloth in ['hanbok','jeogori','guard']:
  d.line((cx-8,49+dy,cx+5,60+dy),fill=tone(accent,1.1),width=2);d.line((cx-10,61+dy,cx+9,61+dy),fill=accent,width=2)
  if view!='back':d.polygon([(cx+2,59+dy),(cx+7,58+dy),(cx+5,63+dy),(cx+2,62+dy)],fill='#bdae7f');d.line((cx+3,63+dy,cx+6,74+dy),fill='#c2b285',width=2)
  if long:
   for x in range(-9,11,4):d.line((cx+x//2,64+dy,cx+x,bottom-2+dy),fill=tone(main,.8 if x>0 else 1.12))
 if cloth in ['apron','gardener']:
  if view!='back':surface(im,[(cx-6,55+dy),(cx+6,55+dy),(cx+10,78+dy),(cx-10,78+dy)],accent);d=ImageDraw.Draw(im);d.rectangle((cx-5,65+dy,cx+4,71+dy),outline=tone(accent,.65));d.line((cx-7,51+dy,cx-5,57+dy),fill=accent,width=2);d.line((cx+7,51+dy,cx+5,57+dy),fill=accent,width=2)
  else:d.line((cx-8,49+dy,cx+8,69+dy),fill=accent,width=2);d.line((cx+8,49+dy,cx-8,69+dy),fill=accent,width=2)
 if cloth in ['uniform','staffvest','blazer']:d.rectangle((cx-8,57+dy,cx-3,59+dy),fill='#d8c79a');d.point((cx-6,58+dy),fill='#535658')
 if prop in ['map','schedule','rope','seed']:
  d.line((cx-8,49+dy,cx+8,69+dy),fill=tone(accent,.7),width=2);d.rectangle((cx+5,67+dy,cx+13,76+dy),fill=tone(accent,.83),outline=tone(accent,.5));d.line((cx+6,69+dy,cx+11,69+dy),fill=tone(accent,1.25))
 # Neck/head are independent authored identity layers; no player face/costume import.
 d.rectangle((cx-3,42+dy,cx+3,50+dy),fill=skin);face(im,s,view,dx,dy,i,action in ['greet','activity']);im.alpha_composite(arms[1])
 if action=='activity'and view!='back':
  d=ImageDraw.Draw(im);x,y=hands[1];x-=3;y-=1
  if prop=='tangerine':d.ellipse((x-3,y-3,x+3,y+3),fill='#e49c3e',outline='#9a602e');d.point((x-1,y-2),fill='#f4c15f');d.line((x,y-3,x+2,y-5),fill='#708653')
  elif prop in ['book','map','clipboard','schedule','ticket']:d.rectangle((x-9,y-4,x+2,y+5),fill='#c6b98e',outline='#544c47');d.line((x-3,y-3,x-3,y+4),fill='#82745e');d.line((x-7,y-1,x-5,y-1),fill='#687d75');d.line((x-1,y+2,x+1,y+2),fill='#687d75')
  elif prop=='cup':d.rectangle((x-5,y-3,x+1,y+4),fill='#e5dcc1',outline='#807465');d.ellipse((x,y-1,x+4,y+3),outline='#d2c2a6');d.line((x-4,y-2,x,y-2),fill='#654536')
  elif prop in ['leaf','seed']:d.ellipse((x-6,y-5,x+1,y+1),fill='#6b9157',outline='#405b39');d.line((x-4,y-3,x,y),fill='#aab977')
  elif prop=='rope':d.arc((x-7,y-4,x+3,y+6),0,345,fill='#c6b27b',width=2);d.line((x,y+4,x+3,y+7),fill='#9d8c61')
 return im

def build(id):
 s=next(s for s in SPECS if s[0]==id);out=P/('npc-'+id);out.mkdir(parents=True,exist_ok=True);src=S/id;src.mkdir(exist_ok=True);frames={};clips={}
 for view in ['front','back','left','right']:
  for action,n in [('idle',2),('walk',8),('greet',8),('activity',8)]:
   names=[]
   for i in range(n):
    name=f'{action}-{view}-{i}';frames[name]=frame(s,view,action,i if action!='idle'else i*2);names.append(name)
   clips[f'{action}-{view}']={'frames':names,'durationsMs':[600 if action=='idle'else 100 if action=='greet'else 130 if action=='activity'else 92]*n,'loop':action!='greet'}
 atlas=Image.new('RGBA',(768,1456));meta={};qa=[]
 for i,(name,im)in enumerate(frames.items()):
  x=i%8*96;y=i//8*112;atlas.paste(im,(x,y));meta[name]={'frame':{'x':x,'y':y,'w':96,'h':112}};bb=im.getbbox();assert bb and bb[0]>0 and bb[1]>0 and bb[2]<96 and bb[3]<112,(id,name,bb);assert set(np.unique(np.array(im)[:,:,3]))<={0,255}
 atlas.save(out/'atlas.png');(out/'atlas.json').write_text(json.dumps({'frames':meta,'meta':{'size':{'w':768,'h':1456}}},indent=2)+'\n');(src/'clips.json').write_text(json.dumps(clips,indent=2)+'\n')
 for view in ['front','back','left','right']:frames['idle-'+view+'-0'].save(src/(view+'-native.png'))
 frames['idle-front-0'].save(out/'preview-native.png')
 board=Image.new('RGBA',(768,4*136),(29,39,49));dr=ImageDraw.Draw(board)
 for row,view in enumerate(['front','back','left','right']):
  for i in range(8):board.alpha_composite(frames[f'walk-{view}-{i}'],(i*96,row*136+20));dr.text((i*96+2,row*136+3),f'{view}-{i}',fill='white')
 board.save(D/f'{id}-walk-source-native.png');board.resize((1536,1088),Image.Resampling.NEAREST).save(D/f'{id}-walk-source-review-2x.png')
 for key,clip in clips.items():
  unique=len({frames[n].tobytes()for n in clip['frames']});assert not key.startswith('walk')or unique==8,(id,key,unique);qa.append({'clip':key,'frames':len(clip['frames']),'unique':unique})
 spec={'id':'npc-'+id,'names':{'vi':s[2],'ko':s[1]},'occupation':s[4],'homeZone':s[3],'clothing':s[5],'hair':s[6],'palette':list(s[7:11]),'occupationProp':s[11],'method':'Own authored native face contours,hair,occupational clothing and materials. Motion landmarks only from approved Juni; no playable face or costume pixels copied. Reproducible integer pixel construction, not a portrait or palette swap.','native':[96,112],'anchor':[48,100],'frames':104,'walkStride':44,'gaitReference':'assets-src/characters/phase1b-frontback-juni/juni-motion-template.json; accepted positive-X stance convention','sha256':hashlib.sha256((out/'atlas.png').read_bytes()).hexdigest(),'clips':qa,'artApproval':'PENDING'};(src/'design.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n');(out/'provenance.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n');print(id,'own104nativeframes;4x8walk distinct',flush=True)
if __name__=='__main__':
 for id in sys.argv[1:]:build(id)
