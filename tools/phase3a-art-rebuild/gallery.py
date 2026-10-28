"""Assemble labelled real-native evidence and lightweight source reviews;never modifies protected art."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,math,sys,numpy as np
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a-art-rebuild';S=R/'assets-src/npcs/phase3a-art-rebuild';sys.path.insert(0,str(Path(__file__).parent));from prepare import clean
IDs=['seoyeon','minseo','harin'];before=json.loads((D/'before-capture.json').read_text());after=json.loads((D/'after-capture.json').read_text());native=json.loads((D/'native-render-qa.json').read_text());inspector=json.loads((D/'clip-inspector-qa.json').read_text());results=[]
# Actual same-frame Photoshop-free native Phaser inspector controls.
for r in inspector['rows']:
 image=Image.open(D/r['file']).convert('RGB');state=r['state']
 for i,s in enumerate(state['sprites']):
  atlas=Image.open(R/'public'/s['source']).convert('RGBA')if s['source'].startswith('assets/')else Image.open(R/s['source']).convert('RGBA');metaPath=R/'public/assets/juni/juni.json'if i==0 else R/f'public/assets/npcs/phase3a/npc-{r["id"]}/atlas.json';f=json.loads(metaPath.read_text())['frames'][s['frame']]['frame'];source=np.array(atlas.crop((f['x'],f['y'],f['x']+96,f['y']+112)));actual=np.array(image.crop((s['x']-48,s['y']-100,s['x']+48,s['y']+12)));diff=int(((source[:,:,3]==255)&np.any(source[:,:,:3]!=actual,2)).sum());assert diff==0,(r['id'],r['direction'],i,diff);results.append({'id':r['id'],'direction':r['direction'],'slot':i,'frame':s['frame'],'mismatch':diff,'native':[96,112]})
(D/'inspector-native-qa.json').write_text(json.dumps({'status':'PASS','captures':len(results),'mismatch':0,'rows':results,'scope':'SUPPLEMENTAL actual Phaser atlas inspector;canonical gameplay evidence is separate'},indent=2)+'\n')
board=Image.new('RGB',(288,3*144),(29,27,36));dr=ImageDraw.Draw(board)
for row,id in enumerate(IDs):
 r=next(r for r in inspector['rows']if r['id']==id and r['direction']=='front');im=Image.open(D/r['file']);dr.text((2,row*144),id+' | actual Phaser clip inspector',fill='white')
 for col,s in enumerate(r['state']['sprites']):
  dr.text((col*96+2,row*144+14),['JUNI','BEFORE','AFTER'][col],fill='white');board.paste(im.crop((s['x']-48,s['y']-100,s['x']+48,s['y']+12)),(col*96,row*144+30))
board.save(D/'juni-before-after-inspector-native.png');board.resize((864,1296),Image.Resampling.NEAREST).save(D/'juni-before-after-inspector-review-3x.png')
board=Image.new('RGB',(288,3*144),(29,27,36));dr=ImageDraw.Draw(board)
for row,id in enumerate(IDs):
 a=next(r for r in after['captures']if r['id']=='npc-'+id and r['audit']['actualFrame'].startswith('greet'));b=next(r for r in before['captures']if r['id']=='npc-'+id and r['audit']['actualFrame'].startswith('greet'));shot=Image.open(a['sourcePath']).convert('RGB');p=a['audit']['player'];sx,sy=a['audit']['camera']['scroll'];x=math.floor(p['x']+.5)-48-sx;y=math.floor(p['y']+.5)-100-sy;parts=[shot.crop((x,y,x+96,y+112))]
 for r,mode in [(b,'before'),(a,'after')]:
  n=next(v for v in native['rows']if v['id']=='npc-'+id and v['mode']==mode and v['frame']==r['audit']['actualFrame']);parts.append(Image.open(D/n['file']))
 dr.text((2,row*144),id+' | actual canonical world',fill='white')
 for col,im in enumerate(parts):dr.text((col*96+2,row*144+14),['JUNI','BEFORE','AFTER'][col],fill='white');board.paste(im,(col*96,row*144+30))
board.save(D/'juni-before-after-world-native.png');board.resize((864,1296),Image.Resampling.NEAREST).save(D/'juni-before-after-world-review-3x.png')
for id in IDs:
 p=S/id;im=clean(Image.open(p/'master-source.png'));im.save(p/'master-clean-rgba.png');q=im.crop(im.getbbox());q.thumbnail((360,480),Image.Resampling.BOX);bg=Image.new('RGBA',(384,512),(29,27,36,255));bg.alpha_composite(q,((384-q.width)//2,(512-q.height)//2));bg.convert('RGB').save(D/f'{id}-master-review.jpg',quality=90)
 turn=Image.new('RGBA',(384,136));dr=ImageDraw.Draw(turn)
 for i,d in enumerate(['front','back','left','right']):dr.text((i*96,1),d,fill='white');turn.alpha_composite(Image.open(p/'native'/f'{d}.png'),(i*96,24))
 bg=Image.new('RGBA',turn.size,(29,27,36,255));bg.alpha_composite(turn);bg.convert('RGB').save(D/f'{id}-native-turnaround.png');bg.resize((1152,408),Image.Resampling.NEAREST).convert('RGB').save(D/f'{id}-native-turnaround-review-3x.png')
 for d in ['front','back','left','right']:
  seq=[]
  for i in range(8):
   q=Image.new('RGBA',(96,112),(29,27,36,255));q.alpha_composite(Image.open(p/'frames'/f'walk-{d}-{i}.png'));seq.append(q.resize((288,336),Image.Resampling.NEAREST))
  seq[0].save(D/f'{id}-walk-{d}-source-motion.webp',save_all=True,append_images=seq[1:],duration=150,loop=0,lossless=True)
print('PASS36nativePhaserinspector sprite readbacks;native world/inspector3columncomparisons;3masters/turnarounds/12sourcegait previews')
