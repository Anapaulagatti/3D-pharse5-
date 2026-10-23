"""Shared native materials + original landmark assets over immutable approved foundation.
No resize of runtime/source artwork. New production namespace only; no historical writes.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,copy,math
from scipy.ndimage import distance_transform_edt
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate3/full-world';O=R/'public/assets/gate3/production';O.mkdir(exist_ok=True);D=R/'docs/gate3-world';D.mkdir(exist_ok=True)
def read(p):return json.loads((R/p).read_text())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
p=read('assets-src/gate3/production-plan-v3.1-restored.json')['plan'];base=read('public/assets/gate3/registration-working-v3/manifest.json');W,H=p['size'];rng=np.random.default_rng(20261023)
# Every material is cut from new host art at native size. Shared global phase avoids chunk seams.
mat=Image.open(S/'materials-host.png').convert('RGBA');tiles={name:mat.crop(box)for name,box in {'grass':(24,92,272,340),'stone':(280,92,524,340),'pavement':(532,92,764,340),'asphalt':(772,92,1010,340),'gravel':(1020,92,1260,340),'wood':(1270,92,1510,340)}.items()}
def tiled(tile):
 a=np.array(tile);return Image.fromarray(a[np.arange(H)[:,None]%a.shape[0],np.arange(W)[None,:]%a.shape[1]])
# The existing Jeju water supplies compatible native sea pixels, without scaling its scenery.
sea=Image.open(R/'public/assets/gate2/c/ground.png').crop((0,0,128,128)).convert('RGBA');ground=tiled(sea);land=Image.new('L',(W,H));ld=ImageDraw.Draw(land)
for x,y,w,h in p['land']:ld.rectangle((x,y,x+w-1,y+h-1),fill=255)
ground.paste(tiled(tiles['grass']),(0,0),land)
# Fine native shore edging is derived from the unchanged reservation, never new quay land.
landA=np.array(land)>0;dist=distance_transform_edt(landA);edge=(dist>0)&(dist<12);shore=Image.fromarray(edge.astype('uint8')*255);ground.paste(tiled(tiles['gravel']),(0,0),shore)
# Courtyard and civic ground ownership designed in a common global phase.
patches=[('stone',(1110,200,2910,1065)),('stone',(420,1070,1700,1600)),('stone',(2280,1090,2980,1640)),('pavement',(420,2030,1870,2760)),('pavement',(2230,2090,3020,2790)),('gravel',(2160,2790,3140,3340)),('pavement',(330,3360,3030,3880))]
for name,box in patches:
 mask=Image.new('L',(W,H));ImageDraw.Draw(mask).rectangle(box,fill=255);mask=Image.fromarray(np.minimum(np.array(mask),np.array(land)));ground.paste(tiled(tiles[name]),(0,0),mask)
routeMask=Image.new('L',(W,H));rd=ImageDraw.Draw(routeMask)
for path in p['paths']:
 if path['id'].startswith('jeju'):continue
 pts=[tuple(v)for v in path['points']];kind='asphalt'if path['kind']in ['main','secondary']and not path['id'].startswith('island')else'stone'if path['kind']in ['heritage','transition']else'gravel';border=Image.new('L',(W,H));bd=ImageDraw.Draw(border);bd.line(pts,fill=255,width=path['width']+14,joint='curve');border=Image.fromarray(np.minimum(np.array(border),np.array(land)));ground.paste(tiled(tiles['pavement']),(0,0),border);mask=Image.new('L',(W,H));ImageDraw.Draw(mask).line(pts,fill=255,width=path['width'],joint='curve');mask=Image.fromarray(np.minimum(np.array(mask),np.array(land)));ground.paste(tiled(tiles[kind]),(0,0),mask);rd.line(pts,fill=255,width=path['width']+70,joint='curve')
# Discrete native road markings on shared asphalt; protected station patch is reinserted later.
gd=ImageDraw.Draw(ground)
for y in range(2130,3790,74):gd.rectangle((2046,y,2049,y+34),fill='#ddd3a6')
for x in range(480,2950,80):gd.rectangle((x,2688,x+38,2691),fill='#ddd3a6')
for cy in [2140,2690,3260,3480,3790]:
 for y in range(cy-36,cy+37,18):gd.rectangle((1980,y,2115,y+7),fill='#e5e0cc')
# Fixed rail reservations; collision stays inherited, no operational trains.
for tr in p['station']['tracks']:
 pts=[tuple(v)for v in tr['points']];gd.line(pts,fill='#696b64',width=48,joint='curve')
 for a,b in zip(pts,pts[1:]):
  dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy)
  for t in np.arange(0,length,16):
   x,y=a[0]+dx*t/length,a[1]+dy*t/length;nx,ny=-dy/length*22,dx/length*22;gd.line((round(x-nx),round(y-ny),round(x+nx),round(y+ny)),fill='#4b3d31',width=5)
  for side in [-1,1]:
   nx,ny=-dy/length*12*side,dx/length*12*side;gd.line((round(a[0]+nx),round(a[1]+ny),round(b[0]+nx),round(b[1]+ny)),fill='#d0c8ac',width=3)
for platform in p['station']['platforms']:
 x,y,w,h=platform['rect'];mask=Image.new('L',(W,H));ImageDraw.Draw(mask).rectangle((x,y,x+w-1,y+h-1),fill=255);ground.paste(tiled(tiles['pavement']),(0,0),mask);ImageDraw.Draw(ground).rectangle((x+w-10,y,x+w-6,y+h-1),fill='#d9b341')
# Bridge and boarding jetties stay at existing coordinates. No ferry operation.
for box in [(3040,3412,3180,3525),(2496,3940,2624,4160),(3150,3956,3180,4084)]:
 mask=Image.new('L',(W,H));ImageDraw.Draw(mask).rectangle(box,fill=255);ground.paste(tiled(tiles['wood']),(0,0),mask)
# Preserve approved painted historical/Jeju source areas exactly. Foregrounds remain independent.
for source,origin in [('a/ground.png',(640,650)),('c/ground.png',(3180,3200))]:ground.paste(Image.open(R/'public/assets/gate2'/source).convert('RGBA'),origin)
floor=Image.open(R/'assets-src/gate3/forecourt-restoration/restored-ground.png').convert('RGBA');ground.paste(floor,(2274,2603))
# Exact baseline collision, including station strip and Jeju mask; independent new objects add local feet only.
walk=np.zeros((H,W),np.uint8)
for c in base['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];walk[y:y+h,x:x+w]=np.frombuffer((R/'public'/c['mask']).read_bytes(),np.uint8).reshape(h,w)
objects=copy.deepcopy(base['objects']);solids=copy.deepcopy(base['logicalSolids']);new=read('assets-src/gate3/full-world/extracted-assets.json');placements=[];conflicts=[]
# Native art has independent visual envelope and ground contact. No scaling to force a reservation.
specs={'archive':([2360,840,400,180],1020),'culture':([2390,1170,460,260],1430),'market':([520,3420,780,240],3660),'ferry':([2330,3550,460,190],3740),'tower':([1080,3000,240,240],3240),'carousel':([2220,2890,390,260],3150),'wheel':([2630,2880,400,280],3160),'palace':([1510,290,1050,460],750)}
for name,(foot,root)in specs.items():
 a=new['buildings'][name];im=Image.open(R/'public'/a['image']).convert('RGBA');w,h=im.size;x=round(foot[0]+foot[2]/2-w/2);y=root-h
 # Approved lower palace fragment owns its pixels; only missing upper extension is new.
 if name=='palace':
  pix=np.array(im);worldY=np.arange(h)+y;worldX=np.arange(w)+x;protected=(worldY[:,None]>=650)&(worldY[:,None]<1674)&(worldX[None,:]>=640)&(worldX[None,:]<2176);pix[protected]=0;im=Image.fromarray(pix);im.save(O/'palace-upper-owned.png',optimize=True);image='assets/gate3/production/palace-upper-owned.png'
 else:image=a['image']
 # Do not overwrite protected station artwork/forecourt with new tall attraction projections.
 protectedStation=(2274,2196,3040,2813)
 intersects=lambda b,c:b[0]<c[2]and b[2]>c[0]and b[1]<c[3]and b[3]>c[1]
 hit=name in ['wheel','carousel']and intersects((x,y,x+w,y+h),protectedStation)
 if hit:
  conflicts.append({'id':name,'nativeEnvelope':[x,y,w,h],'groundReservation':foot,'status':'ACTIVE_NATIVE_VISUAL_PROJECTION_REVIEW / GROUND_FOOTPRINT_UNCHANGED','action':'Foreground depth/occlusion prototype only. No source overwrite, shrink or reservation move. Review station visibility and Juni readability during G3-D; not final spatial/art approval.'})
 ob={'id':'production/'+name,'image':image,'x':x,'y':y,'width':w,'height':h,'sortY':root,'alphaSoftening':.65,'bytes':w*h*4};objects.append(ob);placements.append({'id':name,'active':True,'nativeEnvelope':[x,y,w,h],'groundReservation':foot,'source':a})
# New trees provide varied regional rhythm. Avoid approved scene footprints and every route/entrance/structure.
avoid=np.array(routeMask)>0
for xx,yy,ww,hh in [(640,650,1536,1024),(3180,3200,1024,1536),(2274,2196,766,617)]+[tuple(b['rect'])for b in p['buildings']]+[tuple(b['rect'])for b in p['boundaries']]:avoid[max(0,yy-50):min(H,yy+hh+50),max(0,xx-50):min(W,xx+ww+50)]=True
visualProtected=[(o['x'],o['y'],o['x']+o['width'],o['y']+o['height'])for o in objects]+[(640,650,2176,1674),(3180,3200,4204,4736),(2274,2196,3040,2813)]
placed=[]
for gy in range(350,3840,190):
 for gx in range(340,3080,210):
  x=int(gx+rng.integers(-60,61));y=int(gy+rng.integers(-50,51));t=new['trees'][int(rng.integers(len(new['trees'])))];w,h=t['size'];left=x-w//2;top=y-h+12
  if left<170 or top<90 or x+w//2>=3150:continue
  if np.any(avoid[y-15:y+25,x-22:x+23]):continue
  if any(left<b[2] and left+w>b[0] and top<b[3] and y+12>b[1] for b in visualProtected):continue
  if not landA[y,x]:continue
  ob={'id':f'production/tree-{len(placed):03d}','image':t['image'],'x':left,'y':top,'width':w,'height':h,'sortY':y,'alphaSoftening':.65,'bytes':w*h*4};objects.append(ob);placed.append({'x':x,'y':y,'tree':t['id']});walk[y-8:y+10,x-13:x+14]=0;avoid[y-60:y+60,x-70:x+70]=True
# Small shared street furniture at intentionally spaced public rest nodes.
furniture=[]
for i,(x,y) in enumerate([(1850,1850),(2190,1940),(1910,2860),(1830,3370),(1510,3670),(2130,3850),(980,2880),(2750,3330)]):
 for kind,dx,dy in [('bench-front',0,0),('light',112,-142)]:
  image='assets/gate2/b/prop-'+kind+'.png';im=Image.open(R/'public'/image);w,h=im.size;xx,yy=x+dx,y+dy
  if any(xx<b[2] and xx+w>b[0] and yy<b[3] and yy+h>b[1]for b in visualProtected):continue
  root=yy+h
  if np.any(np.array(routeMask)[root-6:root+4,xx+w//2-15:xx+w//2+16]):continue
  objects.append({'id':f'production/rest-{i}-{kind}','image':image,'x':xx,'y':yy,'width':w,'height':h,'sortY':root,'alphaSoftening':.65,'bytes':w*h*4});furniture.append({'image':image,'world':[xx,yy]});walk[root-6:root+4,xx+w//2-15:xx+w//2+16]=0
# No modifications to canonical forecourt or station collision ownership.
assert ground.crop((2274,2603,2958,2813)).tobytes()==floor.tobytes()
baselineField=np.zeros((H,W),np.uint8)
for c in base['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];baselineField[y:y+h,x:x+w]=np.frombuffer((R/'public'/c['mask']).read_bytes(),np.uint8).reshape(h,w)
assert np.array_equal(walk[2196:2813,2274:2958],baselineField[2196:2813,2274:2958]);assert np.all(walk[2626:2755,2950:2958]==0)
chunks=[]
for y in range(0,H,512):
 for x in range(0,W,512):
  w,h=min(512,W-x),min(512,H-y);id=f'{x//512}-{y//512}';im=O/(id+'.png');ground.crop((x,y,x+w,y+h)).save(im,optimize=True);mask=O/(id+'.bin');mask.write_bytes(walk[y:y+h,x:x+w].tobytes());chunks.append({'id':id,'x':x,'y':y,'width':w,'height':h,'image':str(im.relative_to(R/'public')),'mask':str(mask.relative_to(R/'public')),'bytes':w*h*5,'sha256':sha(im),'maskSha256':sha(mask)})
entries={'palace':[2048,990],'academy':[800,1500],'archive':[2320,1110],'culture':[2610,1550],'transition':[2048,1900],'retail':[1128,2690],'station':[2598.5,2760],'platform':[2980,2690],'namsan':[1460,3260],'maru':[326,3380],'amusement':[2440,3260],'market':[1440,3740],'waterfront':[2048,3790],'ferry':[2900,3480],'jeju':[3500,4055],'oreum':[3730,3335],'house':[3590,4390]}
frames={'palace':[2035,550],'academy':[1350,1200],'archive':[2560,850],'culture':[2620,1250],'transition':[2048,1900],'retail':[1128,2360],'station':[2598.5,2460],'platform':[2970,2450],'namsan':[1200,2920],'maru':[500,3120],'amusement':[2660,3060],'market':[950,3470],'waterfront':[2048,3700],'ferry':[2600,3540],'jeju':[3690,4030],'oreum':[3840,3460],'house':[3610,4300]}
targets=copy.deepcopy(base['targets'])+[{'id':'production/'+b['id'],'x':b['entry'][0],'y':b['entry'][1],'label':b['label']}for b in p['buildings']if b['id']not in ['civic','cafe','books','convenience']]+[{'id':a['id'],'x':a['point'][0],'y':a['point'][1],'label':a['label']}for a in p['accessNodes']]
stops=[{'id':k,'label':label,'x':frames[k][0],'y':frames[k][1],'zoom':.5,'travelMs':1800,'holdMs':2300}for k,label in [('palace','Palace · heritage'),('transition','Garden threshold'),('retail','Modern Korean street'),('station','Hanbit Station'),('namsan','Namsan · southwest'),('amusement','Southeast attraction reservations'),('market','Harbor market'),('oreum','Jeju · volcanic oreum'),('jeju','Jeju · orchard'),('house','Jeju · cultural house')]]
overview=ground.copy()
for o in sorted(objects,key=lambda o:o['sortY']):overview.alpha_composite(Image.open(R/'public'/o['image']).convert('RGBA'),(o['x'],o['y']))
overview.save(D/'world-composite-native.png',optimize=True);overview.thumbnail((870,973),Image.Resampling.NEAREST);overview.save(O/'overview.png',optimize=True)
m=copy.deepcopy(base);m.update(id='production',chunks=chunks,objects=objects,logicalSolids=solids,targets=targets,spawn=[2048,1900],reviewEntries=entries,nativeFrames=frames,stops=stops,overview='assets/gate3/production/overview.png',workingPlan='assets-src/gate3/production-plan-v3.1-restored.json',artStatus='G3-B/C full-world prototype / mixed approved and new art; blocked allocations and consolidated QA remain; NOT final acceptance',regions=[{'scene':z['id'],'rect':z['rect'],'status':'See coverage matrix; no blanket completion claim'}for z in p['zones']]);write(O/'manifest.json',m);write(S/'integration-provenance.json',{'generator':'tools/g3bc_build_world.py','nativeResampling':'NONE','newMaterialsSource':'materials-host.png','sharedGlobalMaterialPhase':True,'historicalSceneExact':True,'jejuSceneExact':True,'canonicalForecourtExact':True,'legacyStationMaskExact':True,'newLandAllocated':False,'bakery':'REQUIRED / UNPLACED','newPlacements':placements,'conflicts':conflicts,'newTrees':placed,'nativeReusedFurniture':furniture,'protectedFoundationManifestUnchanged':sha(R/'public/assets/gate3/registration-working-v3/manifest.json')==read('assets-src/gate3/full-world/foundation-lock.json')['sha256']['public/assets/gate3/registration-working-v3/manifest.json']});print('Full-world prototype:',len(chunks),'chunks,',len(objects),'foregrounds;',len(conflicts),'explicit projection conflicts')
