"""Label/crop real Phaser captures only; never paint game pixels."""
from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];Q=R/'docs/stage-b-polish/quality'
summary=Image.new('RGB',(1040,1740),'#eee7d6');sd=ImageDraw.Draw(summary)
sd.text((16,12),'ACTUAL PHASER / BEFORE 323b44b vs STAGE B POLISH / thumbnails 50%',fill='#203c32')
for i,name in enumerate(['academy','workshop','museum','gate']):
    a=Image.open(Q/f'before/{name}-native.png').convert('RGB');b=Image.open(Q/f'after/{name}-native.png').convert('RGB');assert a.size==b.size==(1024,768)
    board=Image.new('RGB',(2048,808),'#eee7d6');d=ImageDraw.Draw(board)
    d.text((20,12),f'BEFORE / accepted Stage B baseline / {name} / native 1x',fill='#203c32');d.text((1044,12),f'AFTER / targeted polish / {name} / native 1x',fill='#203c32');board.paste(a,(0,40));board.paste(b,(1024,40));board.save(Q/f'{name}-before-after-native.png')
    y=40+i*420;summary.paste(a.resize((512,384),Image.Resampling.NEAREST),(8,y+24));summary.paste(b.resize((512,384),Image.Resampling.NEAREST),(520,y+24));sd.text((16,y),f'{name.upper()} / BEFORE',fill='#203c32');sd.text((532,y),'AFTER',fill='#203c32')
summary.save(Q/'review-board.png')
for name,box in [('academy',(220,568,412,696)),('museum',(728,334,920,462)),('workshop',(222,410,414,538))]:
    im=Image.open(Q/f'after/{name}-native.png');im.crop(box).resize((768,512),Image.Resampling.NEAREST).save(Q/f'{name}-detail-4x.png')
print('Four native before/after boards; summary thumbnails explicitly50%; real-render crops4x.')
