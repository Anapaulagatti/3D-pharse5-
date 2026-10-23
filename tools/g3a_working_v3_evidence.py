"""Native Phaser crop/readback evidence plus a clearly labelled planning diagram."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,copy,math
R=Path(__file__).resolve().parents[1];D=R/'docs/g3a-controlled-finalization';rows=json.loads((D/'native-captures.json').read_text())['rows'];results=[]
rois={'entrance-ground':(2542,2619,2669,2688),'tactile-strip':(2572,2613,2627,2726),'left-planter-pavement':(2302,2669,2549,2726),'right-planter-pavement':(2669,2669,2909,2726),'canopy-platform':(2870,2310,3040,2590)}
for phase,scene in [('before','registration-review'),('after','registration-working-v3')]:
 r=next(r for r in rows if r['name']==phase+'-station-native');m=json.loads((R/f'public/assets/gate3/{scene}/manifest.json').read_text());expected=Image.new('RGBA',tuple(m['size']))
 for c in m['chunks']:expected.paste(Image.open(R/'public'/c['image']),(c['x'],c['y']))
 for o in sorted(m['objects'],key=lambda o:o['sortY']):expected.alpha_composite(Image.open(R/'public'/o['image']).convert('RGBA'),(o['x'],o['y']))
 mat=r['audit']['camera']['matrix'];vx,vy=-mat[4],-mat[5];assert r['audit']['camera']['zoom']==1 and int(vx)==vx and int(vy)==vy
 shot=Image.open(D/(r['name']+'.png')).convert('RGB')
 for name,(x,y,x2,y2)in rois.items():
  actual=shot.crop((int(x-vx),int(y-vy),int(x2-vx),int(y2-vy)));want=expected.crop((x,y,x2,y2)).convert('RGB');diff=int(np.any(np.array(actual)!=np.array(want),2).sum());assert diff==0,(phase,name,diff);actual.save(D/f'{name}-{phase}-1x.png',optimize=True);results.append({'phase':phase,'roi':name,'differentPixelsFromExpectedNativeComposite':diff})
 for o in r['audit']['layers']:
  assert all(float(v).is_integer()for v in o['position']+o['screenOrigin']);assert o['scale']==[1,1]and o['scaleMode']==1
  if 'minFilter'in o:assert o['minFilter']==9728 and o['magFilter']==9728
for n in list(rois)[:4]:assert Image.open(D/f'{n}-before-1x.png').tobytes()==Image.open(D/f'{n}-after-1x.png').tobytes()
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13);sheet=Image.new('RGB',(420,340),'#17242e');d=ImageDraw.Draw(sheet)
for i,phase in enumerate(['before','after']):d.text((10+210*i,8),phase.upper()+' / native 1:1',font=font,fill='white');sheet.paste(Image.open(D/f'canopy-platform-{phase}-1x.png'),(10+210*i,40))
sheet.save(D/'PLATFORM_BEFORE_AFTER_1X.png',optimize=True)
# Technical overlay on genuine Phaser pixels, separate from unannotated native evidence.
r=next(r for r in rows if r['name']=='after-station-native');vx,vy=-r['audit']['camera']['matrix'][4],-r['audit']['camera']['matrix'][5];region=(2860,2320,3040,2760);im=Image.open(D/'after-station-native.png').crop(tuple(int(v)for v in [region[0]-vx,region[1]-vy,region[2]-vx,region[3]-vy])).convert('RGB');out=Image.new('RGB',(640,490),'#17242e');out.paste(im,(10,30));dr=ImageDraw.Draw(out);dr.text((10,7),'PHASER crop + engineering overlay / native1x',font=font,fill='white')
def rect(box,color):x,y,w,h=box;dr.rectangle((10+x-region[0],30+y-region[1],10+x+w-region[0],30+y+h-region[1]),outline=color,width=1)
rect([2920,2350,100,400],'cyan')
for box in [[2929,2389,11,9],[2928,2489,11,6],[2913,2524,7,6]]:rect(box,'#ff986b')
rect([2950,2626,8,129],'#ff4242');dr.line((10+2980-region[0],30+2350-region[1],10+2980-region[0],30+2690-region[1]),fill='#83ff9f',width=1)
for i,t in enumerate(['CYAN: fixed platform reservation100x400','GREEN: checked longitudinal route x2980','ORANGE: real independent support bases','RED: inherited8px source-edge collision guard','Station body collider and accepted floor unchanged.','','The roof rectangle is NOT a physical collider.','Native railing end moved outside platform x2920.','Paving connector90x36 remains inside reservation.','','Local transfer remains BLOCKED pending decision.','No collision override / protected-mask edit applied.']):dr.text((205,40+i*24),t,font=font,fill='white')
out.save(D/'PLATFORM_OWNERSHIP_OVERLAY.png',optimize=True)
# Small plan diagram only. No scene textures or artwork generation.
p=json.loads((R/'assets-src/gate3/production-plan-v3-working.json').read_text())['plan'];board=Image.new('RGB',(1400,1100),'#17242e');bd=ImageDraw.Draw(board);sc=.20;ox,oy=20,60
bd.text((20,12),'WORKING V3 / PLANNING GEOMETRY ONLY — not gameplay or production art',font=font,fill='white')
def box(r):x,y,w,h=r;return(ox+x*sc,oy+y*sc,ox+(x+w)*sc,oy+(y+h)*sc)
for land in p['land']:bd.rectangle(box(land),fill='#40574d',outline='#617e70')
for path in p['paths']:bd.line([(ox+x*sc,oy+y*sc)for x,y in path['points']],fill='#c5be9b',width=max(1,round(path['width']*sc)))
for b in p['buildings']:
 color='#6c746f'if b['kind']!='heritage'else'#897459'
 if b['id']=='convenience':color='#59ae7d'
 if b['id']=='cafe':color='#c5ac64'
 bd.rectangle(box(b['rect']),fill=color,outline='white');bd.text((box(b['rect'])[0]+2,box(b['rect'])[1]+2),b['id'],font=font,fill='white')
for e in p['registrationEasements']:bd.rectangle(box(e['visualEnvelope']),outline='#f9d485',width=1)
for r in p['station']['platforms']:bd.rectangle(box(r['rect']),outline='cyan',width=2)
for ex in p['publicExclusions']:bd.rectangle(box(ex['rect']),outline='#ff8f78',width=1)
# Deferred reference is outline-only over unchanged sea, never new land.
x0,y0,x1,y1=box([550,4300,875,442])
for x in range(round(x0),round(x1),10):bd.line((x,y0,min(x+5,x1),y0),fill='#e3b975');bd.line((x,y1,min(x+5,x1),y1),fill='#e3b975')
for y in range(round(y0),round(y1),10):bd.line((x0,y,x0,min(y+5,y1)),fill='#e3b975');bd.line((x1,y,x1,min(y+5,y1)),fill='#e3b975')
bd.text((x0,y0-18),'Q1 DEFERRED / no land allocated',font=font,fill='#e3b975')
notes=['ACCEPTED AMENDMENTS','Maru contact180,3120,421,210','Glass-door approach326,3343','Only western Namsan loop adjusted','Cafe25px east footprint easement','Retail facade projections: conditional','Heritage/public-route checks: no new conflicts','','BAKERY / REQUIRED WORLD CONTENT','W0 retired; original asset preserved','Q1 candidate only / no added land','Future quay checkpoint: purpose, landscape,','return circulation and measured pacing','','STATION / PROPOSED LOCAL DETAIL','Canonical forecourt and station fixed','Platform reservation100x400 unchanged','Overhead vs grounded support ownership','Native railing opening +90x36 landing','Platform longitudinal walk PASS','Transfer guard8px: decision still required','','GLOBAL CHECKS / NOT OVERALL APPROVAL','9 selected routes pass; no new centre blocks','6 inherited centreline findings retained','WebGL hardware performance unresolved','Physical Android/iPhone NOT TESTED','FINAL G3-A PENDING / G3-B BLOCKED']
for i,t in enumerate(notes):bd.text((920,70+i*30),t,font=font,fill='#f5d994'if t.isupper()else'white')
board.save(D/'WORKING_V3_PLANNING_BOARD.png',optimize=True)
# Verify exact JSON patch reconstructs the new accepted working plan.
delta=json.loads((D/'plan-diff.json').read_text());v=json.loads((R/delta['base']).read_text())
for op in delta['operations']:
 parts=op['path'].split('/')[1:];parent=v
 for k in parts[:-1]:parent=parent[int(k)]if isinstance(parent,list)else parent[k]
 k=parts[-1]
 if isinstance(parent,list):
  i=int(k)
  if op['op']=='add':parent.insert(i,op['value'])
  elif op['op']=='remove':parent.pop(i)
  else:assert parent[i]==op['before'];parent[i]=op['value']
 else:
  if op['op']=='remove':del parent[k]
  else:
   if op['op']=='replace':assert parent[k]==op['before']
   parent[k]=op['value']
assert v==p
(D/'native-proof.json').write_text(json.dumps({'readbacks':results,'fourCanonicalForecourtCropsUnchanged':True,'nearestAndIntegerPlacement':True,'exactPlanDiffReconstructsWorkingPlan':True,'humanVisualApproval':'PENDING for platform detail; forecourt already APPROVED'},indent=2)+'\n')
print('PASS10 native source readbacks, four approved floor crops exact, plan patch round-trip')
