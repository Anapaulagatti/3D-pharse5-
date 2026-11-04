"""Original host-image props -> explicit ownership + shared native registration.
No approved map/source pixels sampled; no background plate emitted.
"""
from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
R=Path.cwd();S=R/'assets-src/farming/phase3bd-final-quality';O=R/'public/assets/farming/phase3bd-final-quality';F=S/'native-frames';F.mkdir(exist_ok=True)
a=np.array(Image.open(S/'master-clean.png').convert('RGBA'));rgb=a[:,:,:3].astype(float);bad=((rgb.max(2)-rgb.min(2))>150)&(rgb.max(2)>210)&(rgb.min(2)<25);a[bad,3]=0;clean=Image.fromarray(a);clean.save(S/'despilled-master.png')
# Explicit authored source ownership: generated props were not exactly regular columns.
bounds=[(40,225,245,310),(315,180,515,310),(575,130,785,310),(810,70,1110,310),(1110,10,1440,310),(1440,15,1760,310)];roots=[(145,288),(420,288),(678,288),(958,288),(1275,288),(1600,288)];names=['sown','sprout','young','growing','ready','ready-alt'];records=[]
for row,crop in enumerate(['radish','scallion']):
 for i,(x0,y0,x1,y1)in enumerate(bounds):
  if row:y0=315;y1=620
  root=roots[i];root=(root[0],root[1]+300*row)
  # Fixed inverse affine; same .115 source->native scale and (20,40) root for all stages.
  inv=1/.115
  im=clean.transform((40,44),Image.Transform.AFFINE,(inv,0,root[0]-20*inv,0,inv,root[1]-40*inv),resample=Image.Resampling.BICUBIC)
  # Source ownership masks remove adjacent props, never select a largest component.
  arr=np.array(im);yy,xx=np.indices((44,40));sx=root[0]+(xx-20)*inv;sy=root[1]+(yy-40)*inv;arr[(sx<x0)|(sx>=x1)|(sy<y0)|(sy>=y1),3]=0
  arr[:,:,3]=np.where(arr[:,:,3]>=150,255,0);arr[arr[:,:,3]==0,:3]=0
  name=f'{crop}-{names[i]}';Image.fromarray(arr).save(F/(name+'.png'));records.append({'name':name,'sourceRect':[x0,y0,x1-x0,y1-y0],'sourceRoot':root,'scale':.115,'native':[40,44],'root':[20,40]})
# Every material is a tiny native tile sampled ONLY from newly generated soil props.
for kind,cx in [('loam',150),('tilled',425),('wet',715)]:
 for i in range(12):
  x=cx-50+(i%4-1)*8;y=712+(i//4)*7
  tile=clean.crop((x,y,x+100,y+100)).resize((16,16),Image.Resampling.BOX).convert('RGBA');arr=np.array(tile)
  assert (arr[:,:,3]>180).all(),(kind,i,'Source sample not solid material')
  arr[:,:,3]=255;Image.fromarray(arr).save(F/(kind+f'-{i}.png'))
(S/'REGISTRATION.json').write_text(json.dumps({'artSource':'host_image','routeActuallyUsed':'image_gen.imagegen (builtin;2calls: original + sheet cleanup)','rawMaster':'master.png','cleanMaster':'master-clean.png','despill':'Remove only saturated RGB matte fringe; alpha threshold150. No source-world/art filters. Native crop fixed-scale .115, no per-stage bbox fitting.','despilledSourcePixels':int(bad.sum()),'nativeFinish':'Fixed authored ownership/root; bicubic source-to-native finish followed by shared Forge palette, binary alpha. Runtime uses exact1:1nearest; approved assets unchanged.','cropFrames':records,'soilFrames':'36original16x16native material components; no140x88/full-bed image'},indent=2)+'\n')
print('12original registered40x44crop props +36native16x16material components')

for name,box in [('debris-stone',(874,680,1128,845)),('debris-straw',(1166,680,1441,846)),('debris-rim',(1481,651,1733,848))]:
 part=clean.crop(box);part.thumbnail((14,12),Image.Resampling.BOX);canvas=Image.new('RGBA',(16,16));canvas.alpha_composite(part,((16-part.width)//2,15-part.height));a=np.array(canvas);a[:,:,3]=np.where(a[:,:,3]>=150,255,0);a[a[:,:,3]==0,:3]=0;Image.fromarray(a).save(F/(name+'.png'))
