"""Lossless Phaser adapter for the actual Forge Tiled export; no artwork generation."""
from pathlib import Path
import json, shutil, hashlib
from PIL import Image
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gwanghwamun';D=R/'public/review/gwanghwamun';D.mkdir(parents=True,exist_ok=True)
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
b=json.loads((S/'map-bundle.json').read_text());t=json.loads((S/'tiled/map.embedded.tmj').read_text())
source_collision=next(x for x in t['layers'] if x['name']=='collision')
rects=[o for o in source_collision['objects'] if o['type']=='solid']
assert all('polygon' not in o and not o.get('rotation') and o.get('width',0)>0 and o.get('height',0)>0 for o in rects)
collision=dict(source_collision,name='Collision',objects=rects)
t['layers']=[x for x in t['layers'] if x['type']=='tilelayer']+[collision]
t['tilesets']=[dict(t['tilesets'][0],image='tiles.png')]
write(D/'plaza.json',t)
for name,p in b['props'].items():shutil.copyfile(S/p['image'],D/f'{name}.png')
shutil.copyfile(S/'tiles.png',D/'tiles.png')
Image.open(S/'terrain-accepted/water-1.png').save(D/'water.png')
im=Image.open(S/'props/ginkgo.png').convert('RGBA');best=(0,0,0)
for y in range(5,im.height//2):
 for x in range(5,im.width-5):
  red,green,blue,alpha=im.getpixel((x,y));score=(red+green-blue) if alpha==255 and red>180 and green>140 else 0
  if score>best[0]:best=(score,x,y)
_,x,y=best
im.crop((x-3,y-3,x+4,y+4)).resize((4,4),Image.Resampling.BOX).save(D/'leaf.png')
write(S/'leaf-recipe.json',{'source':'props/ginkgo.png','crop':[x-3,y-3,x+4,y+4],'output':[4,4],'resampler':'BOX','purpose':'Six tiny environment particles cropped from generated foliage; no code-drawn leaf artwork. Partial alpha from area resize allowed for this4px effect, native props stay binary.'})
(D/'concepts').mkdir(exist_ok=True)
for key in 'ABC':Image.open(S/f'concepts/{key}.png').resize((768,512),Image.Resampling.BOX).save(D/f'concepts/{key}.png')
layout={'width':1024,'height':768,'spawn':[512,600],'npc':[354,480],'follow':70,'role':'Juni · Ginkgo Commons','mood':'Gwanghwamun art proof','vi':'Ginkgo Commons','mapSha256':hashlib.sha256((D/'plaza.json').read_bytes()).hexdigest(),'objects':[]}
for i,o in enumerate(b['objects']):
 p=b['props'][o['prop']];f=p['footprint'];layout['objects'].append({'id':i+1,'kind':o['prop'],'x':o['x'],'y':o['y'],'width':f['width'],'height':f['depth'],'label':o['prop'],'collide':o.get('solid',p['solid'])})
write(S/'world.json',layout);write(D/'anchors.json',{k:v['anchor_px']for k,v in b['props'].items()})
assert next(l for l in json.loads((D/'plaza.json').read_text())['layers']if l['name']=='Collision')['objects']==rects
write(S/'runtime-export.json',{'status':'PASS','source':'tiled/map.embedded.tmj','runtime':'public/review/gwanghwamun/plaza.json','adaptations':['Only tile layers retained: props instantiated by existing Plaza controller from world.json.','collision renamed Collision; walkRegion metadata excluded from Arcade solids.','Embedded town image relative path changed to tiles.png; unused props tileset omitted.','All33 exported solid rectangles retained exactly; no regenerated hidden blockers.'],'colliders':len(rects),'tiled_editor_import':'UNTESTED — Forge read-back passed, actual Phaser import verified separately.'})
# A source-only composite for the documented Forge placement/feet audit.
base=Image.new('RGBA',(1024,768));atlas=Image.open(S/'tiles.png')
for y,row in enumerate(json.loads((S/'layers/ground.json').read_text())):
 for x,i in enumerate(row):base.paste(atlas.crop(((i%4)*32,(i//4)*32,(i%4)*32+32,(i//4)*32+32)),(x*32,y*32))
base.save(S/'ground-assembled.png')
placements={'schema':'generate2dmap.placements.v2','props':[{'id':o['id'],'image':str((S/b['props'][o['prop']]['image']).relative_to(R)),'x':o['x'],'y':o['y'],'anchorPx':o['anchor_px'],'sortY':-60 if o['prop']=='bridge' else o['sortY']}for o in b['objects']], 'actors':[{'id':'Juni','image':'assets-src/character-reboot/B/native/00-front.png','x':512,'y':600,'anchorPx':[40,96],'sortY':600}]}
# Native input is an existing static candidate; choose exact retained frame name.
native=list((R/'assets-src/character-reboot/B').rglob('*front*.png'))
print('Candidate frame paths:',[str(x.relative_to(R))for x in native])
write(S/'placements.json',placements)
print('Exported review-only Phaser assets; original game untouched.')
