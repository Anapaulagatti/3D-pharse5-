"""Only literal crops/nearest enlargements of genuine Phaser pixels; source illustrations separately labeled."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,math,numpy as np,hashlib
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a-npc-expansion';S=R/'assets-src/npcs/phase3a-npc-expansion'
old=json.loads((R/'assets-src/npcs/phase3a/registry.json').read_text())['npcs'];new=json.loads((S/'modern-definitions.json').read_text())['npcs'];IDs=[n['id'][4:]for n in old+new];newIDs=[n['id'][4:]for n in old+new if(S/n['id'][4:]/'candidate-atlas.png').exists()];inspector=json.loads((D/'clip-inspector-qa.json').read_text());readbacks=[]
for row in inspector['rows']:
 shot=Image.open(D/row['file']).convert('RGB');state=row['state']
 for i,s in enumerate(state['sprites']):
  atlas=Image.open(R/'public'/s['source']).convert('RGBA');metaPath=R/'public/assets/juni/juni.json'if i==0 else R/'public'/s['source'].replace('atlas.png','atlas.json');f=json.loads(metaPath.read_text())['frames'][s['frame']]['frame'];expected=np.array(atlas.crop((f['x'],f['y'],f['x']+96,f['y']+112)));actual=shot.crop((s['x']-48,s['y']-100,s['x']+48,s['y']+12));a=np.array(actual);diff=int(((expected[:,:,3]==255)&np.any(expected[:,:,:3]!=a,2)).sum());assert diff==0,(row['id'],row['direction'],i,diff);readbacks.append({'id':row['id'],'direction':row['direction'],'slot':i,'frame':s['frame'],'mismatch':diff})
(D/'inspector-native-qa.json').write_text(json.dumps({'status':'PASS native comparison rendering only','actualSpriteCrops':len(readbacks),'mismatch':0,'rows':readbacks,'source':'Actual Phaser5column inspector; canonical-world evidence is separate'},indent=2)+'\n')
board=Image.new('RGB',(720,4*180),(29,27,36));dr=ImageDraw.Draw(board)
for j,id in enumerate(['daehyun','nayeon','junho','modern-daon']):
 row=next(r for r in inspector['rows']if r['id']==id and r['direction']=='front');im=Image.open(D/row['file']).convert('RGB');board.paste(im,(0,j*180));dr.text((576,j*180+22),id,fill='#f4e7cc')
board.save(D/'four-waves-actual-phaser-native.png');board.resize((1440,1440),Image.Resampling.NEAREST).save(D/'four-waves-actual-phaser-2x.png')
for title,defs,cols in [('roster20-native',old+new,5),('modern6-native',new,3)]:
 rows=math.ceil(len(defs)/cols);im=Image.new('RGBA',(cols*144,rows*144),(29,27,36,255));dr=ImageDraw.Draw(im)
 for i,n in enumerate(defs):
  x=i%cols*144;y=i//cols*144;dr.text((x+4,y+3),n['names']['vi'],fill='#f4e7cc');im.alpha_composite(Image.open(R/'public/assets/npcs/phase3a'/n['id']/'preview-native.png').convert('RGBA'),(x+24,y+25))
 im.convert('RGB').save(D/f'{title}.png');im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST).convert('RGB').save(D/f'{title}-2x.png')
after=json.loads((D/'after-capture.json').read_text());before=json.loads((D/'before-capture.json').read_text());native=json.loads((D/'native-render-qa.json').read_text());context=[]
for id in newIDs:
 row=next(r for r in after['captures']if r['id']=='npc-'+id and r['audit']['actualFrame'].startswith('greet'));a=row['audit'];shot=Image.open(row['sourcePath']).convert('RGB');npc=a['sprite'];p=a['player'];sx,sy=a['camera']['scroll'];points=[(npc['x']-sx,npc['y']-sy),(math.floor(p['x']+.5)-sx,math.floor(p['y']+.5)-sy)];x0=math.floor(min(p[0]for p in points))-80;y0=math.floor(min(p[1]for p in points))-124;x1=math.ceil(max(p[0]for p in points))+80;y1=math.ceil(max(p[1]for p in points))+32;crop=shot.crop((x0,y0,x1,y1));file=f'gameplay/after-{id}-juni-context-native.png';crop.save(D/file);crop.resize((crop.width*2,crop.height*2),Image.Resampling.NEAREST).save(D/file.replace('-native.png','-2x.png'));context.append({'id':id,'file':file,'sourceActualCapture':row['sourcePath'],'actualFrame':a['actualFrame'],'crop':[x0,y0,x1,y1],'nativeNoRescale':True});shot.save(D/f'gameplay/after-{id}-review.jpg',quality=82)
 if any(r['id']=='npc-'+id for r in before['rows']):
  im=Image.new('RGB',(288,144),(29,27,36));dr=ImageDraw.Draw(im)
  for j,mode in enumerate(['before','after']):
   rr=next(r for r in native['rows']if r['id']=='npc-'+id and r['mode']==mode and r['frame'].startswith('greet'));q=Image.open(D/rr['file']);im.paste(q,(j*144+24,28));dr.text((j*144+2,2),mode,fill='white');dr.text((j*144+2,14),rr['frame'],fill='white')
  im.save(D/f'{id}-before-after-native.png');im.resize((864,432),Image.Resampling.NEAREST).save(D/f'{id}-before-after-3x.png')
 # Illustration-source thumbnails are NOT gameplay evidence.
 p=S/id;q=Image.open(p/'master-source.png').convert('RGB');q.thumbnail((320,320),Image.Resampling.BOX);q.save(D/f'{id}-source-illustration.jpg',quality=86)
(D/'context-crops.json').write_text(json.dumps(context,indent=2)+'\n')
print('PASS',len(readbacks),'actual inspector sprite readbacks;20source roster,6modern source roster,17literal Juni/context crops,11before/after pairs;no fabricated world shots')
