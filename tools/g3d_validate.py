from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,subprocess
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-recovery';S=R/'assets-src/gate3/recovery'
def read(p):return json.loads((R/p).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=read('public/assets/gate3/recovery-pilots/manifest.json');old=read('public/assets/gate3/production/manifest.json');shots=read('docs/gate3-recovery/native-captures.json');ground=Image.new('RGBA',tuple(m['size']));field=np.zeros(tuple(reversed(m['size'])),np.uint8)
for c in m['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];ground.paste(Image.open(R/'public'/c['image']),(x,y));field[y:y+h,x:x+w]=np.frombuffer((R/'public'/c['mask']).read_bytes(),np.uint8).reshape(h,w)
readback=[]
for n in ['north','south','namsan']:
 row=next(r for r in shots['rows']if r['name']==n+'-candidate-native');sx,sy=row['audit']['camera']['scroll'];actual=Image.open(D/(n+'-candidate-native.png')).convert('RGB');ground_view=ground.crop((sx,sy,sx+1280,sy+900));expected=Image.alpha_composite(Image.new('RGBA',ground_view.size,'#33494a'),ground_view).convert('RGB');eligible=Image.new('L',actual.size,255);d=ImageDraw.Draw(eligible)
 for ob in m['objects']:d.rectangle((ob['x']-sx,ob['y']-sy,ob['x']+ob['width']-sx-1,ob['y']+ob['height']-sy-1),fill=0)
 px,py=row['state']['x'],row['state']['y'];d.rectangle((px-sx-60,py-sy-130,px-sx+60,py-sy+10),fill=0)
 legacy_alpha_excluded=int(np.count_nonzero((np.array(eligible)>0)&(np.array(ground_view)[:,:,3]<255)));mask=(np.array(eligible)>0)&(np.array(ground_view)[:,:,3]==255);delta=np.any(np.array(actual)!=np.array(expected),axis=2);readback.append({'pilot':n,'comparedOpaqueGroundPixels':int(mask.sum()),'excludedLegacyTranslucentPixels':legacy_alpha_excluded,'scope':'Opaque native ground, excluding foreground/avatar. Legacy translucent unedited paving uses ordinary premultiplied blending, not a new renderer defect.','mismatchedPixels':int((delta&mask).sum()),'status':'PASS'if not np.any(delta&mask)else'FAIL','camera':row['audit']['camera'],'layerSamplingAndScaleExact':all(l.get('scale')==[1,1]and l.get('scaleMode')==1 for l in row['audit']['layers'])})
# Protected station appearance comparison excludes only avatar animation area.
before=Image.open(D/'station-before-native.png').convert('RGB');after=Image.open(D/'station-candidate-native.png').convert('RGB');row=next(r for r in shots['rows']if r['name']=='station-candidate-native');sx,sy=row['audit']['camera']['scroll'];box=(2274-sx,2196-sy,2958-sx,2813-sy);a=np.array(before.crop(box));b=np.array(after.crop(box));stationdiff=np.any(a!=b,axis=2);px,py=row['state']['x'],row['state']['y'];stationdiff[max(0,int(py-2196-130)):min(stationdiff.shape[0],int(py-2196+10)),max(0,int(px-2274-60)):min(stationdiff.shape[1],int(px-2274+60))]=False
checks={}
for name,path in [('approved','docs/g3a-controlled-finalization/protected-assets.json'),('rejected-baseline','assets-src/gate3/recovery/baseline-lock.json')]:
 j=read(path);bad=[p for p,h in j['sha256'].items()if sha(R/p)!=h];checks[name]={'count':len(j['sha256']),'failures':bad,'status':'FAIL'if bad else'PASS'}
# Artifact hashes and native placement invariants.
for ob in m['objects']:assert isinstance(ob['x'],int)and isinstance(ob['y'],int),ob['id']
assert not np.any(field[2626:2755,2950:2958]);assert all(o in m['objects']for o in old['objects']if not o['id'].startswith('production/'))
for x,y,path in [(640,650,'public/assets/gate2/a/ground.png'),(3180,3200,'public/assets/gate2/c/ground.png'),(2274,2603,'assets-src/gate3/forecourt-restoration/restored-ground.png')]:
 im=Image.open(R/path).convert('RGBA');assert ground.crop((x,y,x+im.width,y+im.height)).tobytes()==im.tobytes()
core=[]
for name in ['NativeTexture.ts','PixelGrid.ts','FoundationCamera.ts','Registration.ts','WorldCache.ts','ResourcePool.ts']:
 path='src/gate3/'+name;core.append({'file':path,'unchanged':(R/path).read_bytes()==subprocess.check_output(['git','show','9de752a:'+path],cwd=R)})
oldrefs=read('assets-src/gate3/recovery/baseline-lock.json')['historicalRefs'];now=subprocess.check_output(['git','show-ref','--tags'],text=True,cwd=R);tags=all(line in now.splitlines()for line in oldrefs.splitlines())
movement=read('docs/gate3-recovery/movement-report.json');qa={'method':'Meaningful native renderer/source/mask preservation + actual movement; not artistic acceptance','protectedHashRegistries':checks,'historicalTagsUnchanged':tags,'engineCore':core,'nativeGroundReadback':readback,'protectedStationPixelComparison':{'pixelsDifferentExcludingJuni':int(stationdiff.sum()),'regionWorld':[2274,2196,684,617],'status':'FAIL'if stationdiff.any()else'PASS'},'collisionOwnership':read('assets-src/gate3/recovery/integration-provenance.json')['collisionChanges'],'station8pxStrip':'UNCHANGED/CLOSED','approvedObjectRegistration':'ALL sources/coordinates/pivots unchanged','worldSize':m['size'],'chunksChanged':len(read('assets-src/gate3/recovery/integration-provenance.json')['changedChunks']),'actualMovement':[{'pilot':r['pilot'],'status':r['status'],'legs':len(r['legs'])}for r in movement['rows']],'pageErrors':shots['errors']+movement['errors'],'occlusion':'North/tower selected softening cases supplied; protected retail alpha1 fully hides Juni behind its visual envelope, OPEN P1, not visibility acceptance.','physicalAndroidChrome':'NOT TESTED','physicalIPhoneSafari':'NOT TESTED','hardwareWebGLPerformance':'NOT TESTED','fullWorldArt':'FAIL/HUMAN REJECTED; unchanged outside pilots','unifiedPilotArtApproval':'PENDING HUMAN REVIEW','bakery':'REQUIRED/UNPLACED; W0 retired, Q1 land not allocated','noFullWorldPropagation':True}
(D/'technical-qa.json').write_text(json.dumps(qa,indent=2)+'\n');(D/'protected-hashes.json').write_text(json.dumps({'hashes':checks,'core':core,'historicalTagsUnchanged':tags},indent=2)+'\n')
# Evidence crops of the explicit mask-only approach corrections.
for n,box,rect in [('north',(2470,990,2660,1140),(2508,1020,104,90)),('namsan',(1080,3180,1320,3310),(1160,3240,80,20))]:
 row=next(r for r in shots['rows']if r['name']==n+'-candidate-native');sx,sy=row['audit']['camera']['scroll'];im=Image.open(D/(n+'-candidate-native.png')).convert('RGBA').crop((box[0]-sx,box[1]-sy,box[2]-sx,box[3]-sy));overlay=Image.new('RGBA',im.size);dd=ImageDraw.Draw(overlay);x,y,w,h=rect;dd.rectangle((x-box[0],y-box[1],x+w-box[0]-1,y+h-box[1]-1),fill=(40,210,240,90),outline=(0,255,255,255),width=1);im.alpha_composite(overlay);im.save(D/(n+'-collision-ownership-overlay.png'),optimize=True)
# Density/correlation diagnostics, not artistic thresholds.
def measure(path,box):
 a=np.array(Image.open(R/path).convert('L').crop(box),float);out={'source':path,'box':box,'meanAdjacentLumaDelta':round(float((np.abs(np.diff(a,axis=1)).mean()+np.abs(np.diff(a,axis=0)).mean())/2),3),'autocorrelation':{}}
 for lag in [232,238,240,244,248]:
  if a.shape[1]>lag:
   x,y=a[:,:-lag].ravel(),a[:,lag:].ravel();out['autocorrelation'][str(lag)]=round(float(np.corrcoef(x,y)[0,1]),5)
 return out
metrics={
 'north':{'approved':('assets-src/gate3/recovery/approved-material-0.png',(0,0,320,210)),'before':('assets-src/gate3/recovery/north-ground-before.png',(700,100,1200,450)),'candidate':('assets-src/gate3/recovery/north-ground-derived.png',(780,70,1280,450))},
 'south':{'approved':('assets-src/gate3/recovery/approved-material-1.png',(0,0,320,210)),'before':('assets-src/gate3/recovery/south-ground-before.png',(200,100,700,500)),'candidate':('assets-src/gate3/recovery/south-ground-derived.png',(1230,150,1530,600))},
 'namsan':{'approved':('assets-src/gate3/recovery/approved-material-4.png',(0,0,320,210)),'before':('assets-src/gate3/recovery/namsan-ground-before.png',(700,300,1100,600)),'candidate':('assets-src/gate3/recovery/namsan-ground-derived.png',(700,300,1100,600))}}
(D/'material-density-diagnostics.json').write_text(json.dumps({'warning':'Different material/context samples; correlations show clone motifs, not craftsmanship score. No numeric art PASS threshold.','pilots':{n:{k:measure(*v)for k,v in spec.items()}for n,spec in metrics.items()}},indent=2)+'\n')
print(json.dumps({'readback':readback,'stationDifferent':int(stationdiff.sum()),'movement':qa['actualMovement']},indent=2))
