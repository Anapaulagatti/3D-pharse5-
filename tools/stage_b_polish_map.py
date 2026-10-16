"""Material/placement authoring DATA using generated RGB; never paint replacement art."""
from pathlib import Path
import json, hashlib
import numpy as np
from scipy.ndimage import distance_transform_edt, gaussian_filter
from PIL import Image, ImageDraw
R=Path(__file__).resolve().parents[1];P=R/'assets-src/stage-b-polish'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def courtyard_materials(material,z):
    """Keep approved courts/roads; their material and existing doorway connectors only."""
    d=ImageDraw.Draw(material)
    for court in z['courts']:
        if court['belongsTo'] in ['workshop','museum']:
            d.polygon([tuple(p)for p in court['polygon']],fill=3 if court['belongsTo']=='workshop' else 4)
    # Ground under each existing foundation uses that landmark's own material.
    for building in z['buildings']:
        if building['id'] in ['gate','academy','workshop','museum']:
            value={'gate':1,'academy':2,'workshop':3,'museum':4}[building['id']]
            for mass in building['masses']:
                x,y,w,h=mass['bounds'];d.rectangle((x,y,x+w,y+h),fill=value)
    # Short existing step-to-court aprons, not new streets or altered footprints.
    d.rectangle((448,768,896,800),fill=2)
    d.rectangle((3104,640,3392,672),fill=3)
    d.rectangle((3328,1248,3776,1280),fill=4)
    # Existing original door / approach pairs need continuous worn thresholds.
    d.line([(3168,1064),(3168,1184)],fill=3,width=64)
    d.line([(3552,1248),(3552,1392)],fill=4,width=64)
    d.line([(672,764),(672,1168)],fill=1,width=48)
    # Observational instrument platform already reserved in the approved plan.
    d.rectangle((3600,688,3760,832),fill=4)
    material.save(P/'semantic-materials.png')

def decorate(bundle,place,solid):
    for p in json.loads((P/'props.json').read_text()):
        bundle['props'][p['id']]={'image':'../stage-b-polish/'+p['image'],'sha256':p['sha256'],'anchor_px':p['anchor'],'size':p['size'],'footprint':{'shape':'rect','width':24,'depth':16,'offset':[0,-8],'basis':'world_px'},'solid':False,'occlusion_class':'tall','occupant_policy':'y_sort'}
    placements=[
        ('polish-folio',824,940,70,24,'Academy: hanji stitched primers and brush cup; peer study beside main circulation'),
        ('polish-bamboo',480,1080,36,18,'Academy: celadon bamboo planter, quiet scholar-garden side edge'),
        ('polish-flowers',848,1080,32,16,'Academy: chrysanthemum beside reading bench, off central entry'),
        ('polish-tools',3100,804,64,22,'Workshop: calipers, mallet and wood blanks at service edge'),
        ('polish-chart',3592,948,70,24,'Workshop: star diagram beside celestial observation platform'),
        ('polish-bamboo',3072,904,36,18,'Workshop: contained planting beside west service edge'),
        ('polish-stele',3824,1352,38,22,'Museum: turtle-ship emblem stele at terrace edge; no fabricated historical text'),
        ('polish-flowers',3280,1440,32,16,'Museum: cobalt chrysanthemum pot at quiet west terrace edge'),
        ('polish-flowers',1816,816,32,16,'Gateway: ceremonial chrysanthemum accent outside clear approach'),
        ('polish-flowers',2280,816,32,16,'Gateway: companion accent, central avenue remains open')]
    rows=[]
    for name,x,y,w,h,purpose in placements:
        place(name,x,y,purpose);solid(x-w/2,y-h,w,h,purpose)
        rows.append(dict(prop=name,x=x,y=y,footprint=[x-w/2,y-h,w,h],purpose=purpose))
    (P/'placements.json').write_text(json.dumps(rows,indent=2)+'\n')

