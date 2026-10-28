"""Small authored native corrections of source-owned eyes,not procedural character illustration."""
from pathlib import Path
from PIL import Image
import json,numpy as np
R=Path(__file__).resolve().parents[2];S=R/'assets-src/npcs/phase3a-art-rebuild'
# Each explicit edit follows native source inspection. Colours come only from that identity's native palette.
EDITS={
 'seoyeon':{'front':[(43,37,'highlight'),(52,37,'highlight'),(44,38,'ink'),(53,38,'ink')],'left':[(40,35,'highlight'),(41,36,'ink')],'right':[(55,36,'highlight'),(55,37,'ink')]},
 'minseo':{'front':[(44,36,'highlight'),(52,36,'highlight'),(44,37,'ink'),(53,37,'ink')],'left':[(42,37,'highlight'),(42,38,'ink')],'right':[(56,37,'highlight'),(55,38,'ink')]},
 'harin':{'front':[(45,42,'highlight'),(52,41,'highlight'),(45,43,'ink'),(52,42,'ink')],'left':[(41,38,'highlight'),(41,39,'ink')],'right':[(56,38,'highlight'),(56,39,'ink')]}}
HEAD_REG={'seoyeon':{'left':(44,2),'right':(44,1)},'minseo':{'left':(47,-1),'right':(47,-1)},'harin':{'left':(45,4),'right':(45,4)}}
for id,views in EDITS.items():
 p=S/id;front=np.array(Image.open(p/'native-unretouched/front.png'));colours=front[front[:,:,3]>0][:,:3];ink=tuple(int(x)for x in colours[np.argmin(colours.mean(1))]);light=tuple(int(x)for x in colours[np.argmax(colours.mean(1))]);records=[]
 for d in ['front','back','left','right']:
  im=Image.open(p/'native-unretouched'/f'{d}.png').convert('RGBA')
  for x,y,role in views.get(d,[]):
   old=im.getpixel((x,y));assert old[3]==255,(id,d,x,y);new=(*(light if role=='highlight'else ink),255);im.putpixel((x,y),new);records.append({'direction':d,'xy':[x,y],'before':old,'after':new,'reason':'Recover own illustrated eye glint/pupil cluster lost in area finish; preserve individual face,outline and eyebrows'})
  if d in HEAD_REG[id]:
   cut,delta=HEAD_REG[id][d];head=im.crop((0,0,96,cut));out=im.copy();out.paste((0,0,0,0),(0,0,96,cut));out.alpha_composite(head,(0,delta))
   if delta<0:
    # The original neck's own last source row bridges only the static1px registration gap.
    neck=im.crop((0,cut-1,96,cut));out.alpha_composite(neck,(0,cut-1))
   im=out
  im.save(p/'native'/f'{d}.png')
 (p/'native-retouches.json').write_text(json.dumps({'method':'Explicit local native edits after visual inspection,source-owned palette only;no global filters,no face/body replacement','edits':records,'totalPixelEdits':len(records),'fixedDirectionalHeadRegistration':HEAD_REG[id],'headRegistrationReason':'Static per-view source correction aligning own eye/neck landmarks without scaling,per-frame fitting or changing feet;head artwork is translated intact'},indent=2)+'\n')
 print(id,len(records),'authored eye-cluster native finishing edits')
