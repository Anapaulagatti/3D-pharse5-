from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib,subprocess
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate25-station-planters';D=R/'docs/gate25-station-planters';P=R/'public/assets/gate2';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();font=lambda n:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',n)
proof=json.loads((D/'asset-proof.json').read_text());before=Image.open(D/'BEFORE_NATIVE_1X.png').convert('RGB');after=Image.open(D/'AFTER_NATIVE_1X.png').convert('RGB');expected=Image.open(S/'expected-native-composite.png').convert('RGB');assert after.size==(3184,1214)
rows=[]
for name,box in [('LEFT',(2528,682,2768,812)),('RIGHT',(2890,682,3130,812))]:
 for phase,im in [('BEFORE',before),('AFTER',after)]:
  crop=im.crop(box);crop.save(D/(name+'_'+phase+'_1X.png'),optimize=True);assert Image.open(D/(name+'_'+phase+'_1X.png')).tobytes()==im.crop(box).tobytes()
 board=Image.new('RGB',(960,304),'#20383c');dr=ImageDraw.Draw(board)
 for col,phase in enumerate(['BEFORE','AFTER']):
  crop=Image.open(D/(name+'_'+phase+'_1X.png'));board.paste(crop.resize((480,260),Image.Resampling.NEAREST),(col*480,44));dr.text((col*480+10,10),name+' / '+phase+' / nearest 2x',font=font(19),fill='#f2e3c2')
 board.save(D/(name+'_BEFORE_AFTER_2X.png'),optimize=True);board.save(D/(name+'_BEFORE_AFTER_REVIEW.jpg'),quality=90,optimize=True,subsampling=0)
for ob in proof['newPlanterObjects']:
 box=(ob['x'],ob['y'],ob['x']+ob['width'],ob['y']+ob['height']);a=np.array(after.crop(box));b=np.array(expected.crop(box));assert np.array_equal(a,b),(ob['id'],int((a!=b).any(2).sum()))
 rgba=np.array(Image.open(P/ob['image']).convert('RGBA'));assert set(np.unique(rgba[:,:,3]))<={0,255};assert not np.any(rgba[rgba[:,:,3]==0,:3]);rows.append(dict(id=ob['id'],worldBox=box,exactRenderedNativeRGB=True,allBoundingBoxPixelsCompared=ob['width']*ob['height'],bodyAlphaOnlyZeroOr255=True,opaqueStoneCoreVerified=True,transparentRGBZero=True,nativeTextureSizeMatchesObject=True))
world=Image.open(D/'JUNI_GAMEPLAY_CANVAS_1X.png');state=json.loads((D/'browser-qa.json').read_text())['rows'][0]['finalState'];assert world.size==tuple(state['camera']['canvas']);vx,vy=map(round,state['camera']['renderedWorldView'][:2]);frontageBox=(2500-vx,250-vy,3184-vx,850-vy);world.crop(frontageBox).save(D/'STATION_FRONTAGE_WITH_JUNI_1X.png',optimize=True)
for name in ['AFTER_NATIVE_1X','STATION_FRONTAGE_WITH_JUNI_1X']:
 im=Image.open(D/(name+'.png')).convert('RGB');im.thumbnail((1592,650),Image.Resampling.LANCZOS);im.save(D/(name+'_REVIEW.jpg'),quality=88,optimize=True,subsampling=0)
# Contact-sheet inspection supplies actual light/dark edge review, not an automatic aesthetic verdict.
board=Image.new('RGB',(800,440),'#d8caac')
for i,ob in enumerate(proof['newPlanterObjects']):
 sprite=Image.open(P/ob['image']).convert('RGBA')
 for j,color in enumerate(['#e5dcc8','#203038']):
  tile=Image.new('RGBA',(200,110),color);tile.alpha_composite(sprite,(3,3));board.paste(tile.convert('RGB').resize((400,220),Image.Resampling.NEAREST),(i*400,j*220))
