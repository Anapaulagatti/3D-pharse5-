from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a';reg=json.loads((R/'assets-src/npcs/phase3a/registry.json').read_text())['npcs'];assert len(reg)==14;assert len({n['id']for n in reg})==14;zones={z:sum(n['homeZone']==z for n in reg)for z in {n['homeZone']for n in reg}};assert len(zones)==7 and all(n==2 for n in zones.values());rows=[]
for n in reg:
 atlas=Image.open(R/'public'/n['assets']['texture']).convert('RGBA');meta=json.loads((R/'public'/n['assets']['atlas']).read_text())['frames'];assert atlas.size==(768,1456)and len(meta)==104;frames={}
 for key,row in meta.items():
  f=row['frame'];assert f['w']==96 and f['h']==112;im=atlas.crop((f['x'],f['y'],f['x']+96,f['y']+112));a=np.array(im);assert set(np.unique(a[:,:,3]))<={0,255};bb=im.getbbox();assert bb and 0<bb[0]<bb[2]<96 and 0<bb[1]<bb[3]<112;frames[key]=im
 for name,clip in n['animations'].items():
  assert all(k in frames for k in clip['frames']);assert len(clip['frames'])==len(clip['durationsMs']);unique=len({frames[k].tobytes()for k in clip['frames']});assert not name.startswith('walk')or unique==8,(n['id'],name,unique)
 # Independent native contact extraction, not the authoring guide: y98 is the planted outsole raster.
 stance={}
 for direction in ['right','left']:
  world=[];soles=[]
  for i in range(5):
   a=np.array(frames[f'walk-{direction}-{i}']);xs=np.where(a[98,:,3]>0)[0];groups=np.split(xs,np.where(np.diff(xs)>1)[0]+1);groups=[g for g in groups if len(g)>2];assert groups
   if i==0:g=max(groups,key=lambda g:g.mean())if direction=='right'else min(groups,key=lambda g:g.mean())
   elif i==4:g=min(groups,key=lambda g:g.mean())if direction=='right'else max(groups,key=lambda g:g.mean())
   else:assert len(groups)==1,(n['id'],direction,i,[g.tolist()for g in groups]);g=groups[0]
   x=float(g.mean());soles.append(x);world.append(x+(1 if direction=='right'else-1)*i*44/8)
  drift=max(world)-min(world);assert drift<=1.0,(n['id'],direction,drift);stance[direction]={'actualNativeSoleX':soles,'worldStanceAtNominalPhase':world,'driftPixels':drift,'limit':1.0}
 rows.append({'id':n['id'],'zone':n['homeZone'],'frames':len(frames),'walkDistinctPerDirection':8,'native':[96,112],'anchor':[48,100],'atlasSHA256':hashlib.sha256((R/'public'/n['assets']['texture']).read_bytes()).hexdigest(),'profileContactStance':stance,'sourceArt':'Own native construction; approved Juni motion LANDMARKS only; no player face/costume pixels imported'})
q={'status':'PASS TECHNICAL — ARTISTIC APPROVAL PENDING','npcs':14,'zones':zones,'nativeFrames':sum(r['frames']for r in rows),'nativeWalkFrames':448,'rows':rows,'worldCollision':'Original unchanged fields,validated separately','physicalDevices':'NOT TESTED'};(D/'source-qa.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');print('PASS14NPC/7zones/1456nativeframes/448distinctwalkposes; native profile ground stance<=1.0px')
