"""Only road surfaces/flush infrastructure over approved V3. Literal source RGB, authored geometry."""
from modern_streets_art import *
from PIL import ImageDraw,ImageFilter
import copy,math
from scipy.ndimage import maximum_filter
P=S/'map';P.mkdir(exist_ok=True);(P/'layers').mkdir(exist_ok=True)
OLD=R/'assets-src/v3-final/map';W,H=4352,4800
old=json.loads((OLD/'outdoor-bundle.json').read_text());b=copy.deepcopy(old)
b['name']='Korean Arena — Modern Street and Infrastructure Review'
for p in b['props'].values():p['image']=os.path.relpath((OLD/p['image']).resolve(),P)
for o in b['objects']:
 if o.get('occluder',{}).get('source'):o['occluder']['source']=os.path.relpath((OLD/o['occluder']['source']).resolve(),P)
for t in b['tilesets']:t['manifest']='tileset.json'
for l in b['layers']:
 if l.get('kind')=='tiles':l['data']='layers/'+Path(l['data']).name
for name in ['land-mask.png','walk-mask.png','forest-mask.png']:shutil.copyfile(OLD/name,P/name)
for name in ['deep-water','shallow-water']:
 d=S/'terrain'/f'{name}.png';shutil.copyfile(R/'assets-src/v3-final/terrain'/f'{name}.png',d)
(S/'palette').mkdir(exist_ok=True);shutil.copyfile(R/'assets-src/v3-final/palette/palette.json',S/'palette/palette.json')
shutil.copyfile(R/'assets-src/v3-final/stops.json',S/'stops.json')
base=Image.open(OLD/'ground-native.png').convert('RGB');prior=np.array(base)
land=np.array(Image.open(P/'land-mask.png'))>0;walk=np.array(Image.open(P/'walk-mask.png'))>0
allowed=np.zeros((H,W),bool);allowed[2240:3488,1408:]=True
allowed[2800:3024,576:1040]=True;allowed[2984:3152,928:1280]=True
allowed&=land&walk
def blank():return Image.new('L',(W,H))
def path(points,width):
 im=blank();d=ImageDraw.Draw(im);half=width//2
 for (x,y),(xx,yy)in zip(points,points[1:]):
  assert x==xx or y==yy,('New urban segment must be cardinal',points)
  d.rectangle((min(x,xx)-half,min(y,yy)-half,max(x,xx)+half-1,max(y,yy)+half-1),fill=255)
 return im
def tex(name,rotate=False):
 p=S/'terrain'/f'{name}.png'
 if not p.exists():p=R/'assets-src/v3-final/terrain'/f'{name}.png'
 a=np.array(Image.open(p).convert('RGB'));a=np.rot90(a)if rotate else a
 return Image.fromarray(a[(np.arange(H)%a.shape[0])[:,None],(np.arange(W)%a.shape[1])[None,:]])
def paste(mask,name):
 arr=(np.array(mask)>0)&allowed;base.paste(tex(name),(0,0),Image.fromarray(np.uint8(arr)*255));return arr
