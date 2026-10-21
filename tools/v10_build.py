"""Compile explicitly requested graybox data, never final art, from V10 + protected north."""
import hashlib
import json
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageFilter
from v10_plan import sample_points

R=Path(__file__).resolve().parents[1]
S=R/'assets-src/v10-city'; M=S/'map'; P=R/'public/assets/v10-city'; D=R/'docs/v10-city'
read=lambda p:json.loads(p.read_text())
def write(p,v):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def font(n):return ImageFont.truetype(FONT,n)
COL={'primary':'#c5d0d6','street':'#ccd3d3','lane':'#e0d6c6','promenade':'#bccdcd','park':'#d4d4bd','pier':'#c8d3da','island':'#d6d5c4'}
ZONES={'commons':'#799caa','transit':'#7e94b3','namsan':'#80a494','entertainment':'#ab8d9c','busan-coast':'#789f9d','jeju':'#a59d7c'}

def build():
    for p in [M,P,D]:p.mkdir(parents=True,exist_ok=True)
    plan=read(S/'plan/city.json'); w,h=plan['world']; north=read(R/'assets-src/protected-north/district.json'); lib=read(R/'assets-src/library/props.json')
    ground=Image.new('RGB',(w,h),'#7c9da8');g=ImageDraw.Draw(ground)
    g.polygon(plan['mainland'],fill='#7e9186');g.polygon(plan['island'],fill='#8e9b8b')
    land=Image.new('1',(w,h));ld=ImageDraw.Draw(land);ld.polygon(plan['mainland'],fill=1);ld.polygon(plan['island'],fill=1)
    g.polygon([(200,2560),(640,2336),(1056,2432),(1352,2784),(1280,3192),(992,3440),(512,3440),(160,3120)],fill='#6f8779')
    paving=Image.new('L',(w,h));pd=ImageDraw.Draw(paving)
    for p in plan['roads']:
        pts=sample_points(p); width=p['width']
        pd.line(pts,fill=255,width=width,joint='curve')
        ld.line(pts,fill=1,width=width,joint='curve')
        for x,y in [pts[0],pts[-1]]:
            pd.ellipse((x-width/2,y-width/2,x+width/2,y+width/2),fill=255);ld.ellipse((x-width/2,y-width/2,x+width/2,y+width/2),fill=1)
    # Union public surfaces before edging: intersections have no internal curbs/caps.
    ground.paste('#596e6c',(0,0,w,h),paving.filter(ImageFilter.MaxFilter(13)))
    ground.paste('#cbd3d2',(0,0,w,h),paving)
    for road in plan['roads']:
        if road['kind'] in ['park','island','pier','lane']:
            g.line(sample_points(road),fill=COL[road['kind']],width=road['width'],joint='curve')
    cx,cy,cw,ch=plan['civicCourt'];g.rectangle((cx,cy,cx+cw,cy+ch),fill='#d9d8cd')
    # Seating/planting reservations are diagram geometry, not production props.
    g.rectangle((cx+176,cy+80,cx+352,cy+160),fill='#8eaa96')
    # Railway is adjacent to the east high street, with a protected crossing at book lane.
    g.rectangle((3280,2424,4240,2472),fill='#566d75')
    for x in range(3280,4240,32):g.line((x,2424,x,2472),fill='#91a3a8',width=4)
    g.rectangle((3424,2424,3488,2472),fill='#e1dcc4')
    g.rectangle((3520,2472,4192,2504),fill='#a7b8be')
    # Arcade cannot walk over open sea; merge equal runs into exact 32px rectangles.
    solids=list(north['solids']);water=[]
    for ty in range(2240//32,h//32):
        start=None
        for tx in range(w//32+1):
            blocked=tx<w//32 and not land.getpixel((tx*32+16,ty*32+16))
            if blocked and start is None:start=tx
            if not blocked and start is not None:
                water.append(dict(shape='rect',x=start*32,y=ty*32,w=(tx-start)*32,h=32,reason='V10 sea boundary'));start=None
    solids+=water
    solids += [dict(shape='rect',x=x,y=2424,w=ww,h=48,reason='V10 track, signed crossing gap')for x,ww in [(3280,144),(3488,752)]]
    objects=json.loads(json.dumps(north['objects']));props={};anchors={}
    for obj in objects:
        if 'occluder' in obj:obj['occluder']['source']=obj['prop']+'.png'
    for key in sorted({o['prop']for o in objects}):
        spec=dict(lib[key]);src=R/'assets-src/library'/spec['image'];dst=M/(key+'.png');shutil.copyfile(src,dst);shutil.copyfile(src,P/(key+'.png'))
        spec['image']=key+'.png';spec['solid']=False;props[key]=spec;anchors[key]=spec['anchor_px']
    for lot in plan['plots']:
        x,y,pw,ph=lot['rect'];height=lot['height'];kind='v10-gray-'+lot['id'];color=ZONES[lot['district']]
        im=Image.new('RGBA',(pw,ph+height));q=ImageDraw.Draw(im)
        q.rectangle((0,ph,pw-1,ph+height-1),fill=color,outline='#364c58',width=3)
        q.rectangle((0,0,pw-1,ph-1),fill='#b7c4c6',outline='#425c67',width=3)
        q.line((0,ph,pw,ph),fill='#334d5b',width=4)
        # Clear placeholder ID, not mock final facades.
        q.text((10,12),lot['id'],font=font(20),fill='#223d4b')
        q.text((10,40),lot['label'].replace(' ','\n'),font=font(14),fill='#223d4b')
        if lot['facing']=='south':q.rectangle((pw//2-16,ph+height-20,pw//2+16,ph+height-1),fill='#f5f0dc')
        elif lot['facing']=='north':q.rectangle((pw//2-16,0,pw//2+16,16),fill='#f5f0dc')
        else:q.rectangle((0,ph+height//2-16,16,ph+height//2+16),fill='#f5f0dc')
        im.save(M/(kind+'.png'));im.save(P/(kind+'.png'))
        props[kind]=dict(image=kind+'.png',size=list(im.size),anchor_px=[pw//2,ph+height],solid=False,art_source='code')
        anchors[kind]=props[kind]['anchor_px'];objects.append(dict(id=lot['id'],prop=kind,x=x+pw//2,y=y+ph,sortY=y+ph,scale=1,anchor_px=anchors[kind]))
        solids.append(dict(shape='rect',x=x,y=y,w=pw,h=ph,reason='V10 lot '+lot['id']))
        dx,dy=lot['door'];g.ellipse((dx-12,dy-12,dx+12,dy+12),fill='#f9f0bd')
        if lot['district']=='commons' and lot['id']!='civic-house':
            g.line([(dx,dy),(dx,2960)],fill='#d7d6c9',width=64)
        # Short forecourts make the setback readable without lawns.
        if lot['facing']=='south':g.rectangle((dx-32,y+ph,dx+32,dy+16),fill='#d7d6c9')
        elif lot['facing']=='north':g.rectangle((dx-32,dy-16,dx+32,y),fill='#d7d6c9')
        else:g.rectangle((dx-16,dy-32,x,dy+32),fill='#d7d6c9')
    # Exact native north pixels overwrite any new line above the fixed boundary.
    original=Image.open(R/'assets-src/protected-north/ground-native.png').convert('RGB');ground.paste(original,(0,0))
    assert ImageChops.difference(original,ground.crop((0,0,4352,2240))).getbbox() is None
    ground.save(M/'ground-native.png');land.save(M/'land-mask.png')
    # Lossless exact tile dictionary; no screenshot or legacy atlas input.
    tiles=[];lookup={};data=[]
    for y in range(0,h,32):
        for x in range(0,w,32):
            tile=ground.crop((x,y,x+32,y+32));raw=tile.tobytes()
            if raw not in lookup:lookup[raw]=len(tiles)+1;tiles.append(tile)
            data.append(lookup[raw])
    atlas=Image.new('RGB',(4096,((len(tiles)+127)//128)*32))
    for i,t in enumerate(tiles):atlas.paste(t,((i%128)*32,(i//128)*32))
    atlas.save(M/'tiles.png');shutil.copyfile(M/'tiles.png',P/'tiles.png')
    tm=dict(type='map',version='1.10',orientation='orthogonal',renderorder='right-down',width=w//32,height=h//32,tilewidth=32,tileheight=32,infinite=False,
      layers=[dict(id=1,name='Ground',type='tilelayer',width=w//32,height=h//32,data=data,opacity=1,visible=True,x=0,y=0),dict(id=2,name='Edging',type='tilelayer',width=w//32,height=h//32,data=[0]*len(data),opacity=1,visible=True,x=0,y=0),dict(id=3,name='Collision',type='objectgroup',objects=[dict(id=i+1,x=s['x'],y=s['y'],width=s['w'],height=s['h'],rotation=0,type='',name=s.get('reason','north'),visible=True)for i,s in enumerate(solids)])],
      tilesets=[dict(firstgid=1,name='town',image='tiles.png',imagewidth=atlas.width,imageheight=atlas.height,columns=128,tilecount=len(tiles),tilewidth=32,tileheight=32,spacing=0,margin=0)])
    write(P/'plaza.json',tm);write(M/'plaza.tmj',tm);write(P/'anchors.json',anchors)
    # WorldData adapter keeps the original physics and native prop registrations.
    world=dict(width=w,height=h,spawn=[2176,832],npc=[0,0],follow=48,role='student',mood='neutral',vi='V10 graybox',mapSha256=sha(S/'plan/city.json'),objects=[dict(id=i,kind=o['prop'],x=o['x'],y=o['y'],sortY=o['sortY'],width=props[o['prop']].get('footprint',{}).get('width',24),height=props[o['prop']].get('footprint',{}).get('depth',16),label=o['id'],collide=False)for i,o in enumerate(objects)])
    targets={s['id']:dict(point=s['point'],approach=s['point'])for s in plan['reviewStops']}
    targets.update({p['id']+'-door':dict(point=p['door'],approach=p['door'])for p in plan['plots']})
    bundle=dict(schema='generate2dmap.map_bundle.v2',id='v10-city',world=dict(width=w,height=h,unit='px'),layers=[dict(name='graybox-ground',kind='image',image='ground-native.png',x=0,y=0),dict(name='buildings',kind='objects')],art_source='mixed',props=props,objects=objects,collision=dict(actorRadius=8,ySquash=0.5,solids=solids),spawns=[dict(id='start',x=2176,y=832,facing='south'),dict(id='jeju-arrival',x=3296,y=5216,facing='south')],anchors=targets)
    write(M/'world.json',world);write(M/'bundle.json',bundle)
    for name in ['regions','travel']:write(S/(name+'.json'),plan[name])
    write(S/'water.json',dict(frames=[],periodMs=1200))
    stops=list(north['stops'])+[dict(id=p['id'],x=p['door'][0],y=p['door'][1],text='GRAYBOX · '+p['label']+'. Bố cục đang chờ duyệt; đây chưa phải artwork hoàn chỉnh.')for p in plan['plots']]
    write(S/'stops.json',stops)
    mini=ground.copy()
    for o in objects:
        prop=props[o['prop']];im=Image.open(M/prop['image']).convert('RGBA');mini.paste(im,(round(o['x']-prop['anchor_px'][0]),round(o['y']-prop['anchor_px'][1])),im)
    mini.resize((544,736),Image.Resampling.NEAREST).save(P/'minimap.png')
    write(S/'build-provenance.json',dict(source='new V10 literal plan + protected-north + north-only native library',planSha256=sha(S/'plan/city.json'),atlasSha256=sha(M/'tiles.png'),northGroundExact=True,northObjects=len(north['objects']),tiles=len(tiles),runtimeRoot='assets/v10-city/',finalArt=False))
    print(json.dumps(dict(status='BUILT_GRAYBOX',tiles=len(tiles),northObjects=len(north['objects']),newLots=len(plan['plots']),colliders=len(solids))))

if __name__=='__main__':build()
