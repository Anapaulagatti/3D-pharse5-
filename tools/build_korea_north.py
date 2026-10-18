"""Stage A scene DATA and literal extracted generated boundary strips; real Forge export."""
from korea_art import *
from PIL import ImageDraw
from stage_b_polish_map import terrain_layers
import copy,math
M=F/'skills/generate2dmap/scripts';BASE=R/'assets-src/world-refinement';N=S/'north';D=R/'public/review/living-korea/north';N.mkdir(parents=True,exist_ok=True);D.mkdir(parents=True,exist_ok=True)
B=copy.deepcopy(json.loads((BASE/'outdoor-bundle.json').read_text()));B['id']='korea-north';B['name']='Living Korea — Heritage to Travel Garden';B['world']['height']=2240;B['camera']['bounds']=[0,0,2304,2240]
for p in B['props'].values():p['image']=os.path.relpath((BASE/p['image']).resolve(),N)
B['tilesets']=[{'id':'town','manifest':'tileset.json'}];B['layers']=[{'name':'Ground','kind':'tiles','data':'layers/ground.json','tileset':'town'},{'name':'Edging','kind':'tiles','data':'layers/edging.json','tileset':'town'},{'name':'Props','kind':'objects'}]
# Move full museum functional cluster, never rescale/repaint approved architecture.
ids=['refined-4','refined-73','refined-74','refined-75','refined-76']
# Exact ownership chosen from source coordinates and purpose, not a broad random bbox.
move=[]
for o in B['objects']:
 if ('Museum' in o['purpose'] or o['prop']=='rf-prod-museum' or (o['x'],o['y'])in[(1768,1712),(2096,1712),(2224,1688),(2208,1856),(1712,1768),(2264,1840)]):
  old=[o['x'],o['y']];o['y']+=224;o['sortY']+=224;move.append({'id':o['id'],'prop':o['prop'],'old':old,'new':[o['x'],o['y']],'shift':[0,224],'scale':1})
solids=B['collision']['solids'];kept=[]
for q in solids:
 reason=q.get('reason','')
 if any(k in reason for k in ['palace ','palace west','palace east','Inner wall','Scholar garden','Academy original front wall','Low scholar wall','Workshop timber','Workshop return','Southern review']):continue
 if reason.startswith('H02:')or'Museum'in reason or [q.get('x'),q.get('y')]in [[1753,1698],[2081,1698],[2204,1668],[2181,1844],[1704,1756],[2256,1828]]:q['y']+=224
 kept.append(q)
B['collision']['solids']=kept
removed=[]
for o in list(B['objects']):
 if o['prop']in ['rf-prod-wall','rf-prod-wall-ns','rf-prod-service','rf-prod-low-wall','rf-scholar-return','rf-scholar-wall','rf-work-rail','rf-work-return']:
  removed.append({'id':o['id'],'prop':o['prop'],'point':[o['x'],o['y']]});B['objects'].remove(o)
for k,a in B['anchors'].items():
 if k=='museum':a['point'][1]+=224;a['approach'][1]+=224
B['anchors']['travel-garden']={'point':[1152,2080],'approach':[1152,2048]};B['interactions'].append({'id':'travel-garden','x':1152,'y':2080,'reach':96})
B['collision']['walkRegions']=[{'polygon':[[32,32],[2272,32],[2272,2208],[32,2208]]}]
B['portals']=[{'id':'academy-door','circle':[544,1120,16],'to':'korea-reading-room:start','entranceByFrom':{'korea-reading-room':[544,1152]},'latch':True,'reciprocal':True}]
B['spawns'].append({'id':'travel-return','x':1152,'y':2016,'facing':'north'})
recipes=[]
def solid(x,y,w,h,why):B['collision']['solids'].append({'shape':'rect','x':x,'y':y,'w':w,'h':h,'reason':why})
def addprop(key,path,anchor):
 im=Image.open(path);B['props'][key]={'image':os.path.relpath(path,N),'sha256':sha(path),'size':list(im.size),'anchor_px':anchor,'solid':False,'footprint':{'shape':'rect','width':16,'depth':8,'offset':[0,-4],'basis':'world_px'},'occlusion_class':'tall','occupant_policy':'y_sort'}
def place(key,x,y,why,depth=None):
 p=B['props'][key];B['objects'].append({'id':f'kr-{len(B["objects"])+1}-{key}','prop':key,'x':x,'y':y,'sortY':y if depth is None else depth,'scale':1,'anchor_px':p['anchor_px'],'occlusion':'tall','occluder':{'source':p['image'],'alphaThreshold':128},'purpose':why})
