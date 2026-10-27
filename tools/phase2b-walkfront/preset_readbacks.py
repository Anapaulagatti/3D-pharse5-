from pathlib import Path
from PIL import Image,ImageDraw
import json,math
import numpy as np
D=Path('docs/phase2b-motion/walk-front');q=json.loads((D/'preset-gameplay.json').read_text());rows=[]
for pre in sorted({r['preset']for r in q}):
 board=Image.new('RGB',(768,132),(28,30,38));dr=ImageDraw.Draw(board)
 for r in [r for r in q if r['preset']==pre]:
  a=r['audit'];s=a['state'];sx,sy=a['camera']['scroll'];x=math.floor(s['x']+.5)-48-sx;y=math.floor(s['y']+.5)-100-sy;actual=Image.open(r['sourcePath']).convert('RGB').crop((x,y,x+96,y+112));src=np.array(Image.open(D/f'{pre}-expected-walk-front-{r["index"]}.png'));diff=int(((src[:,:,3]==255)&np.any(src[:,:,:3]!=np.array(actual),2)).sum());assert diff==0,(pre,r['index'],diff);board.paste(actual,(96*r['index'],20));dr.text((96*r['index']+3,2),str(r['index']),fill='white');rows.append({'preset':pre,'index':r['index'],'diffPixels':diff,'nearest':s['samplingMode']==1,'native1to1':a['camera']['zoom']==1})
 board.save(D/f'{pre}-actual-native.png')
assert len(rows)==32;(D/'preset-readbacks.json').write_text(json.dumps({'rows':rows,'diffPixels':0,'scope':'32actualPhaser samples of unchanged cosmetic patches over updated default base; pixel alignment proof, not approval of wardrobe motion. Existing outfit pose pixels remain preserved.'},indent=2)+'\n');print('32 preset native readbacks,0mismatch')
