from pathlib import Path
from PIL import Image,ImageDraw
import json,io,subprocess
import numpy as np
R=Path(__file__).resolve().parents[2];D=R/'docs/phase2b-motion/walk-front';cat=json.loads((R/'assets-src/characters/phase2a/cosmetics/catalog.json').read_text());items={i['id']:i for i in cat['items']};textures={};base=json.loads((D/'before.json').read_text())['commit'];rows=[]
def patch(sprite,v,name):
 r=json.loads((R/'public'/v['mapping']).read_text())['frames'][name]
 if r is None:return sprite
 for k in ['paint','erase']:
  if v[k]not in textures:textures[v[k]]=Image.open(R/'public'/v[k]).convert('RGBA')
 box=(r['x'],r['y'],r['x']+r['w'],r['y']+r['h']);a=np.array(sprite);mask=np.array(textures[v['erase']].crop(box))[:,:,3]>0;a[r['offsetY']:r['offsetY']+r['h'],r['offsetX']:r['offsetX']+r['w']][mask]=0;sprite=Image.fromarray(a);sprite.alpha_composite(textures[v['paint']].crop(box),(r['offsetX'],r['offsetY']));return sprite
for pre in cat['presets']:
 id=pre['appearance']['characterId'];stem=f'public/assets/characters/{id}/atlas';m=json.loads((R/(stem+'.json')).read_text())['frames'];old=Image.open(io.BytesIO(subprocess.check_output(['git','show',base+':'+stem+'.png']))).convert('RGBA');new=Image.open(R/(stem+'.png')).convert('RGBA');board=Image.new('RGBA',(768,280),(28,30,38));dr=ImageDraw.Draw(board);look=pre['appearance'];ids=[x for x in [look['hairstyleId'],look['outfitId'],*look['accessoryIds']]if x];selected=[items[i]for i in ids];variants=[next(v for v in item['variants']if v['characterId']==id)for item in selected if item['category']!='accessory']+[i['patch']for i in cat.get('interactions',[])if i['characterId']==id and all(v in ids for v in i['requiresItemIds'])]+[next(v for v in item['variants']if v['characterId']==id)for item in selected if item['category']=='accessory'];diffs=[]
 for i in range(8):
  f=m[f'walk-front-{i}']['frame'];box=(f['x'],f['y'],f['x']+96,f['y']+112);s=[]
  for row,a in enumerate([old,new]):
   sprite=a.crop(box)
   for v in variants:sprite=patch(sprite,v,f'walk-front-{i}')
   s.append(sprite);board.alpha_composite(sprite,(i*96,row*140+20))
   if row==1:sprite.save(D/f'{pre["id"]}-expected-walk-front-{i}.png')
  diffs.append(int(np.any(np.array(s[0])!=np.array(s[1]),2).sum()))
 for r,label in enumerate(['BEFORE','HOTFIX + unchanged patches']):dr.text((4,r*140+2),pre['id']+' '+label,fill='white')
 board.save(D/f'{pre["id"]}-cosmetic-native.png');rows.append({'preset':pre['id'],'changedCompositePixelsByPhase':diffs,'patchAssets':'UNCHANGED','status':'Visual review; preset coverage does not equal updated base gait approval'})
(D/'cosmetic-regression.json').write_text(json.dumps(rows,indent=2)+'\n')
