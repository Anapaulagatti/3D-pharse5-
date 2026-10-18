"""Final authored world using original/approved literal textures and props. Data/masks are geometry, not code-painted art."""
from v3_final_art import *
from PIL import ImageDraw,ImageFilter
import copy,math,numpy as np
from scipy.ndimage import distance_transform_edt
P=S/'map';P.mkdir(exist_ok=True);(P/'layers').mkdir(exist_ok=True);W,H=4352,4800;COLS,ROWS=W//32,H//32
OLD=R/'assets-src/full-world/map';old=json.loads((OLD/'outdoor-bundle.json').read_text());B=copy.deepcopy(old);B.update(id='v3-korea',name='Korean Arena V3 — Heritage to Contemporary Korea')
for p in B['props'].values():p['image']=os.path.relpath((OLD/p['image']).resolve(),P)
for o in B['objects']:o['occluder']['source']=B['props'][o['prop']]['image']
newmeta={m['id']:m for m in json.loads((S/'props.json').read_text())}
for key,m in newmeta.items():B['props'][key]={'image':os.path.relpath((S/m['image']).resolve(),P),'sha256':m['sha256'],'size':m['size'],'anchor_px':m['anchor'],'solid':False,'footprint':{'shape':'rect','width':16,'depth':8,'offset':[0,-4],'basis':'world_px'},'occlusion_class':'tall','occupant_policy':'y_sort','art_source':'host_image'}
B['tilesets']=[{'id':'town','manifest':'tileset.json'}]
for layer in B['layers']:
 if layer.get('kind')=='tiles':layer['data']='layers/'+('ground.json'if layer['name']=='Ground'else'edging.json');layer.pop('sha256',None)
removed=[];kept=[]
for o in B['objects']:
 remove=False
 if o['id'].startswith('namsan-') and o['prop']in ['kr-tower-shaft','kr-tower-pavilion','kr-overlook-access','kr-telescope','kr-directory','kr-rest']:remove=True
 if o['id'].startswith('full-')and(o['y']>=2400 or o['purpose'].startswith('Authored clustered woodland')):remove=True
 if o['id'].startswith('heritage-')and o['prop']=='kr-directory':remove=True
 if remove:removed.append(o);continue
 if o['prop']=='fw-bookstore':o['x']=1760;o['y']=2280;o['sortY']=2280;o['purpose']='Relocated retained brick bookshop, dedicated cultural frontage away from museum roof/exhibits'
 if o['id'].startswith('heritage-')and o['prop']=='kr-rest':o['x']=1472;o['y']=2320;o['sortY']=2320;o['purpose']='Retained travel rest moved to sheltered cultural/woodland pocket, away from bookshop'
 kept.append(o)
B['objects']=kept
solids=[]
for q in old['collision']['solids']:
 reason=q.get('reason','');keep=reason.startswith('heritage:')or reason.startswith('namsan:')or reason.startswith(('Royal west','Royal garden','Academy outdoor','Workshop measuring','Museum maritime'))
 if reason.startswith('namsan:')and any(k in reason for k in ['Visitor pavilion','Tower shaft','Signed southern','Scenic terrace','Public telescope','Functional path rest']):keep=False
 if reason.startswith('heritage:')and any(k in reason for k in ['Contemporary wayfinding','Modern travel-garden rest']):keep=False
 if keep:solids.append(copy.deepcopy(q))
B['collision']['solids']=solids;B['collision']['rects']=[]
def solid(x,y,w,h,why):B['collision']['solids'].append({'shape':'rect','x':x,'y':y,'w':w,'h':h,'reason':'V3: '+why})
def place(k,x,y,why,foot=None,depth=None):
 a=B['props'][k];o={'id':f'v3-{len(B["objects"]):03}','prop':k,'x':x,'y':y,'sortY':y if depth is None else depth,'scale':1,'anchor_px':a['anchor_px'],'occlusion':'tall','occluder':{'source':a['image'],'alphaThreshold':128},'purpose':why};B['objects'].append(o)
 if foot:solid(x-foot[0]/2,y-foot[1],*foot,why)
 return o
