"""Derived approved zoning/map data; literal approved/generated pixels, not painted RGB."""
from full_world_art import *
from PIL import ImageDraw
from stage_b_polish_map import terrain_layers
import copy,math,numpy as np
from scipy.ndimage import distance_transform_edt
P=S/'map';P.mkdir(exist_ok=True);W,H=4352,4800;COLS=W//32;ROWS=H//32
OFF={'heritage':(1024,0),'namsan':(0,2240),'entertainment':(3072,2240),'busan-coast':(1536,2496),'jeju':(1536,3648)}
plan=json.loads((R/'docs/living-korea/southern-masterplan.json').read_text())
B={'schema':'generate2dmap.map_bundle.v2','id':'full-korea','name':'Living Korea — Heritage to Windstone','world':{'width':W,'height':H,'unit':'px'},'tile_size':[32,32],'tilesets':[{'id':'town','manifest':'tileset.json'}],'layers':[{'name':'Ground','kind':'tiles','data':'layers/ground.json','tileset':'town'},{'name':'Edging','kind':'tiles','data':'layers/edging.json','tileset':'town'},{'name':'Props','kind':'objects'}],'props':{},'objects':[],'collision':{'actorRadius':8,'ySquash':.5,'walkRegions':[{'polygon':[[32,32],[W-32,32],[W-32,H-32],[32,H-32]]}],'solids':[],'rects':[]},'nav':{'cell':4},'spawns':[{'id':'start','x':2176,'y':832,'facing':'south'},{'id':'room-return','x':1568,'y':1152,'facing':'south'},{'id':'jeju-arrival','x':1760,'y':4544,'facing':'north'},{'id':'coast-arrival','x':2848,'y':3136,'facing':'north'}],'anchors':{},'interactions':[],'portals':[],'camera':{'tiltDeg':50,'pixelToWorld':1,'bounds':[0,0,W,H]},'art_source':'host_image'}
unique=[];lookup={}
def reg(im):
 key=im.convert('RGBA').tobytes()
 if key not in lookup:lookup[key]=len(unique);unique.append(im.convert('RGBA'))
 return lookup[key]
