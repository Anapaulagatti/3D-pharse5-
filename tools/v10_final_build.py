"""Compile original V10 image art on the immutable approved V10 plan; no legacy-south helpers."""
import hashlib
import json
import shutil
from pathlib import Path
from PIL import Image, ImageChops
from v10_surfaces import surfaces, decorations

R=Path(__file__).resolve().parents[1]
S=R/'assets-src/v10-city'; M=S/'map'; P=R/'public/assets/v10-city'; D=R/'docs/v10-production'
read=lambda p:json.loads(p.read_text())
def write(p,v):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def build():
    for p in [M,P,D]:p.mkdir(parents=True,exist_ok=True)
    plan=read(S/'plan/city.json'); w,h=plan['world']; north=read(R/'assets-src/protected-north/district.json'); lib=read(R/'assets-src/library/props.json')
    assert sha(S/'plan/city.json')=='808ca4aa56be22afb11b35f30cbe557a5a5915dce272af0e9465257032233cc0', 'Approved plan changed'
    ground,land=surfaces(plan)
    for folder in [M,P]:
        for old in folder.glob('v10-gray-*.png'):old.unlink()
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
        x,y,pw,ph=lot['rect'];kind='v10-'+lot['id'];src=S/'native'/(lot['id']+'.png');im=Image.open(src)
        assert im.size==(pw,ph+lot['height'])
        shutil.copyfile(src,M/(kind+'.png'));shutil.copyfile(src,P/(kind+'.png'))
        props[kind]=dict(image=kind+'.png',size=list(im.size),anchor_px=[pw//2,im.height],solid=False,art_source='host_image')
        anchors[kind]=props[kind]['anchor_px'];objects.append(dict(id=lot['id'],prop=kind,x=x+pw//2,y=y+ph,sortY=y+ph,scale=1,anchor_px=anchors[kind]))
        solids.append(dict(shape='rect',x=x,y=y,w=pw,h=ph,reason='V10 approved property mass '+lot['id']))
    details=decorations(plan);write(S/'production/decorations.json',details)
    for d in details:
        kind='v10-detail-'+d['asset'];src=S/'native'/(d['asset']+'.png');im=Image.open(src);anchor=d['anchor']or[im.width//2,im.height]
        if kind not in props:
            shutil.copyfile(src,M/(kind+'.png'));shutil.copyfile(src,P/(kind+'.png'))
            props[kind]=dict(image=kind+'.png',size=list(im.size),anchor_px=anchor,solid=False,art_source='host_image');anchors[kind]=anchor
        assert d['y']-anchor[1]>=2240,('New art above protected north',d)
        objects.append(dict(id=d['id'],prop=kind,x=d['x'],y=d['y'],sortY=d['y'],scale=1,anchor_px=anchor,purpose=d['purpose']))
        x,y=d['x'],d['y']
        if d['asset']in['pine','cherry','deciduous','tangerine']:solids.append(dict(shape='rect',x=x-8,y=y-10,w=16,h=10,reason='V10 new tree trunk'))
        elif d['asset']=='oreum':solids.append(dict(shape='rect',x=x-64,y=y-32,w=128,h=32,reason='V10 new oreum basalt body'))
        elif d['asset']in['bench','planter']:solids.append(dict(shape='rect',x=x-28,y=y-12,w=56,h=12,reason='V10 new street furnishing'))
        elif d['asset']=='basalt-wall':
            for xx in[x-76,x+32]:solids.append(dict(shape='rect',x=xx,y=y-8,w=44,h=8,reason='V10 new basalt wall; gateway clear'))
        elif d['asset']=='campus-gate':
            for yy in[y-172,y-40]:solids.append(dict(shape='rect',x=x-40,y=yy,w=80,h=36,reason='V10 new ticket pavilion; east-west passage clear'))
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
    world=dict(width=w,height=h,spawn=[2176,832],npc=[0,0],follow=48,role='student',mood='neutral',vi='V10 original Korean city',mapSha256=sha(S/'plan/city.json'),objects=[dict(id=i,kind=o['prop'],x=o['x'],y=o['y'],sortY=o['sortY'],width=props[o['prop']].get('footprint',{}).get('width',24),height=props[o['prop']].get('footprint',{}).get('depth',16),label=o['id'],collide=False)for i,o in enumerate(objects)])
    targets={s['id']:dict(point=s['point'],approach=s['point'])for s in plan['reviewStops']}
    targets.update({p['id']+'-door':dict(point=p['door'],approach=p['door'])for p in plan['plots']})
    bundle=dict(schema='generate2dmap.map_bundle.v2',id='v10-city',world=dict(width=w,height=h,unit='px'),layers=[dict(name='v10-original-image-ground',kind='image',image='ground-native.png',x=0,y=0),dict(name='buildings',kind='objects')],art_source='mixed',props=props,objects=objects,collision=dict(actorRadius=8,ySquash=0.5,solids=solids),spawns=[dict(id='start',x=2176,y=832,facing='south'),dict(id='jeju-arrival',x=3296,y=5216,facing='south')],anchors=targets)
    write(M/'world.json',world);write(M/'bundle.json',bundle)
    for name in ['regions','travel']:write(S/(name+'.json'),plan[name])
    write(S/'water.json',dict(frames=[],periodMs=1200))
    labels={'N1':'서점 · Hiệu sách cửa sổ xanh','N2':'카페 · Cà phê mái vườn','N3':'한글 · Không gian ngôn ngữ','N4':'식품 · Cửa hàng thực phẩm','N5':'공방 · Xưởng gốm và thiết kế','N6':'빵집 · Tiệm bánh phố Gyeol','S1':'책 · Sân đọc sách','S2':'차 · Cà phê sân kính','S5':'공예 · Xưởng sáng tạo','S6':'빵 · Nhà bánh vườn kính','station':'역 · Ga Gyeol','station-kiosk':'커피 · Cà phê nhà ga','station-book':'책 · Quầy sách và vé','civic-house':'마을 · Nhà cộng đồng','coast-1':'수산 · Chợ hải sản','coast-2':'바다 · Cà phê ven biển','terminal':'배 · Nhà ga hành khách','tower':'전망대 · Đài quan sát Namsan','wheel':'관람차 · Vòng quay nhìn biển','carousel':'회전목마 · Vòng ngựa gỗ','pavilion':'공연 · Sân khấu văn hóa','jeju-hall':'마을 · Nhà làng Jeju','jeju-tea':'차 · Nhà trà Jeju'}
    write(S/'production/venue-labels.json',labels)
    stops=list(north['stops'])+[dict(id=p['id'],x=p['door'][0],y=p['door'][1],text=labels[p['id']]+'. Khám phá từ trên biển hiệu và không gian quanh bạn. Đây là hành trình du lịch giáo dục hư cấu; các công trình là thiết kế nguyên bản.')for p in plan['plots']]
    write(S/'stops.json',stops)
    mini=ground.copy()
    for o in objects:
        prop=props[o['prop']];im=Image.open(M/prop['image']).convert('RGBA');mini.paste(im,(round(o['x']-prop['anchor_px'][0]),round(o['y']-prop['anchor_px'][1])),im)
    mini.resize((544,736),Image.Resampling.NEAREST).save(P/'minimap.png')
    write(S/'build-provenance.json',dict(source='approved V10 plan + new host-image originals/native artwork + protected-north only',planSha256=sha(S/'plan/city.json'),atlasSha256=sha(M/'tiles.png'),northGroundExact=True,northObjects=len(north['objects']),tiles=len(tiles),runtimeRoot='assets/v10-city/',finalArt=True))
    print(json.dumps(dict(status='BUILT_ORIGINAL_V10_ART',tiles=len(tiles),northObjects=len(north['objects']),newLots=len(plan['plots']),colliders=len(solids))))

if __name__=='__main__':build()
