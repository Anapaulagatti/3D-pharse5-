"""Native minimum-error edge ownership; no RGB synthesis/filter/resize/reflection."""
from pathlib import Path
import json
import numpy as np
from PIL import Image

def seam(cost, cyclic=False):
 n,k=cost.shape;dp=cost[0].copy();parent=np.zeros((n,k),np.int8)
 start=int(np.argmin(cost[0]+cost[-1]))if cyclic else None
 if cyclic:dp[:]=np.inf;dp[start]=cost[0,start]
 for i in range(1,n):
  choices=np.stack([np.r_[np.inf,dp[:-1]],dp,np.r_[dp[1:],np.inf]])
  step=np.argmin(choices,axis=0);parent[i]=step.astype(np.int8)-1;dp=choices[step,np.arange(k)]+cost[i]
 j=start if cyclic else int(np.argmin(dp));energy=float(dp[j]);out=np.empty(n,np.int16);out[-1]=j
 for i in range(n-1,0,-1):j+=int(parent[i,j]);out[i-1]=j
 return out,energy

def native_periodic(R,S):
 source=np.array(Image.open(R/'assets-src/gate3/reconciliation-v1/ocean-authored.png').convert('RGBA'));H,W=source.shape[:2];assert(W,H)==(1536,1024);assert np.all(source[:,:,3]==255)
 yy,xx=np.indices((H,W),dtype=np.int16);origin=np.stack([yy,xx],axis=2);data=source.copy();maps=origin.copy();records=[]
 # Roll to put the wrap in the middle, quilt one256px native patch with two
 # independent64px native overlap cuts, then unroll. Global period/phase exact.
 for axis in [1,0]:
  length=data.shape[axis];shift=length//2;rolled=np.roll(data,shift,axis=axis);rolledMap=np.roll(maps,shift,axis=axis);start=shift-128;end=shift+128;best=None
  for donor in range(128,length-256,128):
   if axis==1:
    patch=data[:,donor:donor+256].copy();patchMap=maps[:,donor:donor+256].copy();left=rolled[:,start:start+64,:3].astype(float);right=rolled[:,end-64:end,:3].astype(float);lc=np.mean(abs(left-patch[:,:64,:3]),axis=2);rc=np.mean(abs(right-patch[:,-64:,:3]),axis=2)
   else:
    patch=data[donor:donor+256].copy();patchMap=maps[donor:donor+256].copy();left=rolled[start:start+64,:,:3].astype(float);right=rolled[end-64:end,:,:3].astype(float);lc=np.mean(abs(left-patch[:64,:,:3]),axis=2).T;rc=np.mean(abs(right-patch[-64:,:,:3]),axis=2).T
   # Leave8px overlap context on each side. Horizontal cuts are closed loops
   # across X, preserving the already corrected X wrap exactly.
   l,e1=seam(lc[:,8:56],cyclic=axis==0);r,e2=seam(rc[:,8:56],cyclic=axis==0);l+=8;r+=8
   if best is None or e1+e2<best[0]:best=(e1+e2,donor,patch,patchMap,l,r)
  energy,donor,patch,patchMap,l,r=best
  if axis==1:
   q=np.arange(256)[None,:];own=(q>=l[:,None])&(q<192+r[:,None]);view=rolled[:,start:end];om=rolledMap[:,start:end]
  else:
   q=np.arange(256)[:,None];own=(q>=l[None,:])&(q<192+r[None,:]);view=rolled[start:end];om=rolledMap[start:end]
  view[own]=patch[own];om[own]=patchMap[own];data=np.roll(rolled,-shift,axis=axis);maps=np.roll(rolledMap,-shift,axis=axis)
  records.append({'axis':'X'if axis==1 else'Y','nativeDonorRange':[donor,donor+256],'overlap':64,'cyclicCuts':axis==0,'minimumErrorEnergy':energy,'leftCut':l.tolist(),'rightCut':r.tolist()})
 assert np.array_equal(data,source[maps[:,:,0],maps[:,:,1]])
 Image.fromarray(data).save(S/'ocean-native-wrap-repaired.png');np.savez_compressed(S/'ocean-native-origin-map.npz',sourceYX=maps);Image.fromarray(np.any(data!=source,axis=2).astype('uint8')*255).save(S/'ocean-wrap-source-change-mask.png')
 def edge(a,axis):return float(np.abs((a[:,0,:3]if axis=='X'else a[0,:,:3]).astype(float)-(a[:,-1,:3]if axis=='X'else a[-1,:,:3]).astype(float)).mean())
 info={'source':'assets-src/gate3/reconciliation-v1/ocean-authored.png','sourceSize':[W,H],'derived':'ocean-native-wrap-repaired.png','originMap':'ocean-native-origin-map.npz','periodAndWorldPhase':'UNCHANGED1536x1024 /3180,3200','nativeRGBProof':'Every derived RGBA pixel equals one exact original source pixel at an integer coordinate. No blur, sharpen, resize, recolor, reflection or interpolation.','cuts':records,'oldEdgeMeanRGBDelta':{a:edge(source,a)for a in ['X','Y']},'newEdgeMeanRGBDelta':{a:edge(data,a)for a in ['X','Y']},'scope':'Only native overlap ownership near the existing material wrap. Not a generic landscape tile or newly generated world.'}
 (S/'ocean-material-registry.json').write_text(json.dumps(info,indent=2)+'\n');return source,data,info

