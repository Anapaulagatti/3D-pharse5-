"""Assemble the review-only district from recorded generated sources, never generate art/APIs.

Requires the pinned optional Sprite Forge checkout. Every native prop is a Forge
area-finished, palette-applied source image. Python authors layout/collision data only.
"""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys
from PIL import Image

R = Path(__file__).resolve().parents[1]
S = R / 'assets-src/gwanghwamun'
F = Path(os.environ.get('SPRITE_FORGE_ROOT', '/workspace/tooling-cache/agent-sprite-forge'))
M = F / 'skills/generate2dmap/scripts'
V = F / 'skills/video2dsprite/scripts'
P = F / 'skills/generate2dsprite/scripts'
C = R / '.cache/gwanghwamun'
C.mkdir(parents=True, exist_ok=True)
LOG = json.loads((C/'build-commands.json').read_text()) if (C/'build-commands.json').exists() else []

def write(p, data):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

def run(script, *args):
    command = [sys.executable, str(script), *map(str, args)]
    out = subprocess.run(command, cwd=R, env=dict(os.environ, FORGE_MAX_PAID_REQUESTS='0'), capture_output=True, text=True)
    LOG.append({'command': command, 'exit': out.returncode, 'stdout': out.stdout, 'stderr': out.stderr})
    write(C/'build-commands.json', LOG)
    if out.returncode:
        raise RuntimeError(out.stdout + out.stderr)
    print(out.stdout.strip(), flush=True)

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

assert subprocess.check_output(['git', '-C', str(F), 'rev-parse', 'HEAD'], text=True).strip() == '5324342fdfab72430f4e9604f3fe427009f8596d'
specs = {
    'gate': ('gate', 336, 390, 82),
    'pavilion': ('architecture', 174, 182, 54),
    'hall': ('architecture', 210, 185, 58),
    'ginkgo': ('tall', 210, 22, 12),
    'tree': ('tall', 192, 24, 14),
    'sejong': ('tall', 132, 76, 35),
    'bench': ('furniture', 48, 66, 16),
    'lantern': ('furniture', 88, 16, 10),
    'jars': ('furniture', 49, 52, 20),
    'planter': ('furniture', 40, 62, 17),
    'bridge': ('stonework', 52, 0, 0),
    'wall': ('stonework', 52, 112, 18),
}
resized = C/'resized'; resized.mkdir(exist_ok=True)
for name, (pack, height, _, _) in specs.items():
    folder = C/'registered'/name; folder.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(S/f'keyed/{pack}/{name}/prop.png', folder/'000.png')
    dest = C/'finish'/name
    if not dest.exists():
        run(V/'finish_frames.py', 'hd', '--frames', folder, '--output-dir', dest, '--target-height', height, '--display-sizes', '1x', '--clip', name, '--role', 'prop')
    shutil.copyfile(dest/'frames/000.png', resized/f'{name}.png')
if not (S/'palette').exists():
    run(P/'palette_tool.py', 'build', '--input', resized, '--colors', 96, '--balance', '--name', 'Ginkgo Commons', '--output-dir', S/'palette')
if not (C/'quantized').exists():
    run(P/'palette_tool.py', 'apply', '--input', resized, '--palette', S/'palette/palette.json', '--orphans', 0, '--output-dir', C/'quantized')
