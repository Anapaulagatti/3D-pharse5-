"""Compare real native engine readbacks with untouched approved texture pixels."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3a-pixel-audit'
rows=[];proof={}
manifest=json.loads((R/'public/assets/gate3/district/manifest.json').read_text())
ground=Image.open(R/'assets-src/gate25-station-planters/final-clean-ground.png').convert('RGB');g=np.array(ground)
fgmask=Image.new('L',ground.size)
for o in manifest['objects']:
 im=Image.open(R/'public'/o['image']).convert('RGBA');a=im.getchannel('A').point(lambda v:255 if v else 0);fgmask.paste(a,(o['x'],o['y']),a)
chunks=[]
for c in manifest['chunks']:
 a=np.array(Image.open(R/'public'/c['image']).convert('RGB'));b=g[c['y']:c['y']+c['height'],c['x']:c['x']+c['width']];chunks.append({'id':c['id'],'pixels':c['width']*c['height'],'different':int(np.any(a!=b,2).sum())})
proof['runtimeChunks']=chunks
boxes={'forecourt':(2745,700,2895,750),'bakery-station-passage':(2445,500,2525,760),'lower-planting':(2170,950,2580,1040),'curb-road-sidewalk':(2150,805,2610,845),'crisp-station-facade':(2620,545,2790,640)}
for phase in ['before','after']:
 captures=json.loads((D/f'{phase}-capture.json').read_text())
 for r in captures:
  if r['name']!='native':continue
  path=D/f'{phase}-{r["renderer"]}-native{ "-backing" if phase=="after" else ""}.png'
  shot=np.array(Image.open(path).convert('RGB'));vx,vy,w,h=map(int,r['state']['camera']['worldView']);expected=g[vy:vy+h,vx:vx+w];valid=np.array(fgmask)[vy:vy+h,vx:vx+w]==0
  px,py=round(r['state']['x'])-vx,round(r['state']['y'])-vy;valid[max(0,py-112):min(h,py+16),max(0,px-55):min(w,px+56)]=False
  diff=np.max(abs(shot.astype(int)-expected.astype(int)),2)
  rows.append({'phase':phase,'renderer':r['renderer'],'area':'all visible unoccluded ground','pixels':int(valid.sum()),'different':int(((diff>0)&valid).sum()),'maxDelta':int(diff[valid].max())})
  for name,(x,y,x2,y2) in boxes.items():
   v=valid[y-vy:y2-vy,x-vx:x2-vx];d=diff[y-vy:y2-vy,x-vx:x2-vx];rows.append({'phase':phase,'renderer':r['renderer'],'area':name,'pixels':int(v.sum()),'different':int(((d>0)&v).sum()),'maxDelta':int(d[v].max())})
  original=Image.open(R/'assets-src/gate25-station-planters/expected-native-composite.png').convert('RGB')
  for name,box in [('left-planter',(2545,695,2735,782)),('right-planter',(2908,699,3098,782))]:
   x,y,x2,y2=box;a=shot[y-vy:y2-vy,x-vx:x2-vx];b=np.array(original.crop(box));d=np.max(abs(a.astype(int)-b.astype(int)),2);rows.append({'phase':phase,'renderer':r['renderer'],'area':name,'pixels':int(d.size),'different':int((d>0).sum()),'maxDelta':int(d.max())})
proof['nativeSourceComparison']=rows
movement=[]
for r in json.loads((D/'after-capture.json').read_text()):
 if r['name'] not in ['stationary','moving']:continue
 m=r['renderAudit']['camera']['matrix'];vx,vy=map(lambda v:int(-v),m[4:6]);shot=np.array(Image.open(D/f"after-{r['renderer']}-{r['name']}-backing.png").convert('RGB'));h,w=shot.shape[:2];expected=g[vy:vy+h,vx:vx+w];valid=np.array(fgmask)[vy:vy+h,vx:vx+w]==0
 px,py=round(r['state']['x'])-vx,round(r['state']['y'])-vy;valid[max(0,py-112):min(h,py+16),max(0,px-60):min(w,px+61)]=False
 diff=np.max(abs(shot.astype(int)-expected.astype(int)),2)
 movement.append({'renderer':r['renderer'],'capture':r['name'],'worldTopLeft':[vx,vy],'pixels':int(valid.sum()),'different':int(((diff>0)&valid).sum()),'maxDelta':int(diff[valid].max())})
proof['stationaryMovingSourceComparison']=movement
assert all(r['different']==0 for r in movement),movement
# Foreground readback independently checks the protected half-unit station anchor.
r=next(r for r in json.loads((D/'after-capture.json').read_text())if r['name']=='station-pivot');m=r['renderAudit']['camera']['matrix'];vx,vy=map(lambda v:int(-v),m[4:6]);shot=np.array(Image.open(D/'after-auto-station-pivot-backing.png').convert('RGB'));h,w=shot.shape[:2];claim=np.zeros((h,w),bool);actor=np.zeros((h,w),bool);px,py=round(r['state']['x'])-vx,round(r['state']['y'])-vy;actor[max(0,py-112):min(h,py+16),max(0,px-55):min(w,px+56)]=True;pivotrows=[]
for o in sorted(json.loads((R/'public/assets/gate3/registration/manifest.json').read_text())['objects'],key=lambda o:o['sortY'],reverse=True):
 x,y=o['x']-vx,o['y']-vy;src=np.array(Image.open(R/'public'/o['image']).convert('RGBA'));hh,ww=src.shape[:2];x0,y0=max(0,x),max(0,y);x1,y1=min(w,x+ww),min(h,y+hh)
 if x1<=x0 or y1<=y0:continue
 local=src[y0-y:y1-y,x0-x:x1-x];region=claim[y0:y1,x0:x1];use=(local[:,:,3]==255)&(~region)&(~actor[y0:y1,x0:x1]);diff=np.max(abs(shot[y0:y1,x0:x1].astype(int)-local[:,:,:3].astype(int)),2)
 if o['id'].startswith('registration/')and use.sum():pivotrows.append({'object':o['id'],'pixels':int(use.sum()),'different':int(((diff>0)&use).sum()),'maxDelta':int(diff[use].max())})
 region|=local[:,:,3]>0
proof['stationPivotReadback']=pivotrows
assert all(r['different']==0 for r in pivotrows),pivotrows

# Actual engine matrix, texture filters and native layer registration from POST_RENDER.
after=json.loads((D/'after-capture.json').read_text());matrixrows=[]
for r in after:
 audit=r.get('renderAudit')
 if not audit:continue
 layers=audit['layers'];m=audit['camera']['matrix'];z=audit['camera']['zoom'];native=z==1
 matrixrows.append({'renderer':r['renderer'],'capture':r['name'],'cameraZoom':z,'matrix':m,'integerCameraTranslation':all(abs(v-round(v))<1e-6 for v in m[4:6]),'integerNativeLayerOrigins':all(all(float(v).is_integer()for v in o['position'])for o in layers),'unitLayerScale':all(o['scale']==[1,1]for o in layers),'nearest':all(o['scaleMode']==1 and (o.get('minFilter',9728)==9728)and(o.get('magFilter',9728)==9728)for o in layers),'nativeScreenPhase':all(all(abs(v-round(v))<1e-6 for v in o['screenOrigin'])for o in layers)if native else 'NOT APPLICABLE: half-size discards alternate texels','layers':len(layers)})
proof['canvasDrawCalls']=[]
for phase in ['before','after']:
 r=next(r for r in json.loads((D/f'{phase}-capture.json').read_text())if r['renderer']=='canvas'and r['name']=='native');ds=r['canvasDraws'];res={'phase':phase,'uniqueImageDraws':len(ds),'resizedDraws':sum(d['sourceRect'][2:]!=d['destinationRect'][2:]for d in ds),'smoothingEnabledDraws':sum(d['smoothing']for d in ds)};proof['canvasDrawCalls'].append(res)
 if phase=='after':assert res['resizedDraws']==0 and res['smoothingEnabledDraws']==0
proof['postRenderAudit']=matrixrows
assert all(r['integerCameraTranslation'] and r['integerNativeLayerOrigins'] and r['unitLayerScale'] and r['nearest'] for r in matrixrows)
assert all(r['different']==0 for r in rows if r['phase']=='after')
proof['cssPlacement']=[{'renderer':r['renderer'],'phase':phase,'rect':r['rect'],'canvas':r['canvas'],'css':r['css'],'dpr':r['dpr'],'visualScale':r['visualScale']}for phase in ['before','after']for r in json.loads((D/f'{phase}-capture.json').read_text())if r['name']=='odd-display']
# Immutable approved inputs and historical 1341-file inventory.
inventory=json.loads((R/'docs/gate3a/protected-assets.json').read_text());
proof['protectedInventory']={'checked':len(inventory['sha256']),'mismatched':[p for p,h in inventory['sha256'].items()if hashlib.sha256((R/p).read_bytes()).hexdigest()!=h]};assert not proof['protectedInventory']['mismatched']
# Inventory format is handled below after reading its actual schema.
sourcepaths=['assets-src/gate25-reconstruction/ground-revised-host.png','assets-src/gate25-refinement/east-context-host.png','assets-src/gate25-refinement/planting-variation-host.png','assets-src/gate25-station-planters/clean-floor-host.png','assets-src/gate25-station-planters/planter-sprites-host.png','assets-src/gate25-station-planters/final-clean-ground.png']
proof['sources']=[{'file':p,'dimensions':list(Image.open(R/p).size),'sha256':hashlib.sha256((R/p).read_bytes()).hexdigest()}for p in sourcepaths]
(D/'pixel-proof.json').write_text(json.dumps(proof,indent=2)+'\n')
# Readable review boards: exact native crops; enlargement uses nearest only.
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
board=Image.new('RGB',(1110,1040),'#16202a');draw=ImageDraw.Draw(board)
for col,title in enumerate(['Approved source pixels','Before: Phaser native','After: Phaser native']):draw.text((col*370+8,8),title,font=font,fill='white')
before=Image.open(D/'before-auto-native.png').convert('RGB');afterim=Image.open(D/'after-auto-native-backing.png').convert('RGB')
for i,(name,box)in enumerate(list(boxes.items())[:4]+[('left-planter',(2545,695,2725,782))]):
 x,y,x2,y2=box;box=(x,y,min(x2,x+180),min(y2,y+80));local=(box[0]-1904,box[1]-247,box[2]-1904,box[3]-247)
 for col,im in enumerate([Image.open(R/'assets-src/gate25-station-planters/expected-native-composite.png').convert('RGB').crop(box),before.crop(local),afterim.crop(local)]):
  im.save(D/f'{name}-{["source","before","after"][col]}-1x.png');board.paste(im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST),(col*370+8,i*198+67))
 draw.text((8,i*198+40),name+' / 2x nearest review',font=font,fill='white')
board.save(D/'SOURCE_BEFORE_AFTER.png',optimize=True)
assert all(c['different']==0 for c in chunks)
print('PASS: exact native readback, motion, station pivot, 21 chunks, 1341 protected inputs')

for name in ['stationary','moving']:
 board=Image.new('RGB',(1280,480),'#16202a');d=ImageDraw.Draw(board)
 for col,phase in enumerate(['before','after']):
  path=D/f'{phase}-auto-{name}{"-backing" if phase=="after" else ""}.png';im=Image.open(path).convert('RGB');im=im.resize((640,450),Image.Resampling.NEAREST);board.paste(im,(col*640,30));d.text((col*640+8,7),phase+' / '+name+' / 50% review; full native linked in README',font=font,fill='white')
 board.save(D/(name.upper()+'_COMPARISON.png'),optimize=True)
# Canvas-specific before/after at native crop resolution, then nearest enlargement.
board=Image.new('RGB',(1080,700),'#16202a');d=ImageDraw.Draw(board)
for col,label in enumerate(['Approved source','Canvas before','Canvas after']):d.text((col*360+8,8),label,font=font,fill='white')
for i,box in enumerate([(2445,650,2615,750),(2170,950,2340,1040),(2545,695,2715,782)]):
 ims=[Image.open(R/'assets-src/gate25-station-planters/expected-native-composite.png').convert('RGB').crop(box)]
 for phase in ['before','after']:
  im=Image.open(D/f'{phase}-canvas-native{"-backing" if phase=="after" else ""}.png').convert('RGB');ims.append(im.crop((box[0]-1904,box[1]-247,box[2]-1904,box[3]-247)))
 for col,im in enumerate(ims):board.paste(im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST),(col*360+8,i*220+40))
board.save(D/'CANVAS_BEFORE_AFTER.png',optimize=True)
