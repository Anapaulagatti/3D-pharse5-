from pathlib import Path
import json
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];D=R/'docs/phase2a'
def source(id):
 p=R/'public/assets';base=p/'juni/juni'if id=='juni'else p/f'characters/{id}/atlas';return Image.open(str(base)+'.png').convert('RGBA'),json.loads(Path(str(base)+'.json').read_text())['frames']
def frame(id,name):
 atlas,m=source(id);f=m[name]['frame'];return atlas.crop((f['x'],f['y'],f['x']+96,f['y']+112))
board=Image.new('RGBA',(576,136),(29,28,36,255));dr=ImageDraw.Draw(board)
for i,id in enumerate(['juni','haneul','bomi','minjun','ara','doyun']):board.alpha_composite(frame(id,'idle-front-0'),(i*96,22));dr.text((i*96+6,5),id,fill='white')
board.save(D/'six-original-appearances-native.png');board.resize((1152,272),Image.Resampling.NEAREST).save(D/'six-original-appearances-review-2x.png')
for id in ['ara','doyun']:
 board=Image.new('RGBA',(1536,528),(29,28,36,255));dr=ImageDraw.Draw(board)
 for row,key in enumerate(['walk-front','walk-back','run-front','run-back']):
  for i in range(8):
   x=i*192;y=row*132;board.alpha_composite(frame('juni',f'{key}-{i}'),(x,y+20));board.alpha_composite(frame(id,f'{key}-{i}'),(x+96,y+20));dr.text((x+2,y+3),f'{key} {i} Juni/{id}',fill='white')
 board.save(D/f'juni-vs-{id}-native.png')
