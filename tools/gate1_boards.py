"""Labelled evidence boards; no newly painted environment artwork."""
import json,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops
R=Path(__file__).resolve().parents[1];D=R/'docs/gate1';S=R/'assets-src/gate1';font=lambda n:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',n)
native=Image.open(D/'GATE1_STREET_NATIVE.png').convert('RGB');assert native.size==(1536,1024)
native.resize((3072,2048),Image.Resampling.NEAREST).save(D/'GATE1_STREET_2X.png')
north=Image.open(D/'GATE1_NORTH_REFERENCE.png').convert('RGB');approved=Image.open(R/'docs/v10-city/V10_NORTH.png').convert('RGB');exact=ImageChops.difference(north,approved).getbbox()is None;assert exact
board=Image.new('RGB',(2080,848),'#24393c');d=ImageDraw.Draw(board);d.text((16,16),'APPROVED NORTH | actual Phaser 1x',font=font(20),fill='#f4d990');d.text((1056,16),'GATE 1 CANDIDATE | actual Phaser crop 1x',font=font(20),fill='#f4d990');board.paste(north,(16,52));board.paste(native.crop((480,146,1504,914)),(1056,52));d.text((16,824),'Same source-pixel pitch, no image rescaling. Juni retains80px body. Camera crops differ; no user approval implied.',font=font(14),fill='#d7e0cf');board.save(D/'GATE1_NORTH_VS_SOUTH.png')
source=Image.open(S/'native/street-foundation.png').convert('RGB');rects=[(32,0,448,576),(448,0,784,576),(784,0,1104,576),(1104,0,1500,576)];labels=['CAFE | steel + warm stone','BOOKSHOP | ivory brick','LEARNING | glass + blue-white','CONVENIENCE | tile + canopy'];width=sum(b[2]-b[0]for b in rects)+100
board=Image.new('RGB',(width,840),'#24393c');d=ImageDraw.Draw(board);d.text((20,14),'GATE 1 | native source-art architecture/material details (not a gameplay screenshot)',font=font(20),fill='#f4d990');x=20
for rect,label in zip(rects,labels):
 crop=source.crop(rect);d.text((x,51),label,font=font(15),fill='#e5e9d8');board.paste(crop,(x,78));x+=crop.width+20
for i,(label,rect)in enumerate([('Sidewalk',(480,576,608,640)),('Asphalt',(512,656,640,720)),('Brick court',(960,848,1088,912)),('Stone transition',(496,848,624,912)),('Planted edge',(1328,816,1456,880))]):
 x=20+i*300;d.text((x,680),label,font=font(16),fill='#e5e9d8');board.paste(source.crop(rect),(x,710))
d.text((20,796),'Major architecture/ground kept1:1. Palette finish255 colors; support furniture uniformly finished separately. No procedural building art.',font=font(15),fill='#d7e0cf');board.save(D/'GATE1_ARCHITECTURE_BOARD.png')
(D/'board-provenance.json').write_text(json.dumps(dict(northPixelExact=exact,nativeSize=native.size,twoX='exact nearest-neighbor2x',comparison=dict(panel=[1024,768],southCrop=[480,146,1504,914],scale=1),architectureBoard='labelled native source-art details, no resizing',images={p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in D.glob('GATE1_*.png')}),indent=2)+'\n')
print('Native/2x/north comparison/source architecture boards saved; north exact',exact)
