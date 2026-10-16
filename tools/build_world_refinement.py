"""Compact review map DATA; approved/generated pixels only, actual Forge export."""
from world_refinement_art import R,S,C,F,write,sha,run
from PIL import Image,ImageDraw
import json,copy,math,shutil,hashlib
from stage_b_polish_map import terrain_layers
W,H=2304,1920
Z=json.loads((R/'docs/urban-zoning/zoning-plan.json').read_text());L=json.loads((R/'docs/world-refinement/compact-layout.json').read_text());OLD=json.loads((R/'assets-src/seoul-production/outdoor-bundle.json').read_text());M=F/'skills/generate2dmap/scripts'
B={'schema':'generate2dmap.map_bundle.v2','id':'refined-seoul','name':'Living Seoul — Palace, Scholars & Book Lane','world':{'width':W,'height':H,'unit':'px'},'tile_size':[32,32],'tilesets':[{'id':'town','manifest':'tileset.json'}],'layers':[{'name':'Ground','kind':'tiles','data':'layers/ground.json','tileset':'town'},{'name':'Edging','kind':'tiles','data':'layers/edging.json','tileset':'town'},{'name':'Props','kind':'objects'}],'props':{},'objects':[],'collision':{'actorRadius':8,'ySquash':.5,'walkRegions':[{'polygon':[[32,32],[W-32,32],[W-32,H-32],[32,H-32]]}],'solids':[],'rects':[]},'nav':{'cell':4},'spawns':[{'id':'start','x':1152,'y':832,'facing':'north'},{'id':'academy-return','x':544,'y':1152,'facing':'south'}],'anchors':{},'interactions':[],'portals':[],'camera':{'tiltDeg':50,'pixelToWorld':1,'bounds':[0,0,W,H]},'art_source':'host_image'}
for name,p in OLD['props'].items():
 p=copy.deepcopy(p);p['image']='../seoul-production/'+p['image'];p['solid']=False;B['props']['rf-'+name]=p
for p in json.loads((S/'props.json').read_text()):
 B['props'][p['id']]={'image':p['image'],'sha256':p['sha256'],'size':p['size'],'anchor_px':p['anchor'],'footprint':{'shape':'rect','width':24,'depth':16,'offset':[0,-8],'basis':'world_px'},'solid':False,'occlusion_class':'tall','occupant_policy':'y_sort'}
trans=L['groups'];moves=[]
def solid(x,y,w,h,why):B['collision']['solids'].append({'shape':'rect','x':x,'y':y,'w':w,'h':h,'reason':why})
def place(name,x,y,why,group=None,foot=None):
 if group:
  dx,dy=trans[group];moves.append({'prop':name,'old':[x,y],'new':[x+dx,y+dy],'translation':[dx,dy],'scale':1,'reason':why});x+=dx;y+=dy
 p=B['props'][name];B['objects'].append({'id':f'refined-{len(B["objects"])+1}','prop':name,'x':x,'y':y,'sortY':y,'scale':1,'anchor_px':p['anchor_px'],'occlusion':'tall','occluder':{'source':p['image'],'alphaThreshold':128},'purpose':why})
 if foot:
  ww,hh=foot;solid(x-ww/2,y-hh,ww,hh,why)
 return x,y

def reused(name,x,y,group,why,foot=None):return place('rf-'+name,x,y,why,group,foot)
def anchor(name,x,y,ax=None,ay=None):
 B['anchors'][name]={'point':[x,y],'approach':[x if ax is None else ax,y if ay is None else ay]};B['interactions'].append({'id':name,'x':x,'y':y,'reach':96})
# Approved building masses are translated WHOLE; native PNGs/wing geometry untouched.
for building in Z['buildings']:
 if building['id'] in ['academy','workshop','museum']:
  dx,dy=trans[building['id']]
  for mass in building['masses']:
   x,y,w,h=mass['bounds'];solid(x+dx,y+dy,w,h,building['code']+':'+mass['id']+' original native mass, whole-compound translation')
