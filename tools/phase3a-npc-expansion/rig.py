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
CONFIG.update({
 'nayeon':{'hip':83,'knee':90,'shoe':92,'shoulder':50,'hem':85,'apron':True},
 'cheolsu':{'hip':74,'knee':85,'shoe':92,'shoulder':49,'hem':73,'accessories':{'front':[[35,62,43,77]],'back':[[53,62,60,77]],'left':[[51,61,59,78]],'right':[[37,61,45,78]]}},
 'yejin':{'hip':73,'knee':85,'shoe':92,'shoulder':49,'hem':72,'accessories':{'front':[[51,61,59,73]],'back':[],'left':[[39,60,47,73]],'right':[]}},
 'sungmin':{'hip':72,'knee':85,'shoe':94,'shoulder':49,'hem':71}
})
CONFIG.update({
 'junho':{'hip':73,'knee':85,'shoe':94,'shoulder':49,'hem':72,'accessories':{'front':[[35,58,44,71]],'back':[[51,58,60,71]],'left':[[37,58,43,73]],'right':[[50,58,57,73]]}},
 'donghae':{'hip':73,'knee':85,'shoe':93,'shoulder':49,'hem':72,'accessories':{'front':[[51,63,57,78]],'back':[[39,63,45,78]],'left':[[42,62,48,79]],'right':[[43,62,49,79]]}},
 'soobin':{'hip':73,'knee':85,'shoe':94,'shoulder':49,'hem':72,'longHair':True}
})
CONFIG.update({
 'modern-daon':{'hip':73,'knee':85,'shoe':94,'shoulder':49,'hem':72,'longHair':True,'hairBottom':67},
 'modern-miram':{'hip':73,'knee':85,'shoe':94,'shoulder':49,'hem':72},
 'modern-geonu':{'hip':73,'knee':85,'shoe':92,'shoulder':49,'hem':72},
 'modern-seorin':{'hip':73,'knee':85,'shoe':94,'shoulder':49,'hem':72},
 'modern-haru':{'hip':74,'knee':85,'shoe':94,'shoulder':49,'hem':75},
 'modern-yeori':{'hip':74,'knee':85,'shoe':94,'shoulder':49,'hem':80,'longCoat':True,'accessories':{'front':[[35,61,43,73]],'back':[],'left':[[38,60,45,73]],'right':[]}}
})
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
  if k.get('longHair'):
   rgb=a[:,:,:3].astype(int);hair=(yy<k.get('hairBottom',61))&(rgb[:,:,0]<190)&(rgb[:,:,1]<145)&(rgb[:,:,0]>rgb[:,:,1]*1.2)&(rgb[:,:,0]>rgb[:,:,2]*1.3)&opaque
   masks['body']|=hair
   for name in list(masks):
    if name!='body':masks[name]&=~hair
  if k.get('longCoat'):
   rgb=a[:,:,:3].astype(int);coat=(yy>=68)&(yy<=82)&(rgb[:,:,1]>rgb[:,:,0]*1.02)&(rgb[:,:,1]>rgb[:,:,2]*1.04)&opaque
   masks['body']|=coat
   for name in list(masks):
    if any(t in name for t in ['thigh','shin']):masks[name]&=~coat
  if (id=='yejin'or id.startswith('modern-'))and front:
   rgb=a[:,:,:3].astype(int);skin=(rgb[:,:,0]>145)&(rgb[:,:,0]>rgb[:,:,1]*1.25)&(rgb[:,:,0]>rgb[:,:,2]*1.3);ring=binary_dilation(skin,iterations=1)&opaque
   for name in ['Lforearm','Rforearm']:masks[name]&=(yy<65)|ring
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
