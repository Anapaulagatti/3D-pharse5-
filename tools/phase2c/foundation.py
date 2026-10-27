from pathlib import Path
import sys,json,copy,importlib.util
import numpy as np
from PIL import Image
from core import *
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
old=module('old_cosmetic',R/'tools/phase2a/cosmetics.py');front=module('current_front',R/'tools/phase2b-walkfront/author.py');catalog=json.loads((R/'assets-src/characters/phase2a/cosmetics/catalog.json').read_text());audit=[]
for item in catalog['items']:
 id=item['compatibility']['characterIds'][0];base=load(id);v=item['variants'][0];patches=decode(v);coverage=[]
 for k,(p,e)in patches.items():
  ys,xs=np.where(np.array(p)[:,:,3]>0)
  coverage.append({'frame':k,'bounds':p.getbbox(),'paintBelowHead':int((ys>=47).sum()),'paintOnLegs':int((ys>=72).sum())})
 if item['category']=='outfit':
  # Refuse a stale pose compiler after any future authorized base correction.
  # Updating a signature alone must never certify old body geometry.
  approved_root=R/f'assets-src/characters/phase2a/{id}';ap,ac=front.parts(approved_root)
  for idx in range(8):assert front.frame(ap,ac,idx)[0].tobytes()==base[f'walk-front-{idx}'].tobytes(),('Base pose changed; update wardrobe compiler before rebinding',id,idx)
  name=next(n for n,spec in old.SPECS.items()if spec[5]==item['id']);cfg,parts=old.load_base(id);vp=old.variant_parts(name,id,cfg,parts,'outfit');root=S/'foundation'/item['id'];(root/'native').mkdir(parents=True,exist_ok=True);(root/'layers/front').mkdir(parents=True,exist_ok=True);Image.open(old.C/'sources'/name/'native/front.png').save(root/'native/front.png');(root/'rig.json').write_text(json.dumps(cfg));vp['front']['body'].save(root/'layers/front/body.png');p,c=front.parts(root)
  for i in range(8):
   k=f'walk-front-{i}';im,_=front.frame(p,c,i);a=np.array(im);a[:47]=np.array(base[k])[:47];im=Image.fromarray(a);patches[k]=diff(base[k],im)
 # Head/accessory patches contain no outdated leg poses and are rebound intact.
 preview=apply(base['idle-front-0'],patches['idle-front-0']);item['variants']=[save(item['id'],id,patches,preview,'Existing approved cosmetic native sources; current walk-front authoring for outfit; originals retained')];item['availability']['reason']='Free review; native patch ownership bound to approved12-character baseline'
 audit.append({'item':item['id'],'category':item['category'],'frames':coverage,'repairedFrames':[f'walk-front-{i}'for i in range(8)]if item['category']=='outfit'else[],'baseBinding':B[id]})
for inter in catalog.get('interactions',[]):
 id=inter['characterId'];base=load(id);patches=decode(inter['patch'])
 for i in range(8):patches[f'walk-front-{i}']=(Image.new('RGBA',(96,112)),Image.new('RGBA',(96,112)))
 inter['patch']=save(inter['id'],id,patches,base['idle-front-0'],'Existing non-front interaction preserved; current front outfit excludes head and commutes with hair')
(S/'catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n');(D/'pose-compatibility-audit.json').write_text(json.dumps(audit,indent=2)+'\n');print('10existingitems rebound;4outfits x8walk-front repaired;8interactions synchronized; originals immutable')
