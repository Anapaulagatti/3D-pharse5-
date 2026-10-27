from pathlib import Path
from PIL import Image,ImageDraw
import json,math,hashlib
import numpy as np
R=Path(__file__).resolve().parents[2];D=R/'docs/phase2b-motion/walk-front';rows=[]
for id in ['juni','ara','doyun','sori','jiwon','nari','taeyang','yuna','hyunwoo']:
 q=json.loads((D/f'{id}-gameplay.json').read_text());assert not q['errors'];assert len(q['rows'])==1;clip=q['rows'][0];assert len(clip['samples'])==24
 stem='public/assets/juni/juni'if id=='juni'else f'public/assets/characters/{id}/atlas';atlas=Image.open(R/(stem+'.png')).convert('RGBA');m=json.loads((R/(stem+'.json')).read_text())['frames'];board=Image.new('RGB',(768,132),(28,30,38));dr=ImageDraw.Draw(board)
 for s in clip['samples']:
  a=s['audit'];st=a['state'];sx,sy=a['camera']['scroll'];f=m[a['actualFrame']]['frame'];src=np.array(atlas.crop((f['x'],f['y'],f['x']+96,f['y']+112)));shot=Image.open(s['sourcePath']).convert('RGB');x=math.floor(st['x']+.5)-48-sx;y=math.floor(st['y']+.5)-100-sy;body=shot.crop((x,y,x+96,y+112));diff=int(((src[:,:,3]==255)&np.any(src[:,:,:3]!=np.array(body),2)).sum());assert diff==0,(id,s['loop'],s['index'],diff);assert a['camera']['zoom']==1 and st['samplingMode']==1 and all(float(v).is_integer()for v in [sx,sy]);name=f'{id}-loop{s["loop"]}-{s["index"]}';body.save(D/(name+'-body-native.png'));shot.crop((x-48,y-56,x+144,y+168)).save(D/(name+'-context-native.png'))
  if s['loop']==0:board.paste(body,(s['index']*96,20));dr.text((s['index']*96+3,2),str(s['index']),fill='white')
  rows.append({'id':id,'loop':s['loop'],'index':s['index'],'actualFrame':a['actualFrame'],'diffPixels':diff,'nearest':True,'integerCamera':True,'zoom':1,'fullPNG_SHA256':hashlib.sha256(Path(s['sourcePath']).read_bytes()).hexdigest()})
 board.save(D/f'{id}-actual-native.png');first=clip['samples'][0];Image.open(first['sourcePath']).save(D/f'{id}-full-phaser-native.png')
 assert clip['end']['y']>clip['start']['y']+44*3;assert all(r['players']==1 and r['sampling']==1 for r in clip['trace'])
(D/'readbacks.json').write_text(json.dumps({'captures':len(rows),'rows':rows,'diffPixels':sum(r['diffPixels']for r in rows),'actualLoops':27,'reference':'Actual canonical Phaser,9 actors x3consecutive loops x8phases, original60speed, WASD input, native1:1; no forced pose.'},indent=2)+'\n');assert len(rows)==216;print('PASS216actual native1:1 readbacks;0mismatch;27complete loops; one actor')
