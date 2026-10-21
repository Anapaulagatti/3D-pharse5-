"""Process ONLY new V10 host-image originals. No rejected-south inputs."""
import json,hashlib,math,subprocess,sys
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np
R=Path(__file__).resolve().parents[1];S=R/'assets-src/v10-city';C=R/'.cache/v10-production';F=Path('/workspace/tooling-cache/agent-sprite-forge/skills');N=S/'native';N.mkdir(exist_ok=True)
LOG=json.loads((S/'art-processing-log.json').read_text())if(S/'art-processing-log.json').exists()else[];PROOF={}
def run(tool,*args):
    cmd=[sys.executable,str(F/tool),*map(str,args)];p=subprocess.run(cmd,cwd=R,capture_output=True,text=True)
    LOG.append(dict(command=cmd,exit=p.returncode,stdout=p.stdout,stderr=p.stderr));(S/'art-processing-log.json').write_text(json.dumps(LOG,indent=2)+'\n')
    if p.returncode:raise RuntimeError(p.stderr or p.stdout)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def gutter(values,target,limit):
    """Measure genuine empty-alpha gutters; never cut through an authored subject."""
    if target<=0 or target>=len(values):return target
    z=np.flatnonzero(values==0);groups=np.split(z,np.where(np.diff(z)>1)[0]+1)
    candidates=[int((a[0]+a[-1])//2)for a in groups if len(a)>=4 and abs((a[0]+a[-1])/2-target)<limit]
    return min(candidates,key=lambda n:abs(n-target))if candidates else target
def cells(sheet,rows):
    """Measured non-overlapping regions. Fractions are source-canvas coordinates."""
    im=Image.open(S/'originals'/f'{sheet}.png').convert('RGBA');w,h=im.size;result=[]
    for label,box in rows:
        x0,y0,x1,y1=[round(v*(w if i%2==0 else h))for i,v in enumerate(box)]
        opaque=np.array(im.getchannel('A'))>=128
        counts=opaque[y0:y1].sum(axis=0);x0=gutter(counts,x0,w*.08);x1=gutter(counts,x1,w*.08)
        counts=opaque[:,x0:x1].sum(axis=1);y0=gutter(counts,y0,h*.08);y1=gutter(counts,y1,h*.08)
        cell=im.crop((x0,y0,x1,y1));a=np.array(cell);a[:,:,3]=np.where(a[:,:,3]>=128,255,0)
        border=int(np.count_nonzero(a[0,:,3])+np.count_nonzero(a[-1,:,3])+np.count_nonzero(a[:,0,3])+np.count_nonzero(a[:,-1,3]))
        if border:raise RuntimeError(f'Clipped measured source {sheet}/{label}: {border} border pixels; adjust box or reject source')
        result.append((label,Image.fromarray(a)))
        PROOF[label]=dict(original=f'originals/{sheet}.png',originalSha256=sha(S/'originals'/f'{sheet}.png'),sourceBox=[x0,y0,x1,y1],alphaThreshold=128,sourceBorderPixels=border,art_source='host_image')
    cw=max(im.width for _,im in result)+64;ch=max(im.height for _,im in result)+64
    cols=min(4,len(result));rows=math.ceil(len(result)/cols);pack=Image.new('RGBA',(cw*cols,ch*rows))
    for i,(_,im)in enumerate(result):pack.paste(im,((i%cols)*cw+32,(i//cols)*ch+32))
    target=C/(sheet+'-padded.png');pack.save(target);out=C/(sheet+'-extract-'+sha(target)[:12])
    labels=[l for l,_ in result]+['-'for _ in range(rows*cols-len(result))]
    if not (out/'prop-pack.json').exists():
        run(Path('generate2dmap/scripts/extract_prop_pack.py'),'--input',target,'--rows',rows,'--cols',cols,'--labels',','.join(labels),'--background-mode','native_alpha','--component-mode','all','--min-component-area','1','--component-padding','8','--reject-edge-touch','--max-dropped-fraction','0.01','--art-source','host_image','--output-dir',out)
    manifest=json.loads((out/'prop-pack.json').read_text())
    assert manifest['source_sha256']==sha(target),'Stale extraction cache'
    for item in manifest['accepted']:PROOF[item['label']]['extracted']=str(out/item['image']);PROOF[item['label']]['extractionManifest']=str((out/'prop-pack.json').relative_to(R))

def grid(labels,cols,cut=0.5):
    return [(l,[(i%cols)/cols,0 if i<cols else cut,(i%cols+1)/cols,cut if i<cols else 1])for i,l in enumerate(labels)]
def process():
    C.mkdir(exist_ok=True,parents=True)
    cells('shops-six',grid(['bookstore','cafe','language','grocery','design','bakery'],3,500/1024))
    cells('north-frontages-corrected',grid(['north-book','north-cafe','north-design'],3,0.49)[:3]+[('north-bakery',[0,.49,.322,1]),('community',[.322,.49,.79,1]),('kiosk',[.79,.49,1,1])])
    cells('transit',[('station',[0,0,2/3,0.49]),('station-book',[2/3,0,1,0.50]),('fish-market',[0,0.49,0.585,1]),('sea-cafe',[0.585,0.50,1,1])])
    cells('landmarks',grid(['tower','wheel','carousel'],3,0.586)[:3]+[('pavilion',[0,.586,.4167,1]),('terminal',[.4167,.586,.802,1]),('ferry',[.802,.586,1,1])])
    cells('island',[('jeju-hall',[0,0,.355,.51]),('jeju-tea',[.355,0,.70,.51]),('oreum',[.70,0,1,.51]),('tangerine',[0,.51,.307,1]),('basalt-wall',[.307,.51,.70,1]),('view-deck',[.70,.51,1,1])])
    # Edge-clipped ornamental tree/cliff cells are NOT adopted from this sheet.
    cells('nature-corrected',grid(['deciduous','pine','cherry','flowerbed'],2,.5))
    cells('furniture',[('bench',[0,.39,.29,.675]),('lamp',[.29,.39,.515,.675]),('bikes',[.515,.39,.77,.675]),('bollards',[.77,.39,1,.675]),('planter',[0,.675,.245,1]),('rail',[.245,.675,.50,1])])
    cells('infrastructure',[('train',[0,0,.4167,.50]),('pergola',[.4167,0,.6667,.50]),('campus-gate',[.6667,0,1,.50]),('rail-vertical',[0,.50,.25,1]),('stairs',[.25,.50,.6667,1]),('queue',[.6667,.50,1,1])])
    binding={'N1':'bookstore','N2':'cafe','N3':'language','N4':'grocery','N5':'design','N6':'bakery','S1':'north-book','S2':'north-cafe','S5':'north-design','S6':'north-bakery','civic-house':'community','station':'station','station-kiosk':'kiosk','station-book':'station-book','coast-1':'fish-market','coast-2':'sea-cafe','terminal':'terminal','tower':'tower','wheel':'wheel','carousel':'carousel','pavilion':'pavilion','jeju-hall':'jeju-hall','jeju-tea':'jeju-tea'}
    plan=json.loads((S/'plan/city.json').read_text());sizes={p['id']:(p['rect'][2],p['rect'][3]+p['height'])for p in plan['plots']}
    extras={'ferry':(112,224),'deciduous':(176,200),'pine':(176,200),'cherry':(160,180),'flowerbed':(112,52),'bench':(96,48),'lamp':(40,128),'bikes':(96,72),'bollards':(64,56),'planter':(96,72),'rail':(128,56),'rail-vertical':(48,128),'campus-gate':(224,200),'stairs':(128,64),'queue':(96,64),'pergola':(160,140),'train':(608,112),'oreum':(256,224),'tangerine':(128,176),'basalt-wall':(160,64),'view-deck':(176,128)}
    specs=[(id,source,sizes[id],next(p for p in plan['plots']if p['id']==id)['facing'])for id,source in binding.items()]+[(id,id,size,'south')for id,size in extras.items()]
    for id,source,(w,h),face in specs:
        im=Image.open(PROOF[source]['extracted']).convert('RGBA');bbox=im.getchannel('A').getbbox();im=im.crop(bbox)
        k=min((w-4)/im.width,(h-4)/im.height);size=(max(1,round(im.width*k)),max(1,round(im.height*k)))
        # Premultiplied area reduction, then palette/binary-alpha pixel finish.
        im=im.convert('RGBa').resize(size,Image.Resampling.BOX).convert('RGBA');a=np.asarray(im.getchannel('A'));rgb=im.convert('RGB').quantize(colors=128,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGBA');rgb.putalpha(Image.fromarray(np.where(a>=128,255,0).astype('uint8')))
        frame=Image.new('RGBA',(w,h));frame.paste(rgb,((w-size[0])//2,2 if face=='north' else h-size[1]-2))
        frame.save(N/(id+'.png'));PROOF[id+'-native']=dict(source=source,art_source='host_image',size=[w,h],uniformScale=k,alignment='north/top'if face=='north'else'south/bottom',sha256=sha(N/(id+'.png')),image='native/'+id+'.png')
    # Reformat 16 newly painted swatches, retaining source-coordinate provenance.
    src=Image.open(S/'originals/materials.png').convert('RGB');strip=Image.new('RGB',(256,4096));labels=['asphalt','sidewalk','civic','brick','granite','gravel','basalt','leisure','coastal','timber','sea','shallows','grass','soil','meadow','masonry']
    for i,label in enumerate(labels):
        box=[round((i%4)*src.width/4),round((i//4)*src.height/4),round((i%4+1)*src.width/4),round((i//4+1)*src.height/4)];strip.paste(src.crop(box).resize((256,256),Image.Resampling.BOX),(0,i*256));PROOF[label+'-material']=dict(original='originals/materials.png',sourceBox=box,art_source='host_image')
    strip.save(C/'materials-strip.png');args=['--input',C/'materials-strip.png','--rows','16','--cols','1','--tile-size','64','--resampler','lanczos','--edge-policy','isolated','--strict-qc','--output-dir',C/'materials-extracted']
    for i,label in enumerate(labels):args+=['--terrain-row',f'{label}={i}']
    run(Path('generate2dmap/scripts/extract_terrain_tiles.py'),*args)
    terrain=json.loads((C/'materials-extracted/terrain-bundle.json').read_text())
    # Stable native material copies are derived from recorded source cells, never old atlases.
    for i,label in enumerate(labels):
        tile=strip.crop((0,i*256,256,(i+1)*256)).resize((64,64),Image.Resampling.BOX).quantize(colors=64,dither=Image.Dither.NONE).convert('RGB');tile.save(N/(label+'-material.png'));PROOF[label+'-material']['sha256']=sha(N/(label+'-material.png'))
    (S/'art-provenance.json').write_text(json.dumps(PROOF,indent=2)+'\n')
    sheet=Image.new('RGB',(1024,math.ceil(len(specs)/6)*360),'#d8e0db');q=ImageDraw.Draw(sheet)
    for i,(id,*_)in enumerate(specs):
        im=Image.open(N/(id+'.png'));im.thumbnail((156,320),Image.Resampling.NEAREST);x=(i%6)*170+6;y=(i//6)*360+22;sheet.paste(im,(x,y),im);q.text((x,y-16),id,fill='#203849')
    sheet.save(R/'docs/v10-production/V10_SOURCE_ART_REVIEW.png');print('Native V10 art prepared',len(specs),'sprites;16materials')
if __name__=='__main__':process()
