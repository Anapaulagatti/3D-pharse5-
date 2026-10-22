from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib
D=Path(__file__).resolve().parents[1]/'docs/gate25';font=lambda n:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',n)
for name in ['FOLLOW','SCENIC','OVERVIEW','TOUR_1','TOUR_2','TOUR_3','TOUR_4','MUNEUM_TOUR','DISTRICT_1540','DISTRICT_1998','DISTRICT_2520','DISTRICT_2824','JEJU25_NATIVE_1X','DISTRICT_NATIVE_1X']:
 p=D/(name+'.png')
 if p.exists():
  im=Image.open(p).convert('RGB');im.thumbnail((1400,900),Image.Resampling.LANCZOS);im.save(D/(name+'_REVIEW.jpg'),quality=85,optimize=True,subsampling=0)
board=Image.new('RGB',(1120,600),'#20383c');dr=ImageDraw.Draw(board)
for name,label,x,y in [('FOLLOW','Follow /native1:1',0,0),('SCENIC','Manual Scenic /50%',560,0),('OVERVIEW','Full overview /25% orientation',0,300),('TOUR_4','Cinematic Tour /50% house stop',560,300)]:
 dr.text((x+10,y+6),label,font=font(18),fill='#f3e9d0');im=Image.open(D/(name+'.png')).convert('RGB');im.thumbnail((550,255));board.paste(im,(x+5,y+35))
board.save(D/'MOBILE_MODES.jpg',quality=87,optimize=True,subsampling=0)
crops=[]
for x,label in [(1488,'MUNEUM_BAKERY'),(2464,'BAKERY_STATION')]:
 source=D/'DISTRICT_NATIVE_1X.png';box=(x-150,650,x+200,930);crop=Image.open(source).crop(box);p=D/(label+'_CROP_1X.png');crop.save(p,optimize=True);assert Image.open(p).tobytes()==Image.open(source).crop(box).tobytes();crop.resize((700,560),Image.Resampling.NEAREST).save(D/(label+'_2X.png'));crops.append(dict(path=p.name,source=source.name,box=box,pixelEquality=True))
(D/'review-images.json').write_text(json.dumps(dict(crops=crops,images=[dict(path=p.name,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())for p in sorted(D.iterdir())if p.suffix in ['.png','.jpg']]),indent=2)+'\n');print('PASS lightweight review derivatives, native seam crops and nearest2x images')
