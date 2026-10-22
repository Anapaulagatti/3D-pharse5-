"""Two-object repair only: remove old baked planters/shadows, finish crisp native assets, preserve all else."""
from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import label
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate25-station-planters';D=R/'docs/gate25-station-planters';P=R/'public/assets/gate2';O=P/'district-planter-repair';W,H=3184,1214
base=Image.open(R/'assets-src/gate25-refinement/final-ground.png').convert('RGB');floor=Image.open(S/'clean-floor-host.png').convert('RGB').resize((608,188),Image.Resampling.NEAREST);floor.save(S/'clean-floor-native.png');full=Image.new('RGB',base.size);full.paste(floor,(2528,620));ground=base.copy();allowed=Image.new('L',base.size);dr=ImageDraw.Draw(allowed)
# Clear the complete old objects AND their diffuse shadows; lower-left cut protects tactile branch.
polygons=[[(2540,705),(2724,705),(2747,719),(2766,738),(2766,775),(2736,775),(2736,799),(2538,799),(2538,725)],[(2900,705),(3115,705),(3130,733),(3130,798),(2895,798),(2895,727)]]
for poly in polygons:dr.polygon(poly,fill=255)
# Tactile paving (including both lower branches), facade/threshold, crosswalk and all surroundings stay exact.
d=ImageDraw.Draw(allowed);d.rectangle((2737,775,2900,812),fill=0);d.rectangle((2806,650,2844,812),fill=0)
ground.paste(full,(0,0),allowed);ground.save(S/'clean-underpainting.png');allowed.save(S/'removal-mask.png')
sheet=Image.open(S/'planter-sprites-host.png').convert('RGBA');objects=[];records=[];sprite_coverage=np.zeros((H,W),bool);shadow_coverage=np.zeros((H,W),bool)
for name,half,x,y in [('left',(0,0,991,793),2545,695),('right',(991,0,1983,793),2908,699)]:
 raw=sheet.crop(half);v=np.array(raw);yy,xx=np.where(v[:,:,3]>127);box=(int(xx.min()),int(yy.min()),int(xx.max())+1,int(yy.max())+1);crop=raw.crop(box);size=(190,round(crop.height*190/crop.width));native=crop.resize(size,Image.Resampling.NEAREST);a=np.array(native);rgb=a[:,:,:3].astype(int);alpha=a[:,:,3];h,w=alpha.shape
 # Cool cast/contact shadow separates from warm stone and green foliage; no gray matte is sent to GPU.
 stone=Image.new('L',(w,h));ImageDraw.Draw(stone).polygon([(int(w*.015),int(h*.55)),(int(w*.90),int(h*.33)),(int(w*.95),int(h*.33)),(int(w*.95),int(h*.81)),(int(w*.90),int(h*.97)),(int(w*.66),int(h*.97)),(int(w*.66),int(h*.91)),(int(w*.28),int(h*.91)),(int(w*.28),int(h*.97)),(int(w*.015),int(h*.97))],fill=255)
 shadow=(alpha>=128)&(rgb[:,:,2]>rgb[:,:,0]+5)&(rgb[:,:,2]>=rgb[:,:,1]-2)&(np.arange(h)[:,None]>h*.55)&(np.array(stone)==0)
 body=(alpha>=128)&(~shadow);alpha_body=body.astype('uint8')*255
 assert np.all(alpha_body[int(h*.70):int(h*.83),int(w*.30):int(w*.63)]==255),'Opaque central stone face must not contain cutout holes'
 # Palette finishing changes color only, never position/size. No dithering or interpolated sampling.
 indexed=Image.fromarray(a[:,:,:3]).quantize(colors=128,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB');body_rgb=np.array(indexed);body_rgb[~body]=0;body_im=Image.fromarray(np.dstack([body_rgb,alpha_body]));body_im.save(O/(name+'-planter.png'))
 shadow_alpha=np.zeros_like(alpha);shadow_alpha[shadow]=64;shadow_alpha[shadow&(rgb.mean(2)<45)]=96;shadow_rgba=np.zeros_like(a);shadow_rgba[:,:,:3]=[30,28,26];shadow_rgba[:,:,3]=shadow_alpha;shadow_rgba[shadow_alpha==0,:3]=0;shadow_im=Image.fromarray(shadow_rgba);shadow_im.save(S/(name+'-owned-shadow.png'))
 # One associated native shadow bake into clean ground; sprite remains separately Y-sorted.
 g=ground.convert('RGBA');g.alpha_composite(shadow_im,(x,y));ground=g.convert('RGB');sprite_coverage[y:y+h,x:x+w]|=body;shadow_coverage[y:y+h,x:x+w]|=shadow
 objects.append(dict(id='station-planter-'+name,image='district-planter-repair/'+name+'-planter.png',x=x,y=y,width=w,height=h,sortY=778,alphaSoftening=1))
 records.append(dict(id=name,hostSheetHalf=half,cropWithinHalf=box,hostCropSize=crop.size,nativeSize=size,finish='single intentional NEAREST downsample;128-color MEDIANCUT/no dithering; hard alpha128 threshold',worldOrigin=[x,y],footRootY=778,bodyAlphaLevels=[int(n)for n in np.unique(alpha_body)],transparentRgbZero=bool((body_rgb[~body]==0).all()),shadowAlphaLevels=[int(n)for n in np.unique(shadow_alpha)],runtimeResampling='NONE at native zoom1',nativeSpriteSha256=hashlib.sha256((O/(name+'-planter.png')).read_bytes()).hexdigest()))
# Native ground textures preserve exactly the existing ownership windows.
old=json.loads((P/'district-refinement/scene.json').read_text());scene=json.loads(json.dumps(old));scene.update(id='district-planter-repair',label='Gate2.5 · station planter repair / human review pending',grounds=[]);scene['objects']+=objects
for index,(name,x,end) in enumerate([('west',0,1512),('center',1512,2488),('east',2488,W)]):
 if index<2:scene['grounds'].append(dict(old['grounds'][index]))
 else:
  ground.crop((x,0,end,H)).save(O/(name+'.png'));scene['grounds'].append(dict(id=name,image='district-planter-repair/'+name+'.png',x=x,y=0,width=end-x,height=H))
for name in ['west.png','center.png']:
 if (O/name).exists():(O/name).unlink()

ground.save(S/'final-clean-ground.png');expected=ground.convert('RGBA')
for ob in objects:expected.alpha_composite(Image.open(P/ob['image']),(ob['x'],ob['y']))
expected.convert('RGB').save(S/'expected-native-composite.png')
# Local foot solids; keep every existing clearance pixel outside the two original object reservations.
walk=Image.open(P/'district-refinement/walk.png').convert('L');before=np.array(walk);wd=ImageDraw.Draw(walk);foot_regions=[(2540,705,2736,797),(2900,705,3118,797)];solids=[(2549,752,2726,779),(2912,752,3089,779)]
for b in foot_regions:wd.rectangle(b,fill=255)
for b in solids:wd.rectangle(b,fill=0)
walk.save(O/'walk.png');scene['mask']='district-planter-repair/walk.png';scene['limitations']='Only two station planters/source ownership and their local foot solids changed. Human quality approval pending. Gate3 locked; physical devices NOT TESTED.';(O/'scene.json').write_text(json.dumps(scene,ensure_ascii=False,indent=2)+'\n')
# Exact protected regions, clearance and localized ownership proof.
a=np.array(ground);b=np.array(base);authorized=(np.array(allowed)>0)|shadow_coverage;assert not np.any((a!=b).any(2)&(~authorized));assert np.array_equal(a[:697],b[:697]);assert np.array_equal(a[:,2768:2895],b[:,2768:2895]);assert np.array_equal(a[812:],b[812:])
wa=np.array(walk);assert np.array_equal(wa[:,2768:2895],before[:,2768:2895]);assert np.all(wa[697:821,2780:2869]>127);components,n=label(wa>127);root=components[780,1200];assert root
for t in scene['targets']:assert components[t['y'],t['x']]==root
cat=json.loads((P/'catalog.json').read_text());cat=[c for c in cat if c['id']!=scene['id']]
for c in cat:
 if c['id']=='district-refinement':c['label']='HISTORY · refinement / approval qualified by planter defect'
cat.append(dict(id=scene['id'],label='CURRENT · station planter repair / review pending'));(P/'catalog.json').write_text(json.dumps(cat,ensure_ascii=False,indent=2)+'\n')
proof=dict(worldSize=[W,H],newPlanterObjects=objects,newPlanterRecords=records,oldBakedObjectsRemovedBeforeLayering=True,removalMask='assets-src/gate25-station-planters/removal-mask.png',originalGroundUnmodified=True,stationFacadeAndDoorExact=True,MuneumAndBakeryExact=True,centralStripRGBAndCollisionExact=[2768,2895],continuousNativeEntranceClearancePixels=89,clearanceRectangle=[2780,697,2869,821],tactileAndCrosswalkExact=True,foregroundAndJuniPreserved=True,oldForegroundObjectsUnchanged=scene['objects'][:len(old['objects'])]==old['objects'],footSolids=solids,collisionChangesOnlyInside=foot_regions,existingEntranceTargetsConnected=True,chunkEdges=[1512,2488],chunks=3,changedGroundPixels=int((a!=b).any(2).sum()),humanVisualQuality='PENDING_DIRECT_HUMAN_REVIEW')
(D/'asset-proof.json').write_text(json.dumps(proof,indent=2)+'\n');expected.convert('RGB').crop((2500,540,3184,835)).save(S/'authored-frontage-preview.png');print('PASS targeted removal / native sprites+owned shadows / exact architecture+tactile / entrance clearance; art approval PENDING')
