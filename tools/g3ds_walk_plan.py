from pathlib import Path
import json,numpy as np
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-final';m=json.loads((R/'public/assets/gate3/final-world/manifest.json').read_text());field=np.zeros((4864,4352),np.uint8)
for c in m['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];field[y:y+h,x:x+w]=np.fromfile(R/'public'/c['mask'],np.uint8).reshape(h,w)
legs=[
 {'id':'farm-six-plot-aisles','scene':'final-world','entry':'farm','sceneResetBefore':True,'points':[[500,810],[500,720],[570,720],[570,480],[1000,480],[1000,690],[500,690],[500,810]]},
 {'id':'western-house-approach-and-return','scene':'final-world','entry':'western-house','sceneResetBefore':True,'points':[[800,1390],[800,1400],[440,1400],[440,1030],[600,1030],[440,1030],[440,1400],[800,1400]]},
 {'id':'courtyard-public-circulation','scene':'final-world','entry':'western-courtyard','sceneResetBefore':True,'points':[[900,1400],[580,1400],[580,1650],[580,1400],[1100,1400],[900,1400]]},
 {'id':'new-station-entrance','scene':'final-station-candidate','entry':'station','sceneResetBefore':True,'points':[[2598,2760],[2598,2630],[2598,2610],[2598,2760]]},
 {'id':'new-station-crosswalk','scene':'final-station-candidate','entry':'station','sceneResetBefore':False,'points':[[2598,2760],[2598,2855],[2598,2760]]},
]
old=json.loads((R/'docs/gate3-residual/walk-plan.json').read_text())
for i,id in enumerate(['complete-bridge-to-jeju','complete-jeju-to-mainland']):
 q=next(q for q in old['legs']if q['id']==id);legs.append({**q,'scene':'final-world','entry':'bridge-mainland','sceneResetBefore':i==0})
for leg in legs:
 bad=[]
 for a,b in zip(leg['points'],leg['points'][1:]):
  for t in np.linspace(0,1,int(np.linalg.norm(np.array(a)-b))+1):
   x,y=np.rint(np.array(a)*(1-t)+np.array(b)*t).astype(int)
   if not field[y,x]:bad.append([int(x),int(y)])
 assert not bad,(leg['id'],bad[:10])
 leg['gridTarget']=leg['points'][-1]
(D/'walk-plan.json').write_text(json.dumps({'method':'Declared independent review-scene starts for farm/house/courtyard/station/bridge; continuous actual movement within each case. Final two bridge legs continuous outward and return. No in-movement teleport, speed, atlas or collision overrides.','legs':legs},indent=2)+'\n');print('Planned',len(legs),'actual-control cases; all centerline field samples valid')
