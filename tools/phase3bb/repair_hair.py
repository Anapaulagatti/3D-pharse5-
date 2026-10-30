"""Additive native cosmetic finishing. Never exports a base atlas or overwrites old patches.
Uses the existing sparse paint/erase contract, integer pixels, binary ownership.
"""
import sys,json,hashlib,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'phase2c'))
from core import load,decode,apply,R
from designs import registration,viewof,HAIR_PALETTES
D=R/'docs/phase3bb-hotfix'; C=R/'assets-src/characters/phase2c/catalog.json'; cat=json.loads(C.read_text()); report=[]
head_ids={'kr-classic-bob':0,'kr-soft-waves':1,'kr-traditional-braid':2,'kr-layered-cut':3,'kr-high-ponytail':4,'kr-side-part':5}
accessories={'kr-hair-ornament','kr-fashion-cap','kr-garden-hat','ara-shell-barrette'}
def pack(item,id,patches,old,frames):
 out=R/'public/assets/cosmetics/phase3bb'/item/id; assert not out.exists(),'Do not overwrite candidate';out.mkdir(parents=True)
 bbs={k:Image.fromarray(((np.array(p)[:,:,3]>0)|(np.array(e)[:,:,3]>0)).astype('uint8')*255).getbbox() for k,(p,e) in patches.items()}
 w=max(b[2]-b[0]for b in bbs.values()if b);h=max(b[3]-b[1]for b in bbs.values()if b);paint=Image.new('RGBA',(w*12,h*math.ceil(len(patches)/12)));erase=Image.new('RGBA',paint.size);mapping={}
 for i,(k,(p,e))in enumerate(patches.items()):
  b=bbs[k]
  if not b:mapping[k]=None;continue
  x=i%12*w;y=i//12*h;paint.paste(p.crop(b),(x,y));erase.paste(e.crop(b),(x,y));mapping[k]={'x':x,'y':y,'w':b[2]-b[0],'h':b[3]-b[1],'offsetX':b[0],'offsetY':b[1]}
 paint.save(out/'paint.png');erase.save(out/'erase.png');apply(frames['idle-front-0'],patches['idle-front-0']).save(out/'preview-native.png')
 (out/'mapping.json').write_text(json.dumps({'schemaVersion':1,'characterId':id,'baseAtlasSHA256':old['baseAtlasSHA256'],'frames':mapping},indent=2)+'\n')
 (out/'provenance.json').write_text(json.dumps({'itemId':item,'characterId':id,'source':'tools/phase3bb/repair_hair.py; existing native Phase2C patch, own-pose attachment and localized cluster/ownership finishing','previousVariant':old,'noImageGeneration':True,'native':[96,112],'anchor':[48,100],'artApproval':'PENDING_OWNER_REVIEW','preservation':'Old paint/erase/maps and all character atlases unchanged'},indent=2)+'\n')
 v=dict(old);root=str(out.relative_to(R/'public'))
 for key,file in [('paint','paint.png'),('erase','erase.png'),('mapping','mapping.json'),('preview','preview-native.png'),('provenance','provenance.json')]:v[key]=root+'/'+file
 v['assetRevision']=''.join(hashlib.sha256((out/f).read_bytes()).hexdigest()[:12]for f in ['paint.png','erase.png','mapping.json']);return v
