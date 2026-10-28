"""Finish original host-illustrated sources,never draw replacement anatomy or costumes."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[2];S=R/'assets-src/npcs/phase3a-art-rebuild';D=R/'docs/phase3a-art-rebuild';IDS=['seoyeon','minseo','harin'];DIRS=['front','back','left','right']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def clean(im):
 a=np.array(im.convert('RGBA'));c=a[:,:,:3].astype(int);key=(c[:,:,0]>145)&(c[:,:,2]>145)&(c[:,:,0]-c[:,:,1]>100)&(c[:,:,2]-c[:,:,1]>100);a[key]=0;return Image.fromarray(a)
def finish(id):
 p=S/id;raw=Image.open(p/'turnaround-source.png').convert('RGBA');im=clean(raw);im.save(p/'turnaround-keyed.png');w,h=im.size;views=[];records=[];splitY={'seoyeon':627,'minseo':640,'harin':612}[id]
 for i,d in enumerate(DIRS):
  box=[i%2*w//2,0 if i<2 else splitY,(i%2+1)*w//2,splitY if i<2 else h];q=im.crop(box);bb=q.getbbox();assert bb;views.append(q.crop(bb));records.append({'direction':d,'sourceQuadrant':box,'sourceBounds':bb})
 scale=80/max(q.height for q in views);native=[]
 for q,row in zip(views,records):
  size=(round(q.width*scale),round(q.height*scale));q=q.resize(size,Image.Resampling.BOX);a=np.array(q);a[a[:,:,3]<128]=0;a[a[:,:,3]>=128,3]=255;q=Image.fromarray(a);out=Image.new('RGBA',(96,112));placement=(48-size[0]//2,100-size[1]);out.alpha_composite(q,placement);native.append(out);row.update({'size':size,'placement':placement})
 board=Image.new('RGBA',(384,112))
 for i,q in enumerate(native):board.alpha_composite(q,(i*96,0))
 bg=Image.new('RGB',board.size,(29,27,36));bg.paste(board,mask=board.getchannel('A'));pal=bg.quantize(colors=96,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE);board=pal.convert('RGBA')
 alpha=Image.new('L',board.size)
 for i,q in enumerate(native):alpha.paste(q.getchannel('A'),(i*96,0))
 board.putalpha(alpha);(p/'native').mkdir(exist_ok=True);(p/'native-unretouched').mkdir(exist_ok=True)
 for i,d in enumerate(DIRS):
  q=board.crop((i*96,0,(i+1)*96,112));q.save(p/'native-unretouched'/f'{d}.png');q.save(p/'native'/f'{d}.png')
 board.save(p/'native-turnaround.png');preview=Image.new('RGBA',board.size,(29,27,36,255));preview.alpha_composite(board);preview.resize((1536,448),Image.Resampling.NEAREST).convert('RGB').save(D/f'{id}-turnaround-review-4x.png')
 (p/'native-finish.json').write_text(json.dumps({'source':str((p/'turnaround-source.png').relative_to(R)),'sourceSHA256':sha(p/'turnaround-source.png'),'sourceSize':raw.size,'oneSourceToNativeScale':scale,'nativeCell':[96,112],'footAnchor':[48,100],'sourceIsLogicalGrid':False,'finish':'Exact high-saturation magenta alpha removal; one source-to-native BOX/premultiplied area finish for all4views,binaryalpha,shared96colour palette,no dithering; manual native inspection/retouches follow in native-retouches.json','views':records},indent=2)+'\n');print(id,'source',raw.size,'scale',scale,'native',[v['size']for v in records])
if __name__=='__main__':
 for id in IDS:finish(id)
 board=Image.new('RGBA',(288,3*136),(29,27,36,255));dr=ImageDraw.Draw(board)
 for row,id in enumerate(IDS):
  dr.text((0,row*136),'JUNI | BEFORE | '+id.upper()+' SOURCE',fill='white')
  for col,p in enumerate([R/'assets-src/characters/phase1/juni-style-reference.png',D/'before-source'/f'npc-{id}-preview-native.png',S/id/'native/front.png']):board.alpha_composite(Image.open(p).convert('RGBA'),(col*96,row*136+24))
 board.convert('RGB').save(D/'source-native-comparison.png');board.resize((1152,1632),Image.Resampling.NEAREST).convert('RGB').save(D/'source-native-comparison-4x.png')
