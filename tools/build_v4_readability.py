"""Targeted source-art terrain joins and open, physical southern compound edges."""
from v4_readability_art import *
from PIL import ImageDraw,ImageFilter
import numpy as np,copy,math
P=S/'map';P.mkdir(exist_ok=True);(P/'layers').mkdir(exist_ok=True)
OLD=R/'assets-src/modern-streets/map';W,H=4352,4800
old=json.loads((OLD/'outdoor-bundle.json').read_text());b=copy.deepcopy(old);b['name']='Korean Arena — V4 Map Readability and Open Compounds'
for prop in b['props'].values():prop['image']=os.path.relpath((OLD/prop['image']).resolve(),P)
for o in b['objects']:
 if o.get('occluder',{}).get('source'):o['occluder']['source']=os.path.relpath((OLD/o['occluder']['source']).resolve(),P)
for t in b['tilesets']:t['manifest']='tileset.json'
for l in b['layers']:
 if l.get('kind')=='tiles':l['data']='layers/'+Path(l['data']).name
for name in ['land-mask.png','walk-mask.png','forest-mask.png']:shutil.copyfile(OLD/name,P/name)
(S/'terrain').mkdir(exist_ok=True)
for name in ['deep-water','shallow-water']:shutil.copyfile(R/'assets-src/v3-final/terrain'/f'{name}.png',S/'terrain'/f'{name}.png')
base=Image.open(OLD/'ground-native.png').convert('RGB');prior=np.array(base);land=np.array(Image.open(P/'land-mask.png'))>0
allowed=land.copy();allowed[:2240]=False;allowed[3488:]=False
edit=np.zeros((H,W),bool)
def blank():return Image.new('L',(W,H))
def material(name):
 path=R/'assets-src/modern-streets/terrain'/f'{name}.png'
 if not path.exists():path=R/'assets-src/v3-final/terrain'/f'{name}.png'
 a=np.array(Image.open(path).convert('RGB'));return Image.fromarray(a[(np.arange(H)%a.shape[0])[:,None],(np.arange(W)%a.shape[1])[None,:]])
def fill(mask,name):
 global edit
 arr=(np.array(mask)>0)&allowed;edit|=arr;base.paste(material(name),(0,0),Image.fromarray(np.uint8(arr)*255));return arr
def rect(box,r=12):
 m=blank();ImageDraw.Draw(m).rounded_rectangle(box,radius=r,fill=255);return m