for name,x,y,group in [('prod-hall',672,790,'academy'),('prod-study',384,1072,'academy'),('prod-library',960,1008,'academy'),('prod-workshop',3312,850,'workshop'),('prod-museum',3520,1272,'museum'),('prod-sejong',2280,1184,'monument'),('prod-gate',2048,758,'palace')]:reused(name,x,y,group,'Approved '+name+' at original native scale; compact functional frontage')
solid(1304,1088,80,96,'Original Sejong monument base translated, ceremonial centreline clear')
solid(960,544,152,192,'Gateway west podium; original80pxcentre pass')
solid(1192,544,152,192,'Gateway east podium; original80pxcentre pass')
# Original SEVEN exterior palace segments and service openings translated only.
for seg in Z['palace']['segments']:
 (x,y),(xx,yy)=seg['points'];x-=896;xx-=896
 if y==yy:
  solid(x,y-16,xx-x,32,'Original palace '+seg['id']);n=math.ceil((xx-x)/148)
  for i in range(n):place('rf-prod-wall',round(x+(i+.5)*(xx-x)/n),y+16,'Original palace '+seg['id'])
 else:
  solid(x-16,y,32,yy-y,'Original palace '+seg['id']);n=math.ceil((yy-y)/176)
  for i in range(n):place('rf-prod-wall-ns',x,round(y+(i+1)*(yy-y)/n),'Original palace '+seg['id'])
for x in [384,1920]:place('rf-prod-service',x,448,'Original closed side service gate');solid(x-32,336,64,96,'Original closed side service threshold')
# Documented inner-reserve change: real courtyard, hall and64pxopen inner threshold.
for x0,x1 in [(400,970),(1334,1904)]:
 n=math.ceil((x1-x0)/148)
 for i in range(n):place('rf-prod-wall',round(x0+(i+.5)*(x1-x0)/n),448,'Inner palace garden cross-wall return')
solid(400,416,720,32,'Inner wall west return, includes inner gate side pier')
solid(1184,416,720,32,'Inner wall east return, includes inner gate side pier')
place('rf-inner-gate',1152,448,'Distinct single-tier open inner gate, not duplicated monumental gate')
place('rf-royal-hall',1152,320,'Original seven-bay royal exhibition main hall, visible beyond inner gate')
solid(880,160,544,144,'Royal hall wall/body only; eaves and terrace not whole-image collider')
for x in [848,1424]:solid(x,288,32,32,'Royal terrace side balustrade base')
place('rf-exhibit',1456,352,'Royal courtyard: hanji book/printing/textile cultural interpretation',foot=(84,24))
for x in [752,1584]:place('rf-banner',x,336,'Original royal-inspired banner, not a claimed historical flag',foot=(86,18))
for x in [768,1536]:place('rf-stone-lantern',x,496,'Korean seokdeung-inspired garden lantern, original interpretation',foot=(36,24))
# Academy old front threshold, same U geometry; low garden returns with two clear entrances.
for x in [480,864]:reused('prod-low-wall',x,1152,'academy','Accepted academy front edge')
reused('prod-court-gate',672,1152,'academy','Accepted academy south entrance')
for x in [272,688]:solid(x,1456,160,16,'Academy original front wall translated; centre opening kept')
for x in [152,944]:
 for y in [1200,1328]:
  place('rf-scholar-return',x,y,'Academy low scholar-garden return; east shortcut below1328')
  solid(x-6,y-128,32,128,'Scholar garden wall foot, not roof/cap bounding box')
# West final return leaves the south approach; east side1328..1472 remains OPEN.
place('rf-scholar-return',152,1456,'Academy west garden privacy return');solid(146,1328,32,128,'Academy west wall base')
for x in [224,864]:place('rf-scholar-wall',x,1008,'Short scholar-garden return beside actual hall mass');solid(x-68,996,136,12,'Low scholar wall foot')
# Context exhibits are the actual accepted generated assets, not regenerated templates.
for name,x,y,g,why,foot in [
 ('prod-writing',552,1000,'academy','Academy original primer/brush rack',(68,28)),
 ('polish-folio',824,940,'academy','Academy peer study station',(70,24)),
 ('polish-bamboo',480,1080,'academy','Academy quiet side garden',(36,18)),
 ('polish-flowers',848,1080,'academy','Academy reading-bench chrysanthemum',(32,16)),
 ('prod-armillary',3680,822,'workshop','Workshop observation platform celestial sphere',(64,36)),
 ('prod-sundial',3112,988,'workshop','Workshop hemispherical-sundial exhibit',(60,32)),
 ('prod-clock',3520,1040,'workshop','Workshop water-clock interpretation',(68,32)),
 ('polish-tools',3100,804,'workshop','Workshop service measuring tools',(64,22)),
 ('polish-chart',3592,948,'workshop','Workshop observation star chart',(70,24)),
 ('polish-bamboo',3072,1008,'workshop','Workshop contained service planting',(36,18)),
 ('prod-strategy',3408,1356,'museum','Museum open naval-strategy table',(84,32)),
 ('prod-ship',3712,1412,'museum','Museum miniature turtle-ship exhibit',(80,32)),
 ('polish-stele',3824,1352,'museum','Museum original naval-emblem interpretation',(38,22)),
 ('polish-flowers',3264,1480,'museum','Museum cobalt chrysanthemum',(32,16))]:reused(name,x,y,g,why,foot)
