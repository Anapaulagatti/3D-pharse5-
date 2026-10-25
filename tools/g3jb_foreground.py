"""Native binary post mattes: source pixels only, no repaint or resampling."""
from pathlib import Path
from PIL import Image
from scipy.ndimage import label,binary_closing,binary_fill_holes
import numpy as np,json
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate3/jeju-bridges-v1';O=R/'public/assets/gate3/jeju-bridges-world';p=O/'manifest.json';m=json.loads(p.read_text());src=Image.open(S/'combined-native-authoring.png').convert('RGBA');scope=np.array(Image.open(S/'edit-scope-mask.png'))>0
boxes=[('a',3025,3465,40,90,3505),('a',3190,3500,45,115,3553),('a',3300,3530,50,120,3583),('a',3420,3570,50,110,3625),('a',3520,3620,45,65,3660),('b',3115,3955,36,110,3998),('b',3200,3980,40,125,4024),('b',3415,4000,40,125,4058),('b',3540,4040,36,90,4070)];objects=[]
for i,(bridge,x,y,w,h,depth)in enumerate(boxes):
 im=src.crop((x-2816,y-3200,x-2816+w,y-3200+h));a=np.array(im);r,g,b=[a[:,:,k].astype(float)for k in range(3)];mat=(abs(r-g)<22)&(abs(g-b)<24)&(r>30)&(r<218);mat=binary_closing(mat,iterations=1);labs,n=label(mat)
 if not n:continue
 k=max(range(1,n+1),key=lambda k:(labs==k).sum());mat=binary_fill_holes(labs==k)&scope[y:y+h,x:x+w]
 if mat.sum()<100:continue
 a[:,:,3]=mat*255;file=O/f'bridge-{bridge}-front-post-{i}.png';Image.fromarray(a).save(file);objects.append({'id':f'jeju-bridges/{bridge}-front-post-{i}','image':str(file.relative_to(R/'public')),'x':x,'y':y,'width':w,'height':h,'sortY':depth,'alphaSoftening':.6,'bytes':w*h*4})
m['objects']=[o for o in m['objects']if not o['id'].startswith('jeju-bridges/')]+objects;p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');(S/'foreground-ownership.json').write_text(json.dumps({'method':'Exact new source RGBA pixels, binary native gray stone post mattes. Foreground ownership allows Juni to pass behind raised rail shafts above the real deck, not through support feet. Vertical pier faces remain nonwalkable. No painting filters.','objects':objects},indent=2)+'\n');print('Native source foreground posts',len(objects))
