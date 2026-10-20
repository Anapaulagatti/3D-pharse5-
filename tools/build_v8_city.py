"""V8 semantic city rebuild. Plan first; --graybox is deliberately temporary code-colored geometry.
Final artwork uses original source-image textures/props, never a code-drawn substitute map.
"""
from v8_art import *
from PIL import ImageDraw,ImageFilter,ImageChops
import numpy as np,copy,math
P=S/'map';P.mkdir(parents=True,exist_ok=True);W,H=4352,5312;OLD=R/'assets-src/v7-world/map';plan=json.loads((S/'city-masterplan.json').read_text());gray='--graybox'in sys.argv
b=copy.deepcopy(json.loads((OLD/'outdoor-bundle.json').read_text()));b['name']='Korean Arena — V8 Metropolitan Korea / Review Candidate'
for p in b['props'].values():p['image']=os.path.relpath((OLD/p['image']).resolve(),P)
oldobjects=copy.deepcopy(b['objects']);oldby={o['id']:o for o in oldobjects}
def blank():return Image.new('L',(W,H))
def box(q,r=0):
 m=blank();ImageDraw.Draw(m).rounded_rectangle(tuple(q),radius=r,fill=255);return m
def union(*ms):
 a=blank()
 for m in ms:a=ImageChops.lighter(a,m)
 return a
def smooth(points,closed=False):
 p=[tuple(q)for q in points];q=([p[-1]]+p+[p[0],p[1]])if closed else([p[0]]+p+[p[-1]]);out=[]
 for i in range(1,len(q)-2):
  a,c,d,e=q[i-1:i+3];steps=max(8,math.ceil(math.dist(c,d)/5))
  for k in range(steps):
   t=k/steps;t2=t*t;t3=t2*t
   out.append([round(.5*((2*c[j])+(-a[j]+d[j])*t+(2*a[j]-5*c[j]+4*d[j]-e[j])*t2+(-a[j]+3*c[j]-3*d[j]+e[j])*t3))for j in [0,1]])
 out.append(list(p[0]if closed else p[-1]));return out
def stroke(points,width,caps=True):
 m=blank();d=ImageDraw.Draw(m);d.line([tuple(p)for p in points],fill=255,width=width,joint='curve');rad=width//2
 for x,y in ([points[0],points[-1]]if caps else[]):d.ellipse((x-rad,y-rad,x+rad-1,y+rad-1),fill=255)
 return m
paths=json.loads((R/'assets-src/v7-world/material-sources.json').read_text())['textures'];paths.update({'boulevard':'assets-src/v7-world/source/extracted/civic-1.png','avenue':'assets-src/v7-world/source/extracted/civic-1.png','sidewalk':'assets-src/v3-final/terrain/paver.png','coast':'assets-src/v7-world/source/extracted/civic-1.png','retail':'assets-src/v7-world/source/extracted/civic-1.png'})
# A later, explicitly generated native material kit supersedes ONLY these sources.
kit=S/'source/material-paths.json'
if not gray and kit.exists():paths.update(json.loads(kit.read_text()))
textures={};colors={'grass':'#46664f','meadow':'#75836c','forest':'#304d3a','water':'#284f6c','sand':'#d9bd8b','shallows':'#477e8d','basalt':'#545b60','civic':'#b8c5d0','boulevard':'#8eaec5','avenue':'#93afc1','sidewalk':'#c3d2d4','coast':'#a3cdd7','retail':'#b3c2cc','festival':'#bb97b4','earth':'#b69c7e','warm-stone':'#c5b995'}
def texture(name):
 if name not in textures:
  if gray:textures[name]=Image.new('RGB',(W,H),colors.get(name,'#929b8b'))
  else:
   a=np.array(Image.open(R/paths[name]).convert('RGB'));textures[name]=Image.fromarray(a[np.arange(H)[:,None]%a.shape[0],np.arange(W)[None,:]%a.shape[1]])
 return textures[name]
