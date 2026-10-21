"""Check every proposed public route against real shared native body templates."""
from city_geometry import *
b=json.loads((SOURCE/'map/draft.json').read_text());solids=b['collision']['solids'];fail=[];rows=[]
for r in PLAN['roads']:
 points=curve(r['points'],r.get('smooth',False),4);dense=[]
 for a,z in zip(points,points[1:]):
  n=max(1,math.ceil(math.dist(a,z)/4));dense.extend((a[0]+(z[0]-a[0])*i/n,a[1]+(z[1]-a[1])*i/n)for i in range(n))
 dense.append(points[-1]);bad=[]
 for x,y in dense:
  for s in solids:
   if s.get('shape')=='rect'and x+8>=s['x'] and x-8<=s['x']+s['w'] and y+4>=s['y']and y-4<=s['y']+s['h']:
    bad.append({'point':[round(x),round(y)],'reason':s['reason']});break
 if bad:fail.append({'route':r['id'],'count':len(bad),'examples':bad[::max(1,len(bad)//4)][:5]})
 rows.append({'id':r['id'],'points':points,'length':round(sum(math.dist(a,z)for a,z in zip(points,points[1:]))),'blockedSamples':len(bad)})
write(SOURCE/'plan/route-geometry-check.json',{'status':'FAIL'if fail else'PASS','actor':[8,4],'semanticSha256':hashlib.sha256(json.dumps({'collision':b['collision'],'roads':PLAN['roads']},sort_keys=True).encode()).hexdigest(),'failures':fail});write(SOURCE/'plan/navigation-routes.json',rows);print(json.dumps(fail,indent=2));assert not fail
