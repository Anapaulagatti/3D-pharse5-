from pathlib import Path
import json,numpy as np
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-station-clean';m=json.loads((R/'public/assets/gate3/station-clean-world/manifest.json').read_text());f=np.zeros((4864,4352),np.uint8)
for c in m['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];f[y:y+h,x:x+w]=np.fromfile(R/'public'/c['mask'],np.uint8).reshape(h,w)
legs=[{'id':'fresh-station-entrance','points':[[2599,2760],[2599,2610]]},{'id':'platform-transfer-out','points':[[2599,2610],[2599,2680],[2930,2680],[2970,2680],[2970,2530]]},{'id':'platform-side-passage-and-return','points':[[2970,2530],[2970,2680],[2930,2680],[2930,2300],[2930,2680],[2599,2680],[2599,2760]]},{'id':'fresh-road-crossing-and-return','points':[[2599,2760],[2599,2840],[2599,2760]]}]
for i,leg in enumerate(legs):
 leg.update(scene='station-clean-world',entry='station',sceneResetBefore=i==0,gridTarget=leg['points'][-1]);bad=[]
 for a,b in zip(leg['points'],leg['points'][1:]):
  for t in np.linspace(0,1,int(np.linalg.norm(np.array(a)-b))+1):
   x,y=np.rint(np.array(a)*(1-t)+np.array(b)*t).astype(int)
   if not f[y,x]:bad.append([int(x),int(y)])
 assert not bad,(leg['id'],bad[:5])
(D/'walk-plan.json').write_text(json.dumps({'method':'One continuous original-control station route. Initial review spawn only; no in-movement teleport/frame/speed/collision override. New visible floor/legacy prop removal plus genuine platform transfer tested.','legs':legs},indent=2)+'\n')