reset=maximum_filter(np.array(Image.open(OLD/'modern-paving-mask.png')),size=49)>0
reset&=allowed;base.paste(tex('grass'),(0,0),Image.fromarray(np.uint8(reset)*255))
roads=[
 ('heritage-modern-threshold',[[2176,2240],[2176,2384],[2048,2384],[2048,2480]],112,'paver','threshold'),
 ('cultural-east-walk',[[2176,2368],[2976,2368],[2976,2480]],112,'paver','threshold'),
 ('modern-boulevard',[[2048,2480],[2048,2784],[2976,2784],[2976,2480]],128,'concrete','shared-street'),
 ('retail-entrance',[[2560,2752],[2464,2752],[2464,2840]],80,'paver','frontage'),
 ('station-forecourt-link',[[2048,2816],[1792,2816]],88,'paver','station'),
 ('railway-public-crossing',[[2048,2816],[2048,3040]],48,'paver','rail-crossing'),
 ('platform-public-lane',[[1792,3040],[2304,3040],[2304,3160]],80,'paver','station'),
 ('coast-west-promenade',[[1408,3232],[1792,3232],[1792,3224],[2304,3224],[2304,3160]],80,'concrete','promenade'),
 ('platform-west-walk',[[1792,3040],[1792,3232]],80,'concrete','promenade'),
 ('actual-viewdeck-stair',[[2112,3208],[2112,3104]],48,'paver','deck-stairs'),
 ('actual-bridge-link',[[2304,3160],[2464,3160]],48,'paver','bridge'),
 ('coast-east-promenade',[[2464,3160],[2528,3160],[2528,3136],[2912,3136]],80,'concrete','promenade'),
 ('bloom-arrival-boulevard',[[2912,3136],[3232,3136],[3232,3296],[3712,3296],[3712,3120]],112,'paver','park-main'),
 ('urban-park-link',[[2976,2784],[3152,2784],[3152,2848],[3456,2848]],96,'concrete','secondary'),
 ('bloom-central-spine',[[3712,3296],[3712,2464]],112,'paver','park-main'),
 ('bloom-attraction-walk',[[3456,2832],[3456,2848],[4000,2848],[4000,2864]],96,'concrete','park-secondary'),
 ('bloom-wheel-queue',[[3456,2832],[3456,3056],[3712,3056],[3712,3120]],80,'concrete','park-secondary'),
 ('bloom-discovery-walk',[[3920,2848],[3920,3096],[4144,3096],[4144,3136]],88,'concrete','park-secondary'),
 ('namsan-observation-arrival',[[704,2992],[832,2992],[832,2912]],80,'paver','arrival'),
 ('namsan-terrace-arrival',[[1120,3144],[1120,3024]],64,'paver','arrival'),
]
plazas=[
 ('urban-frontage',(2328,2712,2816,2832),'paver'),
 ('station-forecourt',(1536,2752,1992,2844),'paver'),
 ('station-lower-plaza',(1744,3008,2332,3072),'paver'),
 ('coastal-cafe-pocket',(1408,3168,1760,3264),'paver'),
 ('ferry-square',(2704,3096,3008,3216),'paver'),
 ('bloom-wheel-plaza',(3232,2744,3552,2880),'paver'),
 ('bloom-carousel-plaza',(3824,2784,4176,2928),'paver'),
 ('bloom-hall-plaza',(4000,3056,4304,3192),'paver'),
 ('bloom-ticket-plaza',(3584,3192,3840,3344),'paver'),
 ('bloom-kiosk-plaza',(3616,2400,3808,2528),'paver'),
 ('namsan-tower-plaza',(608,2848,1024,3024),'paver'),
 ('namsan-terrace-plaza',(944,2992,1264,3144),'paver'),
]
network=blank();nd=ImageDraw.Draw(network)
route_rows=[]
for key,points,width,material,role in roads:
 mask=path(points,width);network=Image.fromarray(np.maximum(np.array(network),np.array(mask)));paste(mask,material)
 route_rows.append({'id':key,'points':points,'surfaceWidth':width,'clearWidth':min(width-16,64)if role not in ['bridge','rail-crossing','deck-stairs']else 32,'material':material,'role':role})
for key,box,material in plazas:
 mask=blank();ImageDraw.Draw(mask).rounded_rectangle(box,radius=8,fill=255);network=Image.fromarray(np.maximum(np.array(network),np.array(mask)));paste(mask,material)
# Shared urban boulevard gets a continuous medium-charcoal center, bounded by real sidewalk geometry.
asphalt=path([[2048,2480],[2048,2784],[2976,2784],[2976,2480]],64);paste(asphalt,'asphalt')
def tiled_overlay(name,mask,vertical=False):
 im=Image.open(S/'overlays'/f'{name}.png').convert('RGBA')
 if vertical:im=im.transpose(Image.Transpose.ROTATE_90)
 a=np.array(im);a=a[(np.arange(H)%a.shape[0])[:,None],(np.arange(W)%a.shape[1])[None,:]].copy()
 a[:,:,3]=np.minimum(a[:,:,3],np.uint8((np.array(mask)>0)&allowed)*255)
 base.paste(Image.fromarray(a),(0,0),Image.fromarray(a[:,:,3]))
