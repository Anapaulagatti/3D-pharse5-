"""V7 clean semantic terrain/site reconstruction from approved original PNGs.
No V6 southern terrain imported; original host-image materials, no tracing or architecture rescaling.
"""
from v7_art import *
from PIL import ImageDraw,ImageFilter,ImageChops
import numpy as np,copy,math,re
P=S/'map';W,H=4352,5312;OLD=R/'assets-src/v6-restructure/map'
b=copy.deepcopy(json.loads((OLD/'outdoor-bundle.json').read_text()));b['name']='Korean Arena — V7 Living Korea World Reconstruction'
for p in b['props'].values():p['image']=os.path.relpath((OLD/p['image']).resolve(),P)
oldobjects=copy.deepcopy(b['objects']);oldby={o['id']:o for o in oldobjects};oldsolids=copy.deepcopy(b['collision']['solids'])
def blank():return Image.new('L',(W,H))
def box(q,r=0):
 m=blank();ImageDraw.Draw(m).rounded_rectangle(tuple(q),radius=r,fill=255);return m
def union(*ms):
 a=blank()
 for m in ms:a=ImageChops.lighter(a,m)
 return a
def smooth(points,closed=False):
 p=[tuple(q)for q in points];q=([p[-1]]+p+[p[0],p[1]])if closed else([p[0]]+p+[p[-1]])
 out=[]
 for i in range(1,len(q)-2):
  a,c,d,e=q[i-1:i+3];steps=max(8,math.ceil(math.dist(c,d)/5))
  for k in range(steps):
   t=k/steps;t2=t*t;t3=t2*t
   out.append([round(.5*((2*c[j])+(-a[j]+d[j])*t+(2*a[j]-5*c[j]+4*d[j]-e[j])*t2+(-a[j]+3*c[j]-3*d[j]+e[j])*t3))for j in [0,1]])
 out.append(list(p[0]if closed else p[-1]));return out
def stroke(points,width):
 m=blank();d=ImageDraw.Draw(m);d.line([tuple(p)for p in points],fill=255,width=width,joint='curve')
 rad=width//2
 for x,y in [points[0],points[-1]]:d.ellipse((x-rad,y-rad,x+rad-1,y+rad-1),fill=255)
 return m
textures={}
material_paths={'grass':'assets-src/v7-world/source/extracted/grass-1.png','meadow':'assets-src/v7-world/source/extracted/meadow-1.png','heritage-grass':'assets-src/v3-final/terrain/grass.png','forest':'assets-src/gwanghwamun/terrain/grass-2.png','earth':'assets-src/v7-world/source/extracted/earth-1.png','warm-stone':'assets-src/gwanghwamun/terrain/granite-1.png','civic':'assets-src/v7-world/source/extracted/civic-1.png','festival':'assets-src/v7-world/source/extracted/festival-1.png','stone':'assets-src/v3-final/terrain/paver.png','sand':'assets-src/v3-final/terrain/sand.png','basalt':'assets-src/v3-final/terrain/basalt.png','water':'assets-src/v3-final/terrain/deep-water.png','shallows':'assets-src/v3-final/terrain/shallow-water.png'}
def texture(name):
 if name not in textures:
  im=Image.open(R/material_paths[name]).convert('RGB');a=np.array(im);textures[name]=Image.fromarray(a[np.arange(H)[:,None]%a.shape[0],np.arange(W)[None,:]%a.shape[1]])
 return textures[name]