# Workshop OPEN timber equipment edge; public front gap and west service shortcut.
for x in [1504,1776,1920,2064,2200]:
 place('rf-work-rail',x,1440,'Low workshop equipment rail; public entrance1584..1680 stays clear');solid(x-68,1428,136,12,'Workshop timber rail foot')
for x,y in [(1480,1184),(1480,1440),(2224,1328),(2224,1440)]:
 place('rf-work-return',x,y,'Workshop timber return; west service gate1184..1312 stays open');solid(x-6,y-112,32,112,'Workshop return base')
# ONE modern corner, no randomly adjacent modern district or new interiors.
place('rf-cafe',512,1840,'Modern Korean book-and-tea frontage at cultural transition')
solid(352,1680,320,144,'Modern cafe actual facade mass, roof/awning are occluders')
place('rf-cafe-seating',752,1664,'Open modern book-cafe social seating, no enclosing fence',foot=(74,20))
# Pixel-exact structural ownership slices: L-hall and deep tool wing sort separately.
# No approved pixel is redrawn/resampled; strict reconstruction verifies every RGBA byte.
whole=B['props']['rf-prod-workshop'];image=Image.open(S/whole['image']).convert('RGBA');oldroot=[1776,1202];oldleft=oldroot[0]-whole['anchor_px'][0];oldtop=oldroot[1]-whole['anchor_px'][1];cut=1856-oldleft
reconstructed=Image.new('RGBA',image.size);derived=[]
B['objects']=[o for o in B['objects']if o['prop']!='rf-prod-workshop']
for name,box,depth in [('rf-workshop-main',(0,0,cut,image.height),992),('rf-workshop-wing',(cut,0,image.width,image.height),1184)]:
 part=image.crop(box);bb=part.getbbox();bbox=[box[0]+bb[0],box[1]+bb[1],box[0]+bb[2],box[1]+bb[3]];pixels=image.crop(tuple(bbox));reconstructed.paste(pixels,(bbox[0],bbox[1]));native=Image.new('RGBA',(pixels.width+4,pixels.height+4));native.paste(pixels,(2,2));file=S/f'props/{name}.png';native.save(file);anchorpx=[native.width//2,native.height-2];point=[oldleft+bbox[0]-2+anchorpx[0],oldtop+bbox[1]-2+anchorpx[1]]
 B['props'][name]={'image':str(file.relative_to(S)),'sha256':sha(file),'anchor_px':anchorpx,'size':list(native.size),'footprint':{'shape':'rect','width':24,'depth':16,'offset':[0,-8],'basis':'world_px'},'solid':False,'occlusion_class':'tall','occupant_policy':'y_sort'}
 place(name,*point,'Pixel-exact approved workshop ownership slice; independent hall/wing depth');B['objects'][-1]['sortY']=depth;derived.append({'id':name,'sourceBox':bbox,'source':'../seoul-production/props/prod-workshop.png','sourceSha256':sha(S/whole['image']),'image':str(file.relative_to(S)),'sha256':sha(file),'anchor':anchorpx,'point':point,'sortY':depth})
assert reconstructed.tobytes()==image.tobytes(),'Approved workshop reconstruction lost pixels'
write(S/'derived-architecture.json',{'method':'Disjoint ownership crops from existing approved native PNG; no generation/resampling/painting; exact full RGBA reconstruction','sourceSize':list(image.size),'sourceRoot':oldroot,'cut':cut,'pixelDifferences':0,'parts':derived})
# Front stairs are walkable floor: sort by wall/base line, not stair image bottom.
for o in B['objects']:
 if o['prop']in ['rf-royal-hall','rf-prod-hall','rf-prod-study','rf-prod-library','rf-prod-museum','rf-cafe']:
  o['sortY']={'rf-royal-hall':304,'rf-prod-hall':1088,'rf-prod-study':1376,'rf-prod-library':1312,'rf-prod-museum':1664,'rf-cafe':1824}[o['prop']]

# Purposeful facade planting, service storage and resting places; paths never prop scatter.
for prop,positions,why,foot in [
 ('prod-planter',[(384,1148),(704,1148),(1664,1056),(1792,1056),(1768,1712),(2096,1712),(1024,1200),(1408,1200)],'Landmark entry planting outside clear approach',(30,14)),
 ('prod-bench',[(640,1384),(960,1216),(1456,1216),(1536,1408),(2208,1856),(832,592),(1536,576),(944,1712)],'Purposeful reading / cultural / garden rest',(54,12)),
 ('prod-jars',[(976,1240),(1424,1120),(2224,1688)],'Service-side onggi storage, not a public gateway',(40,20)),
 ('prod-lantern',[(464,1584),(624,1584),(880,864),(1424,864),(1568,1400),(1696,1504),(1712,1768),(2264,1840),(1040,1248),(1280,1568)],'Gateways, frontage and turning-point guidance',(16,12)),
 ('polish-flowers',[(920,816),(1384,816),(288,1840),(1072,1584)],'Ceremonial / cultural threshold flowers',(32,16)),
 ('polish-bamboo',[(512,352),(1792,352),(832,1776)],'Contained royal-garden / modern transition planting',(36,18))]:
 for x,y in positions:place('rf-'+prop,x,y,why,foot=foot)
# Curated trees grouped by real gardens/edges, no giant empty grid orchard.
for i,(x,y,why) in enumerate([
 (512,288,'Royal west garden'),(704,272,'Royal west garden'),(1760,272,'Royal east garden'),(1840,560,'Royal garden east return'),(528,576,'Royal west outer garden'),
 (192,800,'Academy north street garden'),(112,1072,'Academy west garden'),(272,1600,'Academy-to-book-lane shade'),(112,1504,'Academy lane edge'),(1008,1136,'Academy east garden'),
 (2064,832,'Workshop rear garden'),(2192,1056,'Observation platform backdrop'),(1472,944,'Workshop western edge'),(1440,1584,'Cultural garden beside history lane'),
 (992,736,'Gateway west garden'),(1488,768,'Gateway east garden'),(800,864,'Hanok-to-palace garden path'),(1424,1088,'Plaza east cultural pocket'),
 (960,1632,'Cultural transition shade'),(1280,1824,'Cultural transition garden'),(1504,1856,'History-lane shade'),(128,1808,'Modern corner green edge'),(2176,512,'Northern east green edge'),(96,528,'Northern west green edge')]):
 prop='rf-prod-ginkgo'if i%3==0 else'rf-prod-tree';place(prop,x,y,why,foot=(24,16))
# No continuation pretending a finished future district. Existing full plan remains a reference.
solid(32,H-2,W-64,2,'Southern review edge; full modern district needs later approval')
for name,x,y,ax,ay in [('gateway',1152,768,1152,832),('outer-court',1152,496,1152,496),('inner-gate',1152,448,1152,480),('royal-hall',1152,320,1152,352),('royal-exhibit',1456,384,1456,404),('royal-west-garden',640,512,640,544),('academy',544,1120,544,1152),('academy-front',544,1456,544,1520),('academy-side',944,1392,976,1392),('workshop',1632,1472,1632,1536),('workshop-service',1480,1264,1440,1264),('armillary',2144,1174,2144,1232),('museum',1984,1696,1984,1808),('modern-cafe',512,1840,512,1872),('sejong',1344,1208,1344,1248),('garden-route',1120,1664,1120,1664)]:anchor(name,x,y,ax,ay)
B['portals']=[{'id':'academy-door','circle':[544,1120,16],'to':'refined-reading-room:start','entranceByFrom':{'refined-reading-room':[544,1152]},'latch':True,'reciprocal':True}]
# Existing generated surfaces + user-authorized compact semantic layout, not new painted art.
material=Image.new('L',(W,H),0);d=ImageDraw.Draw(material)
for road in L['roads']:
 points=[tuple(p)for p in road['points']];width=road['width']+20;d.line(points,fill=road.get('material',1),width=width,joint='curve')
 for x,y in points:
  r=width//2;d.ellipse((x-r,y-r,x+r,y+r),fill=road.get('material',1))
for court in Z['courts']:
 group='palace'if court['belongsTo']=='gate'else court['belongsTo']
 if group in trans and group not in ['palace','monument']:
  dx,dy=trans[group];pts=[(x+dx,min(y+dy,1872))for x,y in court['polygon']];d.polygon(pts,fill={'academy':2,'workshop':3,'museum':4}[group])
for b in L['buildings']:
 for mass in b['masses']:
  x,y,w,h=mass['bounds'];d.rectangle((x,y,x+w,y+h),fill={'gate':1,'academy':2,'workshop':3,'museum':4,'monument':1}[b['id']])
d.polygon([(928,768),(1376,768),(1376,896),(1440,1024),(1440,1312),(1344,1408),(960,1408),(864,1280),(912,1088),(928,896)],fill=1)
d.rectangle((1760-896,448,2336-896,544),fill=1);d.rectangle((1112,400,1192,832),fill=1)
d.rectangle((832,336,1472,408),fill=4)
for pts in [[(1152,384),(1456,404)],[(1152,496),(640,544)],[(1152,496),(1664,544)],[(640,544),(640,336)],[(1664,544),(1712,336)]]:d.line(pts,fill=1,width=48)
d.rectangle((320,1088,768,1120),fill=2);d.line([(544,1084),(544,1488)],fill=1,width=48)
d.line([(1632,1416),(1632,1536)],fill=3,width=64);d.rectangle((1568,992,1856,1024),fill=3)
d.rectangle((2064,1040,2224,1184),fill=4);d.rectangle((1760,1664,2208,1696),fill=4);d.line([(1984,1664),(1984,1808)],fill=4,width=64)
d.rectangle((288,1824,832,1872),fill=4)
material.save(S/'semantic-materials.png')
source=Image.open(R/'assets-src/gwanghwamun/tiles.png').convert('RGBA');tiles=[source.crop(((i%4)*32,(i//4)*32,(i%4+1)*32,(i//4+1)*32))for i in range(8)];unique=[];lookup={}
def register(im):
 key=im.tobytes()
 if key not in lookup:lookup[key]=len(unique);unique.append(im)
 return lookup[key]
ground,edging=terrain_layers(material,tiles,register,output_root=S)
columns=16;atlas=Image.new('RGBA',(columns*32,math.ceil(len(unique)/columns)*32))
for i,im in enumerate(unique):atlas.paste(im,((i%columns)*32,(i//columns)*32))
atlas.save(S/'tiles.png');write(S/'tileset.json',{'schema':'generate2dmap.tileset.v1','image':'tiles.png','sha256':sha(S/'tiles.png'),'tile_size':[32,32],'columns':16,'kind':'flat','materials':['grass','ceremonial-stone','academy-earth','workshop-grit','museum-stone'],'tiles':[{'index':i,'properties':{'material':'existing-generated-RGB-compact-semantic-alpha','walkable':True}}for i in range(len(unique))],'seamless_verified':False,'art_source':'existing'})
for index,obj in enumerate(B['objects']):obj['id']=f'refined-{index+1}'
write(S/'layers/ground.json',ground);write(S/'layers/edging.json',edging);write(S/'outdoor-draft.json',B);write(S/'translations.json',moves)
# Fresh content-addressed hashes include layers, not just JSON references.
fingerprint=hashlib.sha256((''.join(sha(p)for p in [S/'outdoor-draft.json',S/'tileset.json',S/'layers/ground.json',S/'layers/edging.json'])).encode()).hexdigest()[:16];hashed=C/f'outdoor-{fingerprint}.json'
if not hashed.exists():run(M/'map_bundle.py','hash','--bundle',S/'outdoor-draft.json','--output',hashed)
shutil.copyfile(hashed,S/'outdoor-bundle.json');run(M/'map_bundle.py','validate','--bundle',S/'outdoor-bundle.json','--report',C/f'validate-{fingerprint}.json')
for name,script,args in [('navigation','map_nav.py',['check','--publish-on-fail']),('tiled','export_tiled.py',['export','--embedded-variant'])]:
 dest=S/name
 if dest.exists():shutil.move(dest,C/f'previous-{name}-{len(json.loads((S/"commands.json").read_text()))}')
 run(M/script,*args,'--bundle',S/'outdoor-bundle.json','--output-dir',dest)
# Runtime reads real Tiled tile/collision output with the existing Plaza controller.
t=json.loads((S/'tiled/map.embedded.tmj').read_text());collision=next(l for l in t['layers']if l['name']=='collision');solids=[o for o in collision['objects']if o['type']=='solid'];assert all(not o.get('polygon')for o in solids)
t['layers']=[l for l in t['layers']if l['type']=='tilelayer']+[dict(collision,name='Collision',objects=solids)];t['tilesets']=[dict(t['tilesets'][0],image='tiles.png')]
D=R/'public/review/world-refinement';D.mkdir(parents=True,exist_ok=True);write(D/'plaza.json',t);shutil.copyfile(S/'tiles.png',D/'tiles.png')
for name,p in B['props'].items():shutil.copyfile(S/p['image'],D/f'{name}.png')
write(D/'anchors.json',{name:p['anchor_px']for name,p in B['props'].items()});world={'width':W,'height':H,'spawn':[1152,832],'npc':[1344,1248],'follow':55,'role':B['name'],'mood':'Compact royal-to-modern review','vi':B['name'],'mapSha256':sha(D/'plaza.json'),'objects':[{'id':i+1,'kind':o['prop'],'x':o['x'],'y':o['y'],'sortY':o['sortY'],'width':B['props'][o['prop']]['footprint']['width'],'height':B['props'][o['prop']]['footprint']['depth'],'label':o['purpose'],'collide':False}for i,o in enumerate(B['objects'])]};write(S/'world.json',world)
# Real linked-room source, original room art/runtime is never modified.
room=copy.deepcopy(json.loads((R/'assets-src/seoul-production/room-bundle.json').read_text()));room['id']='refined-reading-room';room['portals']=[{'id':'refined-room-exit','circle':[384,510,14],'to':'refined-seoul:academy-return','entranceByFrom':{'refined-seoul':'start'},'latch':True,'reciprocal':True}];write(S/'room-draft.json',room)
rh=C/f'room-{sha(S/"room-draft.json")[:16]}.json'
if not rh.exists():run(M/'map_bundle.py','hash','--bundle',S/'room-draft.json','--output',rh)
shutil.copyfile(rh,S/'room-bundle.json')
for name,other in [('outdoor','room'),('room','outdoor')]:
 dest=S/f'{name}-linked-navigation'
 if dest.exists():shutil.move(dest,C/f'previous-linked-{name}-{len(json.loads((S/"commands.json").read_text()))}')
 run(M/'map_nav.py','check','--bundle',S/f'{name}-bundle.json','--link',S/f'{other}-bundle.json','--output-dir',dest,'--publish-on-fail')
# Actual Forge source composition, separate from later real Phaser screenshots.
base=Image.new('RGBA',(W,H))
for data in [ground,edging]:
 for row,line in enumerate(data):
  for col,idx in enumerate(line):
   if idx>=0:base.alpha_composite(unique[idx],(col*32,row*32))
base.save(S/'layers/base.png');placements={'props':[{'id':o['id'],'image':B['props'][o['prop']]['image'],'x':o['x'],'y':o['y'],'anchorPx':o['anchor_px'],'sortY':o['sortY']}for o in B['objects']]};write(S/'placements.json',placements)
out=S/'composed'
if out.exists():shutil.move(out,C/f'previous-composed-{len(json.loads((S/"commands.json").read_text()))}')
out.mkdir();run(M/'compose_layered_preview.py','--base',S/'layers/base.png','--placements',S/'placements.json','--output',out/'preview.png','--report',out/'composition.json','--bundle',S/'outdoor-bundle.json','--debug-overlay',out/'collision-overlay.png','--audit-out',out/'audit.json')
Image.open(out/'preview.png').resize((288,240),Image.Resampling.NEAREST).save(D/'minimap.png')
write(S/'geometry-proof.json',{'sourceMasterplan':sha(R/'docs/urban-zoning/zoning-plan.json'),'newLayoutSha256':sha(R/'docs/world-refinement/compact-layout.json'),'world':[W,H],'originalPalaceSegments':Z['palace']['segments'],'palaceTranslation':[-896,0],'innerChange':'Closed reserve replaced by hall/garden; original inner cross-wall y432 split around64pxpassage','sourceArtScale':1,'normalWalk':60,'run':100,'newStructures':L['newStructures'],'reservedNPCs':[{'id':'sejong','point':[704,1328]},{'id':'jang','point':[2128,1344]},{'id':'yi','point':[2208,1760]}]})
print(json.dumps({'world':[W,H],'objects':len(B['objects']),'solids':len(solids),'uniqueTiles':len(unique),'atlas':list(atlas.size)}))
