"""Labelled review layout only: generated concepts + untouched real Phaser crops."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
R=Path(__file__).resolve().parents[1];Q=R/'docs/gwanghwamun';S=R/'assets-src/gwanghwamun'
im=Image.new('RGB',(1680,1710),'#eee8d9');d=ImageDraw.Draw(im)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def text(x,y,t,size=18,color='#34443d'):d.text((x,y),t,font=ImageFont.truetype(font,size),fill=color)
text(24,20,'KOREAN ARENA / GWANGHWAMUN PLAZA',32)
text(24,66,'Three environment concepts. Juni provisionally selected; plaza direction still awaits your approval.',18)
for i,(key,title,desc) in enumerate([('A','ROYAL STONE PROMENADE','Formal axis / pale granite / civic calm'),('B','GINKGO COMMONS — RECOMMENDED','Reading garden / warm wood / intimate social pockets'),('C','HANJI LANTERN COURT','Festival courtyard / evening lanterns / cultural stage')]):
 x=24+i*552;src=Image.open(S/f'concepts/{key}.png');src=src.resize((528,352),Image.Resampling.BOX);im.paste(src,(x,110))
 text(x,472,f'{key} / {title}',18);text(x,500,desc,14);text(x,524,'Generated source concept, NOT an engine screenshot.',13,'#786e5e')
text(24,562,'B / REAL PHASER — NATIVE 1×',24)
game=Image.open(Q/'phaser-native-day.png').convert('RGB');assert game.size==(1024,768);im.paste(game,(24,604))
text(24,1380,'Native image pasted pixel-for-pixel. No concept plate is used as the game background.',15)
text(1080,566,'JUNI AT GAMEPLAY SCALE',22)
text(1080,604,'Body80px · four static directions',17)
text(1080,632,'Not a walk/idle animation set.',17)
crop=game.crop((472,504,552,608));im.paste(crop,(1080,675));im.paste(crop.resize((320,416),Image.Resampling.NEAREST),(1200,675))
text(1080,1110,'1×',17);text(1200,1110,'4× actual Phaser pixels',17)
text(1080,1145,'Gate336px high / tea hall210px',17)
text(1080,1173,'Landmark doors remain readable beside Juni.',16)
text(1080,1207,'Generated image props + Forge finish/palette',16)
text(1080,1235,'32px extracted terrain / Tiled map / 33 solids',16)
text(1080,1269,'WASD · Shift · E · touch · Canvas fallback',16)
text(1080,1297,'Water + leaves + lantern tint; reduced motion',16)
text(1080,1331,'Original town retained. No public deployment.',16)
text(24,1420,'DETAIL / 2× NEAREST — REAL PHASER ROOF',18)
detail=game.crop((300,100,684,220)).resize((768,240),Image.Resampling.NEAREST);im.paste(detail,(24,1452))
for i,(name,label) in enumerate([('behind-tree','BEHIND / opaque-pixel cue'),('front-tree','FRONT / clear character')]):
 x=840+i*300;text(x,1420,label,16);p=Image.open(Q/f'{name}.png').convert('RGB').crop((680,470,936,710))
 if name=='front-tree':p=Image.open(Q/f'{name}.png').convert('RGB').crop((680,500,936,740))
 im.paste(p,(x,1452))
im.save(Q/'world-review-board.png')
print(Q/'world-review-board.png')
