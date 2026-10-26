"""Independent cosmetic source pipeline -> sparse native erase/paint packs.
No approved base character file is rewritten. All supported poses are baked here.
"""
from pathlib import Path
import sys,json,math,hashlib,copy
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];S=R/'assets-src/characters/phase2a';C=S/'cosmetics';D=R/'docs/phase2a';PUB=R/'public/assets/cosmetics'
sys.path.insert(0,str(R/'tools/phase1b'));sys.path.insert(0,str(R/'tools/phase2a'))
from animate import layer,render_front,render_side
from art import front,T
SPECS={
 'ara-harbor':('ara','ara-braided-bun','Búi tóc bện','Braided bun','땋은 올림머리','ara-coastal-parka','Áo khoác bến cảng','Coastal parka','해안 파카'),
 'ara-sunlit':('ara','ara-wavy-pixie','Pixie gợn sóng','Wavy pixie','웨이브 픽시','ara-sunlit-linen','Bộ linen nắng ấm','Sunlit linen outfit','햇살 리넨 의상'),
 'doyun-utility':('doyun','doyun-swept-quiff','Tóc vuốt nghiêng','Side-swept quiff','사이드 퀴프','doyun-field-jacket','Bộ áo khoác dã ngoại','Field jacket outfit','필드 재킷 의상'),
 'doyun-varsity':('doyun','doyun-curly-crop','Tóc xoăn ngắn','Curly crop','짧은 곱슬머리','doyun-varsity-cardigan','Bộ cardigan học đường','Varsity cardigan outfit','바시티 카디건 의상'),
}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def keyed(im):
 a=np.array(im.convert('RGBA'));key=(a[:,:,0]>170)&(a[:,:,2]>140)&(a[:,:,1]<100)&(a[:,:,0]>a[:,:,1]*1.6)&(a[:,:,2]>a[:,:,1]*1.5);a[key]=0;return Image.fromarray(a)
