from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-recovery';old=R/'docs/gate3-world';names=['palace','academy','culture','transition','retail','station','namsan','amusement','waterfront','jeju'];boxes=[(140,330,780,780),(20,120,660,570),(100,150,740,600),(100,100,740,550),(100,350,740,800),(640,300,1280,750),(400,420,1040,870),(50,200,690,650),(0,130,640,580),(0,50,640,500)];rows=[]
for page in range(3):
 out=Image.new('RGB',(1300,980),'#243634');d=ImageDraw.Draw(out)
 for i in range(4):
  j=page*4+i
  if j>=len(names):break
  name=names[j];src=old/(name+'-native.png');crop=Image.open(src).convert('RGB').crop(boxes[j]);x=10+i%2*650;y=10+i//2*490;d.text((x,y),name.upper()+' / CURRENT REJECTED CONTEXT / native1:1 crop',fill='white');out.paste(crop,(x,y+28));crop.save(D/(name+'-audit-1x.png'),optimize=True);rows.append({'region':name,'source':str(src.relative_to(R)),'sourceSha256':hashlib.sha256(src.read_bytes()).hexdigest(),'nativeCrop':boxes[j]})
 out.save(D/f'audit-native-board-{page+1}.png',optimize=True)
(D/'audit-source-evidence.json').write_text(json.dumps({'overview':'docs/gate3-world/world-overview-review.jpg','nativeAudit':rows,'scale':1,'sourceSnapshot':'ea50b0f73d31fc5cb7b39be596c423edc0be5b5b','finePixelReviewFromOverview':False},indent=2)+'\n')
