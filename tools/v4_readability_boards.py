"""External labels around actual native Phaser captures; no repainting runtime pixels."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import shutil,json
O=Path('docs/v4-readability');Q=O/'quality';bg='#172c31';fg='#f6ecd1'
def text(im,xy,s,size=22):ImageDraw.Draw(im).text(xy,s,font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',size),fill=fg)
def shot(name):return Image.open(Q/(name+'.png')).convert('RGB')
full=shot('after-full-map-native');assert full.size==(4352,4800);shutil.copyfile(Q/'after-full-map-native.png',O/'FINAL_MAP_V4_FULL_OVERVIEW.png')
im=Image.new('RGB',(1136,1300),bg);text(im,(24,14),'KOREAN ARENA · V4 OPEN COMPOUNDS',25);im.paste(full.resize((1088,1200),Image.Resampling.NEAREST),(24,60));text(im,(24,1270),'One actual Phaser frame · 25% nearest · user visual approval pending',17);im.save(O/'FINAL_MAP_V4_REVIEW_OVERVIEW.png')
panels=[('transition','1 · Central threshold · y2240–2480: connected, softened existing elbow'),('namsan','2 · Namsan · rounded arrival apron / planted stone edge / organic trail'),('promenade','3 · Station / bridge · continuous pedestrian material and open rail edges'),('bloom-spine','4 · Bora Bloom · shared spine, distinct ride pockets and soft boundary'),('retail','5 · Commercial frontage · entry court separated from through movement')]
im=Image.new('RGB',(2048,4128),bg);text(im,(16,10),'BEFORE (LEFT) / V4 (RIGHT) · IDENTICAL PHASER CAMERAS · NATIVE1×',24)
for i,(name,label)in enumerate(panels):
 y=48+i*808;text(im,(16,y),label,21);im.paste(shot('before-'+name+'-native'),(0,y+36));im.paste(shot('after-'+name+'-native'),(1024,y+36))
text(im,(16,4100),'Actual coordinate repairs shown; user circle annotation absent. Original landmarks / Juni / north / Jeju retained.',17);im.save(O/'READABILITY_BEFORE_AFTER.png')
im=Image.new('RGB',(2048,1696),bg);text(im,(16,10),'SOUTHERN DESTINATIONS · ACTUAL PHASER · NATIVE1×',26)
for i,(name,label)in enumerate([('namsan','A · NAMSAN / OPEN LANDSCAPE EDGE'),('station','B · STATION / PLATFORM / PROMENADE'),('bloom-spine','C · BORA BLOOM / PARK LOOP & LIGHT EDGES'),('retail','D · COMMERCIAL / FACADE-FACING APRON')]):
 x=i%2*1024;y=48+i//2*808;text(im,(x+12,y),label,21);im.paste(shot('after-'+name+'-native'),(x,y+36))
text(im,(16,1670),'No concepts substituted.32physical boundary feet retain45clear routes. All original406placements /621solids unchanged.',17);im.save(O/'SOUTHERN_DISTRICT_READABILITY_BOARD.png')
S=Path('assets-src/v4-readability');m={'world':[4352,4800],'boundaryLanguage':json.loads((S/'boundaries.json').read_text()),'pathFixes':json.loads((S/'path-fixes.json').read_text()),'routes':json.loads((S/'routes.json').read_text()),'entrances':{'namsan':[[704,2992],[1120,3144]],'station':[[1792,2816],[2048,2944],[2048,3040]],'commercial':[[2464,2752],[2560,2752]],'amusement':[[3712,3296],[3232,3296],[3456,2848]]}};(O/'COMPOUNDS.json').write_text(json.dumps(m,indent=2)+'\n')
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="4352" height="4800">','<image href="FINAL_MAP_V4_FULL_OVERVIEW.png" width="4352" height="4800"/>']
for p in m['boundaryLanguage']['placements']:
 c=p['collider'];svg.append(f'<rect x="{c["x"]}" y="{c["y"]}" width="{c["w"]}" height="{c["h"]}" fill="#ffcc77" stroke="#ffcc77" stroke-width="4"/>')
for pts in m['entrances'].values():
 for x,y in pts:svg.append(f'<circle cx="{x}" cy="{y}" r="24" fill="none" stroke="#80ffdf" stroke-width="8"/>')
svg.append('</svg>');(O/'COMPOUNDS.svg').write_text('\n'.join(svg));print('Required V4 full frame, native before/after, four-destination board, small review image and editable boundary/entrance overlay exported.')
