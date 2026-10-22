"""Collision-aware walking audit. Grid minima and signed itineraries are distinct metrics."""
import json,pathlib,subprocess,math,hashlib
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra
root=pathlib.Path(__file__).resolve().parents[1]
BASE='21554fac5f3037d51ea3db3e1d79247ce772668e'
def model(p):
 step=16; w=p['size'][0]//step+1;h=p['size'][1]//step+1
 yy,xx=np.mgrid[:h,:w];xx=xx*step;yy=yy*step
 def mask(r,m=0):return (xx>=r[0]-m)&(xx<=r[0]+r[2]+m)&(yy>=r[1]-m)&(yy<=r[1]+r[3]+m)
 free=np.zeros((h,w),bool)
 for r in p['land']:free|=mask(r,-16)
 for b in p['buildings']+p['boundaries']+p.get('landscapeSolids',[]):free&=~mask(b['rect'],16)
 rail=np.zeros_like(free)
 for r in p.get('railKeepouts',[]):rail|=mask(r,16)
 for r in p.get('overpasses',[]):rail&=~mask(r,-16)
 free&=~rail
 indices=np.full((h,w),-1,int);indices[free]=np.arange(free.sum());rows=[];cols=[];weights=[]
 for dy,dx in [(0,1),(1,0),(1,1),(1,-1)]:
  a_y,a_x=np.nonzero(free);b_y=a_y+dy;b_x=a_x+dx
  valid=(b_y>=0)&(b_y<h)&(b_x>=0)&(b_x<w);a_y,a_x,b_y,b_x=[v[valid] for v in [a_y,a_x,b_y,b_x]]
  valid=free[b_y,b_x]
  if dy and dx:valid &= free[a_y,b_x]&free[b_y,a_x]
  a=indices[a_y[valid],a_x[valid]];b=indices[b_y[valid],b_x[valid]]
  rows.extend([a,b]);cols.extend([b,a]);weights.extend([np.full(len(a),step*math.hypot(dx,dy))]*2)
 graph=coo_matrix((np.concatenate(weights),(np.concatenate(rows),np.concatenate(cols))),shape=(free.sum(),free.sum())).tocsr()
 nodes=[{'id':b['id'],'label':b['label'],'point':b['entry']} for b in p['buildings']]+p['accessNodes']
 node_indices=[]
 for n in nodes:
  x,y=[round(v/step) for v in n['point']]
  assert free[y,x],n
  node_indices.append(indices[y,x])
 ds=dijkstra(graph,indices=node_indices,directed=False)
 pairs=[]
 for i,a in enumerate(nodes):
  for j,b in enumerate(nodes):
   if i>=j:continue
   length=float(ds[i,node_indices[j]]);assert math.isfinite(length),(a,b)
   pairs.append({'from':a['id'],'to':b['id'],'worldPx':round(length,1),'walkSeconds':round(length/60,2),'runSeconds':round(length/100,2)})
 nearest=[]
 for a in nodes:
  relevant=[r for r in pairs if a['id'] in [r['from'],r['to']]];best=min(relevant,key=lambda r:r['worldPx']);nearest.append({'id':a['id'],'nearest':best['to'] if best['from']==a['id'] else best['from'],'walkSeconds':best['walkSeconds']})
 return {'nodes':nodes,'pairs':pairs,'nearest':nearest,'gridStep':step,'noCornerCutting':True,'walkSpeed':60,'runSpeed':100,'metric':'8-neighbor collision-grid minimum; not an authored path distance or browser wall-clock measurement'}
before=json.loads(subprocess.check_output(['git','show',f'{BASE}:assets-src/world-gate1/plan.json'],cwd=root,text=True));after=json.loads((root/'assets-src/world-gate1/plan.json').read_text())
result={'currentPlanSha256':hashlib.sha256((root/'assets-src/world-gate1/plan.json').read_bytes()).hexdigest(),'baselineCommit':BASE,'before':model(before),'after':model(after),'limits':['16px grid approximation; actual input travel timing is reported separately.','Free public ground can be walked: shorter signposted routes do not falsely imply the old geometry had no shortcut.','No operating train or ferry is counted in walking results.','No approved movement speed was changed.']}
(root/'docs/world-gate1/exploration-pacing.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'beforeNodes':len(result['before']['nodes']),'afterNodes':len(result['after']['nodes']),'allReachable':True,'longestWalkSeconds':max(r['walkSeconds'] for r in result['after']['pairs'])}))