# Flush stone edging follows the union, so connected walkways never end in arbitrary curbs.
net=Image.fromarray(np.uint8((np.array(network)>0)&allowed)*255)
edge=np.array(net,dtype=int)-np.array(net.filter(ImageFilter.MinFilter(5)),dtype=int)
tiled_overlay('curb',Image.fromarray(np.uint8(edge>0)*255))
am=np.array(asphalt)>0;edge=am&~(np.array(asphalt.filter(ImageFilter.MinFilter(9)))>0)
# Drop curbs at the one actual north-south street crossing and true station path.
edge[2728:2848,2416:2512]=False;edge[2776:2848,1984:2112]=False
tiled_overlay('curb',Image.fromarray(np.uint8(edge)*255))
overlays=[]
def stamp(name,x,y,rotate=0):
 im=Image.open(S/'overlays'/f'{name}.png').convert('RGBA')
 if rotate:im=im.transpose(Image.Transpose.ROTATE_90)
 left=round(x-im.width/2);top=round(y-im.height/2);alpha=np.array(im.getchannel('A'));region=allowed[top:top+im.height,left:left+im.width]
 assert region.shape==alpha.shape and region.all(),(name,x,y)
 base.paste(im,(left,top),im);overlays.append({'overlay':name,'center':[x,y],'rotate90':bool(rotate),'size':list(im.size),'flush':True,'collider':False})
stamp('crossing',2464,2784)
for x,y in [(2464,2736),(2464,2832),(2048,2836),(2048,3024)]:stamp('tactile',x,y)
for x,y in [(2240,2818),(2784,2818),(2940,2656),(1536,3240)]:stamp('grate',x,y)
for x,y in [(1776,2840),(2816,3192),(3536,2880)]:stamp('drain',x,y)
for x,y in [(2224,2744),(2896,3088),(3744,3024)]:stamp('cover',x,y)
base.save(P/'terrain-composite-unquantized.png')
net.save(P/'modern-paving-mask.png');Image.fromarray(np.uint8(reset)*255).save(P/'erased-old-road-mask.png');asphalt.save(P/'asphalt-mask.png')
diff=np.any(np.array(base)!=prior,axis=2);assert not diff[:2240].any()and not diff[3648:].any()
write(S/'streets.json',{'world':[W,H],'baseline':'3209c28','routes':route_rows,'plazas':[{'id':k,'box':list(v),'material':m}for k,v,m in plazas],'overlays':overlays,'semantics':'All new RGB is original host-image/approved existing material art. Masks/road geometry are data. Overlays are flush surfaces, not new obstacles. No new road is a car gameplay system.','preserved':{'all406Placements':all({k:v for k,v in x.items()if k!='occluder'}=={k:v for k,v in y.items()if k!='occluder'}for x,y in zip(b['objects'],old['objects'])),'all621CollisionRectangles':b['collision']==old['collision'],'northRows':[0,2239],'unchangedJejuRows':[3648,4799],'juniFrames':144}})
write(P/'outdoor-draft.json',b);write(S/'routes.json',json.loads((R/'assets-src/v3-final/routes.json').read_text())+[{**r,'zone':'modern-streets'}for r in route_rows])
write(S/'ground-locality.json',{'changedPixelsBeforePalette':int(diff.sum()),'northChangedPixels':int(diff[:2240].sum()),'islandChangedPixels':int(diff[3648:].sum()),'approvedObjectsAndCollisionsEqual':True,'oldGroundSha256':sha(OLD/'ground-native.png')})
print(json.dumps({'routes':len(roads),'plazas':len(plazas),'flushOverlays':len(overlays),'changedGroundPixels':int(diff.sum()),'placementsPreserved':len(b['objects']),'collidersPreserved':len(b['collision']['solids'])}))
