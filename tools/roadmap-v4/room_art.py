"""Original native component art; owner-authorized code fallback. NO image model, filters or external references."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
R=Path.cwd();S=R/'assets-src/roadmap-v4/rooms';O=R/'public/assets/roadmap-v4/rooms';S.mkdir(parents=True,exist_ok=True);O.mkdir(parents=True,exist_ok=True)
P={'edge':'#3c3834','wood':'#987049','shade':'#69513c','lit':'#c7a36b','high':'#e5ca91','paper':'#e9d6ab','green':'#56796c','blue':'#64808b','red':'#a66f50','metal':'#91a29c','darkmetal':'#4e6663'}
frames={}
def new(size):
 im=Image.new('RGBA',size);return im,ImageDraw.Draw(im)
def wood(d,b,light=True):
 x,y,w,h=b;d.rectangle((x,y,x+w-1,y+h-1),fill=P['shade']);d.rectangle((x,y,x+w-4,y+h-5),fill=P['wood']);d.line((x+1,y+1,x+w-5,y+1),fill=P['high']);d.line((x+2,y+2,x+2,y+h-6),fill=P['lit']);
 for yy in range(y+8,y+h-6,10):d.line((x+6,yy,x+w-9,yy),fill=P['shade']);d.line((x+w//3,yy+2,x+w-16,yy+2),fill=P['lit'])
def shadow(d,w,h):d.polygon([(7,h-9),(w-9,h-9),(w-1,h-5),(w-8,h-1),(12,h-1),(1,h-5)],fill='#3b3e33')
def book(d,x,y,h,c):
 d.rectangle((x,y,x+7,y+h),fill=c);d.line((x,y+1,x+6,y+1),fill=P['paper']);d.line((x+1,y+4,x+1,y+h-1),fill=P['lit']);d.line((x+2,y+h-4,x+6,y+h-4),fill=P['paper'])
for key,size in [('bookshelf', (128,144)),('seed-rack',(112,128)),('counter',(192,88)),('counter-side',(80,144)),('reading-table',(128,88)),('book-desk',(128,88)),('workbench',(224,88)),('packing-table',(128,88)),('tool-rack',(160,128)),('seed-crates',(112,80)),('book-stack',(64,64)),('lamp',(48,88)),('stool',(48,56)),('market-window',(112,112)),('library-window',(96,136)),('workshop-vent',(128,88)),('rune-board',(112,112)),('notice-board',(128,112)),('notice-restored',(128,112)),('tool-stand',(96,88)),('parcel',(48,48)),('fragment',(40,40))]:
 im,d=new(size);w,h=size
 if key in ['bookshelf','seed-rack']:
  shadow(d,w,h);wood(d,(4,2,w-12,h-8));d.rectangle((12,9,w-17,h-15),fill=P['edge']);
  for row,yy in enumerate(range(16,h-23,35)):
   for i,x in enumerate(range(16,w-22,11)):
    if key=='bookshelf':book(d,x,yy+(i%3),23-(i%3),[P['green'],P['blue'],P['red'],P['paper']][(i+row)%4])
    else:
     d.polygon([(x,yy+4),(x+7,yy+3),(x+9,yy+23),(x-2,yy+23)],fill=P['paper']);d.line((x,yy+8,x+6,yy+8),fill=P['shade']);d.ellipse((x+1,yy+12,x+5,yy+17),fill=[P['green'],P['red']][(row+i)%2])
   wood(d,(10,yy+25,w-24,5))
 elif key in ['counter','counter-side','reading-table','book-desk','workbench','packing-table','tool-stand']:
  shadow(d,w,h);y=19 if key!='counter-side'else 6;wood(d,(8,y,w-18,h-y-8));d.rectangle((14,y+18,w-15,h-13),fill=P['shade']);d.line((w//2,y+21,w//2,h-15),fill=P['edge']);d.rectangle((19,y+23,w-22,y+29),outline=P['lit']);d.rectangle((w//2-6,y+24,w//2+4,y+27),fill=P['metal']);
  if key in ['reading-table','book-desk']:
   d.polygon([(20,y+2),(w//2,y+4),(w//2-2,y+16),(18,y+13)],fill=P['paper']);d.polygon([(w//2+1,y+4),(w-22,y+2),(w-19,y+13),(w//2+2,y+16)],fill='#c6b68f');d.line((w//2,y+5,w//2,y+14),fill=P['shade']);d.line((25,y+6,w//2-7,y+8),fill=P['shade']);d.line((25,y+10,w//2-8,y+12),fill=P['shade'])
  if key in ['packing-table','counter']:
   d.rectangle((w//2-18,y-8,w//2+17,y+11),fill='#bb9460');d.line((w//2,y-8,w//2,y+11),fill=P['paper'],width=3);d.line((w//2-17,y+1,w//2+16,y+1),fill=P['paper'],width=2);d.rectangle((w-44,y+1,w-20,y+12),fill=P['paper']);d.line((w-40,y+5,w-25,y+5),fill=P['red'],width=2)
  if key in ['workbench','tool-stand']:
   d.line((22,y+10,w-34,y+5),fill=P['metal'],width=3);d.rectangle((w-53,y-7,w-33,y+12),fill=P['darkmetal']);d.rectangle((w-53,y-9,w-32,y-6),fill=P['metal']);d.line((w-42,y+5,w-26,y+9),fill=P['metal'],width=2);d.ellipse((w-28,y+6,w-23,y+11),fill=P['high'])
 elif key=='tool-rack':
  wood(d,(2,6,w-4,h-12));d.rectangle((10,15,w-12,h-20),fill='#4e5650')
  for x in [25,60,97,132]:
   d.line((x,30,x-8,104),fill=P['lit'],width=4);d.line((x+1,30,x-6,100),fill=P['high']);d.rectangle((x-11,25,x+14,34),fill=P['metal']);d.line((x-11,25,x+14,25),fill=P['paper'])
  d.line((12,50,w-14,50),fill=P['shade'],width=3)
 elif key=='seed-crates':
  shadow(d,w,h)
  for x in [4,57]:
   wood(d,(x,28,49,43));d.rectangle((x+5,18,x+42,35),fill=P['paper']);d.line((x+12,18,x+36,18),fill=P['shade'],width=3);d.ellipse((x+19,24,x+29,33),fill=P['green'])
 elif key=='book-stack':
  shadow(d,w,h)
  for i,yy in enumerate([41,31,21]):
   d.rectangle((9+i*2,yy,53,yy+9),fill=[P['green'],P['red'],P['blue']][i]);d.rectangle((12+i*2,yy+2,52,yy+6),fill=P['paper']);d.line((15+i*2,yy+4,48,yy+4),fill='#b2a384')
 elif key=='lamp':
  shadow(d,w,h);d.ellipse((9,74,38,83),fill=P['shade']);d.rectangle((22,35,25,77),fill=P['metal']);d.polygon([(15,9),(32,9),(42,39),(5,39)],fill='#d5b675');d.polygon([(16,12),(23,12),(19,36),(9,36)],fill='#f2dea5');d.line((7,40,41,40),fill=P['shade'],width=2)
 elif key=='stool':
  shadow(d,w,h);d.rectangle((10,21,14,49),fill=P['shade']);d.rectangle((34,21,38,49),fill=P['shade']);d.ellipse((5,9,42,29),fill=P['wood']);d.arc((6,9,41,26),180,360,fill=P['high'],width=2);d.line((10,17,36,17),fill=P['lit'])
 elif key.endswith('window'):
  wood(d,(4,3,w-8,h-8));d.rectangle((12,10,w-14,h-21),fill='#567e87');d.polygon([(13,11),(w-16,11),(13,h-25)],fill='#95b7b2');d.rectangle((w//2-2,10,w//2+2,h-21),fill=P['shade']);d.rectangle((12,h//2-2,w-14,h//2+2),fill=P['shade']);wood(d,(1,h-19,w-3,14))
  if key=='library-window':
   d.polygon([(13,12),(28,12),(24,h-23),(13,h-23)],fill=P['red']);d.polygon([(w-29,12),(w-15,12),(w-15,h-23),(w-25,h-23)],fill=P['red'])
 elif key=='workshop-vent':
  wood(d,(3,8,w-6,h-16));d.rectangle((12,17,w-14,h-20),fill=P['darkmetal'])
  for y in range(20,h-24,7):d.line((15,y,w-17,y),fill=P['metal'],width=2);d.line((15,y+2,w-17,y+2),fill=P['edge'])
 elif key in ['rune-board','notice-board','notice-restored']:
  shadow(d,w,h);wood(d,(4,4,w-10,h-12));d.rectangle((13,13,w-19,h-24),fill='#304e46'if key=='rune-board'else '#bda06b')
  if key=='rune-board':
   d.line((32,30,62,30),fill=P['paper'],width=3);d.line((46,24,46,56),fill=P['paper'],width=3);d.line((28,72,69,72),fill=P['paper'],width=3);d.line((69,72,69,88),fill=P['paper'],width=3)
  else:
   for i,(x,y)in enumerate([(22,24),(66,20),(40,59)]):
    d.rectangle((x,y,x+32,y+28),fill=P['paper']);d.ellipse((x+14,y-2,x+18,y+2),fill=P['red']);d.line((x+5,y+9,x+24,y+9),fill=P['shade']);d.line((x+5,y+15,x+19,y+15),fill=P['green']if key=='notice-restored'else P['shade'])
 elif key=='parcel':
  shadow(d,w,h);wood(d,(4,13,37,29));d.line((21,13,21,40),fill=P['paper'],width=3);d.line((5,26,39,26),fill=P['paper'],width=2)
 elif key=='fragment':
  d.polygon([(7,9),(29,5),(34,14),(29,33),(6,32)],fill=P['paper']);d.line((12,16,25,16),fill=P['green'],width=2);d.line((18,13,18,25),fill=P['green'],width=2)
 frames[key]=im;im.save(S/(key+'.png'))
# Full native floor/wall receivers; independent props/actors remain depth sorted in Phaser, no flattened fake room.
for name,w,h,kind in [('seed-shop',704,512,'stone'),('bookshop',640,544,'wood'),('workshop',704,480,'workshop')]:
 im=Image.new('RGBA',(w,h),'#1c2b29');d=ImageDraw.Draw(im);d.rectangle((26,40,w-27,h-20),fill='#5a4e3c');d.rectangle((32,48,w-33,132),fill='#d2c3a3'if kind!='workshop'else '#aeb9ae');d.rectangle((32,112,w-33,138),fill=P['shade']);d.line((34,113,w-35,113),fill=P['lit'],width=2)
 if kind=='wood':
  for y in range(140,h-24,16):
   for x in range(32-((y//16)%3)*24,w-32,72):
    c=['#94704c','#9d7953','#8d6c4c','#a48159'][(x//24+y//16)%4];d.rectangle((max(32,x),y,min(w-33,x+70),y+14),fill=c);d.line((max(33,x+3),y+2,min(w-34,x+65),y+2),fill='#c4a071');d.line((max(33,x+8),y+9,min(w-34,x+52),y+10),fill='#785c41')
  d.rectangle((208,310,380,424),fill='#446359');d.rectangle((212,314,376,420),outline='#ddca94',width=3)
  for x in range(218,373,10):d.line((x,320,x,414),fill='#668276');d.line((218,318,370,318),fill='#b9b286')
 else:
  tw,th=(36,20)if kind=='stone'else(28,18)
  for y in range(140,h-24,th):
   for x in range(32-tw//2*((y//th)%2),w-32,tw):
    colors=['#b8af94','#b3a98d','#c1b69c','#b2a88d']if kind=='stone'else['#8c9991','#93a097','#8a978e','#a0aaa0'];d.rectangle((max(32,x),y,min(w-33,x+tw-2),y+th-2),fill=colors[(x//tw+y//th)%4]);d.line((max(33,x+2),y+1,min(w-34,x+tw-4),y+1),fill='#d8cdb1'if kind=='stone'else '#bdc6b7');
    if x>=32 and x+tw<w-32:d.line((x+tw-7,y+th-7,x+tw-4,y+th-6),fill='#928975'if kind=='stone'else '#74867e')
 if kind=='workshop':
  d.rectangle((398,315,522,344),outline='#b99e63',width=2)
 d.rectangle((27,h-25,w-28,h-20),fill=P['shade']);d.line((32,h-26,w-33,h-26),fill=P['lit'],width=2);im.save(O/(name+'-ground.png'));im.save(S/(name+'-ground.png'))
# Uniform logical atlas cells, exact per-source frame bounds; never scale to fake actor proportions.
atlas=Image.new('RGBA',(2048,480));meta={}
for i,(k,im)in enumerate(frames.items()):
 x=(i%8)*256;y=(i//8)*160;atlas.alpha_composite(im,(x,y));meta[k]={'frame':{'x':x,'y':y,'w':im.width,'h':im.height},'rotated':False,'trimmed':False,'spriteSourceSize':{'x':0,'y':0,'w':im.width,'h':im.height},'sourceSize':{'w':im.width,'h':im.height}}
atlas.save(O/'kit.png');(O/'kit.json').write_text(json.dumps({'frames':meta,'meta':{'image':'kit.png','scale':'1','art_source':'code'}},indent=2)+'\n');files={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in O.iterdir()if p.is_file()};(S/'PROVENANCE.json').write_text(json.dumps({'art_source':'code','disclosure':'Original code-drawn native components, no image model','source':'tools/roadmap-v4/room_art.py','providerCalls':0,'thirdPartyReferences':[],'sourcePixelScale':1,'worldOrCharactersChanged':False,'independentProps':len(frames),'floorReceivers':3,'nativeSampling':'nearest','review':'PENDING_HUMAN_ART_REVIEW','runtimeHashes':files},indent=2)+'\n');print('Authored',len(frames),'nativecomponents/3distinctfloorreceivers; no image model')
