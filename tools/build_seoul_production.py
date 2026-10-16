"""Author approved geometry; generated pixels only, actual pinned Forge exports. No API calls."""
from pathlib import Path
import json,copy,math,shutil,hashlib,sys
from PIL import Image,ImageDraw
import numpy as np
from production_art import R,S,C,F,run,write,sha
G=R/'assets-src/gwanghwamun';W,H=4096,1728
Z=json.loads((R/'docs/urban-zoning/zoning-plan.json').read_text());old=json.loads((G/'map-bundle.json').read_text());M=F/'skills/generate2dmap/scripts'
B={'schema':'generate2dmap.map_bundle.v2','id':'seoul-production-north','name':'Living Seoul — Gateway, Scholars & Inventions','world':{'width':W,'height':H,'unit':'px'},'tile_size':[32,32],'tilesets':[{'id':'town','manifest':'tileset.json'}],'layers':[{'name':'Ground','kind':'tiles','data':'layers/ground.json','tileset':'town'},{'name':'Edging','kind':'tiles','data':'layers/edging.json','tileset':'town'},{'name':'Props','kind':'objects'}],'props':{},'objects':[],'collision':{'actorRadius':8,'ySquash':.5,'walkRegions':[{'polygon':[[32,32],[W-32,32],[W-32,H-32],[32,H-32]]}],'solids':[],'rects':[]},'nav':{'cell':8},'spawns':[{'id':'start','x':1920,'y':1328,'facing':'north'},{'id':'academy-return','x':672,'y':832,'facing':'south'}],'anchors':{},'interactions':[],'portals':[],'camera':{'tiltDeg':50,'pixelToWorld':1,'bounds':[0,0,W,H]},'art_source':'host_image'}
# Old pixels retained, distinct production-only texture names avoid cache collisions.
for name in ['tree','ginkgo','lantern','bench','jars','planter','sejong']:
 p=copy.deepcopy(old['props'][name]);p['image']='../gwanghwamun/'+p['image'];p['solid']=False;B['props']['prod-'+name]=p
