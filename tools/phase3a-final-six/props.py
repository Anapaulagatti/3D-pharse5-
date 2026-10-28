"""Native source-owned prop finishing and exact wrist registration; no primary art drawing."""
from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[2];S=R/'assets-src/npcs/phase3a-final-six';src=S/'activity-props-source.png'
a=np.array(Image.open(src).convert('RGBA'));c=a[:,:,:3].astype(int);a[(c[:,:,0]>145)&(c[:,:,2]>145)&(c[:,:,0]-c[:,:,1]>100)&(c[:,:,2]-c[:,:,1]>100)]=0;im=Image.fromarray(a);w,h=im.size;rows=[]
for i,(id,size) in enumerate([('seondeok',(6,8)),('sejong',(8,7)),('jang',(9,10)),('saimdang',(9,9)),('yi',(9,8)),('yu',(6,8))]):
 p=S/('history-'+id);box=[i%3*w//3,i//3*h//2,(i%3+1)*w//3,(i//3+1)*h//2];q=im.crop(box);b=q.getbbox();assert b;q=q.crop(b);q.save(p/'activity-prop-source.png');q=q.resize(size,Image.Resampling.BOX);alpha=q.getchannel('A').point(lambda v:255 if v>=128 else 0);bg=Image.new('RGB',size,(29,27,36));bg.paste(q,mask=alpha);q=bg.quantize(colors=16,dither=Image.Dither.NONE).convert('RGBA');q.putalpha(alpha)
 # Put an actual opaque lowest grip pixel at canvas center/bottom, so it
 # touches the authored wrist instead of floating beside the hand.
 a=np.array(q);yy,xx=np.where(a[:,:,3]>0);lowest=int(yy.max());xs=xx[yy==lowest];gx=int(min(xs,key=lambda x:abs(x-size[0]//2)));half=max(gx,size[0]-1-gx);canvas=Image.new('RGBA',(half*2+1,lowest+1));canvas.alpha_composite(q,(half-gx,0));canvas.save(p/'activity-prop-native.png')
 rows.append({'id':'npc-history-'+id,'source':str(src.relative_to(R)),'sourceSHA256':hashlib.sha256(src.read_bytes()).hexdigest(),'sourceCell':box,'sourceBounds':b,'finishSize':size,'nativeCanvas':canvas.size,'grip':[half,lowest],'rights':'Independently illustrated fictional prop, no museum/portrait tracing; not verified historical apparatus'})
(S/'activity-props.json').write_text(json.dumps(rows,indent=2)+'\n');print('Six own illustrated props native-finished; actual opaque grip registered at wrist')
