"""Independent raster-foot template tracking; not a claim of human art approval."""
from pathlib import Path
import json,subprocess,io,hashlib
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];D=R/'docs/phase2b-motion';S=R/'assets-src/characters/phase2b';ids=['sori','jiwon','nari','taeyang','yuna','hyunwoo'];BASE=json.loads((D/'before-manifest.json').read_text())['commit'];rows=[]
def foot_center(im,shoe,shift_y):
 a=np.array(im);s=np.array(shoe);bb=shoe.getbbox();ys,xs=np.where((s[:,:,3]>0)&(np.indices(s.shape[:2])[0]>=bb[3]-2));pattern=s[ys,xs];found=[]
 for dy in range(-4,1):
  for dx in range(-32,33):
   xx=xs+dx;yy=ys+shift_y+dy
   if min(xx)<0 or max(xx)>=96 or min(yy)<0 or max(yy)>=112:continue
   if np.array_equal(a[yy,xx],pattern):found.append((dx,dy))
 assert len(found)==1,found
 x=np.where(s[bb[3]-1,:,3]>0)[0].mean()+found[0][0];return float(x),int(bb[3]-1+shift_y+found[0][1])

for id in ids:
 root=S/id;cfg=json.loads((root/'rig.json').read_text())['right'];shoe=Image.open(root/'layers/right/Rshoe.png').convert('RGBA');shift=cfg['groundY']['R']-cfg['joints']['R'][2][1]
 stem=f'public/assets/characters/{id}/atlas';meta=json.loads((R/(stem+'.json')).read_text())['frames'];old=Image.open(io.BytesIO(subprocess.check_output(['git','show',BASE+':'+stem+'.png']))).convert('RGBA');new=Image.open(R/(stem+'.png')).convert('RGBA')
 for action,stride in [('walk',44),('run',64)]:
  record={'id':id,'action':action,'stride':stride,'method':'Near shoe two-row RGBA strip matched uniquely in full raster; no guide target used for location. At native phase keyposes, nominal world travel is i*stride/8.','before':[],'after':[]}
  for version,sheet in [('before',old),('after',new)]:
   for i in range(5):
    f=meta[f'{action}-right-{i}']['frame'];im=sheet.crop((f['x'],f['y'],f['x']+96,f['y']+112));
    try:x,y=foot_center(im,shoe,shift)
    except AssertionError as e:raise AssertionError((id,action,version,i,str(e)))
    record[version].append({'phaseIndex':i,'nativeSole':[x,y],'worldPointAtNominalPhase':[i*stride/8+x-48,y-100]})
  for version in ['before','after']:
   values=[p['worldPointAtNominalPhase'][0]for p in record[version]];record[version+'WorldStanceDriftPixels']=max(values)-min(values)
  assert record['beforeWorldStanceDriftPixels']>stride*.6,record
  assert record['afterWorldStanceDriftPixels']<=1,record
  assert all(record['after'][i+1]['nativeSole'][0]<record['after'][i]['nativeSole'][0]for i in range(4)),record
  rows.append(record)
(D/'directional-pixel-qa.json').write_text(json.dumps({'rows':rows,'beforeFailsForwardStance':True,'afterPassesQuantizedForwardStance':True,'limits':'Phase-sampled pixel motion, not continuous subpixel or3D mocap. Eight-pose hold quantization can move contact by up to one pose interval; real-world trace/video and artistic review are separate requirements.','thresholds':'New supplementary invariant; existing Forge thresholds unchanged. Maximum1native-pixel phase-sampled stance drift.'},indent=2)+'\n');print('Twelve right walk/run raster tracks: rejected before drift>60%stride; corrected drift<=1px')
