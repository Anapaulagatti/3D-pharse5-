"""First park increment, authored map DATA using generated native art; no API/generation."""
from korea_art import *
from PIL import ImageDraw
from stage_b_polish_map import terrain_layers
import math,copy
P=S/'park';P.mkdir(exist_ok=True);W,H=1408,1280
plan=json.loads((R/'docs/living-korea/southern-masterplan.json').read_text());zone=next(z for z in plan['destinations']if z['id']=='namsan')
B={'schema':'generate2dmap.map_bundle.v2','id':'korea-namsan','name':'Namsan — Hill of Letters','world':{'width':W,'height':H,'unit':'px'},'tile_size':[32,32],'tilesets':[{'id':'town','manifest':'tileset.json'}],'layers':[{'name':'Ground','kind':'tiles','data':'layers/ground.json','tileset':'town'},{'name':'Edging','kind':'tiles','data':'layers/edging.json','tileset':'town'},{'name':'Props','kind':'objects'}],'props':{},'objects':[],'collision':{'actorRadius':8,'ySquash':.5,'walkRegions':[{'polygon':[[32,32],[W-32,32],[W-32,H-32],[32,H-32]]}],'solids':[],'rects':[]},'nav':{'cell':4},'spawns':[{'id':'start','x':704,'y':1056,'facing':'north'}],'anchors':{},'interactions':[],'portals':[{'id':'return-heritage','circle':[704,1120,32],'to':'korea-north:travel-return','entranceByFrom':{'korea-north':[704,1056]},'latch':True,'reciprocal':True}],'camera':{'tiltDeg':50,'pixelToWorld':1,'bounds':[0,0,W,H]},'art_source':'host_image'}
for f in ['park-kit-props.json','tower-props.json','overlook-access-props.json']:
 for p in json.loads((S/f).read_text()):
  B['props'][p['id']]={'image':'../'+p['image'],'sha256':p['sha256'],'size':p['size'],'anchor_px':p['anchor'],'footprint':{'shape':'rect','width':24,'depth':12,'offset':[0,-6],'basis':'world_px'},'solid':False,'occlusion_class':'tall','occupant_policy':'y_sort'}
old=json.loads((R/'assets-src/world-refinement/outdoor-bundle.json').read_text())
for key in ['rf-prod-tree','rf-prod-ginkgo','rf-polish-flowers','rf-prod-planter']:
 p=copy.deepcopy(old['props'][key]);p['image']=os.path.relpath((R/'assets-src/world-refinement'/p['image']).resolve(),P);B['props'][key]=p

def solid(x,y,w,h,why):B['collision']['solids'].append({'shape':'rect','x':x,'y':y,'w':w,'h':h,'reason':why})
def place(k,x,y,why,foot=None,depth=None):
 p=B['props'][k];B['objects'].append({'id':f'park-{len(B["objects"])+1}','prop':k,'x':x,'y':y,'sortY':y if depth is None else depth,'scale':1,'anchor_px':p['anchor_px'],'occlusion':'tall','occluder':{'source':p['image'],'alphaThreshold':128},'purpose':why})
 if foot:w,h=foot;solid(x-w/2,y-h,w,h,why)
