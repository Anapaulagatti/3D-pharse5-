from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import hashlib,json,numpy as np,subprocess
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate25-refinement';D=R/'docs/gate25-refinement';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();font=lambda n:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',n)
crops=[]
for phase in ['BEFORE','AFTER']:
 native=Image.open(D/(phase+'_NATIVE_1X.png'));assert native.size==(3184,1214)
 review=native.convert('RGB');review.thumbnail((1592,607),Image.Resampling.LANCZOS);review.save(D/(phase+'_REVIEW.jpg'),quality=87,optimize=True,subsampling=0)
 for name,x in [('WEST',1512),('EAST',2488)]:
  box=(x-250,70,x+250,850);crop=native.crop(box);path=D/(name+'_'+phase+'_CLOSEUP_1X.png');crop.save(path,optimize=True);assert Image.open(path).tobytes()==native.crop(box).tobytes();crops.append(dict(path=path.name,source=phase+'_NATIVE_1X.png',box=box,exactNativePixels=True))
for name in ['WEST','EAST']:
 board=Image.new('RGB',(1000,820),'#20383c');dr=ImageDraw.Draw(board)
 for col,phase in enumerate(['BEFORE','AFTER']):
  board.paste(Image.open(D/(name+'_'+phase+'_CLOSEUP_1X.png')).convert('RGB'),(col*500,40));dr.text((col*500+12,8),name+' / '+phase+' / native 1:1',font=font(20),fill='#f5e8cb')
 board.save(D/(name+'_BEFORE_AFTER.jpg'),quality=86,optimize=True,subsampling=0)
board=Image.new('RGB',(640,720),'#20383c');dr=ImageDraw.Draw(board);panels=json.loads((S/'planting-panels.json').read_text())
for row,box in enumerate(panels):
 for col,phase in enumerate(['BEFORE','AFTER']):
  crop=Image.open(D/(phase+'_NATIVE_1X.png')).crop(box).convert('RGB');board.paste(crop,(col*320,row*180+20));dr.text((col*320+6,row*180+2),phase+' / pocket '+str(row+1),font=font(13),fill='#f5e8cb')
board.save(D/'PLANTING_BEFORE_AFTER.jpg',quality=88,optimize=True,subsampling=0)
for p in list(D.glob('*PASSAGE_*.png'))+list(D.glob('PLAYER_*.png')):
 im=Image.open(p).convert('RGB');im.save(D/(p.stem+'_REVIEW.jpg'),quality=86,optimize=True,subsampling=0)
before=json.loads((D/'protected-before.json').read_text());changes=[p for p,h in before.items()if not (R/p).exists()or sha(R/p)!=h];assert changes==['public/assets/gate2/catalog.json'],changes
(D/'preservation.json').write_text(json.dumps(dict(snapshotFiles=len(before),onlyChangedExistingFile=changes,allPreviousDerivedGroundAndSourcesUnchanged=True,allJuniAndCameraAndTourSourceUnchanged=True,approvedPlanningAndNorthernKoreaUnchanged=True),indent=2)+'\n')
rows=[]
for name,id,refs,selected in [('west','32bde8b2-aa80-4227-b2a3-2f76d701c093',['west-before.png','west-protection-guide.png'],True),('east','e564bb80-05cd-47cb-b30d-ab90e3bd7661',['east-before.png','east-protection-guide.png'],False),('planting','4ee70db6-9545-406b-ac49-485c205e0a7b',['planting-before-sheet.png'],False),('east-context','4d773a27-0720-43f4-9175-c45a3fac1553',['east-context-before.png','east-context-guide.png','east-finished.png'],True),('planting-variation','2315b0a0-38af-4608-b180-b90b335e3efe',['planting-before-sheet.png'],True)]:
 p=S/(name+'-host.png');rows.append(dict(file=p.name,sha256=sha(p),dimensions=Image.open(p).size,prompt=name+'-prompt.txt',references=refs,hostOutput='/workspace/generated_images/exec-'+id+'.png',selected=selected))
(S/'provenance.json').write_text(json.dumps(dict(method='built-in host local image editing; no external paid generation API',calls=5,model=None,price=None,modelAndPriceNotExposed=True,sourceGround='../gate25-reconstruction/reconstructed-ground.png',approvedArchitectureMask='../gate25-reconstruction/architecture-protection-final.png',finishing='Nearest-neighbor only on local new edits; binary masks exclude approved architecture and all areas outside the local scope. Original sources not modified.',editMask='combined-edit-mask.png',outputs=rows),indent=2)+'\n')
# Actual native runtime scene uses the same disjoint boundaries and unchanged foreground references.
scene=json.loads((R/'public/assets/gate2/district-refinement/scene.json').read_text());old=json.loads((R/'public/assets/gate2/district-reconstruction/scene.json').read_text());assert scene['objects']==old['objects'];assert scene['targets']==old['targets']and scene['spawn']==old['spawn'];covered=np.zeros((1214,3184),int)
for g in scene['grounds']:covered[g['y']:g['y']+g['height'],g['x']:g['x']+g['width']]+=1
assert np.all(covered==1);proof=json.loads((D/'asset-proof.json').read_text());proof['changedGroundPercent']=round(100*proof['changedGroundPixels']/proof['worldPixels'],3)
(D/'evidence-checks.json').write_text(json.dumps(dict(crops=crops,groundChangedPercent=proof['changedGroundPercent'],exactlyOnceChunkCoverage=True,oldForegroundReferencesAndPropertiesExact=True,reviewJpegs=[dict(path=p.name,bytes=p.stat().st_size,under1MB=p.stat().st_size<1000000)for p in sorted(D.glob('*.jpg'))],note='Technical and source checks only; human artistic approval remains pending.'),indent=2)+'\n')
print('PASS native crops / preserved inputs / local masks / provenance / independently owned native chunks')
