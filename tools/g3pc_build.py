"""Native scoped palace repairs; original source files immutable."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,copy,hashlib
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate3/palace-cleanup-v1';D=R/'docs/gate3-palace-cleanup';O=R/'public/assets/gate3/palace-cleanup-world'
def wr(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
lock=json.loads((S/'baseline-lock.json').read_text());b=lock['manifest'];m=copy.deepcopy(b);spec=json.loads((S/'scope.json').read_text());W,H=m['size'];allowed=np.array(Image.open(S/'edit-scope-mask.png'))>0;src=Image.open(S/'local-repair-authored.png').convert('RGBA');assert src.size==(1536,1536)
g=Image.new('RGBA',(W,H));field=np.zeros((H,W),np.uint8)
for c in m['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];g.paste(Image.open(R/'public'/c['image']),(x,y));field[y:y+h,x:x+w]=np.fromfile(R/'public'/c['mask'],np.uint8).reshape(h,w)
before=g.copy();oldfield=field.copy();g.paste(src,(1400,320),Image.open(S/'edit-scope-mask.png').crop((1400,320,2936,1856)))
# No global collision rewrite: align walkable contact field only to explicitly
# authored ceremonial lane and right-hand approach, including native foot margin.
route=Image.new('L',(W,H));dr=ImageDraw.Draw(route);dr.rectangle((1960,1080,2136,1830),fill=255);dr.rectangle((2110,1438,2625,1487),fill=255);dr.rectangle((2575,1400,2625,1487),fill=255)
routearr=(np.array(route)>0)&allowed;field=oldfield.copy()
# Actual stop-back/idle-back contact proves old threshold cells at y1446 are
# closed beneath the newly visible exterior floor. Open ONLY this floor strip.
newfloor=np.zeros((H,W),bool);newfloor[1438:1489,2110:2636]=True;newfloor&=allowed;field[newfloor]=255
objects=[];edited=[]
for ob in m['objects']:
 im=Image.open(R/'public'/ob['image']).convert('RGBA');x,y=ob['x'],ob['y'];a=np.array(im);sub=allowed[max(0,y):min(H,y+im.height),max(0,x):min(W,x+im.width)]
 if x<0 or y<0 or not np.any(sub & (a[:,:,3]>0)):
  objects.append(ob);continue
 # Keep exact original ownership and alpha outside scope. New opaque native RGB
 # inside scope replaces old art; no filters or new foreground silhouettes.
 changed=sub&(a[:,:,3]>0);patch=np.array(g.crop((x,y,x+im.width,y+im.height)));a[changed,:3]=patch[changed,:3];a[changed,3]=255
 n=copy.deepcopy(ob);p=O/(ob['id'].replace('/','-')+'.png');Image.fromarray(a).save(p);n['image']=str(p.relative_to(R/'public'));objects.append(n);edited.append(ob['id'])
# Explicit foreground ownership for the retained right gateway lantern.
fgmask=Image.open(S/'right-gate-foreground-mask.png');box=fgmask.getbbox();x,y,rx,ry=box;im=src.crop(box);im.putalpha(fgmask.crop(box));p=O/'right-gate-foreground.png';im.save(p);objects.append({'id':'palace-cleanup/right-gate-foreground','image':str(p.relative_to(R/'public')),'x':1400+x,'y':320+y,'width':rx-x,'height':ry-y,'sortY':1610,'alphaSoftening':.35,'bytes':(rx-x)*(ry-y)*4})
m['objects']=objects;changedChunks=[];collisionChunks=[]
for c in m['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];im=g.crop((x,y,x+w,y+h))
 if im.tobytes()!=before.crop((x,y,x+w,y+h)).tobytes():
  p=O/(c['id']+'.png');im.save(p);c['image']=str(p.relative_to(R/'public'));c['sha256']=sha(p);changedChunks.append(c['id'])
 if not np.array_equal(field[y:y+h,x:x+w],oldfield[y:y+h,x:x+w]):
  p=O/(c['id']+'.bin');field[y:y+h,x:x+w].tofile(p);c['mask']=str(p.relative_to(R/'public'));c['maskSha256']=sha(p);collisionChunks.append(c['id'])
frames={'palace-axis-local':[2048,1370],'palace-access-local':[2380,1410],'palace-front-local':[2000,650],'palace-combined-local':[1950,790]};entries={k:[2048,1750]for k in frames}
for name,q in [('palace-cleanup-before',copy.deepcopy(b)),('palace-cleanup-world',m)]:
 q.update(id=name,artStatus='Palace local cleanup / HUMAN REVIEW; Hanbit, bridges and western hanok APPROVED LOCKED');q['nativeFrames'].update(frames);q['reviewEntries'].update(entries)
 if name.endswith('world'):
  over=g.copy()
  for o in sorted(objects,key=lambda o:o['sortY']):over.alpha_composite(Image.open(R/'public'/o['image']).convert('RGBA'),(o['x'],o['y']))
  over.crop((1400,320,2936,1856)).save(S/'integrated-context.png');over.thumbnail((870,973),Image.Resampling.NEAREST);over.save(O/'overview.png');q['overview']=str((O/'overview.png').relative_to(R/'public'))
 wr(R/'public/assets/gate3'/name/'manifest.json',q)
wr(S/'integration-provenance.json',{'baseline':lock['HEAD'],'sourceScale':'EXACT native1:1, no resizing/filtering','sourceOrigin':[1400,320],'groundChunks':changedChunks,'collisionChunks':collisionChunks,'collisionCellsChanged':int((field!=oldfield).sum()),'foregroundFragments':edited,'contactPhysicalAndProtectedLogicalSolids':'UNCHANGED','source':'local-repair-authored.png','mask':'edit-scope-mask.png','visualAcceptance':'PENDING HUMAN'})
print(changedChunks,collisionChunks,edited)