def anchor(k,x,y,ax,ay):B['anchors'][k]={'point':[x,y],'approach':[ax,ay]};B['interactions'].append({'id':k,'x':x,'y':y,'reach':96})
# Disjoint source components preserve tower identity while pavilion doors remain human-readable.
place('kr-tower-shaft',832,536,'Original Namsan-inspired observation shaft/disc/antenna',depth=552)
place('kr-tower-pavilion',832,672,'Readable visitor pavilion, same original tower source, welcoming south steps',depth=632)
solid(664,536,336,96,'Visitor pavilion structural wall, walkable steps excluded')
solid(816,472,32,64,'Tower shaft ground support, not observation-disc bbox')
place('kr-directory',512,1168,'Signed southern travel arrival, map of fictional Namsan park',foot=(120,18))
place('kr-overlook-access',1120,816,'Walkable view terrace with actual generated south entry stairs',depth=-65)
# Painted back/side rails and front cliff have exact structural footprints; central stair is OPEN.
for q in [(1040,700,160,12),(984,736,16,48),(1240,736,16,48),(984,792,96,16),(1160,792,96,16)]:solid(*q,'Scenic terrace railing/retaining face;80pxsouth stair remains open')
place('kr-telescope',1120,744,'Public telescope; Korean landscape vocabulary viewpoint',foot=(28,18))
for x,y,why in [(448,608,'West upper hillside retaining terrace'),(352,1088,'Arrival-side wooded hillside'),(1008,480,'East tower garden rocky shoulder'),(1248,640,'Scenic lookout outer hill'),(960,928,'Lower garden grade transition')]:place('kr-cliff',x,y,why,foot=(160,24))
for x,y in [(192,256),(448,224),(640,256),(1120,256),(1216,512),(224,496),(192,736),(224,992),(448,1152),(992,1184),(1216,1120),(1248,928),(1088,480),(544,480)]:place('kr-pine',x,y,'Curated layered Korean red-pine woodland, planted roots off paths',foot=(44,20))
for k,x,y in [('rf-prod-tree',192,1184),('rf-prod-ginkgo',768,1216),('rf-prod-tree',1280,1200),('rf-prod-tree',160,512)]:place(k,x,y,'Retained native foliage at cultural-to-nature transition',foot=(24,16))
for x,y in [(352,896),(960,1152),(1216,1008)]:place('kr-rest',x,y,'Functional path rest with contemporary lamp/bench/planter',foot=(100,20))
for x,y in [(688,672),(976,672),(656,1160),(800,1160)]:place('rf-polish-flowers',x,y,'Terrace and travel arrival flowers outside entry clearance',foot=(32,16))
anchor('tower',832,656,832,688);anchor('viewpoint',1120,744,1120,784);anchor('forest',384,816,384,848);anchor('return',704,1120,704,1088);anchor('directory',512,1168,608,1168)
# Generated ground textures, authored organic semantic geometry, no code-painted terrain RGB.
material=Image.new('L',(W,H),0);d=ImageDraw.Draw(material)
for route in zone['routes']:
 pts=[tuple(p)for p in route];d.line(pts,fill=2,width=92,joint='curve')
 for x,y in pts:d.ellipse((x-46,y-46,x+46,y+46),fill=2)
d.rounded_rectangle((576,1040,864,1200),radius=48,fill=4)
d.rounded_rectangle((624,600,1040,744),radius=36,fill=4)
d.line([(832,640),(832,752)],fill=4,width=100)
d.line([(1120,928),(1120,784)],fill=4,width=80)
d.ellipse((976,688,1264,816),fill=4)
material.save(P/'semantic-materials.png')
raw=Image.open(R/'assets-src/gwanghwamun/tiles.png');tiles=[raw.crop(((i%4)*32,(i//4)*32,(i%4+1)*32,(i//4+1)*32))for i in range(8)];unique=[];lookup={}
def reg(im):
 key=im.tobytes()
 if key not in lookup:lookup[key]=len(unique);unique.append(im)
 return lookup[key]
ground,edge=terrain_layers(material,tiles,reg,output_root=P);atlas=Image.new('RGBA',(512,math.ceil(len(unique)/16)*32))
for i,im in enumerate(unique):atlas.paste(im,((i%16)*32,(i//16)*32))
atlas.save(P/'tiles.png');write(P/'tileset.json',{'schema':'generate2dmap.tileset.v1','image':'tiles.png','sha256':sha(P/'tiles.png'),'tile_size':[32,32],'columns':16,'kind':'flat','materials':['grass','park-earth','stone'],'tiles':[{'index':i,'properties':{'walkable':True}}for i in range(len(unique))],'seamless_verified':False,'art_source':'existing'})
write(P/'layers/ground.json',ground);write(P/'layers/edging.json',edge);write(P/'outdoor-draft.json',B)
print('Prepared first Namsan park',len(B['objects']),'props',len(B['collision']['solids']),'solids')
