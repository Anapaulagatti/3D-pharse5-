from pathlib import Path
import json,numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1];m=json.loads((R/'public/assets/gate3/aligned-world/manifest.json').read_text());sp=m['contactCollision'];atlas=json.loads((R/'public/assets/juni/juni.json').read_text())['frames'];im=Image.open(R/'public/assets/juni/juni.png').convert('RGBA');extra=set()
for n,fr in atlas.items():
 if not(n.startswith('stop-')or n.startswith('turn-')):continue
 f=fr['frame'];a=np.array(im.crop((f['x'],f['y'],f['x']+f['w'],f['y']+f['h'])))[:,:,3];bottom=np.where(a>0)[0].max();ys,xs=np.where((a>0)&(np.indices(a.shape)[0]>=bottom-3));extra.update((int(x-48),int(y-bottom-1))for x,y in zip(xs,ys))
for k in sp['footprints']:sp['footprints'][k]=sorted(set(map(tuple,sp['footprints'][k]))|extra)
Path('/tmp/g3df-stop-manifest.json').write_text(json.dumps(m))
s=(R/'tools/g3df_plan_walk.py').read_text().replace("R=Path(__file__).resolve().parents[1]","R=Path("+repr(str(R))+")").replace("json.loads((R/'public/assets/gate3/aligned-world/manifest.json').read_text())","json.loads(Path('/tmp/g3df-stop-manifest.json').read_text())");s=s[:s.index("add('palace-entrance'")]+"start=(3130,3460)\nadd('complete-bridge-to-jeju',astar(start,(3530,3640),True))\nPath('/tmp/g3df-stop-path.json').write_text(json.dumps(legs))\nprint('STOP/TURN NATIVE CONTACT ROUTE FOUND',len(legs[0]['points']),legs[0]['points'])\n";Path('/tmp/g3df_stop_plan.py').write_text(s)

# The generated planner is diagnostic only; no candidate/runtime asset is written.
import subprocess
result=subprocess.run(['python3','/tmp/g3df_stop_plan.py'],capture_output=True,text=True)
print(result.stdout or result.stderr)
print('Candidate unchanged. Strict stop/turn route:', 'FOUND' if result.returncode==0 else 'FAIL_NO_SAFE_ROUTE')
