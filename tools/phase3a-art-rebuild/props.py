"""Extract host-illustrated props,with exact native grip anchors,no procedural props."""
from pathlib import Path
from PIL import Image
import json,sys
R=Path(__file__).resolve().parents[2];S=R/'assets-src/npcs/phase3a-art-rebuild';sys.path.insert(0,str(Path(__file__).parent));from prepare import clean,sha
source=S/'activity-props-source.png';im=clean(Image.open(source));rows=[]
for id,box,size,anchor in [('seoyeon',[70,140,640,760],(6,8),(3,7)),('minseo',[670,170,1160,750],(6,6),(2,5)),('harin',[1180,150,1720,760],(5,5),(2,4))]:
 q=im.crop(box);bb=q.getbbox();assert bb;q=q.crop(bb);q.save(S/id/'activity-prop-source.png');q=q.resize(size,Image.Resampling.BOX);a=q.getchannel('A').point(lambda v:255 if v>=128 else 0);bg=Image.new('RGB',size,(29,27,36));bg.paste(q,mask=a);q=bg.quantize(colors=16,dither=Image.Dither.NONE).convert('RGBA');q.putalpha(a);q.save(S/id/'activity-prop-native.png');rows.append({'id':id,'source':str(source.relative_to(R)),'sourceSHA256':sha(source),'sourceRegion':box,'sourceBounds':bb,'nativeSize':size,'gripAnchor':anchor,'ownership':'Baked into activity frames at the actual keyed wrist;body occludes props in back view'})
(S/'activity-props.json').write_text(json.dumps(rows,indent=2)+'\n');print('3ownillustrated props extracted at native grip sizes')
