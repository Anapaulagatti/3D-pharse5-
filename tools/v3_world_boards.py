"""Review layout around actual Phaser captures. Never paints runtime game art."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil
O=Path('docs/v3-final');Q=O/'quality';font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';bg='#152c2c';fg='#fff0ce'
def text(im,xy,s,n=20,color=fg):ImageDraw.Draw(im).text(xy,s,font=ImageFont.truetype(font,n),fill=color)
def png(name):return Image.open(Q/(name+'.png')).convert('RGB')
world=png('full-map-overview');assert world.size==(4352,4800);shutil.copyfile(Q/'full-map-overview.png',O/'FINAL_FULL_WORLD_OVERVIEW.png');thumb=world.resize((1088,1200),Image.Resampling.NEAREST)
zones=[('ROYAL HERITAGE',2176,1104,'#ffd176'),('NAMSAN / OBSERVATION',832,2912,'#a7db92'),('BORA BLOOM / LEISURE',3712,2848,'#ffb1d6'),('BLUE LETTER / COAST',2304,3136,'#8cd8ee'),('WINDSTONE / JEJU',2240,4352,'#ffbc88')]
routes=json.loads(Path('assets-src/v3-final/routes.json').read_text())
for journey in [False,True]:
 im=Image.new('RGB',(1648,1320),bg);im.paste(thumb,(24,70));d=ImageDraw.Draw(im);text(im,(24,15),'KOREAN ARENA V3 — '+('EXPLORATION JOURNEY'if journey else'FINAL WORLD CANDIDATE'),26)
 if journey:
  for r in routes:d.line([(24+x/4,70+y/4)for x,y in r['points']],fill='#fff8a8',width=3)
  a=(24+2848/4,70+3184/4);b=(24+1760/4,70+4544/4)
  for i in range(0,20,2):
   p=[a[k]+(b[k]-a[k])*i/20 for k in [0,1]];q=[a[k]+(b[k]-a[k])*(i+1)/20 for k in [0,1]];d.line([tuple(p),tuple(q)],fill='#ff91b1',width=5)
 for i,(label,x,y,col)in enumerate(zones):
  px,py=24+x/4,70+y/4;d.ellipse((px-14,py-14,px+14,py+14),fill=bg,outline=col,width=3);text(im,(px-6,py-12),str(i+1),18,col)
  text(im,(1140,104+i*125),f'{i+1}. {label}',18,col)
  for j,line in enumerate([
   ['Palace · Academy · science','Original roofs and courtyards'],
   ['Glass lobby · steel tower','Forest approach · actual stairs'],
   ['Open ticket plaza · wheel','Carousel · creative discovery hall'],
   ['Station · train · crossing','Promenade · bridge · ferry'],
   ['Oreum · thatched court','Cliff · nature centre · basalt'],
  ][i]):text(im,(1140,135+i*125+j*26),line,16)
 for j,line in enumerate((['Gold: actual public routes','Pink dash: confirmed ferry','North → town → urban gateway','Mainland connected on foot','Jeju is a separate travel visit']if journey else['Actual Phaser Canvas render','4352 × 4800 native supplied','This view: 25%, nearest-neighbor','Juni: unchanged144frames','Final USER approval pending'])):text(im,(1140,800+j*36),line,17)
 text(im,(1140,1070),'Fictional Korean miniature;',16);text(im,(1140,1100),'not real geographic adjacency.',16)
 text(im,(24,1282),'Actual engine pixels + external review labels. No concepts or stitched world mockup. No public deployment.',16)
 im.save(O/('WORLD_JOURNEY_MAP.png'if journey else'FINAL_FULL_WORLD_OVERVIEW_REVIEW.png'))
# Native-size paired environments, with no screenshot resampling.
im=Image.new('RGB',(2048,2448),bg)
for i,(left,right,title)in enumerate([('after-royal-garden-native','after-namsan-hero-native','Royal timber / giwa  |  Steel / glass observation tower'),('after-academy-native','after-coast-station-native','Scholarly courtyard  |  Contemporary rail infrastructure'),('after-workshop-native','after-bora-bloom-native','Invention workshop  |  Coordinated modern amusement plaza')]):
 y=i*816;text(im,(16,y+10),title,22);im.paste(png(left),(0,y+48));im.paste(png(right),(1024,y+48))
im.save(O/'TRADITIONAL_VS_MODERN.png')
im=Image.new('RGB',(2048,2492),bg)
for i,(name,caption)in enumerate([('cultural-street','Bookshop separated from museum; dedicated west frontage'),('coast-station','Modern station / horizontal carriage / real platform stair'),('forest','Organic material masks and curated inaccessible woodland edge')]):
 y=i*816;text(im,(14,y+10),'BEFORE  |  AFTER — '+caption,20)
 if name!='forest':a=png('before-'+name+'-native');b=png('after-'+name+'-native')
 else:
  a=Image.open('docs/full-world/quality/full-map-overview.png').convert('RGB').crop((384,1536,1408,2304));b=world.crop((384,1536,1408,2304))
 im.paste(a,(0,y+48));im.paste(b,(1024,y+48))
text(im,(14,2460),'Latest annotated image was not supplied. These are the actual observed/repaired defects, not claimed annotation matches.',17);im.save(O/'BEFORE_AFTER_MAP_FIXES.png')
im=Image.new('RGB',(2816,1056),bg);text(im,(16,12),'WINDSTONE JEJU — BEFORE / AFTER AT IDENTICAL NATIVE COORDINATES',26)
before=Image.open('docs/full-world/quality/full-map-overview.png').convert('RGB').crop((1536,3840,2944,4800));after=world.crop((1536,3840,2944,4800));im.paste(before,(0,64));im.paste(after,(1408,64));text(im,(16,1025),'Actual Phaser pixels, 1×. New oreum, cultural court, cliff, nature centre, basalt discovery and reciprocal ferry loop.',18);im.save(O/'JEJU_BEFORE_AFTER.png')
im=Image.new('RGB',(2048,2448),bg)
for i,(name,label)in enumerate([('after-royal-garden-native','1 ROYAL HERITAGE'),('after-namsan-hero-native','2 NAMSAN'),('after-bora-bloom-native','3 BORA BLOOM'),('after-coast-bridge-native','4 BLUE LETTER COAST'),('after-jeju-garden-native','5 WINDSTONE JEJU')]):
 x=i%2*1024;y=i//2*816;text(im,(x+16,y+10),label+' · NATIVE1×',22);im.paste(png(name),(x,y+48))
x,y=1024,1632;text(im,(x+16,y+10),'LANDSCAPE PLAY / 844 × 390',22);im.paste(png('mobile-landscape-interface'),(x+16,y+80));text(im,(x+16,y+530),'Analog stick · independent sprint · Explore / Talk / Emote',21);text(im,(x+16,y+575),'OS reduced motion · portrait pause · previous worlds retained',21);text(im,(x+16,y+640),'Native-scale character:80px body /96×112canvas',21);text(im,(x+16,y+690),'Emulated Chromium; physical phones unmeasured.',21);im.save(O/'DISTRICT_IDENTITY_BOARD.png')
# Editable review overlay links actual engine capture, never replaces layered Tiled art.
model={'world':[4352,4800],'capture':'FINAL_FULL_WORLD_OVERVIEW.png','routes':routes,'landmarks':[{'name':n,'point':[x,y],'color':c}for n,x,y,c in zones],'ferry':[[2848,3184],[1760,4544]],'fictionalGeography':True};(O/'WORLD_JOURNEY_MAP.json').write_text(json.dumps(model,indent=2)+'\n')
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="4352" height="4800">','<image href="FINAL_FULL_WORLD_OVERVIEW.png" width="4352" height="4800"/>']
for r in routes:svg.append('<polyline points="'+' '.join(f'{x},{y}'for x,y in r['points'])+'" fill="none" stroke="#fff8a8" stroke-width="8"/>')
svg.append('<path d="M2848 3184L1760 4544" fill="none" stroke="#ff91b1" stroke-width="12" stroke-dasharray="32 24"/>');svg.append('</svg>');(O/'WORLD_JOURNEY_MAP.svg').write_text('\n'.join(svg))
# Enlarged detail is explicitly2× nearest, not native gameplay size.
im=Image.new('RGB',(1536,900),bg);text(im,(16,12),'ACTUAL PHASER PIXEL DETAILS · 2× NEAREST-NEIGHBOR',26)
for i,(s,box,label)in enumerate([('after-jeju-court-native',(360,260,616,580),'Juni visible in courtyard'),('after-namsan-tower-native',(380,280,636,600),'Contemporary lobby / Juni'),('after-coast-bridge-native',(380,280,636,600),'Bridge / same80pxJuni')]):
 x=i*512;im.paste(png(s).crop(box).resize((512,640),Image.Resampling.NEAREST),(x,70));text(im,(x+10,740),label,20)
im.save(O/'PIXEL_DETAIL_AND_SCALE.png');print('Saved actual-engine native boards, review overview and editable journey overlays.')
