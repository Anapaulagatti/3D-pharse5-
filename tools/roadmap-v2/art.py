"""Original authored native crop/prop/icon component art; no image model, donor tracing or paid calls."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,random
R=Path.cwd();O=R/'public/assets/roadmap-v2';S=R/'assets-src/roadmap-v2';O.mkdir(parents=True,exist_ok=True);S.mkdir(parents=True,exist_ok=True)
G=['#214a37','#376b43','#56844b','#84aa59','#b3c578']; B=['#573b2a','#76533a','#a57849','#d4a164']; palette=set(G+B)
def crop(kind,stage):
 im=Image.new('RGBA',(40,44));d=ImageDraw.Draw(im);rng=random.Random(kind+stage);n=['sown','sprout','young','growing','ready'].index(stage)
 d.ellipse((12,38,29,41),fill='#453d2d');palette.add('#453d2d')
 if n==0:
  for x in [17,23]:d.line((x,38,x+1,37),fill='#e0bd74')
  return im
 h=([0,5,9,14,18]if kind=='strawberry'else[0,7,13,20,27])[n];y=39-h
 if kind in ['carrot','sweet-potato','soybean','chili','tomato','cucumber','strawberry']:
  d.line((20,39,20,y),fill=G[1],width=2)
  for j in range(2,n+3):
   yy=39-j*max(2,h//(n+3));side=-1 if j%2 else 1;xx=20+side*(4+j%3)
   d.polygon([(20,yy+3),(xx,yy-3),(xx+side*3,yy-2),(xx+side*2,yy+1)],fill=G[j%3+1]);d.line((20,yy+2,xx,yy-1),fill=G[0])
 if kind=='carrot' and n>=3:
  d.polygon([(17,35),(24,35),(21,41)],fill='#d77e37');d.line((18,36,22,36),fill='#efad52')
 elif kind=='sweet-potato' and n>=3:
  for x in [13,23]:d.ellipse((x,35,x+6,40),fill='#9d5365');d.line((x+2,36,x+5,36),fill='#cf8191')
 elif kind=='soybean' and n>=3:
  for x,yy in [(15,28),(23,24),(21,31)]:d.ellipse((x,yy,x+3,yy+6),fill='#bdba62');d.point((x+1,yy+2),fill='#ebe1a1')
 elif kind in ['chili','tomato','cucumber','strawberry'] and n>=3:
  c={'chili':'#bc4e37','tomato':'#cb5542','cucumber':'#527d38','strawberry':'#d14d50'}[kind]
  for x,yy in ([(12,31),(24,32)]if kind=='strawberry'else[(13,31),(24,27)]):
   if kind=='chili':d.polygon([(x,yy),(x+3,yy),(x+2,yy+7),(x-1,yy+8)],fill=c)
   elif kind=='cucumber':d.rounded_rectangle((x,yy,x+4,yy+10),radius=2,fill=c);d.line((x+1,yy+2,x+1,yy+7),fill='#91aa53')
   elif kind=='strawberry':
    d.polygon([(x,yy),(x+6,yy),(x+6,yy+3),(x+3,yy+7),(x,yy+3)],fill=c);d.line((x+1,yy,x+5,yy),fill=G[3]);d.point((x+2,yy+2),fill='#f6d991');d.point((x+4,yy+3),fill='#f6d991');d.point((x+3,yy+5),fill='#f6d991')
   else:d.ellipse((x,yy,x+6,yy+6),fill=c);d.point((x+2,yy+1),fill='#f1b074');d.line((x+1,yy,x+4,yy),fill=G[2])
 elif kind in ['cabbage','pumpkin']:
  r=3+n*2;d.ellipse((20-r,39-r*2,20+r,39),fill=G[1]if kind=='cabbage'else '#a66b35');
  for j in range(4):
   col=G[2+j%3]if kind=='cabbage'else ['#d79945','#bc7d35','#e5b35c','#c18840'][j]
   d.arc((20-r+j*2,39-r*2+j,20+r-j,39-j),35+j*60,170+j*60,fill=col,width=2)
  d.line((20,39-2*r,21,36-2*r),fill=G[0],width=2)
 elif kind=='rice':
  for x in [13,17,21,25]:
   d.line((20,39,x,y+2),fill=G[2]);d.line((x,y+2,x-3,y+7),fill='#d3be70'if n>=3 else G[3],width=2)
   if n>=3:
    for yy in range(y+3,y+10,2):d.point((x-2,yy),fill='#ead79a')
 elif kind=='flower':
  for x,yy in [(15,y+4),(24,y+1),(20,y+9)]:
   d.line((20,39,x,yy),fill=G[2]);d.ellipse((x-4,yy-3,x+4,yy+3),fill='#c97f94');d.ellipse((x-2,yy-4,x+2,yy+4),fill='#dfa1b0');d.rectangle((x-1,yy-1,x+1,yy+1),fill='#ebd08a')
 if n<3 and kind in ['cabbage','pumpkin','rice','flower']:
  d.line((20,39,20,y+2),fill=G[1]);d.ellipse((14,y,20,y+4),fill=G[2]);d.ellipse((20,y-2,26,y+2),fill=G[3])
 return im
base=R/'public/assets/farming/phase3bd-final-quality';old=json.loads((base/'crops.json').read_text());src=Image.open(base/'crops.png').convert('RGBA');frames={}
for k,v in old['frames'].items():
 f=v['frame'];frames[k]=src.crop((f['x'],f['y'],f['x']+f['w'],f['y']+f['h']))
for k in ['carrot','cabbage','rice','chili','sweet-potato','soybean','pumpkin','cucumber','tomato','strawberry']:
 for st in ['sown','sprout','young','growing','ready']:frames[k+'-'+st]=crop(k,st)
def pack(frames,name,w,h,cols=12):
 atlas=Image.new('RGBA',(cols*w,((len(frames)+cols-1)//cols)*h));data={}
 for i,(key,im) in enumerate(frames.items()):
  x=i%cols*w;y=i//cols*h;atlas.paste(im,(x,y));data[key]={'frame':{'x':x,'y':y,'w':w,'h':h},'rotated':False,'trimmed':False,'spriteSourceSize':{'x':0,'y':0,'w':w,'h':h},'sourceSize':{'w':w,'h':h}}
 atlas.save(O/(name+'.png'));(O/(name+'.json')).write_text(json.dumps({'frames':data,'meta':{'image':name+'.png','scale':'1'}},indent=2)+'\n');atlas.resize((atlas.width*3,atlas.height*3),Image.Resampling.NEAREST).save(S/(name+'-review-3x.png'))
 for k,im in frames.items():
  p=S/name;p.mkdir(exist_ok=True);im.save(p/(k+'.png'))
pack(frames,'crops',40,44)
props={}
for k in ['floor-wood','floor-stone','wall','counter','bookshelf','table','seed-rack','lamp','stool','sign','parcel','fragment','restored-sign','coin','bag','journal','hoe']:
 size=(64,80);im=Image.new('RGBA',size);d=ImageDraw.Draw(im);rng=random.Random(k)
 if k.startswith('floor'):
  c='#a18158'if k.endswith('wood')else '#b8b9a6';d.rectangle((0,0,15,15),fill=c)
  for i in range(20):
   x=rng.randrange(16);y=rng.randrange(16);d.point((x,y),fill='#c4ab7b'if k.endswith('wood')else '#cfcebb')
  d.line((0,15,15,15),fill='#77674c');d.line((15,0,15,15),fill='#998b6a')
 elif k=='wall':
  d.rectangle((0,0,63,79),fill='#d3c2a1');d.rectangle((2,4,61,60),fill='#e4d5b6');d.rectangle((0,64,63,79),fill='#72573e');d.line((0,65,63,65),fill='#a38253',width=2)
 elif k in ['counter','table','bookshelf','seed-rack']:
  y=34 if k!='bookshelf'else 5;d.rectangle((3,y+8,62,76),fill='#493c32');d.rectangle((2,y,59,70),fill='#886442');d.rectangle((3,y+1,58,y+12),fill='#bd9965');d.line((4,y+2,56,y+2),fill='#d7b87c');d.rectangle((7,y+17,54,66),fill='#5c4735')
  if k in ['bookshelf','seed-rack']:
   for yy in [y+16,y+37]:
    for x in range(9,53,7):d.rectangle((x,yy,x+4,yy+14),fill=rng.choice(['#5d8274','#b77b54','#d3bd83','#877f9b']));d.line((x+1,yy+2,x+3,yy+2),fill='#e5d5ac')
    d.rectangle((6,yy+15,55,yy+18),fill='#b68b54')
  else:
   d.line((10,y+24,51,y+24),fill='#aa8455');d.line((29,y+18,29,64),fill='#3f342c')
 elif k=='lamp':
  d.rectangle((29,34,32,68),fill='#6b5c42');d.ellipse((20,64,41,70),fill='#584b38');d.polygon([(23,20),(39,20),(46,41),(16,41)],fill='#eed39a');d.line((23,23,19,38),fill='#fff0bd',width=2)
 elif k=='stool':
  d.rectangle((14,44,18,70),fill='#604d37');d.rectangle((43,44,47,70),fill='#604d37');d.ellipse((10,30,51,48),fill='#b49565');d.arc((10,30,51,48),180,350,fill='#dec391',width=2)
 else:
  # Authored small distinct icons/world props, centered in fixed64x80cell.
  x,y=20,30
  if k in ['sign','restored-sign','journal']:
   d.rectangle((x,y,x+25,y+23),fill='#604632');d.rectangle((x+2,y+2,x+23,y+21),fill='#d7bd87'if k!='restored-sign'else '#f2d78d');
   for yy in [y+7,y+12,y+17]:d.line((x+6,yy,x+19,yy),fill='#49614b',width=2)
  elif k=='coin':d.ellipse((x,y,x+23,y+23),fill='#a87635');d.ellipse((x+2,y+1,x+21,y+20),fill='#e7bd59');d.ellipse((x+6,y+5,x+17,y+16),outline='#fff0a0',width=2)
  elif k=='bag':d.rectangle((x,y+7,x+23,y+28),fill='#8c6b44');d.rectangle((x+3,y+9,x+20,y+24),fill='#bd975e');d.arc((x+5,y,x+18,y+16),180,360,fill='#e2c88c',width=3)
  elif k=='hoe':d.line((x+3,y+29,x+20,y+2),fill='#b98d57',width=3);d.polygon([(x+15,y+1),(x+28,y+5),(x+27,y+12),(x+19,y+8)],fill='#9ca6a0')
  elif k=='parcel':d.rectangle((x,y,x+25,y+22),fill='#ba9a65');d.rectangle((x+11,y,x+14,y+22),fill='#ead6a8');d.rectangle((x,y+8,x+25,y+11),fill='#ead6a8')
  elif k=='fragment':d.polygon([(x,y+5),(x+12,y),(x+24,y+4),(x+20,y+22),(x+3,y+20)],fill='#ddc995');d.line((x+6,y+9,x+16,y+9),fill='#59654a',width=2)
 props[k]=im
pack(props,'props',64,80,8)
# Original compact native icons, no browser vector scaling.
for key in ['coin','bag','journal','hoe']:
 props[key].crop((16,24,48,64)).save(O/(key+'.png'))
h={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in O.iterdir()if p.is_file()}
(S/'PROVENANCE.json').write_text(json.dumps({'art_source':'code + byte-exact retained radish/scallion crop frames','author':'Codex, original native cluster/component drawings','providerCalls':0,'thirdPartyReferences':[],'source':'tools/roadmap-v2/art.py','permission':'Owner MASTER PROMPT V2 deterministic authored fallback; local human art review pending','protectedOriginalsModified':False,'runtimeHashes':h},indent=2)+'\n')
print(json.dumps({'cropFrames':len(frames),'props':len(props),'runtime':h},indent=2))
