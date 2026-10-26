from pathlib import Path
import sys,json,itertools,copy
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parent))
import cosmetics as C
R=C.R;D=C.D;catalog=json.loads((C.C/'catalog.json').read_text());items={i['id']:i for i in catalog['items']};patches={}
allpacks=list(items.values())+[{'id':i['id'],'compatibility':{'characterIds':[i['characterId']]}}for i in catalog.get('interactions',[])]
for item in allpacks:
 id=item['compatibility']['characterIds'][0];p=R/'public/assets/cosmetics'/item['id'];m=json.loads((p/'mapping.json').read_text());keys=json.loads((R/f'public/assets/characters/{id}/atlas.json').read_text())['frames'];assert set(m['frames'])==set(keys);paint=Image.open(p/'paint.png').convert('RGBA');erase=Image.open(p/'erase.png').convert('RGBA');assert paint.size==erase.size;assert set(np.unique(np.array(paint)[:,:,3]))<={0,255};assert set(np.unique(np.array(erase)[:,:,3]))<={0,255};patches[item['id']]=(m['frames'],paint,erase)
def apply(base,name,itemIds):
 out=base.copy()
 selected=[items[v]for v in itemIds];interactions=[i['id']for i in catalog.get('interactions',[])if all(v in itemIds for v in i['requiresItemIds'])]
 order=[i['id']for i in selected if i['category']!='accessory']+interactions+[i['id']for i in selected if i['category']=='accessory']
 for itemId in order:
  mapping,paint,erase=patches[itemId];r=mapping[name]
  if r is None:continue
  box=(r['x'],r['y'],r['x']+r['w'],r['y']+r['h']);x,y=r['offsetX'],r['offsetY'];a=np.array(out);mask=np.array(erase.crop(box))[:,:,3]>0;a[y:y+r['h'],x:x+r['w']][mask]=0;out=Image.fromarray(a);out.alpha_composite(paint.crop(box),(x,y))
 return out
results=[];bad=[]
for id in ['ara','doyun']:
 cfg,baseparts=C.load_base(id);baseframes=C.render_all(cfg,baseparts)
 hairIds=[None]+[i['id']for i in items.values()if i['category']=='hairstyle'and id in i['compatibility']['characterIds']];outfitIds=[None]+[i['id']for i in items.values()if i['category']=='outfit'and id in i['compatibility']['characterIds']];accessory=next(i['id']for i in items.values()if i['category']=='accessory'and id in i['compatibility']['characterIds'])
 sourceMap={k:(name,category)for name,sp in C.SPECS.items()for k,category in [(sp[1],'hairstyle'),(sp[5],'outfit')]if sp[0]==id};sources={k:C.variant_parts(name,id,cfg,baseparts,category)for k,(name,category)in sourceMap.items()}
 # Accessory is independently re-registered from its native source prop and source
 # pose offsets; arm ownership is taken from actual image layers, not pack rectangles.
 occ=copy.deepcopy(baseparts)
 for d in occ:
  occ[d]['body']=Image.new('RGBA',(96,112))
  if id=='doyun'and d in ['left','right']:
   occ[d]['body']=C.layer(baseparts[d]['body'],[(48,52),(56,52),(56,66),(48,66)]if d=='left'else[(40,52),(48,52),(48,66),(40,66)])
 occluders=C.render_all(cfg,occ);owner={};positions={'front':(54,31),'back':(41,31),'left':(47,30),'right':None}if id=='ara'else{'front':(48,48),'back':(48,47),'left':(45,48),'right':(51,48)}
 for name in baseframes:
  d=name.split('-')[1];im=Image.new('RGBA',(96,112));point=positions[d]
  if point:
   prop=Image.open(C.C/f'sources/accessories/native/{accessory}-{d}.png').convert('RGBA');dx,dy=C.body_offset(name);im.alpha_composite(prop,(point[0]-prop.width//2+dx,point[1]+dy));a=np.array(im);a[np.array(occluders[name])[:,:,3]>0]=0;im=Image.fromarray(a)
  owner[name]=im
 for hair,outfit in itertools.product(hairIds,outfitIds):
  parts=copy.deepcopy(sources[outfit]if outfit else baseparts)
  if hair:
   for d in parts:
    parts[d]['body'].paste((0,0,0,0),(0,0,96,46));parts[d]['body'].alpha_composite(sources[hair][d]['body'].crop((0,0,96,46)),(0,0))
  direct=C.render_all(cfg,parts)
  for acc in [False,True]:
   ids=[v for v in [hair,outfit,accessory if acc else None]if v];different=0
   for name,base in baseframes.items():
    expected=direct[name].copy()
    if acc:expected.alpha_composite(owner[name])
    actual=apply(base,name,ids);diff=int(np.any(np.array(actual)!=np.array(expected),2).sum());different+=diff
    if diff and len(bad)<6:
     bad.append({'character':id,'items':ids,'frame':name,'pixelDifference':diff});actual.save(D/f'composition-fail-{len(bad)}-actual.png');expected.save(D/f'composition-fail-{len(bad)}-reference.png')
   results.append({'characterId':id,'itemIds':ids,'frames':len(baseframes),'differentPixelsFromDirectOwnLayerReference':different})
report={'method':'All36 supported independent combinations compared across all112frames against direct own-PNG-layer construction; sparse pack compositor is checked separately from pose authoring. No eager runtime atlas permutations are emitted. Accessories use native prop sources and anatomical/source-layer occlusion.','assetSHA256':{str(p.relative_to(R)):C.sha(p)for p in [C.C/'catalog.json']+[p for p in C.PUB.rglob('*')if p.is_file()and p.suffix in ['.png','.json']]},'combinations':results,'failures':bad,'humanArtAcceptance':'PENDING'};(D/'composition-qa.json').write_text(json.dumps(report,indent=2)+'\n');print('Combinations:',len(results),'badPixels:',sum(r['differentPixelsFromDirectOwnLayerReference']for r in results));assert not bad,bad
