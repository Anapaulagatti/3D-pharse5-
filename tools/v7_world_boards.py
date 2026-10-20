"""Literal real-Phaser native crops, separately labelled reference and nav overlay."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,shutil
R=Path(__file__).resolve().parents[1];D=R/'docs/v7-world';Q=D/'quality/final-render';S=R/'assets-src/v7-world'
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',22)
before=Image.open(R/'docs/final-map-lock/FINAL_LOCK_OVERVIEW.png').convert('RGB');after=Image.open(Q/'full-native.png').convert('RGB');assert before.size==after.size==(4352,5312)
shutil.copyfile(Q/'full-native.png',D/'FINAL_WORLD_OVERVIEW_NATIVE.png');after.resize((2176,2656),Image.Resampling.NEAREST).save(D/'FINAL_WORLD_OVERVIEW_WEB.png');after.resize((1088,1328),Image.Resampling.NEAREST).save(D/'FINAL_WORLD_OVERVIEW_SMALL.png')
rows=[('NAMSAN',(128,2400,1408,3680)),('BUSAN_STATION',(1424,2384,3136,3744)),('AMUSEMENT_PARK',(3104,2400,4352,3744)),('TRANSITION_ROADS',(1856,1856,2800,2528)),('WATERFRONT_FERRY',(1792,3488,3152,4416)),('JEJU',(1408,4096,3296,5248))]
for name,box in rows:
 a,b=before.crop(box),after.crop(box);w,h=a.size;out=Image.new('RGB',(w*2+24,h+72),'#162323');out.paste(a,(0,72));out.paste(b,(w+24,72));draw=ImageDraw.Draw(out);draw.text((16,15),'BEFORE — V6 / real Phaser / native 1:1',font=font,fill='white');draw.text((w+40,15),'AFTER — V7 / same world crop, camera0,0 / zoom1',font=font,fill='white');out.save(D/f'{name}_BEFORE_AFTER.png');b.save(Q/f'{name.lower()}-1x-crop.png')
ref=Image.open(R/'docs/v6-restructure/reference-user.png').convert('RGB');small=after.resize((1088,1328),Image.Resampling.NEAREST);board=Image.new('RGB',(ref.width+small.width+40,max(ref.height,small.height)+80),'#162323');board.paste(ref,(0,80));board.paste(small,(ref.width+40,80));draw=ImageDraw.Draw(board);draw.text((14,18),'REFERENCE ART — visual target, not runtime',font=font,fill='white');draw.text((ref.width+54,18),'V7 — ACTUAL PHASER (integer 1:4 overview)',font=font,fill='white');board.save(D/'REFERENCE_VS_FINAL.png')
nav=after.copy();d=ImageDraw.Draw(nav);routes=json.load(open(S/'routes.json'));stops=json.load(open(S/'stops.json'));travel=json.load(open(S/'travel.json'))
for r in routes:d.line([tuple(p)for p in r['points']],fill='#f5e950',width=7)
for st in stops:
 x,y=st['x'],st['y'];d.ellipse((x-12,y-12,x+12,y+12),fill='#ff5b85',outline='white',width=3);d.text((x+20,y+5),st['id'],font=font,fill='white',stroke_width=3,stroke_fill='#182424')
a=travel['mainlandTrigger'];b=travel['islandTrigger'];d.line([tuple(a),tuple(b)],fill='#ff8edb',width=9);d.text((2384,4056),'FERRY — public interaction, not walkable sea',font=font,fill='white',stroke_width=3,stroke_fill='#182424');nav.save(D/'WORLD_NAVIGATION.png')
(D/'WORLD_NAVIGATION.json').write_text(json.dumps({'basis':'real Phaser native overview, analytical overlay only','routes':routes,'entrances':stops,'travel':travel,'bridge':'coastal-channel-bridge is physically traversable; ferry remains mainland-island transport'},indent=2)+'\n')
(D/'comparison-method.json').write_text(json.dumps({'before':'docs/final-map-lock/FINAL_LOCK_OVERVIEW.png','after':'quality/final-render/full-native.png','viewport':[4352,5312],'camera':[0,0],'zoom':1,'renderer':'Phaser Canvas','DPR':1,'reducedMotion':True,'nativeCropBoxes':dict(rows),'filters':'none','webResampling':'integer 2:1 nearest; small/reference board integer4:1 nearest','reference':'docs/v6-restructure/reference-user.png, never used as terrain or traced'},indent=2)+'\n')
print('V7 required boards and literal gameplay crops written')
