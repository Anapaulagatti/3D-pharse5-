"""Independent literal head-pixel stability control for third-party matcher diagnostics."""
from pathlib import Path
import json,sys,numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[2];S=R/'assets-src/npcs/phase3a-final-six';rows=[];T=json.loads((R/'assets-src/characters/phase1b-frontback-juni/juni-motion-template.json').read_text())['clips']
for id in sys.argv[1:]:
 for d in ['front','back','left','right']:
  own=np.array(Image.open(S/id/'native'/f'{d}.png').convert('RGBA'));ref=T['walk-'+d]if d in ['front','back']else None
  for i in range(8):
   q=np.array(Image.open(S/id/'frames'/f'walk-{d}-{i}.png').convert('RGBA'));dx=ref[i]['bodyDeltaX']if ref else 0;dy=ref[i]['bodyDeltaY']if ref else -round(abs(np.sin(i*np.pi/4)));ys,xs=np.where((own[:,:,3]>0)&(np.indices(own.shape[:2])[0]<44));diff=int(np.any(q[ys+dy,xs+dx]!=own[ys,xs],axis=1).sum());assert diff==0,(id,d,i,diff);rows.append({'id':id,'frame':f'walk-{d}-{i}','actualOwnHeadPixelsCompared':len(xs),'mismatch':diff,'nativeBodyTranslation':[int(dx),int(dy)]})
(R/'docs/phase3a-final-six/head-stability.json').write_text(json.dumps({'status':'PASS','samples':len(rows),'rows':rows,'method':'Literal own illustrated opaque head RGBA pixels compared at exact authored pose translation;no image-matching heuristic or copied player face'},indent=2)+'\n');print('PASS own-head literal frame comparisons; see actual sample count in report')
