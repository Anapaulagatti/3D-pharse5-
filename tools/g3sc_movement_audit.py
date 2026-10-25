"""Actual native Juni contact/body readback for the continuous station route."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-station-clean';m=json.loads((R/'public/assets/gate3/station-clean-world/manifest.json').read_text());motion=json.loads((D/'movement-report.json').read_text());assert motion['complete']and len(motion['legs'])==4 and not motion['errors'];f=np.zeros((4864,4352),np.uint8)
for c in m['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];f[y:y+h,x:x+w]=np.fromfile(R/'public'/c['mask'],np.uint8).reshape(h,w)
atlas=json.loads((R/'public/assets/juni/juni.json').read_text())['frames'];sheet=Image.open(R/'public/assets/juni/juni.png').convert('RGBA');cache={}
def pose(frame):
 if frame not in cache:
  q=atlas[frame]['frame'];im=sheet.crop((q['x'],q['y'],q['x']+q['w'],q['y']+q['h']));a=np.array(im);yy,xx=np.indices(a.shape[:2]);bottom=np.where(a[:,:,3]>0)[0].max();ys,xs=np.where((a[:,:,3]>0)&(yy>=bottom-3));cache[frame]=(im,[(int(x-48),int(y-min(100,bottom+1)))for x,y in zip(xs,ys)])
 return cache[frame]
contact=[]
for leg in motion['legs']:
 bad=[];samples=[s for s in motion['samples']if s.get('leg')==leg['id']]
 for s in samples:
  _,pts=pose(s['frame']);cx,cy=round(s['x']),round(s['y']);unsupported=[[cx+dx,cy+dy]for dx,dy in pts if not f[cy+dy,cx+dx]]
  if unsupported:bad.append({'position':[s['x'],s['y']],'frame':s['frame'],'unsupportedNativeContactPixels':unsupported[:10]})
 contact.append({'id':leg['id'],'actualMovement':leg['status'],'samples':len(samples),'failureSamples':len(bad),'firstFailures':bad[:8]})
visibility=[]
for leg in motion['legs']:
 name='walk-'+leg['id'];a=json.loads((D/(name+'-audit.json')).read_text());s=a['state'];im,pts=pose(s['frame']);rgba=np.array(im);sx,sy=a['camera']['scroll'];assert all(float(v).is_integer()for v in [sx,sy]);cx,cy=round(s['x']),round(s['y']);x0,y0=cx-48-sx,cy-100-sy;shot=Image.open(D/(name+'-native.png')).convert('RGB');actual=np.array(shot.crop((x0,y0,x0+96,y0+112)));cover=np.zeros((112,96),bool)
 for l in a['layers']:
  if not l['key'].startswith('f/')or not l['visible']or l['alpha']<=0:continue
  ob=next(o for o in m['objects']if'f/'+o['id']==l['key'])
  if ob['sortY']<=cy+.1:continue
  x,y,w,h=[ob[k]for k in ['x','y','width','height']];lx=max(cx-48,x);ly=max(cy-100,y);rx=min(cx+48,x+w);ry=min(cy+12,y+h)
  if lx<rx and ly<ry:cover[ly-(cy-100):ry-(cy-100),lx-(cx-48):rx-(cx-48)]|=np.array(Image.open(R/'public'/ob['image']).convert('RGBA').getchannel('A').crop((lx-x,ly-y,rx-x,ry-y)))>0
 mismatch=(rgba[:,:,3]>0)&~cover&np.any(actual!=rgba[:,:,:3],2);assert not mismatch.any(),name;visibility.append({'frame':name,'sourceFrame':s['frame'],'unexplainedChangedJuniPixels':int(mismatch.sum()),'foregroundCoveredNativePixels':int(((rgba[:,:,3]>0)&cover).sum())});dr=ImageDraw.Draw(shot);dr.rectangle((x0,y0,x0+95,y0+111),outline='#ff95d4')
 for dx,dy in pts:dr.point((cx+dx-sx,cy+dy-sy),fill='#74ffbd'if f[cy+dy,cx+dx]else'#ff6060')
 shot.save(D/(name+'-native-contact-overlay.png'))
(D/'body-clearance.json').write_text(json.dumps({'method':'Real4-leg original-control recording. Original atlas96x112, anchor48,100; lowest4 native opaque rows, only raised feet projected to anchor, below-anchor toes retained. Correct current physical .bin and unchanged logical footprint. No forced pose/frame/camera/clock/position/collision override.','contact':contact,'nativeVisibility':visibility,'continuousRoute':True,'physicalDevices':'NOT TESTED','artAcceptance':'PENDING HUMAN'},indent=2)+'\n');print('Movement/body:',len(contact),'actual legs;',sum(q['failureSamples']for q in contact),'unsupported native contact samples;',sum(q['unexplainedChangedJuniPixels']for q in visibility),'unexplained Juni pixels')
