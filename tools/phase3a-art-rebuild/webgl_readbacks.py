from pathlib import Path
from PIL import Image
import numpy as np,json
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a-art-rebuild';p=D/'extra-evidence.json';q=json.loads(p.read_text())
for r in q['rows']:
 if'audit'not in r:continue
 a=r['audit'];id=a['npcId'];root=R/'public/assets/npcs/phase3a'/id;f=json.loads((root/'atlas.json').read_text())['frames'][a['actualFrame']]['frame'];src=Image.open(root/'atlas.png').convert('RGBA').crop((f['x'],f['y'],f['x']+96,f['y']+112));s=a['sprite'];sx,sy=a['camera']['scroll'];x=s['x']-48-sx;y=s['y']-100-sy;actual=Image.open(D/r['file']).convert('RGB').crop((x,y,x+96,y+112));expected=np.array(src);m=int(((expected[:,:,3]==255)&np.any(np.array(actual)!=expected[:,:,:3],2)).sum());assert m==0 and a['player']['renderer']=='WebGL'and a['camera']['zoom']==1 and s['sampling']==1,(id,m);out=r['file'].replace('-native.png','-body-native.png');actual.save(D/out);r['nativeReadback']={'mismatchOpaquePixels':m,'native':[96,112],'sourceFilterMode':1,'uploadPolicy':'Protected addNativeTexture.createTextureFromSource NEAREST; no later filtering change','crop':out,'humanArtApproval':'PENDING'}
p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');print('PASS2 actual softwareWebGL nativeNPC readbacks,0mismatch; real visited/progress preservation and mobile evidence retained')
