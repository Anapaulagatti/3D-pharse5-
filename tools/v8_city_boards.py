"""Review boards from actual Phaser PNGs. Native crops, nearest-only overview reductions."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,shutil
R=Path(__file__).resolve().parents[1];Q=R/'docs/v8-city';D=Q/'quality/final-native';im=Image.open(D/'full-native.png').convert('RGB');old=Image.open(R/'docs/v7-world/FINAL_WORLD_OVERVIEW_NATIVE.png').convert('RGB');assert im.size==old.size==(4352,5312)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',20);small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
im.save(Q/'FINAL_WORLD_OVERVIEW_NATIVE.png');im.resize((2176,2656),Image.Resampling.NEAREST).save(Q/'FINAL_WORLD_OVERVIEW_WEB.png');im.resize((1088,1328),Image.Resampling.NEAREST).save(Q/'overview-small.png')
board=Image.new('RGB',(2176,1390),'#132c38');board.paste(old.resize((1088,1328),Image.Resampling.NEAREST),(0,62));board.paste(im.resize((1088,1328),Image.Resampling.NEAREST),(1088,62));d=ImageDraw.Draw(board);d.text((18,12),'BEFORE • V7 / ea8588f • actual Phaser',font=font,fill='white');d.text((1106,12),'AFTER • V8 candidate • actual Phaser',font=font,fill='white');d.text((18,39),'Matched full-world framing; 4:1 nearest reduction. Native images retained.',font=small,fill='#b8d9df');board.save(Q/'BEFORE_AFTER_WORLD.png')
regions={'NAMSAN_DESIGN_REVIEW':(128,2400,1328,3600),'STATION_URBAN_DESIGN_REVIEW':(1392,2336,3264,3504),'AMUSEMENT_CAMPUS_REVIEW':(3264,2400,4320,3592),'WATERFRONT_AND_FERRY_REVIEW':(1984,3456,3072,4000),'JEJU_SCENIC_PATH_REVIEW':(1504,4160,3200,5200)}
for name,box in regions.items():
 a=im.crop(box);out=Image.new('RGB',(a.width,a.height+70),'#132c38');out.paste(a,(0,70));d=ImageDraw.Draw(out);d.text((16,10),name.replace('_',' '),font=font,fill='white');d.text((16,42),f'Actual Phaser native 1:1 crop {box} • no image filters or resampling',font=small,fill='#b8d9df');out.save(Q/(name+'.png'))
 # Exact same coordinates and scale, no framing tricks around relocated landmarks.
 a=old.crop(box);c=im.crop(box);cmp=Image.new('RGB',(a.width*2,a.height+54),'#132c38');cmp.paste(a,(0,54));cmp.paste(c,(a.width,54));d=ImageDraw.Draw(cmp);d.text((14,14),'V7 before — matched native crop',font=font,fill='white');d.text((a.width+14,14),'V8 candidate — matched native crop',font=font,fill='white');cmp.save(Q/'quality'/f'{name}-BEFORE_AFTER_NATIVE.png')
nav=im.resize((1088,1328),Image.Resampling.NEAREST);d=ImageDraw.Draw(nav);p=json.loads((R/'assets-src/v8-city/city-masterplan.json').read_text())
for q in p['districts']:
 b=[round(x/4)for x in q['bounds']];d.rectangle(b,outline='#ffffff',width=2);d.text((b[0]+4,b[1]+4),q['id'],font=small,fill='#fff4ae',stroke_width=1,stroke_fill='#17303d')
for r in p['roads']:
 d.line([(x/4,y/4)for x,y in r['controlPoints']],fill='#5cf0ed'if r['material']not in ['earth','sand','basalt']else'#fff196',width=2)
for q in p['plots']:
 d.rectangle([round(v/4)for v in q['bounds']],outline='#ffbe79',width=1);x,y=q['entrance'];d.ellipse((x/4-3,y/4-3,x/4+3,y/4+3),fill='#ffbe79')
nav.save(Q/'NAVIGATION_AND_DISTRICT_BOUNDARIES.png')
# 2x integer detail is explicitly labelled, separate from all native-scale evidence.
a=Image.open(D/'urban-junction-native.png');a.resize((a.width*2,a.height*2),Image.Resampling.NEAREST).save(Q/'quality/urban-junction-detail-2x.png')
shutil.copyfile(D/'ground-only-native.png',Q/'STREET_NETWORK_BUILDINGS_HIDDEN.png')
(Q/'quality/board-sources.json').write_text(json.dumps({'source':str((D/'full-native.png').relative_to(R)),'before':'docs/v7-world/FINAL_WORLD_OVERVIEW_NATIVE.png','full':[4352,5312],'web':[2176,2656],'nativeRegionBoxes':regions,'allBoards':'literal actual Phaser pixels; only labeled overview/detail integer nearest scaling, annotations outside native crops; not source composition/AI illustration'},indent=2)+'\n')
print('Actual-engine review boards complete')