# Targeted red-defect repair: approved shop survives in a separate accessible block.
solid(1644,2232,232,48,'Relocated brick bookshop rear wall; broad front apron remains open')
solid(1422,2300,100,20,'Retained cultural trail rest, off main route')
place('v3-wayfinding',2384,2144,'Contemporary route totem replaces small gabled sign at modern transition',(40,12))
place('v3-urban-hub',2560,2688,'Contemporary glass/concrete book-and-transit hub in its own street block',(336,64))
place('v3-bus-stop',2184,2544,'Urban gateway route shelter; waiting bay separated from through movement',(176,24))
place('v3-urban-bench',2752,2752,'Urban hub public rest pocket',(150,20))
# Namsan: authentic tall observation silhouette, steel/glass lobby and elevated open-front terrace.
place('v3-tower',832,2912,'Modern broadcasting observation tower with glazed public lobby',(320,64))
# Tower mass is above its public stairs, not at the front stair foot.
B['collision']['solids'][-1].update(y=2784,h=80)
place('v3-terrace',1120,3104,'Elevated concrete viewing terrace with accessible front stairs',depth=-65)
for q in [(952,2980,16,96),(1272,2980,16,96),(976,2956,288,12),(960,3072,112,16),(1168,3072,112,16)]:solid(*q,'Modern lookout rear/sides/retaining face;96pxcentral stairs clear')
place('v3-trail-pavilion',352,3360,'Modern nature information pavilion at shaded trail junction',(216,48))
place('v3-trail-sign',512,3408,'Contemporary Namsan route marker',(44,16))
for x,y in [(288,3136),(960,3392),(1216,3280)]:place('v3-urban-bench',x,y,'Purposeful modern woodland rest',(128,20))
for x,y in [(1056,2784),(192,2800),(1280,3008),(576,3264)]:place('v3-streetlight-short',x,y,'Modern hill path lighting',(12,12))
# Bora Bloom has linked attraction plazas, a true open entrance, social bays and a new science/creative hall.
place('v3-bloom-entry',3712,3200,'Bora Bloom modern open ticket entrance')
for q in [(3504,3152,120,48),(3800,3152,120,48)]:solid(*q,'Entrance side ticket pods; central pedestrian opening stays clear')
place('v3-wheel',3392,2744,'Contemporary observation wheel with glazed capsules',(272,64))
place('v3-carousel',4000,2784,'Coordinated tensile-petal carousel',(288,64))
place('v3-discovery-hall',4144,3056,'Glass and steel creative discovery hall with greenhouse dome',(300,64))
place('v3-kiosk',3712,2400,'Contemporary park refreshment kiosk at northern social plaza',(160,40))
for x,y in [(3264,3008),(3944,2456)]:place('v3-queue-garden',x,y,'Designed queue/rest bay outside circulation',(136,20))
for x,y in [(3120,2368),(4160,2432),(3200,3392),(4208,3280),(3440,2352)]:place('rf-prod-tree',x,y,'Curated park shade around attraction courts',(24,16))
for x,y in [(3488,3096),(3920,3256),(4208,2904),(3776,2472)]:place('v3-streetlight-tall',x,y,'Modern park pedestrian lighting',(12,12))
for x,y in [(3120,2928),(4224,3248),(3472,3400)]:place('fw-flower-bed',x,y,'Planned flower border beside leisure walkway',(96,16))
# Coast: modern station/trains/cafe, logical rail continuity, one public crossing and new material language.
place('v3-station',1792,2752,'Modern low glazed coastal station and broad accessible entry',(384,64))
place('fw-rail-run',2320,2920,'Retained continuous scenic railway strip on land',depth=-77)
place('fw-crossing',2048,2920,'Purposeful timber crossing separates people from rail',depth=-76)
place('fw-platform-run',2320,3008,'Continuous engineered station platform and retaining face',depth=-75)
place('v3-platform-stairs',2048,3032,'Real front access stair joins public crossing to promenade',depth=-74)
solid(1664,2980,320,28,'Station platform retaining face west of actual stair')
solid(2112,2980,864,28,'Station platform retaining face east of actual stair')
place('v3-train',2640,2912,'Contemporary sightseeing carriage, wheels aligned to horizontal railway',(336,48))
solid(1664,2860,352,48,'Rail north barrier west of crossing');solid(2080,2860,896,48,'Rail north barrier east of crossing')
place('v3-coastal-cafe',1568,3168,'Contemporary sea-view cafe on western promenade pocket',(272,64))
place('v3-ferry-terminal',2848,3088,'Modern ferry waiting terminal at seaside public square',(256,48))
place('fw-jetty',2848,3232,'Coastal ferry pier with land approach',depth=-68)
place('fw-ferry',2848,3376,'Passenger ferry offshore; explicit public-confirmed travel, no walking on sea')
place('v3-modern-bridge',2384,3232,'Open modern steel/glass bridge over real inlet',depth=-69)
for q in [(2336,3056,96,72),(2336,3192,96,72),(2336,3128,96,8),(2336,3184,96,8)]:solid(*q,'Inlet water / north-south bridge safety edge, one clear crossing')
for x,y in [(1856,3288),(1280,3392),(2656,3264)]:place('v3-urban-bench',x,y,'Modern sea-view promenade seating',(144,20))
for x,y in [(1704,3056),(2256,3088),(2736,3088),(3008,3216)]:place('v3-streetlight-tall',x,y,'Contemporary coastal pedestrian light',(12,12))
for x,y in [(1472,3328),(3072,3376),(1248,3560),(4000,3488)]:place('v3-coastal-rocks',x,y,'Organic coastal outcrop merges headland, soil and water',(112,24))
# Accessible contemporary viewing deck: front stairs from the public promenade, rear platform lane stays separate.
place('v3-seawall',2112,3184,'Modern coastal viewing deck with true south-facing accessible stairs',depth=-70)
for q in [(1952,3152,120,32),(2160,3152,112,32),(1968,3072,296,8),(1952,3080,16,72),(2256,3080,16,72)]:solid(*q,'Coastal deck retaining wings / rear/sides;80pxfront stairs remain open')
for x,y in [(1600,3296),(2528,3280),(2992,3280)]:place('v3-glass-rail',x,y,'Engineered coastal safety edge following shore',(144,8))
for x,y in [(1032,2160),(3360,2024),(1216,2512),(3168,2392),(1336,3488),(4240,3360)]:place('v3-rock-garden',x,y,'Layered native shrub/granite edge; terrain mask itself already joins',(64,16))
# Windstone: a genuine destination loop, volcanic focal point, cultural court, modern nature centre and accessible lookout.
place('v3-oreum',2240,4100,'Oreum volcanic focal point, protected cliff face',(400,100))
place('v3-jeju-court',1830,4440,'Jeju thatch/basalt cultural courtyard; south gate is actually open',depth=4330)
place('v3-jeju-court-front',1830,4440,'Separate foreground walls and door leaves; central courtyard never hides Juni',depth=4440)
for q in [(1670,4296,320,32),(1640,4340,24,96),(2000,4340,24,96),(1664,4408,120,24),(1904,4408,104,24)]:solid(*q,'Jeju courtyard back buildings / low walls,120pxgate and yard remain walkable')
place('v3-nature-centre',2464,4472,'Contemporary basalt/glass nature learning centre',(320,64))
place('v3-cliff-lookout',2736,4256,'Dramatic basalt coastal lookout with left land approach',depth=4000)
for q in [(2624,4080,256,176),(2696,3976,160,12),(2840,3988,16,80)]:solid(*q,'Jeju lookout cliff face / safety edge; left-side platform approach remains open')
place('v3-basalt-discovery',2144,4560,'Original three-rock cultural discovery display',(128,24))
place('v3-jeju-gate',1760,4688,'Basalt/guardian ferry arrival gateway with open middle')
for q in [(1648,4664,64,24),(1816,4664,64,24)]:solid(*q,'Island arrival gateway sides; central return approach stays clear')
place('fw-guardian',1664,4528,'Retained original basalt guardian in village garden',(40,20))
place('fw-jetty',1760,4704,'Island ferry landing beyond cultural arrival gate',depth=-68)
place('fw-ferry',1760,4760,'Return passenger ferry within world bounds')
for x,y in [(1696,4080),(1888,4032),(2016,4208),(2784,4400),(2752,4624),(2240,4704),(1952,4640)]:place('fw-tangerine',x,y,'Purposeful island orchard on wind-sheltered edges',(24,16))
for x,y in [(1616,4376),(2160,4432),(2864,4464),(2768,4712),(2112,3976)]:place('fw-coastal-garden',x,y,'Windstone coastal grasses and basalt planting',(64,16))
for x,y in [(1576,4216),(1936,4160),(2584,4712),(2944,4344),(2208,4680)]:place('fw-basalt-wall',x,y,'Low Jeju wind boundary around orchard and court',(88,16))
for x,y in [(1744,4480),(2584,4544),(2592,3920)]:place('v3-wayfinding',x,y,'Contemporary island discovery wayfinding',(36,12))
# Authored routes, not a generic grid; preserve fundamental northern/park exploration geometry.
routes=copy.deepcopy(json.loads((R/'assets-src/full-world/routes.json').read_text()))
for r in routes:
 if r['id']=='entertainment0':r['points']=[[3712,3296],[3712,3120],[3456,3008],[3456,2832],[3712,2848],[4000,2864],[3920,2864],[3920,3096],[4144,3096],[4144,3136],[4144,3096],[3712,3096],[3712,3120]]
 if r['id']=='busan-coast1':r['points']=[[1792,3040],[2048,3040],[2304,3040],[2304,3160]]
 if r['id']=='busan-coast0':r['points']=[[1792,3024],[1792,3224],[2304,3224],[2304,3160]]
 if r['id']=='jeju0':r['points']=[[1760,4544],[1952,4480],[2080,4480],[2080,4256],[2240,4144],[2528,4160],[2528,4320],[2752,4432],[2720,4576],[2464,4640],[2080,4608],[1760,4544]]
 if r['id']=='jeju-arrival-loop':r['points']=[[1760,4544],[1952,4480],[2080,4480],[2080,4256]]
 if r['id']=='namsan1':r['points']=[[704,3264],[928,3296],[1120,3168],[1120,3104],[1120,3024]]
