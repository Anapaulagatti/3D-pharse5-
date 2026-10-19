"""Review boards around actual engine pixels, never substitute concept artwork."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'docs/v6-restructure';Q=D/'quality';S=R/'assets-src/v6-restructure'
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def ft(n):return ImageFont.truetype(font,n)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
full=Image.open(Q/'after-full-map-native.png').convert('RGB');before=Image.open(Q/'before-full-map-native.png').convert('RGB');ref=Image.open(D/'reference-user.png').convert('RGB')
assert full.size==(4352,5312)and before.size==(4352,4800)
full.save(D/'V6_FULL_MAP_OVERVIEW.png');small=full.resize((1088,1328),Image.Resampling.NEAREST);small.save(D/'V6_FULL_MAP_OVERVIEW_SMALL.png')
def board(name,images,titles,width,footer):
 h=max(round(im.height*width/im.width)for im in images);out=Image.new('RGB',(len(images)*(width+24)+24,h+164),'#142d2a');d=ImageDraw.Draw(out)
 for i,(im,title)in enumerate(zip(images,titles)):
  x=24+i*(width+24);d.text((x,16),title,font=ft(24),fill='#fbeac8');im=im.resize((width,round(im.height*width/im.width)),Image.Resampling.NEAREST);out.paste(im,(x,56))
 for i,line in enumerate(footer):d.text((24,h+72+i*24),line,font=ft(17),fill='#e3e8d7')
 out.save(D/name)
board('V6_REFERENCE_COMPARISON.png',[ref,full],['USER ORIGINAL / Drive PNG','V6 / ACTUAL PHASER WORLD'],1161,['Same width, original aspect ratios retained; shorter panel is letterboxed, never stretched.', 'Original artwork reused as editable sprites / tiles; this is a layout reconstruction, not a historical reconstruction.'])
board('V6_BEFORE_AFTER.png',[before,full],['BEFORE / V4 ACTUAL PHASER','AFTER / V6 ACTUAL PHASER'],1088,['Tower (832,2912) -> (704,3008) | Station (1792,2752) -> (2240,2912)', 'Hub (2560,2688) -> (1776,3456) | Cafe (1568,3168) -> (2656,3456)', '122 original placements moved; original north and Juni retained. All image panels preserve their own aspect.'])
routes=json.loads((S/'routes.json').read_text());stops=json.loads((S/'stops.json').read_text());travel=json.loads((S/'travel.json').read_text())
nav=small.copy();d=ImageDraw.Draw(nav,'RGBA');colors=['#fff3a1','#68e2e0','#e9b8fe','#ffa97d']
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="4352" height="5312" viewBox="0 0 4352 5312"><image href="V6_FULL_MAP_OVERVIEW.png" width="4352" height="5312"/>']
for i,r in enumerate(routes):
 color=colors[i%len(colors)];pts=[(p[0]/4,p[1]/4)for p in r['points']];d.line(pts,fill=color,width=3,joint='curve');svg.append('<polyline fill="none" stroke="'+color+'" stroke-width="10" points="'+' '.join(f'{x},{y}'for x,y in r['points'])+'"/>')
for i,s in enumerate(stops):
 x,y=s['x']/4,s['y']/4;d.ellipse((x-4,y-4,x+4,y+4),fill='#fff9d9',outline='#142d2a',width=1)
 d.text((x+6,y-6),s['id'],font=ft(11),fill='#fff9d9',stroke_width=2,stroke_fill='#142d2a')
a,z=travel['mainlandTrigger'],travel['islandTrigger'];d.line([(a[0]/4,a[1]/4),(z[0]/4,z[1]/4)],fill='#fb95b0',width=5)
svg.append(f'<path d="M{a[0]},{a[1]} L{z[0]},{z[1]}" stroke="#fb95b0" stroke-width="16" stroke-dasharray="20 12"/>');svg.append('</svg>')
nav.save(D/'V6_NAVIGATION_MAP.png');(D/'V6_NAVIGATION_MAP.svg').write_text('\n'.join(svg))
(D/'V6_NAVIGATION_MAP.json').write_text(json.dumps({'world':[4352,5312],'basis':'actual Phaser native full frame','routes':routes,'entrances':stops,'ferry':travel},indent=2,ensure_ascii=False)+'\n')
# Native details remain native screenshots; enlarged samples use exact nearest-neighbour pixels.
for name in ['station','namsan','bloom-entry','jeju']:
 im=Image.open(Q/f'after-{name}-native.png');im.crop((256,128,768,640)).resize((1024,1024),Image.Resampling.NEAREST).save(Q/f'{name}-detail-2x.png')
(D/'reference-provenance.json').write_text(json.dumps({'userURL':'https://drive.google.com/file/d/19naWrMNv_BJtFAC-mb7oBjIy2wM5AHPC/view?usp=sharing','downloadedOriginalSha256':sha(D/'reference-original'),'originalSize':list(ref.size),'renderedFullSha256':sha(Q/'after-full-map-native.png'),'renderedFullSize':list(full.size),'comparison':'Full original reference versus full actual Phaser frame; matching panel width, aspect preserved; no reference baked into game.'},indent=2)+'\n')
print('Actual Phaser full-world/reference/before-after/navigation boards saved.')
