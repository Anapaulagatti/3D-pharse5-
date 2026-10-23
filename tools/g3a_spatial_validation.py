from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,heapq,math,subprocess
R=Path(__file__).resolve().parents[1];D=R/'docs/g3a-spatial-review';plan=json.loads((R/'assets-src/gate25/world-plan-v1.json').read_text());old=json.loads((R/'assets-src/gate3/registration/proposal-v1.json').read_text());new=json.loads((R/'assets-src/gate3/registration/proposal-v2-comparison.json').read_text());W,H=plan['size']
def rectmask(rect):
 m=Image.new('L',(W,H));x,y,w,h=rect;ImageDraw.Draw(m).rectangle((x,y,x+w-1,y+h-1),fill=255);return np.array(m)>0
def envelope(b):
 x,y=b['rasterOrigin'];a=b['sourceRect'];return [x,y,a[2]-a[0],a[3]-a[1]]
pathmasks={}
for p in plan['paths']:
 m=Image.new('L',(W,H));ImageDraw.Draw(m).line([tuple(pt)for pt in p['points']],fill=255,width=p['width'],joint='curve');pathmasks[p['id']]=np.array(m)>0
impacts=[]
for variant,proposal in [('waterfront-v1',old),('quay-maru-v2',new)]:
 for b in proposal['buildings']:
  if b['id']not in ['bakery','convenience']:continue
  c=rectmask(b['collision']);e=rectmask(envelope(b));impacts.append({'variant':variant,'building':b['id'],'contact':b['collision'],'envelope':envelope(b),'contactPathIntersections':[{'id':k,'pixels':int((c&m).sum())}for k,m in pathmasks.items()if np.any(c&m)],'visualPathIntersections':[{'id':k,'pixels':int((e&m).sum())}for k,m in pathmasks.items()if np.any(e&m)]})
manifest=json.loads((R/'public/assets/gate3/registration-refined/manifest.json').read_text());walk=np.zeros((H,W),np.uint8)
for c in manifest['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];walk[y:y+h,x:x+w]=np.frombuffer((R/'public'/c['mask']).read_bytes(),np.uint8).reshape(h,w)
def point(x,y):
 if any(x>=s['rect'][0]and y>=s['rect'][1]and x<s['rect'][0]+s['rect'][2]and y<s['rect'][1]+s['rect'][3]for s in manifest['logicalSolids']):return False
 return bool(0<=x<W and 0<=y<H and walk[math.floor(y+.5),math.floor(x+.5)]>127)
# Pixel exact known centreline checks, not snapped near-goal success.
routes=[]
checks=[('maru-front',[[700,3140],[700,3380],[326,3380],[326,3343]]),('namsan-west-loop',[[950,3280],[700,3140],[700,2920],[750,2800]]),('bakery-quay-approach',[[1490,3790],[1490,4790],[984,4790],[984,4770]]),('amusement-main-access',[[2048,3260],[2440,3260],[2440,3200]]),('main-avenue-south',[[2048,3260],[2048,3790]]),('island-arrival-main',[[2048,3480],[2900,3480],[3160,3480]]),('station-threshold',[[2598.5,2760],[2598.5,2610]])]
for name,pts in checks:
 bad=[];length=0
 for a,b in zip(pts,pts[1:]):
  dist=math.dist(a,b);length+=dist
  for i in range(math.ceil(dist)+1):
   t=i/max(1,math.ceil(dist));x=a[0]+(b[0]-a[0])*t;y=a[1]+(b[1]-a[1])*t
   if not point(x,y):bad.append([round(x,3),round(y,3)])
 routes.append({'id':name,'points':pts,'lengthPx':round(length,3),'walkSeconds':round(length/60,3),'status':'FAIL'if bad else'PASS','failedSamples':bad[:12],'method':'actual continuous logical solids + mask at JS-round; <=1px centreline steps including exact endpoints; not exhaustive navigation/visual acceptance'})
# Exact orthogonal foot-field widths, with declared physical reservation distinct from centre-position field.
def span(x,y,axis):
 if not point(x,y):return None
 lo=hi=x if axis=='x'else y
 while lo>0 and point(lo-1,y)if axis=='x'else lo>0 and point(x,lo-1):lo-=1
 limit=W if axis=='x'else H
 while hi+1<limit and (point(hi+1,y)if axis=='x'else point(x,hi+1)):hi+=1
 return {'first':lo,'last':hi,'centreFieldWidthPx':hi-lo+1}
clearances={'maruFrontGap':{'physicalGapPx':90,'JuniMaxVisibleWidthPx':49,'centreAtY':3380,'northSideVisualMarginPx':25.5,'southSideVisualMarginPx':15.5,'fieldAtX560':span(560,3380,'y')},'maruDoor':{'sourceCropLocalOpening':[112,395,68,117],'conservativeVisualClearWidthPx':68,'JuniMaxVisibleWidthPx':49,'nominalEachSidePx':9.5,'threshold':[326,3343],'centreField':span(326,3343,'x'),'limitation':'Opening identified by native visual inspection; a clear approach to existing door, not an implemented interior.'},'maruEastScenic':{'reservedWidthPx':100,'envelopeEastX':601,'pathCentreX':700,'envelopeToReservationGapPx':49},'maruWest':{'shoreGapPx':20,'publicAccess':False},'bakeryEastAccess':{'reservedWidthPx':96,'wallToCentrePx':65,'JuniSideToWallPx':40.5,'fieldAtY4500':span(1490,4500,'x')},'bakeryThreshold':{'point':[984,4770],'walkable':point(984,4770),'field':span(984,4770,'x')},'station':{'logicalAnchor':[2238.5,2180],'collider':[2322.5,2380,555,210],'threshold':[2598.5,2610],'sourceAisleWidthPx':89,'JuniWidthPx':49,'sideMarginPx':20,'continuousLeftInside':not point(2322.5,2400)}}
# Preserve entire approved art/renderer core and original candidate/default world manifests.
protected=json.loads((R/'docs/gate3a/protected-assets.json').read_text())['sha256'];assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in protected.items())
for path in ['src/gate3/FoundationCamera.ts','src/gate3/NativeTexture.ts','src/gate3/Registration.ts','src/gate3/PixelGrid.ts','public/assets/gate3/registration/manifest.json','public/assets/gate3/world/manifest.json','assets-src/gate25/world-plan-v1.json','assets-src/gate3/registration/proposal-v1.json']:
 assert (R/path).read_bytes()==subprocess.check_output(['git','show','46c6d2d:'+path],cwd=R),path
out={'routeImpacts':impacts,'routes':routes,'clearances':clearances,'protectedInputs':len(protected),'coreRendererAndOriginalPlansUnchanged':True,'fullNativeSizePreserved':True,'approvedMasterplanChanged':False,'landProposal':new['bakerySite'],'scope':'Targeted candidate only; geometry PASS is not artistic approval'}
(D/'spatial-validation.json').write_text(json.dumps(out,indent=2)+'\n');print([(r['id'],r['status'],r['failedSamples'][:2])for r in routes]);print(impacts);print(clearances)
