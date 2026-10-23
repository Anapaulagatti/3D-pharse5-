"""Destination coverage is an inventory, never a declaration of artistic acceptance."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-world';D.mkdir(exist_ok=True);p=json.loads((R/'assets-src/gate3/production-plan-v3.1-restored.json').read_text())['plan'];rows=[]
for kind,key in [('district','zones'),('destination','buildings'),('landscape','features'),('access','accessNodes')]:
 for item in p[key]:rows.append({'id':kind+'/'+item['id'],'label':item.get('label',item['id']),'reservation':item.get('rect',item.get('point',item.get('entry'))),'status':'PENDING_INVENTORY_VALIDATION','artAcceptance':'PENDING / new work requires consolidated human review'})
rows.append({'id':'destination/bakery','label':'오월제과 Bakery','status':'BLOCKED_PLACEMENT / COMPLETE_STANDALONE_ASSET','reservation':None,'artAcceptance':'APPROVED_STANDALONE / world placement deferred'})
for item in p['station']['platforms']:rows.append({'id':'rail/'+item['id'],'reservation':item['rect'],'status':'PENDING_INVENTORY_VALIDATION'})
for item in p['station']['tracks']:rows.append({'id':'rail/'+item['id'],'reservation':item['points'],'status':'PENDING_INVENTORY_VALIDATION'})
(D/'coverage.json').write_text(json.dumps({'plan':'assets-src/gate3/production-plan-v3.1-restored.json','fullCoverageClaim':False,'items':rows},ensure_ascii=False,indent=2)+'\n');print(len(rows),'required coverage entries')