extra=[('coast-bridge-link',[[2304,3160],[2464,3160],[2656,3136],[2912,3136]],48),('coastal-viewing-deck',[[2112,3208],[2112,3104]],48),('cultural-book-front',[[1760,2368],[1760,2336]],64),('urban-hub-front',[[2048,2784],[2304,2784],[2560,2784],[2560,2752]],80),('park-central-plaza',[[3712,3120],[3712,2848],[3712,2464]],80),('namsan-coast-shortcut',[[1120,3168],[1280,3232],[1408,3232],[1568,3232],[1792,3232],[1792,3136]],64),('island-court-approach',[[1952,4480],[1830,4480],[1830,4384]],48),('island-lookout',[[2528,4160],[2528,4032],[2736,4032]],48),('island-learning',[[2464,4640],[2464,4544],[2144,4608]],64)]
for name,points,width in extra:routes.append({'id':name,'zone':'v3','points':points,'clearWidth':width})
# Corresponding cultural stops remain concise game-facing content; no authoring/tool implementation text.
stops=[('hall',2176,320,'궁궐 · Cung điện. Các sân và cổng tạo thứ bậc từ không gian công cộng đến đại điện.'),('hanji',2480,384,'한지 · Giấy hanji. Từ sợi dâu đến trang sách: một vật liệu gắn với nghề thủ công Hàn Quốc.'),('royal-garden',1568,528,'정자 · Đình nghỉ. Dừng lại bên vườn, nhìn mái giwa và thưởng thức khoảng sân yên tĩnh.'),('science',2656,1472,'과학 · Khoa học. Thiên cầu và dụng cụ đo gợi những phát minh quan sát bầu trời.'),('museum',3008,2028,'역사 · Lịch sử. Các mô hình hàng hải kể chuyện kỹ nghệ đóng tàu và di sản biển.'),('bookshop',1760,2336,'서점 · Hiệu sách. 책 · Sách. Một góc đọc nhỏ nối phố học với hành trình hôm nay.'),('urban-hub',2560,2752,'도시 · Đô thị. 유리 · Kính. 콘크리트 · Bê tông. Cửa kính rộng và kết cấu thép đánh dấu nhịp sống hiện đại.'),('tower',832,2912,'전망탑 · Tháp quan sát. Đi từ rừng núi đến đài kính trên cao: một hành trình gợi Namsan.'),('terrace',1120,3024,'전망 · Tầm nhìn. Bậc thang dẫn lên sân ngắm cảnh; hãy theo lan can để nhìn lại đường rừng.'),('wheel',3392,2832,'관람차 · Vòng quay ngắm cảnh. Những cabin kính và khung thép trắng tạo điểm hẹn giữa công viên hoa.'),('carousel',4000,2864,'회전목마 · Trò quay vòng. Mái cánh hoa dẫn lối từ khu vui chơi đến vườn nghỉ và nhà khám phá.'),('creative-hall',4144,3136,'발견 · Khám phá. Nhà kính, khu vườn và những hình khối khoa học gợi trí tò mò của người khám phá.'),('park-entry',3712,3272,'입구 · Lối vào. Chọn nhánh vòng quay, vườn hoa hay nhà khám phá rồi gặp nhau ở quảng trường.'),('station',1792,2816,'역 · Nhà ga. 기차 · Tàu. Hãy dùng lối gỗ được đánh dấu để băng qua đường ray.'),('coast-viewdeck',2112,3104,'전망대 · Sàn ngắm biển. Bậc thang phía trước dẫn lên sân; lối đi ở phía nam nối quán cà phê và cầu.'),('cafe',1568,3232,'카페 · Quán cà phê. 바다 · Biển. Nghỉ dưới mái kính và nhìn mặt nước từ đường dạo.'),('bridge',2320,3160,'다리 · Cầu. Thép và kính nối hai phía lòng nước; lối đi bộ tách khỏi đường ray.'),('jeju-court',1830,4480,'초가 · Nhà mái tranh. Đá basalt, tường thấp và mái buộc dây gợi cách cư dân Jeju thích nghi với gió.'),('oreum',2240,4144,'오름 · Đồi núi lửa. 귤 · Quýt. Đá núi lửa và cây trái tạo nên bản sắc vườn Windstone.'),('lookout',2736,4032,'해안 · Bờ biển. Vách basalt đen gặp sóng xanh; từ sàn ngắm cảnh hãy nhìn đường đi ven đảo.'),('nature-centre',2464,4544,'자연 · Thiên nhiên. Tìm ba mẫu đá ở sân để khám phá dấu vết dung nham nguội.')]
write(S/'stops.json',[{'id':k,'x':x,'y':y,'text':t}for k,x,y,t in stops]);B['anchors']={};B['interactions']=[]
for k,x,y,t in stops:B['anchors'][k]={'point':[x,y],'approach':[x,y]};B['interactions'].append({'id':k,'x':x,'y':y,'reach':104})
B['portals']=[{'id':'academy','circle':[1568,1120,24],'to':'v3-reading-room:start','entranceByFrom':{'v3-reading-room':[1568,1152]},'reciprocal':True,'activation':'intent','radius':96,'travelDirection':[0,-1]},{'id':'ferry-jeju','circle':[2848,3184,28],'to':'v3-korea:jeju-arrival','reciprocal':False,'activation':'intent','radius':96,'travelDirection':[0,1]},{'id':'ferry-coast','circle':[1760,4608,28],'to':'v3-korea:coast-arrival','reciprocal':False,'activation':'intent','radius':96,'travelDirection':[0,1]}]
write(S/'routes.json',routes);write(S/'removed-candidate-instances.json',removed)
# Terrain composition follows below; all visible RGB comes from retained source images.
# One shaped mainland and one Jeju travel island; no map-chunk grass rectangles beside the ocean.
mainland=[(0,0),(W,0),(W,3344),(4000,3408),(3712,3488),(3328,3472),(3040,3312),(2832,3264),(2640,3300),(2464,3264),(2304,3264),(2240,3296),(2048,3328),(1792,3280),(1536,3300),(1432,3456),(1216,3616),(832,3616),(384,3504),(0,3392)]
island=[(1696,4064),(1856,3936),(2080,3872),(2336,3872),(2592,3872),(2864,4016),(2944,4352),(2848,4656),(2496,4736),(2048,4736),(1696,4704),(1568,4480),(1600,4224)]
land=Image.new('L',(W,H));ld=ImageDraw.Draw(land);ld.polygon(mainland,fill=255);ld.polygon(island,fill=255)
# Inlet follows the connected sea, intentionally crossed only by the bridge deck.
ld.polygon([(2336,3056),(2432,3056),(2432,3300),(2336,3300)],fill=0)
forest=Image.new('L',(W,H));fd=ImageDraw.Draw(forest)
fd.polygon([(0,0),(984,0),(1040,256),(968,544),(1080,768),(984,1056),(1104,1344),(1016,1632),(1040,1856),(968,2080),(1184,2224),(1384,2336),(1232,2480),(1024,2600),(768,2560),(416,2464),(192,2608),(224,3024),(384,3248),(688,3432),(1008,3456),(1200,3360),(1360,3352),(1376,3504),(1216,3616),(832,3616),(384,3504),(0,3392)],fill=255)
fd.polygon([(3504,0),(W,0),(W,3344),(4096,3424),(4256,3200),(4216,2912),(4280,2688),(4240,2448),(4080,2256),(3632,2304),(3408,2176),(3480,1920),(3376,1664),(3504,1408),(3408,1120),(3536,832),(3416,512)],fill=255)
# Natural small island windbreaks stay off useful loop; not a replacement for developed destinations.
for q in [(1600,4208,1752,4384),(2640,4616,2816,4728),(1856,3912,2016,4016)]:fd.ellipse(q,fill=255)
for r in routes:
 pts=[tuple(p)for p in r['points']];fd.line(pts,fill=0,width=r['clearWidth']+104,joint='curve')
 for x,y in pts:rad=(r['clearWidth']+104)//2;fd.ellipse((x-rad,y-rad,x+rad,y+rad),fill=0)
