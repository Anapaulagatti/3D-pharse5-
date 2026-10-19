"""Editable V6 reconstruction from original native artwork and authored geometry.

No provider calls, flattened reference painting, resized buildings or new character art.
"""
from v6_restructure_art import *
from PIL import ImageDraw, ImageFilter
import numpy as np, copy, math
P=S/'map'; P.mkdir(exist_ok=True); (P/'layers').mkdir(exist_ok=True)
OLD=R/'assets-src/v4-readability/map'; W,H=4352,5312
old=json.loads((OLD/'outdoor-bundle.json').read_text()); b=copy.deepcopy(old)
b['name']='Korean Arena — V6 Living Korea Reconstructed World'
b['world']['height']=H; b['camera']['bounds']=[0,0,W,H]
b['collision']['walkRegions'][0]['polygon']=[[32,32],[W-32,32],[W-32,H-32],[32,H-32]]
for p in b['props'].values():p['image']=os.path.relpath((OLD/p['image']).resolve(),P)
for t in b['tilesets']:t['manifest']='tileset.json'
for l in b['layers']:
 if l.get('kind')=='tiles':l['data']='layers/'+Path(l['data']).name
for name in ['terrain','palette']:(S/name).mkdir(exist_ok=True)
shutil.copyfile(R/'assets-src/v3-final/palette/palette.json',S/'palette/palette.json')
for name in ['deep-water','shallow-water']:shutil.copyfile(R/f'assets-src/v3-final/terrain/{name}.png',S/f'terrain/{name}.png')
def blank():return Image.new('L',(W,H))
def rect(box,r=0):
 m=blank();ImageDraw.Draw(m).rounded_rectangle(box,radius=r,fill=255);return m
