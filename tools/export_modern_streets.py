"""Actual Forge palette/map/nav/Tiled/compose export of V3; no generation or provider routes."""
from modern_streets_art import *
from PIL import Image
import math,copy,numpy as np
P=S/'map';M=F/'skills/generate2dmap/scripts'
def hashed(draft,out):
 # A draft can be byte-identical while referenced terrain changes. Cache ALL current input bytes.
 refs=[]
 def visit(v):
  if isinstance(v,dict):
   for k,a in v.items():
    if k in ['manifest','image','data','source']and isinstance(a,str):
     p=(draft.parent/a).resolve()
     if p.is_file():refs.append([str(p.relative_to(R)),sha(p)])
    visit(a)
  elif isinstance(v,list):
   for a in v:visit(a)
 visit(json.loads(draft.read_text()));fingerprint=hashlib.sha256(json.dumps([sha(draft),sorted(refs)]).encode()).hexdigest()[:16]
 cache=C/f'hash-references-{fingerprint}.json'
 if not cache.exists():
  temp=draft.parent/f'.hash-{fingerprint}.json'
  run(M/'map_bundle.py','hash','--bundle',draft,'--output',temp)
  shutil.copyfile(temp,out);shutil.move(temp,cache)
 else:shutil.copyfile(cache,out)
 write(S/'last-hash-inputs.json',{'draft':str(draft.relative_to(R)),'fingerprint':fingerprint,'references':refs})
