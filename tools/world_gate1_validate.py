"""Offline source preservation + conservative foot-clearance reachability, not art approval."""
import collections, hashlib, json, pathlib, subprocess
root=pathlib.Path(__file__).resolve().parents[1]
p=json.loads((root/'assets-src/world-gate1/plan.json').read_text())
def inside(x,y,r,m=0):return r[0]-m<=x<=r[0]+r[2]+m and r[1]-m<=y<=r[1]+r[3]+m
def original_free(x,y):return any(inside(x,y,r,-16) for r in p['land']) and not any(inside(x,y,b['rect'],16) for b in p['buildings']+p['boundaries']+p['landscapeSolids'])
def free(x,y):return original_free(x,y) and (not any(inside(x,y,r,16) for r in p['railKeepouts']) or any(inside(x,y,r,-16) for r in p['overpasses']))
step=16
start=tuple(round(v/step) for v in p['spawn']); seen={start}; queue=collections.deque([start])
while queue:
 x,y=queue.popleft()
 for v in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
  if v not in seen and free(v[0]*step,v[1]*step):seen.add(v);queue.append(v)
targets=[]
for b in p['buildings']+[{'id':n['id'],'entry':n['point']} for n in p['accessNodes']]:
 cell=tuple(round(v/step) for v in b['entry']);targets.append({'id':b['id'],'entry':b['entry'],'reachable':cell in seen})
assert all(t['reachable'] for t in targets),targets
base='ee70c54e0a9be56c02736988c30556ed122c074c'
# Entire old code/art/runtime remains unchanged. Metadata authority files are the only edits.
protected=[]
for prefix in ['src','public','assets-src/gate1','assets-src/protected-north','package.json','package-lock.json']:
 paths=subprocess.check_output(['git','ls-tree','-r','--name-only',base,'--',prefix],cwd=root,text=True).splitlines()
 for rel in paths:
  old=subprocess.check_output(['git','show',f'{base}:{rel}'],cwd=root)
  now=(root/rel).read_bytes();assert old==now,rel
  protected.append({'path':rel,'sha256':hashlib.sha256(now).hexdigest()})
imports={}
for f in (root/'src/world-gate1').glob('*.ts'):
 imports[str(f.relative_to(root))]=[l.strip() for l in f.read_text().splitlines() if l.startswith('import ')]
# No V1-V10 import or rejected-source helper in the new production source tree.
for f in [*(root/'src/world-gate1').glob('*'),root/'assets-src/world-gate1/plan.json']:
 text=f.read_text();assert not any(s in text for s in ['v10-city','v9-world','v10-production','gate1/map','gate1_build']),str(f)
prior=json.loads(subprocess.check_output(['git','show','21554fa:assets-src/world-gate1/plan.json'],cwd=root,text=True))
assert p['boundaries']==prior['boundaries']
for group,ids in [('buildings',['palace','gate','archive','academy','teahouse','culture']),('zones',['palace','academy','culture','transition']),('paths',['heritage-spine','academy-lane','archive-access','threshold','garden-walk'])]:
 for id in ids:assert next(x for x in p[group] if x['id']==id)==next(x for x in prior[group] if x['id']==id),(group,id)
assert p['land'][:5]==prior['land']
for id in ['tower','carousel','wheel']:
 assert next(x for x in p['buildings'] if x['id']==id)==next(x for x in prior['buildings'] if x['id']==id)
for id in ['tower','leisure']:
 assert next(x for x in p['zones'] if x['id']==id)==next(x for x in prior['zones'] if x['id']==id)
for id in ['tower-approach','leisure-access','leisure-garden-loop']:
 assert next(x for x in p['paths'] if x['id']==id)==next(x for x in prior['paths'] if x['id']==id)
assert next(x for x in p['zones'] if x['id']=='tower')['rect'][0]<2048
assert next(x for x in p['zones'] if x['id']=='leisure')['rect'][0]>2048
for e in p['facadeReserves']:
 assert e['rect'][1]>=2080 and e['rect'][3]==500 and e['nativeDoorHeight']==100
 a=next(x for x in p['buildings'] if x['id']==e['id']);old=next(x for x in prior['buildings'] if x['id']==e['id']);assert a['rect'][2:]==old['rect'][2:]
result={'northPlanExactVsPreviousReview':True,'jejuOutlineBridgeAndFerryPiersPreserved':True,'namsanAndAmusementGeometryPreserved':True,'stationPlatforms':2,'stationTracks':2,'fullSizeFacadeHeight':500,'doorToJuniBodyRatio':1.25,'compositionRestored':'Namsan southwest; amusement southeast','stage':p['stage'],'planSha256':hashlib.sha256((root/'assets-src/world-gate1/plan.json').read_bytes()).hexdigest(),'gridStep':step,'footClearance':16,'reachableCells':len(seen),'targets':targets,'preservedFileCount':len(protected),'preserved':protected,'imports':imports,'limits':['Reachability is geometric, not an art quality judgment.','Grid only; curved route and runtime collision tested separately in browser.','Legacy files retained as historical archive, excluded from the new entry dependency graph.']}
(root/'docs/world-gate1/source-and-navigation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'targets':len(targets),'reachable':sum(t['reachable'] for t in targets),'protected':len(protected),'planSha256':result['planSha256']}))
