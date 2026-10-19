"""External review labels around real Phaser pixels. Never paints runtime art."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import shutil,json
O=Path('docs/modern-streets');Q=O/'quality';bg='#172c31';fg='#f6ecd1'
def text(im,xy,s,size=22):ImageDraw.Draw(im).text(xy,s,font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',size),fill=fg)
def shot(name):return Image.open(Q/(name+'.png')).convert('RGB')
full=shot('after-full-map-native');assert full.size==(4352,4800)
shutil.copyfile(Q/'after-full-map-native.png',O/'FINAL_FULL_MAP_OVERVIEW.png')
im=Image.new('RGB',(1136,1300),bg);text(im,(24,14),'KOREAN ARENA · MODERN STREET REVIEW',25);im.paste(full.resize((1088,1200),Image.Resampling.NEAREST),(24,60));text(im,(24,1270),'One actual Phaser frame · 25% nearest · final user approval pending',18);im.save(O/'FINAL_FULL_MAP_OVERVIEW_REVIEW.png')
im=Image.new('RGB',(2048,3312),bg);text(im,(16,10),'BEFORE / AFTER · IDENTICAL PHASER CAMERAS · NATIVE1×',26)
for i,(name,label)in enumerate([('transition','Connected threshold replaces the isolated dark surface patch'),('retail','Shared street, frontage sidewalk, actual zebra / tactile landing'),('station','Defined forecourt, one rail crossing and actual platform stair'),('bloom-spine','Cardinal park spine, ride plazas and orderly pedestrian branches')]):
 y=48+i*808;text(im,(16,y),label,22);im.paste(shot('before-'+name+'-native'),(0,y+36));im.paste(shot('after-'+name+'-native'),(1024,y+36))
text(im,(16,3280),'Approved buildings / placement / collision / Juni unchanged; comparisons show actual rendered pixels.',18);im.save(O/'MODERN_STREETS_BEFORE_AFTER.png')
im=Image.new('RGB',(2048,2508),bg);text(im,(16,10),'MODERN INFRASTRUCTURE · ACTUAL PHASER · NATIVE1×',26)
for i,(name,label)in enumerate([('transition','1 · HERITAGE TO CONTEMPORARY THRESHOLD'),('retail','2 · RETAIL FRONTAGE / VISIBLE CROSSING'),('station','3 · STATION FORECOURT / SAFE RAIL ACCESS'),('promenade','4 · CONTINUOUS PROMENADE / REAL BRIDGE'),('bloom-spine','5 · PARK SPINE / ATTRACTION PLAZAS'),('namsan','6 · OBSERVATION ARRIVAL / TRAILS RETAINED')]):
 x=i%2*1024;y=48+i//2*808;text(im,(x+12,y),label,20);im.paste(shot('after-'+name+'-native'),(x,y+36))
text(im,(16,2480),'Screenshots are1×; no generated concept plates. Full world and landscape playable build supplied separately.',17);im.save(O/'MODERN_INFRASTRUCTURE_BOARD.png')
model=json.loads(Path('assets-src/modern-streets/streets.json').read_text());(O/'ROAD_HIERARCHY.json').write_text(json.dumps(model,indent=2)+'\n')
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="4352" height="4800">','<image href="FINAL_FULL_MAP_OVERVIEW.png" width="4352" height="4800"/>']
for r in model['routes']:svg.append('<polyline points="'+' '.join(f'{x},{y}'for x,y in r['points'])+'" fill="none" stroke="#ffd977" stroke-width="6"/>')
svg.append('</svg>');(O/'ROAD_HIERARCHY.svg').write_text('\n'.join(svg))
print('Four required review PNGs plus editable street hierarchy from actual Phaser captures.')