def line(points,width):
 m=blank();d=ImageDraw.Draw(m);d.line(points,fill=255,width=width,joint='curve')
 for x,y in points:d.ellipse((x-width//2,y-width//2,x+width//2-1,y+width//2-1),fill=255)
 return m
def union(*ms):return Image.fromarray(np.maximum.reduce([np.array(m)for m in ms]))
textures={}
def material(name):
 if name not in textures:
  path=R/f'assets-src/modern-streets/terrain/{name}.png'
  if not path.exists():path=R/f'assets-src/v3-final/terrain/{name}.png'
  a=np.array(Image.open(path).convert('RGB'));textures[name]=Image.fromarray(a[(np.arange(H)%a.shape[0])[:,None],(np.arange(W)%a.shape[1])[None,:]])
 return textures[name]
base=material('deep-water').copy()
land=blank(); d=ImageDraw.Draw(land)
# Broad coherent mainland with organic headlands; no old coast/inlet left beneath relocated shops.
coast=[(0,0),(W-1,0),(W-1,3648),(4288,3700),(4096,3800),(3888,3832),(3664,3800),(3376,3776),(3072,3808),(2816,3824),(2528,3792),(2240,3808),(1984,3816),(1728,3800),(1504,3768),(1280,3824),(1024,3856),(768,3800),(512,3776),(256,3744),(0,3648)]
d.polygon(coast,fill=255)
d.rectangle((448,3672,4160,3824),fill=255) # engineered continuous quay under full promenade, not walkable painted water
# Larger natural island, preserving every cultural ensemble position relative to its peers.
island=blank();di=ImageDraw.Draw(island)
di.polygon([(1504,4416),(1568,4272),(1792,4144),(2016,4032),(2240,3968),(2448,4016),(2688,4096),(2944,4224),(3136,4416),(3232,4656),(3168,4928),(2912,5120),(2560,5184),(2112,5160),(1760,5104),(1536,4912),(1440,4656)],fill=255)
island=island.filter(ImageFilter.GaussianBlur(18)).point(lambda v:255 if v>=128 else 0)
land=union(land,island)
# Match prior northern land/walk pixels exactly, rather than repainting the historical district.
land.paste(Image.open(OLD/'land-mask.png').crop((0,0,W,2240)),(0,0))
la=np.array(land)>0
small=land.resize((W//4,H//4),Image.Resampling.NEAREST)
outer=small.filter(ImageFilter.MaxFilter(9)).resize((W,H),Image.Resampling.NEAREST);shallow=small.filter(ImageFilter.MaxFilter(25)).resize((W,H),Image.Resampling.NEAREST)
base.paste(material('shallow-water'),(0,0),shallow)
base.paste(material('sand'),(0,0),outer)
base.paste(material('grass'),(0,0),land)
# Image-generated forest floor and soft terrain transitions, bounded masks only.
forest=union(rect((0,2240,120,3500),48),rect((96,2240,1400,2456),64),rect((4160,2240,W,3500),48))
base.paste(material('forest'),(0,0),forest.filter(ImageFilter.GaussianBlur(14)))
base.paste(Image.open(OLD/'ground-native.png').crop((0,0,W,2240)).convert('RGB'),(0,0))
# Retain Jeju authored ground/paths literally inside its prior land mask, moved +320Y.
oldland=Image.open(OLD/'land-mask.png').crop((0,3648,W,4800))
base.paste(Image.open(OLD/'ground-native.png').crop((0,3648,W,4800)).convert('RGB'),(0,3968),oldland)
walk=land.copy();walk.paste(Image.open(OLD/'walk-mask.png').crop((0,0,W,2240)),(0,0))
def fill(mask,name):
 a=np.array(mask)>0;a[:2240]=False;a&=la
 base.paste(material(name),(0,0),Image.fromarray(np.uint8(a)*255))
routes=[]
def route(key,points,width=80,mat='concrete',clear=48):
 fill(line(points,width),mat);routes.append({'id':key,'zone':'v6','points':points,'clearWidth':clear})
def apron(box,mat='paver',r=22):fill(rect(box,r),mat)
# Formal historical spine into civic plaza. Three separate campuses, real side approaches to station.
route('historical-civic',[(2176,2176),(2176,2560)],144,clear=64)
apron((2032,2424,2336,2664))
route('civic-cross-boulevard',[(1472,2608),(3024,2608)],128,clear=64)
route('west-boulevard',[(1472,2384),(1472,3744)],144,clear=64)
route('east-boulevard',[(3024,2352),(3024,3744)],144,clear=64)
route('station-west-arrival',[(2176,2608),(1856,2608),(1856,3024),(2240,3024)],112,clear=64)
route('station-east-arrival',[(3024,2928),(2768,2928),(2768,3024),(2240,3024)],96,clear=48)
apron((1920,2912,2640,3096))
route('rail-public-crossing',[(2240,3024),(2240,3312)],96,clear=40)
route('retail-forecourt',[(1472,3536),(3024,3536)],112,clear=64)
apron((1576,3456,1984,3584));apron((2456,3456,2848,3584))
route('station-to-coastal-plaza',[(2240,3312),(2240,3504),(2016,3504),(2016,3680),(2240,3680),(2240,3744)],96,clear=48)
apron((2000,3632,2432,3776))
route('coastal-promenade',[(512,3744),(4096,3744)],112,clear=64)
route('public-ferry-approach',[(2240,3744),(2496,3744),(2496,3912)],88,clear=40)
# Purposeful coastal footbridge and deck: below shops, independent from the railway.
route('coastal-bridge',[(2784,3680),(2896,3680),(3024,3680)],72,clear=32)
route('coastal-deck-stair',[(2944,3744),(2944,3912),(2752,3912),(2752,3808)],64,clear=32)
apron((2624,3672,2872,3784),'concrete')
# Winding nature trail stays in west campus; irregular garden paths, not vehicle streets.
route('namsan-arrival',[(1472,3536),(1120,3536),(1120,3296)],88,'sand',48)
route('tower-trail',[(1120,3536),(960,3456),(704,3376),(544,3296),(512,3120),(704,3120),(704,3072)],80,'sand',40)
route('namsan-north-loop',[(704,3120),(960,3136),(1120,3008),(1136,2880),(1264,2880),(1264,2832),(1376,2832),(1376,2552),(864,2640),(512,2688),(352,2848),(384,3072),(512,3120)],72,'sand',32)
route('pavilion-spur',[(1136,2880),(1104,2848)],72,'sand',32)
apron((472,3008,920,3152),'paver',48)
apron((976,3376,1280,3432),'sand')
# Amusement loop and individualized gardens/ride forecourts.
route('park-main-entry',[(3024,3584),(3552,3584),(3552,3424),(3520,3152)],112,'paver',48)
route('park-loop',[(3264,3152),(4192,3152),(4192,3344),(3792,3344),(3792,3584),(3792,3296),(3264,3296),(3264,3152)],80,clear=40)
route('wheel-approach',[(3328,3152),(3328,3104)],80,clear=32)
route('carousel-approach',[(3968,3152),(3968,3072)],80,clear=32)
route('hall-approach',[(3792,3584),(4016,3584)],80,clear=40)
route('park-kiosk-garden',[(3520,3152),(3728,3152),(3728,2640)],88,'paver',40)
apron((3144,3040,3512,3184));apron((3760,3008,4184,3176))
apron((3808,3504,4224,3624));apron((3384,3504,3720,3640))
apron((3616,2576,3840,2688))
# Island arrival from north jetty, heritage garden paths preserved +320, meaningful outer loop.
route('island-north-arrival',[(2496,4192),(2496,4376),(2528,4560)],88,'sand',40)
route('island-garden-link',[(2528,4560),(2528,4640),(2240,4640),(2240,4800),(1830,4800)],80,'sand',40)
route('island-oreum-approach',[(2528,4560),(2528,4464),(2240,4464)],80,'sand',32)
route('island-lookout',[(2528,4464),(2544,4352),(2736,4352)],72,'sand',32)
route('island-nature-centre',[(2528,4640),(2736,4640),(2736,4896),(2464,4896)],80,'sand',40)
route('island-village-south',[(1830,4800),(1830,4896),(1760,4896),(1760,5008)],80,'sand',40)
route('island-outer-garden',[(1760,4896),(2048,4896),(2048,4800),(2048,4560),(2240,4560)],72,'sand',32)
# Jetty walkable geometry is explicit, never makes the open-water crossing walkable.
jetty=union(rect((2464,3744,2528,3936)),rect((2464,4000,2528,4224)),rect((2592,3776,2912,3912)),line([(2944,3744),(2944,3912),(2752,3912)],128))
walk=union(walk,jetty);base.paste(material('paver'),(0,0),jetty)
la=np.array(land)>0
# Keep all native historic placements; curated southern objects are intentionally relocated.
objects=[];relocations=[]
oldby={o['id']:o for o in old['objects']}
def addold(key,x=None,y=None):
 o=copy.deepcopy(oldby[key]);ox,oy=o['x'],o['y'];o['x']=ox if x is None else x;o['y']=oy if y is None else y;o['sortY']+=o['y']-oy
 o['occluder']['source']=b['props'][o['prop']]['image'];objects.append(o)
 if [ox,oy]!=[o['x'],o['y']]:relocations.append({'id':key,'prop':o['prop'],'before':[ox,oy],'after':[o['x'],o['y']]})
 return o
for o in old['objects']:
 if o['y']<2240:addold(o['id'])
positions={'full-185':(1688,2552),'heritage-kr-144-kr-rest':(1664,2400),'v3-177':(1776,3456),'v3-178':(2776,2560),'v3-179':(1728,3616),'v3-180':(704,3008),'v3-181':(1120,3376),'v3-182':(1104,2784),'v3-183':(1264,3488),'v3-184':(352,3200),'v3-185':(784,3488),'v3-186':(1264,3104),'v3-187':(1216,2856),'v3-188':(272,2928),'v3-189':(1280,3264),'v3-190':(608,3432),'v3-191':(3552,3504),'v3-192':(3328,3040),'v3-193':(3968,3008),'v3-194':(4016,3504),'v3-195':(3728,2576),'v3-196':(3360,3240),'v3-197':(4048,3240),'v3-198':(3184,2640),'v3-199':(4208,2640),'v3-200':(3168,3464),'v3-201':(4240,3504),'v3-202':(3456,2600),'v3-203':(3168,3168),'v3-204':(3888,3624),'v3-205':(4208,3136),'v3-206':(3864,2664),'v3-207':(3192,3360),'v3-208':(4184,3616),'v3-209':(3408,3656),'v3-210':(2240,2912),'v3-211':(2240,3152),'v3-212':(2240,3152),'v3-213':(2240,3240),'v3-214':(2240,3264),'v3-215':(2624,3144),'v3-216':(2656,3456),'v3-217':(2240,3632),'v3-218':(2496,3936),'v3-219':(2592,3936),'v3-220':(2896,3752),'v3-221':(1920,3808),'v3-222':(1216,3696),'v3-223':(2640,3664),'v3-224':(1648,2984),'v3-225':(2384,3328),'v3-226':(2864,3472),'v3-227':(3024,3824),'v3-228':(320,3808),'v3-229':(3104,3840),'v3-230':(1200,3864),'v3-231':(4080,3816),'v3-232':(2752,3888),'v3-233':(1808,3824),'v3-234':(2016,3824),'v3-235':(3056,3824),'v3-238':(1280,2504),'v3-239':(3248,2504),'v3-240':(1296,3656),'v3-241':(4208,3704)}
for key,p in positions.items():addold(key,*p)
for o in old['objects']:
 if 3648<=o['y']and not o['id'].startswith('v4-'):addold(o['id'],o['x'],o['y']+320)
# Reuse native nature components, now distributed around trails and buffered campuses.
foliage=[('namsan-park-6',384,2672),('namsan-park-7',288,3344),('namsan-park-8',928,2952),('namsan-park-9',1248,2920),('namsan-park-10',848,3280),('namsan-park-11',192,2528),('namsan-park-12',448,2512),('namsan-park-13',704,2528),('namsan-park-14',1312,2704),('namsan-park-15',1280,2768),('namsan-park-16',208,2840),('namsan-park-17',192,3104),('namsan-park-18',224,3312),('namsan-park-19',448,3512),('namsan-park-20',896,3576),('namsan-park-21',1280,3480),('namsan-park-22',1280,3144),('namsan-park-23',1008,2680),('namsan-park-24',560,2864),('namsan-park-25',192,3520),('namsan-park-26',640,3584),('namsan-park-27',1328,3640),('namsan-park-28',160,2744),('namsan-park-32',504,3032),('namsan-park-33',904,3032),('namsan-park-34',464,3440),('namsan-park-35',1040,3416)]
for key,x,y in foliage:addold(key,x,y)
# Public northern island pier reuses the approved native jetty image, independently editable.
o=copy.deepcopy(oldby['v3-218']);o.update(id='v6-island-north-pier',x=2496,y=4160,sortY=4160);o['occluder']['source']=b['props'][o['prop']]['image'];objects.append(o)
b['objects']=objects
# Native physical templates follow their moved objects, including compound side gaps/stair wings.
# Exclude only moved bookshop, retain genuine historic blockers.
solids=[copy.deepcopy(s)for s in old['collision']['solids']if s['y']+s['h']<=2240 and 'bookshop'not in s.get('reason','').lower()]
reason_ids={'brick bookshop':'full-185','glass/concrete book-and':'v3-177','gateway route shelter':'v3-178','Urban hub public rest':'v3-179','broadcasting observation':'v3-180','Modern lookout rear':'v3-181','nature information pavilion':'v3-182','Namsan route marker':'v3-183','Entrance side ticket':'v3-191','observation wheel':'v3-192','petal carousel':'v3-193','creative discovery hall':'v3-194','refreshment kiosk':'v3-195','low glazed coastal station':'v3-210','sightseeing carriage':'v3-215','sea-view cafe':'v3-216','ferry waiting terminal':'v3-217','Coastal deck retaining':'v3-232','Retained cultural trail rest':'heritage-kr-144-kr-rest'}
newby={o['id']:o for o in objects}
for s in old['collision']['solids']:
 if s['y']+s['h']<=2240:continue
 reason=s.get('reason','')
 if 'boundary matching'in reason or reason.startswith('V4')or 'sliver'in reason or 'Rail north barrier'in reason or 'platform retaining'in reason or 'Inlet water'in reason:continue
 if s['y']>=3648:
  t=copy.deepcopy(s);t['y']+=320;solids.append(t);continue
 matches=[key for phrase,key in reason_ids.items()if phrase in reason]
 if matches:key=matches[0]
 else:
  # Small curated roots/benches/lights use their existing native body; choose original nearest feet.
  cx=s['x']+s['w']/2;cy=s['y']+s['h']
  candidates=[o for o in old['objects']if o['id']in newby and o['y']>=2240]
  near=min(candidates,key=lambda o:math.hypot(o['x']-cx,o['y']-cy))
  if math.hypot(near['x']-cx,near['y']-cy)>48:continue
  key=near['id']
 t=copy.deepcopy(s);t['x']+=newby[key]['x']-oldby[key]['x'];t['y']+=newby[key]['y']-oldby[key]['y'];solids.append(t)
def solid(x,y,w,h,reason):
 q={'shape':'rect','x':x,'y':y,'w':w,'h':h,'reason':'V6: '+reason};solids.append(q);return q
# 96px public crossing,128px platform stair gap at the actual image/stair x2240.
for x,end in [(1584,2192),(2288,2896)]:solid(x,3092,end-x,48,'rail safety barrier either side of real crossing')
for x,end in [(1584,2176),(2304,2896)]:solid(x,3212,end-x,28,'platform retaining face either side of actual stair')
# Purposeful native boundary modules: short horizontals, vertical edges use upright planters.
boundaries=[]
def place(kind,x,y,zone):
 p=b['props'][kind];key='v6-edge-'+str(len(boundaries)+1);o={'id':key,'prop':kind,'x':x,'y':y,'sortY':y,'scale':1,'anchor_px':p['anchor_px'],'occlusion':p.get('occlusion_class','low'),'occluder':{'source':p['image'],'alphaThreshold':128,'sha256':p['sha256']},'purpose':f'V6 {zone} native {kind} boundary; gates remain open'};objects.append(o)
 fp=p['footprint'];q=solid(x-fp['width']/2,y-fp['depth'],fp['width'],fp['depth'],f'{zone} visible boundary feet {key}');boundaries.append({'id':key,'collider':q})
for zone,x0,x1,y0,y1,gap,kind in [('namsan',176,1328,2456,3616,1120,'v4-rail'),('entertainment',3200,4240,2480,3648,3552,'v4-park')]:
 for x in range(x0+64,x1,144):
  place(kind,x,y0,zone)
  if abs(x-gap)>160:place(kind,x,y1,zone)
 for y in range(y0+160,y1-64,160):
  for x in [x0,x1]:place('v4-planter',x,y,zone)
for x in [1632,1728,2608,2880]:
 place('v4-hedge',x,2960,'station forecourt');place('v4-planter',x,3408,'retail garden')
for x in range(400,4050,160):
 if abs(x-2496)>112 and abs(x-2752)>176 and abs(x-2944)>112:place('v4-rail',x,3800,'continuous promenade')
for x,y in [(1792,2664),(2592,2664),(3136,3512),(3808,2768),(1536,3664),(2912,3664)]:place('v4-sign',x,y,'wayfinding')
# Curated planted buffers use the same approved source trees/flowers, outside actual routes.
for kind,x,y in [
 ('rf-prod-ginkgo',1648,2792),('rf-prod-tree',2800,2784),
 ('rf-prod-ginkgo',2656,2768),('rf-prod-tree',2000,2728),
 ('rf-polish-flowers',2016,3080),('rf-polish-flowers',2528,3080),
 ('rf-prod-tree',1600,3280),('rf-prod-ginkgo',2864,3304),
 ('rf-prod-tree',3200,2880),('rf-prod-ginkgo',3504,2824),
 ('rf-prod-tree',3856,2864),('rf-prod-ginkgo',4240,2880),
 ('rf-polish-flowers',3392,3392),('rf-polish-flowers',4072,3392),
 ('fw-tangerine',2992,4720),('fw-tangerine',2912,4976),
 ('fw-coastal-garden',3056,4832),('fw-coastal-garden',1968,5072),
 ('v3-coastal-rocks',3088,4952),('v3-coastal-rocks',1632,5000),
]:place(kind,x,y,'landscape buffer')
# Terrain boundary comes from new walk mask, not old ocean rectangles at obsolete positions.
wa=np.array(walk)>0
blocked=~wa
blocked[:2240]=False
# 32px bands compressed vertically into maximal rectangles; shore is visibly conservative.
cell=32; grid=blocked.reshape(H//cell,cell,W//cell,cell).any(axis=(1,3));active={};merged=[]
for gy,row in enumerate(grid):
 runs=[];start=None
 for gx,v in enumerate(list(row)+[False]):
  if v and start is None:start=gx
  if not v and start is not None:runs.append((start,gx));start=None
 nxt={}
 for span in runs:
  if span in active:q=active.pop(span);q[3]+=cell
  else:q=[span[0]*cell,gy*cell,(span[1]-span[0])*cell,cell]
  nxt[span]=q
 merged+=list(active.values());active=nxt
merged+=list(active.values())
for q in merged:solid(*q,'new authored sea/shore boundary; open water not walkable')
# Close a single4x4unreachable nav cell beneath the visible coastal rock-garden base.
for q in solids:
 if q['x']==4176 and q['y']==3688 and q['w']==64 and q['h']==16:
  q['w']=80;q['h']=24;q['reason']='V6: Coastal rock-garden visible base, seals nonpublic4pxshore sliver'
b['collision']['solids']=solids
# Every relevant stop/label/anchor is moved with its physical landmark and real front approach.
stopcoords={'bookshop':[1688,2608],'urban-hub':[1776,3520],'tower':[704,3072],'terrace':[1120,3296],'wheel':[3328,3104],'carousel':[3968,3072],'creative-hall':[4016,3584],'park-entry':[3552,3576],'station':[2240,2976],'coast-viewdeck':[2752,3808],'cafe':[2656,3520],'bridge':[2896,3680]}
stops=json.loads((R/'assets-src/v3-final/stops.json').read_text())
for s in stops:
 if s['id']in stopcoords:s['x'],s['y']=stopcoords[s['id']]
 elif s['y']>=3648:s['y']+=320
 b['anchors'][s['id']]={'point':[s['x'],s['y']],'approach':[s['x'],s['y']]}
b['interactions']=[{'id':s['id'],'x':s['x'],'y':s['y'],'reach':104}for s in stops]
for spawn in b['spawns']:
 if spawn['id']=='jeju-arrival':spawn['x'],spawn['y']=2496,4280
 if spawn['id']=='coast-arrival':spawn['x'],spawn['y']=2496,3864
for p in b['portals']:
 if p['id']=='ferry-jeju':p['circle']=[2496,3912,28]
 if p['id']=='ferry-coast':p['circle']=[2496,4208,28]
write(S/'stops.json',stops)
write(S/'travel.json',{'mainlandTrigger':[2496,3912],'islandTrigger':[2496,4208],'mainlandArrival':[2496,3864],'islandArrival':[2496,4280],'discovery':[2144,4880]})
land.save(P/'land-mask.png');walk.save(P/'walk-mask.png');forest.save(P/'forest-mask.png');base.save(P/'terrain-composite-unquantized.png')
write(P/'outdoor-draft.json',b);write(S/'relocations.json',{'baseline':'2b5244db06d4cabbaa47196d0f2c78f55d6107ca','worldBefore':[4352,4800],'worldAfter':[W,H],'placements':relocations})
write(S/'boundaries.json',boundaries)
oldroutes=json.loads((R/'assets-src/v3-final/routes.json').read_text())
routes=[r for r in oldroutes if all(p[1]<2240 for p in r['points'])]+routes
write(S/'routes.json',routes)
print(json.dumps({'objects':len(objects),'relocated':len(relocations),'solids':len(solids),'newBoundaryModules':len(boundaries),'routes':len(routes),'world':[W,H]}))
