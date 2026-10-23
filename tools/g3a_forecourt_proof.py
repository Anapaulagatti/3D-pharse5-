"""Read-only forecourt lineage, extraction and real-Phaser native pixel comparison."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib,subprocess
R=Path(__file__).resolve().parents[1];D=R/'docs/g3a-forecourt-audit';S=R/'assets-src/gate25-station-planters';W,H=3184,1214
rois={'entrance-ground':(2768,706,2895,775),'tactile-strip':(2798,700,2853,813),'left-planter-pavement':(2528,756,2775,813),'right-planter-pavement':(2895,756,3135,813),'crisp-door-reference':(2750,570,2895,680),'crisp-planter-reference':(2570,743,2715,779)}
original=np.array(Image.open(R/'assets-src/gate25-reconstruction/original-ground.png').convert('RGB'));raw=Image.open(R/'assets-src/gate25-reconstruction/ground-revised-host.png').convert('RGB');rawnative=np.array(raw.resize((W,H),Image.Resampling.NEAREST));protected=np.array(Image.open(R/'assets-src/gate25-reconstruction/architecture-protection-final.png'))>0
reconstructed=np.array(Image.open(R/'assets-src/gate25-reconstruction/reconstructed-ground.png').convert('RGB'));refined=np.array(Image.open(R/'assets-src/gate25-refinement/final-ground.png').convert('RGB'));final=Image.open(S/'final-clean-ground.png').convert('RGBA');finalrgb=np.array(final.convert('RGB'));owner=np.zeros((H,W),np.uint8);owner[protected]=1
# Distinguish same-Y native bollard underpainting from the host background.
fg=json.loads((R/'assets-src/gate25-reconstruction/foreground-ownership.json').read_text())
for o in fg['bollards']:
 a=np.array(Image.open(R/'public/assets/gate2'/o['image']).convert('RGBA'))[:,:,3]>0;x,y=o['x'],o['y'];owner[y:y+a.shape[0],x:x+a.shape[1]][a]=2
refinemask=np.array(Image.open(R/'assets-src/gate25-refinement/combined-edit-mask.png'))>0;owner[refinemask]=3
removal=np.array(Image.open(S/'removal-mask.png'))>0;owner[removal]=4
for name,x,y in [('left',2545,695),('right',2908,699)]:
 a=np.array(Image.open(S/(name+'-owned-shadow.png')).convert('RGBA'))[:,:,3]>0;owner[y:y+a.shape[0],x:x+a.shape[1]][a]=5
names=['host background finished2030x775→3184x1214 NEAREST','protected original native architecture/source','same-Y native paver underpainting below original bollard','local refinement host finish under binary mask','planter-removal floor2170x725→608x188 NEAREST','separately owned native shadow bake']
# Reproduce only the latest floor/shadow composites, without writing source assets.
floor=Image.open(S/'clean-floor-host.png').convert('RGB').resize((608,188),Image.Resampling.NEAREST);assert np.array_equal(np.array(floor),np.array(Image.open(S/'clean-floor-native.png').convert('RGB')))
rebuilt=Image.fromarray(refined).convert('RGBA');temp=Image.new('RGBA',(W,H));temp.paste(floor,(2528,620));rebuilt.paste(temp,(0,0),Image.fromarray(removal.astype('uint8')*255))
for name,x,y in [('left',2545,695),('right',2908,699)]:rebuilt.alpha_composite(Image.open(S/(name+'-owned-shadow.png')).convert('RGBA'),(x,y))
assert np.array_equal(np.array(rebuilt.convert('RGB')),finalrgb)
# Verify extraction and chunking as a separate stage from source painting.
box=(2500,690,3184,900);expectedPatch=finalrgb[690:900,2500:3184];m=json.loads((R/'public/assets/gate3/registration-refined/manifest.json').read_text());patch=Image.new('RGBA',(684,210))
for c in m['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];ax,ay=max(2274,x),max(2603,y);bx,by=min(2958,x+w),min(2813,y+h)
 if bx>ax and by>ay:patch.paste(Image.open(R/'public'/c['image']).convert('RGBA').crop((ax-x,ay-y,bx-x,by-y)),(ax-2274,ay-2603))
assert np.array_equal(np.array(patch)[:,:,:3],expectedPatch);assert np.all(np.array(patch)[:,:,3]==255)
# East source texture is also a literal crop of the same final-clean ground.
east=np.array(Image.open(R/'public/assets/gate2/district-planter-repair/east.png').convert('RGB'));assert np.array_equal(east[690:900,12:696],expectedPatch)
visible=np.ones((H,W),bool)
for o in json.loads((R/'public/assets/gate3/district/manifest.json').read_text())['objects']:
 a=np.array(Image.open(R/'public'/o['image']).convert('RGBA'))[:,:,3]>0;x,y=o['x'],o['y'];visible[y:y+a.shape[0],x:x+a.shape[1]][a]=False
lineage=[]
for name,(x,y,x2,y2)in rois.items():
 region=finalrgb[y:y2,x:x2];codes=owner[y:y2,x:x2];n=region.shape[0]*region.shape[1]
 lineage.append({'roi':name,'sourceBox':[x,y,x2,y2],'pixels':n,'ownership':[{ 'stage':names[int(k)],'pixels':int(np.sum(codes==k))}for k in np.unique(codes)],'equalRawFinishedPixels':int(np.all(region==rawnative[y:y2,x:x2],2).sum()),'equalOriginalNativePixels':int(np.all(region==original[y:y2,x:x2],2).sum()),'visibleGroundPixels':int(visible[y:y2,x:x2].sum()),'visibleGroundOwnership':[{ 'stage':names[int(k)],'pixels':int(np.sum((codes==k)&visible[y:y2,x:x2]))}for k in np.unique(codes)if np.any((codes==k)&visible[y:y2,x:x2])],'rawFinishIsNotRuntimeResampling':True})
 Image.fromarray(region).save(D/(name+'-stored-ground-1x.png'))
 # Original native reference is a recovery source, not an applied fix or claimed current gameplay.
 Image.fromarray(original[y:y2,x:x2]).save(D/(name+'-original-recovery-reference-1x.png'))
# Expected composites use the actual scene foreground ownership, not a facade-only comparison.
captures=json.loads((D/'captures.json').read_text());results=[]
for r in captures['rows']:
 scene=r['scene'];manifest=json.loads((R/f'public/assets/gate3/{scene}/manifest.json').read_text());expected=final.copy();dx,dy=(0,0)if scene=='district'else(-226,1913)
 for o in sorted(manifest['objects'],key=lambda o:o['sortY']):
  x,y=o['x']-dx,o['y']-dy
  if x+o['width']<2500 or x>3184 or y+o['height']<540 or y>835:continue
  expected.alpha_composite(Image.open(R/'public'/o['image']).convert('RGBA'),(x,y))
 mat=r['audit']['camera']['matrix'];vx,vy=-mat[4],-mat[5];assert all(float(v).is_integer()for v in [vx,vy]);shot=Image.open(D/r['path']).convert('RGB');suffix=f"{scene}-{r['renderer']}-{r['phase']}"
 for name,(x,y,x2,y2)in rois.items():
  world=[x+dx,y+dy,x2+dx,y2+dy];crop=shot.crop(tuple(int(v)for v in [world[0]-vx,world[1]-vy,world[2]-vx,world[3]-vy]));source=expected.crop((x,y,x2,y2)).convert('RGB');a,b=np.array(crop),np.array(source);diff=np.max(abs(a.astype(int)-b.astype(int)),2)
  results.append({'case':suffix,'roi':name,'pixels':int(diff.size),'differentFromExpectedSourceComposite':int((diff>0).sum()),'maxDelta':int(diff.max())});assert not np.any(diff),(suffix,name)
  crop.save(D/f'{name}-{suffix}-1x.png',optimize=True)
  if r['scene']=='district'and r['renderer']=='auto':
   crop.save(D/f'{name}-{r["phase"]}-1x.png',optimize=True)
   if r['phase']=='after':source.save(D/f'{name}-source-composite-1x.png',optimize=True)
 assert all(o['position'][0].is_integer()if isinstance(o['position'][0],float)else isinstance(o['position'][0],int)for o in r['audit']['layers'])
 assert all(o['scale']==[1,1]and o['scaleMode']==1 and o.get('minFilter',9728)==9728 and o.get('magFilter',9728)==9728 for o in r['audit']['layers'])
for name in rois:
 assert (D/f'{name}-before-1x.png').read_bytes()==(D/f'{name}-after-1x.png').read_bytes()
# Native1x contact sheet: no scaling, sharpening or browser fit. Labels are outside the crops.
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14);sheet=Image.new('RGB',(960,800),'#17242e');d=ImageDraw.Draw(sheet)
for i,t in enumerate(['Stored source / expected composite','Before focused audit','After audit / source unchanged']):d.text((i*320+8,8),t,font=font,fill='white')
y=40
for name in rois:
 d.text((8,y),name+' / native1x',font=font,fill='#f5d6a0');y+=24
 for col,tag in enumerate(['source-composite','before','after']):
  im=Image.open(D/f'{name}-{tag}-1x.png');sheet.paste(im,(col*320+8,y))
 y+=Image.open(D/f'{name}-before-1x.png').height+24
sheet.save(D/'NATIVE_1X_COMPARISON.png',optimize=True)
recovery=Image.new('RGB',(720,560),'#17242e');dr=ImageDraw.Draw(recovery);dr.text((8,8),'Current forecourt / still soft',font=font,fill='white');dr.text((368,8),'Earlier native source / REFERENCE ONLY',font=font,fill='white');yy=40
for name in list(rois)[:4]:
 dr.text((8,yy),name+' / native1x, no resizing',font=font,fill='#f5d6a0');yy+=24
 for col,tag in enumerate(['after','original-recovery-reference']):
  im=Image.open(D/f'{name}-{tag}-1x.png');recovery.paste(im,(col*360+8,yy))
 yy+=Image.open(D/f'{name}-after-1x.png').height+24
recovery.save(D/'NATIVE_RECOVERY_REFERENCE_NOT_APPLIED.png',optimize=True)
# A review-only edit-mask proposal, not applied to a source or runtime texture.
mask=Image.new('L',(684,210));d=ImageDraw.Draw(mask);d.rectangle((0,7,683,122),fill=255) # source y697..812 only
# Protect original architecture, current tactile guards, complete original foreground bounds and source bodies.
p=Image.fromarray(protected[690:900,2500:3184].astype('uint8')*255);ma=np.array(mask);ma[np.array(p)>0]=0
for o in json.loads((R/'public/assets/gate3/district/manifest.json').read_text())['objects']:
 x,y=o['x']-2500,o['y']-690
 if x+o['width']>0 and x<684 and y+o['height']>0 and y<210:ma[max(0,y):min(210,y+o['height']),max(0,x):min(684,x+o['width'])]=0
for x,y,x2,y2 in [(2737,775,2901,813),(2806,650,2845,813)]:ma[max(0,y-690):min(210,y2-690),max(0,x-2500):min(684,x2-2500)]=0
Image.fromarray(ma).save(D/'CONSERVATIVE_REVIEW_BOUNDARY_NOT_APPLIED.png')
# Forecourt visual baseline remains FAIL; preservation/transport fidelity is a separate result.
protectedFiles=json.loads((R/'docs/gate3a/protected-assets.json').read_text())['sha256'];assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==h for p,h in protectedFiles.items())
for p in (R/'src/gate3').rglob('*'):
 if p.is_file():assert p.read_bytes()==subprocess.check_output(['git','show','b7cf611:'+str(p.relative_to(R))],cwd=R)
proof={'status':'RUNTIME TRANSPORT PASS / FORECOURT VISUAL SOFTNESS FAIL-OPEN','lineage':lineage,'patchExtraction':{'sourceBox':list(box),'worldRasterOrigin':[2274,2603],'translation':[-226,1913],'nativeSize':[684,210],'comparedPixels':684*210,'different':0,'alphaOpaqueEverywhere':True,'filterOrFeatherApplied':False},'floorAuthoringResize':{'input':[2170,725],'output':[608,188],'filter':'historical NEAREST, not runtime','xScale':608/2170,'yScale':188/725,'aspectRatioChange':(608/188)/(2170/725)},'sourceCompositeRebuild':'PASS exact floor/owned-shadow recipe','nativeReadback':results,'beforeAfterAuditCrops':'byte-identical / NO VISUAL REPAIR CLAIM','unchangedProtectedFiles':len(protectedFiles),'runtimeFilesUnchangedFrom':'b7cf611','newSourceArtApplied':False,'G3B':'BLOCKED'}
(D/'proof.json').write_text(json.dumps(proof,indent=2)+'\n');print('PASS',len(results),'native ROI source/composite matches; exact143640px extraction; source-art softness remains FAIL-OPEN');print([(r['roi'],r['ownership'])for r in lineage])
