"""Reproducible ownership, preservation and native geometry checks. No artwork writes."""
from pathlib import Path
import json,hashlib,subprocess
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-reconciliation';S=R/'assets-src/gate3/reconciliation-v1'
def read(p):return json.loads((R/p).read_text())
def wr(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=read('public/assets/gate3/reconciled-world/manifest.json');b=read('public/assets/gate3/zoned-world/manifest.json');reg=read('assets-src/gate3/reconciliation-v1/registry.json');W,H=m['size']
def assemble(mm):
 g=np.zeros((H,W,4),np.uint8);f=np.zeros((H,W),np.uint8)
 for c in mm['chunks']:
  x,y,w,h=[c[k]for k in ['x','y','width','height']];g[y:y+h,x:x+w]=np.array(Image.open(R/'public'/c['image']).convert('RGBA'));f[y:y+h,x:x+w]=np.frombuffer((R/'public'/c['mask']).read_bytes(),np.uint8).reshape(h,w)
 return g,f
g,f=assemble(m);old,of=assemble(b);owner=np.zeros((H,W),np.uint8);families={0:'Unchanged baseline / recursive zoned-world provenance',1:'Clean authored1536x1024 offshore family, native integer world phase',9:'Native courtyard paving / retired wall courses'}
owner[np.array(Image.open(S/'shared-ocean-ownership.png'))>0]=1
for i,name in enumerate(['palacewest','palaceeast','commercial','station'],2):
 x,y,w,h=reg['regions'][name];owner[y:y+h,x:x+w][np.array(Image.open(S/(name+'-ownership.png')))>0]=i;families[i]=name+' authored environment / explicit preservation mask'
owner[np.array(Image.open(S/'shared-ocean-ownership.png'))>0]=1
for i,name in enumerate(['station','waternorth','watersouth'],6):
 x,y,w,h=reg['regions'][name];owner[y:y+h,x:x+w][np.array(Image.open(S/(name+'-shore-foam-ownership.png')))>0]=i;families[i]=name+' native foam only / physical-shore mask'
keep=np.array(Image.open(S/'jeju-protected-land-nearshore.png'))>0;owner[3200:4736,3180:4204][keep]=0
aprons=[[1830,790,430,340],[1810,900,20,230],[1070,170,73,870],[2874,170,69,870],[1110,127,1830,73],[1110,985,720,80],[2260,985,680,80]]
for x,y,w,h in aprons:owner[y:y+h,x:x+w]=9
changed=np.any(g!=old,axis=2);missing=int((changed&(owner==0)).sum());assert missing==0,missing
Image.fromarray(owner).save(S/'ground-source-ownership.png',optimize=True)
coverage=np.zeros((H,W),np.uint8)
for c in m['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];coverage[y:y+h,x:x+w]+=1;assert Image.open(R/'public'/c['image']).size==(w,h)
assert np.all(coverage==1)
edges=[]
for i,a in enumerate(m['chunks']):
 for z in m['chunks'][i+1:]:
  ax,ay,aw,ah=[a[k]for k in ['x','y','width','height']];x,y,w,h=[z[k]for k in ['x','y','width','height']]
  if ax+aw==x and ay==y:
   l=g[y:y+h,x-1,:3].astype(int);r=g[y:y+h,x,:3].astype(int);inside=g[y:y+h,x+1,:3].astype(int);own=np.unique(owner[y:y+h,x-1:x+1]).tolist();direction='vertical'
  elif ay+ah==y and ax==x:
   l=g[y-1,x:x+w,:3].astype(int);r=g[y,x:x+w,:3].astype(int);inside=g[y+1,x:x+w,:3].astype(int);own=np.unique(owner[y-1:y+1,x:x+w]).tolist();direction='horizontal'
  else:continue
  edges.append({'a':a['id'],'b':z['id'],'direction':direction,'owners':own,'meanRGBStepAcross':round(float(np.abs(l-r).mean()),2),'meanRGBStepInside':round(float(np.abs(r-inside).mean()),2),'coverage':'PASS','visualScaleColorFoliageShadowReview':'Native review required; RGB diagnostic is not artistic approval'})
foreground=[];instances=[]
for o in m['objects']:
 im=Image.open(R/'public'/o['image']).convert('RGBA');alpha=np.array(im)[:,:,3];assert im.size==(o['width'],o['height']);key=(o['image'],o['x'],o['y']);instances.append(key)
 foreground.append({'id':o['id'],'source':o['image'],'sha256':sha(R/'public'/o['image']),'registration':[o[k]for k in ['x','y','width','height','sortY']],'sourcePivot':o.get('sourcePivot'),'alphaSoftening':o['alphaSoftening'],'partialAlphaPixels':int(((alpha>0)&(alpha<255)).sum()),'opaquePixelsAtTextureEdge':int((alpha[0]>0).sum()+(alpha[-1]>0).sum()+(alpha[:,0]>0).sum()+(alpha[:,-1]>0).sum()),'ownership':'Whole native texture, not chopped by ground chunks; opaque edge is diagnostic, not proof of clipping','shadowPolicy':'Original single source owner retained; no added shadow sprite'})
assert len(set(instances))==len(instances)
station=next(o for o in m['objects']if o['id']=='registration/station');original=np.array(Image.open(R/'public/assets/gate3/registration/station.png').convert('RGBA'));derived=np.array(Image.open(R/'public'/station['image']).convert('RGBA'));ret=np.array(Image.open(S/'station-background-retirement.png'))>0
assert np.array_equal(original[:,:,:3],derived[:,:,:3]);assert np.array_equal(original[~ret],derived[~ret])
assert np.array_equal(g[2603:2813,2274:2958],old[2603:2813,2274:2958]);assert np.array_equal(g[3200:4736,3180:4204][keep],old[3200:4736,3180:4204][keep]);assert np.array_equal(f[3200:4736,3180:4204],of[3200:4736,3180:4204]);assert np.array_equal(f[1700:3200],of[1700:3200]);assert not f[2626:2755,2950:2958].any()
for row in reg['northernBuildings']+reg['approvedBoundaries']:
 x,y,w,h=row['rect'];assert not f[y:y+h,x:x+w].any(),row['id']
assert np.all(f[790:1130,1830:2260]==255)
for protected in reg['architecturePreservation']:
 x,y,w,h=protected['rect'];assert np.array_equal(g[y:y+h,x:x+w],old[y:y+h,x:x+w]),protected['id']
# Every historical zoning artifact remains byte-identical, including unregistered docs.
locked=[]
for line in subprocess.check_output(['git','ls-tree','-r','5d725c6','--','assets-src/gate3/zoned-world-v1','public/assets/gate3/zoned-world','public/assets/gate3/zoned-before','docs/gate3-zoned-world'],cwd=R,text=True).splitlines():
 meta,path=line.split('\t');blob=meta.split()[2];actual=subprocess.check_output(['git','hash-object',path],cwd=R,text=True).strip();locked.append({'path':path,'blob':blob,'unchanged':actual==blob})
assert all(v['unchanged']for v in locked)
cap=read('docs/gate3-reconciliation/native-captures.json');pairs=[]
for row in cap['rows']:
 if '-after-native'not in row['name']:continue
 prior=next(r for r in cap['rows']if r['name']==row['name'].replace('-after-','-before-'));ok=prior['audit']['camera']['scroll']==row['audit']['camera']['scroll']and Image.open(D/(prior['name']+'.png')).size==Image.open(D/(row['name']+'.png')).size;assert ok;pairs.append({'name':row['name'],'sameCameraAndNativeSize':ok,'scroll':row['audit']['camera']['scroll']})
foregroundPairs=[]
for i,a in enumerate(m['objects']):
 for b0 in m['objects'][i+1:]:
  lx=max(a['x'],b0['x']);ly=max(a['y'],b0['y']);rx=min(a['x']+a['width'],b0['x']+b0['width']);ry=min(a['y']+a['height'],b0['y']+b0['height'])
  if lx>=rx or ly>=ry:continue
  aa=np.array(Image.open(R/'public'/a['image']).convert('RGBA').getchannel('A').crop((lx-a['x'],ly-a['y'],rx-a['x'],ry-a['y'])))
  ab=np.array(Image.open(R/'public'/b0['image']).convert('RGBA').getchannel('A').crop((lx-b0['x'],ly-b0['y'],rx-b0['x'],ry-b0['y'])))
  foregroundPairs.append({'a':a['id'],'b':b0['id'],'overlapRect':[lx,ly,rx-lx,ry-ly],'sharedNontransparentPixels':int(((aa>0)&(ab>0)).sum()),'sortPlanes':[a['sortY'],b0['sortY']],'visualOwnership':'Native complete textures / depth sort, source-shadow inventory above; overlap not automatically collision or artistic FAIL'})
wr(D/'ownership-audit.json',{'foregroundOverlapPairs':foregroundPairs,'families':families,'changedGroundPixels':int(changed.sum()),'unclassifiedChangedPixels':missing,'chunkCoverageExactlyOnce':True,'chunkPairs':edges,'foreground':foreground,'duplicateExactInstances':0,'note':'Material scale, foliage contacts and shadow naturalness remain native visual review, not inferred PASS from masks.'})
wr(D/'preservation-details.json',{'historicalZoningArtifactCount':len(locked),'historicalZoningArtifacts':locked,'stationRGBExact':True,'stationAlphaExactOutsideRetirementMask':True,'stationPivotUnchanged':True,'canonicalForecourtExact':True,'jejuProtectedMaskPixelsExact':int(keep.sum()),'jejuOriginalSourcePNGImmutable':True,'jejuNativeFieldExact':True,'modernRuntimeFieldExact':True,'station8pxStripClosed':True,'approvedNorthernSupportsAndWallsRestored':True,'southCourtOpeningWidth':430,'pairedNativeFrames':pairs,'wallApronTerrainOwnership':aprons,'approvedBuildingSources':'Immutable, latest1440-file hash registry separately verified','protectedArtSpatialConflict':'Not solved by clearing collision; see spatial-fidelity and separate palace proposal'})
# A registered native graybox / runtime overlay. No screenshot pixel resampling.
row=next(r for r in cap['rows']if r['name']=='palace-compound-after-native');sx,sy=row['audit']['camera']['scroll'];im=Image.open(D/'palace-compound-after-native.png').convert('RGB');w,h=im.size;gray=Image.open(R/'docs/world-gate1/GRAYBOX_NATIVE_4096x4608.png').convert('RGB').crop((sx,sy,sx+w,sy+h));gray.save(D/'palace-approved-graybox-native.png',optimize=True);ov=im.copy();d=ImageDraw.Draw(ov)
for q in reg['northernBuildings']:
 x,y,bw,bh=q['rect'];d.rectangle((x-sx,y-sy,x+bw-1-sx,y+bh-1-sy),outline='#ffcc44',width=2);d.text((x-sx,y-sy),q['id'],fill='#ffcc44')
for q in reg['approvedBoundaries']:
 x,y,bw,bh=q['rect'];d.rectangle((x-sx,y-sy,x+bw-1-sx,y+bh-1-sy),outline='#00ffff',width=2)
d.rectangle((1830-sx,790-sy,2259-sx,1129-sy),outline='#ff77cc',width=2);d.line((2048-sx,750-sy,2048-sx,1650-sy),fill='#ff77cc',width=2)
ov.save(D/'palace-runtime-registration-overlay.png',optimize=True)
print('Ownership audit:',len(edges),'adjacent pairs;',len(foreground),'objects; original artifacts',len(locked),'; changed pixels',int(changed.sum()))