for p in json.loads((S/'props.json').read_text()):
 B['props'][p['id']]={'image':p['image'],'sha256':p['sha256'],'anchor_px':[p['size'][0]//2,p['size'][1]-2],'size':p['size'],'footprint':{'shape':'rect','width':24,'depth':16,'offset':[0,-8],'basis':'world_px'},'solid':False,'occlusion_class':'tall','occupant_policy':'y_sort'}
def place(prop,x,y,why,depth=None):
 p=B['props'][prop];B['objects'].append({'id':f'production-{len(B["objects"])+1}','prop':prop,'x':x,'y':y,'sortY':y if depth is None else depth,'scale':1,'anchor_px':p['anchor_px'],'occlusion':'tall','occluder':{'source':p['image'],'alphaThreshold':128},'purpose':why})
def solid(x,y,w,h,why): B['collision']['solids'].append({'shape':'rect','x':x,'y':y,'w':w,'h':h,'reason':why})
def anchor(id,x,y,ax=None,ay=None):
 B['anchors'][id]={'point':[x,y],'approach':[ax if ax is not None else x,ay if ay is not None else y]};B['interactions'].append({'id':id,'x':x,'y':y,'reach':96})
# EXACT approved structural footprint bounds. Courtyards are deliberately left walkable.
for ident in ['academy','workshop','museum']:
 building=next(b for b in Z['buildings'] if b['id']==ident)
 for mass in building['masses']:solid(*mass['bounds'],f'{building["code"]}:{mass["id"]} approved mass')
place('prod-hall',672,790,'A01 five-bay lecture facade; open south entrance')
place('prod-study',384,1072,'A01 long west study wing; independent Y-sorted roof')
place('prod-library',960,1008,'A01 shorter east library wing; independent roof')
place('prod-workshop',3312,850,'H01 asymmetric main hall + east tool wing, empty L-court stays open')
place('prod-museum',3520,1272,'H02 long naval-history hall + offset west entrance vestibule')
place('prod-sejong',2280,1184,'P01 bronze Hangul monument; not rejected NPC art')
solid(2240,1088,80,96,'P01 approved monument base')
# Gate mass divided around a real 80px passage; dynamic door collision is added at runtime.
place('prod-gate',2048,758,'G01 original ceremonial gate, three stone arches')
solid(1856,544,152,192,'G01 west podium; center passage clear')
solid(2088,544,152,192,'G01 east podium; center passage clear')
# Closed palace inner reserve and coherent original seven boundary segments.
solid(1296,32,1504,400,'Inner palace remains reserved closed; no new palace district')
for seg in Z['palace']['segments']:
 (x,y),(xx,yy)=seg['points']
 if y==yy:
  solid(x,y-16,xx-x,32,seg['id']);n=math.ceil((xx-x)/148)
  for i in range(n):place('prod-wall',round(x+(i+.5)*(xx-x)/n),y+16,'Palace boundary '+seg['id'],y+16)
 else:
  solid(x-16,y,32,yy-y,seg['id']);n=math.ceil((yy-y)/176)
  for i in range(n):place('prod-wall-ns',x,round(y+(i+1)*(yy-y)/n),'Palace boundary '+seg['id'])
for x in [1280,2816]:
 place('prod-service',x,448,'Closed palace service gate; original boundary gap')
 solid(x-32,336,64,96,'Closed palace service threshold')
# North edge of first outer court: inner palace is closed, outer visit only through main gate.
for x in range(1360,2800,148):place('prod-wall',x,448,'Inner reserved-palace return, keeps first outer court bounded',448)
solid(1296,416,1504,32,'Inner palace court closed')
# Boundary fence uses low domestic garden walls only around functional courts, no town fortress.
for x in [480,864]:place('prod-low-wall',x,1152,'Academy south court edge; clear 224px entrance')
place('prod-court-gate',672,1152,'Academy open courtyard threshold')
for x in [400,816]:solid(x,1136,160,16,'Academy low front court wall')
# Small contextual exhibits with explicit foot bases and cultural purposes.
for prop,x,y,why,w,d in [
 ('prod-writing',552,1000,'Academy courtyard primer and brush display',68,28),
 ('prod-armillary',3680,822,'Workshop approved observation platform: celestial sphere',64,36),
 ('prod-sundial',3112,988,'Workshop demonstration: hemispherical sundial',60,32),
 ('prod-clock',3520,1040,'Workshop demonstration: water clock',68,32),
 ('prod-strategy',3408,1380,'Museum west terrace strategy table',84,32),
 ('prod-ship',3712,1412,'Museum miniature exhibit, no invented harbor',80,32)]:
 place(prop,x,y,why);solid(x-w/2,y-d,w,d,why)
# Landscape and furnishings are authored at destination edges, never on entrances/NPC reservations.
for prop,positions,purpose in [
 ('prod-lantern',[(592,1176),(752,1176),(1776,864),(2320,864),(3104,1152),(3232,1152),(3280,1352),(3856,1424),(1456,1336),(2640,1456)],'Entrance / street-turn wayfinding'),
 ('prod-bench',[(1552,1104),(2496,1104),(768,1064),(3072,1056),(3912,1384),(1728,1344)],'Off-route social / reading rest'),
 ('prod-planter',[(512,828),(832,828),(3200,704),(3328,704),(3424,1296),(3664,1296),(1760,1200),(2432,1200)],'Destination facade / plaza planting'),
 ('prod-jars',[(3000,760),(3032,792),(1040,1040),(1072,1072),(3880,1216)],'Service storage beside appropriate courtyard')]:
 for x,y in positions:place(prop,x,y,purpose)
# Native generated terrain; road/court masks are editable planning DATA, not code-painted art.
material=Image.new('L',(W,H),0);d=ImageDraw.Draw(material)
for road in Z['roads']:
 pts=road['points'];d.line([tuple(p) for p in pts],fill=1,width=road['clearWidth']+20,joint='curve')
 for x,y in pts:
  r=(road['clearWidth']+20)//2;d.ellipse((x-r,y-r,x+r,y+r),fill=1)
for court in Z['courts']:
 if min(p[1]for p in court['polygon'])<H and court['belongsTo'] in ['gate','academy','monument','workshop','museum','plaza']:
  d.polygon([tuple(p)for p in court['polygon']],fill=2 if court['belongsTo'] in ['academy','workshop'] else 1)
d.rectangle((1760,448,2336,544),fill=1);d.rectangle((2008,512,2088,832),fill=1)
# Grounding each mass uses earth/stone under source-generated architecture.
for b in Z['buildings']:
 if b['id'] in ['gate','academy','workshop','museum']:
  for mass in b['masses']:
   x,y,w,h=mass['bounds'];d.rectangle((x,y,x+w,y+h),fill=2)
# Add ordered planting groups matching approved parcels and street buffers.
positions=[]
for row,y in enumerate([180,340,500]):
 for col,x in enumerate([160,350,550,760,970]):positions.append((x+(row%2)*40,y+(col%2)*24,'Academy orchard backdrop'))
for row,y in enumerate([150,325]):
 for col,x in enumerate([3032,3232,3432,3632,3856]):positions.append((x+(row%2)*24,y+(col%2)*20,'Workshop rear service-yard orchard edge'))
for x,y in [(140,760),(180,980),(160,1200),(280,1392),(512,1456),(752,1432),(1000,1488),(1112,1640),(1480,1648),(1656,1528),(1840,1608),(2040,1648),(2256,1584),(2472,1608),(3000,1472),(3136,1730),(3760,1656),(3976,1152),(3984,944),(2944,912),(2872,1072),(1120,712),(1120,920),(2608,1072),(1440,984),(1544,864),(2440,856),(2704,912)]:positions.append((x,y,'Planted street / district-edge buffer; no random street obstruction'))
for i,(x,y,purpose) in enumerate(positions):
 if y>H-32:continue
 place('prod-ginkgo' if i%3==0 else 'prod-tree',x,y,purpose)
 solid(x-12,y-16,24,16,'Tree trunk only; canopy not a solid')
# Reserve southern Stage C continuations. No fake finished buildings/water placed here.
solid(32,H-48,W-64,16,'Review boundary; southern districts await Stage B approval')
for id,x,y,ax,ay in [('gateway',2048,768,2048,832),('outer-court',2048,496,2048,496),('academy',672,800,672,832),('academy-front',672,1136,672,1200),('workshop',3168,1120,3168,1184),('armillary',3680,822,3680,880),('museum',3552,1280,3552,1392),('sejong-monument',2280,1208,2280,1248),('west-service',1200,400,1200,400),('history-return',3008,1600,3008,1600)]:anchor(id,x,y,ax,ay)
B['portals']=[{'id':'academy-door','circle':[672,800,16],'to':'seoul-production-reading-room:start','entranceByFrom':{'seoul-production-reading-room':[672,832]},'latch':True,'reciprocal':True}]
# Base tiles copied exactly from accepted generated texture sheet; masks keep their RGB values.
source=Image.open(G/'tiles.png').convert('RGBA');tiles=[source.crop(((i%4)*32,(i//4)*32,(i%4+1)*32,(i//4+1)*32))for i in range(8)]
unique=[];lookup={};ground=[];edging=[];a=np.array(material)
def register(im):
 key=im.tobytes()
 if key not in lookup:lookup[key]=len(unique);unique.append(im)
 return lookup[key]
for row in range(H//32):
 gr=[];ed=[]
 for col in range(W//32):
  variation=(col*17+row*29+col*row)%2;gr.append(register(tiles[4+variation]));mask=a[row*32:(row+1)*32,col*32:(col+1)*32]
  if not mask.any():ed.append(-1);continue
  out=Image.new('RGBA',(32,32))
  for val,index in [(1,variation),(2,2+variation)]:
   rgb=tiles[index].copy();rgb.putalpha(Image.fromarray((mask==val).astype('uint8')*255));out.alpha_composite(rgb)
  ed.append(register(out))
 ground.append(gr);edging.append(ed)
columns=16;atlas=Image.new('RGBA',(columns*32,math.ceil(len(unique)/columns)*32))
for i,im in enumerate(unique):atlas.paste(im,((i%columns)*32,(i//columns)*32))
atlas.save(S/'tiles.png');write(S/'tileset.json',{'schema':'generate2dmap.tileset.v1','image':'tiles.png','sha256':sha(S/'tiles.png'),'tile_size':[32,32],'columns':columns,'kind':'flat','materials':['grass','granite','earth'],'tiles':[{'index':i,'properties':{'material':'generated-terrain-with-approved-geometry-alpha','walkable':True}}for i in range(len(unique))],'seamless_verified':False,'art_source':'host_image','note':'Unchanged approved RGB; new authored semantic alpha variants, not procedural painted terrain.'})
write(S/'layers/ground.json',ground);write(S/'layers/edging.json',edging);material.save(S/'layers/terrain-material-mask.png')
write(S/'outdoor-draft.json',B)
hashed=C/f'production-hashed-{sha(S/"outdoor-draft.json")[:12]}.json'
if not hashed.exists():run(M/'map_bundle.py','hash','--bundle',S/'outdoor-draft.json','--output',hashed)
shutil.copyfile(hashed,S/'outdoor-bundle.json')
run(M/'map_bundle.py','validate','--bundle',S/'outdoor-bundle.json','--report',C/f'validation-{len(json.loads((S/"commands.json").read_text()))}.json')
for part,script,args in [('navigation','map_nav.py',['check','--publish-on-fail']),('tiled','export_tiled.py',['export','--embedded-variant'])]:
 dest=S/part
 if dest.exists():shutil.move(dest,C/f'previous-{part}-{len(json.loads((S/"commands.json").read_text()))}')
 run(M/script,*args,'--bundle',S/'outdoor-bundle.json','--output-dir',dest)
# Exact exported collision rectangles form the actual Phaser static bodies.
t=json.loads((S/'tiled/map.embedded.tmj').read_text());collision=next(l for l in t['layers'] if l['name']=='collision');solids=[o for o in collision['objects'] if o['type']=='solid'];assert all(not o.get('polygon') for o in solids)
t['layers']=[l for l in t['layers'] if l['type']=='tilelayer']+[dict(collision,name='Collision',objects=solids)];t['tilesets']=[dict(t['tilesets'][0],image='tiles.png')]
D=R/'public/review/seoul-production';D.mkdir(parents=True,exist_ok=True);write(D/'plaza.json',t);shutil.copyfile(S/'tiles.png',D/'tiles.png')
for name,p in B['props'].items():shutil.copyfile(S/p['image'],D/f'{name}.png')
write(D/'anchors.json',{name:p['anchor_px']for name,p in B['props'].items()})
world={'width':W,'height':H,'spawn':[1920,1328],'npc':[2280,1248],'follow':55,'role':B['name'],'mood':'Northern Stage B review','vi':B['name'],'mapSha256':sha(D/'plaza.json'),'objects':[{'id':i+1,'kind':o['prop'],'x':o['x'],'y':o['y'],'width':B['props'][o['prop']]['footprint']['width'],'height':B['props'][o['prop']]['footprint']['depth'],'label':o['purpose'],'collide':False}for i,o in enumerate(B['objects'])]}
write(S/'world.json',world)
write(S/'geometry-proof.json',{'masterplanSha256':sha(R/'docs/urban-zoning/zoning-plan.json'),'world':[W,H],'fullApprovedWorld':Z['world'],'masses':[{'building':b['id'],'masses':b['masses']}for b in Z['buildings'] if b['id'] in ['gate','academy','workshop','museum']],'palaceWalls':Z['palace']['segments'],'npcReservations':Z['npcs'],'firstSliceOnly':True,'gatePolicy':'Runtime dynamic leaf opens only first outer court; reserved inner palace remains closed. Static navigation bundle represents gate OPEN; runtime tests separately prove closed/open.'})
print('Production map exported; inspect raw QA and real Phaser before review.')
