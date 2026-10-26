"""Read actual POST_RENDER captures and compare against the independently packed native art."""
from pathlib import Path
from PIL import Image
import numpy as np,json,math
R=Path(__file__).resolve().parents[2];D=R/'docs/phase2a';q=json.loads((D/'actual-gameplay.json').read_text());cat=json.loads((R/'assets-src/characters/phase2a/cosmetics/catalog.json').read_text());items={i['id']:i for i in cat['items']};textures={};report=[]
def patch(sprite,v,name):
 root=R/'public';mapping=json.loads((root/v['mapping']).read_text())['frames'];r=mapping[name]
 if r is None:return sprite
 if v['paint']not in textures:textures[v['paint']]=Image.open(root/v['paint']).convert('RGBA');textures[v['erase']]=Image.open(root/v['erase']).convert('RGBA')
 box=(r['x'],r['y'],r['x']+r['w'],r['y']+r['h']);a=np.array(sprite);mask=np.array(textures[v['erase']].crop(box))[:,:,3]>0;a[r['offsetY']:r['offsetY']+r['h'],r['offsetX']:r['offsetX']+r['w']][mask]=0;sprite=Image.fromarray(a);sprite.alpha_composite(textures[v['paint']].crop(box),(r['offsetX'],r['offsetY']));return sprite
for row in q['rows']:
 a=row['audit'];state=a['state'];id=row['id'];name=a.get('actualFrame',state['frame']);meta=json.loads((R/f'public/assets/characters/{id}/atlas.json').read_text())['frames'];atlas=Image.open(R/f'public/assets/characters/{id}/atlas.png').convert('RGBA');f=meta[name]['frame'];sprite=atlas.crop((f['x'],f['y'],f['x']+96,f['y']+112));look=state['appearance'];ids=[v for v in [look['hairstyleId'],look['outfitId'],*look['accessoryIds']]if v];selected=[items[v]for v in ids]
 variants=[next(v for v in item['variants']if v['characterId']==id)for item in selected if item['category']!='accessory']+[i['patch']for i in cat.get('interactions',[])if i['characterId']==id and all(v in ids for v in i['requiresItemIds'])]+[next(v for v in item['variants']if v['characterId']==id)for item in selected if item['category']=='accessory']
 for v in variants:sprite=patch(sprite,v,name)
 shot=Image.open(row['sourcePath']).convert('RGB');sx,sy=a['camera']['scroll'];x=math.floor(state['x']+.5)-48-sx;y=math.floor(state['y']+.5)-100-sy;actual=shot.crop((x,y,x+96,y+112));rgb=np.array(sprite);diff=int(((rgb[:,:,3]==255)&np.any(np.array(actual)!=rgb[:,:,:3],2)).sum());assert diff==0,(row['mode'],name,diff);assert a['camera']['zoom']==1 and all(float(v).is_integer()for v in [sx,sy]);assert state['samplingMode']==1
 dest=f'{row["mode"]}-{row["action"]}-{row["view"]}-native-crop.png';actual.save(D/dest);shot.crop((x-72,y-56,x+168,y+168)).save(D/f'{row["mode"]}-{row["action"]}-{row["view"]}-context-native.png');report.append({'mode':row['mode'],'clip':row['action']+'-'+row['view'],'actualFrame':name,'opaqueNativePixels':int((rgb[:,:,3]==255).sum()),'unexplainedPixelMismatch':diff,'native':[96,112],'scale':[1,1],'nearest':True,'integerCamera':True,'observedFrames':row['observedFrames'],'crop':dest})
for mode in q['modes']:
 rows=[r for r in report if r['mode']==mode['name']];board=Image.new('RGB',(672,256))
 for i,r in enumerate(rows):board.paste(Image.open(D/r['crop']),(i%7*96,i//7*128+16))
 from PIL import ImageDraw
 dr=ImageDraw.Draw(board)
 for i,r in enumerate(rows):dr.text((i%7*96+2,i//7*128+2),r['clip'],fill='white')
 board.save(D/f'{mode["name"]}-actual-native-sheet.png');board.resize((1344,512),Image.Resampling.NEAREST).save(D/f'{mode["name"]}-actual-review-2x.png')
(D/'native-pixel-qa.json').write_text(json.dumps({'method':'Opaque pixels from actual native Phaser backing PNGs compared with source atlas plus independently decoded sparse item/ownership masks; zero resampling. Normalized actor positions use JS Math.round semantics.','rows':report,'captures':len(report),'unexplainedPixelMismatch':sum(r['unexplainedPixelMismatch']for r in report),'humanArtAcceptance':'PENDING'},indent=2)+'\n');print('Native actual Phaser pixel readbacks:',len(report),'mismatch0')
