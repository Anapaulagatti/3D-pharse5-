"""Reproducible G3-A technical chunks. No new production artwork, scaling or source edits."""
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np
import json, hashlib
R=Path(__file__).resolve().parents[1]
OUT=R/'public/assets/gate3'; OUT.mkdir(parents=True,exist_ok=True)
P=json.loads((R/'assets-src/gate3/production-plan-v1.json').read_text()); plan=P['plan']
proof=[]
def scene(s): return json.loads((R/f'public/assets/gate2/{s}/scene.json').read_text())
def image(s): return Image.open(R/'public/assets/gate2'/s).convert('RGBA')
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def bake(kind,size,ground,walk,objects,spawn,targets,stops,regions):
 folder=OUT/kind;folder.mkdir(exist_ok=True);chunks=[]
 for y in range(0,size[1],512):
  for x in range(0,size[0],512):
   w,h=min(512,size[0]-x),min(512,size[1]-y); id=f'{x//512}-{y//512}'
   path=folder/f'{id}.png'; ground.crop((x,y,x+w,y+h)).save(path,optimize=True)
   mask=folder/f'{id}.bin'; mask.write_bytes(walk[y:y+h,x:x+w].astype('uint8').tobytes())
   chunks.append(dict(id=id,x=x,y=y,width=w,height=h,image=f'assets/gate3/{kind}/{id}.png',mask=f'assets/gate3/{kind}/{id}.bin',bytes=w*h*5,sha256=digest(path),maskSha256=digest(mask)))
 overview=ground.copy();overview.thumbnail((870,973),Image.Resampling.NEAREST)
 overview.save(folder/'overview.png',optimize=True)
 for o in objects:
  o['image']='assets/gate2/'+o['image'];o['bytes']=o['width']*o['height']*4
 data=dict(id=kind,size=size,spawn=spawn,targets=targets,stops=stops,chunks=chunks,objects=objects,regions=regions,overview=f'assets/gate3/{kind}/overview.png',budgetBytes=64*1024*1024,maxConcurrent=2,prototypeBaseline='01f4f954771595061d31cf2e8f53d49ce52910a0',coordinateMapping='identity / scale1 / integer native origins',artStatus='G3-A foundation; unpainted regions are engineering geometry, NOT production art')
 (folder/'manifest.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 proof.append(dict(scene=kind,chunks=len(chunks),size=size,maxTextureDimension=512,groundDecodedBytes=size[0]*size[1]*4,allGroundChunkPixelsExact=True,maskBytes=size[0]*size[1]))
 # Assert each runtime PNG/mask exactly matches the offline logical world, including all edges.
 for c in chunks:
  x,y,w,h=[c[k] for k in ['x','y','width','height']]
  assert np.array_equal(np.asarray(Image.open(OUT.parent.parent/c['image'])),np.asarray(ground.crop((x,y,x+w,y+h))))
  assert (OUT.parent.parent/c['mask']).read_bytes()==walk[y:y+h,x:x+w].tobytes()
 return data
size=plan['size']; ground=Image.new('RGBA',size,(34,61,75,255));d=ImageDraw.Draw(ground)
walk=Image.new('L',size,0);m=ImageDraw.Draw(walk)
def rect(r):x,y,w,h=r;return (int(x),int(y),int(x+w),int(y+h))
for r in plan['land']:
 d.rectangle(rect(r), fill='#52635b');x,y,w,h=r;m.rectangle((x+16,y+16,x+w-16,y+h-16),fill=255)
for z in plan['zones']:
 d.rectangle(rect(z['rect']),outline='#94a49b',width=3)
 d.text((z['rect'][0]+18,z['rect'][1]+18),z['id'].upper()+' / G3-B ART PENDING',fill='white')
for path in plan['paths']:d.line([tuple(v) for v in path['points']],fill='#8d8c7c',width=path['width'],joint='curve')
for b in plan['buildings']+plan['boundaries']+plan['landscapeSolids']:
 d.rectangle(rect(b['rect']),fill='#3b4448');x,y,w,h=b['rect'];m.rectangle((x-16,y-16,x+w+16,y+h+16),fill=0)
for r in plan['railKeepouts']:m.rectangle(rect([r[0]-16,r[1]-16,r[2]+32,r[3]+32]),fill=0)
for r in plan['overpasses']:m.rectangle(rect([r[0]+16,r[1]+16,r[2]-32,r[3]-32]),fill=255)
# Approved registered local collision proof includes mainland/bridge/arrival; no ferry traversal.
jmask=image('jeju-fit/walk.png').convert('L');walk.paste(jmask,(2350,3100))
objects=[];targets=[];regions=[];walkarr=np.array(walk,dtype=np.uint8)
for s,ox,oy in [('a',640,650),('c',3180,3200)]:
 data=scene(s);src=image(data['ground']);ground.paste(src,(ox,oy));mask=np.array(image(data['mask']).convert('L'))
 h,w=mask.shape;walkarr[oy:oy+h,ox:ox+w]=mask
 for o in data['objects']:
  o=o.copy();o['id']=s+'/'+o['id'];o['x']+=ox;o['y']+=oy;o['sortY']+=oy;objects.append(o)
 for t in data['targets']:targets.append(dict(t,id=s+'/'+t['id'],x=t['x']+ox,y=t['y']+oy))
 regions.append(dict(scene=s,rect=[ox,oy,w,h],status='approved native artwork / no scale change'))
 assert np.array_equal(np.asarray(ground)[oy:oy+h,ox:ox+w],np.asarray(src))
stops=[dict(id='coast',label='Jeju · coastal arrival',x=3460,y=3850,zoom=.5,travelMs=2000,holdMs=2100),dict(id='oreum',label='Jeju · oreum crater',x=3850,y=3405,zoom=.5,travelMs=2000,holdMs=2100),dict(id='orchard',label='Jeju · tangerine orchard',x=3940,y=4060,zoom=.5,travelMs=2000,holdMs=2100),dict(id='house',label='Jeju · cultural house',x=3635,y=4300,zoom=.5,travelMs=2000,holdMs=2100)]
bake('world',size,ground,walkarr,objects,plan['spawn'],targets,stops,regions)
data=scene('district-planter-repair');size=data['size'];ground=Image.new('RGBA',size)
for g in data['grounds']:ground.paste(image(g['image']),(g['x'],g['y']))
mask=np.array(image(data['mask']).convert('L'))
bake('district',size,ground,mask,data['objects'],data['spawn'],data['targets'],[dict(id=t['id'],label=t['label'],x=t['x'],y=t['y']-120,zoom=.5,travelMs=2000,holdMs=2100) for t in data['targets']], [{'status':'ISOLATED CACHE LAB / not a registered full-world district','rect':[0,0,*size]}])
(R/'docs/gate3a/chunk-generation-proof.json').write_text(json.dumps({'generator':'tools/gate3_assets.py','productionPlanSha256':digest(R/'assets-src/gate3/production-plan-v1.json'),'sourceResampling':False,'newProductionArtwork':False,'proof':proof},indent=2)+'\n')
print(json.dumps(proof))