props = {}
for name, (_, _, w, h) in specs.items():
    im = Image.open(C/f'quantized/{name}.png').convert('RGBA')
    im = im.crop(im.getbbox()); canvas = Image.new('RGBA', (im.width+4, im.height+4));canvas.paste(im,(2,2))
    path = S/f'props/{name}.png'; path.parent.mkdir(exist_ok=True);canvas.save(path)
    # All runtime pivots are precisely the bottom-centre support line, with2px margin.
    props[name] = {'image': f'props/{name}.png', 'sha256':sha(path), 'anchor_px':[canvas.width//2, canvas.height-1], 'size':list(canvas.size), 'footprint': {'shape':'rect','width':w,'depth':h,'offset':[0,-h/2],'basis':'world_px'}, 'solid': bool(w), 'occlusion_class':'tall', 'status':'accepted'}

# Curated terrain passed unchanged Forge contrast/variant/border gates. No seam claim.
atlas = Image.new('RGBA', (128,64)); tiledata=[]
for row,material in enumerate(['granite','earth','grass','water']):
    for variant in range(2):
        idx=row*2+variant;im=Image.open(S/f'terrain-accepted/{material}-{variant+1}.png').convert('RGBA')
        atlas.paste(im,((idx%4)*32,(idx//4)*32)); tiledata.append({'index':idx,'properties':{'material':material,'walkable':True}})
atlas.save(S/'tiles.png')
write(S/'tileset.json', {'schema':'generate2dmap.tileset.v1','image':'tiles.png','sha256':sha(S/'tiles.png'),'tile_size':[32,32],'columns':4,'kind':'flat','materials':['granite','earth','grass','water'],'tiles':tiledata,'seamless_verified':False,'art_source':'host_image'})

ground=[]
for row in range(24):
    line=[]
    for col in range(32):
        x,y=col*32+16,row*32+16
        # Deliberately asymmetric garden pockets; paths remain broad at gameplay size.
        garden=any(((x-cx)/rx)**2+((y-cy)/ry)**2<1 for cx,cy,rx,ry in [(150,210,170,230),(900,245,130,225),(115,730,195,115),(935,740,145,130)])
        earth=(y>610 or (x<330 and 410<y<620) or (x>775 and 440<y<650))
        material=2 if garden else 1 if earth else 0
        if 672<=x<736 and 416<=y<736: material=3
        line.append(material*2+((col*17+row*29+col*row)%2))
    ground.append(line)
write(S/'layers/ground.json',ground)
write(S/'layers/edging.json',[[-1]*32 for _ in range(24)])
objects=[]
def place(prop,x,y, label=None, solid=None):
    p=props[prop]; o={'id':f'{prop}-{len(objects)+1}','prop':prop,'x':x,'y':y,'scale':1,'anchor_px':p['anchor_px'],'sortY':y,'occlusion':p['occlusion_class'],'occluder':{'source':p['image'],'alphaThreshold':128}}
    if solid is not None:o['solid']=solid
    objects.append(o)

place('gate',512,345)
place('pavilion',165,440)
place('hall',862,420)
place('sejong',354,480)
for kind,x,y in [('ginkgo',155,250),('tree',900,230),('tree',100,590),('ginkgo',910,620),('ginkgo',190,725),('tree',815,700),('tree',110,728)]:place(kind,x,y)
for x,y in [(270,365),(750,340),(429,705),(575,705)]:place('lantern',x,y)
for x,y in [(272,505),(826,520),(520,430)]:place('bench',x,y)
for x,y in [(75,458),(939,458),(215,458)]:place('jars',x,y)
for x,y in [(292,355),(710,390),(300,552),(800,550),(420,718),(575,718)]:place('planter',x,y)
place('bridge',704,622,solid=False)
for x,y in [(80,350),(948,350),(80,675),(948,675)]:place('wall',x,y)
anchors={'gate':{'point':[512,355],'approach':[512,390]},'sejong':{'point':[354,490],'approach':[354,520]},'pavilion':{'point':[165,448],'approach':[165,492]},'hall':{'point':[862,430],'approach':[862,480]},'bridge':{'point':[704,610],'approach':[640,610]}}
bundle={'schema':'generate2dmap.map_bundle.v2','id':'gwanghwamun-review','name':'Ginkgo Commons — Gwanghwamun Plaza art proof','tile_size':[32,32],'world':{'width':1024,'height':768,'unit':'px'},'tilesets':[{'id':'town','manifest':'tileset.json'}],'layers':[{'name':'Ground','kind':'tiles','data':'layers/ground.json','tileset':'town'},{'name':'Edging','kind':'tiles','data':'layers/edging.json','tileset':'town'},{'name':'Props','kind':'objects'}],'props':props,'objects':objects,'collision':{'actorRadius':8,'ySquash':0.5,'walkRegions':[{'polygon':[[32,32],[992,32],[992,736],[32,736]]}],'solids':[{'shape':'rect','x':672,'y':416,'w':64,'h':166},{'shape':'rect','x':672,'y':626,'w':64,'h':110}],'rects':[]},'nav':{'cell':4},'spawns':[{'id':'start','x':512,'y':600,'facing':'south'}],'anchors':anchors,'interactions':[{'id':k,'x':v['point'][0],'y':v['point'][1],'reach':100} for k,v in anchors.items()],'portals':[],'camera':{'tiltDeg':50,'pixelToWorld':1,'bounds':[0,0,1024,768]},'art_source':'host_image'}
write(S/'map-draft.json',bundle)
hashed = S/f'map-hashed-{sha(S/"map-draft.json")[:12]}.json'
if not hashed.exists(): run(M/'map_bundle.py','hash','--bundle',S/'map-draft.json','--output',hashed)
shutil.copyfile(hashed,S/'map-bundle.json')
hashed.unlink()  # Only this script's temporary duplicate; canonical bundle retained.
run(M/'map_bundle.py','validate','--bundle',S/'map-bundle.json','--report',C/f'bundle-qa-{sha(S/"map-bundle.json")[:12]}-{len(LOG)}.json')
if not (S/'navigation').exists(): run(M/'map_nav.py','check','--bundle',S/'map-bundle.json','--output-dir',S/'navigation','--publish-on-fail')
if not (S/'tiled').exists(): run(M/'export_tiled.py','export','--bundle',S/'map-bundle.json','--output-dir',S/'tiled','--embedded-variant')
for report in [S/'navigation/nav-report.json',S/'tiled/export-report.json']:
    assert json.loads(report.read_text())['inputs'][0]['sha256']==sha(S/'map-bundle.json'), 'Stale derived Forge export: retain existing output in .cache, then rerun this authorized source-processing command.'
write(C/'build-commands.json',LOG)
print('Layered review source assembled; runtime adapter is separate, no production assets replaced.')
