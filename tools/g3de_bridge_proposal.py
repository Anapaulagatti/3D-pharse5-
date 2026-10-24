"""Measured protected-geometry proposal only. Does not write live world or collision."""
from pathlib import Path
import json,heapq
import numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt,label
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate3/residual-v1';D=R/'docs/gate3-residual';m=json.loads((R/'public/assets/gate3/aligned-world/manifest.json').read_text());sp=m['contactCollision'];ox,oy,w,h=sp['rect'];physical=np.fromfile(R/'public'/sp['physical'],np.uint8).reshape(h,w)>0;atlas=json.loads((R/'public/assets/juni/juni.json').read_text())['frames'];sheet=Image.open(R/'public/assets/juni/juni.png').convert('RGBA');points=set();poses={}
for name,fr in atlas.items():
 if not name.startswith(('walk-','run-','start-','idle-','stop-','turn-')):continue
 f=fr['frame'];al=np.array(sheet.crop((f['x'],f['y'],f['x']+f['w'],f['y']+f['h'])))[:,:,3];ys,xs=np.where(al>0);bottom=int(ys.max());ys,xs=np.where((al>0)&(np.indices(al.shape)[0]>=bottom-3));pts=set((int(x-48),int(y-min(100,bottom+1)))for x,y in zip(xs,ys));points|=pts;poses[name]={'nativeBottom':bottom,'projectedContacts':sorted(pts)}
postFeet=[[3080,3430,11,4],[3080,3446,11,4],[3080,3465,12,4],[3080,3488,11,4],[3080,3514,11,4],[3150,3548,22,5],[3190,3574,24,5],[3306,3601,25,5],[3217,3551,8,4],[3255,3558,8,4],[3287,3565,8,4],[3324,3566,22,5]]
yy,xx=np.indices((h,w));wx=xx+ox;wy=yy+oy;bounded=(wx>=3128)&(wx<=3515)&(wy>=3440)&(wy<=3660);dist=distance_transform_edt(~physical);start=(3110-ox,3460-oy);end=(3530-ox,3640-oy);trials=[];solution=None
for radius in range(0,33):
 pa=physical|((dist<=radius)&bounded)
 for x,y,ww,hh in postFeet:pa[y-oy:y-oy+hh,x-ox:x-ox+ww]=False
 valid=np.ones((h,w),bool)
 for dx,dy in points:
  shifted=np.ones((h,w),bool);x1=max(0,-dx);x2=min(w,w-dx);y1=max(0,-dy);y2=min(h,h-dy);shifted[y1:y2,x1:x2]=pa[y1+dy:y2+dy,x1+dx:x2+dx];valid&=shifted
 labs,_=label(valid);a=labs[start[1],start[0]];b=labs[end[1],end[0]];ok=bool(a>0 and a==b);change=pa&~physical;trials.append({'maximumShoulderPx':radius,'newSurfacePixels':int(change.sum()),'allPoseContactConnectivity':ok,'startSupported':bool(a),'endSupported':bool(b)})
 if ok:solution=(radius,pa,valid,change);break
assert solution is not None,'No bounded safe proposal; do not install any geometry'
radius,pa,valid,change=solution
# Exact shortest4-connected path, all supported pose pixels at every1px.
q=[(0,0,start)];cost={start:0};parent={}
while q:
 _,g,u=heapq.heappop(q)
 if u==end:break
 if cost[u]!=g:continue
 for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
  v=(u[0]+dx,u[1]+dy)
  if not(0<=v[0]<w and 0<=v[1]<h)or not valid[v[1],v[0]]:continue
  ng=g+1
  if ng<cost.get(v,1e9):cost[v]=ng;parent[v]=u;heapq.heappush(q,(ng+abs(v[0]-end[0])+abs(v[1]-end[1]),ng,v))
path=[end]
while path[-1]!=start:path.append(parent[path[-1]])
path.reverse();path=[[x+ox,y+oy]for x,y in path];ys,xs=np.where(change);box=[int(xs.min()+ox),int(ys.min()+oy),int(xs.max()-xs.min()+1),int(ys.max()-ys.min()+1)]
# Only material actually needed to support this safe path, plus2px structural margin,
# is proposed rather than blindly expanding every deck edge.
needed=np.zeros((h,w),bool)
for x,y in path:
 for dx,dy in points:
  px=x+dx-ox;py=y+dy-oy
  if 0<=px<w and 0<=py<h and not physical[py,px]:needed[py,px]=True
from scipy.ndimage import binary_dilation
needed=binary_dilation(needed,iterations=2)&change;proposed=physical|needed
# Check selected route against the reduced exact repair mask, all contacts must still fit.
assert all(proposed[y+dy-oy,x+dx-ox]for x,y in path for dx,dy in points if 0<=x+dx-ox<w and 0<=y+dy-oy<h)
ys,xs=np.where(needed);box=[int(xs.min()+ox),int(ys.min()+oy),int(xs.max()-xs.min()+1),int(ys.max()-ys.min()+1)];Image.fromarray(needed.astype('uint8')*255).save(S/'bridge-proposed-visible-structure-mask.png');Image.fromarray(proposed.astype('uint8')*255).save(S/'bridge-proposed-physical.png')
labs,n=label(needed);islands=[]
for k in range(1,n+1):
 yy,xx=np.where(labs==k);islands.append({'worldRect':[int(xx.min()+ox),int(yy.min()+oy),int(xx.max()-xx.min()+1),int(yy.max()-yy.min()+1)],'addedSurfacePixels':int(len(xx))})
report={'status':'PROPOSAL ONLY / NOT INSTALLED','baseline':'9827761','method':'Exact native opaque lowest4 rows per walk/run/start/idle/stop/turn frame raised feet projected to unchanged ground anchor while below-anchor toes retain their ACTUAL native offsets. Universal pose union is a conservative guarantee for arbitrary stops and direction changes; no sprite bounding-box test.4-connected1px physical search, original post-foot holes retained.','nativeAtlas':'UNCHANGED96x112, anchor48,100','nativePoseCount':len(poses),'contactOffsets':sorted(points),'trials':trials,'baselineAllPoseRoute':'FAIL','proposedAllPoseRoute':'PASS_GEOMETRY_MODEL_ONLY / not actual production movement','maximumRequiredShoulderPx':radius,'exactAddedSurfacePixels':int(needed.sum()),'worldBounds':box,'components':islands,'unchanged':'Bridge endpoints, original deck pixels/design/scale, Jeju, physical post supports and main live collision. No new land is silently allocated.','requiresApproval':'Bounded stone stair/deck shoulder must be visibly authored with support/rail/shore detailing within this exact mask before any live collision enlargement. This diagnostic mask is not artwork or permission to walk on invisible water. No masterplan amendment applied.','route':path,'poses':poses}
(S/'bridge-clearance-proposal.json').write_text(json.dumps(report,indent=2)+'\n');(D/'bridge-clearance-proposal.json').write_text(json.dumps({k:v for k,v in report.items()if k!='poses'},indent=2)+'\n');print('PROPOSAL ONLY:',radius,'px maximum shoulder;',int(needed.sum()),'new visible support pixels;',box,'components',len(islands))
