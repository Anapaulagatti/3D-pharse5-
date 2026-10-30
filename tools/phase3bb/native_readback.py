from pathlib import Path
import sys,json,math
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'phase2c'))
from compose import Composer
from core import *
D=R/'docs/phase3bb-hotfix/native';c=Composer();rows=[]
for r in json.loads((D/'CAPTURES.json').read_text()):
 a=r['audit'];s=a['state'];look=s['appearance'];ids=[i for i in [look['hairstyleId'],look['outfitId'],*look['accessoryIds']]if i];sprite=np.array(c.render(r['id'],ids,a['actualFrame']));shot=Image.open(D/r['file']).convert('RGB');sx,sy=a['camera']['scroll'];x=math.floor(s['x']+.5)-48-sx;y=math.floor(s['y']+.5)-100-sy;actual=shot.crop((x,y,x+96,y+112));diff=int(((sprite[:,:,3]==255)&np.any(np.array(actual)!=sprite[:,:,:3],2)).sum());assert diff==0,(r['id'],r['action'],r['view'],diff);assert a['camera']['zoom']==1 and all(float(v).is_integer()for v in[sx,sy]);assert s['samplingMode']==1
 crop=r['file'].replace('.png','-native-crop.png');actual.save(D/crop);rows.append({'character':r['id'],'action':r['action'],'view':r['view'],'frame':a['actualFrame'],'opaquePixels':int((sprite[:,:,3]==255).sum()),'mismatch':diff,'crop':crop})
report={'status':'PASS ACTUAL NATIVE PIXEL READBACK','captures':len(rows),'mismatch':sum(r['mismatch']for r in rows),'method':'Real Phaser POST_RENDER canvas pixels compared with independently decoded native source+head patches. Only opaque sprite pixels; background is not used to certify sprite art. Native zoom1, integer camera, nearest mode1.','rows':rows,'humanArtAcceptance':'PENDING','physicalDevices':'NOT TESTED'}
(R/'docs/phase3bb-hotfix/NATIVE_READBACK.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS',len(rows),'native Phaser captures; 0 opaque-pixel mismatch')
