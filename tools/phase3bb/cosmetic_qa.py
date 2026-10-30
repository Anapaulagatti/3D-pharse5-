from pathlib import Path
import sys,json,hashlib
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'phase2c'))
from compose import Composer
from core import *
c=Composer();rows=[]
for item in c.catalog['items']:
 for v in item['variants']:
  frames=c.base(v['characterId']);patch=c.patch(v);assert set(frames)==set(patch)
  total=0
  for name,(p,e) in patch.items():
   assert p.size==e.size==(96,112)
   assert set(np.unique(np.array(p)[:,:,3]))<={0,255};assert set(np.unique(np.array(e)[:,:,3]))<={0,255}
   result=apply(frames[name],(p,e));assert result.getbbox();total+=1
   if '/phase3bb/'in v['paint']:
    assert np.array_equal(np.array(result)[80:],np.array(frames[name])[80:]),(item['id'],name,'head cosmetic touched feet')
  rows.append({'item':item['id'],'character':v['characterId'],'frames':total,'headRevision':'/phase3bb/'in v['paint']})
# Compare old/derived content explicitly; the original patch files remain untouched.
q=json.loads((R/'docs/phase3bb-hotfix/HAIR_REPAIR.json').read_text())
for r in q['variants']:
 item=c.items[r['item']];v=next(x for x in item['variants']if x['characterId']==r['character']);prov=json.loads((R/'public'/v['provenance']).read_text());old=decode(prov['previousVariant']);new=decode(v);r['changed']=sum(a[0].tobytes()!=new[k][0].tobytes()or a[1].tobytes()!=new[k][1].tobytes()for k,a in old.items())
(R/'docs/phase3bb-hotfix/HAIR_REPAIR.json').write_text(json.dumps(q,indent=2)+'\n')
report={'status':'PASS STRUCTURAL; visual human review pending','items':len(c.items),'variants':len(rows),'frames':sum(r['frames']for r in rows),'rows':rows,'checks':['every atlas frame mapped','binary alpha','native96x112','head variants leave bottom32 rows/feet pixel-identical'],'artisticAcceptance':'PENDING','physicalDevices':'NOT TESTED'}
(R/'docs/phase3bb-hotfix/COSMETIC_QA.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status'],report['variants'],report['frames'])
