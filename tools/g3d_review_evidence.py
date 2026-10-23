from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-recovery';sources=[]
refs={'north':('docs/gate2/A_NATIVE_1X.png',(520,360,1160,860)),'south':('docs/gate2/B_NATIVE_1X.png',(0,240,640,740)),'namsan':('docs/gate2/A_NATIVE_1X.png',(0,80,640,580))}
boxes={'north':(500,300,1140,800),'south':(280,340,920,840),'namsan':(350,320,990,820)}
for name,(path,box)in refs.items():
 ref=Image.open(R/path).convert('RGB').crop(box);out=Image.new('RGB',(1944,550),'#203735');draw=ImageDraw.Draw(out)
 labels=['APPROVED NATIVE REFERENCE','CURRENT / ART REJECTED','CORRECTED PILOT / HUMAN REVIEW PENDING']
 images=[ref]+[Image.open(D/f'{name}-{state}-native.png').convert('RGB').crop(boxes[name])for state in ['before','candidate']]
 for i,im in enumerate(images):
  out.paste(im,(8+i*648,42));draw.text((8+i*648,14),labels[i],fill='white');im.save(D/f'{name}-comparison-{i}-1x.png',optimize=True)
 out.save(D/f'{name}-comparison-native.png',optimize=True);out.save(D/f'{name}-comparison-review.jpg',quality=86,subsampling=0,optimize=True)
 sources.append({'pilot':name,'approvedReference':path,'approvedCrop':list(box),'referenceMeaning':'Approved Korean historical garden detail, not a previously approved Namsan design'if name=='namsan'else'Approved actual Phaser native frame','currentCandidateCrop':list(boxes[name]),'nativeComparisonScale':1})
 for state in ['before','candidate']:
  im=Image.open(D/f'{name}-{state}-native.png').convert('RGB');im.resize((960,675),Image.Resampling.NEAREST).save(D/f'{name}-{state}-review.jpg',quality=85,subsampling=0,optimize=True)
# Fine seams/contact checks use1x native crops; no resampling.
crops={'north-approved-boundary':('north',(400,180,720,700)),'north-archive-contact':('north',(610,190,1200,460)),'south-curb-contact':('south',(300,570,980,820)),'south-namsan-join':('namsan',(250,175,1050,380)),'namsan-entry-contact':('namsan',(450,465,850,820))}
for key,(name,box)in crops.items():
 out=Image.new('RGB',((box[2]-box[0])*2+24,box[3]-box[1]+45),'#203735');d=ImageDraw.Draw(out)
 for i,state in enumerate(['before','candidate']):
  crop=Image.open(D/f'{name}-{state}-native.png').convert('RGB').crop(box);crop.save(D/f'{key}-{state}-1x.png',optimize=True);x=8+i*(crop.width+8);out.paste(crop,(x,35));d.text((x,10),state.upper()+' / actual Phaser native1x',fill='white')
 out.save(D/f'{key}-comparison-1x.png',optimize=True);out.save(D/f'{key}-review.jpg',quality=86,subsampling=0,optimize=True)
(D/'comparison-provenance.json').write_text(json.dumps({'comparisons':sources,'seamCrops':crops,'nativePNGOriginalsUnmodified':True,'jpegPreviews':'Convenience copies only; not pixel-quality evidence','previewSizes':{p.name:p.stat().st_size for p in D.glob('*review.jpg')}},indent=2)+'\n')