def terrain_layers(material,old_tiles,register):
    """Texture-backed binary material boundaries; no blur, no invented RGB.

    Signed-distance coverage is editable map geometry. Small irregular clusters
    come from the actual generated earth image, at a fixed 2px grid. Stone paths
    retain their full approved clear width, with worn joints and earth shoulders.
    """
    a=np.array(material);h,w=a.shape;yy,xx=np.indices((h,w),dtype=np.int32)
    def repeat(im):
        q=np.array(im.convert('RGBA'));return q[yy%q.shape[0],xx%q.shape[1]]
    # Existing formal granite and grass remain pixel-exact in their interiors.
    grass=repeat(old_tiles[4]);stone=repeat(old_tiles[0])
    for row in range(h//32):
        for col in range(w//32):
            variation=(col*17+row*29+col*row)%2
            if variation:
                grass[row*32:row*32+32,col*32:col*32+32]=np.array(old_tiles[5])
                stone[row*32:row*32+32,col*32:col*32+32]=np.array(old_tiles[1])
    generated={}
    for val,name in [(2,'academy'),(3,'workshop'),(4,'museum')]:
        one=Image.open(P/f'terrain/{name}-1.png');two=Image.open(P/f'terrain/{name}-2.png')
        q=repeat(one);v=repeat(two);switch=((xx//128+yy//128)%2)==1;q[switch]=v[switch];generated[val]=q
    earth=generated[2]
    # Measured texture luminance supplies natural cluster variation, not RNG art.
    src=np.array(Image.open(P/'raw/terrain.png').convert('L').crop((0,0,512,512)).resize((256,256),Image.Resampling.BOX),dtype=np.float32)
    src=gaussian_filter(src,1.2);src=(src-src.mean())/max(1.,float(src.std()))
    cluster=src[(yy//2)%256,(xx//2)%256].clip(-1.8,1.8)
    out=grass.copy();inside=a>0;outer=distance_transform_edt(~inside)
    # Generated interwoven turf/soil, rather than a flat orange outline.
    verge=repeat(Image.open(P/'verge/soil-1.png'))
    turf=repeat(Image.open(P/'verge/turf-1.png'))
    apron=(~inside)&(outer<18+cluster*4)
    out[apron]=turf[apron]
    inner_apron=(~inside)&(outer<7+cluster*2)
    out[inner_apron]=verge[inner_apron]
    for val,texture in [(1,stone),*generated.items()]:
        mask=a==val;out[mask]=texture[mask]
    # A worn 4–8px earth reveal around stone/gray gravel edges. Never reduces
    # the authored road clear width: original road DATA includes 10px shoulders.
    dist=distance_transform_edt(inside)
    worn=inside&(dist<5+cluster*1.4)
    out[worn]=verge[worn]
    # Grass fingers on earth/soil edge, kept in the narrow border only.
    fringe=(~inside)&(outer>11+cluster*5)&(outer<26)
    out[fringe]=grass[fringe]
    # Same technique joins court materials to granite without abrupt rectangles.
    for val in [3,4]:
        mask=a==val
        inner=distance_transform_edt(mask)
        join=mask&(inner<3+cluster*1.2)&(~worn)
        out[join]=earth[join]
    out[:,:,3]=255
    Image.fromarray(out).save(P/'terrain-composite.png')
    Image.fromarray((apron|worn|fringe).astype('uint8')*255).save(P/'transition-coverage.png')
    # Keep layer ordering/runtime unchanged; generated material is composed into
    # ordinary reusable 32px cells (no background plate in Phaser).
    ground=[];edging=[]
    for row in range(h//32):
        gr=[];ed=[]
        for col in range(w//32):
            variation=(col*17+row*29+col*row)%2
            gr.append(register(old_tiles[4+variation]))
            rgb=out[row*32:row*32+32,col*32:col*32+32].copy()
            base=grass[row*32:row*32+32,col*32:col*32+32]
            if np.array_equal(rgb,base):ed.append(-1)
            else:
                rgb[:,:,3]=np.where(np.any(rgb[:,:,:3]!=base[:,:,:3],axis=2),255,0)
                ed.append(register(Image.fromarray(rgb)))
        ground.append(gr);edging.append(ed)
    report={'method':'Generated-RGB material composite and binary clustered edge masks; no code-painted texture, no alpha blur','apronPixels':int(apron.sum()),'transitionPixels':int((apron|worn|fringe).sum()),'maxApronPx':26,'roadDataAndBuildingCoordinatesChanged':False,'seamlessWangCertified':False,'sourceTileSize':128,'runtimeTileSize':32,'sourceSha256':sha(P/'raw/terrain.png'),'vergeSha256':sha(P/'raw/verge.png')}
    (P/'terrain-report.json').write_text(json.dumps(report,indent=2)+'\n')
    return ground,edging
