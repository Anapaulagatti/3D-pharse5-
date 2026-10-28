"""Author image-owned native limb masks/joints; no primary character pixels drawn."""
from pathlib import Path
import json,sys
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import binary_dilation
R=Path(__file__).resolve().parents[2];S=R/'assets-src/npcs/phase3a-art-rebuild';sys.path.insert(0,str(R/'tools/phase1b'));from animate import layer
IDS=['seoyeon','minseo','harin'];DIRS=['front','back','left','right']
def rect(x0,y0,x1,y1):return [[x0,y0],[x1,y0],[x1,y1],[x0,y1]]
def author(id):
 p=S/id;cfg={'nativeCell':[96,112],'footAnchor':[48,100],'artSource':'Own host-image illustrated turnaround;explicit native alpha layer ownership,not procedural body painting','views':{}}
 for d in DIRS:
  im=Image.open(p/'native'/f'{d}.png').convert('RGBA');yy,xx=np.indices((112,96));front=d in ['front','back'];hipY=75 if id=='minseo'else 66;split=86 if id=='minseo'else 82;shoeY=93 if id!='harin'else 92;shoulderY=50 if id=='harin'else 49
  masks={};joints={};arms={};patches=[];accessories=[]
  if front:
   armsPolys={
    'L':[[42,shoulderY-1],[39,shoulderY],[31,61],[30,72],[35,75],[40,61],[44,53]],
    'R':[[54,shoulderY-1],[58,shoulderY],[66,61],[66,73],[61,75],[56,61],[52,53]]}
   for side,poly in armsPolys.items():
    mask=np.array(layer(Image.new('RGBA',(96,112),(255,255,255,255)),poly))[:,:,3]>0
    masks[side+'upperarm']=mask&(yy<=62);masks[side+'forearm']=mask&(yy>=59)
   for side,left in [('L',True),('R',False)]:
    half=xx<48 if left else xx>=48;leg=half&(yy>=hipY-3)&(np.array(im)[:,:,3]>0)
    if id=='minseo':
     a=np.array(im);pants=(a[:,:,2]>=a[:,:,0]*.75)&(a[:,:,1]>a[:,:,0]*.85);leg&=pants|(yy>=88)
    if id=='seoyeon'and d=='front':accessories=[rect(51,55,56,74)]
    if id=='harin':accessories=[rect(52 if d=='front'else 36,61,60 if d=='front'else 44,76)]
    for poly in accessories:
     omit=np.array(layer(Image.new('RGBA',(96,112),(255,255,255,255)),poly))[:,:,3]>0;leg&=~omit
    for name,lo,hi in [('thigh',hipY-3,split+2),('shin',split-2,shoeY+2),('shoe',shoeY,111)]:masks[side+name]=leg&(yy>=lo)&(yy<hi)
    x=43 if left else 54;ankleX=40 if left else 56;joints[side]=[[x,hipY],[x if id=='minseo'else x-1 if left else x+1,split],[ankleX,95]]
   armL=np.array(layer(Image.new('RGBA',(96,112),(255,255,255,255)),armsPolys['L']))[:,:,3]>0;armR=np.array(layer(Image.new('RGBA',(96,112),(255,255,255,255)),armsPolys['R']))[:,:,3]>0
   body=(yy<=hipY+2)&~((armL|armR)&(yy>=shoulderY+1))
   if id=='minseo':
    a=np.array(im);apron=(a[:,:,0]>a[:,:,2]*1.25)&(a[:,:,0]>a[:,:,1]*1.05);body|=apron&(yy>=hipY)&(yy<=79)&(xx>=37)&(xx<=60)
   for poly in accessories:body|=np.array(layer(Image.new('RGBA',(96,112),(255,255,255,255)),poly))[:,:,3]>0
   masks['body']=body;arms={'L':[[42,shoulderY],[37,61],[34,69]],'R':[[54,shoulderY],[60,61],[63,69]]};near='R'
  else:
   face=-1 if d=='left'else 1;near='R';nearX=51 if face<0 else 46;farX=44 if face<0 else 52
   # Independent directional illustrations remain separate. Their own near/far fabric supplies underlying projection.
   for side,x in [('L',farX),('R',nearX)]:
    leg=(yy>=hipY-3)&(xx>=x-6)&(xx<=x+6)
    if id=='minseo':
     a=np.array(im);pants=(a[:,:,2]>=a[:,:,0]*.75)&(a[:,:,1]>a[:,:,0]*.85);leg&=pants|(yy>=88)
    for name,lo,hi in [('thigh',hipY-3,split+2),('shin',split-2,shoeY+2),('shoe',shoeY,111)]:masks[side+name]=leg&(yy>=lo)&(yy<hi)
    joints[side]=[[49+(0 if side=='R'else face),hipY],[x,split],[x,95]]
   shoulder=[51 if face<0 else 46,shoulderY];elbow=[53 if face<0 else 44,61];wrist=[54 if face<0 else 43,70]
   nearPoly=[[shoulder[0]-4,shoulderY-2],[shoulder[0]+4,shoulderY-2],[wrist[0]+4,74],[wrist[0]-4,74]];m=np.array(layer(Image.new('RGBA',(96,112),(255,255,255,255)),nearPoly))[:,:,3]>0
   masks['Rupperarm']=m&(yy<=63);masks['Rforearm']=m&(yy>=59)
   farPoly=[[farX-4,shoulderY],[farX+3,shoulderY],[farX+3,72],[farX-6,72]];mfar=np.array(layer(Image.new('RGBA',(96,112),(255,255,255,255)),farPoly))[:,:,3]>0
   masks['Lupperarm']=mfar&(yy<=62);masks['Lforearm']=mfar&(yy>=59)
   body=(yy<=hipY+2)&~((m|mfar)&(yy>=shoulderY+3));arms={'R':[shoulder,elbow,wrist],'L':[[farX,shoulderY],[farX,61],[farX+face*2,69]]}
   if id=='minseo':
    a=np.array(im);apron=(a[:,:,0]>a[:,:,2]*1.25)&(a[:,:,0]>a[:,:,1]*1.05);body|=apron&(yy<=79)&(yy>=hipY)&(xx>=39)&(xx<=56)
   if id=='harin':
    poly=rect(36 if d=='left'else 48,59,47 if d=='left'else 56,74);body|=np.array(layer(Image.new('RGBA',(96,112),(255,255,255,255)),poly))[:,:,3]>0
   masks['body']=body
  # Ownership cleanup: exclude original A-pose hands from leg textures and crop forearms to actual skin/cuff.
  original=np.array(im);rgb=original[:,:,:3].astype(int);skin=(rgb[:,:,0]>rgb[:,:,1]*1.3)&(rgb[:,:,0]>rgb[:,:,2]*1.35)&(rgb[:,:,0]>170)&(rgb[:,:,2]<rgb[:,:,1]*.98);skinRing=binary_dilation(skin,iterations=1)&(original[:,:,3]>0)
  for name in list(masks):
   if 'forearm'in name:masks[name]&=(yy<64)|skinRing
   if any(n in name for n in ['thigh','shin']):
    if front:masks[name]&=(yy>75)|((xx>=39)&(xx<=58))
    else:masks[name]&=~(m&(yy<=74))
  bodyImage=im.copy()
  if not front:
   # Own same-row shirt/apron material recovers only the occluded torso beneath the extracted near sleeve.
   bodyPoly=[[46,44],[51,44],[53,51],[51,58],[52,hipY+2],[44,hipY+2],[43,55],[43,49]]if d=='left'else[[45,44],[50,44],[53,49],[54,55],[53,hipY+2],[45,hipY+2],[45,58],[43,51]]
   if id=='minseo':bodyPoly=[[46,47],[51,47],[53,52],[52,63],[55,78],[44,78],[42,67],[43,54]]if d=='left'else[[45,47],[50,47],[53,54],[54,67],[53,78],[42,78],[45,63],[43,52]]
   core=np.array(layer(Image.new('RGBA',(96,112),(255,255,255,255)),bodyPoly))[:,:,3]>0;body=(yy<=shoulderY)|core;recover=(m|(original[:,:,3]==0))&core&(yy>=shoulderY+1)
   own=np.array(im)
   for y,x in zip(*np.where(recover)):own[y,x]=original[y,45 if d=='left'else 51]
   bodyImage=Image.fromarray(own);masks['body']=body
   if id=='seoyeon'and d=='left':
    accessory=(xx>=37)&(xx<=42)&(yy>=55)&(yy<=74);masks['body']|=accessory;own[accessory]=original[accessory]
   if id=='harin':
    accessory=(xx>=(36 if d=='left'else 48))&(xx<=(47 if d=='left'else 56))&(yy>=59)&(yy<=74);masks['body']|=accessory;own[accessory]=original[accessory]
   bodyImage=Image.fromarray(own);patches.append({'purpose':'Under-near-arm torso occlusion recovery only','method':'Clone same-row own illustrated safe inner torso column45/51 only within authored torso silhouette polygon and occluded near-sleeve mask','pixels':int(recover.sum())})
  o=p/'layers'/d;o.mkdir(parents=True,exist_ok=True);ownership={}
  for name,mask in masks.items():
   a=np.array(bodyImage if name=='body'else im);a[~mask]=0;q=Image.fromarray(a);q.save(o/f'{name}.png');assert q.getbbox(),(id,d,name);ownership[name]={'source':f'native/{d}.png','visiblePixels':int((a[:,:,3]>0).sum()),'bounds':q.getbbox()}
  if not front:
   # Far limb is occluded in the source; recover it from THIS view's own visible sleeve/hand,not the torso or another actor.
   shift=farX-shoulder[0]
   for segment in ['upperarm','forearm']:
    nearImage=Image.open(o/f'R{segment}.png').convert('RGBA');farImage=Image.new('RGBA',(96,112));farImage.alpha_composite(nearImage,(shift,-1));farImage.save(o/f'L{segment}.png');ownership['L'+segment]['occlusionRecovery']={'source':f'R{segment}.png','translate':[shift,-1],'underTorso':True}
   arms['L']=[[v[0]+shift,v[1]-1]for v in arms['R']]
  cfg['views'][d]={'joints':joints,'arms':arms,'hipY':hipY,'near':near,'facing':0 if front else(-1 if d=='left'else 1),'ownership':ownership,'accessoryTorsoMasks':accessories,'clothRecovery':patches,'alphaMaskFiles':[str((o/f'{n}.png').relative_to(p))for n in masks]}
 (p/'rig.json').write_text(json.dumps(cfg,indent=2)+'\n');print(id,len(masks),'source-owned parts×4views;manualjoints andalphamasks')
if __name__=='__main__':
 for id in IDS:author(id)
