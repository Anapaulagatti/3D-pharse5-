"""Label original generated/Forge-finished art; no new game pixels painted."""
from production_art import R,S,write
from PIL import Image,ImageDraw,ImageFont
import json
Q=R/'docs/seoul-production';Q.mkdir(exist_ok=True)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def f(n):return ImageFont.truetype(font,n)
def board(size,title,sub):
 im=Image.new('RGB',size,'#f0e8d2');d=ImageDraw.Draw(im);d.text((36,24),title,font=f(30),fill='#23483d');d.text((36,68),sub,font=f(17),fill='#4f5d50');return im,d
studies=json.loads((S/'studies/manifest.json').read_text())['studies']
labels=['G01 Ceremonial gateway','A01 Scholar U-campus','H01 Invention L-workshop','H02 History + west vestibule','C01 Botanical painting studio','P02 Open garden pavilion','M01 Bookshop with reading niche','M02 Hanji / stationery counter','M03 Tea veranda + kitchen','M04 Open craft workbay','R01 U courtyard home','R02 L garden household','R03 Detached two-pavilion home','R04 Well / service courtyard home']
# Preserve declared order of institutional/civil files, not alphabetical.
order=['gate','academy','workshop','museum','art','pavilion','bookshop','stationery','teahouse','craft','home-u','home-l','home-two','home-well']
by={p['id']:p for p in studies};im,d=board((1720,2040),'LIVING SEOUL / ARCHITECTURE ART BIBLE','Stage A studies / approximate 0.5 world-relative scale / original generated art / NOT completed runtime buildings')
for i,(name,label) in enumerate(zip(order,labels)):
 x=36+(i%3)*560;y=120+(i//3)*380;p=by[name+'-study'];art=Image.open(S/p['image']).convert('RGBA');d.rounded_rectangle((x,y,x+540,y+360),12,fill='#dedbc7');im.paste(art,(x+(540-art.width)//2,y+35),art);d.text((x+16,y+300),label,font=f(17),fill='#23483d');d.text((x+16,y+326),'First Stage B' if name in ['gate','academy','workshop','museum'] else 'Future Stage C / CONCEPT ONLY',font=f(14),fill='#765b39')
im.save(Q/'architecture-art-bible.png')
# Exact native actor from unchanged approved atlas.
atlas=json.loads((R/'public/review/juni-animation/juni.json').read_text());r=atlas['frames']['idle-front-0']['frame'];actor=Image.open(R/'public/review/juni-animation/juni.png').crop((r['x'],r['y'],r['x']+r['w'],r['y']+r['h']))
im,d=board((2048,1420),'FIRST STAGE B / LANDMARK IDENTITIES AT 1x NATIVE','Same Juni80px in every panel / no stretching / original pixel-finished architecture / user visual approval pending')
props={p['id']:Image.open(S/p['image']).convert('RGBA')for p in json.loads((S/'props.json').read_text())}
for i,(title,ids) in enumerate([('G01 / Palace gateway',[('prod-gate',0,0)]),('A01 / Three-block reading courtyard',[('prod-hall',0,0),('prod-study',-288,109),('prod-library',288,78)]),('H01 / Technical asymmetric court',[('prod-workshop',0,0)]),('H02 / Naval history + west vestibule',[('prod-museum',0,0)])]):
 x=32+(i%2)*1008;y=116+(i//2)*636;d.rounded_rectangle((x,y,x+984,y+612),12,fill='#dedbc7');d.text((x+20,y+18),title,font=f(23),fill='#23483d')
 if i==1:
  for key,dx,dy in ids:
   p=props[key];im.paste(p,(x+492+dx-p.width//2,y+55+dy),p)
 else:
  p=props[ids[0][0]];im.paste(p,(x+(984-p.width)//2,y+573-p.height),p)
 im.paste(actor,(x+470,y+480),actor);d.text((x+20,y+574),'Juni / native80px body',font=f(17),fill='#4f5d50')
im.save(Q/'building-identity-board.png')
write(Q/'board-source.json',{'bibleManifest':'../../assets-src/seoul-production/studies/manifest.json','productionManifest':'../../assets-src/seoul-production/props.json','actor':'../../public/review/juni-animation/juni.png','generator':'../../tools/production_boards.py','nativeBoardScale':1,'conceptBoardWorldRelativeScale':.5,'note':'Art Bible future families are original studies only; Stage B native board is asset composition, not a Phaser screenshot.'})
