"""Controlled single-scale native finish of authored directional sources.
No per-animation-frame normalization. Source pixels and transformation records retained.
"""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[2]
S=R/'assets-src/characters/phase1b'
def prepare(id):
 p=S/id;im=Image.open(p/'turnaround-source.png').convert('RGBA');a=np.array(im)
 key=(a[:,:,0]>170)&(a[:,:,2]>140)&(a[:,:,1]<100)&(a[:,:,0]>a[:,:,1]*1.6)&(a[:,:,2]>a[:,:,1]*1.5)
 a[key]=0;clean=Image.fromarray(a);clean.save(p/'turnaround-keyed.png')
 w,h=im.size;directions=['front','back','left','right'];crops=[];records=[]
 for i,d in enumerate(directions):
  q=clean.crop((i%2*w//2,i//2*h//2,(i%2+1)*w//2,(i//2+1)*h//2));bb=q.getbbox();crops.append(q.crop(bb));records.append({'direction':d,'sourceQuadrant':[i%2*w//2,i//2*h//2,w//2,h//2],'bbox':bb})
 # Rest silhouettes share one source-to-native scale, not independently stretched.
 scale=80/crops[0].height
 natives=[]
 for q,row in zip(crops,records):
  size=(round(q.width*scale),round(q.height*scale));q=q.resize(size,Image.Resampling.BOX);aa=np.array(q);aa[aa[:,:,3]<128]=0;aa[aa[:,:,3]>=128,3]=255
  q=Image.fromarray(aa);out=Image.new('RGBA',(96,112));pos=(48-size[0]//2,100-size[1]);out.alpha_composite(q,pos);natives.append(out);row.update({'nativeSize':size,'placement':pos,'scale':scale})
 # One shared native palette across all directions, no dither.
 board=Image.new('RGBA',(384,112))
 for i,q in enumerate(natives):board.alpha_composite(q,(i*96,0))
 rgb=Image.new('RGB',board.size,(30,25,35));rgb.paste(board,mask=board.getchannel('A'));pal=rgb.quantize(colors=96,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
 rgba=pal.convert('RGBA');rgba.putalpha(board.getchannel('A'));(p/'native').mkdir(exist_ok=True)
 for i,d in enumerate(directions):rgba.crop((i*96,0,(i+1)*96,112)).save(p/'native'/f'{d}.png')
 rgba.save(p/'native-turnaround.png');rgba.resize((1536,448),Image.Resampling.NEAREST).save(p/'native-turnaround-4x.png')
 (p/'native-finish.json').write_text(json.dumps({'source':str((p/'turnaround-source.png').relative_to(R)),'sourceSHA256':hashlib.sha256((p/'turnaround-source.png').read_bytes()).hexdigest(),'sourceSize':im.size,'nativeCell':[96,112],'anchor':[48,100],'finish':'single-scale premultiplied area reduction, binary alpha, shared96-color palette; explicit native visual inspection required; not a native-grid source','records':records},indent=2)+'\n')
if __name__=='__main__':
 import sys
 prepare(sys.argv[1])
