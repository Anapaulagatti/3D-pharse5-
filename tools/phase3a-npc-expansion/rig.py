"""Author own-image alpha masks and joints, never draw primary faces or costumes."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,sys
from scipy.ndimage import binary_dilation
R=Path(__file__).resolve().parents[2];S=R/'assets-src/npcs/phase3a-npc-expansion'
CONFIG={
 'daehyun':{'hip':78,'knee':88,'shoe':94,'shoulder':49,'hem':79,'accessories':{'front':[[49,59,55,79]],'back':[],'left':[[37,57,43,80]],'right':[[51,57,57,80]]}},
 'jiho':{'hip':73,'knee':85,'shoe':94,'shoulder':49,'hem':72,'accessories':{'front':[[52,60,60,74]],'back':[[36,60,43,74]],'left':[[47,60,57,75]],'right':[[45,60,55,75]]}},
 'eunji':{'hip':73,'knee':85,'shoe':94,'shoulder':50,'hem':72},
 'seojun':{'hip':74,'knee':85,'shoe':94,'shoulder':49,'hem':73,'accessories':{'front':[[49,61,55,80]],'back':[],'left':[[37,60,43,80]],'right':[[51,60,57,80]]}}}
def poly(shape):
 im=Image.new('1',(96,112));ImageDraw.Draw(im).polygon([tuple(p)for p in shape],fill=1);return np.array(im,dtype=bool)
def box(a):x,y,w,z=a;return poly([[x,y],[w,y],[w,z],[x,z]])
def author(id):
 p=S/id;k=CONFIG[id];cfg={'nativeCell':[96,112],'footAnchor':[48,100],'source':'Own independent illustrated directional PNGs; own alpha masks and registration; no player RGB','designRegistration':k,'views':{}};yy,xx=np.indices((112,96))
 for d in ['front','back','left','right']:
  im=Image.open(p/'native'/f'{d}.png').convert('RGBA');a=np.array(im);opaque=a[:,:,3]>0;hip=k['hip'];knee=k['knee'];shoe=k['shoe'];sy=k['shoulder'];front=d in ['front','back'];masks={};joints={};arms={};patch=[];access=np.zeros((112,96),dtype=bool)
  for bb in k.get('accessories',{}).get(d,[]):access|=box(bb)
  if front:
   armPolys={'L':[[43,sy-1],[36,sy-1],[26,61],[26,76],[37,77],[42,58],[44,53]],'R':[[53,sy-1],[60,sy-1],[70,61],[70,76],[59,77],[54,58],[52,53]]};armMask={s:poly(q)for s,q in armPolys.items()}
   for s in ['L','R']:
    masks[s+'upperarm']=armMask[s]&(yy<=63);masks[s+'forearm']=armMask[s]&(yy>=60)
    left=s=='L';leg=(xx<48 if left else xx>=48)&(yy>=hip-3)&((yy>77)|((xx>=39)&(xx<=58)))&~access
    for n,lo,hi in [('thigh',hip-3,knee+2),('shin',knee-2,shoe+2),('shoe',shoe,112)]:masks[s+n]=leg&(yy>=lo)&(yy<hi)
    joints[s]=[[43 if left else 54,hip],[42 if left else 55,knee],[40 if left else 56,96]]
   masks['body']=((yy<=k['hem'])&~((armMask['L']|armMask['R'])&(yy>=sy+1)))|access
   arms={'L':[[42,sy],[37,62],[34,71]],'R':[[54,sy],[60,62],[63,71]]};bodyImage=im;near='R'
  else:
   facing=-1 if d=='left'else 1;nearX=51 if facing<0 else 46;farX=44 if facing<0 else 52;shoulder=[nearX,sy];elbow=[nearX-facing*2,62];wrist=[nearX-facing*3,71]
   m=poly([[nearX-4,sy-2],[nearX+4,sy-2],[wrist[0]+4,75],[wrist[0]-4,75]]);masks['Rupperarm']=m&(yy<=64);masks['Rforearm']=m&(yy>=60)
   for s,x in [('L',farX),('R',nearX)]:
    leg=(yy>=hip-3)&(xx>=x-6)&(xx<=x+6)&~access&~(m&(yy<=75))
    for n,lo,hi in [('thigh',hip-3,knee+2),('shin',knee-2,shoe+2),('shoe',shoe,112)]:masks[s+n]=leg&(yy>=lo)&(yy<hi)
    joints[s]=[[49+(0 if s=='R'else facing),hip],[x,knee],[x,96]]
   core=poly([[46,sy-3],[51,sy-3],[53,sy+3],[52,61],[53,k['hem']],[43,k['hem']],[44,59],[43,sy+4]])
   # Recover occluded cloth from this illustration's own same-row inner fabric only.
   recovered=a.copy();recover=core&(m|~opaque)&(yy>=sy+1)
   safe=45 if d=='left'else 50
   for y,x in zip(*np.where(recover)):
    if a[y,safe,3]:recovered[y,x]=a[y,safe]
   bodyImage=Image.fromarray(recovered);masks['body']=(yy<=sy)|core|access;arms={'R':[shoulder,elbow,wrist]};shift=farX-nearX;arms['L']=[[v[0]+shift,v[1]-1]for v in arms['R']];near='R';patch=[{'method':'Own same-row inner fabric within authored torso polygon only','candidatePixels':int(recover.sum()),'safeColumn':safe}]
  out=p/'layers'/d;out.mkdir(parents=True,exist_ok=True);ownership={}
  for n,m in masks.items():
   arr=np.array(bodyImage if n=='body'else im);arr[~m]=0;q=Image.fromarray(arr);assert q.getbbox(),(id,d,n);q.save(out/f'{n}.png');ownership[n]={'source':f'native/{d}.png','pixels':int((arr[:,:,3]>0).sum()),'bounds':q.getbbox()}
  if not front:
   for seg in ['upperarm','forearm']:
    nearImage=Image.open(out/f'R{seg}.png');q=Image.new('RGBA',(96,112));q.alpha_composite(nearImage,(shift,-1));q.save(out/f'L{seg}.png');ownership['L'+seg]={'source':f'layers/{d}/R{seg}.png','occlusionRecovery':[shift,-1],'sameActorSameView':True}
  cfg['views'][d]={'joints':joints,'arms':arms,'hipY':hip,'near':near,'facing':0 if front else facing,'ownership':ownership,'clothRecovery':patch}
 (p/'rig.json').write_text(json.dumps(cfg,indent=2)+'\n');print(id,'own image rig authored')
if __name__=='__main__':
 for id in sys.argv[1:]:author(id)
