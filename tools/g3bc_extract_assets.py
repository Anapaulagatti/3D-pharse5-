"""Technical native atlas extraction. RGB pixels never filtered, scaled or recolored.
Explicit chroma-owner alpha mask; source host outputs are immutable.
"""
from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
from scipy.ndimage import label,find_objects
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate3/full-world';O=R/'public/assets/gate3/production-assets';O.mkdir(exist_ok=True);records={'buildings':{},'trees':[]};masks=S/'alpha-masks';masks.mkdir(exist_ok=True)
def extract(source,name,box):
 src=Image.open(S/source).convert('RGBA');crop=src.crop(box);a=np.array(crop);rgb=a[:,:,:3].astype(float);r,g,b=[rgb[:,:,i]for i in range(3)];chroma=(r>110)&(b>90)&(g<np.minimum(r,b)*.75)&(r>b*.7)&(b>r*.5);alpha=(~chroma).astype('uint8')*255;a[:,:,3]=alpha;a[chroma,:3]=0;# Remove detached neighboring-wheel fragments in the tower cell, not tower RGB.
 if name=='tower':
  labs,n=label(a[:,:,3]>0);boxes=find_objects(labs)
  for i,bb in enumerate(boxes,1):
   if bb is not None and bb[1].start>=330 and bb[0].stop<550:a[labs==i]=0
  alpha=a[:,:,3].copy()
 im=Image.fromarray(a);bounds=im.getbbox();assert bounds;im=im.crop(bounds);path=O/(name+'.png');im.save(path,optimize=True);Image.fromarray(alpha).save(masks/(name+'.png'),optimize=True)
 result={'id':name,'image':str(path.relative_to(R/'public')),'source':source,'sourceSha256':hashlib.sha256((S/source).read_bytes()).hexdigest(),'sourceCell':list(box),'nativeCrop':[box[0]+bounds[0],box[1]+bounds[1],box[0]+bounds[2],box[1]+bounds[3]],'size':list(im.size),'alphaMask':'alpha-masks/'+name+'.png','resampling':'NONE','visibleRGBPreserved':True,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()};valid=np.array(im)[:,:,3]>0;original=np.array(src.crop(result['nativeCrop']));assert np.array_equal(np.array(im)[:,:,:3][valid],original[:,:,:3][valid]);return result
for name,box in {'tower':(0,0,355,770),'wheel':(355,0,800,770),'carousel':(800,0,1254,770),'market':(0,780,715,1254),'ferry':(715,780,1254,1254)}.items():records['buildings'][name]=extract('landmarks-finished.png',name,box)
for name,box in {'palace':(0,0,1254,770),'archive':(0,780,625,1254),'culture':(625,780,1254,1254)}.items():records['buildings'][name]=extract('historical-finished.png',name,box)
for i in range(12):
 x0=round((i%4)*1254/4);x1=round((i%4+1)*1254/4);y0=(i//4)*418;y1=y0+418;records['trees'].append(extract('trees-native.png',f'tree-native-{i}',(x0,y0,x1,y1)))
(S/'extracted-assets.json').write_text(json.dumps(records,indent=2)+'\n');print({k:v['size']for k,v in records['buildings'].items()})
