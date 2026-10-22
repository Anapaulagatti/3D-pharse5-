from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3a';font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
# Review derivatives only; native captures and approved sources stay untouched.
pairs=[('NORTH',R/'docs/gate2/A_NATIVE_1X.png',(460,180,1536,1024),D/'north-native.png',(0,0,1076,844)),('JEJU',R/'docs/gate2/C_NATIVE_1X.png',(0,245,960,1145),D/'jeju-native.png',(320,0,1280,900)),('STATION',R/'docs/gate25-station-planters/AFTER_NATIVE_1X.png',(1904,247,3184,1147),D/'station-native.png',(0,0,1280,900))]
board=Image.new('RGB',(1200,1110),'#192832');draw=ImageDraw.Draw(board)
for i,(name,a,ra,b,rb) in enumerate(pairs):
 for col,(p,box,title) in enumerate([(a,ra,'Approved baseline'),(b,rb,'G3-A native chunk rendering')]):
  im=Image.open(p).convert('RGB').crop(box)
  im.thumbnail((586,312),Image.Resampling.NEAREST);board.paste(im,(col*600+6,i*370+46));draw.text((col*600+8,i*370+12),name+' / '+title,font=font,fill='white')
board.save(D/'APPROVED_VS_G3A_REVIEW.jpg',quality=86,optimize=True)
for name in ['north-native','jeju-native','station-native','world-overview','mobile-tour']:
 im=Image.open(D/f'{name}.png').convert('RGB');im.thumbnail((960,700),Image.Resampling.NEAREST);im.save(D/f'{name}-preview.jpg',quality=85,optimize=True)
# Each crop is untouched original-resolution screenshot pixels.
for name,rect in [('north-native',(200,250,520,490)),('jeju-native',(650,250,970,490)),('station-native',(760,300,1080,540))]:Image.open(D/f'{name}.png').crop(rect).save(D/f'{name}-pixels-1x.png')
# Explicit spatial-review diagram; this is not gameplay or revised planning authority.
canvas=Image.new('RGB',(1050,1040),'#192832');d=ImageDraw.Draw(canvas);scale=.18;ox,oy=90,75
preview=Image.open(R/'public/assets/gate3/world/overview.png').convert('RGB').resize((int(4352*scale),int(4864*scale)),Image.Resampling.NEAREST);canvas.paste(preview,(ox,oy))
def box(rect,color,width=3):x,y,w,h=rect;d.rectangle((ox+x*scale,oy+y*scale,ox+(x+w)*scale,oy+(y+h)*scale),outline=color,width=width)
box([0,0,4352,4864],'white');box([-225.5,1913,3184,1214],'#ff817c');box([2238.5,2180,720,720],'#ffd36e');box([3180,3200,1024,1536],'#8affdc')
d.text((20,15),'REGISTRATION CONFLICT / diagnostic only, approved plan unchanged',font=font,fill='white')
for i,t in enumerate(['Red: intact district anchored to protected station -> west edge -225.5px','Yellow: protected station source origin (2238.5,2180); half-pixel phase','Green: approved expanded Jeju native frame (3180,3200,1024,1536)','No relocation, scaling or masterplan amendment applied.']):d.text((20,955+i*21),t,font=font,fill='white')
canvas.save(D/'registration-conflict.png',optimize=True)
print('Review boards and native crops complete')
