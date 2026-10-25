"""Original native atlas contact and body readback for BOTH real bridge sessions."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-jeju-bridges';S=R/'assets-src/gate3/jeju-bridges-v1';m=json.loads((R/'public/assets/gate3/jeju-bridges-world/manifest.json').read_text());motion=json.loads((D/'movement-report.json').read_text());assert motion['complete']and len(motion['legs'])==8 and not motion['errors'];phys=np.array(Image.open(S/'visible-physical-support.png'))>0;atlas=json.loads((R/'public/assets/juni/juni.json').read_text())['frames'];sheet=Image.open(R/'public/assets/juni/juni.png').convert('RGBA');cache={}
def pose(frame):
 if frame not in cache:
  q=atlas[frame]['frame'];im=sheet.crop((q['x'],q['y'],q['x']+q['w'],q['y']+q['h']));a=np.array(im);yy,xx=np.indices(a.shape[:2]);bottom=np.where(a[:,:,3]>0)[0].max();ys,xs=np.where((a[:,:,3]>0)&(yy>=bottom-3));cache[frame]=(im,[(int(x-48),int(y-min(100,bottom+1)))for x,y in zip(xs,ys)])
 return cache[frame]
contact=[]
for leg in motion['legs']:
 samples=[s for s in motion['samples']if s.get('leg')==leg['id']];bad=[]
 for s in samples:
  _,pts=pose(s['frame']);cx,cy=round(s['x']),round(s['y']);unsupported=[[cx+dx,cy+dy]for dx,dy in pts if not phys[cy+dy,cx+dx]]
  if unsupported:bad.append({'position':[s['x'],s['y']],'frame':s['frame'],'unsupportedNativeContactPixels':unsupported[:8]})
 contact.append({'leg':leg['id'],'actualMovement':leg['status'],'samples':len(samples),'failureSamples':len(bad),'firstFailures':bad[:8],'sampledActions':sorted({s['frame'].split('-')[0]for s in samples})})
visibility=[];allShots=[{'name':'walk-'+l['id']+'-native','audit':json.loads((D/('walk-'+l['id']+'-audit.json')).read_text())}for l in motion['legs']]+[{'name':q['name'],'audit':q}for q in motion['poseShots']]
for row in allShots:
 a=row['audit'];s=a['state'];im,pts=pose(s['frame']);rgb=np.array(im);sx,sy=map(round,a['camera']['scroll']);cx,cy=round(s['x']),round(s['y']);x0,y0=cx-48-sx,cy-100-sy;shot=Image.open(D/(row['name']+'.png')).convert('RGB');actual=np.array(shot.crop((x0,y0,x0+96,y0+112)));cover=np.zeros((112,96),bool)
 for l in a['layers']:
  if not l['key'].startswith('f/')or not l['visible']or l['alpha']<=0:continue
  ob=next(o for o in m['objects']if'f/'+o['id']==l['key'])
  if ob['sortY']<=cy+.1:continue
  x,y,w,h=[ob[k]for k in ['x','y','width','height']];lx=max(cx-48,x);ly=max(cy-100,y);rx=min(cx+48,x+w);ry=min(cy+12,y+h)
  if lx<rx and ly<ry:cover[ly-cy+100:ry-cy+100,lx-cx+48:rx-cx+48]|=np.array(Image.open(R/'public'/ob['image']).getchannel('A').crop((lx-x,ly-y,rx-x,ry-y)))>0
 diff=(rgb[:,:,3]>0)&~cover&np.any(actual!=rgb[:,:,:3],2);unsupported=[[cx+dx,cy+dy]for dx,dy in pts if not phys[cy+dy,cx+dx]];visibility.append({'frame':row['name'],'nativeAtlasFrame':s['frame'],'unexplainedJuniPixelChanges':int(diff.sum()),'foregroundCoveredNativePixels':int(((rgb[:,:,3]>0)&cover).sum()),'unsupportedFootPixels':unsupported[:8]});dr=ImageDraw.Draw(shot);dr.rectangle((x0,y0,x0+95,y0+111),outline='#fa8ac9')
 for dx,dy in pts:dr.point((cx+dx-sx,cy+dy-sy),fill='#66ffc8'if phys[cy+dy,cx+dx]else'#ff5757')
 shot.save(D/(row['name']+'-contact-overlay.png'))
summary={}
for k in ['a','b']:
 c=[q for q in contact if q['leg'].startswith('bridge-'+k)];poses=[q for q in visibility if'bridge-'+k in q['frame']];summary[k.upper()]={'walkingTraversal':'PASS'if all('PASS'in q['actualMovement']for q in c)else'FAIL','normalAndRunningBothDirections':len(c)==4,'stopTurnPoseSupport':'PASS'if not any(q['failureSamples']for q in c)and not any(q['unsupportedFootPixels']for q in poses)else'FAIL','sampledNativeContacts':sum(q['samples']for q in c),'unsupportedSampleCount':sum(q['failureSamples']for q in c),'JuniNativeReadback':'PASS'if not any(q['unexplainedJuniPixelChanges']for q in poses)else'FAIL','posesObserved':sorted({q['nativeAtlasFrame'].split('-')[0]for q in poses}),'artAcceptance':'PENDING HUMAN'}
report={'method':'Two separate review spawns, four uninterrupted actual-control legs per crossing, original WASD/Shift/joystick. All native opaque lowest4 rows, raised feet projected to anchor, actual below-anchor toes retained. Collision centre field has1px phase safety. Floor TOP PLANE excludes vertical pier faces; raised railing/post shafts have original-source foreground ownership. No speed/pose/position/collision overrides.','summary':summary,'contact':contact,'nativeVisibility':visibility,'physicalAndroidChrome':'NOT TESTED','physicalIPhoneSafari':'NOT TESTED','hardwarePerformance':'NOT TESTED','artAcceptance':'PENDING HUMAN'};(D/'body-clearance.json').write_text(json.dumps(report,indent=2)+'\n');print(summary)
assert all(q['stopTurnPoseSupport']=='PASS'and q['JuniNativeReadback']=='PASS'for q in summary.values()),'DO NOT CLAIM BRIDGE PASS'
