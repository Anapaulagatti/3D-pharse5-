from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,numpy as np
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a-final-six';inspector=json.loads((D/'clip-inspector-qa.json').read_text());readbacks=[]
for row in inspector['rows']:
 shot=Image.open(D/row['file']).convert('RGB');state=row['state']
 for i,s in enumerate(state['sprites']):
  atlas=Image.open(R/'public'/s['source']).convert('RGBA');metaPath=R/'public/assets/juni/juni.json'if i==0 else R/'public'/s['source'].replace('atlas.png','atlas.json');f=json.loads(metaPath.read_text())['frames'][s['frame']]['frame'];expected=np.array(atlas.crop((f['x'],f['y'],f['x']+96,f['y']+112)));actual=shot.crop((s['x']-48,s['y']-100,s['x']+48,s['y']+12));a=np.array(actual);diff=int(((expected[:,:,3]==255)&np.any(expected[:,:,:3]!=a,2)).sum());assert diff==0,(row['id'],row['direction'],i,diff);readbacks.append({'id':row['id'],'direction':row['direction'],'slot':i,'frame':s['frame'],'mismatch':diff})
(D/'inspector-native-qa.json').write_text(json.dumps({'status':'PASS native comparison rendering only','actualSpriteCrops':len(readbacks),'mismatch':0,'rows':readbacks,'source':'Actual Phaser5column inspector; canonical-world evidence is separate'},indent=2)+'\n')

board=Image.new('RGB',(720,6*180),(29,27,36))
ids=['history-seondeok','history-sejong','history-jang','history-saimdang','history-yi','history-yu']
for j,id in enumerate(ids):
 row=next(r for r in inspector['rows']if r['id']==id and r['direction']=='front');im=Image.open(D/row['file']).convert('RGB');board.paste(im,(0,j*180));ImageDraw.Draw(board).text((576,j*180+22),id,fill='#f4e7cc')
board.save(D/'six-actual-phaser-comparison-native.png');board.resize((1440,2160),Image.Resampling.NEAREST).save(D/'six-actual-phaser-comparison-2x.png')
old=json.loads((R/'assets-src/npcs/phase3a/registry.json').read_text())['npcs']+json.loads((R/'assets-src/npcs/phase3a-npc-expansion/modern-definitions.json').read_text())['npcs'];new=json.loads((R/'assets-src/npcs/phase3a-final-six/definitions.json').read_text())['npcs'];font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',11)
board=Image.new('RGBA',(1032,840),(29,27,36,255));draw=ImageDraw.Draw(board);draw.text((10,6),'SOURCE ART / native1:1 —20accepted baseline +6history ART CANDIDATES (facts/costumes UNVERIFIED)',font=font,fill='#f4e7cc')
for i,n in enumerate(old):
 x=(i%5)*172;y=35+(i//5)*150;draw.text((x+4,y+2),n['names']['vi'],font=font,fill='#f4e7cc');draw.text((x+4,y+17),n['names']['ko'],font=font,fill='#c9b8a2');q=Image.open(R/'public/assets/npcs/phase3a'/n['id']/'preview-native.png').convert('RGBA');board.alpha_composite(q,(x+38,y+34))
draw.text((10,640),'NEW SIX / speculative history art, source verification pending —not final26NPCacceptance',font=font,fill='#f4c273')
for i,n in enumerate(new):
 x=i*172;y=665;draw.text((x+4,y),n['names']['vi'],font=font,fill='#f4c273');draw.text((x+4,y+15),n['names']['ko'],font=font,fill='#d7b6a2');q=Image.open(R/'public/assets/npcs/phase3a'/n['id']/'preview-native.png').convert('RGBA');board.alpha_composite(q,(x+38,y+32))
board.convert('RGB').save(D/'roster26-art-candidates-native.png')
print('PASS',len(readbacks),'actual5column Phaser sprite readbacks; source26roster separately labelled')
