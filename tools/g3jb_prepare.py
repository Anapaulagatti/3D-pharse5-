"""Freeze approved Hanbit/current world and exact TWO crossing edit masks BEFORE art."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,copy,hashlib,subprocess,numpy as np
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate3/jeju-bridges-v1';D=R/'docs/gate3-jeju-bridges'
def wr(p,q):p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
m=json.loads((R/'public/assets/gate3/station-clean-world/manifest.json').read_text());W,H=m['size']
if not(S/'baseline-lock.json').exists():wr(S/'baseline-lock.json',{'HEAD':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'manifest':m,'files':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for root in ['assets-src','public']for p in sorted((R/root).rglob('*'))if p.is_file()and'/jeju-bridges-'not in str(p)}})
# Polygons follow existing crossing corridors. No island landmark or ordinary road edits.
polys={'A':[(3020,3370),(3168,3370),(3150,3320),(3260,3320),(3260,3485),(3250,3498),(3370,3530),(3498,3580),(3545,3662),(3498,3700),(3410,3650),(3290,3630),(3160,3615),(3085,3560),(3035,3520)],'B':[(3030,3880),(3170,3915),(3200,3945),(3340,3970),(3460,4000),(3600,3990),(3610,4110),(3515,4120),(3380,4115),(3210,4090),(3100,4070),(3040,4010)]}
mask=Image.new('L',(W,H));dr=ImageDraw.Draw(mask)
for p in polys.values():dr.polygon(p,fill=255)
mask.save(S/'edit-scope-mask.png');g=Image.new('RGBA',(W,H));f=np.zeros((H,W),np.uint8)
for c in m['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];g.paste(Image.open(R/'public'/c['image']),(x,y));f[y:y+h,x:x+w]=np.fromfile(R/'public'/c['mask'],np.uint8).reshape(h,w)
for o in sorted(m['objects'],key=lambda o:o['sortY']):g.alpha_composite(Image.open(R/'public'/o['image']).convert('RGBA'),(o['x'],o['y']))
g.save(S/'before-static-world.png');Image.fromarray(f).save(S/'before-walkable.png');origin=[2816,3200];crop=g.crop((2816,3200,4352,4224));crop.save(S/'before-two-crossings.png');guide=crop.copy();dr=ImageDraw.Draw(guide)
for name,p in polys.items():
 pp=[(x-2816,y-3200)for x,y in p];dr.line(pp+[pp[0]],fill='#ff39be',width=2);dr.text(pp[0],name,fill='white',stroke_width=1,stroke_fill='black')
guide.save(S/'exact-edit-guide.png')
frames={'bridge-a-full':[3310,3540],'bridge-a-mainland':[3120,3480],'bridge-a-island':[3470,3630],'bridge-b-full':[3340,4020],'bridge-b-mainland':[3130,4000],'bridge-b-island':[3540,4070]};entries={k:([3010,3460]if k.startswith('bridge-a')else[3030,3920])for k in frames}
for scene in ['jeju-bridges-before','jeju-bridges-world']:
 q=copy.deepcopy(m);q.update(id=scene,artStatus='HANBIT APPROVED LOCKED / TWO JEJU CROSSINGS HUMAN REVIEW');q['nativeFrames'].update(frames);q['reviewEntries'].update(entries);wr(R/'public/assets/gate3'/scene/'manifest.json',q)
wr(S/'scope.json',{'baseline':json.loads((S/'baseline-lock.json').read_text())['HEAD'],'origin':origin,'sourceSize':[1536,1024],'polygons':polys,'bounds':{k:[min(x for x,y in p),min(y for x,y in p),max(x for x,y in p)-min(x for x,y in p)+1,max(y for x,y in p)-min(y for x,y in p)+1]for k,p in polys.items()},'protected':'Entire world outside polygons, all source files, approved station/art/registration/entrance/platform; oreum/orchard/house/island paths outside bridge approach. No ordinary road movement or protected endpoint relocation.','ownership':'A original native Jeju deck plus4 alignment foreground rail objects; B original native Jeju ground, no independent foreground. Prior QA covers A only, not B.','policy':'Actual changes must be subset of exact masks. Bridge widening may extend visible supported DECK over water locally, never new island/mainland land. Any protected-reservation conflict stays uninstalled.'})
print('Frozen two separate crossings/masks and',len(json.loads((S/'baseline-lock.json').read_text())['files']),'immutable files')
