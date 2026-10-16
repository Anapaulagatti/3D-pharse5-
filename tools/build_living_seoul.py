"""Process retained generated art and author first-slice data; NEVER call providers.

Optional pinned Forge is an authoring tool, not a setup/runtime dependency.
The western plaza, its source textures, props and Juni atlas are read-only inputs.
"""
from pathlib import Path
import copy, hashlib, json, os, shutil, subprocess, sys
from PIL import Image

R = Path(__file__).resolve().parents[1]
S = R/'assets-src/living-seoul'
G = R/'assets-src/gwanghwamun'
F = Path(os.environ.get('SPRITE_FORGE_ROOT','/workspace/tooling-cache/agent-sprite-forge'))
M = F/'skills/generate2dmap/scripts'
C = R/'.cache/living-seoul'
commands = json.loads((S/'commands.json').read_text()) if (S/'commands.json').exists() else []
def write(p,v):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def run(script,*args):
    cmd=[sys.executable,str(script),*map(str,args)]
    out=subprocess.run(cmd,cwd=R,env=dict(os.environ,FORGE_MAX_PAID_REQUESTS='0'),capture_output=True,text=True)
    commands.append({'command':cmd,'exit':out.returncode,'stdout':out.stdout,'stderr':out.stderr})
    write(S/'commands.json',commands)
    print(out.stdout or out.stderr,flush=True)
    if out.returncode: raise RuntimeError(out.stderr+out.stdout)

assert subprocess.check_output(['git','-C',str(F),'rev-parse','HEAD'],text=True).strip()=='5324342fdfab72430f4e9604f3fe427009f8596d'
# Exact source prompts/references; builtin host route, not provider generation.
write(S/'image-route.json',{'route':'host_image: image_gen','model':None,'estimateUsd':None,'paid_api_requests':0,'video_generation':0,'calls':[
 {'source':'raw/academy.png','prompt':'academy-prompt.txt','reference':'../gwanghwamun/props/hall.png'},
 {'source':'raw/reading-kit.png','prompt':'kit-prompt.txt','reference':'raw/academy.png'},
 {'source':'raw/room.png','prompt':'room-prompt.txt','reference':'raw/academy.png'},
], 'art_source':'host_image', 'hashes':{str(p.relative_to(S)):sha(p) for p in sorted((S/'raw').glob('*.png'))},'note':'Returned model/cost unexposed. Exactly three actual image calls; original host outputs retained. No code-drawn game art.'})
native=C/'resized';native.mkdir(parents=True,exist_ok=True)
specs={'academy':('academy',245,440,75),'kiosk':('kit',132,132,30),'desk':('kit',68,112,28),'shelf':('kit',136,123,23),'sign':('kit',94,58,16)}
for name,(pack,h,_,_) in specs.items():
    source=C/'frames'/name;source.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(S/f'keyed/{pack}/{name}/prop.png',source/'000.png')
    dest=C/'finish'/name
    if not dest.exists():run(F/'skills/video2dsprite/scripts/finish_frames.py','hd','--frames',source,'--output-dir',dest,'--target-height',h,'--display-sizes','1x','--role','prop','--clip',name)
    shutil.copyfile(dest/'frames/000.png',native/f'{name}.png')