def finish_variant(name):
 p=C/'sources'/name;id=SPECS[name][0];im=Image.open(p/'turnaround-source.png').convert('RGBA');clean=keyed(im);clean.save(p/'turnaround-keyed.png');ref=json.loads((S/id/'native-finish.json').read_text());scale=ref['records'][0]['scale']*ref['sourceSize'][0]/im.width;w,h=im.size;frames=[];records=[]
 for i,d in enumerate(['front','back','left','right']):
  q=clean.crop((i%2*w//2,i//2*h//2,(i%2+1)*w//2,(i//2+1)*h//2));bb=q.getbbox();q=q.crop(bb);size=(round(q.width*scale),round(q.height*scale));q=q.resize(size,Image.Resampling.BOX);a=np.array(q);a[a[:,:,3]<128]=0;a[a[:,:,3]>=128,3]=255;q=Image.fromarray(a);pos=[48-size[0]//2,100-size[1]]
  if pos[1]<1:raise ValueError((name,d,'hairstyle exceeds approved native cell',pos,size))
  out=Image.new('RGBA',(96,112));out.alpha_composite(q,tuple(pos));base=np.array(Image.open(S/id/'native'/f'{d}.png'));test=np.array(out)
  # Shoe-root alignment only; no individual frame or limb normalization.
  by,bx=np.nonzero(base[93:100,:,3]);ty,tx=np.nonzero(test[93:100,:,3]);dx=round(float(bx.mean()-tx.mean()))if len(tx)and len(bx)else 0
  aligned=Image.new('RGBA',(96,112));aligned.alpha_composite(out,(dx,0));frames.append(aligned);records.append({'view':d,'rawBBox':bb,'fixedScale':scale,'size':size,'placement':[pos[0]+dx,pos[1]],'sourceRootAlignmentX':dx})
 board=Image.new('RGBA',(384,112))
 for i,im in enumerate(frames):board.alpha_composite(im,(i*96,0))
 rgb=Image.new('RGB',board.size,(30,25,35));rgb.paste(board,mask=board.getchannel('A'));pal=rgb.quantize(colors=96,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGBA');pal.putalpha(board.getchannel('A'));(p/'native').mkdir(exist_ok=True)
 for i,d in enumerate(['front','back','left','right']):pal.crop((i*96,0,(i+1)*96,112)).save(p/'native'/f'{d}.png')
 pal.save(p/'native-turnaround.png');pal.resize((1536,448),Image.Resampling.NEAREST).save(D/f'{name}-cosmetic-source-4x.png');(p/'native-finish.json').write_text(json.dumps({'sourceSHA256':sha(p/'turnaround-source.png'),'baseCharacter':id,'registrationPolicy':'One fixed source-to-native scale inherited from the base identity, adjusted only for source-canvas resolution; integer shoe-root alignment; no per-frame normalization','records':records},indent=2)+'\n')
def load_base(id):
 cfg=json.loads((S/id/'rig.json').read_text());parts={d:{p.stem:Image.open(p).convert('RGBA')for p in(S/id/'layers'/d).glob('*.png')}for d in ['front','back','left','right']};return cfg,parts

def render_all(cfg,parts):
 frames={}
 for d in ['front','back','left','right']:
  renderer=render_front if d in ['front','back']else render_side
  for action in ['walk','run']:
   for i in range(8):frames[f'{action}-{d}-{i}']=front(parts[d],cfg[d],T[f'{action}-{d}'][i])if d in ['front','back']else renderer(parts[d],cfg[d],i/8,action)
  for action,phases in [('idle',[0,.5]),('start',[.25,.18,.08]),('stop',[.08,.18,.25])]:
   for i,phase in enumerate(phases):frames[f'{action}-{d}-{i}']=renderer(parts[d],cfg[d],phase,'idle'if action=='idle'else'walk')
  if d=='front':
   for action in ['wave','celebrate']:
    for i in range(8):frames[f'{action}-{d}-{i}']=render_front(parts[d],cfg[d],i/8,action)
 return frames

def variant_parts(name,id,cfg,baseparts,category):
 parts=copy.deepcopy(baseparts)
 for d in parts:
  original=Image.open(C/'sources'/name/'native'/f'{d}.png').convert('RGBA');im=original.copy()
  for patch in cfg[d].get('clothRecovery',[]):im.alpha_composite(im.crop(tuple(patch['source'])),tuple(patch['target']))
  if category=='hairstyle':
   body=baseparts[d]['body'].copy();body.paste((0,0,0,0),(0,0,96,46));body.alpha_composite(layer(original,cfg[d]['masks']['body']).crop((0,0,96,46)),(0,0))
   # Preserve Ara/Doyun's original eyes, nose, mouth and neck pixels.
   face={'front':(40,33,56,44),'left':(35,33,50,44),'right':(46,33,61,44),'back':None}[d]
   if face:body.alpha_composite(baseparts[d]['body'].crop(face),(face[0],face[1]))
   body.alpha_composite(baseparts[d]['body'].crop((41,43,55,47)),(41,43));parts[d]['body']=body
  else:
   for key,poly in cfg[d]['masks'].items():
    q=layer(original if 'arm'in key or key=='body'else im,poly)
    if d in ['left','right']and key in ['Lthigh','Lshin','Lshoe']:
     a=np.array(q);a[:,:,:3]=np.rint(a[:,:,:3].astype(float)*.68).astype('uint8');q=Image.fromarray(a)
    if key=='body':q.paste((0,0,0,0),(0,0,96,46));q.alpha_composite(baseparts[d]['body'].crop((0,0,96,46)),(0,0))
    parts[d][key]=q
 return parts

def save_item(itemId,id,category,names,baseframes,frames,source,owner_frames=None):
 out=PUB/itemId;out.mkdir(exist_ok=True,parents=True);sourceout=C/'items'/itemId;sourceout.mkdir(exist_ok=True,parents=True);patches={};stats=[]
 for name,im in frames.items():
  a,b=np.array(baseframes[name]),np.array(im);mask=np.any(a!=b,2)if owner_frames is None else np.array(owner_frames[name])[:,:,3]>0
  bb=Image.fromarray(mask.astype('uint8')*255).getbbox()
  if not bb:patches[name]=None;continue
  if owner_frames is None:paint=b.copy();paint[~mask]=0
  else:paint=np.array(owner_frames[name]).copy()
  erase=np.zeros_like(paint);erase[mask]=255;patches[name]=(bb,Image.fromarray(paint).crop(bb),Image.fromarray(erase).crop(bb));stats.append({'frame':name,'changedPixels':int(mask.sum()),'bounds':bb})
 maxw=max(v[0][2]-v[0][0]for v in patches.values()if v);maxh=max(v[0][3]-v[0][1]for v in patches.values()if v);cols=12;rows=math.ceil(len(patches)/cols);paint=Image.new('RGBA',(cols*maxw,rows*maxh));erase=Image.new('RGBA',paint.size);mapping={}
 for i,(name,value)in enumerate(patches.items()):
  if not value:mapping[name]=None;continue
  bb,p,e=value;x,y=i%cols*maxw,i//cols*maxh;paint.paste(p,(x,y));erase.paste(e,(x,y));mapping[name]={'x':x,'y':y,'w':p.width,'h':p.height,'offsetX':bb[0],'offsetY':bb[1]}
 paint.save(out/'paint.png');erase.save(out/'erase.png');(out/'mapping.json').write_text(json.dumps({'schemaVersion':1,'characterId':id,'frames':mapping},indent=2)+'\n');frames['idle-front-0'].save(out/'preview-native.png')
 for name,im in frames.items():
  bb=im.getbbox();assert bb and bb[0]>0 and bb[1]>0 and bb[2]<96 and bb[3]<112,(itemId,name,bb);assert set(np.unique(np.array(im)[:,:,3]))<={0,255}
 # Full material layers/frames remain authoring sources, not runtime eager permutations.
 sheet=Image.new('RGBA',(768,528),(29,28,36,255));dr=ImageDraw.Draw(sheet)
 for row,key in enumerate(['walk-front','walk-back','run-front','run-back']):
  for i in range(8):sheet.alpha_composite(frames[f'{key}-{i}'],(i*96,row*132+20));dr.text((i*96+2,row*132+3),f'{key}-{i}',fill='white')
 sheet.save(D/f'{itemId}-native.png')
 provenance={'itemId':itemId,'characterId':id,'category':category,'source':source,'artSource':'host_image + existing own identity/layer artwork; offline native articulation, no base atlas changes','poseCompiler':'tools/phase2a/art.py + cosmetics.py, exact same poses/anchor as base','baseAtlasSHA256':sha(R/f'public/assets/characters/{id}/atlas.png'),'frames':len(frames),'explicitHiddenFrames':sum(v is None for v in mapping.values()),'packedRGBABytesPerImage':paint.width*paint.height*4,'patches':stats,'humanArtAcceptance':'PENDING'}
 (sourceout/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n');(out/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
 return {'id':itemId,'name':dict(zip(['vi','en','ko'],names)),'category':category,'compatibility':{'characterIds':[id]},'variants':[{'characterId':id,'paint':f'assets/cosmetics/{itemId}/paint.png','erase':f'assets/cosmetics/{itemId}/erase.png','mapping':f'assets/cosmetics/{itemId}/mapping.json','preview':f'assets/cosmetics/{itemId}/preview-native.png','registration':{'width':96,'height':112,'anchor':[48,100],'sampling':'nearest','occlusion':'baked-native-visibility'},'provenance':f'assets/cosmetics/{itemId}/provenance.json'}],'availability':{'status':'free-review','reason':'Complete native-frame cosmetic patch pack; identity and anatomy gate inspected; final human Phase2A approval pending'}}

def build_clothes():
 items=[]
 for name,spec in SPECS.items():
  id,hair,hvi,hen,hko,outfit,ovi,oen,oko=spec;finish_variant(name);cfg,base=load_base(id);baseframes=render_all(cfg,base)
  for n,im in baseframes.items():assert im.tobytes()==Image.open(S/id/'frames'/f'{n}.png').convert('RGBA').tobytes(),('base pose compiler drift',id,n)
  for category,itemId,names in [('hairstyle',hair,[hvi,hen,hko]),('outfit',outfit,[ovi,oen,oko])]:
   frames=render_all(cfg,variant_parts(name,id,cfg,base,category));items.append(save_item(itemId,id,category,names,baseframes,frames,str((C/'sources'/name/'turnaround-source.png').relative_to(R))))
 (C/'catalog.json').write_text(json.dumps({'schemaVersion':1,'items':items,'presets':[]},indent=2)+'\n');print('Baked',len(items),'hair/outfit items,112 registered poses each; approved bases untouched')
def body_offset(name):
 action,view,num=name.split('-');i=int(num)
 if action in ['walk','run']and view in ['front','back']:
  p=T[f'{action}-{view}'][i];return p.get('bodyDeltaX',0),p['bodyDeltaY']
 phase=i/8
 if action=='idle':phase=[0,.5][i];return 0,-round((1-math.cos(phase*math.tau))/2)
 if action in ['start','stop']:phase=([.25,.18,.08]if action=='start'else[.08,.18,.25])[i]
 return 0,round(-abs(math.sin(phase*math.tau))*(2 if action=='run'else 1))

def accessory_parts():
 p=C/'sources/accessories';im=keyed(Image.open(p/'source.png'));w,h=im.size;allparts={};records=[]
 for row,itemId in enumerate(['ara-shell-barrette','doyun-linen-kerchief']):
  raw=[]
  for col,d in enumerate(['front','back','left','right']):
   q=im.crop((col*w//4,row*h//2,(col+1)*w//4,(row+1)*h//2));bb=q.getbbox();raw.append((d,q.crop(bb),bb))
  scale=(4 if row==0 else 11)/raw[0][1].width;parts={}
  for d,q,bb in raw:
   size=(max(1,round(q.width*scale)),max(1,round(q.height*scale)));q=q.resize(size,Image.Resampling.BOX);a=np.array(q);a[a[:,:,3]<128]=0;a[a[:,:,3]>=128,3]=255;q=Image.fromarray(a);rgb=q.convert('RGB').quantize(colors=16,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGBA');rgb.putalpha(q.getchannel('A'));parts[d]=rgb;records.append({'itemId':itemId,'view':d,'bbox':bb,'scale':scale,'nativeSize':size})
  allparts[itemId]=parts
  (p/'native').mkdir(exist_ok=True)
  for d,q in parts.items():q.save(p/'native'/f'{itemId}-{d}.png')
 (p/'native-registration.json').write_text(json.dumps({'sourceSHA256':sha(p/'source.png'),'method':'Uniform source-to-native scale per prop, binary alpha and16-color material finish; source views are static props, never character animation sheets','records':records},indent=2)+'\n');return allparts

def build_accessories():
 native=accessory_parts();catalog=json.loads((C/'catalog.json').read_text());items=[]
 for itemId,id,names in [('ara-shell-barrette','ara',['Kẹp tóc vỏ sò','Golden shell barrette','조개 머리핀']),('doyun-linen-kerchief','doyun',['Khăn linen gạch ấm','Rust linen neckerchief','리넨 넥커치프'])]:
  cfg,parts=load_base(id);baseframes=render_all(cfg,parts);occ=copy.deepcopy(parts)
  for d in occ:
   occ[d]['body']=Image.new('RGBA',(96,112))
   if itemId.startswith('doyun')and d in ['left','right']:
    poly=[(48,52),(56,52),(56,66),(48,66)]if d=='left'else[(40,52),(48,52),(48,66),(40,66)]
    occ[d]['body']=layer(parts[d]['body'],poly)
  occluders=render_all(cfg,occ);owner={};frames={}
  positions={'front':(54,31),'back':(41,31),'left':(47,30),'right':None}if id=='ara'else{'front':(48,48),'back':(48,47),'left':(45,48),'right':(51,48)}
  for name,base in baseframes.items():
   d=name.split('-')[1];target=positions[d];out=Image.new('RGBA',(96,112))
   if target:
    sprite=native[itemId][d];dx,dy=body_offset(name);out.alpha_composite(sprite,(target[0]-sprite.width//2+dx,target[1]+dy));a=np.array(out);oc=np.array(occluders[name])[:,:,3]>0;a[oc]=0;out=Image.fromarray(a)
   owner[name]=out;im=base.copy();im.alpha_composite(out);frames[name]=im
  item=save_item(itemId,id,'accessory',names,baseframes,frames,str((C/'sources/accessories/source.png').relative_to(R)),owner)
  item['availability']['reason']+='; anatomical attachment baked before playback; explicit right-profile head occlusion for Ara barrette'if id=='ara'else'; neck attachment and sleeve occlusion baked for every pose'
  items.append(item)
 catalog['items']=[i for i in catalog['items']if i['category']!='accessory']+items
 catalog['presets']=[{'id':f'review-{id}-{n}','name':name,'appearance':{'schemaVersion':2,'characterId':id,'hairstyleId':hair,'outfitId':outfit,'accessoryIds':[accessory]}}for id,n,name,hair,outfit,accessory in [
 ('ara','harbor','Ara · Dạo bến cảng','ara-braided-bun','ara-coastal-parka','ara-shell-barrette'),('ara','sunlit','Ara · Ngày nắng','ara-wavy-pixie','ara-sunlit-linen','ara-shell-barrette'),
 ('doyun','field','Doyun · Dã ngoại','doyun-swept-quiff','doyun-field-jacket','doyun-linen-kerchief'),('doyun','varsity','Doyun · Phố học đường','doyun-curly-crop','doyun-varsity-cardigan','doyun-linen-kerchief')]]
 (C/'catalog.json').write_text(json.dumps(catalog,indent=2,ensure_ascii=False)+'\n');print('Added2 fully frame-registered accessories; catalog10 items,4 review presets')

def build_interactions():
 catalog=json.loads((C/'catalog.json').read_text());interactions=[]
 for id in ['ara','doyun']:
  cfg,base=load_base(id);baseframes=render_all(cfg,base);own=[(name,sp)for name,sp in SPECS.items()if sp[0]==id]
  for hname,hspec in own:
   hairparts=variant_parts(hname,id,cfg,base,'hairstyle');hairframes=render_all(cfg,hairparts)
   for oname,ospec in own:
    outfitparts=variant_parts(oname,id,cfg,base,'outfit');hybrid=copy.deepcopy(outfitparts)
    for d in hybrid:hybrid[d]['body'].paste((0,0,0,0),(0,0,96,46));hybrid[d]['body'].alpha_composite(hairparts[d]['body'].crop((0,0,96,46)),(0,0))
    direct=render_all(cfg,hybrid);modular={}
    itemId=ospec[5];p=PUB/itemId;m=json.loads((p/'mapping.json').read_text())['frames'];paint=Image.open(p/'paint.png').convert('RGBA');erase=Image.open(p/'erase.png').convert('RGBA');bad=0
    for name,im in hairframes.items():
     out=im.copy();v=m[name]
     if v:
      box=(v['x'],v['y'],v['x']+v['w'],v['y']+v['h']);a=np.array(out);mask=np.array(erase.crop(box))[:,:,3]>0;a[v['offsetY']:v['offsetY']+v['h'],v['offsetX']:v['offsetX']+v['w']][mask]=0;out=Image.fromarray(a);out.alpha_composite(paint.crop(box),(v['offsetX'],v['offsetY']))
     modular[name]=out;bad+=int(np.any(np.array(out)!=np.array(direct[name]),2).sum())
    if bad:
     repairId=f'occlusion-{hspec[1]}-{ospec[5]}'
     correction=save_item(repairId,id,'interaction',['Native ownership correction']*3,modular,direct,[str((C/'sources'/hname/'turnaround-source.png').relative_to(R)),str((C/'sources'/oname/'turnaround-source.png').relative_to(R))])
     interactions.append({'id':repairId,'characterId':id,'requiresItemIds':[hspec[1],ospec[5]],'applyPhase':'before-accessories','patch':correction['variants'][0]})
 catalog['interactions']=interactions;(C/'catalog.json').write_text(json.dumps(catalog,indent=2,ensure_ascii=False)+'\n');print('Baked',len(interactions),'sparse native hair/raised-sleeve ownership interactions')

if __name__=='__main__':
 if '--prepare' in sys.argv:
  for name in SPECS:finish_variant(name)
 elif '--accessories' in sys.argv:build_accessories()
 elif '--interactions' in sys.argv:build_interactions()
 else:build_clothes();build_accessories();build_interactions()
