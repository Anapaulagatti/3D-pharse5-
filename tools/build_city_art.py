"""Stage D: compose original IMAGE pixels on validated V9 semantic masks.
No old southern image/coordinate/terrain input. No code-drawn substitute art.
"""
from city_geometry import *
from PIL import ImageOps,ImageChops
import numpy as np
from scipy.ndimage import distance_transform_edt
import random,shutil
P=SOURCE/'map';A=SOURCE/'art';L=ROOT/'assets-src/library';F=SOURCE/'layers';F.mkdir(exist_ok=True)
for owned_mask in F.glob('*.png'):owned_mask.unlink()
props=json.loads((L/'props.json').read_text());extra={};objects=[];solids=[];reasons=[]
for k in ['new-grocery','new-bakery','new-language','new-gallery']:
 path=(A/'shops-finished'/(k+'.png')).resolve();extra[k]={'image':str(path.relative_to(ROOT)),'sha256':sha(path),'anchor_px':[128,222],'size':[256,224],'footprint':{'shape':'rect','width':208,'depth':48,'offset':[0,-24],'basis':'world_px'},'solid':False,'occlusion_class':'tall','status':'accepted','art_source':'host_image','colliders':[{'x':-104,'y':-48,'w':208,'h':48}]}
for k in ['campus-fence','park-fence']:
 path=A/'fences-finished'/(k+'.png');extra[k]={'image':str(path.relative_to(ROOT)),'sha256':sha(path),'anchor_px':[72,46],'size':[144,48],'footprint':{'shape':'rect','width':140,'depth':8,'offset':[0,-4],'basis':'world_px'},'solid':False,'occlusion_class':'low','status':'accepted','art_source':'host_image','colliders':[{'x':-70,'y':-8,'w':140,'h':8}]}
props.update(extra)
# Source texture sampling only. Natural cells are mirrored into seamless128px repeats.
# Every RGB remains a generated material pixel; no saturation, blur or painted overlay.
materials={}
for k in json.loads((A/'materials-index.json').read_text())['names']:
 source=A/'materials-extracted'/(k+'-1.png');revised=A/'water-revised'/(k+'-1.png');source=revised if revised.exists()else source;im=Image.open(source).convert('RGBA')
 if k in ['park-grass','forest-grass','mulch','park-trail','basalt','jeju-trail','jeju-grass','rail-gravel','sea','shallows']:
  t=Image.new('RGBA',(128,128));t.paste(im,(0,0));t.paste(ImageOps.mirror(im),(64,0));t.paste(ImageOps.flip(im),(0,64));t.paste(ImageOps.flip(ImageOps.mirror(im)),(64,64));im=t
 materials[k]=im

def texture(k):
 im=materials[k];row=Image.new('RGBA',(W,im.height))
 for x in range(0,W,im.width):row.paste(im,(x,0))
 out=Image.new('RGBA',(W,H))
 for y in range(0,H,im.height):out.paste(row,(0,y))
 return out
planes={}
def paint(k,mask,name=None):
 if k not in planes:planes[k]=texture(k)
 ground.paste(planes[k],(0,0),mask)
 if name:mask.save(F/(name+'.png'))
def shape_mask(rect=None,poly=None,ellipse=None):
 im=Image.new('L',(W,H));d=ImageDraw.Draw(im)
 if rect:d.rectangle(rect,fill=255)
 if poly:d.polygon([tuple(p)for p in poly],fill=255)
 if ellipse:d.ellipse(ellipse,fill=255)
 return im
