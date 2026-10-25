from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-final';S=R/'assets-src/gate3/final-surgical-v1'
def wr(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
m=json.loads((R/'public/assets/gate3/final-world/manifest.json').read_text());sp=m['contactCollision'];ox,oy,w,h=sp['rect'];physical=np.fromfile(R/'public'/sp['physical'],np.uint8).reshape(h,w);atlas=json.loads((R/'public/assets/juni/juni.json').read_text())['frames'];sheet=Image.open(R/'public/assets/juni/juni.png').convert('RGBA');cache={}
def pose(name):
 if name not in cache:
  f=atlas[name]['frame'];im=sheet.crop((f['x'],f['y'],f['x']+f['w'],f['y']+f['h']));a=np.array(im);ys,xs=np.where(a[:,:,3]>0);bottom=int(ys.max());ys,xs=np.where((a[:,:,3]>0)&(np.indices(a.shape[:2])[0]>=bottom-3));cache[name]=(im,[(int(x-48),int(y-min(100,bottom+1)))for x,y in zip(xs,ys)])
 return cache[name]
def ground(s):
 if not(ox<=round(s['x'])<ox+w and oy<=round(s['y'])<oy+h):return None
 _,pts=pose(s['frame']);cx,cy=round(s['x']),round(s['y']);bad=[]
 for dx,dy in pts:
  x,y=cx+dx-ox,cy+dy-oy
  if 0<=x<w and 0<=y<h and not physical[y,x]:bad.append([cx+dx,cy+dy])
 return bad
reports=[];frames=[]
for filename in ['movement-report.json','bridge-movement-report.json']:
 p=D/filename
 if not p.exists():continue
 motion=json.loads(p.read_text());rows=[]
 for leg in motion['legs']:
  samples=[s for s in motion['samples']if s.get('leg')==leg['id']];checked=0;fail=[]
  for sample in samples:
   bad=ground(sample)
   if bad is None:continue
   checked+=1
   if bad:fail.append({'position':[sample['x'],sample['y']],'frame':sample['frame'],'unsupportedProjectedContactPixels':bad[:12]})
  rows.append({'id':leg['id'],'actualControlResult':leg['status'],'sampleCount':len(samples),'nativeContactSamples':checked,'contactFailureSamples':len(fail),'firstFailures':fail[:8]})
 reports.append({'file':filename,'complete':motion['complete'],'errors':motion['errors'],'legs':rows,'physicalDevice':False})
 for a in motion.get('movingShots',[]):frames.append((a['name'],a))
 for a in motion.get('poseShots',[]):frames.append((a['name'],a))
 # Endpoints have their own same-POST_RENDER audit and native image.
 for leg in motion['legs']:
  name=('bridge-proof-'if filename.startswith('bridge-')else'walk-')+leg['id'];p=D/(name+'-audit.json')
  if p.exists():frames.append((name+'-native',json.loads(p.read_text())))
# Compare the actual native Juni pixels, while accounting only for the actual depth-sorted foreground.
visibility=[]
for name,a in frames:
 s=a['state'];im,pts=pose(s['frame']);pixels=np.array(im);cx,cy=round(s['x']),round(s['y']);sx,sy=a['camera']['scroll'];shot=Image.open(D/(name+'.png')).convert('RGB');x0,y0=cx-48-sx,cy-100-sy
 if not(0<=x0 and 0<=y0 and x0+96<=shot.width and y0+112<=shot.height):continue
 actual=np.array(shot.crop((x0,y0,x0+96,y0+112)));cover=np.zeros((112,96),bool);coverNames=[]
 for l in a['layers']:
  if not l['key'].startswith('f/')or not l['visible']or l.get('alpha',1)<=0:continue
  ob=next((ob for ob in m['objects']if 'f/'+ob['id']==l['key']),None)
  if ob is None or ob['sortY']<=round(cy)+.1:continue
  layer=Image.open(R/'public'/ob['image']).convert('RGBA');lx=max(cx-48,ob['x']);ly=max(cy-100,ob['y']);rx=min(cx+48,ob['x']+ob['width']);ry=min(cy+12,ob['y']+ob['height'])
  if lx>=rx or ly>=ry:continue
  alpha=np.array(layer.getchannel('A').crop((lx-ob['x'],ly-ob['y'],rx-ob['x'],ry-ob['y'])))>0;cover[ly-(cy-100):ry-(cy-100),lx-(cx-48):rx-(cx-48)]|=alpha
  if alpha.any():coverNames.append(ob['id'])
 opaque=pixels[:,:,3]>0;diff=np.any(actual!=pixels[:,:,:3],axis=2);unintended=int((opaque&~cover&diff).sum());upper=opaque&(np.indices(opaque.shape)[0]<75);upperCovered=int((upper&cover).sum());visibility.append({'frame':name,'worldPosition':[s['x'],s['y']],'atlasFrame':s['frame'],'opaqueNativeJuniPixels':int(opaque.sum()),'unexplainedChangedJuniPixels':unintended,'foregroundOcclusionPixels':int((opaque&cover).sum()),'upperBodyOcclusionPixels':upperCovered,'sourcePixelVisibilityFraction':round(float((opaque&~cover&~diff).sum()/opaque.sum()),4),'occludingObjects':coverNames,'result':'PASS_NO_UNEXPLAINED_CLIPPING'if not unintended else'FAIL_UNEXPLAINED_PIXEL_CHANGE','meaning':'Near rail/stone and cutaway-wall overlap is recorded explicitly, not misreported as total body invisibility or a ground footprint.'})
 # Native diagnostic overlay: sprite outline and projected original foot-contact pixels.
 out=shot.copy();dr=ImageDraw.Draw(out);dr.rectangle((x0,y0,x0+95,y0+111),outline='#ff80c5')
 for dx,dy in pts:dr.point((cx+dx-sx,cy+dy-sy),fill='#ff5f61'if[cx+dx,cy+dy]in(ground(s)or[])else'#70ffbb')
 out.save(D/(name+'-body-overlay.png'))
wr(D/'body-clearance.json',{'method':'Actual original atlas96x112 anchor48,100. Ground-contact pixels are lowest4 opaque rows; only raised feet project to the original anchor, and below-anchor toes retain actual native offsets. Per-direction/gait guards plus actual sampled frames; full native sprite visibility independently read back against foreground depth. No avatar rescale or arbitrary49x17 silhouette-on-ground assumption.','controlReports':reports,'capturedPoseContact':[{'frame':name,'worldPosition':[a['state']['x'],a['state']['y']],'atlasFrame':a['state']['frame'],'unsupportedProjectedPixels':ground(a['state']),'status':'FAIL'if ground(a['state'])else'NO_FAILURE_IN_CAPTURED_POSE_ONLY'}for name,a in frames if '-stop-'in name or '-turn-'in name],'nativeVisibility':visibility,'artAcceptance':'Human review required; expected railing/cutaway occlusion is not automatically an artistic PASS.','physicalDevices':'NOT TESTED'})
print('Movement audit:',[(r['file'],r['complete'])for r in reports],'; visibility frames',len(visibility),'; unexplained Juni pixels',sum(r['unexplainedChangedJuniPixels']for r in visibility))
