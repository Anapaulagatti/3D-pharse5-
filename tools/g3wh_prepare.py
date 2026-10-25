"""Freeze approved world and TWO exact local masks before any art changes."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,copy,hashlib,subprocess,numpy as np
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate3/west-hanok-v1';D=R/'docs/gate3-west-hanok'
def wr(p,q):p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
m=json.loads((R/'public/assets/gate3/jeju-bridges-world/manifest.json').read_text());W,H=m['size']
if not(S/'baseline-lock.json').exists():wr(S/'baseline-lock.json',{'HEAD':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'manifest':m,'files':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for root in ['assets-src','public']for p in sorted((R/root).rglob('*'))if p.is_file()and'/west-hanok-'not in str(p)}})
polys={'house':[(545,940),(580,880),(990,880),(1095,945),(1095,1325),(1050,1358),(600,1358),(545,1200)],'courtyard':[(603,1408),(1179,1408),(1189,1460),(1189,1660),(1165,1700),(625,1700),(603,1670)]};mask=Image.new('L',(W,H));dr=ImageDraw.Draw(mask)
for poly in polys.values():dr.polygon(poly,fill=255)
mask.save(S/'edit-scope-mask.png');g=Image.new('RGBA',(W,H));field=np.zeros((H,W),np.uint8)
for c in m['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];g.paste(Image.open(R/'public'/c['image']),(x,y));field[y:y+h,x:x+w]=np.fromfile(R/'public'/c['mask'],np.uint8).reshape(h,w)
for ob in sorted(m['objects'],key=lambda o:o['sortY']):g.alpha_composite(Image.open(R/'public'/ob['image']).convert('RGBA'),(ob['x'],ob['y']))
g.crop((320,750,1856,1774)).save(S/'before-authoring-context.png');Image.fromarray(field).save(S/'before-collision.png');guide=g.crop((320,750,1856,1774));dr=ImageDraw.Draw(guide)
for name,p in polys.items():p=[(x-320,y-750)for x,y in p];dr.line(p+[p[0]],fill='#ff37be',width=2);dr.text(p[0],name,fill='white',stroke_fill='black',stroke_width=1)
guide.save(S/'exact-edit-guide.png');wr(S/'scope.json',{'baseline':json.loads((S/'baseline-lock.json').read_text())['HEAD'],'origin':[320,750],'sourceSize':[1536,1024],'polygons':polys,'preservedFacadeAxisX':850,'existingPublicApproach':[850,1400],'interiorPolicy':'Existing source collision/public lanes retained; no newly opened house/garden interior','palaceWestWallProtectedAtX':1107,'protectedPublicLanes':{'westHouseX':440,'gardenWestX':580,'betweenHouseGardenY':1400},'allowed':'Rebuild complete western hanok visible structure and lower enclosed garden ONLY. No new footprint/roads/gameplay. Keep collision EXACT unless actual necessary local correction is demonstrated.','retiredTargetObjects':['surgical/house-west-roof','a/foreground-pine','surgical/courtyard-west-return']})
frames={'west-house-local':[825,1100],'west-garden-local':[895,1550],'west-both-local':[990,1285]};entries={k:[440,1400]for k in frames}
for scene in ['west-hanok-before','west-hanok-world']:
 q=copy.deepcopy(m);q.update(id=scene,artStatus='Hanbit and Jeju bridge visuals APPROVED LOCKED / western repair HUMAN REVIEW');q['nativeFrames'].update(frames);q['reviewEntries'].update(entries);wr(R/'public/assets/gate3'/scene/'manifest.json',q)
print('Frozen',len(json.loads((S/'baseline-lock.json').read_text())['files']),'historical files; exact2 masks')