land=land_mask();land.save(P/'walk-mask.png');soil=shape_mask(poly=PLAN['mainland']);soil=ImageChops.lighter(soil,shape_mask(poly=PLAN['island']));ImageDraw.Draw(soil).rectangle((0,0,W,2239),fill=255);ground=texture('sea');small=np.array(soil.resize((W//4,H//4),Image.Resampling.NEAREST))>0;distance=distance_transform_edt(~small)
for cutoff,k in [(16,'shallows'),(4,'coastal-stone')]:
 edge=Image.fromarray(np.uint8((distance<=cutoff)&(~small))*255).resize((W,H),Image.Resampling.NEAREST);paint(k,edge,'shore-'+k)
paint('park-grass',soil,'land');paint('jeju-grass',shape_mask(poly=PLAN['island']),'jeju-land')
# Landscaped masses/beds are explicit planned zones rather than random vacant lawn.
for i,poly in enumerate([[[0,2240],[704,2240],[896,2800],[448,3376],[320,3984],[0,4032]],[[768,2240],[1072,2240],[1072,2528],[928,2768],[736,2768]],[[2816,2240],[4352,2240],[4352,3312],[4160,3304],[4096,2864],[3776,2720],[3152,2768]],[[2944,3408],[3408,3392],[3504,3648],[2800,3656]],[[288,3840],[608,3840],[768,4232],[352,4224]]]):paint('forest-grass',shape_mask(poly=poly),'forest-bed-'+str(i))
# Planted campus side boundaries; west gateway aligns with its new public connector.
for box in [[2800,3504,2864,4200],[2800,4280,2864,4544],[4160,3504,4224,4544]]:paint('forest-grass',shape_mask(rect=box))
# Public civic square contains a planted central island, not a vacant giant gray sheet.
paint('coastal-stone',shape_mask(poly=[[2048,2784],[2288,2784],[2448,2936],[2288,3104],[2048,3104],[1888,2936]]),'civic-square')
paint('mulch',shape_mask(ellipse=[2072,2872,2280,2992]),'meeting-garden')
# Plots get frontage courts and small back/side planting margins, not isolated paving patches.
courts=Image.new('L',(W,H))
for p in PLAN['plots']:
 x,y=p['site'];l,t,r,b=p['bounds'];kind='leisure-paving'if p['id']in['wheel','carousel','visitor','discovery-hall','campus-entry']else'basalt'if p['id']in['village','nature-center','basalt-learning']else'park-trail'if p['id']in['tower','garden-pavilion','oreum','cliff-lookout']else'concrete'
 half=276 if p['id']=='station' else 152 if p['id']in['cafe','ferry-terminal']else 128
 frontage=shape_mask(rect=[max(l,x-half),y-12,min(r,x+half),p['entrance'][1]+24])
 if p['id']in['village','nature-center','basalt-learning']:
  frontage=shape_mask(poly=[[x-112,y-8],[x+112,y-8],[x+128,y+40],[x+96,p['entrance'][1]+24],[x-96,p['entrance'][1]+24],[x-128,y+40]]);kind='coastal-stone'
 paint(kind,frontage,'court-'+p['id']);courts=ImageChops.lighter(courts,frontage)
 # Back edges are planted with actual props; no disconnected mulch bars.
# Public surfaces union first: curbs never draw circles or closed seams at joins.
allroads=[r for r in PLAN['roads']if r['kind']!='timber'];public=ImageChops.lighter(route_mask(allroads),courts);public=ImageChops.lighter(public,shape_mask(poly=[[2048,2784],[2288,2784],[2448,2936],[2288,3104],[2048,3104],[1888,2936]]))
for r in allroads:
 scenic=r['kind']in['scenic','island'];outer='basalt'if r['kind']=='island'else'forest-grass'if scenic else'civic-inset'
 paint(outer,ImageChops.subtract(route_mask([r],12),public))
 if not scenic:paint('coastal-stone',ImageChops.subtract(route_mask([r],6),public))
for kind in ['local','secondary','primary','civic','leisure','coastal','scenic','island']:
 group=[r for r in allroads if r['kind']==kind]
 if not group:continue
 material={'scenic':'park-trail','island':'jeju-trail','leisure':'leisure-paving','coastal':'coastal-stone','primary':'city-herringbone','civic':'city-stone','local':'concrete','secondary':'city-stone'}[kind]
 paint(material,route_mask(group),'routes-'+kind)
# New rail ground and one perpendicular safe crossing.
paint('rail-gravel',shape_mask(rect=[704,3504,2048,3616]),'rail-corridor');paint('concrete',shape_mask(rect=[720,3616,2032,3688]),'station-platform');paint('city-stone',shape_mask(rect=[1904,3512,1968,3728]),'designated-crossing')
# Structured boarding connector, narrow wood artwork deck, no bridge.
paint('coastal-stone',ImageChops.darker(soil,shape_mask(rect=[2512,4696,2608,4800])),'boarding-neck');paint('basalt',shape_mask(rect=[2016,5376,2112,5504]),'island-arrival-plaza')
# New site placements use native approved illustrations ONLY AFTER graybox verification.
def add(k,x,y,why,body=True,sort=None):
 p=props[k];o=object_at(k,x,y,why,props,'v9-'+str(len(objects)+1));o['sortY']=y if sort is None else sort;objects.append(o)
 if body:
  for c in p.get('colliders',[]):solids.append(dict(shape='rect',x=x+c['x'],y=y+c['y'],w=c['w'],h=c['h'],reason='V9 '+why))
 return o
for p in PLAN['plots']:
 add(p['asset'],*p['site'],p['function'],False)
 for x,y,w,h in p['bodyRects']:solids.append(dict(shape='rect',x=x,y=y,w=w,h=h,reason='V9 verified site body: '+p['id']))
solids.append(dict(shape='rect',x=2088,y=2880,w=176,h=96,reason='Civic planted meeting garden, ring stays open'))
add('fw-rail-run',1376,3584,'One aligned original railway source strip',False,3500);add('fw-platform-run',1376,3672,'Single original raised platform behind station',False,3552);add('v3-train',1136,3576,'Train aligned with dedicated rail corridor');add('v3-platform-stairs',1936,3696,'Accessible marked crossing and platform approach',False);add('fw-crossing',1936,3620,'Single perpendicular designated rail crossing',False,3698)
# Rail blocking follows new coordinates; physical train body is additional, never a road.
solids.extend([{'shape':'rect','x':720,'y':3560,'w':1184,'h':48,'reason':'New railway west of designated crossing'},{'shape':'rect','x':1968,'y':3560,'w':64,'h':48,'reason':'New railway east of designated crossing'}])
add('fw-jetty',2560,4928,'Mainland single timber landing beside ferry',False);add('fw-ferry',2712,4920,'Mainland ferry physically alongside east boarding edge',False);add('kr-pier',2560,4776,'Narrow terminal-to-jetty wooden approach',False)
add('fw-jetty',2064,5408,'Jeju arrival landing with stairs toward island',False);add('fw-ferry',2280,5344,'Island ferry alongside landing, no decorative bridge',False)
# Purposeful public amenities, placed outside every through-route.
for x,y in [(2032,3096),(2336,3096),(1440,4024),(1712,4024),(2376,4712),(2936,4704),(3456,4720)]:add('rf-prod-bench',x,y,'Public rest seating facing nearby square or promenade',False)
for x,y in [(2048,3024),(2304,3024),(1224,2832),(1704,2832),(2592,2832),(1296,3344),(1592,3344)]:add('v4-planter',x,y,'Frontage planting keeps walking center free',False)
for x,y in [(2496,3120),(2800,3120)]:add('rf-cafe-seating',x,y,'Cafe side terrace, not the main route',False)
for x,y in [(2176,2896)]:add('rf-prod-ginkgo',x,y,'Signature civic meeting-garden ginkgo',False)
for x,y in [(3232,3024),(3776,3064),(3680,3424),(3136,3376)]:add('rf-prod-bench',x,y,'Namsan shade/rest pocket beside scenic trail',False)
for x,y in [(3104,2872),(4048,3072),(3296,3440)]:add('v3-rock-garden',x,y,'Namsan planted slope rock garden',False)
for x,y in [(1552,3704),(2064,3920),(2640,4080),(2872,3280),(4072,3464),(2640,4720),(2016,5512)]:add('v4-sign',x,y,'Human-scale wayfinding at an actual destination junction',False)
for x,y in [(1864,2776),(2376,2824),(2576,3440),(2472,3760),(2576,4000),(2472,4416),(2992,3984),(3496,3976),(4032,4296),(2960,4584),(3584,4592)]:add('v3-streetlight-short',x,y,'Coordinated urban/campus/public-edge lighting',False)
# Campus: distinct floral boundary + coordinated fence on horizontal edges, gated open access.
for x in range(2928,4176,144):
 if abs(x-4080)>96:add('campus-fence',x,3504,'Entertainment north perimeter with signed visitor gate',True)
for x in range(2928,4176,144):
 if abs(x-3216)>240 and abs(x-4032)>128:add('campus-fence',x,4560,'Entertainment south boundary, wide main gateway preserved',True)
for y in range(3600,4480,144):
 for x in [2840,4184]:add('v4-planter',x,y,'Campus side boundary: planted edge, no rotated facade',False)
for box in [[2824,3504,16,696],[2824,4280,16,264],[4200,3504,16,1040]]:solids.append(dict(shape='rect',x=box[0],y=box[1],w=box[2],h=box[3],reason='Planted campus side boundary, purposeful west gate remains open'))
# Park low boundary gives it a destination footprint; openings correspond to semantic routes.
for x in range(2960,4256,144):add('park-fence',x,2320,'Namsan northern overlook boundary',True)
for x in range(3008,4112,144):
 if abs(x-3872)>128:add('v4-hedge',x,3456,'Namsan planted southern threshold with gate opening',False)
add('rf-prod-bench',4104,4576,'Eastern promenade viewpoint and campus access rest',False)
add('fw-coastal-garden',4080,4504,'Eastern waterfront gateway planting, outside through-route',False)
# Waterfront rails follow landward promenade edge. No rail across ferry approach.
coast=next(r for r in PLAN['roads']if r['id']=='coastal-promenade');coastpoints=curve(coast['points'],True,96)
last=None
for x,y in coastpoints:
 if last is not None and math.dist(last,[x,y])<158:continue
 if abs(x-2560)<160:continue
 add('v3-glass-rail',x,y+68,'Seaward promenade safety rail interrupted only at boarding',False);last=[x,y]
# Botanical and volcanic planting is arranged in named beds/masses, with route/site clearance.
routeclear=np.array(route_mask(PLAN['roads'],96));native_land=np.array(land);rng=random.Random(9021)
def clear(x,y,margin=28):
 if not(0<=x<W and 2464<=y<H):return False
 if native_land[y,x]<128 or routeclear[y,x]>0:return False
 for p in PLAN['plots']:
  l,t,r,b=p['artBounds']
  if l-margin<x<r+margin and t-margin<y<b+margin:return False
 return True
plantings=[]
# Fixed lattice jitter inside specific landscape beds = repeatable horticultural groups, not route-plugging scatter.
for name,box,step,kinds in [('west-forest',[96,2416,976,4080],152,['rf-prod-tree','rf-prod-ginkgo','kr-pine']),('namsan-canopy',[2928,2440,4240,3416],168,['rf-prod-tree','rf-prod-ginkgo']),('campus-gardens',[2856,3552,4160,4488],184,['rf-prod-ginkgo','rf-prod-tree']),('jeju-orchards',[608,5120,2144,5960],176,['fw-tangerine','rf-prod-tree'])]:
 for y in range(box[1],box[3],step):
  for x in range(box[0],box[2],step):
   xx=x+rng.randint(-24,24);yy=y+rng.randint(-20,20)
   if clear(xx,yy,40):
    kind=kinds[rng.randrange(len(kinds))];add(kind,xx,yy,name+' planted canopy/orchard bed',False);plantings.append({'bed':name,'kind':kind,'point':[xx,yy]})
# Ordered street planting bays; strong frontage instead of buildings floating in grass.
for x,y in [(1088,2448),(1424,2448),(1816,2384),(2320,2400),(2736,2448),(1104,2928),(1712,2952),(2240,3536),(2400,3600),(1744,3800),(1760,4112),(2048,4240),(2800,4352),(4160,4176)]:
 if clear(x,y,28):add('rf-prod-ginkgo',x,y,'Street tree within an explicit planted property edge',False)
for x,y in [(2992,3600),(3456,3704),(4048,4160),(3456,4448)]:add('fw-flower-bed',x,y,'Campus color-coordinated floral court edge',False)
for x,y in [(1136,5904),(1496,5840)]:add('fw-guardian',x,y,'Jeju cultural courtyard guardian',True)
for x,y in [(1008,5712),(1664,5784),(1760,5544)]:add('fw-basalt-wall',x,y,'Jeju basalt garden boundary, clear of loop',False)
# Planted gallery court in the vacated northwest pocket, not an empty building plot.
for x,y in [(1512,3240),(1648,3240)]:add('rf-prod-bench',x,y,'Neighborhood pocket court seating beside bakery frontage',False)
add('fw-flower-bed',1584,3152,'Neighborhood pocket garden replacing relocated gallery plot',False)
# Preserve native historical RGB/geometry exactly after new southern material composition.
ground.paste(Image.open(ROOT/'assets-src/protected-north/ground-native.png'),(0,0));ground.save(P/'ground-native.png')
solids+=water_solids(land);b=bundle(objects,solids);b['art_source']='host_image';write(P/'draft.json',b);write(P/'extra-props.json',extra);write(SOURCE/'planting.json',plantings);write(SOURCE/'material-composition.json',{'source':'16 original host-image swatches','pixels':'Literal nearest-sampled source RGB. Natural-repeat reflections are reversible image transforms, not blurred seam interpolation or palette filters.','maskFolder':'layers','roadHierarchy':'plan/city.json','north':'literal protected image pasted last','southPositions':'New plan after graybox bb8c9e7','props':len(objects),'maskCount':len(list(F.glob('*.png')))})
# Delete only known generated graybox runtime copies now superseded after their pushed checkpoint.
for path in (ROOT/'public/assets/world').glob('gray-*.png'):path.unlink()
print('Final image-art composition:',len(objects),'southern props,',len(solids),'new solids')