def apply_wrap(g,R,S):
 old,new,info=native_periodic(R,S);W,H=g.size;yy,xx=np.indices((H,W),dtype=np.int32);oldWorld=old[(yy-3200)%1024,(xx-3180)%1536];newWorld=new[(yy-3200)%1024,(xx-3180)%1536];current=np.array(g);matches=np.all(current==oldWorld,axis=2);atlasChange=np.any(oldWorld!=newWorld,axis=2);owner=np.array(Image.open(R/'assets-src/gate3/reconciliation-v1/shared-ocean-ownership.png'))>0
 coast=np.array(Image.open(S/'southern-shared-water-mask.png'))>0;owner[3840:4280,:3180]|=coast
 # No land/core district ownership can be changed by a water-material correction.
 owner[80:3980,160:3160]=False
 keep=np.array(Image.open(R/'assets-src/gate3/reconciliation-v1/jeju-protected-land-nearshore.png'))>0;owner[3200:4736,3180:4204]&=~keep
 mask=matches&atlasChange&owner;current[mask]=newWorld[mask];g=Image.fromarray(current);Image.fromarray(mask.astype('uint8')*255).save(S/'shared-ocean-wrap-world-mask.png')
 record={'id':'shared-ocean-native-wrap','materialRegistry':'ocean-material-registry.json','worldMask':'shared-ocean-wrap-world-mask.png','pixels':int(mask.sum()),'rootCause':'Existing1536x1024 source is not periodic; both sides of visible3180 boundary already match its last/first columns. Native-overlap cuts repair the material itself; no extra canonical island painting.','period':[1536,1024],'phase':[3180,3200],'protected':'All approved island/nearshore bitmap pixels, mainland core, geometry, original source files exact. Only still-owned shared-ocean native texels at existing wrap bands changed.','rejectedTrial':'shared-water-registry-v2.json / physical-water expansion ineffective and NOT INSTALLED','artAcceptance':'PENDING HUMAN'}
 (S/'shared-ocean-wrap-registration.json').write_text(json.dumps(record,indent=2)+'\n');return g,record

if __name__=='__main__':
 R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate3/residual-v1';m=json.loads((R/'public/assets/gate3/residual-world/manifest.json').read_text());g=Image.new('RGBA',m['size'])
 for c in m['chunks']:g.paste(Image.open(R/'public'/c['image']),(c['x'],c['y']))
 g,record=apply_wrap(g,R,S)
 for o in sorted(m['objects'],key=lambda o:o['sortY']):g.alpha_composite(Image.open(R/'public'/o['image']).convert('RGBA'),(o['x'],o['y']))
 g.crop((2300,3530,3580,4430)).save('/tmp/g3de-native-wrap-draft.png');print(json.dumps(record,indent=2))
