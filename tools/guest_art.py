"""Original stylized historical guests sharing the accepted native chibi anatomy, not portraits."""
from PIL import Image,ImageDraw
from avatar_art import draw,pose,W,H,P
import math
N={'idle':6,'walk':12,'wave':8,'think':8,'pose':6,'start':3,'stop':3,'turn':3}
def guest(actor,key,mood=None):
 st=pose(key);a,dr,i,cx,cy,dy,side,sign,phase=(st[k] for k in ['a','dr','i','cx','cy','dy','side','sign','phase']);parts=draw(key)
 mood=mood or ('happy' if a=='wave' else 'focused' if a in ['think','pose'] else 'neutral')
 im=parts['body'].copy();d=ImageDraw.Draw(im)
 def poly(p,c):d.polygon([(x+4,y+8) for x,y in p],fill=P.get(c,c))
 def rect(b,c):
  x,y,xx,yy=b
  if xx>=x and yy>=y:d.rectangle((x+4,y+8,xx+4,yy+8),fill=P.get(c,c))
 def line(p,c,w=1):d.line([(x+4,y+8) for x,y in p],fill=P.get(c,c),width=w)
 # King Sejong: muted vermilion robe, original sun-rosette badge, winged ikseongwan-inspired cap.
 if actor=='sejong':
  poly([(12,32+dy),(27,32+dy),(31,47+dy),(28,51+dy),(10,51+dy),(8,46+dy)],'ink')
  poly([(13,33+dy),(26,33+dy),(29,47+dy),(27,49+dy),(11,49+dy),(10,45+dy)],'coralD')
  poly([(13,34+dy),(19,35+dy),(20,47+dy),(12,47+dy),(11,43+dy)],'coral');line([(13,35+dy),(13,43+dy)],'coralL')
  line([(12,46+dy),(27,46+dy)],'goldD',2);line([(18,34+dy),(21,37+dy),(24,33+dy)],'cream',2)
  for j in [-1,1]:
   x=(cx+sign*round(math.sin(phase)*5)*j) if side and a=='walk' else 9 if j<0 else 31;y=41+dy+(round(math.sin(phase)*3)*j if a=='walk' else 0)
   if a=='wave' and j==1:x,y=37,[40,36,24,12,10,14,22,38][i]+dy
   if a=='think' and j==1:x,y=25,[38,35,32,30,29,30,33,38][i]+dy
   line([(14 if j<0 else 25,34+dy),(7 if j<0 else 33,36+dy),(x,y-2)],'ink',7);line([(14 if j<0 else 25,34+dy),(7 if j<0 else 33,36+dy),(x,y-2)],'coralD',5);line([(14 if j<0 else 25,34+dy),(x,y-3)],'coral',2)
  if not side:
   rect((17,38+dy,23,43+dy),'goldD');rect((18,38+dy,22,42+dy),'gold');rect((20,37+dy,20,43+dy),'cream');line([(17,40+dy),(23,40+dy)],'cream')
  # Cap has separate front/back and profile crowns and wings, never a modern portrait trace.
  if side:
   def hp(x,y):return (cx+sign*x,cy+y)
   poly([hp(-13,0),hp(-13,-10),hp(-8,-16),hp(7,-16),hp(11,-11),hp(11,-1)],'ink');poly([hp(-10,-2),hp(-10,-10),hp(-6,-14),hp(6,-14),hp(8,-10),hp(8,-3)],'hairM');line([hp(-8,-11),hp(-5,-13),hp(5,-13)],'hair')
   poly([hp(-11,-7),hp(-18,-9),hp(-18,-4),hp(-11,-2)],'ink');line([hp(-17,-7),hp(-12,-5)],'hairM')
  else:
   poly([(cx-15,cy-2),(cx-14,cy-10),(cx-8,cy-16),(cx+7,cy-16),(cx+13,cy-11),(cx+15,cy-2)],'ink');poly([(cx-12,cy-4),(cx-11,cy-10),(cx-7,cy-14),(cx+6,cy-14),(cx+10,cy-10),(cx+12,cy-4)],'hairM');line([(cx-9,cy-10),(cx-6,cy-12),(cx+5,cy-12)],'hair')
   for j in [-1,1]:poly([(cx+j*12,cy-9),(cx+j*18,cy-11),(cx+j*18,cy-5),(cx+j*12,cy-3)],'ink');line([(cx+j*14,cy-7),(cx+j*17,cy-8)],'hairM')
   if dr=='up':poly([(cx-13,cy-3),(cx+13,cy-3),(cx+11,cy+7),(cx+6,cy+12),(cx-6,cy+12),(cx-12,cy+7)],'hairD');line([(cx-8,cy+3),(cx-4,cy+8),(cx+4,cy+8)],'hairM')
  im.alpha_composite(parts['face-'+mood]);d=ImageDraw.Draw(im)
  if dr!='up':
   bx=cx if not side else cx+sign*9
   line([(bx-3,cy+10),(bx-1,cy+11)],'hairM');line([(bx+1,cy+11),(bx+3,cy+10)],'hairM');poly([(bx-3,cy+13),(bx+3,cy+13),(bx+2,cy+16),(bx,cy+18),(bx-2,cy+16)],'creamD');line([(bx,cy+14),(bx,cy+16)],'cream')
  # Book follows the thinking hand. Grounded robe leaves alternating boots readable.
  by=33+dy if a=='think' and i in [2,3,4,5] else 39+dy;bx=24 if dr!='up' else 12
  rect((bx,by,bx+10,by+10),'goldD');rect((bx+1,by+1,bx+9,by+8),'cream');line([(bx+5,by+2),(bx+5,by+8)],'creamD');line([(bx+2,by+3),(bx+3,by+3)],'coralD');line([(bx+7,by+4),(bx+8,by+4)],'jadeD')
  if a=='wave':
   y=[40,36,24,12,10,14,22,38][i]+dy;rect((35,y-2,39,y+2),'skinD');rect((36,y-2,38,y+1),'skinL')
 elif actor in ['jang','saimdang','yi']:
  if actor in ['jang','yi']:
   im.alpha_composite(parts['outfit1']);d=ImageDraw.Draw(im)
  else:
   poly([(11,36+dy),(28,36+dy),(32,49+dy),(29,52+dy),(10,52+dy),(7,49+dy)],'ink');poly([(12,37+dy),(27,37+dy),(30,49+dy),(27,50+dy),(11,50+dy),(9,48+dy)],'jadeD');poly([(13,38+dy),(19,38+dy),(18,50+dy),(11,49+dy)],'jade');line([(14,40+dy),(12,48+dy)],'jadeL')
   poly([(12,32+dy),(27,32+dy),(29,38+dy),(24,40+dy),(13,39+dy),(10,36+dy)],'creamD');poly([(13,33+dy),(25,33+dy),(26,37+dy),(21,38+dy),(13,37+dy)],'cream');line([(15,33+dy),(20,36+dy),(23,33+dy)],'white',2);line([(21,36+dy),(25,41+dy)],'coralD',2)
   for j in [-1,1]:
    x=9 if j<0 else 31;y=41+dy+(round(math.sin(phase)*3)*j if a=='walk' else 0)
    if a=='wave' and j==1:x,y=37,[40,36,24,12,10,14,22,38][i]+dy
    line([(14 if j<0 else 25,34+dy),(x,y-2)],'creamD',5);line([(14 if j<0 else 25,34+dy),(x,y-2)],'cream',3);rect((x-2,y-2,x+2,y+2),'skinM');rect((x-1,y-2,x+1,y+1),'skinL')
  if actor=='jang':
   # Work coat and reinforced cuffs, a practical tied cap, no modern goggles.
   line([(13,42+dy),(26,42+dy)],'bagD',2);rect((19,41+dy,22,43+dy),'gold');rect((11,38+dy,13,40+dy),'jadeL')
   poly([(cx-13,cy-3),(cx-12,cy-11),(cx-6,cy-16),(cx+6,cy-16),(cx+12,cy-10),(cx+13,cy-3)],'hairD');poly([(cx-10,cy-6),(cx-9,cy-11),(cx-5,cy-14),(cx+5,cy-14),(cx+9,cy-10),(cx+10,cy-6)],'navyD');line([(cx-11,cy-4),(cx+11,cy-4)],'creamD',2);line([(cx-9,cy-11),(cx-5,cy-13),(cx,cy-13)],'navyL')
   if dr=='up':poly([(cx-12,cy-2),(cx+12,cy-2),(cx+10,cy+8),(cx+4,cy+12),(cx-6,cy+12),(cx-11,cy+7)],'hairD');line([(cx-8,cy+4),(cx+6,cy+6)],'hairM')
   im.alpha_composite(parts['face-'+mood]);d=ImageDraw.Draw(im);im.alpha_composite(parts['hands']);d=ImageDraw.Draw(im)
   # Small original brass astronomical model: ring and stand, not a copied instrument asset.
   bx=29 if dr!='up' else 12;by=37+dy-(5 if a=='pose' and i in [2,3] else 0)
   d.ellipse((bx-2+4,by-5+8,bx+6+4,by+3+8),outline=P['goldD'],width=2);line([(bx+2,by-4),(bx+2,by+5)],'gold');line([(bx-1,by-1),(bx+5,by-1)],'gold');line([(bx-2,by+6),(bx+6,by+6)],'bagD',2)
  elif actor=='saimdang':
   # Center-parted hair with a low bun and a slim pin; no modern portrait source.
   poly([(cx-14,cy+5),(cx-15,cy-5),(cx-11,cy-13),(cx-4,cy-16),(cx+5,cy-16),(cx+12,cy-11),(cx+15,cy-4),(cx+13,cy+7),(cx+10,cy+8),(cx+9,cy-3),(cx+3,cy-7),(cx,cy-9),(cx-4,cy-5),(cx-9,cy-3),(cx-11,cy+8)],'hairD');line([(cx-10,cy-8),(cx-6,cy-12),(cx-1,cy-13)],'hair');line([(cx+2,cy-13),(cx+8,cy-9),(cx+11,cy-4)],'hairM',2)
   if dr=='up':
    poly([(cx-13,cy-3),(cx+13,cy-3),(cx+11,cy+8),(cx+5,cy+13),(cx-5,cy+13),(cx-11,cy+8)],'hairD');rect((cx-5,cy+10,cx+6,cy+16),'hairM');line([(cx-9,cy+12),(cx+10,cy+12)],'gold');line([(cx-8,cy-2),(cx-6,cy+6)],'hairM')
   elif side:
    xx=cx-sign*12;rect((xx-4,cy+8,xx+3,cy+14),'hairD');rect((xx-2,cy+9,xx+2,cy+12),'hairM');line([(xx-5,cy+10),(xx+5,cy+10)],'gold')
   im.alpha_composite(parts['face-'+mood]);d=ImageDraw.Draw(im)
   bx=25 if dr!='up' else 10;by=42+dy;rect((bx,by,bx+9,by+8),'bagD');rect((bx+1,by+1,bx+8,by+7),'cream');line([(bx+4,by+6),(bx+4,by+2)],'jadeD');line([(bx+2,by+3),(bx+4,by+4),(bx+7,by+2)],'jade')
   if a!='wave':line([(31,35+dy),(35,45+dy)],'bagD',2);line([(31,34+dy),(32,36+dy)],'hairD',2)
  else:
   # Stylized lamellar cuirass and broad military hat; maps replace weapons in this social scene.
   poly([(12,33+dy),(27,33+dy),(28,44+dy),(24,47+dy),(14,47+dy),(11,43+dy)],'navyD');line([(12,34+dy),(9,37+dy)],'coralD',3);line([(26,34+dy),(30,37+dy)],'coralD',3)
   for yy in [35,39,43]:
    for xx in [14,18,22]:rect((xx,yy+dy,xx+2,yy+dy+2),'goldD');rect((xx,yy+dy,xx+1,yy+dy),'creamD')
   line([(13,45+dy),(26,45+dy)],'bagD',2)
   poly([(cx-13,cy-3),(cx-12,cy-11),(cx-7,cy-16),(cx+6,cy-16),(cx+12,cy-10),(cx+13,cy-3)],'ink');poly([(cx-10,cy-4),(cx-10,cy-10),(cx-5,cy-14),(cx+5,cy-14),(cx+9,cy-9),(cx+10,cy-4)],'navyD');line([(cx-7,cy-10),(cx-4,cy-12),(cx,cy-12)],'navyL');rect((cx-17,cy-3,cx+17,cy),'ink');line([(cx-15,cy-2),(cx+13,cy-2)],'hairM');rect((cx-1,cy-17,cx+1,cy-14),'gold');line([(cx+1,cy-17),(cx+7,cy-20),(cx+8,cy-17)],'coralD',2)
   if dr=='up':poly([(cx-12,cy),(cx+12,cy),(cx+10,cy+9),(cx+5,cy+13),(cx-5,cy+13),(cx-11,cy+7)],'hairD');line([(cx,cy+10),(cx+2,cy+17)],'coralD',2)
   im.alpha_composite(parts['face-'+mood]);d=ImageDraw.Draw(im);im.alpha_composite(parts['hands']);d=ImageDraw.Draw(im)
   if dr!='up':
    xx=cx if not side else cx+sign*9;line([(xx-2,cy+13),(xx,cy+15),(xx+2,cy+13)],'hairM')
   bx=25 if dr!='up' else 11;by=39+dy;rect((bx,by,bx+10,by+8),'goldD');rect((bx+1,by+1,bx+9,by+7),'cream');line([(bx+2,by+6),(bx+5,by+3),(bx+8,by+5)],'jadeD');rect((bx+7,by+2,bx+8,by+3),'coralD')
 else:raise ValueError(actor)
 return im
