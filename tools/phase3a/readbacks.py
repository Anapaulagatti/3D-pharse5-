"""Independent native atlas-versus-real-Phaser readback; opaque body pixels only, not artificial visual approval."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,numpy as np,math,sys
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a';folder=D/('pilot'if'pilot'in sys.argv else'gameplay');rows=[]
p=folder/'actual-pilot.json'
if p.exists():
 for r in json.loads(p.read_text())['rows']:rows.append({'file':r['id']+'-actual-native.png','audit':r['audit']})
p=folder/'actual-motion.json'
if p.exists():
 for r in json.loads(p.read_text())['rows']:rows.extend(r['captures'])
p=folder/'actual-gameplay.json'
if p.exists():rows+=json.loads(p.read_text())['captures']
reports=[]
for r in rows:
 a=r['audit'];id=a['npcId'];name=a['actualFrame'];stem=R/'public/assets/npcs/phase3a'/id;meta=json.loads((stem/'atlas.json').read_text())['frames'][name]['frame'];src=Image.open(stem/'atlas.png').convert('RGBA').crop((meta['x'],meta['y'],meta['x']+96,meta['y']+112));p=a['sprite'];sx,sy=a['camera']['scroll'];x=round(p['x'])-48-sx;y=round(p['y'])-100-sy;assert a['camera']['zoom']==1 and float(x).is_integer()and float(y).is_integer()and p['sampling']==1;actual=Image.open(r.get('sourcePath',folder/r['file'])).convert('RGB').crop((x,y,x+96,y+112));b=np.array(src);diff=int(((b[:,:,3]==255)&np.any(np.array(actual)!=b[:,:,:3],2)).sum());assert diff==0,(id,name,diff);file=r['file'].replace('.png','-body-native.png');actual.save(folder/file);reports.append({'npcId':id,'frame':name,'opaquePixels':int((b[:,:,3]==255).sum()),'mismatch':diff,'crop':file,'native':[96,112],'scale':p['scale'],'integerPhase':True,'nearest':True})
(folder/'native-pixel-qa.json').write_text(json.dumps({'status':'PASS','captures':len(reports),'rows':reports,'mismatch':sum(r['mismatch']for r in reports),'humanArtApproval':'PENDING'},indent=2)+'\n');print('PASS',len(reports),'native actualNPC captures;0pixelmismatch')
