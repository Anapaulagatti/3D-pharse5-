"""Protected baseline, real Forge map contracts/nav and native-source integrity."""
from pathlib import Path
import json,subprocess,hashlib,shutil,time
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate2';P=R/'public/assets/gate2';D=R/'docs/gate2';F=Path('/workspace/tooling-cache/agent-sprite-forge/skills/generate2dmap/scripts');log=[]
def write(p,o):p.write_text(json.dumps(o,indent=2)+'\n')
def run(*args):
 p=subprocess.run(list(map(str,args)),cwd=R,capture_output=True,text=True);log.append(dict(command=list(map(str,args)),exit=p.returncode,stdout=p.stdout,stderr=p.stderr));write(D/'forge-commands.json',log);return p.returncode
base='e0a5c0aeff1a2980042983e6091abff11b987fad';protected=[]
for prefix in ['src','public/assets/juni','assets-src/world-gate1','assets-src/protected-north','assets-src/gate1','assets-src/library','package.json','package-lock.json']:
 paths=subprocess.check_output(['git','ls-tree','-r','--name-only',base,'--',prefix],cwd=R,text=True).splitlines()
 for rel in paths:
  old=subprocess.check_output(['git','show',f'{base}:{rel}'],cwd=R);assert old==(R/rel).read_bytes(),rel;protected.append(dict(path=rel,sha256=hashlib.sha256(old).hexdigest()))
rows=[]
for s in json.loads((S/'scenes.json').read_text()):
 id=s['id'];folder=S/'maps'/id;archive=R/'.cache/gate2/previous-verify'/str(time.time_ns())/id;archive.mkdir(parents=True)
 for old in ['hashed-bundle.json','bundle-report.json','nav']:
  if (folder/old).exists():shutil.move(str(folder/old),str(archive/old))
 b=json.loads((folder/'bundle.json').read_text());b['props']={};b['objects']=[]
 for o in s['objects']:
  src=P/o['image'];name=o['id']+'.png';shutil.copy2(src,folder/name);anchor=[o['width']/2,min(o['height'],max(0,o['sortY']-o['y']))]
  b['props'][o['id']]=dict(image=name,size=[o['width'],o['height']],anchor_px=anchor,solid=False,art_source='existing'if id=='b'else'host_image',occlusion_class='tall',occupant_policy='y_sort')
  b['objects'].append(dict(id=o['id'],prop=o['id'],x=o['x']+anchor[0],y=o['y']+anchor[1],sortY=o['sortY'],scale=1,anchor_px=anchor))
 if b['objects']:b['layers'].append(dict(name='native-depth-layers',kind='objects'))
 write(folder/'bundle.json',b)
 assert run('python3',F/'map_bundle.py','hash','--bundle',folder/'bundle.json','--output',folder/'hashed-bundle.json')==0
 assert run('python3',F/'map_bundle.py','validate','--bundle',folder/'hashed-bundle.json','--report',folder/'bundle-report.json')==0
 nav=run('python3',F/'map_nav.py','check','--bundle',folder/'hashed-bundle.json','--output-dir',folder/'nav','--publish-on-fail')
 rows.append(dict(scene=id,forgeNavigationExit=nav,bundleReport=str((folder/'bundle-report.json').relative_to(R))))
 im=Image.open(P/id/'ground.png').convert('RGBA');assert list(im.size)==s['size'];assert set(im.getchannel('A').get_flattened_data())<={0,255}
 if id in ['a','c','transition']:assert Image.open(S/'originals'/({'a':'north','c':'jeju'}.get(id,id)+'.png')).size==im.size
 if id=='b':assert ImageChops.difference(im,Image.open(R/'assets-src/gate1/native/street-foundation.png').convert('RGBA')).getbbox() is None
write(D/'source-preservation.json',dict(approvedBaseline=base,protectedFiles=len(protected),preserved=protected,sceneChecks=rows,approvedPlanModified=False,gate3='LOCKED',sourcePixels='A/B/C/transition 1:1; station1254→720 uniform authoring finish documented; no Jeju minification'))
print(json.dumps({'protectedFiles':len(protected),'sceneChecks':rows}))
