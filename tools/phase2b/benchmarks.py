from pathlib import Path
import json,subprocess,io
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];D=R/'docs/phase2b';ids=['juni','haneul','bomi','minjun','ara','doyun','sori','jiwon','nari','taeyang','yuna','hyunwoo'];cache={}
def frame(id,name,approved=False):
 key=(id,approved)
 if key not in cache:
  stem='public/assets/juni/juni'if id=='juni'else f'public/assets/characters/{id}/atlas'
  def data(ext):return subprocess.check_output(['git','show','ed75734d0e0865274ca0b82bab2495d78878d24b:'+stem+ext])if approved else (R/(stem+ext)).read_bytes()
  cache[key]=(Image.open(io.BytesIO(data('.png'))).convert('RGBA'),json.loads(data('.json'))['frames'])
 sheet,meta=cache[key];f=meta[name]['frame'];return sheet.crop((f['x'],f['y'],f['x']+96,f['y']+112))
def save(im,name):
 im.save(D/(name+'-native.png'));im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST).save(D/(name+'-review-2x.png'))
board=Image.new('RGBA',(1152,136),(29,28,36,255));dr=ImageDraw.Draw(board)
for i,id in enumerate(ids):board.alpha_composite(frame(id,'idle-front-0'),(i*96,22));dr.text((i*96+4,4),id,fill='white')
save(board,'twelve-character-lineup')
oldboard=Image.new('RGBA',(1152,136),(29,28,36,255));dr=ImageDraw.Draw(oldboard)
for i,id in enumerate(ids[:6]):
 a=frame(id,'idle-front-0',True);b=frame(id,'idle-front-0');assert a.tobytes()==b.tobytes();oldboard.alpha_composite(a,(i*192,22));oldboard.alpha_composite(b,(i*192+96,22));dr.text((i*192+2,4),id+' approved/current',fill='white')
save(oldboard,'protected-six-reference-comparison')
for id in ids[6:]:
 im=Image.open(R/f'assets-src/characters/phase2b/{id}/native-turnaround.png');save(im,id+'-turnaround')
 for action in ['walk','run']:
  board=Image.new('RGBA',(1536,528),(29,28,36,255));dr=ImageDraw.Draw(board)
  for row,view in enumerate(['front','back','left','right']):
   for i in range(8):
    x=i*192;y=row*132;board.alpha_composite(frame('juni',f'{action}-{view}-{i}'),(x,y+20));board.alpha_composite(frame(id,f'{action}-{view}-{i}'),(x+96,y+20));dr.text((x+2,y+3),f'{view} {i} Juni/{id}',fill='white')
  board.save(D/f'juni-vs-{id}-{action}-native.png')
 for action in ['wave','celebrate']:
  seq=[]
  for i in range(8):
   im=Image.new('RGBA',(96,112),(29,28,36,255));im.alpha_composite(frame(id,f'{action}-front-{i}'));seq.append(im)
  seq[0].save(D/f'{id}-{action}-motion-native.png',save_all=True,append_images=seq[1:],duration=100,loop=0,disposal=0,blend=0)
print('Twelve native identities, six protected source comparisons, twelve Juni gait comparisons and native emotes')
