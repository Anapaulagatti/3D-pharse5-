"""Source-owned native finish; no primary anatomy painting. 80px shared rest scale."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,sys
import numpy as np
R=Path(__file__).resolve().parents[2];S=R/'assets-src/npcs/phase3a-npc-expansion';D=R/'docs/phase3a-npc-expansion';DIRS=['front','back','left','right'];SPLIT={'daehyun':627,'jiho':627,'eunji':600,'seojun':627,'nayeon':625,'cheolsu':610,'yejin':614,'sungmin':627}
def finish(id):
 p=S/id;raw=Image.open(p/'turnaround-source.png').convert('RGBA');a=np.array(raw);c=a[:,:,:3].astype(int);a[(c[:,:,0]>145)&(c[:,:,2]>145)&(c[:,:,0]-c[:,:,1]>100)&(c[:,:,2]-c[:,:,1]>100)]=0;im=Image.fromarray(a);im.save(p/'turnaround-keyed.png');w,h=im.size;split=SPLIT[id];rows=[];views=[]
 for i,d in enumerate(DIRS):
  box=[i%2*w//2,0 if i<2 else split,(i%2+1)*w//2,split if i<2 else h];q=im.crop(box);b=q.getbbox();assert b;views.append(q.crop(b));rows.append({'direction':d,'sourceQuadrant':box,'sourceBounds':b})
 scale=80/max(q.height for q in views);board=Image.new('RGBA',(384,112));(p/'native').mkdir(exist_ok=True)
 for i,(q,row)in enumerate(zip(views,rows)):
  size=[round(q.width*scale),round(q.height*scale)];q=q.resize(size,Image.Resampling.BOX);a=np.array(q);a[a[:,:,3]<128]=0;a[a[:,:,3]>=128,3]=255;q=Image.fromarray(a);xy=[48-size[0]//2,100-size[1]];board.alpha_composite(q,(i*96+xy[0],xy[1]));row.update(size=size,placement=xy)
 alpha=board.getchannel('A');bg=Image.new('RGB',board.size,(29,27,36));bg.paste(board,mask=alpha);board=bg.quantize(colors=96,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGBA');board.putalpha(alpha)
 for i,d in enumerate(DIRS):board.crop((i*96,0,(i+1)*96,112)).save(p/'native'/f'{d}.png')
 board.save(p/'native-turnaround.png');bg=Image.new('RGBA',board.size,(29,27,36,255));bg.alpha_composite(board);bg.convert('RGB').save(D/f'{id}-turnaround-native.png');bg.resize((1536,448),Image.Resampling.NEAREST).convert('RGB').save(D/f'{id}-turnaround-4x.png')
 (p/'native-finish.json').write_text(json.dumps({'sourceSHA256':hashlib.sha256((p/'turnaround-source.png').read_bytes()).hexdigest(),'sourceSize':raw.size,'sharedSourceToNativeScale':scale,'nativeCell':[96,112],'footAnchor':[48,100],'finish':'Premultiplied BOX source-to-native, binary alpha, shared96colour palette,no dither; not runtime resampling','views':rows},indent=2)+'\n');print(id,[v['size']for v in rows])
if __name__=='__main__':
 for id in sys.argv[1:]:finish(id)