def wall(key,kind,x0,y0,x1,y1,why):
 im=Image.open(S/f'props/{kind}.png').convert('RGBA');bb=im.getbbox();im=im.crop(bb)
 vertical=x0==x1
 if vertical:
  crop=[0,8,im.width,im.height-25]if kind=='kr-palace-v'else[0,36,im.width,48];tile=im.crop(crop);length=y1-y0;result=Image.new('RGBA',(tile.width,length));step=tile.height
  for y in range(0,length,step):result.paste(tile.crop((0,0,tile.width,min(step,length-y))),(0,y))
  anchor=[result.width//2,length];point=[x0,y1];solid(x0-8,y0,16,length,why)
 else:
  crop=[18,0,42,im.height]if kind=='kr-timber-h'else[8,0,im.width-8,im.height];tile=im.crop(crop);length=x1-x0;result=Image.new('RGBA',(length,tile.height));step=tile.width
  for x in range(0,length,step):result.paste(tile.crop((0,0,min(step,length-x),tile.height)),(x,0))
  anchor=[0,result.height];point=[x0,y0];solid(x0,y0-16,length,16,why)
 path=N/f'props/{key}.png';path.parent.mkdir(exist_ok=True);result.save(path);addprop(key,path,anchor);place(key,*point,why)
 recipes.append({'id':key,'kind':kind,'source':f'../props/{kind}.png','trim':list(bb),'sourceCrop':crop,'tileStride':step,'from':[x0,y0],'to':[x1,y1],'nativeScale':1,'overlappingTilePixels':0,'why':why})
# Palace boundary: deliberate single main entrance; misleading side-gate sprites removed.
wall('palace-north','kr-palace-h',384,80,1920,80,'Palace continuous northern enclosure')
for x in [384,1920]:wall(f'palace-side-{x}','kr-palace-v',x,80,x,720,'Palace coherent side return; false floating service gates removed')
wall('palace-front-west','kr-palace-h',384,720,936,720,'Palace wall joins outer gate west podium')
wall('palace-front-east','kr-palace-h',1368,720,1920,720,'Palace wall joins outer gate east podium')
wall('palace-inner-west','kr-palace-h',384,448,1056,448,'Inner court boundary socket to inner gate west pier')
wall('palace-inner-east','kr-palace-h',1248,448,1920,448,'Inner court boundary socket to inner gate east pier')
# Physical inner gate piers meet same64px open passage; painted wings overlap only architectural socket.
solid(1056,416,64,32,'Inner gate west side pier');solid(1184,416,64,32,'Inner gate east side pier')
# Academy U buildings already enclose court. Low front wall terminates at stone garden piers,
# no tall return sprites poking through roof, east shortcut remains intentionally open.
wall('academy-front-west','kr-scholar-h',304,1472,480,1472,'Academy low garden frontage west, U buildings define side boundaries')
wall('academy-front-east','kr-scholar-h',608,1472,832,1472,'Academy low garden frontage east with open east garden shortcut')
# Real service/front openings, no stacked/overlapping rails/posts.
for key,x0,x1 in [('work-front-west',1480,1584),('work-front-east',1680,2224)]:wall(key,'kr-timber-h',x0,1440,x1,1440,'Workshop purposeful timber enclosure with96pxfront opening')
for key,x,y0,y1 in [('work-west-rear',1480,1040,1184),('work-west-front',1480,1312,1440),('work-east',2224,1040,1440)]:wall(key,'kr-timber-v',x,y0,x,y1,'Workshop continuous return, west128pxservice gap')
wall('work-rear-east','kr-timber-h',2016,1040,2224,1040,'Observation garden rear return meets equipment wing')
# A single extracted native end post grounds each purposeful timber opening.
cap=Image.open(S/'props/kr-timber-h.png').crop((2,2,18,36));capfile=N/'props/kr-timber-cap.png';cap.save(capfile);addprop('kr-timber-cap',capfile,[8,34])
posts=set()
for q in recipes:
 if q['kind']not in ['kr-timber-h','kr-timber-v']:continue
 (x0,y0),(x1,y1)=q['from'],q['to'];n=math.ceil(math.hypot(x1-x0,y1-y0)/96)
 for i in range(n+1):posts.add((round(x0+(x1-x0)*i/n),round(y0+(y1-y0)*i/n)))
for x,y in sorted(posts):
 place('kr-timber-cap',x,y,'One authored post per timber socket; shared corners deduplicated, no baked end-post doubles');solid(x-6,y-10,12,10,'Timber terminal/intermediate post base')
write(N/'timber-sockets.json',{'posts':[list(p)for p in sorted(posts)],'uniquePosts':len(posts),'maximumSpan':96,'method':'Literal post-free generated beam gaps tiled without overlap; separately extracted native posts once per socket; graph junctions deduplicated'})
# Quiet garden rest between workshop and translated museum, outside the cross-lane.
for key,x,y,why in [('rf-polish-flowers',1848,1520,'Museum cross-lane garden edge'),('rf-polish-flowers',2056,1520,'Museum cross-lane garden edge'),('rf-prod-bench',2144,1552,'Purposeful pedestrian pause between separate institutions'),('rf-prod-planter',1520,1056,'Workshop rear terminal planting')]:
 place(key,x,y,why);solid(x-16,y-14,32,14,why)
# Corner piers only where actual masonry boundaries meet; never duplicate each module's posts.
addprop('kr-pier',S/'props/kr-pier.png',[22,62])
for x,y in [(384,80),(1920,80),(384,720),(1920,720),(384,448),(1920,448),(304,1472),(832,1472)]:place('kr-pier',x,y,'One deliberate grounded wall junction / garden end pier')
# Keep new piers off public entrances and give foot collision.
for x,y in [(384,80),(1920,80),(384,720),(1920,720),(384,448),(1920,448),(304,1472),(832,1472)]:solid(x-12,y-16,24,16,'Boundary pier base')
# Update public road apron and museum frontage as a whole.
material=Image.new('L',(2304,2240),0);material.paste(Image.open(BASE/'semantic-materials.png'),(0,0));draw=ImageDraw.Draw(material)
draw.rectangle((1672,1420,2272,1918),fill=0);draw.rectangle((1696,1696,2224,1920),fill=4)
for points,width,fill in [([(1632,1536),(1632,1616),(1984,1616),(2240,1616)],72,1),([(1632,1616),(1584,1760),(1640,2016),(1856,2064),(1984,2032),(1984,1920)],80,4),([(1120,1664),(1152,1888),(1152,2080)],96,1),([(512,1872),(800,1920),(1152,2080)],72,4),([(1152,2080),(1456,2080),(1640,2016)],80,4)]:
 draw.line(points,fill=fill,width=width+20,joint='curve')
 for x,y in points:r=(width+20)//2;draw.ellipse((x-r,y-r,x+r,y+r),fill=fill)
draw.rounded_rectangle((1008,1984,1296,2176),radius=32,fill=4)
material.save(N/'semantic-materials.png')
rawtiles=Image.open(R/'assets-src/gwanghwamun/tiles.png');tiles=[rawtiles.crop(((i%4)*32,(i//4)*32,(i%4+1)*32,(i//4+1)*32))for i in range(8)];unique=[];lookup={}
def register(im):
 key=im.tobytes()
 if key not in lookup:lookup[key]=len(unique);unique.append(im)
 return lookup[key]
ground,edge=terrain_layers(material,tiles,register,output_root=N);atlas=Image.new('RGBA',(512,math.ceil(len(unique)/16)*32))
for i,im in enumerate(unique):atlas.paste(im,((i%16)*32,(i//16)*32))
atlas.save(N/'tiles.png');write(N/'tileset.json',{'schema':'generate2dmap.tileset.v1','image':'tiles.png','sha256':sha(N/'tiles.png'),'tile_size':[32,32],'columns':16,'kind':'flat','materials':['grass','stone','earth','grit','silver-stone'],'tiles':[{'index':i,'properties':{'walkable':True}}for i in range(len(unique))],'seamless_verified':False,'art_source':'existing'})
write(N/'layers/ground.json',ground);write(N/'layers/edging.json',edge)
# First travel-garden wayfinding/rest, not another modern district.
if (S/'park-kit-props.json').exists():
 for key,x,y,why,foot in [('kr-directory',1360,2144,'Contemporary wayfinding at the signed regional travel garden',(120,18)),('kr-rest',944,2176,'Modern travel-garden rest, off main walking route',(100,20))]:
  meta=next(q for q in json.loads((S/'park-kit-props.json').read_text())if q['id']==key);addprop(key,S/meta['image'],meta['anchor']);place(key,x,y,why);solid(x-foot[0]/2,y-foot[1],*foot,why)
 B['portals'].append({'id':'to-namsan','circle':[1152,2080,32],'to':'korea-namsan:start','entranceByFrom':{'korea-namsan':[1152,2016]},'latch':True,'reciprocal':True})
write(N/'boundary-recipes.json',recipes);write(N/'museum-translations.json',move);write(N/'removed-boundary-instances.json',removed)
for o in B['objects']:o['occluder']['source']=B['props'][o['prop']]['image']
write(N/'outdoor-draft.json',B)
print('Prepared',len(B['objects']),'objects',len(B['collision']['solids']),'solids','museum cluster',len(move))
