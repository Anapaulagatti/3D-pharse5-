"""Whole local house/garden rebuild, native pixels; existing collision EXACT."""
from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import binary_dilation,binary_closing
import numpy as np,json,copy,hashlib
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate3/west-hanok-v1';O=R/'public/assets/gate3/west-hanok-world';D=R/'docs/gate3-west-hanok'
def wr(p,q):p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
lock=json.loads((S/'baseline-lock.json').read_text());m=copy.deepcopy(lock['manifest']);spec=json.loads((S/'scope.json').read_text());W,H=m['size'];mask=Image.open(S/'edit-scope-mask.png');allowed=np.array(mask)>0;src=Image.open(S/'local-repair-authored.png').convert('RGBA');assert src.size==(1536,1024);g=Image.new('RGBA',(W,H))
for c in m['chunks']:g.paste(Image.open(R/'public'/c['image']),(c['x'],c['y']))
before=g.copy();g.paste(src,(320,750),mask.crop((320,750,1856,1774)))
retired=[];kept=[]
for o in m['objects']:
 if o['id']not in spec['retiredTargetObjects']:kept.append(o);continue
 im=Image.open(R/'public'/o['image']).convert('RGBA');a=np.array(im);x,y=o['x'],o['y'];sub=allowed[y:y+im.height,x:x+im.width];a[:,:,3][sub]=0
 if np.any(a[:,:,3]):
  ob=copy.deepcopy(o);file=O/(o['id'].replace('/','-')+'-outside.png');Image.fromarray(a).save(file);ob['image']=str(file.relative_to(R/'public'));kept.append(ob)
 retired.append(o['id'])
m['objects']=kept;parts=[]
# Foreground ownership copies the new painting's exact RGB at integer scale.
for name,box,depth in [('house',(545,880,1096,1359),1360),('garden',(603,1408,1190,1701),1674)]:
 x,y,rx,ry=box;im=src.crop((x-320,y-750,rx-320,ry-750));a=np.array(im);r,gr,b=[a[:,:,i].astype(float)for i in range(3)];scope=allowed[y:ry,x:rx]
 if name=='house':
  blue=(b>r*.9)&(gr>r*.85)&(b>35)&(r<165);near=binary_dilation(blue,iterations=8);wood=(r>gr*1.1)&(gr>b*1.05);mat=blue|(near&wood)
 else:
  vegetation=(gr>r*1.03)&(gr>b*1.12);stone=(abs(r-gr)<25)&(abs(gr-b)<30)&(r<195);wood=(r>gr*1.16)&(gr>b*1.15)&(r<180);mat=vegetation|stone|wood
  # Exact owned garden silhouette; exclude neighboring public ground.
  form=Image.new('L',im.size);dr=ImageDraw.Draw(form);dr.polygon([(0,55),(25,0),(160,0),(200,35),(235,0),(390,0),(450,45),(560,0),(586,65),(586,260),(550,285),(20,285),(0,260)],fill=255);mat&=np.array(form)>0
 mat&=scope;a[:,:,3]=mat*255;file=O/(name+'-foreground.png');Image.fromarray(a).save(file);ob={'id':'west-hanok/'+name+'-foreground','image':str(file.relative_to(R/'public')),'x':x,'y':y,'width':im.width,'height':im.height,'sortY':depth,'alphaSoftening':.35,'bytes':im.width*im.height*4};m['objects'].append(ob);parts.append(ob)
changed=[]
for c in m['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];im=g.crop((x,y,x+w,y+h))
 if im.tobytes()!=before.crop((x,y,x+w,y+h)).tobytes():file=O/(c['id']+'.png');im.save(file);c['image']=str(file.relative_to(R/'public'));c['sha256']=sha(file);changed.append(c['id'])
frame=json.loads((R/'public/assets/gate3/west-hanok-before/manifest.json').read_text());m.update(id='west-hanok-world',artStatus='LOCAL western house/garden human review / Hanbit and Jeju bridge visuals APPROVED LOCKED',nativeFrames=frame['nativeFrames'],reviewEntries=frame['reviewEntries']);over=g.copy()
for o in sorted(m['objects'],key=lambda o:o['sortY']):over.alpha_composite(Image.open(R/'public'/o['image']).convert('RGBA'),(o['x'],o['y']))
over.crop((320,750,1856,1774)).save(S/'integrated-context.png');over.thumbnail((870,973),Image.Resampling.NEAREST);over.save(O/'overview.png');m['overview']=str((O/'overview.png').relative_to(R/'public'));wr(O/'manifest.json',m);wr(S/'integration-provenance.json',{'baseline':lock['HEAD'],'source':'local-repair-authored.png','sourceOrigin':[320,750],'sourceScale':'EXACT1:1 / integer placement / no filters or resampling','exactMask':'edit-scope-mask.png','groundChunksChanged':changed,'collisionChunksChanged':[],'collisionPolicy':'ALL fields/logical solids/native contact spec EXACT unchanged','retiredTargetFragments':retired,'newNativeForegrounds':parts,'protected':'All other objects, station, BOTH bridges, island, palace, public roads, Juni and source files exact','artAcceptance':'PENDING HUMAN'})
print('Changed ground chunks',changed,'; collision changes0')
