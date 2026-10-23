"""Isolated native floor recovery. No resize, filtering, approved-source writes or mask edits."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate3/forecourt-restoration';P=R/'public/assets/gate3/registration-forecourt';D=R/'docs/g3a-forecourt-restoration'
if (R/'assets-src/gate3/approved-station-forecourt.json').exists():
 raise SystemExit('Approved forecourt is frozen. Reuse approved-station-forecourt.json; do not regenerate accepted pixels. Historical reproduction: use the pre-approval checkpoint in a separate checkout.')
for p in [S,P,D]:p.mkdir(parents=True,exist_ok=True)
box=(2500,690,3184,900);W,H=684,210
old=np.array(Image.open(R/'assets-src/gate25-station-planters/final-clean-ground.png').convert('RGB'));native=np.array(Image.open(R/'assets-src/gate25-reconstruction/original-ground.png').convert('RGB'))
def mask(polys):
 im=Image.new('L',(3184,1214));d=ImageDraw.Draw(im)
 for p in polys:d.polygon(p,fill=255)
 return np.array(im)>0
# Follow the forecourt perimeter; retain the existing lamp/tree pockets, facade and curb.
editable=mask([[(2500,705),(3110,705),(3110,756),(3136,756),(3136,811),(2500,811)]])
architecture=np.array(Image.open(R/'assets-src/gate25-reconstruction/architecture-protection-final.png').convert('L'))>0
editable &= ~architecture
# Current route measured before editing. Explicit locked silhouettes; no route/width/turn changes.
tactile=mask([[(2816,705),(2834,705),(2834,751),(2816,751)],[(2803,775),(2848,775),(2848,795),(2803,795)],[(2771,796),(2803,796),(2803,810),(2771,810)],[(2849,796),(2887,796),(2887,810),(2849,810)]]) & editable
# Native source props AND their cast shadows are not recoverable ground. Cover entire ownership,
# including pixels hidden by current opaque planter bodies; no old shadow is retained underneath.
retired=mask([[(2562,705),(2786,705),(2786,773),(2771,773),(2771,800),(2538,800),(2538,758),(2562,758)],[(2880,705),(3110,705),(3110,756),(3130,756),(3130,801),(2880,801)]])
retired |= mask([[(2500,705),(2562,705),(2562,811),(2500,811)]])
for cx,top in [(2533,782),(2615,792),(2747,782),(2909,782),(3027,793),(3120,782)]:
 retired |= mask([[(cx-16,top-2),(cx+35,top-2),(cx+35,811),(cx-16,811)]])
# Native material translation only. Same perspective rows, no interpolation. Three source
# strips avoid all baked props and tactile material. Integer horizontal tiling fills only
# occluded/retired-object ground; the unoccluded native paving remains at exact coordinates.
rest=native.copy();sy,sx=np.indices(old.shape[:2]);donorx=sx.copy();donory=sy.copy()
for y in range(705,812):
 start,width=(2850,29) if y<797 else (2804,44)
 for x in range(2500,3137):
  if retired[y,x] or (not tactile[y,x] and ((2814<=x<=2835 and y<=753) or (2786<=x<=2850 and 773<=y<=797) or (2768<=x<=2889 and y>=795))):
   xx=start+(x-start)%width
   rest[y,x]=native[y,xx];donorx[y,x]=xx
# Recover native tactile material inside the CURRENT locked route, never its old silhouette.
# Single-pixel row/column extension uses neighboring native material, not a rescale.
for y,x in zip(*np.where(tactile)):
 if y<=751:xx=min(x,2832);yy=y
 elif y<=795:xx=min(max(x,2804),2847);yy=y
 elif x<2820:xx=min(max(x,2773),2801);yy=min(y,810)
 else:xx=min(max(x,2849),2882);yy=min(y,810)
 rest[y,x]=native[yy,xx];donorx[y,x]=xx;donory[y,x]=yy
clean=old.copy();clean[editable]=rest[editable]
# Keep the original independent shadow art exactly; composite once over restored ground.
shadowmask=np.zeros(editable.shape,bool);floor=Image.fromarray(clean).convert('RGBA')
for name,x,y in [('left',2545,695),('right',2908,699)]:
 shadow=Image.open(R/f'assets-src/gate25-station-planters/{name}-owned-shadow.png').convert('RGBA');a=np.array(shadow);inside=editable[y:y+a.shape[0],x:x+a.shape[1]]
 # Original shadow pixels outside repair already exist in old; do not double-bake them.
 a[:,:,3][~inside]=0;floor.alpha_composite(Image.fromarray(a),(x,y));shadowmask[y:y+a.shape[0],x:x+a.shape[1]] |= (a[:,:,3]>0)
result=np.array(floor.convert('RGB'));changed=np.any(result!=old,2)
assert not np.any(changed&~editable)
assert np.array_equal(result[812:],old[812:]);assert not np.any(changed&architecture)
for name,a in [('repair-mask',editable),('tactile-locked-mask',tactile),('retired-props-exclusion-mask',retired&editable),('owned-shadow-mask',shadowmask),('changed-pixels-mask',changed)]:Image.fromarray(a.astype('uint8')*255).crop(box).save(S/(name+'.png'))
Image.fromarray(clean).crop(box).save(S/'native-clean-ground.png');Image.fromarray(result).crop(box).save(S/'restored-ground.png')
# Each restored pixel has an explicit native reference coordinate, before unchanged shadow ownership.
np.savez_compressed(S/'native-source-map.npz',x=donorx[690:900,2500:3184].astype('uint16'),y=donory[690:900,2500:3184].astype('uint16'))
manifest=json.loads((R/'public/assets/gate3/registration-refined/manifest.json').read_text());baseline=json.loads(json.dumps(manifest));manifest['id']='registration-forecourt';manifest['artStatus']='ISOLATED native ground restoration candidate; human visual approval pending; G3-B BLOCKED'
changedchunks=[]
for c in manifest['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];ax,ay=max(x,2274),max(y,2603);bx,by=min(x+w,2958),min(y+h,2813)
 if bx<=ax or by<=ay:continue
 tex=Image.open(R/'public'/c['image']).convert('RGBA');arr=np.array(tex);before=arr.copy()
 submask=editable[ay-1913:by-1913,ax+226:bx+226];sub=result[ay-1913:by-1913,ax+226:bx+226]
 view=arr[ay-y:by-y,ax-x:bx-x];view[:,:,:3][submask]=sub[submask]
 if np.array_equal(arr,before):continue
 path=P/(c['id']+'.png');Image.fromarray(arr).save(path);c['image']=str(path.relative_to(R/'public'));c['sha256']=hashlib.sha256(path.read_bytes()).hexdigest();changedchunks.append(c['id'])
assert changedchunks==['4-5','5-5'];assert manifest['objects']==baseline['objects'];assert manifest['logicalSolids']==baseline['logicalSolids'];assert [c['mask']for c in manifest['chunks']]==[c['mask']for c in baseline['chunks']]
(P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
provenance={'scope':'Candidate only, source rectangle [2500,690,3184,900], world raster [2274,2603]','source':'assets-src/gate25-reconstruction/original-ground.png','baseline':'assets-src/gate25-station-planters/final-clean-ground.png','sourceBox':box,'sourceToWorld':[-226,1913],'nativeRecoveredAtSameCoordinate':int(np.sum(editable&~tactile&~retired&(donorx==sx)&(donory==sy))),'nativeReferenceMaterialPixels':int(np.sum(editable&((donorx!=sx)|(donory!=sy)))),'editablePixels':int(editable.sum()),'changedPixels':int(changed.sum()),'affectedChunks':changedchunks,'resizingFilteringSharpening':'NONE','tactilePolicy':'Locked current route masks; native material copied within silhouette, no collision/route changes','shadowPolicy':'Original independent RGBA; composite once over clean restored ownership only','sourceMap':'native-source-map.npz: global original-source x/y for every patch pixel; consult repair-mask first','missingGround':'Native same-row clean strips translated in integer pixels only beneath retired props/shadows; no old benches, planter bodies or bollards copied','protectedSourceFiles':'All immutable; verified separately','humanVisualApproval':'PENDING'}
(S/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n');print(json.dumps(provenance,indent=2))