land=Image.open(OLD/'land-mask.png').convert('L');ImageDraw.Draw(land).rectangle((2784,3576,2848,3792),fill=255) # remove obsolete contradictory inlet/bridge
base=texture('water').copy();small=land.resize((W//4,H//4),Image.Resampling.NEAREST);outer=small.filter(ImageFilter.MaxFilter(7)).resize((W,H),Image.Resampling.NEAREST);shallow=small.filter(ImageFilter.MaxFilter(15)).resize((W,H),Image.Resampling.NEAREST)
for mat,mask in [('shallows',shallow),('sand',outer),('grass',land)]:base.paste(texture(mat),(0,0),mask)
walk=land.copy();layers={};routes=[];courts=[]
def fill(mask,mat):
 mask=ImageChops.multiply(mask,land);base.paste(texture(mat),(0,0),mask);layers[mat]=union(layers.get(mat,blank()),mask)
 return mask
# Grounds establish COMPLETE URBAN BLOCKS before frontage routes, not disconnected pavement patches.
for q in plan['plots']:
 fill(box(q['bounds'],8),q['material']);courts.append({'id':q['id'],'box':q['bounds'],'material':q['material'],'radius':8})
# Independent campus is a landscaped base; its courts are tied by a hierarchy of internal routes.
fill(box((3312,2448,4272,3552),32),'meadow')
for q in plan['plots']:
 if q['material']=='festival':fill(box(q['bounds'],24),'festival')
for rr in plan['roads']:
 r=copy.deepcopy(rr);r['points']=smooth(r['controlPoints'],r['closed'])if r['curve']else r['controlPoints']+([r['controlPoints'][0]]if r['closed']else[]);routes.append(r)
 if r['material']=='original-timber':continue
 # A narrow material edging is sourced from genuine stone pixels, not blurry feathering.
 if not gray:fill(stroke(r['points'],r['width']+12,r['material']in ['earth','sand','basalt','warm-stone']),'basalt'if r['material']in ['sand','basalt']else 'stone')
 fill(stroke(r['points'],r['width'],r['material']in ['earth','sand','basalt','warm-stone']),r['material'])
# Warm north handoff stops at exact immutable historical boundary.
base.paste(Image.open(OLD/'ground-native.png').crop((0,0,W,2240)).convert('RGB'),(0,0))
land.paste(Image.open(OLD/'land-mask.png').crop((0,0,W,2240)),(0,0));walk=land.copy()
decks=union(box((2480,3696,2576,3904)),box((2456,3776,2600,3840)),box((1840,4232,1936,4472)),box((1816,4232,1960,4296)))
a=np.array(Image.open(R/'public/review/v6-restructure/world/fw-jetty.png').convert('RGB').crop((48,36,144,76)));wood=Image.fromarray(a[np.arange(H)[:,None]%a.shape[0],np.arange(W)[None,:]%a.shape[1]])
base.paste(wood,(0,0),decks);walk=union(walk,decks)
# All southern layouts are retired from this active entry; source PNGs and V7 remain recoverable.
keep={'full-185','heritage-kr-144-kr-rest'}|{f'v3-{i}'for i in [177,178,180,181,182,183,191,192,193,194,195,210,211,213,214,215,216,217,218,219,232,242,243,244,245,246,247,248,249,251,264,265,266,267]}|{'v6-island-north-pier'}
positions=plan['positions'];positions['v3-211']=[2736,2456];positions['v3-213']=[2736,2544];positions['v3-217']=[2752,3592]
objects=[];moved=[];removed=[]
for old in oldobjects:
 if old['y']>=2240 and old['id']not in keep:removed.append(old['id']);continue
 o=copy.deepcopy(old)
 if o['id']in positions:o['x'],o['y']=positions[o['id']]
 o['sortY']+=o['y']-old['y'];o['occluder']['source']=b['props'][o['prop']]['image'];objects.append(o)
 if [o['x'],o['y']]!=[old['x'],old['y']]:moved.append({'id':o['id'],'prop':o['prop'],'before':[old['x'],old['y']],'after':[o['x'],o['y']]})
newby={o['id']:o for o in objects}
# Native 1024px rail/platform segments cropped from preserved 1312px original strips.
# No resampling: shortened terminal siding fits dedicated transit plot east of boulevard.
for key,kind in [('v3-211','fw-rail-run'),('v3-213','fw-platform-run')]:
 prop=copy.deepcopy(b['props'][kind]);src=Image.open(P/prop['image']);dest=S/'source'/f'{kind}-native-section.png';dest.parent.mkdir(parents=True,exist_ok=True);src.crop((144,0,1168,src.height)).save(dest)
 prop['image']=os.path.relpath(dest,P);prop['anchor_px']=[512,prop['anchor_px'][1]];prop['size']=[1024,src.height];prop['sha256']=sha(dest)
 b['props']['v8-'+kind]=prop;o=newby[key];o['prop']='v8-'+kind;o['anchor_px']=prop['anchor_px'];o['occluder']['source']=prop['image'];o['occluder']['sha256']=sha(dest)
# Relocate actual building collision templates; no old roads/walls/sea masks freeze the new plan.
reasons={'brick bookshop':'full-185','glass/concrete book-and':'v3-177','gateway route shelter':'v3-178','broadcasting observation':'v3-180','Modern lookout rear':'v3-181','nature information pavilion':'v3-182','Namsan route marker':'v3-183','Entrance side ticket':'v3-191','observation wheel':'v3-192','petal carousel':'v3-193','creative discovery hall':'v3-194','refreshment kiosk':'v3-195','low glazed coastal station':'v3-210','sightseeing carriage':'v3-215','sea-view cafe':'v3-216','ferry waiting terminal':'v3-217','Coastal deck retaining':'v3-232','Retained cultural trail rest':'heritage-kr-144-kr-rest','Contemporary volcanic':'v3-242','volcanic hill':'v3-242','nature learning':'v3-245','nature centre':'v3-245','cliff lookout':'v3-246','lookout cliff face':'v3-246','basalt discovery':'v3-247','Jeju courtyard back':'v3-243','three-rock cultural':'v3-247','Island arrival gateway':'v3-248','basalt guardian':'v3-249'}
solids=[]
for old in b['collision']['solids']:
 if old['y']+old['h']<=2240:solids.append(copy.deepcopy(old));continue
 matches=[key for phrase,key in reasons.items()if phrase.lower()in old.get('reason','').lower()]
 if not matches:continue
 key=matches[0]
 if key not in newby:continue
 q=copy.deepcopy(old);q['x']+=newby[key]['x']-oldby[key]['x'];q['y']+=newby[key]['y']-oldby[key]['y'];q['reason']='V8 relocated native architecture: '+old['reason'];solids.append(q)
def solid(x,y,w,h,reason):solids.append({'shape':'rect','x':x,'y':y,'w':w,'h':h,'reason':'V8: '+reason})
solid(2224,2396,1024,64,'continuous rail safety boundary, no public crossing');solid(2224,2516,400,28,'platform retaining face left of existing stair');solid(2784,2516,464,28,'platform retaining face right of existing stair')
site=[]
def place(kind,x,y,purpose,body=True):
 prop=b['props'][kind];key='v8-site-'+str(len(site)+1);o={'id':key,'prop':kind,'x':x,'y':y,'sortY':y,'scale':1,'anchor_px':prop['anchor_px'],'occlusion':prop.get('occlusion_class','low'),'occluder':{'source':prop['image'],'alphaThreshold':128,'sha256':prop['sha256']},'purpose':purpose};objects.append(o);site.append(o)
 if body:
  fp=prop['footprint'];solid(x-fp['width']/2,y-fp['depth'],fp['width'],fp['depth'],'visible '+key+' '+purpose)
if not gray:
 # Curbs and repeated urban tree pits define occupied city blocks rather than grass gaps.
 for x0,x1,y0,y1 in [(1456,1968,2448,2912),(1456,1968,3120,3456),(2368,3072,3120,3456)]:
  for x in range(x0+48,x1,136):
   place('v4-planter',x,y0+16,'commercial plot rear planter edge')
  for x in [x0+40,x1-40]:place('v3-streetlight-short',x,y1-24,'street-facing frontage light')
 for x,y in [(2024,2528),(2024,2896),(2024,3168),(2024,3488),(2200,2672),(2200,3168),(2200,3488),(1488,2864),(1928,2864),(2384,3424),(3056,3424),(2368,2896),(3040,2896)]:place('v4-planter',x,y,'urban planted curb / route framing')
 for x,y in [(1496,2664),(1944,2664),(1496,3216),(1944,3216),(2432,3224),(3000,3224),(2344,2776),(3080,2776)]:place('rf-prod-ginkgo',x,y,'aligned civic street tree, outside through route')
 for x,y in [(1544,2880),(1864,2880),(2424,2904),(3000,2904),(2432,3416),(2976,3416)]:place('rf-prod-bench',x,y,'commercial/station resting bay')
 # Independent campus perimeters, with actual west park gate and south entertainment gate.
 for name,x0,x1,y0,y1,gate,rail in [('Namsan',160,1296,2432,3584,3008,'v4-rail'),('Bora Bloom',3296,4288,2432,3568,3744,'v4-park')]:
  for x in range(x0+72,x1,136):
   place(rail,x,y0,name+' north perimeter')
   if name=='Namsan'and 576<x<896:continue
   if name=='Bora Bloom'and abs(x-3744)<264:continue
   place(rail,x,y1,name+' south perimeter')
  for y in range(y0+96,y1-32,96):
   for x in [x0,x1]:
    if name=='Namsan'and x==x1 and abs(y-3008)<112:continue
    place('v4-planter',x,y,name+' planted perimeter / open gateway')
 for x in range(416,4144,136):
  if abs(x-2528)>128:place('v4-rail',x,3760,'continuous coastal safety edge; terminal gate remains open')
 for x,y in [(416,2504),(960,2616),(256,2888),(288,3304),(560,3408),(1192,3224),(1024,3544),(3520,2616),(4232,2800),(3392,3464),(4000,3496),(3064,3584),(1320,3600)]:place('rf-prod-tree',x,y,'designed park/campus/coastal planting pocket')
 for x,y in [(832,2736),(1208,2960),(416,3488),(3584,3104),(3952,2824),(4048,3464),(1936,4880),(2496,4976),(2872,4496)]:place('rf-polish-flowers',x,y,'off-route landmark garden accents')
 for x,y in [(784,2960),(520,3352),(1152,3464),(3408,2880),(4120,3520),(2920,3632),(2320,3584),(3024,3672),(2320,5040)]:place('rf-prod-bench',x,y,'scenic rest with visible route gap')
 for x,y in [(2088,4456),(2080,4992),(2744,4904)]:place('fw-tangerine',x,y,'Jeju orchard wind shelter')
# Coast and sea geometry authored from physical walk mask, no invisible broad deck.
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
for q in merged:solid(*q,'coast/water footprint from new walk mask')
b['objects']=objects;b['collision']['solids']=solids
stops=json.loads((R/'assets-src/v7-world/stops.json').read_text());ids={'bookshop':'full-185','urban-hub':'v3-177','tower':'v3-180','terrace':'v3-181','wheel':'v3-192','carousel':'v3-193','creative-hall':'v3-194','park-entry':'v3-191','station':'v3-210','cafe':'v3-216','coast-viewdeck':'v3-232','oreum':'v3-242','cliff-lookout':'v3-246','lookout':'v3-246'}
stops=[v for v in stops if v['id']!='bridge']
for stop in stops:
 if stop['id']in ids:
  o=newby[ids[stop['id']]];stop['x'],stop['y']=o['x'],o['y']+56
 b['anchors'][stop['id']]={'point':[stop['x'],stop['y']],'approach':[stop['x'],stop['y']]}
b['anchors'].pop('bridge',None)
b['interactions']=[{'id':o['id'],'x':o['x'],'y':o['y'],'reach':104}for o in stops]
for spawn in b['spawns']:
 if spawn['id']=='jeju-arrival':spawn['x'],spawn['y']=plan['transport']['islandArrival']
 if spawn['id']=='coast-arrival':spawn['x'],spawn['y']=plan['transport']['mainlandArrival']
for portal in b['portals']:
 if portal['id']=='ferry-jeju':portal['circle']=[*plan['transport']['mainlandTrigger'],28]
 if portal['id']=='ferry-coast':portal['circle']=[*plan['transport']['islandTrigger'],28]
write(S/'stops.json',stops);write(S/'travel.json',plan['transport']);write(S/'routes.json',routes);write(S/'courts.json',courts);write(S/'relocations.json',{'baseline':plan['baseline'],'placements':moved,'removedActiveSouthernPlacements':removed,'oldRoadGeometryImported':False,'allOriginalSourcesRetained':True,'stage':'graybox'if gray else'premium-candidate'})
land.save(P/'land-mask.png');walk.save(P/'walk-mask.png');base.save(P/'terrain-composite-unquantized.png');write(P/'outdoor-draft.json',b)
for name,mask in layers.items():mask.save(P/f'{name}-mask.png')
write(S/'material-sources.json',{'art_source':'existing'if gray else'existing+host_image','graybox':gray,'textures':paths,'resampling':'none on approved art; infrastructure rail strips only cropped at native size','oldSouthernGroundImported':False,'noTracing':True})
print(json.dumps({'stage':'graybox'if gray else'premium','objects':len(objects),'relocatedLandmarks':len(moved),'solids':len(solids),'newRoutes':len(routes)}))