if not (S/'palette').exists():run(F/'skills/generate2dsprite/scripts/palette_tool.py','build','--input',native,'--colors',96,'--balance','--name','Sejong Academy','--output-dir',S/'palette')
if not (C/'quantized').exists():run(F/'skills/generate2dsprite/scripts/palette_tool.py','apply','--input',native,'--palette',S/'palette/palette.json','--orphans',0,'--output-dir',C/'quantized')
newprops={}
for name,(_,_,w,h) in specs.items():
    im=Image.open(C/f'quantized/{name}.png').convert('RGBA');im=im.crop(im.getbbox())
    canvas=Image.new('RGBA',(im.width+4,im.height+4));canvas.paste(im,(2,2));p=S/f'props/{name}.png';p.parent.mkdir(exist_ok=True);canvas.save(p)
    newprops[name]={'image':f'props/{name}.png','sha256':sha(p),'anchor_px':[canvas.width//2,canvas.height-1],'size':list(canvas.size),'footprint':{'shape':'rect','width':w,'depth':h,'offset':[0,-h/2],'basis':'world_px'},'solid':True,'occlusion_class':'tall','occupant_policy':'y_sort'}
# A generated room foundation, not a procedural floor. Uniform scale, 1px aspect crop.
room=Image.open(S/'raw/room.png').convert('RGB');room=room.resize((769,576),Image.Resampling.BOX).crop((0,0,768,576));room=room.quantize(colors=128,method=Image.Quantize.MEDIANCUT).convert('RGBA');room.save(S/'room-base.png')
write(S/'room-finish.json',{'input_sha256':sha(S/'raw/room.png'),'output_sha256':sha(S/'room-base.png'),'size':[768,576],'operations':['BOX area reduction to769x576','crop1px right to4:3','128-color no-dither median-cut'],'not_claimed':'Seamless tile or generated logical pixel grid.'})
original=json.loads((G/'map-bundle.json').read_text())
out=copy.deepcopy(original);out.update(id='living-seoul-first-slice',name='Living Seoul — Plaza / Book Alley / Hangul Academy')
out['world']['width']=2048;out['camera']['bounds']=[0,0,2048,768]
out['tilesets']=[{'id':'town','manifest':'../gwanghwamun/tileset.json'}]
for p in out['props'].values():p['image']='../gwanghwamun/'+p['image']
out['props'].update(newprops)
for o in out['objects']:o['occluder']['source']=out['props'][o['prop']]['image']
out['collision']['walkRegions'][0]['polygon']=[[32,32],[2016,32],[2016,736],[32,736]]
oldground=json.loads((G/'layers/ground.json').read_text());ground=[]
way=[(1024,608),(1184,608),(1312,544),(1440,544),(1536,480),(1800,480),(1920,576)]
def distance(x,y,a,b):
    dx,dy=b[0]-a[0],b[1]-a[1];t=max(0,min(1,((x-a[0])*dx+(y-a[1])*dy)/(dx*dx+dy*dy)))
    return ((x-a[0]-t*dx)**2+(y-a[1]-t*dy)**2)**.5
for row in range(24):
    line=oldground[row][:]
    for col in range(32,64):
        x,y=col*32+16,row*32+16
        path=min(distance(x,y,a,b) for a,b in zip(way,way[1:]))<60
        court=1270<x<1770 and 360<y<564
        reading=1770<x<1970 and 430<y<670
        gardenloop=1100<x<1260 and 400<y<700
        m=0 if path or court else 1 if reading or gardenloop else 2
        line.append(m*2+(col*17+row*29+col*row)%2)
    ground.append(line)
write(S/'outdoor/ground.json',ground);write(S/'outdoor/edging.json',[[-1]*64 for _ in range(24)])
out['layers']=[{'name':'Ground','kind':'tiles','data':'outdoor/ground.json','tileset':'town'},{'name':'Edging','kind':'tiles','data':'outdoor/edging.json','tileset':'town'},{'name':'Props','kind':'objects'}]
def place(prop,x,y,purpose):
    p=out['props'][prop];out['objects'].append({'id':f'district-{len(out["objects"])+1}','prop':prop,'x':x,'y':y,'scale':1,'anchor_px':p['anchor_px'],'sortY':y,'occlusion':'tall','occluder':{'source':p['image'],'alphaThreshold':128},'purpose':purpose})
place('academy',1536,410,'Academy hall; south steps lead to reading room')
place('kiosk',1850,527,'Book exchange beside library garden')
place('sign',1425,505,'Academy entrance direction')
for prop,x,y,purpose in [
 ('ginkgo',1115,245,'Shade at book-alley turn'),('tree',1240,195,'Rear academy garden'),('ginkgo',1450,230,'Rear academy orchard'),('tree',1690,230,'Rear reading garden'),('ginkgo',1865,240,'Rear library garden'),('tree',1980,340,'East boundary green buffer'),('tree',1100,450,'Rest garden'),('ginkgo',1200,730,'South alley shade'),('tree',1650,720,'South reading garden'),('tree',1940,730,'East garden edge'),('ginkgo',1810,730,'Library garden shade'),
 ('pavilion',1190,385,'Small covered reading corner'),
 ('bench',1138,504,'Rest beneath west garden tree'),('bench',1750,575,'Library garden rest facing courtyard'),('bench',1380,650,'Alley resting corner'),
 ('jars',1310,428,'Storage beside academy timber wall'),('jars',1765,416,'Storage at east academy wall'),('jars',1145,407,'Reading pavilion water jars'),
 ('planter',1375,420,'Flowers flank academy approach'),('planter',1700,423,'Flowers flank academy approach'),('planter',1910,552,'Kiosk flowers'),('planter',1360,605,'Alley edge planting'),
 ('lantern',1060,553,'Plaza/alley threshold'),('lantern',1330,503,'Academy courtyard turn'),('lantern',1730,493,'Library connection'),('lantern',1900,635,'Garden loop turn'),
 ('wall',1120,116,'Rear garden boundary'),('wall',1925,145,'Rear library boundary')]:place(prop,x,y,purpose)
# Named reachable approaches, not points embedded inside solid facades.
out['anchors'].update({'book-alley':{'point':[1100,608],'approach':[1100,608]},'academy':{'point':[1536,434],'approach':[1536,475]},'library':{'point':[1850,552],'approach':[1850,570]},'garden':{'point':[1720,624],'approach':[1720,624]}})
out['interactions']=[{'id':k,'x':v['point'][0],'y':v['point'][1],'reach':90} for k,v in out['anchors'].items()]
out['portals']=[{'id':'academy-door','circle':[1536,434,16],'to':'academy-reading-room:start','entranceByFrom':{'academy-reading-room':[1536,475]},'latch':True,'reciprocal':True}]
out['spawns']=[{'id':'start','x':512,'y':600,'facing':'south'},{'id':'academy-return','x':1536,'y':475,'facing':'south'}]
write(S/'outdoor-draft.json',out)
# The room is its own lazy-loaded chunk/bundle, with reciprocal exits and explicit foot blockers.
rp={k:copy.deepcopy(v) for k,v in newprops.items() if k in ['shelf','desk']}
roomobj=[]
for i,(prop,x,y) in enumerate([('shelf',170,240),('shelf',600,240),('desk',385,320)]):
    p=rp[prop];roomobj.append({'id':f'room-{i}','prop':prop,'x':x,'y':y,'sortY':y,'scale':1,'anchor_px':p['anchor_px'],'occlusion':'tall'})
write(S/'room/ground.json',[[-1]*24 for _ in range(18)]);write(S/'room/edging.json',[[-1]*24 for _ in range(18)])
rb={'schema':'generate2dmap.map_bundle.v2','id':'academy-reading-room','name':'Sejong Hangul Academy — reading room (unmanned first slice)','world':{'width':768,'height':576,'unit':'px'},'tile_size':[32,32],'tilesets':[{'id':'town','manifest':'../gwanghwamun/tileset.json'}],'layers':[{'name':'RoomBase','kind':'image','image':'room-base.png'},{'name':'Ground','kind':'tiles','data':'room/ground.json','tileset':'town'},{'name':'Edging','kind':'tiles','data':'room/edging.json','tileset':'town'},{'name':'Props','kind':'objects'}],'props':rp,'objects':roomobj,'collision':{'actorRadius':8,'ySquash':.5,'walkRegions':[{'polygon':[[40,156],[728,156],[728,536],[40,536]]}],'solids':[],'rects':[]},'nav':{'cell':4},'spawns':[{'id':'start','x':384,'y':490,'facing':'north'}],'anchors':{'study':{'point':[385,354],'approach':[385,370]},'exit':{'point':[384,510],'approach':[384,490]}},'interactions':[{'id':'study','x':385,'y':354,'reach':90},{'id':'exit','x':384,'y':510,'reach':60}],'portals':[{'id':'reading-room-exit','circle':[384,510,14],'to':'living-seoul-first-slice:academy-return','entranceByFrom':{'living-seoul-first-slice':'start'},'latch':True,'reciprocal':True}],'art_source':'host_image'}
write(S/'room-draft.json',rb)
for name in ['outdoor','room']:
    canonical=S/f'{name}-bundle.json';draft=S/f'{name}-draft.json'
    hashed=C/f'{name}-hashed-{sha(draft)[:12]}.json'
    if not hashed.exists():run(M/'map_bundle.py','hash','--bundle',draft,'--output',hashed)
    shutil.copyfile(hashed,canonical)
    # map paths remain relative to S, not .cache: canonical validation after hashing.
    run(M/'map_bundle.py','validate','--bundle',canonical,'--report',C/f'{name}-validation-{len(commands)}.json')
    derived=S/name
    for part,report in [('navigation','nav-report.json'),('tiled','export-report.json'),('linked-navigation','nav-report.json')]:
        target=derived/part
        if target.exists() and json.loads((target/report).read_text())['inputs'][0]['sha256']!=sha(canonical):
            saved=C/'previous-derived'/f'{name}-{part}-{len(commands)}';saved.parent.mkdir(parents=True,exist_ok=True);shutil.move(target,saved)
    if not (derived/'navigation').exists():run(M/'map_nav.py','check','--bundle',canonical,'--output-dir',derived/'navigation','--publish-on-fail')
    if not (derived/'tiled').exists():run(M/'export_tiled.py','export','--bundle',canonical,'--output-dir',derived/'tiled','--embedded-variant')
    t=json.loads((derived/'tiled/map.embedded.tmj').read_text());collision=next(l for l in t['layers'] if l['name']=='collision')
    solids=[o for o in collision['objects'] if o['type']=='solid']
    assert all(not o.get('polygon') and not o.get('rotation') for o in solids)
    # Phaser rectangular world bounds alone cannot enforce the narrower room walk region.
    walls=[] if name=='outdoor' else [{'id':9000+i,'type':'solid','x':x,'y':y,'width':w,'height':h} for i,(x,y,w,h) in enumerate([(0,0,768,156),(0,0,40,576),(728,0,40,576),(0,536,768,40)])]
    t['layers']=[l for l in t['layers'] if l['type']=='tilelayer']+[dict(collision,name='Collision',objects=solids+walls)]
    t['tilesets']=[dict(t['tilesets'][0],image='tiles.png')]
    D=R/f'public/review/living-seoul/{name}';D.mkdir(parents=True,exist_ok=True);write(D/'plaza.json',t)
    b=json.loads(canonical.read_text())
    for prop,p in b['props'].items():shutil.copyfile(S/p['image'],D/f'{prop}.png')
    shutil.copyfile(G/'tiles.png',D/'tiles.png')
    if name=='room':shutil.copyfile(S/'room-base.png',D/'room-base.png')
    layout={'width':b['world']['width'],'height':b['world']['height'],'spawn':[b['spawns'][0]['x'],b['spawns'][0]['y']],'npc':[354,480],'follow':55,'role':b['name'],'mood':'Living Seoul review','vi':b['name'],'mapSha256':sha(D/'plaza.json'),'objects':[]}
    for i,o in enumerate(b['objects']):
        f=b['props'][o['prop']]['footprint'];layout['objects'].append({'id':i+1,'kind':o['prop'],'x':o['x'],'y':o['y'],'width':f['width'],'height':f['depth'],'label':o['prop'],'collide':o.get('solid',b['props'][o['prop']]['solid'])})
    write(S/f'{name}-world.json',layout);write(D/'anchors.json',{k:p['anchor_px']for k,p in b['props'].items()})
    write(derived/'runtime-export.json',{'source_bundle_sha256':sha(canonical),'tiled_solids_exact':len(solids),'runtime_region_boundary_rectangles':walls,'note':'Room boundary rectangles enforce its canonical walk region; all exported original solids unchanged.'})
for name,other in [('outdoor','room'),('room','outdoor')]:
    dest=S/name/'linked-navigation'
    if dest.exists() and any(not (dest/i['path']).exists() or sha(dest/i['path'])!=i['sha256'] for i in json.loads((dest/'nav-report.json').read_text())['inputs']):
        shutil.move(dest,C/'previous-derived'/f'{name}-linked-refresh-{len(commands)}')
    if not dest.exists():run(M/'map_nav.py','check','--bundle',S/f'{name}-bundle.json','--link',S/f'{other}-bundle.json','--output-dir',dest)
write(S/'preserved-baseline.json',{'baseline':'5b0eabacb28e0cd74e0519b9e69bc9fc75e14a83','preserved':[{'path':str(p.relative_to(R)),'sha256':sha(p)} for directory in ['assets-src/gwanghwamun','assets-src/juni-animation','public/review/gwanghwamun','public/review/juni-animation','assets-src/world','assets-src/actors'] for p in sorted((R/directory).rglob('*')) if p.is_file()],'west_ground_equal':all(row[:32]==oldground[y] for y,row in enumerate(ground)),'west_objects_equal':[{k:v for k,v in o.items() if k!='occluder'} for o in out['objects'][:32]]==[{k:v for k,v in o.items() if k!='occluder'} for o in original['objects']]})
print('First-slice source and runtime export complete. Inspect raw QA; no art approval inferred.')
