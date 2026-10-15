"""Provisionally accepted native chibi identity, authored animation poses. Code-drawn, no image model."""
from PIL import Image,ImageDraw
import math
P={'ink':'#302d3d','edge':'#504252','skinD':'#b97568','skinM':'#df9d7d','skin':'#f4c8a1','skinL':'#ffe0b8','blush':'#dc8d87','white':'#fff0d2','iris':'#436a73','irisL':'#79b6ab','hairD':'#272c3d','hairM':'#424456','hair':'#626376','hairL':'#858797','brownD':'#543747','brownM':'#80505a','brown':'#ab7569','brownL':'#ce9b7f','jadeD':'#345a5b','jade':'#548780','jadeL':'#8bb4a0','jadeH':'#bdd0ad','navyD':'#343c56','navy':'#52617d','navyL':'#7f93a0','creamD':'#b7a88e','cream':'#e8d4ab','goldD':'#af7a46','gold':'#e6b66b','coralD':'#9f4d55','coral':'#d47b72','coralL':'#edac90','shoeD':'#353440','shoe':'#665460','shoeL':'#99838a','bagD':'#684552','bag':'#ad7763','bagL':'#d8a67b'}
A={'idle':6,'walk':12,'run':12,'wave':8,'celebrate':10,'pose':6,'think':8,'start':3,'stop':3,'turn':3};D=['down','left','right','up'];L=['body','outfit0','outfit1','hair0','hair1','satchel','hands']+['face-'+x for x in ['neutral','happy','focused','surprised']];W,H=48,64
def draw(key):
 a,dr,n=key.split('-');i=int(n);side=dr in ['left','right'];sign=1 if dr=='right' else -1
 running=a=='run';walking=a=='walk';moving=running or walking
 phase=i*2*math.pi/(12 if moving else A[a])
 dy=([0,0,0,-1,-1,0][i] if a=='idle' else [0,1,0,-1,0,0,0,1,0,-1,0,0][i] if walking else [0,-1,-2,-1,0,1,0,-1,-2,-1,0,1][i] if running else [1,1,0][i] if a=='start' else [-1,1,0][i] if a=='stop' else [0,0,1][i] if a=='turn' else [1,1,0,-2,-3,-2,0,1,0,0][i] if a=='celebrate' else 0)
 lean=(sign*2 if side else round(math.sin(phase))) if running else round(math.sin(phase)*.7) if walking else 0
 cx=20+lean;cy=17+dy
 legs=[]
 for j in [-1,1]:
  p=(i/12+(0 if j==1 else .5))%1
  if moving:
   stance=.50 if running else .60
   if p<stance:reach=(11 if running else 8)*(1-2*p/stance);lift=0
   else:
    u=(p-stance)/(1-stance);reach=(11 if running else 8)*(-1+2*u);lift=round(math.sin(u*math.pi)*(7 if running else 4))
   fx=20+(sign*round(reach) if side else j*4+round(math.sin(phase)*.5))
   fy=53-lift if side else 53-round(reach*.24)-lift
   knee=(round((20+j*3+fx)/2)+(sign*2 if side and lift else 0),47+dy-(2 if lift else 0))
  else:fx=20+j*4;fy=52;knee=(18+j*4,47+dy)
  legs.append((j,fx,min(53,fy),knee))
 ims={k:Image.new('RGBA',(W,H)) for k in L};ds={k:ImageDraw.Draw(v) for k,v in ims.items()}
 def poly(k,pts,c):ds[k].polygon([(x+4,y+8) for x,y in pts],fill=P.get(c,c))
 def rect(k,box,c):
  x,y,xx,yy=box
  if xx>=x and yy>=y:ds[k].rectangle((x+4,y+8,xx+4,yy+8),fill=P.get(c,c))
 def line(k,pts,c,width=1):ds[k].line([(x+4,y+8) for x,y in pts],fill=P.get(c,c),width=width)
 # Near/far legs alternate contacts. Supporting foot travels backward in local space;
 # runtime phase is driven by actual travelled distance, not a wall-clock loop.
 stride=round(math.sin(phase)* (7 if running else 5)) if moving else 0
 for j,fx,fy,knee in legs:
  if moving:
   line('body',[(18+j*3+lean,43+dy),knee,(fx,fy-1)],'ink',5)
   line('body',[(18+j*3+lean,43+dy),knee,(fx,fy-1)],'skin' if j==1 else 'skinD',3)
   rect('body',(fx-3,fy-1,fx+3,fy+2),'shoeD');rect('body',(fx-2,fy-1,fx+2,fy),'shoe' if j==-1 else 'shoeL')
  else:
   fx=20+j*4;fy=52
   poly('body',[(16+j*4+lean,42+dy),(21+j*4+lean,42+dy),(fx+2,fy),(fx-3,fy)],'ink')
   line('body',[(18+j*4+lean,43+dy),(fx,fy-1)],'skin' if j<0 else 'skinM',3)
   rect('body',(fx-3,fy-1,fx+3,min(55,fy+2)),'shoeD');rect('body',(fx-2,fy-1,fx+2,fy),'shoe');rect('body',(fx-2,fy-1,fx,fy-1),'shoeL')
 # Explicit profile has protruding nose/chin, ear and shifted jaw; back has nape only.
 if side:
  def pt(x,y):return (cx+sign*x,cy+y)
  shape=[pt(-12,-9),pt(-8,-14),pt(4,-14),pt(11,-9),pt(12,-1),pt(13,2),pt(12,5),pt(11,5),pt(10,11),pt(4,14),pt(-6,13),pt(-12,8)]
  poly('body',shape,'ink');poly('body',[pt(-10,-8),pt(-7,-12),pt(3,-12),pt(9,-8),pt(10,0),pt(11,2),pt(10,3),pt(8,10),pt(3,12),pt(-5,11),pt(-10,7)],'skinM')
  poly('body',[pt(-2,-9),pt(7,-7),pt(8,0),pt(11,2),pt(8,4),pt(7,9),pt(2,11),pt(-2,9)],'skin');rect('body',(cx-2,cy+12,cx+2,cy+17),'skinD')
 else:
  poly('body',[(cx-10,cy-13),(cx+8,cy-13),(cx+14,cy-7),(cx+14,cy+6),(cx+10,cy+12),(cx+5,cy+15),(cx-6,cy+15),(cx-12,cy+11),(cx-15,cy+5),(cx-15,cy-5)],'ink')
  poly('body',[(cx-10,cy-11),(cx+7,cy-11),(cx+12,cy-6),(cx+12,cy+5),(cx+9,cy+10),(cx+4,cy+13),(cx-5,cy+13),(cx-10,cy+9),(cx-13,cy+4),(cx-13,cy-4)],'skinM')
  poly('body',[(cx-10,cy-8),(cx+6,cy-9),(cx+10,cy-5),(cx+10,cy+5),(cx+6,cy+10),(cx-4,cy+11),(cx-10,cy+7),(cx-12,cy+1)],'skin')
  rect('body',(cx-8,cy-4,cx+5,cy+1),'skinL');rect('body',(cx-3,cy+13,cx+3,cy+17),'skinD')
  if dr=='up':
   poly('body',[(cx-9,cy-8),(cx+9,cy-8),(cx+10,cy+7),(cx+5,cy+12),(cx-5,cy+12),(cx-10,cy+7)],'skinM');line('body',[(cx-4,cy+13),(cx+3,cy+13)],'skinD')
 # Shoulders below chin, hands separated from torso. Frontward bent elbows on emotes.
 hands=[(8,42+dy+stride//2),(32,42+dy-stride//2)]
 if side:
  hands=[(cx-sign*stride,40+dy-round(math.cos(phase)*2)),(cx+sign*stride,42+dy+round(math.cos(phase)*2))] if moving else [(cx-4,41+dy),(cx+4,43+dy)]
 if a=='wave':hands[1]=(37,[40,36,24,12,10,14,22,38][i]+dy)
 if a=='celebrate':hands=[(2,[42,40,32,22,12,10,15,25,35,41][i]+dy),(37,[42,40,32,22,12,10,15,25,35,41][i]+dy)]
 if a=='pose':hands=[(9,40+dy),(32,[38,34,32,31,34,38][i]+dy)]
 if a=='think':hands=[(9,41+dy),(24,[38,35,32,30,29,30,33,38][i]+dy)]
 if a in ['start','stop','turn']:hands=[(8+lean,41+dy),(32+lean,41+dy)]
 for outfit in [0,1]:
  k='outfit'+str(outfit);dark,mid,hi=('jadeD','jade','jadeL') if outfit==0 else ('navyD','navy','navyL')
  for j,fx,fy,knee in legs:
   if outfit==0:rect(k,(14+4*j+lean,40+dy,21+4*j+lean,45+dy),dark);rect(k,(15+4*j+lean,41+dy,20+4*j+lean,43+dy),'cream')
   elif moving:
    line(k,[(18+j*3+lean,42+dy),knee,(fx,fy-1)],'navyD',5);line(k,[(18+j*3+lean,42+dy),knee,(fx,fy-1)],'navyL' if j==1 else 'navy',2)
   else:
    fx=20+j*4;fy=51
    line(k,[(18+j*4+lean,42+dy),(fx,fy-1)],'navyD',5);line(k,[(18+j*4+lean,42+dy),(fx,fy-1)],'navyL',2)
  if side:
   poly(k,[(cx-6,32+dy),(cx+5,32+dy),(cx+8,41+dy),(cx+5,45+dy),(cx-5,45+dy),(cx-7,40+dy)],'ink')
   poly(k,[(cx-5,33+dy),(cx+4,33+dy),(cx+6,41+dy),(cx+4,43+dy),(cx-4,43+dy),(cx-5,39+dy)],dark)
   poly(k,[(cx-sign*4,34+dy),(cx+sign*2,34+dy),(cx+sign*4,42+dy),(cx-sign*3,42+dy)],mid);line(k,[(cx-sign*4,35+dy),(cx-sign*4,40+dy)],hi)
  else:
   poly(k,[(13+lean,32+dy),(26+lean,32+dy),(28,41+dy),(25,45+dy),(14,45+dy),(11,41+dy)],'ink')
   poly(k,[(14+lean,33+dy),(25+lean,33+dy),(26,41+dy),(24,43+dy),(15,43+dy),(13,41+dy)],dark)
   poly(k,[(14+lean,33+dy),(20+lean,34+dy),(21,42+dy),(15,42+dy),(13,39+dy)],mid);line(k,[(14+lean,34+dy),(14,39+dy)],hi)
  for j,(x,y) in enumerate(hands):
   shoulder=(14+lean if j==0 else 25+lean,34+dy)
   elbow=(6 if j==0 else 34,35+dy) if y<30 else (x,38+dy)
   line(k,[shoulder,elbow,(x,y-3)],'ink',5);line(k,[shoulder,elbow,(x,y-3)],mid,3);line(k,[shoulder,elbow],hi)
  if dr=='up':
   line(k,[(15+lean,35+dy),(24+lean,35+dy)],hi);rect(k,(18+lean,36+dy,21+lean,39+dy),'cream' if outfit else 'jadeL')
   if outfit:rect(k,(18+lean,36+dy,21+lean,37+dy),'gold')
  elif side:
   line(k,[(cx-sign*4,33+dy),(cx+sign*4,34+dy)],'coralL' if outfit==0 else 'cream',2)
   if outfit==0:poly(k,[(cx-sign*4,34+dy),(cx-sign*7,35+dy),(cx-sign*7,41+dy),(cx-sign*4,40+dy)],'coral')
   else:rect(k,(cx+sign*3,37+dy,cx+sign*3+1,39+dy),'gold')
  elif outfit==0:
   poly(k,[(13+lean,32+dy),(20+lean,35+dy),(26+lean,32+dy),(25+lean,35+dy),(20+lean,38+dy),(15+lean,35+dy)],'coralD');line(k,[(14+lean,33+dy),(20+lean,35+dy),(25+lean,33+dy)],'coralL',2)
   poly(k,[(22+lean,35+dy),(25+lean,36+dy),(27+(round(math.sin(phase-.7)*2) if moving else 0),42+dy),(23,41+dy)],'coral');rect(k,(15+lean,38+dy,17+lean,40+dy),'gold')
  else:
   poly(k,[(16+lean,33+dy),(23+lean,33+dy),(21+lean,42+dy),(18+lean,42+dy)],'cream');poly(k,[(13+lean,33+dy),(18+lean,36+dy),(16+lean,39+dy)],hi);poly(k,[(25+lean,33+dy),(22+lean,36+dy),(24+lean,39+dy)],mid);rect(k,(24,37+dy,26,39+dy),'gold');rect(k,(19,36+dy,20,38+dy),'coralD')
 for x,y in hands:
  # Hands placed on body outside cloth to keep fingers readable.
  rect('hands',(x-2,y-2,x+2,y+2),'skinD');rect('hands',(x-1,y-2,x+1,y+1),'skinL')
 # Four facial moods as independently selectable registered overlays. Back has no pasted face.
 for mood in ['neutral','happy','focused','surprised']:
  k='face-'+mood
  if dr=='up':continue
  eyes=[(-6,3),(6,3)] if not side else [(7*sign,3)]
  blink=a=='idle' and i in [1,2];happy=mood=='happy' or a=='celebrate';focus=mood=='focused' or a in ['pose','think'];surprise=mood=='surprised'
  for ex,ey in eyes:
   x=cx+ex;y=cy+ey
   if blink:line(k,[(x-2,y+3),(x+2,y+3)],'edge');line(k,[(x-1,y+4),(x+1,y+4)],'skinD')
   elif happy:line(k,[(x-2,y+3),(x-1,y+1),(x+1,y+1),(x+2,y+3)],'ink');rect(k,(x-2,y+5,x+2,y+5),'blush')
   else:
    rect(k,(x-2,y,x+2,y+5),'ink');rect(k,(x-1,y+1,x+2,y+4),'white');rect(k,(x-1,y+1,x+1,y+4),'iris');rect(k,(x,y+1,x+1,y+3),'ink');rect(k,(x-1,y+1,x-1,y+2),'white');rect(k,(x,y+4,x+1,y+4),'irisL')
    if focus:line(k,[(x-2,y-2),(x+2,y-1)],'edge')
    elif surprise:line(k,[(x-2,y-3),(x+2,y-3)],'edge')
   if not side:rect(k,(x-2,cy+10,x+1,cy+10),'blush')
  mx=cx if not side else cx+sign*10
  if surprise:rect(k,(mx-1,cy+10,mx+1,cy+12),'coralD');rect(k,(mx,cy+10,mx,cy+10),'skinD')
  elif happy:line(k,[(mx-2,cy+10),(mx-1,cy+12),(mx+1,cy+12),(mx+2,cy+10)],'coralD');rect(k,(mx,cy+12,mx+1,cy+12),'coralL')
  else:line(k,[(mx-1,cy+11),(mx+1,cy+11)],'coralD');rect(k,(mx-1,cy+10,mx,cy+10),'skinL')
  if side:rect(k,(cx-sign*2,cy+5,cx-sign*2+1,cy+8),'skinD')
 # Sculpted hair cap, asymmetrical fringe, nape and direction-specific mass.
 for h in [0,1]:
  k='hair'+str(h);hd,hm,hc,hl=('hairD','hairM','hair','hairL') if h==0 else ('brownD','brownM','brown','brownL')
  if side:
   def hp(x,y):return (cx+sign*x,cy+y)
   poly(k,[hp(-15,7),hp(-16,-4),hp(-11,-13),hp(-4,-16),hp(6,-15),hp(12,-9),hp(12,-4),hp(8,0),hp(7,-4),hp(3,-2),hp(-1,-4),hp(-5,1),hp(-5,7),hp(-9,10)],hd)
   poly(k,[hp(-13,1),hp(-13,-5),hp(-9,-11),hp(-3,-14),hp(5,-13),hp(9,-9),hp(6,-6),hp(1,-7),hp(-4,-4),hp(-8,3),hp(-9,7)],hm)
   poly(k,[hp(-11,-7),hp(-7,-11),hp(-1,-12),hp(5,-11),hp(5,-9),hp(-2,-9),hp(-6,-5)],hc);line(k,[hp(-9,-9),hp(-3,-12),hp(1,-12)],hl)
   if h==0:poly(k,[hp(-10,2),hp(-5,-1),hp(-6,7),hp(-10,9)],hm);rect(k,(cx+sign*5,cy-10,cx+sign*5+1,cy-8),'gold')
   else:
    poly(k,[hp(-12,1),hp(-16,6),hp(-16,15),hp(-12,17),hp(-8,12),hp(-9,4)],hd);poly(k,[hp(-13,5),hp(-14,11),hp(-12,14),hp(-10,10)],hc);line(k,[hp(-15,3),hp(-10,5)],'coral',2)
  else:
   poly(k,[(cx-16,cy+1),(cx-15,cy-8),(cx-10,cy-14),(cx-4,cy-16),(cx+6,cy-16),(cx+13,cy-11),(cx+16,cy-4),(cx+15,cy+6),(cx+11,cy+9),(cx+10,cy-1),(cx+6,cy-5),(cx+1,cy-3),(cx-4,cy-1),(cx-8,cy+3),(cx-11,cy+5),(cx-12,cy+9),(cx-15,cy+6)],hd)
   poly(k,[(cx-14,cy-5),(cx-10,cy-12),(cx-3,cy-14),(cx+5,cy-14),(cx+11,cy-10),(cx+12,cy-6),(cx+7,cy-8),(cx+3,cy-5),(cx-3,cy-5),(cx-8,cy),(cx-11,cy+1)],hm)
   poly(k,[(cx-11,cy-8),(cx-6,cy-12),(cx+2,cy-12),(cx+7,cy-10),(cx+5,cy-9),(cx-3,cy-9),(cx-7,cy-5),(cx-10,cy-3)],hc)
   line(k,[(cx-8,cy-10),(cx-3,cy-12),(cx+1,cy-12)],hl)
   poly(k,[(cx-7,cy-3),(cx-3,cy-6),(cx+2,cy-7),(cx-1,cy-3),(cx-5,cy)],hm)
   if dr=='up':
    poly(k,[(cx-14,cy-3),(cx+13,cy-3),(cx+13,cy+7),(cx+9,cy+13),(cx+4,cy+15),(cx-5,cy+15),(cx-11,cy+10),(cx-14,cy+4)],hd)
    poly(k,[(cx-12,cy-3),(cx+10,cy-3),(cx+10,cy+6),(cx+5,cy+11),(cx-4,cy+12),(cx-9,cy+7)],hm)
    line(k,[(cx-8,cy-4),(cx-8,cy+3),(cx-4,cy+8)],hc,2);line(k,[(cx+6,cy-3),(cx+7,cy+3),(cx+4,cy+8)],hc)
   if h==0:poly(k,[(cx+8,cy-10),(cx+12,cy-8),(cx+11,cy-5),(cx+8,cy-7)],'gold');rect(k,(cx+9,cy-8,cx+10,cy-7),'white')
   else:
    for sign2 in [-1,1]:
     xx=cx+sign2*14;yy=cy+2+(round(math.sin(phase-.9)) if moving else 0)
     poly(k,[(xx-3,yy),(xx+3,yy),(xx+5,yy+6),(xx+4,yy+13),(xx,yy+16),(xx-4,yy+12),(xx-5,yy+6)],hd);poly(k,[(xx-2,yy+3),(xx+2,yy+3),(xx+3,yy+10),(xx,yy+13),(xx-2,yy+9)],hc);line(k,[(xx-3,yy),(xx+3,yy)],'coral',2);rect(k,(xx-1,yy-1,xx+1,yy+1),'coralL')
 # Directional strap and bag: back pack flap / side body / front hip, slight lag on run.
 k='satchel';bob=(round(math.sin(phase-.8)) if moving else -1 if a=='idle' and i in [3,4] else 0)
 if dr=='up':
  line(k,[(cx-6,33+dy),(cx-5,42+dy)],'bagD',2);line(k,[(cx+6,33+dy),(cx+5,42+dy)],'bagD',2);bx=cx-5;by=36+dy+bob
 elif side:
  line(k,[(cx-sign*4,33+dy),(cx-sign*3,42+dy)],'bagD',2);bx=cx-sign*7-4;by=39+dy+bob
 else:line(k,[(cx-7,33+dy),(cx+9,44+dy)],'bagD',2);line(k,[(cx-6,33+dy),(cx+9,43+dy)],'bagL');bx=cx+8;by=40+dy+bob
 rect(k,(bx,by,bx+8,by+8),'bagD');rect(k,(bx+1,by+1,bx+7,by+6),'bag');rect(k,(bx+1,by+1,bx+7,by+2),'bagL');rect(k,(bx+3,by+3,bx+5,by+4),'gold');rect(k,(bx+1,by+7,bx+6,by+7),'skinD')
 return ims

def composite(key,h=0,o=0,mood='neutral',bag=True):
 ims=draw(key);im=Image.new('RGBA',(W,H))
 for k in ['body','outfit'+str(o),'face-'+mood,'hair'+str(h),'hands']+(['satchel'] if bag else []):im.alpha_composite(ims[k])
 return im
