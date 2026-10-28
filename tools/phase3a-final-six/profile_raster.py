"""Independently track actual native near-shoe raster, without trusting pose-key targets."""
from pathlib import Path
from PIL import Image
import numpy as np,json,sys
R=Path(__file__).resolve().parents[2];S=R/'assets-src/npcs/phase3a-final-six';D=R/'docs/phase3a-final-six';rows=[]
for id in sys.argv[1:]:
 for d,sign in [('left',-1),('right',1)]:
  shoe=Image.open(S/id/'layers'/d/'Rshoe.png').convert('RGBA');a=np.array(shoe);y,x=np.where((a[:,:,3]>0)&(np.indices(a.shape[:2])[0]>=shoe.getbbox()[3]-2));pattern=a[y,x];tracks=[]
  for i in range(5):
   f=np.array(Image.open(S/id/'frames'/f'walk-{d}-{i}.png').convert('RGBA'));found=[]
   for dy in range(-4,3):
    for dx in range(-28,29):
     yy,xx=y+dy,x+dx
     if yy.min()>=0 and yy.max()<112 and xx.min()>=0 and xx.max()<96 and np.array_equal(f[yy,xx],pattern):found.append([dx,dy])
   tracks.append({'frame':i,'matches':found,'worldSoleXAtNominalPhase':float(x.mean()+found[0][0]+sign*i*44/8)if len(found)==1 else None})
  values=[r['worldSoleXAtNominalPhase']for r in tracks];drift=max(values)-min(values)if all(v is not None for v in values)else None;rows.append({'id':id,'direction':d,'status':'PASS RASTER SCOPE'if drift is not None and drift<=1 else'WARN NOT VERIFIED','worldStanceDriftPixels':drift,'tracks':tracks,'method':'Actual near-shoe lowest2rowRGBA matching across5stance images; independent of rig target coordinates; nominal44px world stride'})
(D/'profile-raster-qa.json').write_text(json.dumps({'rows':rows,'humanGaitApproval':'PENDING','passes':sum(r['status']=='PASS RASTER SCOPE'for r in rows),'warnings':sum(r['status']!='PASS RASTER SCOPE'for r in rows)},indent=2)+'\n');print(len(rows),'independent raster tracks;',sum(r['status']=='PASS RASTER SCOPE'for r in rows),'PASS, remaining retained as WARN')
