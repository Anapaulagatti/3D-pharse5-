"""Read-only acceptance data validation through pinned Forge; no image generation."""
from pathlib import Path
import json,subprocess,shutil,time,sys
from PIL import Image
R=Path(__file__).resolve().parents[1];P=R/'public/assets/gate2';D=R/'docs/gate2/acceptance/contracts';D.mkdir(parents=True,exist_ok=True);C=R/'.cache/gate2/acceptance/contracts';C.mkdir(parents=True,exist_ok=True);F=Path('/workspace/tooling-cache/agent-sprite-forge/skills/generate2dmap/scripts');calls=[]
def write(p,o):p.write_text(json.dumps(o,indent=2)+'\n')
def run(*args):
 r=subprocess.run(list(map(str,args)),cwd=R,capture_output=True,text=True);calls.append(dict(command=list(map(str,args)),exit=r.returncode,stdout=r.stdout,stderr=r.stderr));write(D/'commands.json',calls);assert r.returncode==0,(r.stdout,r.stderr)
for id in (sys.argv[1:] or ['original','station','seam','jeju-fit']):
 folder=C/id
 if folder.exists():shutil.move(str(folder),str(C/(id+'-previous-'+str(time.time_ns()))))
 folder.mkdir();s=json.loads((P/id/'scene.json').read_text());w,h=s['size'];layers=[]
 for i,g in enumerate(s.get('grounds',[dict(image=s['ground'],x=0,y=0)])):
  filename=f'ground{i}.png';shutil.copy2(P/g['image'],folder/filename);layers.append(dict(name=f'ground{i}',kind='image',image=filename,x=g['x'],y=g['y']))
 props={};objects=[]
 for o in s['objects']:
  filename=o['id']+'.png';shutil.copy2(P/o['image'],folder/filename);a=[o['width']/2,min(o['height'],max(0,o['sortY']-o['y']))];props[o['id']]=dict(image=filename,size=[o['width'],o['height']],anchor_px=a,solid=False,art_source='existing',occlusion_class='tall',occupant_policy='y_sort');objects.append(dict(id=o['id'],prop=o['id'],x=o['x']+a[0],y=o['y']+a[1],sortY=o['sortY'],anchor_px=a,scale=1))
 if objects:layers.append(dict(name='foreground',kind='objects'))
 mask=Image.open(P/s['mask']).convert('L');blocked=[]
 for y in range(0,h,8):
  start=None
  for x in range(0,w+8,8):
   off=x>=w or mask.getpixel((min(x+4,w-1),min(y+4,h-1)))<128
   if off and start is None and x<w:start=x
   if not off and start is not None:blocked.append(dict(shape='rect',x=start,y=y,w=x-start,h=min(8,h-y)));start=None
   if x>=w and start is not None:blocked.append(dict(shape='rect',x=start,y=y,w=w-start,h=min(8,h-y)));start=None
 bundle=dict(schema='generate2dmap.map_bundle.v2',id='gate2-acceptance-'+id,world=dict(width=w,height=h,unit='px'),art_source='host_image'if id=='original'else'existing',layers=layers,props=props,objects=objects,collision=dict(actorRadius=0,ySquash=1,solids=blocked),spawns=[dict(id='entry',x=s['spawn'][0],y=s['spawn'][1],facing='front')],anchors={t['id']:dict(point=[t['x'],t['y']],approach=[t['x'],t['y']])for t in s['targets']})
 write(folder/'bundle.json',bundle);run('python3',F/'map_bundle.py','hash','--bundle',folder/'bundle.json','--output',folder/'hashed.json');run('python3',F/'map_bundle.py','validate','--bundle',folder/'hashed.json','--report',folder/'bundle-report.json');run('python3',F/'map_nav.py','check','--bundle',folder/'hashed.json','--output-dir',folder/'nav','--publish-on-fail');run('python3',F/'build_scene_preview.py','--bundle',folder/'hashed.json','--output-dir',folder/'preview')
 out=D/id;out.mkdir(exist_ok=True);shutil.copy2(folder/'bundle-report.json',out/'bundle-report.json');shutil.copy2(folder/'nav/nav-report.json',out/'nav-report.json');print(id,'PASS',flush=True)
