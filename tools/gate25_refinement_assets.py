"""Strict local environment refinement: immutable prior ground, binary edit masks, native chunks."""
from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import binary_dilation,label
import json,hashlib,numpy as np
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate25-refinement';D=R/'docs/gate25-refinement';P=R/'public/assets/gate2';O=P/'district-refinement';W,H=3184,1214
base=Image.open(R/'assets-src/gate25-reconstruction/reconstructed-ground.png').convert('RGB');ground=base.copy();protected=np.array(Image.open(R/'assets-src/gate25-reconstruction/architecture-protection-final.png'))>0;owned=np.zeros((H,W),bool);regions=[]
for name,box,poly in [
 ('west',(1290,130,1720,780),[(1494,130),(1568,130),(1568,772),(1469,772),(1469,286),(1494,286)]),
 ('east-context',(2290,0,2860,780),[(2434,130),(2740,130),(2740,303),(2547,303),(2547,772),(2434,772)])]:
 raw=Image.open(S/(name+'-host.png')).convert('RGB');finish=raw.resize((box[2]-box[0],box[3]-box[1]),Image.Resampling.NEAREST);finish.save(S/(name+'-finished.png'))
 full=Image.new('RGB',(W,H));full.paste(finish,box[:2]);mask=Image.new('L',(W,H));ImageDraw.Draw(mask).polygon(poly,fill=255);a=(np.array(mask)>0)&(~protected);owned|=a;ground.paste(full,(0,0),Image.fromarray(a.astype('uint8')*255));Image.fromarray(a.astype('uint8')*255).save(S/(name+'-edit-mask.png'));regions.append(dict(name=name,sourceCrop=box,editPolygon=poly,pixels=int(a.sum()),hostNativeSize=raw.size))
# Four subtle foliage accents; original path, bed outline and all border/cap pixels stay exact.
sheet=Image.open(S/'planting-variation-host.png').convert('RGB').resize((640,320),Image.Resampling.NEAREST);sheet.save(S/'planting-variation-finished.png');panels=json.loads((S/'planting-panels.json').read_text());arr=np.array(base).astype(float)
for i,box in enumerate(panels):
 x0,y0,x1,y1=box;v=arr[y0:y1,x0:x1];green=(v[:,:,1]>v[:,:,0]*1.03)&(v[:,:,1]>v[:,:,2]*1.10)&(v[:,:,1]>45);mask=binary_dilation(green,iterations=4)
 mask[:40]=False;mask[146:]=False;mask[:,:18]=False;mask[:,-18:]=False
 # Keep boundary foliage tips unchanged; edit individual leaf/flower interiors, not a rectangular patch.
 local=sheet.crop(((i%2)*320,(i//2)*160,(i%2+1)*320,(i//2+1)*160));full=Image.new('RGB',(W,H));full.paste(local,(x0,y0));a=np.zeros((H,W),bool);a[y0:y1,x0:x1]=mask;a&=~protected;owned|=a;ground.paste(full,(0,0),Image.fromarray(a.astype('uint8')*255));regions.append(dict(name='foliage-'+str(i+1),sourceCrop=box,pixels=int(a.sum())))
new=np.array(ground);old=np.array(base);changed=(new!=old).any(2);assert np.array_equal(new[protected],old[protected]);assert not np.any(changed&(~owned));ground.save(S/'final-ground.png');Image.fromarray(owned.astype('uint8')*255).save(S/'combined-edit-mask.png');ground.resize((1592,607),Image.Resampling.NEAREST).save(S/'authoring-review.png')
scene=json.loads((P/'district-reconstruction/scene.json').read_text());previous=json.loads(json.dumps(scene));scene.update(id='district-refinement',label='Gate2.5 · final composition refinement / approval pending',grounds=[])
for name,x,end in [('west',0,1512),('center',1512,2488),('east',2488,W)]:
 ground.crop((x,0,end,H)).save(O/(name+'.png'));scene['grounds'].append(dict(id=name,image='district-refinement/'+name+'.png',x=x,y=0,width=end-x,height=H))
# Only the two redesigned passages receive collision changes; all preexisting primary routes/bed paths untouched.
walk=Image.open(P/'district-reconstruction/walk.png').convert('L');before=np.array(walk);wd=ImageDraw.Draw(walk)
# Foot-space remains outside the protected building projection and the new left-edge pockets.
lanes=[(1508,150,1535,779),(2490,150,2531,779)]
for b in lanes:wd.rectangle(b,fill=255)
# Entire planted shoulders remain nonwalkable, including low lantern support/contact shadows.
pockets=[(1470,326,1500,384),(1470,540,1506,600),(1470,648,1506,746),(2436,254,2476,375),(2436,530,2480,638)]
for b in pockets:wd.rectangle(b,fill=0)
walk.save(O/'walk.png');scene['mask']='district-refinement/walk.png';scene['limitations']='Local final composition review; no art approval, Gate3 locked. Architecture, Juni, source scale, main coordinates and all other scenes unchanged.'
scene['routes']+= [dict(id='west-pedestrian-alley',points=[[1524,780],[1524,180]],width=28),dict(id='station-garden-connector',points=[[2508,780],[2508,180]],width=40)]
assert scene['spawn']==previous['spawn'] and scene['targets']==previous['targets'] and scene['objects']==previous['objects'] and scene['size']==previous['size'];(O/'scene.json').write_text(json.dumps(scene,indent=2,ensure_ascii=False)+'\n')
after=np.array(walk);delta=after!=before;allowed=np.zeros((H,W),bool)
for b in lanes+pockets:x0,y0,x1,y1=b;allowed[y0:y1+1,x0:x1+1]=True
assert not np.any(delta&(~allowed));assert not np.any((after>127)&protected&(~(before>127)))
connected,n=label(after>127);component=connected[780,1200];assert component
for x,y in [(t['x'],t['y'])for t in scene['targets']]+[(1524,180),(2508,180)]:assert connected[y,x]==component,(x,y)
cat=json.loads((P/'catalog.json').read_text());cat=[c for c in cat if c['id']!='district-refinement']
for c in cat:
 if c['id']=='district-reconstruction':c['label']='HISTORY · reconstructed district candidate'
cat.append(dict(id=scene['id'],label='CURRENT · final composition / approval pending'));(P/'catalog.json').write_text(json.dumps(cat,indent=2,ensure_ascii=False)+'\n')
proof=dict(worldSize=[W,H],changedGroundPixels=int(changed.sum()),worldPixels=W*H,allowedEditPixels=int(owned.sum()),unchangedOutsideLocalMask=True,protectedArchitecturePixels=int(protected.sum()),protectedArchitectureExact=True,originalFacadeAndEntranceCoordinatesExact=True,JuniAndForegroundObjectsExact=True,chunkEdges=[1512,2488],nativeGroundChunks=3,collisionChangedPixels=int(delta.sum()),collisionChangesOnlyInsideTwoPassages=True,mainAndLowerPathCollisionUnchanged=True,laneFootRectangles=lanes,newPlantPocketFootRectangles=pockets,existingEntranceTargetsConnected=True,newPassagesConnectedToSidewalk=True,regions=regions,humanVisualApproval='PENDING')
(D/'asset-proof.json').write_text(json.dumps(proof,indent=2)+'\n');print('PASS localized masks / exact protected architecture and coordinates / native chunks / connected pedestrian lanes')
