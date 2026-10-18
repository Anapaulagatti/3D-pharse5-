"""Route intent versus actual exported feet blockers; fixed clear widths, no art generation."""
from pathlib import Path
import json,math,hashlib
R=Path(__file__).resolve().parents[1];S=R/'assets-src/living-korea';D=R/'docs/living-korea'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
plan=json.loads((D/'southern-masterplan.json').read_text());park=next(z for z in plan['destinations']if z['id']=='namsan')
roads={'north':[
 {'id':'avenue-to-travel','width':80,'points':[[1152,832],[1152,1440],[1120,1664],[1152,1888],[1152,2016]]},
 {'id':'academy-side','width':64,'points':[[1152,1328],[944,1392],[768,1392],[768,1344],[544,1344],[544,1152]]},
 {'id':'workshop-front','width':64,'points':[[1152,1328],[1376,1344],[1376,1504],[1632,1536]]},
 {'id':'workshop-service','width':64,'points':[[1376,1344],[1440,1264],[1568,1264]]},
 {'id':'new-cross-lane','width':64,'points':[[1632,1616],[2240,1616]]},
 {'id':'museum-garden-front','width':64,'points':[[1632,1536],[1584,1760],[1640,2016],[1856,2064],[1984,2032],[1984,1920]]},
 {'id':'book-to-travel','width':64,'points':[[512,1872],[800,1920],[1152,2080]]},
 {'id':'royal-inner','width':48,'points':[[1152,320],[1152,544]]}],
 'park':[{'id':f'park-loop-{i+1}','width':64,'points':route}for i,route in enumerate(park['routes'])]+[{'id':'actual-overlook-stair','width':48,'points':[[1120,928],[1120,784]]}]}
fail=[];count=0;inputs={}
for name,routes in roads.items():
 bundle=S/name/'outdoor-bundle.json';b=json.loads(bundle.read_text());solids=b['collision']['solids'];inputs[name]=sha(bundle)
 for road in routes:
  for a,z in zip(road['points'],road['points'][1:]):
   dx,dy=z[0]-a[0],z[1]-a[1];length=math.hypot(dx,dy);nx,ny=-dy/length,dx/length
   for i in range(math.ceil(length/8)+1):
    t=min(1,i*8/length);x,y=a[0]+dx*t,a[1]+dy*t
    for side in [-1,0,1]:
     offset=side*(road['width']/2-10);px,py=x+nx*offset,y+ny*offset;count+=1
     for angle in [None,*range(0,360,45)]:
      xx=px+(0 if angle is None else 8*math.cos(math.radians(angle)));yy=py+(0 if angle is None else 4*math.sin(math.radians(angle)))
      hit=next((q for q in solids if q['x']<=xx<=q['x']+q['w']and q['y']<=yy<=q['y']+q['h']),None)
      if hit:
       if not any(f['road']==road['id']and f['reason']==hit['reason']for f in fail):fail.append({'zone':name,'road':road['id'],'point':[round(px,2),round(py,2)],'reason':hit['reason']})
       break
report={'status':'FAIL'if fail else'PASS','method':'Every8px centre and both clear-width shoulders, true8x4ellipse plus centre against all exported source rectangles. Public roads64/80, palace48, designed stair48; no renderer/test bypass.','sampledPositions':count,'inputs':inputs,'masterplanSha256':sha(D/'southern-masterplan.json'),'roads':roads,'failures':fail}
(D/'quality/road-clearance.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':report['status'],'samples':count,'failures':fail}));assert not fail