raw=Image.open(R/'assets-src/gwanghwamun/tiles.png').convert('RGBA');oldtiles=[raw.crop(((i%4)*32,(i//4)*32,(i%4+1)*32,(i//4+1)*32))for i in range(8)]
grass=[reg(oldtiles[4]),reg(oldtiles[5])];waters=[reg(oldtiles[6]),reg(oldtiles[7])]
ground=[[grass[(x*17+y*29+x*y)%2]for x in range(COLS)]for y in range(ROWS)];edge=[[-1]*COLS for _ in range(ROWS)]
def addsolid(x,y,w,h,why):B['collision']['solids'].append({'shape':'rect','x':x,'y':y,'w':w,'h':h,'reason':why})
def asset(key,path,size,anchor,meta=None):
 path=path.resolve();p=copy.deepcopy(meta)if meta else {'footprint':{'shape':'rect','width':24,'depth':12,'offset':[0,-6],'basis':'world_px'},'solid':False,'occlusion_class':'tall','occupant_policy':'y_sort'}
 p.update(image=os.path.relpath(path,P),sha256=sha(path),size=size,anchor_px=anchor)
 if key in B['props']:assert B['props'][key]['sha256']==p['sha256'],key
 B['props'][key]=p

def place(key,x,y,why,foot=None,depth=None):
 a=B['props'][key];B['objects'].append({'id':f'full-{len(B["objects"])+1:03}','prop':key,'x':x,'y':y,'sortY':y if depth is None else depth,'scale':1,'anchor_px':a['anchor_px'],'occlusion':'tall','occluder':{'source':a['image'],'alphaThreshold':128},'purpose':why})
 if foot:
  w,h=foot;a['footprint']={'shape':'rect','width':w,'depth':h,'offset':[0,-h/2],'basis':'world_px'};addsolid(x-w/2,y-h,w,h,why)
def anchor(key,x,y,ax,ay,reach=104):B['anchors'][key]={'point':[x,y],'approach':[ax,ay]};B['interactions'].append({'id':key,'x':x,'y':y,'reach':reach})
def stamp_layers(folder,dx,dy):
 a=Image.open(folder/'tiles.png').convert('RGBA');columns=json.loads((folder/'tileset.json').read_text())['columns'];cache={}
 for name,target in [('ground',ground),('edging',edge)]:
  data=json.loads((folder/f'layers/{name}.json').read_text())
  for y,row in enumerate(data):
   for x,i in enumerate(row):
    if i<0:continue
    if i not in cache:cache[i]=reg(a.crop(((i%columns)*32,(i//columns)*32,(i%columns+1)*32,(i//columns+1)*32)))
    target[dy//32+y][dx//32+x]=cache[i]
def import_zone(name,folder):
 dx,dy=OFF[name];old=json.loads((folder/'outdoor-bundle.json').read_text())
 for key,p in old['props'].items():asset(key,folder/p['image'],p['size'],p['anchor_px'],p)
 for o in old['objects']:
  q=copy.deepcopy(o);q['id']=f'{name}-{q["id"]}';q['x']+=dx;q['y']+=dy;q['sortY']=q['sortY']+dy if q['sortY']>=0 else q['sortY'];q['occluder']['source']=B['props'][q['prop']]['image'];B['objects'].append(q)
 for s in old['collision']['solids']:addsolid(s['x']+dx,s['y']+dy,s['w'],s['h'],name+': '+s.get('reason','existing structure'))
 for k,a in old['anchors'].items():
  p=a['point'];ap=a.get('approach',p);anchor(name+'-'+k,p[0]+dx,p[1]+dy,ap[0]+dx,ap[1]+dy)
 stamp_layers(folder,dx,dy)
import_zone('heritage',R/'assets-src/living-korea/north');import_zone('namsan',R/'assets-src/living-korea/park')
for kit in ['festival','coast','jeju','courtyards','infrastructure']:
 for p in json.loads((S/f'{kit}-props.json').read_text()):asset(p['id'],S/p['image'],p['size'],p['anchor'])
# All raw/new sources remain; reusable native runs use disjoint literal source pixels.
def run_image(name,key,width):
 p=B['props'][key];src=Image.open(P/p['image']).convert('RGBA');part=src.crop((16,0,src.width-16,src.height));out=Image.new('RGBA',(width,src.height))
 for x in range(0,width,part.width):out.paste(part.crop((0,0,min(part.width,width-x),part.height)),(x,0))
 dest=S/f'props/{name}.png';out.save(dest);asset(name,dest,list(out.size),[width//2,out.height-2]);return out
run_image('fw-rail-run','fw-rail',1312);run_image('fw-platform-run','fw-platform',1312)
# Purposeful off-route courtyard additions preserve all existing architectural silhouettes.
for k,x,y,foot,why in [('fw-royal-pavilion',1568,480,(160,40),'Royal west garden rest pavilion, not another enclosed hall'),('fw-scholar-rest',2432,480,(88,20),'Royal garden scholar rock/plum/bench'),('fw-hanji-desk',1312,1360,(88,24),'Academy outdoor writing display, away from hall entrance'),('fw-science',2848,1312,(110,24),'Workshop measuring exhibit, brass material identity'),('fw-maritime',2880,2064,(100,24),'Museum maritime garden, open pedestrian frontage'),('fw-bookstore',2752,2256,(232,48),'Contemporary cultural street bookshop, graduated red-brick frontage')]:place(k,x,y,why,foot)
anchor('garden-pavilion',1568,480,1568,528);anchor('bookstore',2752,2256,2752,2304)
# Distinct flower-and-kite leisure park; meaningful open arch, garden loop, individual ride masses.
def local(zone,key,x,y,why,foot=None,depth=None):
 dx,dy=OFF[zone];place(key,x+dx,y+dy,why,foot,depth+dy if depth is not None and depth>=0 else depth)
local('entertainment','fw-festival-gate',640,960,'Original Bora Bloom open flower arch',depth=960)
for x in [512,768]:addsolid(3072+x-20,2240+920,40,40,'Flower arch pier; centre passage remains open')
for k,x,y,f,why in [('fw-wheel',320,512,(248,64),'Garden wheel with distinct radial silhouette'),('fw-carousel',928,544,(264,72),'Petal carousel and public apron'),('fw-kiosk',640,432,(152,32),'Original modern refreshment/ticket kiosk')]:local('entertainment',k,x,y,why,f)
for x,y in [(128,640),(128,832),(1152,640),(1152,832),(352,976),(928,976),(256,320),(1088,320)]:local('entertainment','fw-flower-bed',x,y,'Curated open park flower boundary',(112,16))
for x,y in [(448,864),(832,864),(192,496),(1088,544)]:local('entertainment','fw-banner',x,y,'Flower festival wayfinding; rooted off public route',(20,12))
for x,y in [(128,192),(512,256),(768,256),(1152,192),(128,1088),(1152,1088)]:local('entertainment','rf-prod-tree',x,y,'Park shaded garden edge',(24,16))
anchor('bloom-wheel',3392,2752,3392,2832);anchor('bloom-carousel',4000,2784,4000,2864);anchor('bloom-arch',3712,3200,3712,3272)
# Coast: station north of rail, full rail/road continuity, one controlled pedestrian crossing.
local('busan-coast','fw-station',288,256,'Coastal station north of track, original modern arched roof',(264,48))
local('busan-coast','fw-rail-run',784,424,'Continuous1312px scenic rail strip, entirely on land',depth=-77)
local('busan-coast','fw-crossing',512,424,'Purpose-built north/south crossing across rail',depth=-76)
local('busan-coast','fw-platform-run',784,512,'Continuous public station platform edge',depth=-75)
local('busan-coast','fw-train',912,410,'Original stationary sightseeing train; wheels on rails',(224,64))
# Railroad blocks everywhere except the64px timber crossing; no walking through parked train.
addsolid(1664,2496+364,512-32-128,48,'Rail north barrier, west of crossing');addsolid(1536+544,2496+364,1440-544,48,'Rail north barrier, east of crossing')
local('busan-coast','fw-ferry-pavilion',1312,592,'Modern ferry waiting pavilion above shore',(200,32))
local('busan-coast','fw-jetty',1312,688,'Actual ferry jetty, land approach remains open',depth=-68)
local('busan-coast','fw-ferry',1312,864,'Small passenger ferry beside signed pier; not automatic transport',None)
# Inlet is a real obstacle; bridge spans its96px width with clear64px deck.
local('busan-coast','fw-inlet-bridge',848,716,'Bridge across real coastal inlet',depth=-69)
for q in [(800,560,96,72),(800,696,96,40)]:addsolid(1536+q[0],2496+q[1],q[2],q[3],'Inlet water outside bridge deck')
addsolid(1536+800,2496+632,96,8,'North bridge rail');addsolid(1536+800,2496+688,96,8,'South bridge rail')
addsolid(1536,2496+736,1536,416,'Sea: travel to Jeju by explicit ferry, never walking through water')
for x,y in [(224,728),(608,728),(1120,728)]:local('busan-coast','fw-sea-bench',x,y,'Promenade seating with sea-facing view',(100,20))
for x,y in [(96,192),(576,224),(1152,224),(1456,512)]:local('busan-coast','rf-prod-tree',x,y,'Station garden shade outside rail footprint',(24,16))
anchor('coast-station',1824,2768,1824,2816);anchor('rail-crossing',2048,2880,2048,2944);anchor('coast-bridge',2384,3160,2320,3160);anchor('coast-ferry',2848,3184,2848,3136)
# Windstone: volcanic hill, orchard and sculpture have wholly different source silhouettes.
for k,x,y,f,why in [('fw-oreum',736,448,(288,112),'Volcanic oreum hill, not walkable painted cliff'),('fw-guardian',384,752,(48,20),'Original basalt guardian cultural interpretation'),('fw-jeju-shelter',864,736,(180,40),'Timber and basalt coastal garden shelter')]:local('jeju',k,x,y,why,f)
for x,y in [(192,608),(416,416),(1088,352),(1248,608),(1216,944),(736,1024),(352,992)]:local('jeju','fw-tangerine',x,y,'Windstone orchard, planted outside loop',(28,16))
for x,y in [(160,800),(672,816),(960,832),(1248,864),(544,512)]:local('jeju','fw-coastal-garden',x,y,'Wind-shaped grasses and volcanic flower garden',(80,16))
for x,y in [(256,528),(416,528),(960,800),(1280,800),(640,1008),(800,1008)]:local('jeju','fw-basalt-wall',x,y,'Low basalt garden edge with deliberate route openings',(112,20))
local('jeju','fw-jetty',224,1024,'Jeju travel landing, safe approach north',depth=-68)
local('jeju','fw-ferry',224,1136,'Return ferry at island garden edge',None)
anchor('jeju-guardian',1920,4400,1920,4432);anchor('jeju-oreum',2272,4096,2240,4144);anchor('jeju-shelter',2400,4384,2400,4432);anchor('jeju-ferry',1760,4608,1760,4544)
# Editable routes in global coordinates. Foot links follow approved local paths plus explicit commons.
routes=[]
for z in plan['destinations']:
 if z['id']=='heritage':continue
 dx,dy=OFF[z['id']]
 for i,r in enumerate(z['routes']):routes.append({'id':z['id']+str(i),'zone':z['id'],'points':[[x+dx,y+dy]for x,y in r],'clearWidth':48 if z['id']=='namsan'else 64})
extra=[('heritage-to-commons',[[2176,2016],[2176,2368],[2048,2464],[2048,2784]],80),('commons-to-hill',[[2176,2368],[1600,2368],[1440,2464],[1280,2416],[1024,2416],[832,2560],[608,2624],[608,2928],[704,2992]],64),('commons-to-bloom',[[2176,2368],[2944,2368],[2992,2512],[2976,2784],[3136,2800],[3328,2816],[3456,2848]],80),('coast-to-bloom',[[2912,3160],[2912,3136],[3072,3136],[3328,3296],[3712,3296],[3712,3120]],80),('station-approach',[[2048,2944],[2048,2816],[1824,2816]],64),('jeju-arrival-loop',[[1760,4544],[1952,4480],[2080,4256]],64)]
extra.append(('rail-crossing',[[2048,2784],[2048,2944]],64))
for name,points,width in extra:routes.append({'id':name,'zone':'connector','points':points,'clearWidth':width})
# Two purposefully narrowed bridge approaches declare the actual48pxclear deck.
coast_route=next(r for r in routes if r['id']=='busan-coast0')
coast_route['points']=[[1792,3024],[1792,3136],[2176,3160],[2304,3160]]
routes.append({'id':'coastal-bridge','zone':'busan-coast','points':[[2304,3160],[2384,3160],[2464,3160]],'clearWidth':48})
routes.append({'id':'coastal-east-promenade','zone':'busan-coast','points':[[2464,3160],[2592,3160],[2912,3136]],'clearWidth':64})
next(r for r in routes if r['id']=='busan-coast1')['points']=[[1792,3024],[2176,3024],[2592,3024],[2656,3024],[2656,3136],[2912,3136]]
# Generate terrain from approved source textures per modest-size ROI, never code-painted RGB.
def paint_region(name,box,selected,base_material=None):
 x0,y0,x1,y1=box;w,h=x1-x0,y1-y0;out=P/'terrain'/name;out.mkdir(parents=True,exist_ok=True)
 m=base_material.copy()if base_material is not None else Image.new('L',(w,h),0);draw=ImageDraw.Draw(m)
 for r in selected:
  pts=[(x-x0,y-y0)for x,y in r['points']];width=r['clearWidth']+24;draw.line(pts,fill=2 if name in ['hill','jeju']else 4,width=width,joint='curve')
  for x,y in pts:draw.ellipse((x-width//2,y-width//2,x+width//2,y+width//2),fill=2 if name in ['hill','jeju']else 4)
 m.save(out/'semantic-materials.png');g,e=terrain_layers(m,oldtiles,reg,output_root=out)
 # For connectors, overlay only near new path. Existing native ground outside remains exact.
 coverage=None
 if name=='commons':coverage=distance_transform_edt(np.array(m)==0)<24
 for y in range(h//32):
  for x in range(w//32):
   gy=y0//32+y;gx=x0//32+x
   if coverage is None:ground[gy][gx]=g[y][x];edge[gy][gx]=e[y][x]
   else:
    mask=coverage[y*32:y*32+32,x*32:x*32+32]
    if not mask.any():continue
    rgb=unique[g[y][x]].copy()
    if e[y][x]>=0:rgb.alpha_composite(unique[e[y][x]])
    prior=unique[ground[gy][gx]].copy()
    if edge[gy][gx]>=0:prior.alpha_composite(unique[edge[gy][gx]])
    prior.paste(rgb,(0,0),Image.fromarray(mask.astype('uint8')*255));edge[gy][gx]=reg(prior)
 return m
paint_region('hill',(0,2240,1408,3520),[r for r in routes if r['id']=='commons-to-hill'],Image.open(R/'assets-src/living-korea/park/semantic-materials.png'))
for z in ['entertainment','busan-coast','jeju']:
 zone=next(v for v in plan['destinations']if v['id']==z);dx,dy=OFF[z];w,h=zone['world'];paint_region('jeju'if z=='jeju'else z,(dx,dy,dx+w,dy+h),[r for r in routes if r['zone']==z])
paint_region('commons',(1280,2016,3456,3392),[r for r in routes if r['zone']=='connector'and r['id']!='jeju-arrival-loop'])
# Authored continuous coast and island outline: real source water/sand, not rectangular panels.
sea=Image.new('L',(W,H),0);sd=ImageDraw.Draw(sea)
coastline=[(1536,3232),(1568,3232),(2144,3232),(2304,3200),(2640,3232),(3040,3200),(3072,3232),(3072,H),(1536,H)]
sd.polygon(coastline,fill=255);sd.rectangle((0,3520,W-1,H-1),fill=255);sd.rectangle((2336,3056,2431,3232),fill=255)
island=Image.new('L',(W,H),0);isd=ImageDraw.Draw(island)
island_points=[(1696,4064),(1856,3936),(2080,3872),(2336,3872),(2592,3936),(2816,4096),(2880,4384),(2816,4624),(2496,4704),(2048,4704),(1696,4672),(1600,4480),(1600,4224)]
isd.polygon(island_points,fill=255);sea.paste(0,(0,0),island)
sea.save(P/'sea-mask.png');island.save(P/'island-mask.png')
swatches={name:Image.open(S/f'terrain-native/{name}.png').convert('RGBA')for name in ['forest','sand','basalt','brick']}
def swatch_tile(name,x,y):return swatches[name].crop(((x%4)*32,(y%4)*32,(x%4+1)*32,(y%4+1)*32))
# Natural near-shore material transition uses original generated sand pixels.
wa=np.array(sea);water_cells=wa.reshape(ROWS,32,COLS,32).mean(axis=(1,3))>96
x0,y0,x1,y1=1504,3008,3104,H
near=distance_transform_edt(wa[y0:y1,x0:x1]==0)<32
for y in range(y0//32,ROWS):
 for x in range(x0//32,x1//32):
  wet=wa[y*32:y*32+32,x*32:x*32+32]>0
  dryshore=near[y*32-y0:y*32-y0+32,x*32-x0:x*32-x0+32]&~wet
  if not wet.any()and not dryshore.any():continue
  rgb=unique[ground[y][x]].copy()
  if edge[y][x]>=0:rgb.alpha_composite(unique[edge[y][x]])
  if dryshore.any():rgb.paste(swatch_tile('sand',x,y),(0,0),Image.fromarray(dryshore.astype('uint8')*255))
  if wet.any():rgb.paste(oldtiles[6+(x+y)%2],(0,0),Image.fromarray(wet.astype('uint8')*255))
  if wet.all():ground[y][x]=waters[(x+y)%2];edge[y][x]=-1
  else:edge[y][x]=reg(rgb)
# Basalt garden and cultural brick aprons give distinct places distinct ground language.
for name,cx,cy,rx,ry in [('basalt',1920,4400,96,64),('basalt',2400,4416,144,64),('brick',2752,2304,144,48),('brick',3712,3088,160,128)]:
 noise=np.array(swatches['forest'].convert('L'),dtype=float);noise=(noise-noise.mean())/max(1.,noise.std())
 for y in range((cy-ry-16)//32,(cy+ry+48)//32):
  for x in range((cx-rx-16)//32,(cx+rx+48)//32):
   yy,xx=np.indices((32,32));wx=x*32+xx;wy=y*32+yy
   mask=((wx-cx)/rx)**2+((wy-cy)/ry)**2 < 1+.10*noise[(wy//2)%128,(wx//2)%128].clip(-1.5,1.5)
   if not mask.any():continue
   rgb=unique[ground[y][x]].copy()
   if edge[y][x]>=0:rgb.alpha_composite(unique[edge[y][x]])
   rgb.paste(swatch_tile(name,x,y),(0,0),Image.fromarray(mask.astype('uint8')*255));edge[y][x]=reg(rgb)
# Navigable area has an island outline and purposeful connector lanes; sea/forest is not filler land.
walk=np.zeros((ROWS,COLS),dtype=bool)
def walkrect(x,y,w,h):walk[y//32:(y+h)//32,x//32:(x+w)//32]=True
for z in plan['destinations']:
 if z['id']=='jeju':continue
 dx,dy=OFF[z['id']];w,h=z['world'];walkrect(dx+32,dy+32,w-64,h-64)
walk|=np.array(island).reshape(ROWS,32,COLS,32).mean(axis=(1,3))>200
for q in [(1344,2080,1920,544),(2912,3040,512,352),(3008,2752,256,192)]:walkrect(*q)
blocked=(~walk)
# Bridge deck is the only deliberate walkable span across inlet water; rails stay physical.
blocked[3136//32:3200//32,2336//32:2432//32]=False
active={};outside=[]
for y in range(ROWS+1):
 runs=[];row=blocked[y]if y<ROWS else np.zeros(COLS,dtype=bool);x=0
 while x<COLS:
  if not row[x]:x+=1;continue
  start=x
  while x<COLS and row[x]:x+=1
  runs.append((start,x))
 nxt={run:active.get(run,y)for run in runs}
 for (a,b),sy in active.items():
  if (a,b)not in nxt:outside.append([a*32,sy*32,(b-a)*32,(y-sy)*32])
 active=nxt
for q in outside:addsolid(*q,'Nonwalking forest/sea frame; explicit bridge/ferry access')
# Actual water gets16pxboundary cells so a dry north promenade is not blocked by a32pxinlet tile.
water16=wa.reshape(H//16,16,W//16,16).mean(axis=(1,3))>127
water16[3136//16:3184//16,2336//16:2432//16]=False
active={}
for y in range(H//16+1):
 row=water16[y]if y<H//16 else np.zeros(W//16,dtype=bool);runs=[];x=0
 while x<W//16:
  if not row[x]:x+=1;continue
  a=x
  while x<W//16 and row[x]:x+=1
  runs.append((a,x))
 nxt={v:active.get(v,y)for v in runs}
 for (a,b),sy in active.items():
  if(a,b)not in nxt:addsolid(a*16,sy*16,(b-a)*16,(y-sy)*16,'Visible sea/inlet water,16pxboundary; bridge deck excluded')
 active=nxt

# Generated low forest texture replaces empty exterior grass. No arbitrary grid of tall trees.
for y in range(ROWS):
 for x in range(COLS):
  if not walk[y,x]and not wa[y*32:y*32+32,x*32:x*32+32].any()and not np.array(island.crop((x*32,y*32,x*32+32,y*32+32))).any():ground[y][x]=reg(swatch_tile('forest',x,y));edge[y][x]=-1
woodlands=[(384,320),(576,640),(320,992),(544,1280),(352,1600),(640,1900),(384,2176),(224,3648),(416,3968),(224,4320),(448,4592),(3712,288),(4032,608),(3776,928),(4096,1248),(3776,1600),(4032,1920),(4000,3712),(3712,4000),(4096,4288),(3808,4608),(896,3840),(1152,4224),(896,4512),(3392,3744),(3584,4160),(3344,4544)]
for i,(cx,cy)in enumerate(woodlands):
 for j,(dx,dy)in enumerate([(0,0),(-104,96),(96,32),(24,176)]):
  x,y=cx+dx,cy+dy
  if x<160 or x>W-160 or y<256 or y>H-64:continue
  if walk[y//32,x//32]or water_cells[y//32,x//32]:continue
  key=['kr-pine','rf-prod-tree','rf-prod-tree','rf-prod-ginkgo'][(i+j)%4]
  place(key,x,y,'Authored clustered woodland mass beyond travel-zone boundary')
write(S/'shoreline.json',{'coastline':coastline,'islandOutline':island_points,'waterIsBlocked':True,'bridgeDeck':[2336,3136,96,64],'ferryExplicit':True,'forestClusters':woodlands,'terrainArtSource':'original host image6, actual Forge terrain extraction + palette; mask geometry only'})

# Reciprocal explicit ferry and retained Academy room, with arrivals outside all triggers.
B['portals']=[{'id':'academy','circle':[1568,1120,24],'to':'full-reading-room:start','entranceByFrom':{'full-reading-room':[1568,1152]},'reciprocal':True,'activation':'intent','radius':96,'travelDirection':[0,1]}, {'id':'ferry-jeju','circle':[2848,3184,28],'to':'full-korea:jeju-arrival','reciprocal':False,'activation':'intent','radius':96,'travelDirection':[0,1]},{'id':'ferry-coast','circle':[1760,4608,28],'to':'full-korea:coast-arrival','reciprocal':False,'activation':'intent','radius':96,'travelDirection':[0,1]}]
B['portals'][0]['travelDirection']=[0,-1]
# Final compact metadata/source exports.
write(S/'routes.json',routes);write(S/'world-layout.json',{'approvedPlanSha256':sha(R/'docs/living-korea/southern-masterplan.json'),'world':[W,H],'offsets':OFF,'fictionalGeography':True,'localLayoutsPreserved':['heritage','namsan'],'walkRects':'original zones + signed commons; excluded frame physically blocked','ferry':'same outdoor scene, explicit reciprocal public travel, not walking over sea'})
# Atlas64columns caps GPU texture dimensions despite many reusable blended source cells.
atlas=Image.new('RGBA',(2048,math.ceil(len(unique)/64)*32))
for i,im in enumerate(unique):atlas.paste(im,((i%64)*32,(i//64)*32))
atlas.save(P/'tiles.png');write(P/'tileset.json',{'schema':'generate2dmap.tileset.v1','image':'tiles.png','sha256':sha(P/'tiles.png'),'tile_size':[32,32],'columns':64,'kind':'flat','materials':['grass','earth','stone','water'],'tiles':[{'index':i,'properties':{'walkable':True}}for i in range(len(unique))],'art_source':'existing','seamless_verified':False});write(P/'layers/ground.json',ground);write(P/'layers/edging.json',edge);write(P/'outdoor-draft.json',B);write(S/'water.json',{'tileIndices':waters,'region':[0,3200,W,1600],'inlet':[2336,3056,96,176]})
print(json.dumps({'objects':len(B['objects']),'colliders':len(B['collision']['solids']),'atlas':list(atlas.size),'uniqueTiles':len(unique),'world':[W,H]}))
