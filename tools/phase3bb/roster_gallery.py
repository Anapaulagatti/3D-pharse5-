from pathlib import Path
import json
from PIL import Image,ImageDraw
R=Path.cwd();rows=[]
for n in ['phase3a/registry.json','phase3a-npc-expansion/modern-definitions.json','phase3a-final-six/definitions.json']:rows+=json.loads((R/'assets-src/npcs'/n).read_text())['npcs']
ident={r['npcId']:r for r in json.loads((R/'assets-src/npcs/phase3a-finalization/identity-presentations.json').read_text())['identities']};board=Image.new('RGBA',(6*180,5*150),(24,36,43));dr=ImageDraw.Draw(board);data=[]
for i,n in enumerate(rows):
 tex=Image.open(R/'public'/n['assets']['texture']).convert('RGBA');meta=json.loads((R/'public'/n['assets']['atlas']).read_text());f=meta['frames']['idle-front-0']['frame'];crop=tex.crop((f['x'],f['y'],f['x']+96,f['y']+112));name=ident[n['id']]['publicName']if n['id']in ident else n['names'];x=i%6*180;y=i//6*150;board.alpha_composite(crop,(x+42,y));dr.text((x+5,y+115),name['vi'],fill=(255,221,159));dr.text((x+5,y+131),'fictional era'if n['id']in ident else'resident / visitor',fill=(180,204,198));data.append({'id':n['id'],'name':name,'eraFictional':n['id']in ident,'atlas':n['assets']['texture'],'frames':len(meta['frames'])})
board.save(R/'docs/phase3bb-hotfix/ROSTER26-native.png');(R/'docs/phase3bb-hotfix/ROSTER26.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');assert len(rows)==26 and len({r['id']for r in rows})==26
print('26 unique identities; native originals unaltered')
