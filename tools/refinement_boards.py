"""Label and arrange genuine engine evidence. Does not repaint game artwork."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1];Q=R/'docs/world-refinement/quality';font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18);small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
def canvas(w,h):return Image.new('RGB',(w,h),'#172f2e')
def text(im,xy,s,f=font):ImageDraw.Draw(im).text(xy,s,fill='#fff0c8',font=f)
for name in ['palace','academy','workshop','museum']:
 a=Image.open(Q/f'before-{name}-native.png').convert('RGB');b=Image.open(Q/f'after-{name}-native.png').convert('RGB');board=canvas(2080,824);board.paste(a,(8,48));board.paste(b,(1048,48));text(board,(12,12),'BEFORE / Stage B / native 1x');text(board,(1052,12),'AFTER / Compact Living Seoul / native 1x');board.save(Q/f'{name}-comparison.png')
# Full district is explicitly an overview at0.5x, not mislabelled as native gameplay.
board=canvas(1760,1430);text(board,(20,16),'LIVING SEOUL / compact royal-to-modern review / actual Phaser renders')
board.paste(Image.open(Q/'overview.png').convert('RGB'),(16,52));text(board,(20,1024),'2304x1920 world, overview0.5x. Same native Juni80pxbody and building pixels.',small)
for name,y,label in [('palace',52,'Royal hall / new meaningful destination'),('modern',482,'Book & tea / ONE modern street corner')]:
 im=Image.open(Q/f'after-{name}-native.png').convert('RGB').resize((512,384),Image.Resampling.NEAREST);board.paste(im,(1200,y));text(board,(1200,y+392),label,small);text(board,(1200,y+414),'0.5x thumbnail; full native screenshot supplied',small)
# Native enlarged evidence crops, nearest-neighbour only, no synthesized pixels.
for name,x,crop in [('academy',16,(320,280,576,440)),('workshop',552,(384,304,640,464)),('modern',1088,(384,568,640,728))]:
 im=Image.open(Q/f'after-{name}-native.png').convert('RGB').crop(crop).resize((512,320),Image.Resampling.NEAREST);board.paste(im,(x,1080));text(board,(x,1403),name+' / exact screenshot crop enlarged2x',small)
board.save(Q/'review-board.png')
# Actual native avatar+architecture scale, labelled unscaled screenshot above and2x crop below.
im=Image.open(Q/'after-palace-native.png').convert('RGB');detail=im.crop((368,200,656,344)).resize((864,432),Image.Resampling.NEAREST);detail.save(Q/'palace-avatar-detail-3x.png')
print('4native before/after boards + actual Phaser overview/detail board saved; no artwork generation.')
