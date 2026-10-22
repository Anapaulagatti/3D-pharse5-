"""Derivative review exports / requested technical diagrams; native inputs never rewritten."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'docs/gate2';O=D/'final-review';O.mkdir(exist_ok=True)
font=lambda n:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',n)
F=font(18);SM=font(14);BG='#172d34';WHITE='#f2ead7';BLUE='#6bc8ef';AMBER='#ffb963';GREEN='#8dcc9c'
def read(name):return Image.open(D/name).convert('RGB')
def light(im,name,maxsize=(1100,850)):
 im=im.copy();im.thumbnail(maxsize,Image.Resampling.LANCZOS);im.save(O/name,quality=85,optimize=True,subsampling=0)
def native_crop(path,box,name):
 im=Image.open(path);im.crop(box).save(O/name,optimize=True)
board=Image.new('RGB',(1024,844),BG);dr=ImageDraw.Draw(board)
items=[('Muneum / approved original',R/'docs/gate1/GATE1_STREET_NATIVE.png',(0,0,1024,768)),('Historical North / A',D/'A_NATIVE_1X.png',(400,0,1424,768)),('Modern B / reused Muneum',D/'B_NATIVE_1X.png',(0,0,1024,768)),('Jeju / C + local access fix',O/'JEJU_ACCESS_NATIVE_1X.png',(128,720,1008,1380))]
for i,(label,p,box) in enumerate(items):
 x=i%2*512;y=i//2*422;im=Image.open(p).convert('RGB').crop(box).resize((512,384),Image.Resampling.LANCZOS);dr.text((x+10,y+8),label,font=F,fill=WHITE);board.paste(im,(x,y+38))
light(board,'01_COMPARISON.jpg')
light(read('TRANSITION_NATIVE_1X.png'),'02_TRANSITION.jpg')
light(read('STATION_NATIVE_1X.png'),'03_STATION_JUNI.jpg')
light(Image.open(O/'JEJU_ACCESS_NATIVE_1X.png').convert('RGB'),'04_JEJU_TERRAIN_JUNI.jpg',(640,960))
light(Image.open(O/'JEJU_ACCESS_GAMEPLAY_1X.png').convert('RGB'),'05_JEJU_ACCESS_JUNI.jpg')
# Lossless pixel crops: no resampling or palette changes.
for id in ['A','B']:
 native_crop(D/f'{id}_ARCHITECTURE_1X.png',(288,248,736,584),f'{id}_PIXELS_1X.png')
native_crop(R/'docs/gate1/GATE1_STREET_NATIVE.png',(360,230,808,566),'MUNEUM_PIXELS_1X.png')
native_crop(D/'TRANSITION_NATIVE_1X.png',(600,340,1048,676),'TRANSITION_PIXELS_1X.png')
native_crop(D/'STATION_NATIVE_1X.png',(136,200,584,536),'STATION_PIXELS_1X.png')
native_crop(O/'JEJU_ACCESS_NATIVE_1X.png',(250,1010,698,1346),'JEJU_HOUSE_PIXELS_1X.png')
native_crop(O/'JEJU_ACCESS_NATIVE_1X.png',(350,250,798,586),'JEJU_TERRAIN_PIXELS_1X.png')
# Before/after screenshots, native pixel pitch preserved in both panels; review derivative only.
bf=read('C_NATIVE_1X.png').crop((350,1000,730,1350));af=Image.open(O/'JEJU_ACCESS_NATIVE_1X.png').convert('RGB').crop((350,1000,730,1350));pair=Image.new('RGB',(760,390),BG);q=ImageDraw.Draw(pair);q.text((10,10),'Before / delivered Gate2',font=F,fill=WHITE);q.text((390,10),'After / entrance paving only',font=F,fill=WHITE);pair.paste(bf,(0,40));pair.paste(af,(380,40));light(pair,'06_ACCESS_BEFORE_AFTER.jpg')
# Exact planning data, drawn as technical diagrams, never claimed as gameplay.
p=json.loads((R/'assets-src/world-gate1/plan.json').read_text());proposal=json.loads((R/'assets-src/gate2/plan/jeju-localized-proposal.json').read_text())
im=Image.new('RGB',(1320,820),BG);d=ImageDraw.Draw(im);d.text((18,12),'JEJU FIT / BEFORE AND PROPOSED AFTER — not applied to Gate1',font=font(22),fill=WHITE)
for side in [0,1]:
 ox=side*660+25;oy=85;scale=.29
 def pt(x,y):return (round(ox+(x-2350)*scale),round(oy+(y-3100)*scale))
 def rect(r,color,width=3):
  x,y,w,h=r;d.rectangle([pt(x,y),pt(x+w,y+h)],outline=color,width=width)
 def line(points,color,width=3):d.line([pt(*v)for v in points],fill=color,width=width)
 def dot(v,color):x,y=pt(*v);d.ellipse((x-5,y-5,x+5,y+5),fill=color)
 d.text((ox,55),'BEFORE / approved'if not side else'AFTER / proposal overlay',font=F,fill=WHITE)
 rect([2350,3100,810,880],GREEN);rect([3290,3260,720,1260],BLUE);rect([3040,3390,400,180],BLUE,2);rect([2496,3940,128,220],BLUE,2);rect([3210,4036,180,128],BLUE,2)
 line([[2560,4100],[3240,4100]],BLUE);dot([2560,4100],BLUE);dot([3240,4100],BLUE)
 line([[4096,3100],[4096,4608],[2350,4608]],BLUE,2)
 if side:
  rect(proposal['nativeStudyFrame'],AMBER,2);rect(proposal['approximateLand'],AMBER,4)
  line([[4352,3100],[4352,4864],[2350,4864]],AMBER,2)
  line([[3160,3480],[3180,3480],[3180,3560]],AMBER,5);dot([3180,3560],AMBER)
  line([[2560,4100],[3180,4020]],AMBER,3);dot([3180,4020],AMBER);rect([3150,3956,180,128],AMBER,2)
 d.text((ox,625),'Blue: approved720x1260 land + bridge/piers',font=SM,fill=BLUE)
 if side:
  d.text((ox,649),'Orange: approx910x1380 land;1024x1536 frame',font=SM,fill=AMBER)
  d.text((ox,673),'Canvas4352x4864; mainland remains fixed',font=SM,fill=WHITE)
 else:
  d.text((ox,649),'Approved canvas4096x4608',font=SM,fill=WHITE)
 d.text((ox,700),'Coordinate units: native world pixels; display0.29x',font=SM,fill=WHITE)
light(im,'07_JEJU_RESERVATION_OVERLAY.jpg',(1320,820))
# Arrival-detail overlay: independent axis scales identical between before/after.
im=Image.new('RGB',(1200,760),BG);d=ImageDraw.Draw(im);d.text((20,12),'ARRIVAL ALIGNMENT / BEFORE → PROPOSED AFTER',font=font(22),fill=WHITE)
for row,(title,region,oldpts,newpts) in enumerate([
 ('Upper bridge / existing bridge corridor + connector',(3060,3380,400,260),[[3160,3480],[3290,3480]],[[3160,3480],[3180,3480],[3180,3560]]),
 ('Ferry / mainland terminal fixed; island landing shifts(-60,-80)',(2460,3900,1000,350),[[2560,4100],[3240,4100]],[[2560,4100],[3180,4020]])]):
 y0=65+row*340;d.text((20,y0),title,font=F,fill=WHITE)
 for side in [0,1]:
  x0=20+side*600;y=y0+50;rx,ry,rw,rh=region;sc=min(540/rw,220/rh)
  def xy(v):return (x0+(v[0]-rx)*sc,y+(v[1]-ry)*sc)
  def ln(pts,col):d.line([xy(v)for v in pts],fill=col,width=4)
  d.text((x0,y0+26),'BEFORE'if not side else'PROPOSED / blue retained for comparison',font=SM,fill=WHITE);ln(oldpts,BLUE)
  if side:ln(newpts,AMBER)
  for j,v in enumerate(newpts if side else oldpts):
   xx,yy=xy(v);d.ellipse((xx-4,yy-4,xx+4,yy+4),fill=AMBER if side else BLUE);d.text((xx-20,yy+10),str(tuple(v)),font=SM,fill=WHITE) if not(row==0 and side==1) else d.text((xx-12 if j==0 else xx+8,yy-22 if j<2 else yy+8),chr(65+j),font=SM,fill=WHITE)
  if row==0 and side==1:
   d.text((x0,y0+245),'A mainland(3160,3480); B elbow(3180,3480)',font=SM,fill=WHITE)
   d.text((x0,y0+265),'C proposed art endpoint(3180,3560)',font=SM,fill=WHITE)
 d.text((20,y0+300),'Engineering, bridge clearance and final shoreline alignment remain UNPROVEN.',font=SM,fill=WHITE)
light(im,'08_ARRIVAL_ALIGNMENT.jpg',(1200,760))
im=Image.new('RGB',(1600,700),BG);d=ImageDraw.Draw(im);d.text((20,15),'STATION COLLISION /10px DEPTH DISCREPANCY — proposal only',font=font(22),fill=WHITE)
for side in [0,1]:
 ox=30+side*800;oy=110;d.text((ox,65),'BEFORE / approved560x210'if not side else'AFTER / study555x220 overlay',font=F,fill=WHITE)
 def r(box,c,width=3):x,y,w,h=box;d.rectangle((ox+x-2290,oy+y-2350,ox+x+w-2290,oy+y+h-2350),outline=c,width=width)
 r([2320,2380,560,210],BLUE)
 r([2290,2610,700,160],GREEN,2)
 if side:
  r([2320,2380,555,220],AMBER);d.rectangle((ox+30,oy+240,ox+585,oy+250),fill=AMBER)
 d.text((ox,550),'y2590 approved south edge',font=SM,fill=BLUE)
 if side:d.text((ox,575),'y2600 study south edge (+10)',font=SM,fill=AMBER)
 d.text((ox,oy+305),'Forecourt starts y2610 / unchanged',font=SM,fill=GREEN)
 d.text((ox,595),'1 diagram pixel =1 world pixel',font=SM,fill=WHITE)
d.text((20,610),'Shared north/west edge assumed ONLY for comparison; native study is not registered into the world.',font=SM,fill=WHITE)
d.text((20,638),'No masterplan, forecourt, platforms or tracks were changed. Final threshold/collision fit needs review.',font=SM,fill=WHITE)
light(im,'09_STATION_DEPTH_OVERLAY.jpg',(1600,700))
# File sizes and practical decoded memory estimate, not a hardware performance measurement.
rows=[dict(path=str(f.relative_to(R)),bytes=f.stat().st_size,under1MB=f.stat().st_size<1000000,sha256=hashlib.sha256(f.read_bytes()).hexdigest()) for f in sorted(O.iterdir())if f.suffix in ['.jpg','.png']]
inv=[]
for f in sorted((R/'public/assets/gate2').rglob('*.png'))+[R/'public/assets/juni/juni.png']:
 with Image.open(f)as im:inv.append(dict(path=str(f.relative_to(R)),size=im.size,rgba8Bytes=im.width*im.height*4))
(O/'review-files.json').write_text(json.dumps(dict(files=rows,textureInventory=inv,rgba8TotalBytes=sum(v['rgba8Bytes']for v in inv)),indent=2)+'\n');print(json.dumps(rows))
