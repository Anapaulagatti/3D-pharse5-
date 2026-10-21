"""Native imagery → editable tiles/props → real Forge/Tiled/nav. No media/API route."""
from map_pipeline import *
from PIL import Image,ImageOps,ImageChops
import math,os,shutil
S=SOURCE;P=S/'map';L=ROOT/'assets-src/library';D=ROOT/'public/assets/world';M=FORGE/'skills/generate2dmap/scripts';P.mkdir(parents=True,exist_ok=True);D.mkdir(parents=True,exist_ok=True)
def hashed(src,dest):
 temp=src.parent/('.hashed-'+str(len(json.loads((SOURCE/'forge-commands.json').read_text())))+'.json')
 run(M/'map_bundle.py','hash','--bundle',src,'--output',temp);shutil.copyfile(temp,dest);shutil.move(temp,CACHE/temp.name)
def export():
 src=Image.open(P/'ground-native.png').convert('RGBA');W,H=src.size;unique=[];lookup={};grid=[]
 for y in range(0,H,32):
  row=[]
  for x in range(0,W,32):
   tile=src.crop((x,y,x+32,y+32));key=tile.tobytes()
   if key not in lookup:lookup[key]=len(unique);unique.append(tile)
   row.append(lookup[key])
  grid.append(row)
 # Six gentle source-pixel water phases; no synthetic video or timing claim.
 water_groups=[];water_seen=set();draft_art=json.loads((P/'draft.json').read_text()).get('art_source')
 if draft_art=='host_image':
  for kind in ['sea','shallows']:
   file=SOURCE/'art/water-revised'/(kind+'-1.png')
   if not file.exists():continue
   im=Image.open(file).convert('RGBA');base=Image.new('RGBA',(128,128));base.paste(im,(0,0));base.paste(ImageOps.mirror(im),(64,0));base.paste(ImageOps.flip(im),(0,64));base.paste(ImageOps.flip(ImageOps.mirror(im)),(64,64))
   for yy in range(0,128,32):
    for xx in range(0,128,32):
     key=base.crop((xx,yy,xx+32,yy+32)).tobytes();idx=lookup.get(key)
     if idx is None or idx in water_seen:continue
     water_seen.add(idx);group=[idx]
     for shift in [1,2,3,2,1]:group.append(len(unique));unique.append(ImageChops.offset(base,shift,0).crop((xx,yy,xx+32,yy+32)))
     water_groups.append(group)
 cols=128;atlas=Image.new('RGBA',(cols*32,math.ceil(len(unique)/cols)*32));assert max(atlas.size)<=4096
 for i,tile in enumerate(unique):atlas.paste(tile,((i%cols)*32,(i//cols)*32))
 atlas.save(P/'tiles.png');write(P/'tileset.json',{'schema':'generate2dmap.tileset.v1','image':'tiles.png','sha256':sha(P/'tiles.png'),'tile_size':[32,32],'columns':cols,'kind':'flat','materials':['approved-north','authored-south'],'tiles':[{'index':i,'properties':{'walkable':True}}for i in range(len(unique))],'art_source':'host_image','seamless_verified':False});write(P/'layers/ground.json',grid);write(P/'layers/edging.json',[[-1]*(W//32)for _ in range(H//32)])
 b=json.loads((P/'draft.json').read_text());used={o['prop']for o in b['objects']};catalog=json.loads((L/'props.json').read_text());catalog={k:dict(v,image=str(L/v['image']))for k,v in catalog.items()};extra=P/'extra-props.json';catalog.update(json.loads(extra.read_text())if extra.exists()else{});b['props']={}
 for key in used:
  p=dict(catalog[key]);p['image']=os.path.relpath(p['image'],P);p.pop('colliders',None);b['props'][key]=p
 for o in b['objects']:o['occluder']['source']=b['props'][o['prop']]['image']
 write(P/'draft.json',b);hashed(P/'draft.json',P/'bundle.json')
 bundle=P/'bundle.json';out=CACHE/('export-'+sha(bundle)[:16]);out.mkdir(exist_ok=True)
 report=out/f'validation-{len(json.loads((S/"forge-commands.json").read_text()))}.json';run(M/'map_bundle.py','validate','--bundle',bundle,'--report',report)
 if not(out/'tiled').exists():run(M/'export_tiled.py','export','--bundle',bundle,'--embedded-variant','--output-dir',out/'tiled')
 dest=P/'tiled'
 if dest.exists():shutil.move(dest,CACHE/('prior-tiled-'+str(len(json.loads((S/'forge-commands.json').read_text())))))
 shutil.copytree(out/'tiled',dest);t=json.loads((dest/'map.embedded.tmj').read_text());coll=next(l for l in t['layers']if l['name']=='collision');t['layers']=[l for l in t['layers']if l['type']=='tilelayer']+[dict(coll,name='Collision',objects=[o for o in coll['objects']if o['type']=='solid'])];t['tilesets']=[dict(t['tilesets'][0],image='tiles.png')];write(D/'plaza.json',t);shutil.copyfile(P/'tiles.png',D/'tiles.png')
 for key,p in b['props'].items():shutil.copyfile(P/p['image'],D/f'{key}.png')
 allowed={k+'.png'for k in used}|{'tiles.png','minimap.png'}
 removed=[]
 for prior in D.glob('*.png'):
  if prior.name not in allowed:removed.append({'file':prior.name,'sha256':sha(prior)});prior.unlink()
 write(S/'runtime-pruned.json',{'onlySupersededRuntimeCopies':removed,'originalArt':'Preserved independently in assets-src/library and recovery tags'})
 write(D/'anchors.json',{key:p['anchor_px']for key,p in b['props'].items()});world={'width':W,'height':H,'spawn':[2176,832],'npc':[2336,832],'follow':55,'role':b['name'],'mood':'Korean learning world','vi':b['name'],'mapSha256':sha(D/'plaza.json'),'objects':[{'id':i+1,'kind':o['prop'],'x':o['x'],'y':o['y'],'sortY':o['sortY'],'width':b['props'][o['prop']]['footprint']['width'],'height':b['props'][o['prop']]['footprint']['depth'],'label':o['purpose'],'collide':False}for i,o in enumerate(b['objects'])]};write(P/'world.json',world)
 # Source interior references were recursively preserved before cleanup.
 room=ROOT/'assets-src/interiors/academy';hashed(room/'bundle-draft.json',room/'bundle.json')
 for name,source,other in [('world',bundle,room/'bundle.json'),('academy',room/'bundle.json',bundle)]:
  output=out/(name+'-nav')
  if not output.exists():run(M/'map_nav.py','check','--bundle',source,'--link',other,'--output-dir',output,'--publish-on-fail')
  dest=S/(name+'-navigation')
  if dest.exists():shutil.move(dest,CACHE/('prior-'+name+'-nav-'+str(len(json.loads((S/'forge-commands.json').read_text())))))
  shutil.copytree(output,dest)
 placements={'props':[{'id':o['id'],'image':b['props'][o['prop']]['image'],'x':o['x'],'y':o['y'],'anchorPx':o['anchor_px'],'sortY':o['sortY']}for o in b['objects']]};write(P/'placements.json',placements);compose=out/'compose';compose.mkdir(exist_ok=True)
 if not(compose/'preview.png').exists():run(M/'compose_layered_preview.py','--base',P/'ground-native.png','--placements',P/'placements.json','--bundle',bundle,'--output',compose/'preview.png','--report',compose/'report.json','--debug-overlay',compose/'debug.png','--audit-out',compose/'audit.json')
 Image.open(compose/'preview.png').resize((288,round(H*288/W)),Image.Resampling.NEAREST).save(D/'minimap.png')
 write(S/'water.json',{'frames':water_groups,'periodMs':180,'source':'Original host-generated sea/shallows, nearest literal pixel-offset phases0,1,2,3,2,1; not video synthesis'});print(json.dumps({'world':[W,H],'props':len(used),'placements':len(b['objects']),'solids':len(b['collision']['solids']),'uniqueTiles':len(unique),'atlas':list(atlas.size)}))
if __name__=='__main__':export()
