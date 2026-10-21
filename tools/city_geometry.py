"""Semantic V9 plan geometry, shared by temporary graybox and image-art assembly."""
from map_pipeline import *
from PIL import Image,ImageDraw
import math,copy
PLAN=json.loads((SOURCE/'plan/city.json').read_text());W,H=PLAN['world']
def curve(points,smooth=False,spacing=8):
 if not smooth:return [tuple(p)for p in points]
 # Centripetal-like local cubic, no image tracing. Limited overshoot checked against terrain.
 out=[];ps=[points[0]]+points+[points[-1]]
 for i in range(1,len(ps)-2):
  a,b,c,d=ps[i-1:i+3];steps=max(4,math.ceil(math.dist(b,c)/spacing))
  for n in range(steps):
   t=n/steps;t2=t*t;t3=t2*t
   out.append(tuple(round(.5*((2*b[k])+(-a[k]+c[k])*t+(2*a[k]-5*b[k]+4*c[k]-d[k])*t2+(-a[k]+3*b[k]-3*c[k]+d[k])*t3))for k in [0,1]))
 out.append(tuple(points[-1]));return out
def route_mask(roads,extra=0):
 im=Image.new('L',(W,H));d=ImageDraw.Draw(im)
 for r in roads:
  pts=curve(r['points'],r.get('smooth',False));width=r['width']+extra;d.line(pts,fill=255,width=width,joint='curve')
  for x,y in [pts[0],pts[-1]]:d.ellipse((x-width//2,y-width//2,x+width//2,y+width//2),fill=255)
 return im

def land_mask():
 im=Image.new('L',(W,H));d=ImageDraw.Draw(im);d.rectangle((0,0,W,2239),fill=255)
 d.polygon([tuple(p)for p in PLAN['mainland']],fill=255);d.polygon([tuple(p)for p in PLAN['island']],fill=255)
 # Individual narrow transport decks; there is no mainland-island bridge.
 d.rectangle((2512,4696,2608,4928),fill=255);d.rectangle((2016,5248,2112,5528),fill=255)
 return im

def water_solids(mask,cell=16):
 # Exact declared 16px transport shoreline mask, horizontal runs merged vertically.
 pix=mask.load();rows={};out=[]
 for y in range(2240,H,cell):
  runs=[];start=None
  for x in range(0,W+cell,cell):
   blocked=x<W and pix[min(W-1,x+cell//2),min(H-1,y+cell//2)]==0
   if blocked and start is None:start=x
   if not blocked and start is not None:runs.append((start,x-start));start=None
  active={}
  for key in runs:
   if key in rows:rect=rows.pop(key);rect['h']+=cell
   else:rect={'shape':'rect','x':key[0],'y':y,'w':key[1],'h':cell,'reason':'V9 new coastline: water is not walkable'}
   active[key]=rect
  out.extend(rows.values());rows=active
 out.extend(rows.values());return out

def object_at(kind,x,y,purpose,props,id):
 p=props[kind];return {'id':id,'prop':kind,'x':x,'y':y,'sortY':y,'scale':1,'anchor_px':p['anchor_px'],'occlusion':'tall','occluder':{'source':p['image'],'alphaThreshold':128},'purpose':purpose}

def bundle(objects,solids):
 n=json.loads((ROOT/'assets-src/protected-north/district.json').read_text());b=json.loads((SOURCE/'map/draft.json').read_text());b.update(name='Korean Arena — V9 new southern world candidate',world={'width':W,'height':H,'unit':'px'},objects=n['objects']+objects)
 b['collision'].update(solids=n['solids']+solids,walkRegions=[{'polygon':[[0,0],[W,0],[W,H],[0,H]]}]);b['camera']['bounds']=[0,0,W,H]
 b['spawns']=n['spawns']+[{'id':'ferry-mainland','x':PLAN['travel']['mainlandArrival'][0],'y':PLAN['travel']['mainlandArrival'][1],'facing':'north'},{'id':'ferry-jeju','x':PLAN['travel']['islandArrival'][0],'y':PLAN['travel']['islandArrival'][1],'facing':'south'}]
 b['anchors']=dict(n['anchors']);b['interactions']=[{'id':s['id'],'x':s['x'],'y':s['y'],'reach':104}for s in n['stops']]
 for p in PLAN['plots']:
  b['anchors'][p['id']]={'point':p['entrance'],'approach':p['entrance']};b['interactions'].append({'id':p['id'],'x':p['entrance'][0],'y':p['entrance'][1],'reach':96})
 # Real runtime transport is intentional and tested both ways. Independent arrival spawns seed island nav.
 b['portals']=[q for q in b['portals']if q['id']=='academy']
 write(SOURCE/'travel.json',PLAN['travel']);write(SOURCE/'regions.json',[{'id':'heritage','bounds':[0,0,4352,2240],'ambient':[2176,1120]}]+[dict(id=d['id'],bounds=d['bounds'],ambient=[(d['bounds'][0]+d['bounds'][2])//2,(d['bounds'][1]+d['bounds'][3])//2])for d in PLAN['districts']])
 labels={'bookshop':'책방 · Hiệu sách','library':'서재 · Nhà đọc ở ngưỡng phố','neighborhood-service':'안내 · Nhà thông tin','cafe':'카페 · Quán cà phê','tower':'전망대 · Đài quan sát','garden-pavilion':'쉼터 · Đình nghỉ','station':'기차역 · Nhà ga','transit-shelter':'정류장 · Trạm xe','coastal-cafe':'바다 카페 · Cà phê biển','lookout':'바다 · Ngắm biển','wheel':'관람차 · Vòng quay','carousel':'회전목마 · Đu quay','visitor':'안내소 · Quầy thông tin','discovery-hall':'문화관 · Nhà văn hóa','campus-entry':'입구 · Cổng công viên','ferry-terminal':'선착장 · Bến phà','oreum':'오름 · Đồi núi lửa','village':'마을 · Làng Jeju','nature-center':'자연 · Nhà thiên nhiên','cliff-lookout':'절벽 · Mỏm đá','basalt-learning':'현무암 · Đá basalt','corner-grocery':'가게 · Tạp hóa','bakery':'빵집 · Tiệm bánh','language-center':'배움 · Lớp cộng đồng','design-gallery':'공방 · Gallery gốm'}
 stops=n['stops']+[{'id':p['id'],'x':p['entrance'][0],'y':p['entrance'][1],'text':labels[p['id']]+'. Điểm gặp gỡ và khám phá từ vựng Hàn Quốc. Theo phố lát để đến ga, công viên và bến phà.'}for p in PLAN['plots']]
 write(SOURCE/'stops.json',stops);return b