def finish():
 # Finish the literal RGB terrain/mask composition with the real shared-palette tool.
 inp=P/'terrain-composite-unquantized.png';q=C/f'ground-palette-{sha(inp)[:16]}'
 if not q.exists():run(F/'skills/generate2dsprite/scripts/palette_tool.py','apply','--input',inp,'--palette',S/'palette/palette.json','--orphans',0,'--output-dir',q)
 src=Image.open(q/inp.name).convert('RGBA');src.save(P/'ground-native.png');W,H=src.size;unique=[];lookup={}
 def reg(im):
  im=im.convert('RGBA');key=im.tobytes()
  if key not in lookup:lookup[key]=len(unique);unique.append(im)
  return lookup[key]
 a=np.array(src);ground=[]
 for y in range(H//32):ground.append([reg(Image.fromarray(a[y*32:y*32+32,x*32:x*32+32]))for x in range(W//32)])
 # Gentle real source-pixel ripple phases; only full-water cells are animated, shoreline art stays stable.
 waves=[]
 for name in ['deep-water','shallow-water']:
  texture=np.array(Image.open(S/f'terrain/{name}.png').convert('RGBA'))
  for ty in range(4):
   for tx in range(4):
    indices=[]
    for phase in [0,1,2,3,2,1]:
     data=np.roll(texture,phase,axis=1);indices.append(reg(Image.fromarray(data[ty*32:ty*32+32,tx*32:tx*32+32])))
    waves.append(indices)
 columns=128;atlas=Image.new('RGBA',(columns*32,math.ceil(len(unique)/columns)*32));assert max(atlas.size)<=4096,(len(unique),atlas.size)
 for i,im in enumerate(unique):atlas.paste(im,((i%columns)*32,(i//columns)*32))
 atlas.save(P/'tiles.png');write(P/'tileset.json',{'schema':'generate2dmap.tileset.v1','image':'tiles.png','sha256':sha(P/'tiles.png'),'tile_size':[32,32],'columns':columns,'kind':'flat','materials':['original-heritage','grass','forest','concrete','pavers','asphalt','sand','basalt','water'],'tiles':[{'index':i,'properties':{'walkable':True}}for i in range(len(unique))],'art_source':'host_image','seamless_verified':False})
 write(P/'layers/ground.json',ground);write(P/'layers/edging.json',[[-1]*(W//32)for _ in range(H//32)]);write(S/'water.json',{'frames':waves,'periodMs':180,'source':'literal generated water pixels shifted0,1,2,3,2,1; no code-painted water; visible tiles only'})
 b=json.loads((P/'outdoor-draft.json').read_text());used={o['prop']for o in b['objects']};b['props']={k:v for k,v in b['props'].items()if k in used};write(P/'outdoor-draft.json',b);hashed(P/'outdoor-draft.json',P/'outdoor-bundle.json');bundle=P/'outdoor-bundle.json';out=C/f'export-{sha(bundle)[:16]}';out.mkdir(exist_ok=True)
 run(M/'map_bundle.py','validate','--bundle',bundle,'--report',out/'validate.json')
 if not (out/'tiled').exists():run(M/'export_tiled.py','export','--embedded-variant','--bundle',bundle,'--output-dir',out/'tiled')
 dest=P/'tiled'
 if dest.exists():shutil.move(dest,C/f'prior-tiled-{sha(dest/"map.embedded.tmj")[:12]}-{len(json.loads((S/"commands.json").read_text()))}')
 shutil.copytree(out/'tiled',dest);t=json.loads((dest/'map.embedded.tmj').read_text());collision=next(l for l in t['layers']if l['name']=='collision');solids=[o for o in collision['objects']if o['type']=='solid'];assert all(not o.get('polygon')for o in solids)
 t['layers']=[l for l in t['layers']if l['type']=='tilelayer']+[dict(collision,name='Collision',objects=solids)];t['tilesets']=[dict(t['tilesets'][0],image='tiles.png')]
 d=R/'public/review/modern-streets/world';d.mkdir(parents=True,exist_ok=True);write(d/'plaza.json',t);shutil.copyfile(P/'tiles.png',d/'tiles.png')
 for k,p in b['props'].items():shutil.copyfile(P/p['image'],d/f'{k}.png')
 shutil.copyfile(R/'public/review/full-world/world/rf-prod-doors.png',d/'rf-prod-doors.png')
 write(d/'anchors.json',{k:p['anchor_px']for k,p in b['props'].items()})
 world={'width':W,'height':H,'spawn':[2176,832],'npc':[2336,832],'follow':55,'role':b['name'],'mood':'Heritage to contemporary Korean exploration','vi':b['name'],'mapSha256':sha(d/'plaza.json'),'objects':[{'id':i+1,'kind':o['prop'],'x':o['x'],'y':o['y'],'sortY':o['sortY'],'width':b['props'][o['prop']]['footprint']['width'],'height':b['props'][o['prop']]['footprint']['depth'],'label':o['purpose'],'collide':False}for i,o in enumerate(b['objects'])]};write(P/'world.json',world)
 # Retained room source is rebased, not regenerated, and linked to the new map.
 old=R/'assets-src/full-world/room-bundle.json'
 def rebase(v):
  if isinstance(v,dict):return {k:(os.path.relpath((old.parent/a).resolve(),S)if k in ['manifest','image','data','source']and isinstance(a,str)and a.startswith('../')else rebase(a))for k,a in v.items()}
  if isinstance(v,list):return [rebase(a)for a in v]
  return v
 room=rebase(json.loads(old.read_text()));room['id']='v3-reading-room';room['portals']=[{'id':'return-world','circle':[384,536,20],'to':'v3-korea:room-return','entranceByFrom':{'v3-korea':[384,480]},'reciprocal':True}];write(S/'room-draft.json',room);hashed(S/'room-draft.json',S/'room-bundle.json')
 print(json.dumps({'props':len(b['objects']),'uniqueAssets':len(used),'solids':len(solids),'uniqueTiles':len(unique),'atlas':list(atlas.size),'world':[W,H]}))
def validate():
 bundle=P/'outdoor-bundle.json';cache=C/f'qa-{sha(bundle)[:16]}';cache.mkdir(exist_ok=True)
 for name,source,other in [('world',bundle,S/'room-bundle.json'),('room',S/'room-bundle.json',bundle)]:
  out=cache/f'{name}-nav'
  if not out.exists():run(M/'map_nav.py','check','--bundle',source,'--link',other,'--output-dir',out,'--publish-on-fail')
  dest=S/f'{name}-navigation'
  if dest.exists():shutil.move(dest,C/f'prior-nav-{name}-{len(json.loads((S/"commands.json").read_text()))}')
  shutil.copytree(out,dest)
 b=json.loads(bundle.read_text());placements={'props':[{'id':o['id'],'image':b['props'][o['prop']]['image'],'x':o['x'],'y':o['y'],'anchorPx':o['anchor_px'],'sortY':o['sortY']}for o in b['objects']]};write(P/'placements.json',placements)
 # Representative unchanged Juni frame, proper native anchor; no static avatar is baked into game minimap.
 image=R/'assets-src/full-world/actor-proof.png';placements['actors']=[{'id':'approved-Juni-native','image':str(image),'x':2176,'y':832,'anchorPx':[48,100],'sortY':832}];write(P/'actor-placements.json',placements)
 out=cache/'compose'
 if not out.exists():
  out.mkdir();run(M/'compose_layered_preview.py','--base',P/'ground-native.png','--placements',P/'actor-placements.json','--output',out/'preview.png','--report',out/'composition.json','--bundle',bundle,'--debug-overlay',out/'collision-overlay.png','--audit-out',out/'audit.json')
 if (P/'composed').exists():shutil.move(P/'composed',C/f'prior-compose-{len(json.loads((S/"commands.json").read_text()))}')
 shutil.copytree(out,P/'composed')
 # Actorless minimap composition is separate; keep the real actor in the actual Phaser renderer.
 out=cache/'minimap'
 if not out.exists():out.mkdir();run(M/'compose_layered_preview.py','--base',P/'ground-native.png','--placements',P/'placements.json','--output',out/'preview.png','--report',out/'composition.json')
 Image.open(out/'preview.png').resize((288,round(4800*288/4352)),Image.Resampling.NEAREST).save(R/'public/review/modern-streets/world/minimap.png')
if __name__=='__main__':{'finish':finish,'validate':validate}[sys.argv[1]]()
