"""Actual Forge composition and linked-room navigation; preserves all old inputs."""
from production_art import R,S,C,F,run,write,sha
from PIL import Image
import json,copy,shutil
B=json.loads((S/'outdoor-bundle.json').read_text());W=B['world']['width'];H=B['world']['height'];tiles=Image.open(S/'tiles.png').convert('RGBA');base=Image.new('RGBA',(W,H))
for name in ['ground','edging']:
 for row,line in enumerate(json.loads((S/f'layers/{name}.json').read_text())):
  for col,index in enumerate(line):
   if index>=0:base.alpha_composite(tiles.crop(((index%16)*32,(index//16)*32,(index%16+1)*32,(index//16+1)*32)),(col*32,row*32))
base.save(S/'layers/base.png')
placements={'props':[{'id':o['id'],'image':str((S/B['props'][o['prop']]['image']).resolve()),'x':o['x'],'y':o['y'],'anchorPx':o['anchor_px'],'sortY':o['sortY']}for o in B['objects']]}
write(S/'placements.json',placements)
# Fresh derived folder each edit; original reports remain retained in .cache.
out=S/'composed'
if out.exists():shutil.move(out,C/f'composed-{len(json.loads((S/"commands.json").read_text()))}')
out.mkdir()
run(F/'skills/generate2dmap/scripts/compose_layered_preview.py','--base',S/'layers/base.png','--placements',S/'placements.json','--output',out/'preview.png','--report',out/'composition.json','--bundle',S/'outdoor-bundle.json','--debug-overlay',out/'collision-overlay.png','--audit-out',out/'audit.json')
im=Image.open(out/'preview.png');im.resize((512,216),Image.Resampling.NEAREST).save(R/'public/review/seoul-production/minimap.png')
# Preserve old room pixels/runtime; only a new reciprocal source link is authored.
room=copy.deepcopy(json.loads((R/'assets-src/living-seoul/room-bundle.json').read_text()));room['id']='seoul-production-reading-room'
for ts in room['tilesets']:ts['manifest']='../living-seoul/'+ts['manifest']
for layer in room['layers']:
 for key in ['data','image']:
  if key in layer:layer[key]='../living-seoul/'+layer[key]
for p in room['props'].values():p['image']='../living-seoul/'+p['image']
room['portals']=[{'id':'production-room-exit','circle':[384,510,14],'to':'seoul-production-north:academy-return','entranceByFrom':{'seoul-production-north':'start'},'latch':True,'reciprocal':True}]
write(S/'room-draft.json',room)
# Hash paths at canonical source root, never in cache.
hashed=C/f'room-hashed-{sha(S/"room-draft.json")[:12]}.json'
if not hashed.exists():run(F/'skills/generate2dmap/scripts/map_bundle.py','hash','--bundle',S/'room-draft.json','--output',hashed)
shutil.copyfile(hashed,S/'room-bundle.json')
# New production portal only: baseline room is never modified.
draft=json.loads((S/'outdoor-draft.json').read_text());draft['portals'][0]['to']='seoul-production-reading-room:start';draft['portals'][0]['entranceByFrom']={'seoul-production-reading-room':[672,832]};write(S/'outdoor-draft.json',draft)
hashed=C/f'linked-outdoor-hashed-{sha(S/"outdoor-draft.json")[:12]}-{sha(S/"tileset.json")[:12]}-{sha(S/"layers/edging.json")[:12]}.json'
if not hashed.exists():run(F/'skills/generate2dmap/scripts/map_bundle.py','hash','--bundle',S/'outdoor-draft.json','--output',hashed)
shutil.copyfile(hashed,S/'outdoor-bundle.json')
for name,other in [('outdoor','room'),('room','outdoor')]:
 dest=S/f'{name}-linked-navigation'
 if dest.exists():shutil.move(dest,C/f'linked-{name}-{len(json.loads((S/"commands.json").read_text()))}')
 run(F/'skills/generate2dmap/scripts/map_bundle.py','validate','--bundle',S/f'{name}-bundle.json','--report',C/f'linked-{name}-validation-{len(json.loads((S/"commands.json").read_text()))}.json')
 run(F/'skills/generate2dmap/scripts/map_nav.py','check','--bundle',S/f'{name}-bundle.json','--link',S/f'{other}-bundle.json','--output-dir',dest,'--publish-on-fail')