def line(points,width,round=True):
 m=blank();d=ImageDraw.Draw(m);d.line(points,fill=255,width=width,joint='curve')
 if round:
  for x,y in points:d.ellipse((x-width//2,y-width//2,x+width//2-1,y+width//2-1),fill=255)
 return m
def union(*masks):return Image.fromarray(np.maximum.reduce([np.array(x)for x in masks]))
fixes=[]
def fix(key,box,shape,mat,why):
 # Restore only declared old road apron; new painted source texture is clipped to authored geometry.
 fill(rect(box,0),'grass');fill(shape,mat);fixes.append({'id':key,'box':box,'material':mat,'reason':why})
# Natural hillside destination: rounded apron, distinct from organic trail; no new car road.
fix('namsan-rounded-arrival',[600,2838,1032,3034],union(rect((608,2848,1024,3024),24),line([(576,2928),(704,2992),(832,2992),(832,2912)],72)),'paver','Remove square clipped apron corners, retain72px organic arrival and actual tower steps.')
# Bridge and deck are approached on their actual upper stair line; one continuous cool pedestrian material.
fix('bridge-west-joint',[2248,3096,2464,3236],union(line([(2304,3040),(2304,3160),(2464,3160)],80),rect((2256,3120,2344,3224),12)),'concrete','Remove half-material elbow/leftover vertical paving by the actual bridge at y3160; narrow stair stays separate.')
fix('bridge-east-joint',[2464,3088,2672,3224],line([(2464,3160),(2528,3160),(2528,3136),(2672,3136)],80),'concrete','Continuous bridge-to-promenade edge; no diagonal gravel wedge or abrupt24px offset.')
# Retail: generous facade-facing entry court inside street loop, separated from through movement.
fill(rect((2320,2688,2832,2756),12),'paver');fill(line([(2464,2752),(2464,2840)],72),'paver')
# Recover crossing markings removed by new apron; preserve actual shared-street and original crossing semantics.
# Park: coherent closed walking loop with separated ride forecourts, not a box-shaped vehicular grid.
park_loop=[(3456,2848),(3920,2848),(3920,3056),(3456,3056),(3456,2848)]
fill(line(park_loop,80),'concrete');fill(line([(3712,3296),(3712,2464)],112),'paver')
fill(rect((3584,3192,3840,3344),22),'paver')
fixes.append({'id':'park-loop-material-joints','box':[3408,2800,3976,3144],'material':'concrete/paver','reason':'Close internal loop along existing clear ground, give shared center spine continuous112px paver and80px secondary concrete; preserve individual ride aprons.'})
# Correct step-like notches in threshold and promenade only, preserving historic pixels above y2240.
fill(line([(2176,2240),(2176,2384),(2048,2384),(2048,2480)],112),'paver')
fixes.append({'id':'central-transition-elbow','box':[1992,2240,2232,2536],'material':'paver','reason':'Round clipped threshold elbow and keep continuous112px entry at existing alignment.'})
# Use literal image-generated curb pixels only on the editable compound border, with no curb across entrances.
def edge(mask):
 m=np.array(mask)>0;er=np.array(mask.filter(ImageFilter.MinFilter(5)))>0;return m&~er&allowed
def overlay(name,mask):
 im=np.array(Image.open(R/f'assets-src/modern-streets/overlays/{name}.png').convert('RGBA'));im=im[(np.arange(H)%im.shape[0])[:,None],(np.arange(W)%im.shape[1])[None,:]].copy();im[:,:,3]=np.minimum(im[:,:,3],np.uint8(mask)*255);base.paste(Image.fromarray(im),(0,0),Image.fromarray(im[:,:,3]))
# Ground border only at outer destination aprons, no interior joint seams.
for box in [(608,2848,1024,3024),(2320,2688,2832,2756),(3584,3192,3840,3344)]:
 mask=edge(rect(box,22));mask[2720:2860,2416:2512]=False;mask[2830:3008,560:752]=False;mask[3180:3350,3650:3776]=False;overlay('curb',mask)
# Restore literal zebra/tactile art in original location.
for name,x,y in [('crossing',2464,2784),('tactile',2464,2736),('tactile',2464,2832)]:
 im=Image.open(R/f'assets-src/modern-streets/overlays/{name}.png').convert('RGBA');base.paste(im,(x-im.width//2,y-im.height//2),im)
base.save(P/'terrain-composite-unquantized.png');Image.fromarray(np.uint8(edit)*255).save(P/'edit-mask.png')
# Compact new modules are additions only, old406objects and621solids untouched.
recipes=json.loads((S/'prop-recipes.json').read_text())
for row in recipes:
 k='v4-'+row['id'];im=Image.open(S/'props'/f'{k}.png');w,h=im.size;fw=12 if row['id']=='sign'else 48 if row['id']=='planter'else w-12;depth=16 if row['id']=='planter'else 8
 b['props'][k]={'image':'../props/'+k+'.png','sha256':sha(S/'props'/f'{k}.png'),'size':[w,h],'anchor_px':[w//2,h-1],'solid':False,'footprint':{'shape':'rect','width':fw,'depth':depth,'offset':[0,-depth/2],'basis':'world_px'},'occlusion_class':'low'if row['id']not in ['planter','sign']else'tall','occupant_policy':'y_sort','art_source':'host_image'}
placements=[]
def place(zone,kind,x,y):placements.append({'zone':zone,'kind':kind,'x':x,'y':y})
# Broken, low landscape edge: west/north trail and southern overlook stair remain open.
for x,y in [(672,3036),(904,3036),(616,2850),(964,2850),(1000,3188)]:place('namsan','stone',x,y)
for x,y in [(752,2824),(944,2824),(1000,3148)]:place('namsan','planter',x,y)
place('namsan','sign',624,3096)
# Forecourt pockets and commercial facade apron, main travel lane stays outside.
for x,y in [(1584,2848),(1872,2848),(2360,2744)]:place('station'if x<2000 else'commercial','hedge',x,y)
for x,y in [(2320,2712),(2832,2712)]:place('commercial','planter',x,y)
place('commercial','sign',2296,2712)
# Waterfront is a through-walk with rail ends away from bridge/stairs/arrival stops.
for x,y in [(1888,3264),(2224,3264),(2608,3224),(2760,3224),(2944,3232)]:place('promenade','rail',x,y)
for x,y in [(1824,3080),(2224,3080),(2744,3112),(2968,3104)]:place('promenade','planter',x,y)
place('station','sign',1960,3076)
# One district, decorative open perimeter sections and one primary arch, multiple safe secondary access gaps.
for x,y in [(3328,2920),(3536,2920),(4000,2968),(4152,2968),(3600,3352),(3824,3352),(3384,3152),(3552,3152),(4048,3192),(4232,3192)]:place('amusement','park',x,y)
for x,y in [(3616,2792),(3824,2792),(3576,2984),(3792,2984)]:place('amusement','hedge',x,y)
for x,y in [(3584,3224),(3840,3224),(3336,2808),(4160,2832)]:place('amusement','planter',x,y)
place('amusement','sign',3792,3320)
# Validate exact original route feet+shoulders before publishing any new object. Never relax clearance.
routes=json.loads((R/'assets-src/modern-streets/routes.json').read_text())
routes += [{'id':'v4-park-lower-loop','zone':'v4','points':[[3456,2848],[3456,3056],[3920,3056],[3920,2848]],'clearWidth':64}]
def route_hit(rect):
 for r in routes:
  for a,z in zip(r['points'],r['points'][1:]):
   dx,dy=z[0]-a[0],z[1]-a[1];dist=math.hypot(dx,dy)
   if not dist:continue
   for i in range(math.ceil(dist/8)+1):
    f=min(1,i*8/dist)
    for off in [-(r['clearWidth']/2-8),0,r['clearWidth']/2-8]:
     x=a[0]+dx*f-dy/dist*off;y=a[1]+dy*f+dx/dist*off
     if x+8>rect['x']and x-8<rect['x']+rect['w']and y+4>rect['y']and y-4<rect['y']+rect['h']:return r['id']
 return None
conflicts=[]
for i,p in enumerate(placements):
 prop=b['props']['v4-'+p['kind']];fp=prop['footprint'];rect={'shape':'rect','x':p['x']-fp['width']/2,'y':p['y']-fp['depth'],'w':fp['width'],'h':fp['depth'],'reason':f"V4 open {p['zone']} boundary {i+1}"};hit=route_hit(rect)
 if hit:conflicts.append({'placement':p,'route':hit});continue
 k='v4-boundary-'+str(i+1);b['objects'].append({'id':k,'prop':'v4-'+p['kind'],'x':p['x'],'y':p['y'],'sortY':p['y'],'scale':1,'anchor_px':prop['anchor_px'],'occlusion':prop['occlusion_class'],'occluder':{'source':prop['image'],'alphaThreshold':128,'sha256':prop['sha256']},'purpose':f"V4 {p['zone']}: low {p['kind']} edge, open approach retained"});b['collision']['solids'].append(rect);p.update(id=k,collider=rect)
if conflicts:print('PLACEMENT CONFLICTS NEED AUTHORING',json.dumps(conflicts));write(S/'initial-placement-diagnostics.json',conflicts)
accepted=[p for p in placements if 'id'in p]
write(S/'boundaries.json',{'placements':accepted,'omittedConflictingTrials':conflicts,'principle':'Open short perimeter sections only, original roads/entrances retained; physical feet match low visible modules.'});write(S/'routes.json',routes);write(S/'path-fixes.json',{'annotationAvailable':False,'defects':fixes,'northAndJejuUnchanged':True});write(P/'outdoor-draft.json',b)
print(json.dumps({'newBoundaries':len(accepted),'rejectedDraftPositions':len(conflicts),'oldObjects':406,'totalObjects':len(b['objects']),'totalSolids':len(b['collision']['solids']),'changedPixels':int(np.any(np.array(base)!=prior,axis=2).sum())}))
