"""Actual Forge map hash/validate/nav/Tiled/compose; publish stored Phaser inputs."""
from full_world_art import *
from PIL import Image
import math
M=F/'skills/generate2dmap/scripts'
def export(folder,name,runtime):
 p=S/folder;draft=p/f'{name}-draft.json';fp=sha(draft)[:12]+'-'+sha(p/'tiles.png')[:12];cache=C/f'{folder}-{fp}';cache.mkdir(parents=True,exist_ok=True)
 hashed=cache/'bundle.json'
 if not hashed.exists():run(M/'map_bundle.py','hash','--bundle',draft,'--output',hashed)
 shutil.copyfile(hashed,p/f'{name}-bundle.json');bundle=p/f'{name}-bundle.json';b=json.loads(bundle.read_text())
 run(M/'map_bundle.py','validate','--bundle',bundle,'--report',cache/'validate.json')
 for sub,script,args in [('navigation','map_nav.py',['check','--publish-on-fail']),('tiled','export_tiled.py',['export','--embedded-variant'])]:
  out=cache/sub
  if not out.exists():run(M/script,*args,'--bundle',bundle,'--output-dir',out)
  dest=p/sub
  if dest.exists():shutil.move(dest,C/f'previous-{folder}-{sub}-{len(json.loads((S/"commands.json").read_text()))}')
  shutil.copytree(out,dest)
 t=json.loads((p/'tiled/map.embedded.tmj').read_text());collision=next(l for l in t['layers']if l['name']=='collision');solids=[o for o in collision['objects']if o['type']=='solid'];assert all(not o.get('polygon')for o in solids)
 t['layers']=[l for l in t['layers']if l['type']=='tilelayer']+[dict(collision,name='Collision',objects=solids)];t['tilesets']=[dict(t['tilesets'][0],image='tiles.png')]
 d=R/'public/review/full-world'/runtime;d.mkdir(parents=True,exist_ok=True);write(d/'plaza.json',t);shutil.copyfile(p/'tiles.png',d/'tiles.png')
 for key,a in b['props'].items():shutil.copyfile(p/a['image'],d/f'{key}.png')
 write(d/'anchors.json',{k:a['anchor_px']for k,a in b['props'].items()})
 w,h=b['world']['width'],b['world']['height'];spawn=next(a for a in b['spawns']if a['id']=='start')
 world={'width':w,'height':h,'spawn':[spawn['x'],spawn['y']],'npc':[spawn['x']+160,spawn['y']],'follow':55,'role':b['name'],'mood':'Original Korean travel-world review increment','vi':b['name'],'mapSha256':sha(d/'plaza.json'),'objects':[{'id':i+1,'kind':o['prop'],'x':o['x'],'y':o['y'],'sortY':o['sortY'],'width':b['props'][o['prop']]['footprint']['width'],'height':b['props'][o['prop']]['footprint']['depth'],'label':o['purpose'],'collide':False}for i,o in enumerate(b['objects'])]};write(p/'world.json',world)
 # Compose literal exported pixels and props for editable source audit (not Phaser proof).
 atlas=Image.open(p/'tiles.png').convert('RGBA');base=Image.new('RGBA',(w,h))
 for layer in [p/'layers/ground.json',p/'layers/edging.json']:
  for y,row in enumerate(json.loads(layer.read_text())):
   for x,i in enumerate(row):
    if i>=0:base.alpha_composite(atlas.crop(((i%64)*32,(i//64)*32,(i%64+1)*32,(i//64+1)*32)),(x*32,y*32))
 base.save(p/'layers/base.png');placements={'props':[{'id':o['id'],'image':b['props'][o['prop']]['image'],'x':o['x'],'y':o['y'],'anchorPx':o['anchor_px'],'sortY':o['sortY']}for o in b['objects']]};write(p/'placements.json',placements)
 out=cache/'composed'
 if not out.exists():out.mkdir();run(M/'compose_layered_preview.py','--base',p/'layers/base.png','--placements',p/'placements.json','--output',out/'preview.png','--report',out/'composition.json','--bundle',bundle,'--debug-overlay',out/'collision-overlay.png','--audit-out',out/'audit.json')
 if (p/'composed').exists():shutil.move(p/'composed',C/f'previous-{folder}-composed-{len(json.loads((S/"commands.json").read_text()))}')
 shutil.copytree(out,p/'composed');base=Image.open(out/'preview.png');base.resize((288,round(h*288/w)),Image.Resampling.NEAREST).save(d/'minimap.png');print(json.dumps({'folder':folder,'objects':len(b['objects']),'colliders':len(solids),'world':[w,h]}))
if __name__=='__main__':
 export('map','outdoor','world')
