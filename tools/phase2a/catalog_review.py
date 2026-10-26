from pathlib import Path
from PIL import Image,ImageDraw
import json,numpy as np
R=Path(__file__).resolve().parents[2];D=R/'docs/phase2a';catalog=json.loads((R/'assets-src/characters/phase2a/cosmetics/catalog.json').read_text());names=['idle-front-0','idle-back-0','idle-left-0','idle-right-0','walk-front-3','run-back-3','wave-front-5','celebrate-front-4'];boards=[]
for item in catalog['items']:
 v=item['variants'][0];id=v['characterId'];base=Image.open(R/f'public/assets/characters/{id}/atlas.png').convert('RGBA');atlas=json.loads((R/f'public/assets/characters/{id}/atlas.json').read_text())['frames'];paint=Image.open(R/'public'/v['paint']).convert('RGBA');erase=Image.open(R/'public'/v['erase']).convert('RGBA');mapping=json.loads((R/'public'/v['mapping']).read_text())['frames'];row=Image.new('RGBA',(768,145),(29,28,36,255));dr=ImageDraw.Draw(row);dr.text((4,2),item['id'],fill=(255,227,153))
 for i,name in enumerate(names):
  f=atlas[name]['frame'];sprite=base.crop((f['x'],f['y'],f['x']+96,f['y']+112));r=mapping[name]
  if r:
   box=(r['x'],r['y'],r['x']+r['w'],r['y']+r['h']);a=np.array(sprite);mask=np.array(erase.crop(box))[:,:,3]>0;a[r['offsetY']:r['offsetY']+r['h'],r['offsetX']:r['offsetX']+r['w']][mask]=0;sprite=Image.fromarray(a);sprite.alpha_composite(paint.crop(box),(r['offsetX'],r['offsetY']))
  row.alpha_composite(sprite,(i*96,31));dr.text((i*96+2,17),name,fill='white')
 boards.append(row)
for n in range(2):
 board=Image.new('RGBA',(768,725))
 for i,row in enumerate(boards[n*5:n*5+5]):board.paste(row,(0,i*145))
 board.save(D/f'catalog-{n+1}-native.png');board.resize((1536,1450),Image.Resampling.NEAREST).save(D/f'catalog-{n+1}-review-2x.png')
