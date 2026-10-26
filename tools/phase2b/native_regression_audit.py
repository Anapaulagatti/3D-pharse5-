from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib,math
R=Path(__file__).resolve().parents[2];D=R/'docs/phase2b';q=json.loads((D/'native-regression.json').read_text());old=json.loads((R/'docs/phase1/native-captures.json').read_text());rows=[]
assert not q['errors']
for row in [r for r in q['rows']if'id'not in r]:
 before=next(r for r in old['rows']if r['phase']=='after'and r['entry']==row['entry']and r['renderer']==row['renderer']);a,b=before['audit'],row['audit'];assert a['camera']==b['camera'];assert b['camera']['zoom']==1;assert all(float(v).is_integer()for v in b['camera']['scroll']);im0=np.array(Image.open(R/'docs/phase1'/before['file']).convert('RGBA'));im1=np.array(Image.open(D/row['file']).convert('RGBA'));ok=np.ones(im0.shape[:2],bool);sx,sy=a['camera']['scroll']
 for state in [a['state'],b['state']]:
  x,y=round(state['x'])-sx,round(state['y'])-sy;ok[max(0,y-100):min(len(ok),y+12),max(0,x-48):min(ok.shape[1],x+48)]=False
 count=int((np.any(im0!=im1,2)&ok).sum());assert count==0,(row['file'],count);assert all(l['scaleMode']==1 for l in b['layers']);rows.append({'entry':row['entry'],'renderer':b['state']['renderer'],'pixelsCompared':int(ok.sum()),'worldChangedPixels':count,'sameNativeCamera':True,'nearest':True})
# Exact source pixels in native single-character station renders, except legitimate foreground.
m=json.loads((R/'public/assets/gate3/palace-cleanup-world/manifest.json').read_text());body=[];line=Image.new('RGBA',(576,112));comp=Image.new('RGB',(1440,224))
for i,row in enumerate(r for r in q['rows']if'id'in r):
 id=row['id'];a=row['audit'];state=a['state'];asset='assets/juni/juni'if id=='juni'else f'assets/characters/{id}/atlas';atlas=json.loads((R/'public'/f'{asset}.json').read_text());sheet=Image.open(R/'public'/f'{asset}.png').convert('RGBA');f=atlas['frames'][state['frame']]['frame'];sprite=sheet.crop((f['x'],f['y'],f['x']+96,f['y']+112));rgb=np.array(sprite);sx,sy=a['camera']['scroll'];cx,cy=math.floor(state['x']+.5),math.floor(state['y']+.5);x0,y0=cx-48-sx,cy-100-sy;shot=Image.open(D/row['file']).convert('RGB');actual=np.array(shot.crop((x0,y0,x0+96,y0+112)));cover=np.zeros((112,96),bool)
 for l in a['layers']:
  if not l['key'].startswith('f/')or not l['visible']or l['alpha']<=0:continue
  ob=next(o for o in m['objects']if'f/'+o['id']==l['key'])
  if ob['sortY']<=cy+.1:continue
  x,y,w,h=[ob[k]for k in ['x','y','width','height']];lx=max(cx-48,x);ly=max(cy-100,y);rx=min(cx+48,x+w);ry=min(cy+12,y+h)
  if lx<rx and ly<ry:cover[ly-cy+100:ry-cy+100,lx-cx+48:rx-cx+48]|=np.array(Image.open(R/'public'/ob['image']).getchannel('A').crop((lx-x,ly-y,rx-x,ry-y)))>0
 diff=(rgb[:,:,3]>0)&~cover&np.any(actual!=rgb[:,:,:3],2);assert not diff.any(),(id,int(diff.sum()));body.append({'id':id,'actualFrame':state['frame'],'unexplainedChangedPixels':int(diff.sum()),'nativeCell':[96,112],'sourceScale':[1,1],'nearest':True});crop=shot.crop((x0-72,y0-56,x0+168,y0+168));crop.save(D/f'{id}-station-native-crop.png');comp.paste(crop,(240*i,0));line.alpha_composite(sprite,(96*i,0))
comp.save(D/'six-native-gameplay-crops.png');comp.resize((2880,448),Image.Resampling.NEAREST).save(D/'six-gameplay-crops-2x.png');line.save(D/'actual-phaser-body-lineup-native.png');(D/'approved-six-native-pixel-qa.json').write_text(json.dumps({'pairedWorld':rows,'worldPixelsCompared':sum(r['pixelsCompared']for r in rows),'worldChangedPixels':0,'playerNativeReadback':body,'humanArtApproval':'APPROVED_PHASE2A'},indent=2)+'\n');print('PASS',sum(r['pixelsCompared']for r in rows),'unchanged world pixels,6native player readbacks exact')
