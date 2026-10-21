"""Actual playable temporary geometry only; final source artwork must come later."""
from city_geometry import *
P=SOURCE/'map';G=SOURCE/'graybox';G.mkdir(exist_ok=True);props={};objects=[];solids=[]
mask=land_mask();ground=Image.new('RGBA',(W,H),'#224d6a');ground.paste('#668078',(0,0,W,H),mask);roads=route_mask(PLAN['roads']);ground.paste('#bec5be',(0,0,W,H),roads)
# Clear site volumes expose proportions before positioning any illustrated reused art.
for i,p in enumerate(PLAN['plots']):
 x,y=p['site'];l,t,r,b=p['artBounds'];w,h=r-l,b-t;im=Image.new('RGBA',(w,h));d=ImageDraw.Draw(im);d.rectangle((2,2,w-3,h-3),fill='#667c8b',outline='#f5db9b',width=4);d.line((2,h-24,w-3,h-24),fill='#233c4e',width=12);kind='gray-'+p['id'];path=(G/(kind+'.png')).resolve();im.save(path);props[kind]={'image':str(path),'anchor_px':[x-l,y-t],'size':[w,h],'footprint':{'shape':'rect','width':24,'depth':16,'offset':[0,-8],'basis':'world_px'},'solid':False,'occlusion_class':'tall','art_source':'code','status':'placeholder'};objects.append(object_at(kind,x,y,p['function'],props,'v9-gray-'+p['id']))
 for a,b,c,d in p['bodyRects']:solids.append(dict(shape='rect',x=a,y=b,w=c,h=d,reason='V9 new site '+p['id']+' native-art local collision template'))
# Rail safety: only one public perpendicular crossing, no frozen old geometry.
d=ImageDraw.Draw(ground);d.line((720,3584,2032,3584),fill='#344757',width=48);d.rectangle((1904,3528,1968,3640),fill='#d1b8a2')
solids.extend([{'shape':'rect','x':720,'y':3560,'w':1184,'h':48,'reason':'New railway west of designated crossing'},{'shape':'rect','x':1968,'y':3560,'w':64,'h':48,'reason':'New railway east of designated crossing'}]);solids+=water_solids(mask)
ground.paste(Image.open(ROOT/'assets-src/protected-north/ground-native.png'),(0,0));ground.save(P/'ground-native.png');mask.save(P/'walk-mask.png');write(P/'extra-props.json',props);b=bundle(objects,solids);b['art_source']='code';write(P/'draft.json',b);write(G/'disclosure.json',{'art_source':'code','purpose':'Temporary Stage C navigation geometry, not final artwork','planSha256':sha(SOURCE/'plan/city.json'),'illustratedSouthernBuildingsPositioned':False});print('Graybox authored from new plan; north literal, south temporary geometry')
