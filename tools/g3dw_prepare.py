"""Freeze native registration guides for consolidated world recovery; no source art overwrite."""
from pathlib import Path
from PIL import Image,ImageDraw
import json
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate3/recovery-world-v1';m=json.loads((R/'public/assets/gate3/recovery-pilots/manifest.json').read_text());p=json.loads((R/'assets-src/gate3/production-plan-v3.1-restored.json').read_text())['plan'];W,H=m['size'];ground=Image.new('RGBA',(W,H))
for c in m['chunks']:ground.paste(Image.open(R/'public'/c['image']),(c['x'],c['y']))
# Ground-only guides: no new architecture is baked into a material panel. Canonical A/C/floor remain visible as locked context.
guide=ground.copy();d=ImageDraw.Draw(guide)
for b in p['buildings']:
 x,y,w,h=b['rect'];d.rectangle((x,y,x+w-1,y+h-1),outline='#f18da0',width=2);d.text((x+5,y+5),'RESERVED '+b['id'],fill='#fff1d0')
for q in p['paths']:
 d.line([tuple(z)for z in q['points']],fill='#65d6db',width=2,joint='curve')
# Non-overlapping final ownership cores will be chosen after neighboring source overlaps are authored.
regions={'northwest':[160,80,1536,1024],'palacecourt':[1280,80,1536,1024],'northeast':[1664,576,1536,1024],'academywest':[160,896,1536,1024],'thresholdwest':[160,1536,1536,1024],'thresholdeast':[1664,1536,1536,1024],'urbanwest':[160,2304,1536,1024],'urbanse':[1664,2304,1536,1024],'harborwest':[160,2976,1536,1024],'harboreast':[1664,2976,1536,1024],'rail':[2816,1792,1536,1024],'jejunorth':[2816,3072,1536,1024],'jejusouth':[2816,3840,1536,1024]}
for name,(x,y,w,h)in regions.items():guide.crop((x,y,x+w,y+h)).save(S/(name+'-guide.png'),optimize=True);ground.crop((x,y,x+w,y+h)).save(S/(name+'-before-ground.png'),optimize=True)
(S/'panel-registry.json').write_text(json.dumps({'worldSize':[W,H],'regions':regions,'guides':'Native layout only; cyan centerlines/pink reserved footprints are technical guides, not source style. Remove guide marks in authored ground. No new buildings/tall trees.','protectedGround':[{'source':'public/assets/gate2/a/ground.png','rect':[640,650,1536,1024]},{'source':'public/assets/gate2/c/ground.png','rect':[3180,3200,1024,1536]},{'source':'assets-src/gate3/forecourt-restoration/restored-ground.png','rect':[2274,2603,684,210]}]},indent=2)+'\n')
# Native tree bank:24 independent256x256 cells constrain ordinary trees to honest player scale.
t=Image.new('RGBA',(1536,1024),(30,52,50,255));td=ImageDraw.Draw(t);tree=Image.open(R/'public/assets/gate2/b/prop-heritage-tree.png').convert('RGBA')
for row in range(4):
 for col in range(6):
  x,y=col*256,row*256;td.rectangle((x+12,y+10,x+243,y+245),outline='#89b8a0',width=1);t.alpha_composite(tree,(x+33,y+40))
t.save(S/'tree-native-guide.png',optimize=True)
# Tower options, empty target slots at actual native dimensions; native Juni is a reference marker only.
atlas=json.loads((R/'public/assets/juni/juni.json').read_text());f=atlas['frames']['idle-front-0']['frame'];j=Image.open(R/'public/assets/juni/juni.png').convert('RGBA').crop((f['x'],f['y'],f['x']+f['w'],f['y']+f['h']))
t=Image.new('RGBA',(1536,1024),'#203735');td=ImageDraw.Draw(t)
for box,label in [((170,370,530,840),'A COMPLETE470px profile / base240 / door105'),((680,170,1080,840),'B COMPLETE670px profile / base240 / door105')]:td.rectangle(box,outline='#9bd0b5',width=2);td.text((box[0],box[3]+18),label,fill='white')
for x in [302,844]:td.rectangle((x,675,x+76,780),outline='#f5dc8a',width=2)
t.alpha_composite(j,(1180,728));td.text((1150,880),'ORIGINAL JUNI96x112',fill='white');td.text((1150,910),'Ignore avatar in exported assets',fill='white');t.save(S/'tower-options-guide.png',optimize=True)
# Roof-only reference slot; no full hall/base is requested from the generator.
t=Image.new('RGBA',(1536,1024),'#203735');td=ImageDraw.Draw(t);td.rectangle((170,270,1360,620),outline='#9bd0b5',width=2);td.text((180,650),'ROOF ONLY / full giwa roof+dancheong eave / no facade, floor or plinth',fill='white');td.text((180,680),'Target about1190x350 native; detailed original Korean source is authority',fill='white');t.save(S/'palace-roof-guide.png',optimize=True)
print('Prepared',len(regions),'native ground guides and three bounded native sprite guides')