forest=np.array(forest)>0;land_a=np.array(land)>0;forest&=land_a
# Real walkable envelopes / route shoulders; geometry agrees with visible sea/forest.
walk=Image.new('L',(W,H));wd=ImageDraw.Draw(walk)
for points in [[(768,32),(3584,32),(3584,2144),(3008,2336),(2752,2420),(2176,2416),(1760,2384),(1424,2240),(768,2120)],[(96,2368),(416,2320),(768,2392),(1152,2352),(1376,2608),(1336,2800),(1344,3200),(1392,3344),(1200,3472),(864,3504),(512,3520),(192,3392),(64,3088)],[(3104,2304),(3504,2256),(3984,2240),(4296,2384),(4320,3168),(4176,3360),(3696,3424),(3248,3344),(3088,3184),(3112,2944),(3040,2768)],[(1472,2528),(1792,2464),(2240,2544),(2720,2528),(3024,2656),(3040,3152),(2936,3296),(2624,3312),(2368,3280),(2080,3344),(1712,3312),(1408,3280),(1376,3104)],[(1984,2256),(2944,2256),(3072,2672),(2816,2856),(2112,2848),(1952,2640)],island]:wd.polygon(points,fill=255)
for r in routes:
 pts=[tuple(p)for p in r['points']];wd.line(pts,fill=255,width=r['clearWidth']+80,joint='curve')
 for x,y in pts:rad=(r['clearWidth']+80)//2;wd.ellipse((x-rad,y-rad,x+rad,y+rad),fill=255)
