from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[2];S=R/'assets-src/npcs/phase3a-npc-expansion'
def key(im):
 a=np.array(im.convert('RGBA'));c=a[:,:,:3].astype(int);a[(c[:,:,0]>145)&(c[:,:,2]>145)&(c[:,:,0]-c[:,:,1]>100)&(c[:,:,2]-c[:,:,1]>100)]=0;return Image.fromarray(a)
source=S/'modern-props-source.png';im=key(Image.open(source));w,h=im.size;rows=[]
for i,(id,size)in enumerate([('modern-daon',(6,8)),('modern-miram',(7,7)),('modern-geonu',(7,8)),('modern-seorin',(7,8)),('modern-haru',(4,8)),('modern-yeori',(6,8))]):
 box=[i%3*w//3,i//3*h//2,(i%3+1)*w//3,(i//3+1)*h//2];q=im.crop(box);src=source
 if id=='modern-miram':src=S/id/'activity-ball-source.png';q=key(Image.open(src));box=None
 bb=q.getbbox();assert bb;q=q.crop(bb);p=S/id;q.save(p/'activity-prop-source.png');q=q.resize(size,Image.Resampling.BOX);alpha=q.getchannel('A').point(lambda v:255 if v>=128 else 0);bg=Image.new('RGB',size,(29,27,36));bg.paste(q,mask=alpha);q=bg.quantize(colors=16,dither=Image.Dither.NONE).convert('RGBA');q.putalpha(alpha);q.save(p/'activity-prop-native.png');rows.append({'id':id,'source':str(src.relative_to(R)),'sourceSHA256':hashlib.sha256(src.read_bytes()).hexdigest(),'sourceCell':box,'bounds':bb,'nativeSize':size,'grip':[size[0]//2,size[1]-1],'rejectedBoardCell':'Oval American football NOT USED; separately illustrated round association football used'if id=='modern-miram'else None})
(S/'modern-props.json').write_text(json.dumps(rows,indent=2)+'\n')