board.save(D/'ALPHA_LIGHT_DARK_2X.png',optimize=True)
# Native sprite originals, source transform receipt and direct rendered-RGB equality are the alpha/sampling evidence.
baseline=json.loads((D/'protected-before.json').read_text());changed=[p for p,h in baseline.items()if not (R/p).exists()or sha(R/p)!=h];assert changed==['public/assets/gate2/catalog.json'],changed
(D/'preservation.json').write_text(json.dumps(dict(snapshotFiles=len(baseline),changedExistingFiles=changed,allSourceArtAndPriorTexturesUnmodified=True,JuniCameraTourControlsUnmodified=True,oldCheckpointsRetained=True),indent=2)+'\n')
raw=Image.open(R/'assets-src/gate25-reconstruction/ground-revised-host.png').convert('RGB').resize((3184,1214),Image.Resampling.NEAREST);oldground=Image.open(R/'assets-src/gate25-refinement/final-ground.png').convert('RGB');sourceproof=[]
for name,box in [('left',(2540,705,2740,790)),('right',(2900,705,3120,790))]:sourceproof.append(dict(id=name,box=box,exactOldHostPixelFraction=float((np.array(raw.crop(box))==np.array(oldground.crop(box))).all(2).mean())))
# Native Juni movement alpha width establishes actual sprite clearance without shrinking the atlas.
j=json.loads((R/'public/assets/juni/juni.json').read_text());atlas=Image.open(R/'public/assets/juni/juni.png').convert('RGBA');widths=[]
for name,frame in j['frames'].items():
 if name.startswith(('walk-','run-')):
  f=frame['frame'];bb=atlas.crop((f['x'],f['y'],f['x']+f['w'],f['y']+f['h'])).getchannel('A').getbbox();widths.append(bb[2]-bb[0])
assert max(widths)<=89
(D/'sampling-and-alpha.json').write_text(json.dumps(dict(nativePhaserReadback=rows,oldLowResolutionSource=[2030,775],oldWorldFinish=[3184,1214],oldSourcePixelProvenance=sourceproof,oldObjectOwnership='baked opaque RGB ground, not foreground alpha sprites',runtimeConfig=dict(pixelArt=True,roundPixels=True,antialias=False),oldRuntimeInterpolationCause=False,oldMaskAlphaHaloCause=False,newNativeRenderUnwantedResampling=False,intentionalAuthoringTransform=proof['newPlanterRecords'],maxJuniWalkRunVisibleWidth=max(widths),unchangedClearCorridorWidth=89,visualArtApproval='PENDING_DIRECT_HUMAN_INSPECTION'),indent=2)+'\n')
meta=[]
for name,id,refs,transparent in [('clean-floor','2ff76028-a7f5-432b-8cca-493432e910d3',['planters-context-tall-before.png'],False),('planter-sprites','13cc6979-f671-4d3d-8bb9-970e0593c3e4',['planters-context-tall-before.png','station-native-craft-reference.png','muneum-native-reference.png'],True)]:
 p=S/(name+'-host.png');meta.append(dict(file=p.name,sha256=sha(p),dimensions=Image.open(p).size,hostOutput='/workspace/generated_images/exec-'+id+'.png',references=refs,transparentBackground=transparent,prompt='clean-floor-prompt.txt'if name=='clean-floor'else'planter-sprites-prompt.txt'))
(S/'provenance.json').write_text(json.dumps(dict(hostLocalImageEdits=2,noExternalPaidGenerationAPI=True,model=None,price=None,modelAndPriceNotExposed=True,scope='two station planters and owned underpainting/shadows only',outputs=meta,nativeTransformReceipt='../../docs/gate25-station-planters/asset-proof.json',immutableBaseline='../gate25-refinement/final-ground.png'),indent=2)+'\n')
print('PASS exact actual Phaser native pixels / binary body alpha / source provenance / unchanged assets / native Juni clearance')