walk_a=(np.array(walk)>0)&land_a
# Forest can have an inviting undergrowth fringe, but the dense nonwalking core is explicit.
walk_a&=~forest
# Only actual bridge deck crosses inlet; keep48pxclear and public north/south rails.
walk_a[3136:3184,2288:2480]=True
# Source material fields. All RGB below is literal retained/generated texture art.
tex={p.stem:Image.open(p).convert('RGB')for p in (S/'terrain').glob('*.png')};tex['brick']=Image.open(R/'assets-src/full-world/terrain-native/brick.png').convert('RGB')
def texture(name,box=None):
 if box is None:x,y,w,h=0,0,W,H
 else:x,y,w,h=box
 src=np.array(tex[name]);hh,ww=src.shape[:2];return Image.fromarray(src[(np.arange(y,y+h)%hh)[:,None],(np.arange(x,x+w)%ww)[None,:]])
base=texture('grass')
def overlay(mask,name,feather=0):
 arr=np.asarray(mask,dtype=bool)
 if not arr.any():return
 if feather:
  signed=distance_transform_edt(arr)-distance_transform_edt(~arr)
  # Source-informed irregular alpha, not painted RGB and not a repeated Bayer/checker dither.
  src=np.array(tex['forest'].convert('L'),dtype=np.float32);src=(src-src.mean())/max(1.,float(src.std()))
  yy=np.arange(H)%src.shape[0];xx=np.arange(W)%src.shape[1];jitter=src[yy[:,None],xx[None,:]]*3
  alpha=np.clip((signed+jitter+feather)/(2*feather),0,1);matte=Image.fromarray(np.uint8(np.rint(alpha*255)));del signed,jitter,alpha
 else:matte=Image.fromarray(np.uint8(arr)*255)
 base.paste(texture(name),(0,0),matte)
