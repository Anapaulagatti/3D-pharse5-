"""Sparse native patch ownership. Never writes a base atlas or historical source."""
from pathlib import Path
import json,hashlib,math
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[2];S=R/'assets-src/characters/phase2c';D=R/'docs/phase2c';P=R/'public/assets/cosmetics/phase2c';B=json.loads((S/'base-bindings.json').read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(id):
 stem='assets/juni/juni'if id=='juni'else f'assets/characters/{id}/atlas';atlas=Image.open(R/'public'/f'{stem}.png').convert('RGBA');meta=json.loads((R/'public'/f'{stem}.json').read_text())['frames'];out={}
 for k,v in meta.items():
  f=v['frame'];out[k]=atlas.crop((f['x'],f['y'],f['x']+96,f['y']+112))
 return out

def decode(v):
 m=json.loads((R/'public'/v['mapping']).read_text())['frames'];p=Image.open(R/'public'/v['paint']).convert('RGBA');e=Image.open(R/'public'/v['erase']).convert('RGBA');out={}
 for key,f in m.items():
  paint=Image.new('RGBA',(96,112));erase=Image.new('RGBA',(96,112))
  if f:
   box=(f['x'],f['y'],f['x']+f['w'],f['y']+f['h']);paint.paste(p.crop(box),(f['offsetX'],f['offsetY']));erase.paste(e.crop(box),(f['offsetX'],f['offsetY']))
  out[key]=(paint,erase)
 return out

def apply(im,patch):
 p,e=patch;a=np.array(im).copy();a[np.array(e)[:,:,3]>0]=0;q=Image.fromarray(a);q.alpha_composite(p);return q

def save(item,id,patches,preview,source):
 out=P/item/id;out.mkdir(parents=True,exist_ok=True);packed={};maxw=maxh=1
 for k,(p,e)in patches.items():
  mask=(np.array(p)[:,:,3]>0)|(np.array(e)[:,:,3]>0);bb=Image.fromarray(mask.astype('uint8')*255).getbbox()
  packed[k]=None if not bb else(bb,p.crop(bb),e.crop(bb))
  if bb:maxw=max(maxw,bb[2]-bb[0]);maxh=max(maxh,bb[3]-bb[1])
 paint=Image.new('RGBA',(maxw*12,maxh*math.ceil(len(packed)/12)));erase=Image.new('RGBA',paint.size);m={}
 for i,(k,v)in enumerate(packed.items()):
  if v is None:m[k]=None;continue
  bb,p,e=v;x=i%12*maxw;y=i//12*maxh;paint.paste(p,(x,y));erase.paste(e,(x,y));m[k]={'x':x,'y':y,'w':p.width,'h':p.height,'offsetX':bb[0],'offsetY':bb[1]}
 paint.save(out/'paint.png');erase.save(out/'erase.png');preview.save(out/'preview-native.png');(out/'mapping.json').write_text(json.dumps({'schemaVersion':1,'characterId':id,'baseAtlasSHA256':B[id],'frames':m},indent=2)+'\n');prov={'itemId':item,'characterId':id,'baseAtlasSHA256':B[id],'source':source,'frames':len(patches),'hiddenFrames':sum(v is None for v in m.values()),'native':[96,112],'anchor':[48,100],'policy':'Current approved base ownership; sparse native paint/erase,nearest,versioned derived assets,originals immutable','artApproval':'PENDING'};(out/'provenance.json').write_text(json.dumps(prov,indent=2)+'\n');root=str(out.relative_to(R/'public'))
 return {'characterId':id,'paint':root+'/paint.png','erase':root+'/erase.png','mapping':root+'/mapping.json','preview':root+'/preview-native.png','provenance':root+'/provenance.json','baseAtlasSHA256':B[id],'poseRevision':'phase2b-walkfront-approved-20261027','registration':{'width':96,'height':112,'anchor':[48,100],'sampling':'nearest','occlusion':'baked-native-visibility'}}
def diff(base,desired):
 a,b=np.array(base),np.array(desired);mask=np.any(a!=b,2);p=b.copy();p[~mask]=0;e=np.zeros_like(p);e[mask]=255;return Image.fromarray(p),Image.fromarray(e)
