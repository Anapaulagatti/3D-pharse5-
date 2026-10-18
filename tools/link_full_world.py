"""Rebase retained room source and verify actual full-world/room reciprocal navigation."""
from full_world_art import *
import time
old=R/'assets-src/living-korea/north/room-bundle.json'
def rebase(v):
 if isinstance(v,dict):return {k:(os.path.relpath((old.parent/a).resolve(),S)if k in ['manifest','image','data','source']and isinstance(a,str)and a.startswith('../')else rebase(a))for k,a in v.items()}
 if isinstance(v,list):return [rebase(a)for a in v]
 return v
b=rebase(json.loads(old.read_text()));b['id']='full-reading-room';b['portals']=[{'id':'return-world','circle':[384,536,20],'to':'full-korea:room-return','entranceByFrom':{'full-korea':[384,480]},'reciprocal':True}];write(S/'room-draft.json',b)
hashed=C/f'room-{sha(S/"room-draft.json")[:12]}.json'
if not hashed.exists():run(F/'skills/generate2dmap/scripts/map_bundle.py','hash','--bundle',S/'room-draft.json','--output',hashed)
if (S/'room-bundle.json').exists():shutil.copyfile(S/'room-bundle.json',C/f'prior-room-{sha(S/"room-bundle.json")[:12]}.json')
shutil.copyfile(hashed,S/'room-bundle.json')
for name,bundle,link in [('world',S/'map/outdoor-bundle.json',S/'room-bundle.json'),('room',S/'room-bundle.json',S/'map/outdoor-bundle.json')]:
 out=C/f'linked-{name}-{sha(bundle)[:12]}-{sha(link)[:12]}';out.mkdir(exist_ok=True)if False else None
 if not out.exists():run(F/'skills/generate2dmap/scripts/map_nav.py','check','--bundle',bundle,'--link',link,'--output-dir',out,'--publish-on-fail')
 dest=S/f'linked-{name}'
 if dest.exists():shutil.move(dest,C/f'previous-{name}-{time.time_ns()}')
 shutil.copytree(out,dest)
