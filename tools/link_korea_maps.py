"""Validate actual reciprocal heritage/room/Namsan graph with pinned Forge."""
from korea_art import *
import copy
M=F/'skills/generate2dmap/scripts';N=S/'north';BASE=R/'assets-src/world-refinement'
b=copy.deepcopy(json.loads((BASE/'room-bundle.json').read_text()))
def rebase(v):
 if isinstance(v,dict):
  for k,x in v.items():
   if k in ['manifest','image','source','data']and isinstance(x,str)and (BASE/x).is_file():v[k]=os.path.relpath((BASE/x).resolve(),N)
   else:rebase(x)
 elif isinstance(v,list):
  for x in v:rebase(x)
rebase(b);b['id']='korea-reading-room';b['portals']=[{'id':'korea-room-exit','circle':[384,510,14],'to':'korea-north:academy-return','entranceByFrom':{'korea-north':'start'},'latch':True,'reciprocal':True}];write(N/'room-draft.json',b)
out=C/f'room-{sha(N/"room-draft.json")[:16]}'/'bundle.json'
out.parent.mkdir(exist_ok=True)
if not out.exists():run(M/'map_bundle.py','hash','--bundle',N/'room-draft.json','--output',out)
shutil.copyfile(out,N/'room-bundle.json')
paths={'north':N/'outdoor-bundle.json','room':N/'room-bundle.json','park':S/'park/outdoor-bundle.json'}
fingerprint=hashlib.sha256(''.join(sha(p)for p in paths.values()).encode()).hexdigest()[:16]
for name,path in paths.items():
 dest=C/f'linked-{name}-{fingerprint}';args=['check','--bundle',path]
 for other,linked in paths.items():
  if other!=name:args+=['--link',linked]
 args+=['--output-dir',dest,'--publish-on-fail']
 if not dest.exists():run(M/'map_nav.py',*args)
 j=json.loads((dest/'nav-report.json').read_text());assert j['status']=='pass',(name,j)
 target=S/f'linked-{name}'
 if target.exists():shutil.move(target,C/f'previous-linked-{name}-{len(json.loads((S/"commands.json").read_text()))}')
 shutil.copytree(dest,target)
write(S/'linked-inputs.json',{'bundles':{k:{'file':str(p.relative_to(S)),'sha256':sha(p)}for k,p in paths.items()},'status':'PASS','explicitArrivalOutsideTravelTrigger':True,'runtimeRoomArtChanged':False})