for item in cat['items']:
 if item['id'] not in head_ids and item['id']not in accessories:continue
 for j,old in enumerate(item['variants']):
  id=old['characterId'];frames=load(id);patches=decode(old);changed=[]
  for name,(p,e)in patches.items():
   original_p=p.tobytes();original_e=e.tobytes();base=frames[name];v=viewof(name,base,frames);dx,dy=registration(base,frames['idle-'+v+'-0']);a=np.array(p);ea=np.array(e);ba=np.array(base)
   if item['id']in head_ids:
    style=head_ids[item['id']];pal=HAIR_PALETTES[style]; yy,xx=np.indices((112,96));mask=a[:,:,3]>0
    # Replace single-pixel speckle with deliberately continuous native strands.
    # Keep original outline clusters and the authored silhouette; no filtering.
    edge=np.zeros_like(mask)
    for oy,ox in [(-1,0),(1,0),(0,-1),(0,1)]:edge|=mask&~np.roll(mask,(oy,ox),(0,1))
    x=xx-dx;y=yy-dy;shade=np.clip(np.floor(5-((x-42)/13)**2-(y-28)/9),1,5).astype(int)
    ribbon=((x+(y-25)//7+style)%7==0)&(y>26)&(y<44);shade=np.clip(shade+ribbon,1,6);shade[edge]=0
    for n,c in enumerate(pal):a[mask&(shade==n),:3]=c
    # A bob/wavy back needs a continuous nape, not a rectangular transparent bite.
    if v=='back' and style in [0,1]:
     for row in range(37+dy,45+dy):
      cols=np.where(mask[row])[0]
      if len(cols)>1:
       for col in range(cols.min(),cols.max()+1):
        if not mask[row,col]:a[row,col]=[*pal[2 if row<43+dy else 1],255]
   elif item['id']in ['kr-fashion-cap','kr-garden-hat']:
    # Historical rectangular erase removed scalp around, rather than beneath,
    # the actual hat. Restrict ownership to its native painted contour.
    owned=a[:,:,3]>0;expanded=owned.copy()
    for oy,ox in [(-1,0),(1,0),(0,-1),(0,1)]:expanded|=np.roll(owned,(oy,ox),(0,1))
    ea[~expanded]=0
   elif item['id']=='kr-hair-ornament':
    # Compact asymmetric silk knot, four authored placements. Do not float
    # above the temple or erase approved hair/skin.
    p=Image.new('RGBA',(96,112));draw=ImageDraw.Draw(p);x,y={'front':(59,29),'back':(39,31),'left':(54,30),'right':(39,30)}[v];x+=dx;y+=dy
    draw.polygon([(x-3,y-1),(x,y),(x-3,y+2),(x-4,y)],fill=(148,53,65,255));draw.polygon([(x,y),(x+3,y-2),(x+4,y),(x+2,y+2)],fill=(188,76,85,255));draw.point((x,y),fill=(235,190,113,255));draw.point((x-2,y),fill=(211,107,106,255));a=np.array(p);ea[:]=0
   else:
    # Existing shell pixels are preserved; remove detached isolated pixels.
    occupied=a[:,:,3]>0;near=np.zeros_like(occupied)
    for oy,ox in [(-1,0),(1,0),(0,-1),(0,1)]:near|=np.roll(occupied,(oy,ox),(0,1))
    a[occupied&~near]=0
   # Face/hand silhouette is always in front of headwear (palette from this
   # frame, not a reference-alpha subtraction that can erase moving hair).
   if item['id'] in head_ids or item['id']=='kr-hair-ornament':
    yy,xx=np.indices((112,96));skin=(ba[:,:,3]>0)&(ba[:,:,0]>100)&(ba[:,:,0].astype(int)-ba[:,:,1]>24)&(ba[:,:,1].astype(int)-ba[:,:,2]>12)&(yy>=33+dy)&(yy<47+dy)
    face=(xx>=40+dx)&(xx<=56+dx)
    if v=='back':skin&=yy>=43+dy
    else:skin&=face
    a[skin]=0;ea[skin]=0
   new=(Image.fromarray(a),Image.fromarray(ea));
   if original_p!=new[0].tobytes()or original_e!=new[1].tobytes():changed.append(name)
   patches[name]=new
  item['variants'][j]=pack(item['id'],id,patches,old,frames);report.append({'item':item['id'],'character':id,'frames':len(patches),'changed':len(changed),'oldPreserved':True})
C.write_text(json.dumps(cat,ensure_ascii=False,indent=2)+'\n');(D/'HAIR_REPAIR.json').write_text(json.dumps({'variants':report,'originalsOverwritten':False,'humanArtApproval':'PENDING','nativeSampling':'1:1; integer/binary alpha; no interpolation'},indent=2)+'\n');print('Additive head patches',len(report))
