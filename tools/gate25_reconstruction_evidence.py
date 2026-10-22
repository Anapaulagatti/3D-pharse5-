from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,numpy as np,subprocess
R=Path(__file__).resolve().parents[1];D=R/'docs/gate25-reconstruction';S=R/'assets-src/gate25-reconstruction';O=R/'public/assets/gate2/district-reconstruction';font=lambda n:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',n)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
crops=[]
for label,x in [('WEST',1512),('EAST',2488)]:
 for band,y0,y1 in [('FULL_HEIGHT',0,1214),('UPPER',0,400),('MIDDLE',400,850),('LOWER',850,1214)]:
  width=640;box=(x-width//2,y0,x+width//2,y1);board=Image.new('RGB',(width*2,y1-y0+40),'#20383c');dr=ImageDraw.Draw(board)
  for col,phase in enumerate(['BEFORE','AFTER']):
   src=D/(phase+'_NATIVE_1X.png');im=Image.open(src);crop=im.crop(box);name=f'{label}_{band}_{phase}_1X.png';crop.save(D/name,optimize=True);assert Image.open(D/name).tobytes()==im.crop(box).tobytes();board.paste(crop.convert('RGB'),(col*width,40));dr.text((col*width+12,8),f'{label} / {band} / {phase} / native 1:1',font=font(17),fill='#f3e9d0');crops.append(dict(path=name,source=src.name,box=box,nativePixelsExact=True))
  board.save(D/f'{label}_{band}_BEFORE_AFTER.jpg',quality=85,optimize=True,subsampling=0)
for name in ['BEFORE_NATIVE_1X','AFTER_NATIVE_1X']:
 im=Image.open(D/(name+'.png')).convert('RGB');im.thumbnail((1592,607),Image.Resampling.LANCZOS);im.save(D/(name+'_REVIEW.jpg'),quality=86,optimize=True,subsampling=0)
for p in list(D.glob('TOUR_*.png'))+list(D.glob('PLAYER_*.png'))+list(D.glob('PAN_*.png'))+list(D.glob('FOREGROUND_*.png')):
 im=Image.open(p).convert('RGB');im.thumbnail((1280,900),Image.Resampling.LANCZOS);im.save(D/(p.stem+'_REVIEW.jpg'),quality=85,optimize=True,subsampling=0)
# Verify immutable inputs against the snapshot taken BEFORE any reconstruction.
before=json.loads((D/'protected-before.json').read_text());changed=[p for p,h in before.items()if not (R/p).exists()or sha(R/p)!=h];assert changed==['public/assets/gate2/catalog.json'],changed
remote=subprocess.check_output(['git','ls-remote','origin','refs/heads/main','refs/heads/art-gate/final-gate1-world','refs/tags/checkpoint/gate1-approved-planning-20261022^{}'],cwd=R,text=True)
refs={line.split()[1]:line.split()[0]for line in remote.splitlines()};assert refs['refs/heads/main']=='33360ed1989e4db9fc3fc4e3686ca385e0b00908';assert refs['refs/heads/art-gate/final-gate1-world']==refs['refs/tags/checkpoint/gate1-approved-planning-20261022^{}']=='e0a5c0aeff1a2980042983e6091abff11b987fad'
old='4eef7a7';source_diff=subprocess.check_output(['git','diff',old,'--','src','public/assets/juni','assets-src/gate1','assets-src/gate2','assets-src/world-gate1'],cwd=R,text=True);assert not source_diff
(D/'preservation.json').write_text(json.dumps(dict(snapshotFiles=len(before),changedExistingFiles=changed,approvedSourcesAndHistoricalDerivedAssetsUnmodified=True,JuniAndTourAndMobileSourceUnmodified=True,protectedRefs=refs),indent=2)+'\n')
# Native immutable facade comparison and disjoint runtime windows; aesthetic quality is not inferred.
mask=np.array(Image.open(S/'architecture-protection-final.png'))>0;source=np.array(Image.open(S/'original-ground.png').convert('RGB'));ground=np.array(Image.open(S/'reconstructed-ground.png').convert('RGB'));assert np.array_equal(source[mask],ground[mask]);scene=json.loads((O/'scene.json').read_text());assembled=Image.new('RGB',(3184,1214));cover=np.zeros((1214,3184),int)
for ch in scene['grounds']:
 p=R/'public/assets/gate2'/ch['image'];im=Image.open(p);assert im.size==(ch['width'],ch['height']);assembled.paste(im,(ch['x'],ch['y']));cover[ch['y']:ch['y']+ch['height'],ch['x']:ch['x']+ch['width']]+=1
assert np.all(cover==1);assert assembled.tobytes()==Image.open(S/'reconstructed-ground.png').convert('RGB').tobytes();assert len({o['id']for o in scene['objects']})==len(scene['objects'])
rows=[]
for name,host,prompt,refs_ in [('ground-host.png','/workspace/generated_images/exec-cdde0739-861e-4e65-9575-58f90a0b658f.png','ground-authoring-prompt.txt',['original-ground.png','environment-authoring-guide-v1.png']),('ground-revised-host.png','/workspace/generated_images/exec-c968c92f-7ce7-46af-9ac8-5ef968634993.png','ground-revision-prompt.txt',['ground-host.png'])]:
 rows.append(dict(file=name,sha256=sha(S/name),dimensions=Image.open(S/name).size,hostOutput=host,prompt=prompt,referenceFiles=refs_))
(S/'provenance.json').write_text(json.dumps(dict(method='built-in host image editing / two clean-environment authoring calls / NO external paid provider API',model=None,price=None,hostModelAndPriceUnavailable=True,inputs=rows,finish='nearest-neighbor to3184x1214 ONLY for newly authored environment; protected original architecture pasted at original pixels; source images unmodified',protectedArchitectureMask='architecture-protection-final.png',foreground='foreground-ownership.json',allOriginalArtRetained=True,originalDistrictSource='assets-src/gate25-polish/finished-background.png',noBuildingsGenerated=True),indent=2)+'\n')
(D/'evidence-checks.json').write_text(json.dumps(dict(crops=crops,facadePixelEquality=True,protectedPixels=int(mask.sum()),chunkOwnershipExactlyOnce=True,chunkEdges=[1512,2488],runtimeGrounds=3,foregroundObjects=len(scene['objects']),runtimeWorldSize=[3184,1214],reviewJpegs=[dict(path=p.name,bytes=p.stat().st_size,under1MB=p.stat().st_size<1000000)for p in D.glob('*.jpg')],note='These are source/geometry checks, NOT artistic approval.'),indent=2)+'\n')
print('PASS native crop equality / architecture RGB / source preservation / exactly-once chunks / provenance')
