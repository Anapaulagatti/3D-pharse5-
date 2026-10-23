"""Readback/protection proof and unscaled native comparison evidence."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib,subprocess
R=Path(__file__).resolve().parents[1];D=R/'docs/g3a-forecourt-restoration';S=R/'assets-src/gate3/forecourt-restoration'
rois={'entrance-ground':(2768,706,2895,775),'tactile-strip':(2798,700,2853,813),'left-planter-pavement':(2528,756,2775,813),'right-planter-pavement':(2895,756,3135,813),'door-reference':(2750,570,2895,680),'curb-reference':(2538,812,3130,830)}
old=Image.open(R/'assets-src/gate25-station-planters/final-clean-ground.png').convert('RGBA');new=old.copy();new.paste(Image.open(S/'restored-ground.png'),(2500,690));original=Image.open(R/'assets-src/gate25-reconstruction/original-ground.png').convert('RGB')
baseline=json.loads((R/'public/assets/gate3/registration-refined/manifest.json').read_text());candidate=json.loads((R/'public/assets/gate3/registration-forecourt/manifest.json').read_text());assert baseline['objects']==candidate['objects'];assert baseline['logicalSolids']==candidate['logicalSolids']
for a,b in zip(baseline['chunks'],candidate['chunks']):
 assert a['mask']==b['mask'] and a['maskSha256']==b['maskSha256']
 assert hashlib.sha256((R/'public'/b['mask']).read_bytes()).hexdigest()==b['maskSha256']
 assert hashlib.sha256((R/'public'/b['image']).read_bytes()).hexdigest()==b['sha256']
protected=json.loads((R/'docs/gate3a/protected-assets.json').read_text())['sha256'];bad=[p for p,h in protected.items()if hashlib.sha256((R/p).read_bytes()).hexdigest()!=h];assert not bad,bad
# All existing approved source/runtime files plus renderer code must remain byte-identical to parent.
protected_paths=['assets-src/gate25-station-planters','assets-src/gate25-reconstruction','assets-src/gate25-refinement','public/assets/gate3/world','public/assets/gate3/registration','public/assets/gate3/registration-refined','public/assets/gate3/district','public/assets/juni','src/gate3/FoundationCamera.ts','src/gate3/PixelGrid.ts','src/gate3/NativeTexture.ts','src/gate3/WorldCache.ts','src/gate3/Registration.ts']
protected_paths += [str(p.relative_to(R))for p in (R/'src/gate3').rglob('*')if p.is_file()and p.name!='main.ts']
assert not subprocess.check_output(['git','diff','4370f43','--']+protected_paths,cwd=R).strip()
mask=np.array(Image.open(S/'repair-mask.png'))>0;patch=np.array(Image.open(S/'restored-ground.png').convert('RGB'));before=np.array(old.convert('RGB'))[690:900,2500:3184];assert not np.any(np.any(patch!=before,2)&~mask)
# Re-stitch literal candidate chunk pixels; alpha must remain opaque.
stitch=Image.new('RGBA',(684,210))
for c in candidate['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];ax,ay=max(2274,x),max(2603,y);bx,by=min(2958,x+w),min(2813,y+h)
 if bx>ax and by>ay:stitch.paste(Image.open(R/'public'/c['image']).convert('RGBA').crop((ax-x,ay-y,bx-x,by-y)),(ax-2274,ay-2603))
assert np.array_equal(np.array(stitch)[:,:,:3],patch);assert np.all(np.array(stitch)[:,:,3]==255)
rows=json.loads((D/'captures.json').read_text())['rows'];results=[]
for r in rows:
 if not r['name'].endswith('-native') or 'frontage' in r['name'] or 'entrance-juni' in r['name'] or 'moving' in r['name']:continue
 phase='after'if r['scene']=='registration-forecourt'else'before';expected=(new if phase=='after'else old).copy()
 for o in sorted(candidate['objects'],key=lambda x:x['sortY']):
  x,y=o['x']+226,o['y']-1913
  if x+o['width']<2500 or x>3184 or y+o['height']<540 or y>850:continue
  expected.alpha_composite(Image.open(R/'public'/o['image']).convert('RGBA'),(x,y))
 mat=r['audit']['camera']['matrix'];vx,vy=-mat[4],-mat[5];assert int(vx)==vx and int(vy)==vy
 shot=Image.open(D/(r['name']+'.png')).convert('RGB')
 for name,(x,y,x2,y2)in rois.items():
  actual=shot.crop((int(x-226-vx),int(y+1913-vy),int(x2-226-vx),int(y2+1913-vy)));want=expected.crop((x,y,x2,y2)).convert('RGB');diff=np.any(np.array(actual)!=np.array(want),2)
  results.append({'frame':r['name'],'roi':name,'pixels':int(diff.size),'differentPixels':int(diff.sum())});assert not diff.any(),results[-1]
  if r['renderer']=='auto':actual.save(D/f'{name}-{phase}-1x.png',optimize=True)
 assert r['audit']['camera']['zoom']==1
 for o in r['audit']['layers']:
  assert all(float(v).is_integer()for v in o['position']+o['screenOrigin']);assert o['scale']==[1,1]and o['scaleMode']==1
  if 'minFilter'in o:assert o['minFilter']==9728 and o['magFilter']==9728
 if r['renderer']=='auto':
  shot.crop((int(2500-226-vx),int(540+1913-vy),int(3184-226-vx),int(850+1913-vy))).save(D/f'station-frontage-{phase}-1x.png',optimize=True)
# Frontage with Juni is a genuine unscaled crop from the original Phaser frame.
front=next(r for r in rows if r['name']=='after-auto-frontage-juni-native');mat=front['audit']['camera']['matrix'];vx,vy=-mat[4],-mat[5]
Image.open(D/(front['name']+'.png')).crop((int(2500-226-vx),int(283+1913-vy),int(3184-226-vx),int(900+1913-vy))).save(D/'station-with-juni-1x.png',optimize=True)
for name,box in rois.items():original.crop(box).save(D/f'{name}-original-source-1x.png',optimize=True)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
sheet=Image.new('RGB',(1000,650),'#17242e');dr=ImageDraw.Draw(sheet)
for i,label in enumerate(['Earlier native SOURCE (retired props)','BEFORE / current Phaser','RESTORED / candidate Phaser']):dr.text((i*332+8,8),label,font=font,fill='white')
y=40
for name,box in list(rois.items())[:4]:
 dr.text((8,y),name+' / exact 1:1 pixel scale',font=font,fill='#ffdf9a');y+=22
 for col,im in enumerate([original.crop(box),Image.open(D/f'{name}-before-1x.png'),Image.open(D/f'{name}-after-1x.png')]):sheet.paste(im,(col*332+8,y))
 y+=box[3]-box[1]+22
sheet.save(D/'SOURCE_CURRENT_RESTORED_1X.png',optimize=True)
for n in ['entrance-ground','tactile-strip','left-planter-pavement','right-planter-pavement']:
 a=Image.open(D/f'{n}-before-1x.png');b=Image.open(D/f'{n}-after-1x.png');s=Image.new('RGB',(max(480,a.width*2+30),a.height+55),'#17242e');d=ImageDraw.Draw(s);d.text((8,8),'BEFORE / native 1:1',font=font,fill='white');d.text((s.width//2+8,8),'RESTORED / native 1:1',font=font,fill='white');s.paste(a,(8,35));s.paste(b,(s.width//2+8,35));s.save(D/f'{n}-comparison-1x.png',optimize=True)
# Exact protected perimeter/architecture comparisons, distinct from human art judgement.
for name in ['door-reference','curb-reference']:assert Image.open(D/f'{name}-before-1x.png').tobytes()==Image.open(D/f'{name}-after-1x.png').tobytes()
proof={'nativeReadback':results,'protectedAssetHashes':{'checked':len(protected),'different':bad},'existingSourceAndRuntimeDirectoriesUnchanged':protected_paths,'chunkCountChanged':2,'allCollisionReferencesAndHashesUnchanged':True,'logicalSolidsAndForegroundObjectsExact':True,'JuniNativeScale':1,'stationPivot':'unchanged explicit source pivot [0.5,0]; integer raster edges','repairOnlyInsideMask':True,'candidatePatchAlpha':[255],'rendererCoreChanged':False,'humanArtApproval':'PENDING; zero readback differences do not prove artistic success'}
(D/'technical-proof.json').write_text(json.dumps(proof,indent=2)+'\n');print('PASS',len(results),'native ROI readbacks;',len(protected),'protected hashes; candidate ground only')
