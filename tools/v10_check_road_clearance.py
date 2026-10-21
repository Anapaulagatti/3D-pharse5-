"""Check approved centre lines with the final actor-footprint collision model."""
import sys,json
from pathlib import Path
sys.path.insert(0,'/workspace/tooling-cache/agent-sprite-forge/skills/generate2dmap/scripts')
import map_bundle,map_nav
from v10_plan import sample_points
R=Path(__file__).resolve().parents[1];bundle=map_bundle.load_bundle(R/'assets-src/v10-city/map/bundle-hashed.json');model=map_nav.collision_model(bundle);plan=json.loads((R/'assets-src/v10-city/plan/city.json').read_text());rows=[]
for road in plan['roads']:
 pts=sample_points(road);blocked=[]
 for a,b in zip(pts,pts[1:]):
  if not model.segment_clear(a,b):blocked.append([a,b])
 rows.append(dict(id=road['id'],segments=len(pts)-1,blocked=blocked))
result=dict(status='FAIL'if any(r['blocked']for r in rows)else'PASS',method='Exact final Forge actor-footprint model, every approved sampled centre-line segment',roads=rows)
(R/'docs/v10-production/road-clearance.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if result['status']!='PASS':sys.exit(1)
