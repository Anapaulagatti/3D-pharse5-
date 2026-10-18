"""Presentation annotations around actual Phaser captures; never paints runtime game artwork."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib
Q=Path('docs/full-world/quality');O=Path('docs/full-world');font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def f(n):return ImageFont.truetype(font,n)
def text(im,xy,s,n=20,fill='#fff0ce'):ImageDraw.Draw(im).text(xy,s,font=f(n),fill=fill)
base=Image.open(Q/'full-map-overview.png').convert('RGB');thumb=base.resize((1088,1200),Image.Resampling.NEAREST)
zones=[('HERITAGE · Palace / Academy',(1024,0,3328,2240),'#ffd176'),('NAMSAN · Tower forest',(0,2240,1408,3520),'#a7db92'),('BORA BLOOM · Leisure',(3072,2240,4352,3392),'#ffb1d6'),('BLUE LETTER · Station / sea',(1536,2496,3072,3648),'#8cd8ee'),('WINDSTONE · Jeju garden',(1536,3648,2944,4800),'#ffbc88')]
routes=json.loads(Path('assets-src/full-world/routes.json').read_text())
for mode in ['labeled-world-plan','journey-overview']:
 im=Image.new('RGB',(1600,1300),'#152c2c');im.paste(thumb,(24,70));d=ImageDraw.Draw(im);text(im,(24,15),'LIVING KOREA — '+mode.upper().replace('-',' '),26)
 for i,(label,rect,col) in enumerate(zones):
  x,y,x2,y2=rect;d.rectangle((24+x/4,70+y/4,24+x2/4,70+y2/4),outline=col,width=3)
  text(im,(1140,100+i*130),str(i+1)+'  '+label,17,col)
  text(im,(1140,127+i*130),f'{x},{y} → {x2},{y2}',14)
 if mode=='journey-overview':
  for r in routes:
   d.line([(24+x/4,70+y/4)for x,y in r['points']],fill='#fff8a8',width=3)
  a=(24+2848/4,70+3184/4);b=(24+1760/4,70+4544/4);d.line([a,b],fill='#ff91b1',width=4)
  for p in [a,b]:d.ellipse((p[0]-6,p[1]-6,p[0]+6,p[1]+6),fill='#ff91b1')
  text(im,(1140,810),'Gold: walkable paths',18);text(im,(1140,842),'Pink: confirmed ferry',18)
 else:
  text(im,(1140,810),'Solid palace enclosure;',18);text(im,(1140,840),'streets stay outside it.',18)
 text(im,(1140,930),'4352 × 4800 native world',17);text(im,(1140,965),'Original artwork / Juni 80px',17);text(im,(1140,1030),'Fictional condensed journey;',16);text(im,(1140,1060),'not real Korean adjacency.',16)
 text(im,(24,1275),'Actual Phaser overview at 25% nearest-neighbor + planning annotations. Native original supplied separately.',15)
 im.save(O/(mode+'.png'))
# Native gameplay contact sheet, no scene resampling.
shots=['after-royal-garden-native','after-academy-native','after-workshop-native','after-museum-street-native','after-cultural-street-native','after-namsan-tower-native','after-bora-bloom-native','after-coast-station-native','after-jeju-garden-native']
im=Image.new('RGB',(3072,2448),'#152c2c')
for i,s in enumerate(shots):
 x=i%3*1024;y=i//3*816;text(im,(x+12,y+9),s.removeprefix('after-').removesuffix('-native').upper(),20);im.paste(Image.open(Q/(s+'.png')),(x,y+48))
im.save(O/'gameplay-scale-overview.png')
im=Image.new('RGB',(2048,2450),'#152c2c')
for i,s in enumerate(['royal-garden','academy','museum-street']):
 y=i*816
 for k,label in enumerate(['before','after']):text(im,(k*1024+12,y+9),label.upper()+' — '+s,20);im.paste(Image.open(Q/(label+'-'+s+'-native.png')),(k*1024,y+48))
im.save(O/'before-after.png')
# Compact review board: clearly scaled engine screenshots, enlarged pixel crops separate.
im=Image.new('RGB',(1688,1320),'#152c2c');text(im,(24,12),'LIVING KOREA — FULL WORLD + LANDSCAPE PLAY REVIEW',27)
im.paste(base.resize((544,600),Image.Resampling.NEAREST),(24,65))
for i,s in enumerate(['after-royal-garden-native','after-bora-bloom-native','after-coast-station-native','after-jeju-garden-native']):
 x=600+(i%2)*536;y=65+(i//2)*410;text(im,(x,y),s[6:-7].upper(),18);im.paste(Image.open(Q/(s+'.png')).resize((512,384),Image.Resampling.NEAREST),(x,y+25))
text(im,(24,700),'FIVE DESTINATIONS · ONE OUTDOOR WORLD',18);text(im,(24,736),'New source checkpoint; not a public release.',16)
im.paste(Image.open(Q/'mobile-landscape-interface.png'),(24,870));text(im,(900,905),'ACTUAL MOBILE HUD / 844 × 390',20);text(im,(900,950),'Analog stick + independent sprint',18);text(im,(900,985),'Explore / Talk / Emote',18);text(im,(900,1030),'Portrait pauses for rotation.',18);text(im,(900,1100),'Native captures and real input videos',18);text(im,(900,1135),'are provided separately.',18)
im.save(O/'review-board.png')
# Editable annotation model and SVG reference actual capture (relative link retained).
model={'world':[4352,4800],'capture':'quality/full-map-overview.png','districts':[{'label':l,'rect':r,'color':c}for l,r,c in zones],'routes':routes,'ferry':[[2848,3184],[1760,4544]],'fictionalGeography':True}
(O/'world-plan.json').write_text(json.dumps(model,indent=2)+'\n')
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="4352" height="4800" viewBox="0 0 4352 4800">','<image href="quality/full-map-overview.png" width="4352" height="4800"/>']
for l,(x,y,x2,y2),c in zones:svg +=[f'<rect x="{x}" y="{y}" width="{x2-x}" height="{y2-y}" fill="none" stroke="{c}" stroke-width="12"/>',f'<text x="{x+24}" y="{y+70}" fill="{c}" stroke="#142a25" stroke-width="2" font-size="48">{l}</text>']
for r in routes:svg.append('<polyline points="'+' '.join(f'{x},{y}'for x,y in r['points'])+'" fill="none" stroke="#fff8a8" stroke-width="10"/>')
svg.append('</svg>');(O/'world-plan.svg').write_text('\n'.join(svg))
print('Exported actual-capture boards, editable SVG/JSON; no runtime asset changes.')