overlay(forest,'forest',24)
# Actual approved heritage court/road pixels, with narrow semantic verges instead of an entire rectangular chunk.
northmat=np.array(Image.open(R/'assets-src/living-korea/north/semantic-materials.png').convert('L'))>0
oldnorth=Image.open(R/'assets-src/living-korea/north/terrain-composite.png').convert('RGB');assert oldnorth.size==(2304,2240)
dist=distance_transform_edt(~northmat);alpha=np.uint8(np.clip((24-dist)/24,0,1)*255);base.paste(oldnorth,(1024,0),Image.fromarray(alpha));del dist,alpha
# Purposeful path/plaza masks, not large material rectangles that reveal map sections.
def blank():return Image.new('L',(W,H))
def route_mask(selected,extra=24):
 im=blank();d=ImageDraw.Draw(im)
 for r in selected:
  pts=[tuple(p)for p in r['points']];width=r['clearWidth']+extra;d.line(pts,fill=255,width=width,joint='curve')
  for x,y in pts:rad=width//2;d.ellipse((x-rad,y-rad,x+rad,y+rad),fill=255)
 return im
nature=route_mask([r for r in routes if r['zone']in ['namsan','jeju']or r['id'].startswith(('island-','namsan-coast'))]);overlay(np.array(nature)>0,'sand',16)
modern=route_mask([r for r in routes if r['zone']not in ['namsan','jeju']and not r['id'].startswith(('island-','namsan-coast'))],40);md=ImageDraw.Draw(modern)
for x,y,rx,ry in [(832,2912,240,112),(1120,3064,184,96),(3392,2784,208,128),(4000,2792,216,128),(3712,2928,224,224),(4144,3136,176,96),(3712,2464,152,96),(1792,2792,256,96),(2560,2752,232,96),(1568,3232,184,64),(2848,3168,184,96)]:md.ellipse((x-rx,y-ry,x+rx,y+ry),fill=255)
# Retained bookshop's own frontage, well separated from museum and cafe silhouettes.
md.rounded_rectangle((1584,2256,1944,2368),radius=32,fill=255)
overlay(np.array(modern)>0,'concrete',12)
park=blank();pd=ImageDraw.Draw(park)
for x,y,rx,ry in [(3392,2792,176,104),(4000,2800,176,104),(4144,3144,144,80)]:pd.ellipse((x-rx,y-ry,x+rx,y+ry),fill=255)
overlay(np.array(park)>0,'paver',8)
# Connected modern shared street: an asphalt carriage/shared lane nested in a real sidewalk envelope.
asphalt=blank();ad=ImageDraw.Draw(asphalt);street=[(2176,2328),(2176,2368),(2048,2464),(2048,2784)];ad.line(street,fill=255,width=64,joint='curve')
for x,y in street:ad.ellipse((x-32,y-32,x+32,y+32),fill=255)
overlay(np.array(asphalt)>0,'asphalt',8)
# Island court and volcanic forecourts use local materials; modern glass centre gets engineered paving.
jejum=blank();jd=ImageDraw.Draw(jejum)
for x,y,rx,ry in [(1830,4400,200,144),(2144,4560,128,64),(2240,4128,176,64)]:jd.ellipse((x-rx,y-ry,x+rx,y+ry),fill=255)
overlay(np.array(jejum)>0,'basalt',14)
jejum=blank();jd=ImageDraw.Draw(jejum);jd.rounded_rectangle((2232,4456,2680,4584),radius=32,fill=255);jd.polygon([(2504,4008),(2824,4008),(2824,4056),(2504,4056)],fill=255);overlay(np.array(jejum)>0,'paver',8)
# Water is continuous across ENTIRE world width outside the shaped land, not an inset blue rectangle.
water_a=~land_a;overlay(water_a,'deep-water')
water_dist=distance_transform_edt(water_a);xx=np.arange(W)[None,:];yy=np.arange(H)[:,None];depth=np.where(xx<1500,40,np.where(xx>3100,56,96));depth=np.where(yy>=3648,np.where(xx>2450,36,68),depth);shallow=water_a&(water_dist<depth);overlay(shallow,'shallow-water',18);del water_dist,depth,xx,yy
# Narrow sand/stone shore is geographically derived, with generated grain-informed edges.
shore=(distance_transform_edt(land_a)<24)&land_a;overlay(shore,'sand',6)
# Bridge deck art itself is separate; its open arch shows this connected inlet water beneath.
base.save(P/'terrain-composite-unquantized.png')
# Save editable geometry masks and explicit shore/route source data before finishing.
land.save(P/'land-mask.png');Image.fromarray(np.uint8(forest)*255).save(P/'forest-mask.png');Image.fromarray(np.uint8(walk_a)*255).save(P/'walk-mask.png');modern.save(P/'modern-paving-mask.png');nature.save(P/'nature-path-mask.png')
write(S/'layout.json',{'world':[W,H],'mainlandOutline':mainland,'islandOutline':island,'heritageOldPixelsKept':True,'bookshopRelocation':{'from':[2752,2256],'to':[1760,2280],'museumSourcePixelsUnchanged':True},'ferry':{'coast':[2848,3184],'island':[1760,4608],'safeArrivals':[[2848,3136],[1760,4544]],'explicit':True},'annotatedReferenceReceived':False,'naturalBoundsFromMasks':True,'fictionalGeography':True})
# Matching16pxoutside collision runs preserve actual feet/camera continuity, not blank rectangle limits.
cell=16;free=walk_a.reshape(H//cell,cell,W//cell,cell).mean(axis=(1,3))>.75
active={}
for y in range(H//cell+1):
 row=~free[y]if y<H//cell else np.zeros(W//cell,dtype=bool);runs=[];x=0
 while x<W//cell:
  if not row[x]:x+=1;continue
  a=x
  while x<W//cell and row[x]:x+=1
  runs.append((a,x))
 nxt={v:active.get(v,y)for v in runs}
 for(a,b),sy in active.items():
  if(a,b)not in nxt:solid(a*cell,sy*cell,(b-a)*cell,(y-sy)*cell,'Natural sea/forest boundary matching authored land/walk masks')
 active=nxt
# Close two4pxnavigation-grid slivers behind nonpublic shore/oreum boundaries.
solid(1584,4320,32,48,'Nonpublic shore sliver within windbreak boundary')
solid(2608,3896,24,24,'Nonpublic oreum rear-edge sliver')
# Curated edge planting follows the natural boundary, not a regular tree grid or oversized seam cover.
for k,x,y in [('kr-pine',832,480),('rf-prod-tree',1016,928),('rf-prod-ginkgo',896,1440),('kr-pine',1008,1824),('rf-prod-tree',1184,2176),('kr-pine',3520,320),('rf-prod-tree',3376,768),('rf-prod-ginkgo',3488,1216),('kr-pine',3408,1640),('rf-prod-tree',3520,2048),('rf-prod-tree',3040,2464),('kr-pine',1376,2688),('rf-prod-tree',1360,3488),('kr-pine',224,3504),('rf-prod-ginkgo',4240,3360),('rf-prod-tree',3200,3456)]:place(k,x,y,'Layered original foliage at authored terrain edge, not camouflage for a seam')
# Curated nonwalking hillside backdrop. Terrain is already continuous; never a seam-covering oversized canopy.
# Native-size art only, fixed offsets, constrained to forest >=96px from public walk envelope.
core_distance=distance_transform_edt(~walk_a)
groves=[('west-royal',416,320),('west-academy',400,848),('west-scholars',416,1392),('west-cultural',480,1904),('west-hills',560,2240),('east-royal',3904,320),('east-science',3936,848),('east-museum',3872,1376),('east-cultural',3904,1888)]
patterns=[ [(-240,-176),(-88,-224),(80,-192),(248,-128),(-256,-16),(-112,-48),(64,-40),(224,40),(-208,144),(-48,128),(128,176),(264,224),(-272,288),(-112,320),(80,336)], [(-224,-224),(-48,-192),(144,-224),(288,-112),(-272,-48),(-88,-16),(96,-48),(240,80),(-224,128),(-64,176),(112,144),(272,240),(-256,304),(-80,320),(96,320)] ]
for i,(name,cx,cy) in enumerate(groves):
 for j,(dx,dy) in enumerate(patterns[i%2]):
  x,y=cx+dx,cy+dy
  if not(128<=x<W-128 and 240<=y<2304):continue
  if forest[y,x] and core_distance[y,x]>=96:
   place(['kr-pine','rf-prod-tree','rf-prod-ginkgo','kr-pine'][j%4],x,y,'Inaccessible '+name+' woodland backdrop; natural boundary, native-size original canopy')
del core_distance
# Save draft before actual Forge finishing/export; all source paths are relative to this bundle.
write(P/'outdoor-draft.json',B);write(S/'routes.json',routes)
print(json.dumps({'draftProps':len(B['objects']),'solids':len(B['collision']['solids']),'size':[W,H],'newArtRGB':'host-image + approved assets; masks/data authored','removedInstances':len(removed)}))