land=blank();d=ImageDraw.Draw(land)
# New modest engineered quay and actual drainage inlet beneath the usable bridge.
d.polygon([(0,0),(4351,0),(4351,3616),(4256,3704),(4048,3784),(3616,3792),(3232,3784),(2992,3776),(2880,3808),(2688,3792),(2432,3776),(2176,3792),(1824,3808),(1376,3776),(1056,3808),(736,3760),(448,3712),(128,3680),(0,3584)],fill=255)
d.rectangle((2784,3576,2848,3872),fill=0)
island=blank();d=ImageDraw.Draw(island);outline=smooth([(1552,4608),(1648,4416),(1888,4240),(2176,4160),(2496,4184),(2752,4272),(3024,4416),(3168,4640),(3104,4904),(2872,5088),(2496,5168),(2080,5144),(1784,5056),(1568,4880)],True);d.polygon([tuple(p)for p in outline],fill=255);land=union(land,island)
# Literal approved north: the only editable historical exception is the southern handoff.
land.paste(Image.open(OLD/'land-mask.png').crop((0,0,W,2240)),(0,0))
base=texture('water').copy();small=land.resize((W//4,H//4),Image.Resampling.NEAREST);outer=small.filter(ImageFilter.MaxFilter(7)).resize((W,H),Image.Resampling.NEAREST);shallow=small.filter(ImageFilter.MaxFilter(15)).resize((W,H),Image.Resampling.NEAREST);base.paste(texture('shallows'),(0,0),shallow);base.paste(texture('sand'),(0,0),outer);base.paste(texture('grass'),(0,0),land)
base.paste(Image.open(OLD/'ground-native.png').crop((0,0,W,2240)).convert('RGB'),(0,0))
# Strip only the old southern handoff's road pixels. The prior repair mask is
# an erasure diagnostic, never a V7 road layout or imported southern ground.
transition_erase=blank()
prior=Image.open(R/'assets-src/v6-path-fix/edit-mask.png').convert('L')
transition_erase.paste(prior.crop((0,1920,W,2240)),(0,1920))
base.paste(texture('heritage-grass'),(0,0),transition_erase)
# Native source-pixel material boundary follows landscape pockets, not a straight
# screenshot-wide color filter. Historical pixels above2240 stay literal outside
# the explicitly erased southern handoff.
band=blank();edge=smooth([(0,2448),(512,2344),(1024,2480),(1664,2328),(2240,2400),(2944,2352),(3520,2456),(4351,2360)])
ImageDraw.Draw(band).polygon([(0,2240),(4351,2240)]+[tuple(p)for p in reversed(edge)],fill=255)
base.paste(texture('heritage-grass'),(0,0),ImageChops.multiply(band,land))
walk=land.copy();layers={};routes=[];courts=[]
def fill(mask,mat,clip=True):
 mask=ImageChops.multiply(mask,land)if clip else mask
 base.paste(texture(mat),(0,0),mask)
 layers[mat]=union(layers.get(mat,blank()),mask)
 return mask
def route(key,points,width,mat,clear=32,curve=True,closed=False):
 dense=smooth(points,closed)if curve else points
 mask=stroke(dense,width);fill(mask,mat)
 routes.append({'id':key,'points':dense,'controlPoints':points,'width':width,'clearWidth':clear,'material':mat,'curve':curve,'closed':closed})
 return mask
def court(key,q,mat='stone',radius=24):
 mask=box(q,radius);fill(mask,mat);courts.append({'id':key,'box':q,'material':mat,'radius':radius});return mask
# The threshold is warm masonry; the station is approached at its actual SOUTH facade.
route('historic-threshold',[(2176,1984),(2176,2152),(2224,2288),(2224,2400)],112,'warm-stone',48)
route('academy-threshold',[(1952,1984),(2048,2072),(2176,2152)],96,'warm-stone',32)
route('museum-threshold',[(2640,2000),(2560,2080),(2392,2192),(2224,2288)],96,'warm-stone',32)
court('welcome-threshold',(2080,2320,2368,2448),'warm-stone',28)
route('west-station-arrival',[(2224,2400),(2048,2448),(1920,2560),(1920,2928)],112,'civic',48)
route('east-station-arrival',[(2224,2400),(2424,2456),(2560,2592),(2560,2928)],112,'civic',48)
route('bookshop-frontage',[(1664,2536),(1808,2536),(1920,2600)],88,'warm-stone',32)
court('bookshop-plot',(1520,2480,1840,2592),'warm-stone',20)
route('shelter-frontage',[(2560,2592),(2688,2552),(2768,2536)],80,'warm-stone',32)
court('shelter-plot',(2656,2480,2880,2592),'warm-stone',20)
# Broad but bounded station court with two garden wings, not a carpet of paving.
court('station-civic-court',(1984,2832,2496,3064),'civic',28)
route('station-frontage',[(1456,2928),(1920,2928),(2240,2928),(2560,2928),(3152,2928)],112,'civic',64,False)
route('west-boulevard',[(1456,2928),(1456,3712)],112,'stone',48,False)
route('east-boulevard',[(3152,2928),(3152,3712)],112,'stone',48,False)
court('library-plot',(1456,2808,1872,2968),'warm-stone',20)
court('cafe-plot',(2656,2808,3072,2968),'warm-stone',20)
route('rail-and-platform-stair',[(2240,2928),(2240,3264),(2240,3376)],96,'civic',40,False)
route('lower-public-square',[(1456,3376),(1920,3376),(2240,3376),(2688,3376),(3152,3376)],104,'civic',48,False)
court('transit-gathering',(1992,3264,2488,3432),'warm-stone',30)
route('terminal-west-arrival',[(2240,3376),(2000,3440),(2000,3656),(2240,3712)],96,'civic',40)
route('terminal-east-arrival',[(2240,3376),(2496,3440),(2496,3656),(2240,3712)],96,'civic',40)
court('terminal-waiting',(2032,3616,2448,3736),'stone',24)
route('coastal-promenade-west',[(704,3712),(1456,3712),(2240,3712),(2784,3712)],96,'warm-stone',48,False)
route('coastal-promenade-east',[(2848,3712),(3616,3712),(4112,3688)],96,'warm-stone',48)
# Namsan: one readable landscaped loop, secondary woodland discovery and arrivals.
route('namsan-arrival',[(1456,3712),(1264,3712),(1120,3664),(1120,3472)],88,'earth',40)
route('namsan-tower-loop',[(1120,3472),(848,3520),(576,3392),(416,3248),(416,3096),(592,3080),(848,3096),(1040,3112),(1264,3168),(1264,3360)],88,'earth',40,True,True)
court('tower-observation',(472,2984,928,3144),'warm-stone',40)
route('tower-front',[(592,3096),(704,3072),(848,3096)],88,'warm-stone',32)
route('namsan-discovery',[(416,3096),(336,2840),(464,2712),(784,2640),(928,2704),(944,2864),(1136,2872),(1264,3016),(1264,3168)],72,'earth',32)
court('pavilion-arrival',(1008,2816,1264,2928),'warm-stone',24)
court('terrace-arrival',(872,3392,1176,3480),'warm-stone',28)
route('lookout-stairs',[(1120,3472),(1024,3472),(1024,3392)],72,'warm-stone',32)
# Amusement: centred entrance, one independent loop and real attraction frontages.
route('amusement-entry',[(3152,3712),(3440,3712),(3616,3696),(3712,3616),(3712,3456)],112,'warm-stone',48)
route('amusement-loop',[(3352,3200),(3472,3128),(3920,3128),(4168,3200),(4168,3488),(3968,3536),(3712,3456),(3352,3456)],88,'warm-stone',40,True,True)
court('wheel-court',(3232,2992,3600,3136),'stone',36)
court('carousel-court',(3776,2992,4208,3136),'festival',48)
route('wheel-arrival',[(3464,3128),(3464,3024)],88,'stone',32,False)
route('carousel-arrival',[(4000,3128),(4000,3024)],88,'warm-stone',32,False)
court('discovery-hall',(3808,3440,4168,3544),'civic',28)
route('hall-arrival',[(4168,3488),(4072,3504),(3968,3496)],80,'civic',32)
route('kiosk-garden',[(3472,3128),(3712,3072),(3736,2736)],80,'earth',32)
court('kiosk-garden',(3616,2672,3856,2784),'warm-stone',24)
court('coastal-lookout-landside',(3200,3616,3504,3696),'stone',20)
route('coastal-lookout-stairs',[(3344,3712),(3344,3616)],80,'stone',32,False)
# Island roads are rebuilt on CLEAN original grass, never old pasted road rectangles.
route('jeju-arrival',[(2704,4352),(2616,4392),(2560,4520),(2504,4600)],76,'sand',32)
route('jeju-oreum-loop',[(2560,4520),(2312,4528),(2048,4504),(1856,4384),(1960,4296),(2144,4240),(2392,4248),(2552,4368)],76,'sand',32,True,True)
route('jeju-village-route',[(2312,4528),(2144,4560),(2064,4640),(2048,4776),(1944,4800),(1830,4800)],76,'sand',32)
route('jeju-garden-link',[(2504,4600),(2376,4664),(2240,4704),(2160,4800)],76,'sand',32)
route('jeju-scenic-circuit',[(1830,4800),(1864,4904),(1976,5000),(2160,5080),(2432,5072),(2736,5000),(2928,4816),(2880,4720),(2640,4704),(2504,4600)],76,'sand',32)
route('jeju-learning-arrival',[(2160,4800),(2144,4848)],72,'basalt',32,False)
route('jeju-nature-centre',[(2640,4704),(2736,4800),(2616,4896),(2464,4896)],76,'sand',32)
route('jeju-cultural-gateway',[(1864,4904),(1808,4928),(1760,5008)],76,'basalt',32)
route('jeju-viewpoint',[(2896,4792),(2864,4720)],76,'basalt',32)
court('village-threshold',(1712,4752,1952,4824),'basalt',24)
court('oreum-interpretation',(2104,4416,2408,4504),'basalt',32)
court('nature-centre-stair',(2264,4792,2680,4912),'stone',24)
court('viewpoint-front',(2752,4688,2992,4792),'basalt',24)
# Actual supports only: narrow boarding gangways and short stream bridge; open sea is blocked.
decks=union(box((2192,3712,2288,3904)),box((2168,3776,2312,3840)),box((2656,4160,2752,4360)),box((2632,4160,2776,4224)),box((2744,3664,2896,3752)))
for key,points in [('mainland-boarding',[[2240,3712],[2240,3864]]),('island-boarding',[[2704,4240],[2704,4352]]),('coastal-channel-bridge',[[2744,3712],[2896,3712]])]:
 routes.append({'id':key,'points':points,'controlPoints':points,'width':64,'clearWidth':32,'material':'original-timber','curve':False,'closed':False})
walk=union(land,decks)
# The sea-side planted verge beyond the visible quay rail is not a walking
# strip. Match the physical shore to that rail, including its eastern return.
ImageDraw.Draw(walk).rectangle((2928,3752,4351,3840),fill=0)
ImageDraw.Draw(walk).rectangle((4240,3664,4351,3840),fill=0)
# Literal approved opaque wood pixels, not a giant stretched deck sprite.
pier=Image.open(R/'public/review/v6-restructure/world/fw-jetty.png').convert('RGBA').crop((48,36,144,76)).convert('RGB');a=np.array(pier);wood=Image.fromarray(a[np.arange(H)[:,None]%a.shape[0],np.arange(W)[None,:]%a.shape[1]])
base.paste(wood,(0,0),decks)
# Relocate actual native assets and transport all their physical templates.
positions={'v3-232':(3344,3616),'full-185':(1664,2480),'heritage-kr-144-kr-rest':(1664,2384),'v3-177':(1664,2808),'v3-178':(2768,2480),'v3-179':(1728,3504),'v3-180':(704,3008),'v3-181':(1024,3392),'v3-182':(1136,2816),'v3-183':(1264,3504),'v3-191':(3712,3616),'v3-192':(3464,2992),'v3-193':(4000,2992),'v3-194':(3968,3440),'v3-195':(3736,2672),'v3-196':(3344,3256),'v3-197':(4056,3256),'v3-198':(3296,2704),'v3-199':(4192,2720),'v3-200':(3280,3520),'v3-201':(4240,3536),'v3-202':(3440,2704),'v3-203':(3280,3096),'v3-204':(3864,3608),'v3-205':(4232,3112),'v3-206':(3872,2792),'v3-207':(3232,3352),'v3-208':(4184,3616),'v3-209':(3440,3616),'v3-210':(2240,2832),'v3-211':(2240,3104),'v3-212':(2240,3104),'v3-213':(2240,3192),'v3-214':(2240,3216),'v3-215':(2600,3096),'v3-216':(2848,2808),'v3-217':(2240,3616),'v3-218':(2240,3904),'v3-219':(2376,3912),'v3-220':(2816,3736),'v3-221':(1920,3760),'v3-222':(1216,3696),'v3-223':(2608,3696),'v3-224':(1992,2976),'v3-225':(2384,3344),'v3-226':(3008,2976),'v3-227':(3152,3760),'v3-229':(3376,3760),'v3-230':(1200,3808),'v3-231':(4080,3784),'v3-233':(1808,3768),'v3-234':(2016,3768),'v3-235':(3056,3768),'v3-238':(1280,2496),'v3-239':(3232,2496),'v3-240':(1280,3648),'v3-241':(4208,3664),'v3-266':(2584,5096),'v3-265':(1832,4568),'v3-246':(2864,4688),'v6-island-north-pier':(2704,4288)}
landscape={'fw-tangerine','fw-coastal-garden','v3-coastal-rocks','rf-prod-tree','rf-prod-ginkgo','rf-polish-flowers','v3-queue-garden','v3-streetlight-tall','v3-streetlight-short','rf-prod-bench','rf-prod-planter','v3-urban-bench'}
remove=set()|{o['id']for o in oldobjects if o['id'].startswith(('v6-edge-','namsan-park-'))or(o['y']>=2240 and o['prop']in landscape)}
objects=[];moved=[]
for old in oldobjects:
 if old['id']in remove:continue
 o=copy.deepcopy(old)
 if o['id']in positions:o['x'],o['y']=positions[o['id']]
 o['sortY']+=o['y']-old['y'];o['occluder']['source']=b['props'][o['prop']]['image'];objects.append(o)
 if [o['x'],o['y']]!=[old['x'],old['y']]:moved.append({'id':o['id'],'prop':o['prop'],'before':[old['x'],old['y']],'after':[o['x'],o['y']]})
newby={o['id']:o for o in objects}
reason_ids={'brick bookshop':'full-185','glass/concrete book-and':'v3-177','gateway route shelter':'v3-178','Urban hub public rest':'v3-179','broadcasting observation':'v3-180','Modern lookout rear':'v3-181','nature information pavilion':'v3-182','Namsan route marker':'v3-183','Entrance side ticket':'v3-191','observation wheel':'v3-192','petal carousel':'v3-193','creative discovery hall':'v3-194','refreshment kiosk':'v3-195','low glazed coastal station':'v3-210','sightseeing carriage':'v3-215','sea-view cafe':'v3-216','ferry waiting terminal':'v3-217','Coastal deck retaining':'v3-232','Retained cultural trail rest':'heritage-kr-144-kr-rest','Contemporary volcanic':'v3-242','volcanic hill':'v3-242','nature learning':'v3-245','nature centre':'v3-245','cliff lookout':'v3-246','lookout cliff face':'v3-246','basalt discovery':'v3-247'}
solids=[]
for old in oldsolids:
 if old['y']+old['h']<=2240:solids.append(copy.deepcopy(old));continue
 reason=old.get('reason','')
 if 'visible boundary feet'in reason or 'new authored sea/shore'in reason or 'rail safety barrier'in reason or 'platform retaining face'in reason:continue
 matches=[key for phrase,key in reason_ids.items()if phrase.lower()in reason.lower()]
 if matches:key=matches[0]
 else:
  cx=old['x']+old['w']/2;cy=old['y']+old['h'];candidates=[o for o in oldobjects if o['y']>=2240 and not o['id'].startswith('v6-edge-')]
  key=min(candidates,key=lambda o:math.hypot(o['x']-cx,o['y']-cy))['id']
 if key not in newby:continue
 q=copy.deepcopy(old);q['x']+=newby[key]['x']-oldby[key]['x'];q['y']+=newby[key]['y']-oldby[key]['y'];q['reason']='V7 moved native template: '+reason;solids.append(q)
def solid(x,y,w,h,reason):solids.append({'shape':'rect','x':x,'y':y,'w':w,'h':h,'reason':'V7: '+reason})
for x,end in [(1584,2192),(2288,2896)]:solid(x,3044,end-x,48,'rail barrier beside actual timber crossing')
for x,end in [(1584,2176),(2304,2896)]:solid(x,3164,end-x,28,'platform retaining face; central stairs open')
# Purposeful independent campus boundaries. No fence is used to hide paving.
boundaries=[]
def place(kind,x,y,purpose,body=True):
 prop=b['props'][kind];key='v7-site-'+str(len(boundaries)+1);o={'id':key,'prop':kind,'x':x,'y':y,'sortY':y,'scale':1,'anchor_px':prop['anchor_px'],'occlusion':prop.get('occlusion_class','low'),'occluder':{'source':prop['image'],'alphaThreshold':128,'sha256':prop['sha256']},'purpose':purpose};objects.append(o);boundaries.append(o)
 if body:
  fp=prop['footprint'];solid(x-fp['width']/2,y-fp['depth'],fp['width'],fp['depth'],'visible '+key+' '+purpose)
for prefix,x0,x1,y0,y1,gap,rail in [('Namsan',192,1360,2512,3584,1120,'v4-rail'),('Amusement',3264,4256,2528,3664,3712,'v4-park')]:
 for x in range(x0+64,x1-24,136):
  place(rail,x,y0,prefix+' north boundary')
  if abs(x-gap)>176 and not(prefix=='Amusement'and abs(x-3344)<112):place(rail,x,y1,prefix+' perimeter at main entrance')
 for y in range(y0+96,y1-48,80):
  for x in [x0,x1]:place('v4-planter',x,y,prefix+' planted side enclosure')
for x in range(448,4144,136):
 if abs(x-2240)>120 and not 2680<x<2950:place('v4-rail',x,3760,'promenade guardrail; boarding and bridge openings')
# Station gardens and purposeful edge plots, not scattered obstruction.
for x in [1976,2504]:
 for y in [2584,2736]:place('rf-prod-ginkgo',x,y,'station rear garden framing; route gaps protected')
for x in [2032,2448]:place('v4-planter',x,3000,'station forecourt corner planting')
for x in [1584,2960]:place('v4-hedge',x,3320,'lower public square planted boundary')
for x in [1552,1808]:place('v4-hedge',x,2784,'library independent plot')
for x in [2720,2960]:place('v4-hedge',x,2784,'cafe independent plot')
for x,y in [(1896,2520),(2576,2520),(2048,3040),(2432,3040),(2032,3456),(2448,3456),(1488,3496),(3120,3496)]:place('v3-streetlight-short',x,y,'transit and civic wayfinding light')
for x,y in [(960,3584),(3600,3320),(4064,3616),(2352,4464),(1952,4928)]:place('rf-prod-bench',x,y,'off-route scenic resting pocket')
for x,y in [(1600,2680),(2880,2680),(2016,3504),(2464,3504),(3512,3168),(4080,3248),(2064,4560),(2640,4960)]:place('rf-polish-flowers',x,y,'intentional civic/attraction/island garden accent')
# Curated landscape is newly site-planned; old scattered roots/walls do not dictate roads.
for kind,x,y in [('kr-pine',288,2768),('kr-pine',304,3312),('rf-prod-tree',544,2800),('rf-prod-tree',960,3304),('rf-prod-ginkgo',1232,2600),('rf-prod-ginkgo',1248,2880),('rf-prod-tree',576,3272),('rf-prod-tree',880,2624),('rf-prod-ginkgo',3440,2792),('rf-prod-tree',4112,2776),('rf-prod-tree',3744,3320),('fw-flower-bed',3616,3336),('fw-tangerine',1960,4616),('fw-tangerine',2128,4928),('fw-tangerine',2768,4872),('fw-coastal-garden',3008,4640),('fw-coastal-garden',2048,4888)]:
 place(kind,x,y,'designed landscape pocket outside circulation')
b['objects']=objects
# Conservative sea blockers rebuilt from actual walk mask. No imaginary walkable sea.
a=np.array(walk)>0;blocked=~a;blocked[:2240]=False;cell=16;g=blocked.reshape(H//cell,cell,W//cell,cell).any(axis=(1,3));active={};merged=[]
for gy,row in enumerate(g):
 spans=[];start=None
 for gx,v in enumerate(list(row)+[False]):
  if v and start is None:start=gx
  if not v and start is not None:spans.append((start,gx));start=None
 nxt={}
 for span in spans:
  if span in active:q=active.pop(span);q[3]+=cell
  else:q=[span[0]*cell,gy*cell,(span[1]-span[0])*cell,cell]
  nxt[span]=q
 merged+=list(active.values());active=nxt
merged+=list(active.values())
for q in merged:solid(*q,'new coastline/walk-mask water boundary')
b['collision']['solids']=solids
stops=json.loads((R/'assets-src/v6-restructure/stops.json').read_text());stopids={'bookshop':'full-185','urban-hub':'v3-177','tower':'v3-180','terrace':'v3-181','wheel':'v3-192','carousel':'v3-193','creative-hall':'v3-194','park-entry':'v3-191','station':'v3-210','cafe':'v3-216','bridge':'v3-220','coast-viewdeck':'v3-232','oreum':'v3-242','cliff-lookout':'v3-246','lookout':'v3-246'}
for stop in stops:
 if stop['id']in stopids:
  o=newby[stopids[stop['id']]];stop['x'],stop['y']=o['x'],o['y']+56
 if stop['id']=='bridge':stop['x'],stop['y']=2816,3712
 b['anchors'][stop['id']]={'point':[stop['x'],stop['y']],'approach':[stop['x'],stop['y']]}
b['interactions']=[{'id':o['id'],'x':o['x'],'y':o['y'],'reach':104}for o in stops]
for spawn in b['spawns']:
 if spawn['id']=='jeju-arrival':spawn['x'],spawn['y']=2704,4352
 if spawn['id']=='coast-arrival':spawn['x'],spawn['y']=2240,3808
for portal in b['portals']:
 if portal['id']=='ferry-jeju':portal['circle']=[2240,3864,28]
 if portal['id']=='ferry-coast':portal['circle']=[2704,4240,28]
write(S/'stops.json',stops);write(S/'travel.json',{'mainlandTrigger':[2240,3864],'islandTrigger':[2704,4240],'mainlandArrival':[2240,3808],'islandArrival':[2704,4352],'discovery':[2144,4880]})
write(S/'routes.json',routes);write(S/'courts.json',courts);write(S/'relocations.json',{'baseline':'3a559c0fe8d274ea0a7e275719231d188df30f4b','placements':moved,'removedObsoletePlacementIds':sorted(remove),'activeRoadSource':'one clean editable route/court graph; V6 road/polish layers never imported'})
land.save(P/'land-mask.png');walk.save(P/'walk-mask.png');base.save(P/'terrain-composite-unquantized.png');write(P/'outdoor-draft.json',b)
for name,mask in layers.items():mask.save(P/f'{name}-mask.png')
write(S/'material-sources.json',{'art_source':'existing+host_image','textures':material_paths,'resampling':'none at runtime; new source atlas integer512-to128 nearest extraction recorded separately; approved props never resized','roadHistoryImported':False,'referenceTracing':False,'woodSource':'literal approved fw-jetty opaque crop48,36,144,76'})
# Fail at authoring geometry before any expensive export; never weaken actor/body sizes.
fail=[];samples=0
for route in routes:
 for x,y in route['points']:
  samples+=1
  hit=next((q for q in solids if x+8>q['x']and x-8<q['x']+q['w']and y+4>q['y']and y-4<q['y']+q['h']),None)
  if hit:fail.append({'route':route['id'],'point':[x,y],'reason':hit['reason']})
write(C/'initial-route-diagnostics.json',{'samples':samples,'failures':fail});print(json.dumps({'objects':len(objects),'moved':len(moved),'solids':len(solids),'routes':len(routes),'routeFailures':len(fail),'examples':fail[:18]}))
