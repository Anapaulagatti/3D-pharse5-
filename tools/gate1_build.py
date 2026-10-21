"""Compile ONLY one new Gate1 scene. No full-map or rejected-south inputs."""
import hashlib,json,shutil
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate1';M=S/'map';P=R/'public/assets/gate1';M.mkdir(exist_ok=True);P.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def build():
 full=Image.open(S/'native/street-foundation.png').convert('RGBA');w,h=full.size;assert(w,h)==(1536,1024)
 floor=full.copy();floor.paste((0,0,0,0),(0,0,w,576));floor.save(M/'floor.png')
 props={};objects=[];anchors={};worldObjects=[]
 def prop(name,image,anchor,existing=False):
  shutil.copy2(image,M/(name+'.png'));im=Image.open(image)
  props[name]=dict(image=name+'.png',size=list(im.size),anchor_px=anchor,solid=False,art_source='existing'if existing else'host_image');anchors[name]=anchor
 def put(name,x,y,depth=None):
  key=f'gate1-{len(objects)+1}';objects.append(dict(id=key,prop=name,x=x,y=y,sortY=y if depth is None else depth,scale=1,anchor_px=anchors[name]));worldObjects.append(dict(id=len(objects),kind=name,x=x,y=y,width=0,height=0,label=name,collide=False))
 arch=full.crop((0,0,w,576));arch.save(M/'architecture.png');props['architecture']=dict(image='architecture.png',size=[w,576],anchor_px=[0,576],solid=False,art_source='host_image');anchors['architecture']=[0,576];put('architecture',0,576,560)
 for name in ['bench-front','bench-back','light','tree-planter','bikes','flowerbox']:
  image=S/'native'/(name+'.png');im=Image.open(image);prop(name,image,[im.width//2,im.height])
 tree=R/'assets-src/library/native/rf-prod-tree.png';prop('heritage-tree',tree,[94,195],True)
 # Deliberate corner planting and an inward-facing seating court, at native scale.
 for x,y in [(64,920),(1496,624)]:put('tree-planter',x,y);put('heritage-tree',x,y-5)
 put('bench-front',1216,872);put('bench-back',1216,988)
 put('light',744,624);put('light',1464,968)
 put('bikes',1440,616);put('flowerbox',1080,1008)
 # Painted-source architecture and low boundaries; these exact rectangles also feed Tiled.
 solids=[dict(shape='rect',x=0,y=0,w=w,h=560,reason='New adjoining street wall, no walk-through facade'),dict(shape='rect',x=0,y=896,w=312,h=128,reason='Outside-slice heritage forecourt behind the closed low boundary; not a public path')]
 for x,y,ww,hh in [(0,720,176,72),(0,808,304,88),(272,880,40,144),(304,832,176,72),(736,832,48,192),(784,792,96,40),(1096,776,224,56),(1312,816,104,64),(1384,872,64,152),(736,960,128,64)]:solids.append(dict(shape='rect',x=x,y=y,w=ww,h=hh,reason='Measured new-source low wall/raised planting'))
 for x in [54,294,748,1384,1476]:solids.append(dict(shape='rect',x=x-6,y=616,w=12,h=12,reason='Painted curb bollard'))
 for o in objects:
  name=o['prop'];x=o['x'];y=o['y']
  if name=='heritage-tree':solids.append(dict(shape='rect',x=x-8,y=y-8,w=16,h=8,reason='Protected-source tree trunk, not canopy'))
  elif name in['bench-front','bench-back','tree-planter','bikes','flowerbox','light']:
   ww={'bench-front':92,'bench-back':92,'tree-planter':64,'bikes':96,'flowerbox':88,'light':12}[name];hh=12 if name!='light'else 8;solids.append(dict(shape='rect',x=x-ww/2,y=y-hh,w=ww,h=hh,reason='New original '+name+' physical support'))
 venues=[dict(id='cafe',x=242,y=580,label='모퉁이 커피 · Cà phê góc phố',text='커피 · Cà phê.\nMột góc sáng ấm để dừng chân và trò chuyện.'),dict(id='bookshop',x=598,y=580,label='문장 책방 · Hiệu sách Munjang',text='책 · Sách.\nCửa kính mở tầm nhìn vào những kệ sách của khu phố.'),dict(id='learning',x=888,y=580,label='배움 · Không gian học',text='배우다 · Học.\nMột địa điểm dành cho các cuộc gặp và hoạt động học sau khi chuẩn mỹ thuật được duyệt.'),dict(id='convenience',x=1288,y=580,label='마루 편의점 · Cửa hàng Maru',text='가게 · Cửa hàng.\nGóc mua sắm quen thuộc của cư dân phố Muneum.'),dict(id='court',x=1120,y=928,label='만남 · Sân gặp gỡ',text='만나다 · Gặp gỡ.\nMột khoảng sân nhỏ có ghế đối diện, cây và hoa, nối trực tiếp với vạch qua đường.')]
 targets=[dict(id=v['id'],x=v['x'],y=v['y'],radius=12)for v in venues]
 b=dict(schema='generate2dmap.map_bundle.v2',id='gate1-muneum',world=dict(width=w,height=h,unit='px'),art_source='mixed',layers=[dict(name='original-ground',kind='image',image='floor.png',x=0,y=0),dict(name='original-architecture-and-street-furniture',kind='objects')],props=props,objects=objects,collision=dict(actorRadius=8,ySquash=.5,solids=solids),spawns=[dict(id='entry',x=192,y=590,facing='right')],anchors={t['id']:dict(point=[t['x'],t['y']],approach=[t['x'],t['y']])for t in targets})
 write(M/'bundle.json',b);write(M/'anchors.json',anchors);write(M/'venues.json',venues)
 # Lossless32px dictionary of ORIGINAL authored image; no repeated placeholder materials.
 tiles=[];lookup={};data=[]
 for yy in range(0,h,32):
  for xx in range(0,w,32):
   im=floor.crop((xx,yy,xx+32,yy+32));key=im.tobytes()
   if key not in lookup:lookup[key]=len(tiles);tiles.append(im)
   data.append(lookup[key]+1)
 atlas=Image.new('RGBA',(4096,((len(tiles)+127)//128)*32))
 for i,tile in enumerate(tiles):atlas.paste(tile,((i%128)*32,(i//128)*32))
 atlas.save(M/'tiles.png')
 tm=dict(compressionlevel=-1,height=h//32,width=w//32,infinite=False,orientation='orthogonal',renderorder='right-down',tileheight=32,tilewidth=32,type='map',version='1.10',tiledversion='1.10.2',nextlayerid=4,nextobjectid=len(solids)+1,layers=[dict(id=1,name='Ground',type='tilelayer',width=w//32,height=h//32,data=data,opacity=1,visible=True,x=0,y=0),dict(id=2,name='Edging',type='tilelayer',width=w//32,height=h//32,data=[0]*len(data),opacity=1,visible=True,x=0,y=0),dict(id=3,name='Collision',type='objectgroup',visible=True,opacity=1,x=0,y=0,objects=[dict(id=i+1,x=s['x'],y=s['y'],width=s['w'],height=s['h'],rotation=0,name=s['reason'],type='',visible=True)for i,s in enumerate(solids)])],tilesets=[dict(columns=128,firstgid=1,image='tiles.png',imageheight=atlas.height,imagewidth=atlas.width,margin=0,name='town',spacing=0,tilecount=len(tiles),tileheight=32,tilewidth=32)])
 write(M/'plaza.tmj',tm);write(P/'plaza.json',tm)
 for name in props:shutil.copy2(M/props[name]['image'],P/(name+'.png'))
 shutil.copy2(M/'tiles.png',P/'tiles.png')
 world=dict(width=w,height=h,spawn=[192,590],npc=[1120,928],follow=48,role='Gate1 original Korean street',mood='day',vi='Phố Muneum',mapSha256=sha(M/'bundle.json'),objects=worldObjects)
 write(M/'world.json',world)
 write(S/'build-proof.json',dict(world=[w,h],source=sha(S/'originals/street-foundation.png'),native=sha(S/'native/street-foundation.png'),majorArtSpatialScale=1,tiles=len(tiles),solids=len(solids),doors=len(venues),northFullMapModified=False))
 print(json.dumps(dict(status='BUILT_GATE1_ONLY',world=[w,h],objects=len(objects),solids=len(solids),tiles=len(tiles))))
if __name__=='__main__':build()
