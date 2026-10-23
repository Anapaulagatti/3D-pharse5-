from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib,copy
R=Path(__file__).resolve().parents[1];D=R/'docs/g3a-spatial-review';capture=json.loads((D/'native-captures.json').read_text());plan=json.loads((R/'assets-src/gate25/world-plan-v1.json').read_text());new=json.loads((D/'proposal-v2-comparison.json').read_text());val=json.loads((D/'spatial-validation.json').read_text());rows=[]
for r in capture['results']:
 scene=r['scene'];manifest=json.loads((R/f'public/assets/gate3/{scene}/manifest.json').read_text());shot=np.array(Image.open(D/(r['name']+'-1x.png')).convert('RGB'));m=r['renderAudit']['camera']['matrix'];vx,vy=int(-m[4]),int(-m[5]);h,w=shot.shape[:2];claimed=np.zeros((h,w),bool);actor=np.zeros((h,w),bool);px,py=round(r['state']['x'])-vx,round(r['state']['y'])-vy;actor[max(0,py-112):min(h,py+16),max(0,px-56):min(w,px+57)]=True
 for o in sorted(manifest['objects'],key=lambda o:o['sortY'],reverse=True):
  x,y=o['x']-vx,o['y']-vy;src=np.array(Image.open(R/'public'/o['image']).convert('RGBA'));hh,ww=src.shape[:2];x0,y0=max(0,x),max(0,y);x1,y1=min(w,x+ww),min(h,y+hh)
  if x1<=x0 or y1<=y0:continue
  part=src[y0-y:y1-y,x0-x:x1-x];region=claimed[y0:y1,x0:x1];valid=(part[:,:,3]==255)&(~region)&(~actor[y0:y1,x0:x1]);diff=np.max(abs(shot[y0:y1,x0:x1].astype(int)-part[:,:,:3].astype(int)),2)
  if o['id'].startswith('registration/')and valid.sum():rows.append({'capture':r['name'],'object':o['id'],'opaqueCompared':int(valid.sum()),'different':int(((diff>0)&valid).sum()),'maxDelta':int(diff[valid].max())})
  region|=part[:,:,3]>0
 assert all(o['scale']==[1,1]and all(float(v).is_integer()for v in o['position'])and o['scaleMode']==1 and o.get('minFilter',9728)==9728 and o.get('magFilter',9728)==9728 for o in r['renderAudit']['layers'])
 assert all(abs(v-round(v))<1e-6 for v in m[4:6])
assert not capture['errors'];assert all(r['different']==0 for r in rows),rows
# Native corrected Canvas readback against approved ground and both full planter composites.
r=next(r for r in capture['results']if r['name']=='render-after-native');shot=np.array(Image.open(D/'render-after-native-1x.png').convert('RGB'));m=r['renderAudit']['camera']['matrix'];vx,vy=int(-m[4]),int(-m[5]);manifest=json.loads((R/'public/assets/gate3/district/manifest.json').read_text());ground=np.array(Image.open(R/'assets-src/gate25-station-planters/final-clean-ground.png').convert('RGB'))[vy:vy+900,vx:vx+1280];mask=Image.new('L',(3184,1214))
for o in manifest['objects']:
 a=Image.open(R/'public'/o['image']).convert('RGBA').getchannel('A').point(lambda v:255 if v else 0);mask.paste(a,(o['x'],o['y']),a)
valid=np.array(mask)[vy:vy+900,vx:vx+1280]==0;px,py=round(r['state']['x'])-vx,round(r['state']['y'])-vy;valid[py-112:py+16,px-55:px+56]=False;diff=np.max(abs(shot.astype(int)-ground.astype(int)),2);rgb={'unoccludedPixels':int(valid.sum()),'different':int(((diff>0)&valid).sum()),'maxDelta':int(diff[valid].max())};assert rgb['different']==0
proof={'foregroundReadback':rows,'correctedCanvasGroundReadback':rgb,'nativeScreenshots':{p.name:{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'size':list(Image.open(p).size),'capture':('original-resolution crop of actual Phaser screenshot, no resampling' if '-frontage-' in p.name else 'actual Phaser POST_RENDER backing PNG'if p.name!='render-before-native-1x.png'else'byte-identical prior native Canvas before evidence')}for p in D.glob('*-1x.png')},'integerNativePlacement':True,'nearest':True,'sourceTexturesChanged':False}
(D/'native-pixel-proof.json').write_text(json.dumps(proof,indent=2)+'\n')
# Non-art technical overlay; original artwork is never rescaled or pasted into this diagram.
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15);small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',12);board=Image.new('RGB',(1800,1000),'#17242e');d=ImageDraw.Draw(board);s=.26
old=json.loads((R/'assets-src/gate3/registration/proposal-v1.json').read_text())
for col,(label,proposal)in enumerate([('W0 / existing waterfront - reject',old),('Q1 / southwest quay - conditional comparison',new)]):
 panel=Image.new('RGB',(900,1000),'#17242e');d=ImageDraw.Draw(panel);ox=35;oy=80
 def point(p):return (ox+(p[0]-160)*s,oy+(p[1]-2090)*s)
 def rect(r):x,y,w,h=r;return (*point([x,y]),*point([x+w,y+h]))
 d.text((ox,15),label,font=font,fill='white')
 for r in plan['land']:
  if r[1]+r[3]>2090:d.rectangle(rect(r),fill='#394943',outline='#788d82')
 if col:d.rectangle(rect([460,3940,1120,908]),fill='#555750',outline='#f7c975',width=3);d.text(point([480,4060]),'NEW LAND / NOT APPROVED',font=small,fill='#ffdb86')
 for p in plan['paths']:
  if max(v[1]for v in p['points'])<2090:continue
  d.line([point(v)for v in p['points']],fill='#9daaaa',width=max(1,round(p['width']*s)),joint='curve')
 for b in plan['buildings']:
  if b['rect'][1]<2090:continue
  d.rectangle(rect(b['rect']),fill='#27313b',outline='#d0d9e0');d.text(point([b['rect'][0],b['rect'][1]]),b['id'],font=small,fill='white')
 for b in proposal['buildings']:
  if b['id']not in ['bakery','convenience']:continue
  env=[*b['rasterOrigin'],b['sourceRect'][2]-b['sourceRect'][0],b['sourceRect'][3]-b['sourceRect'][1]];d.rectangle(rect(env),outline='#f49dbb',width=2);d.rectangle(rect(b['collision']),outline='#ffcf75',width=3);d.text(point([b['collision'][0],b['collision'][1]+20]),b['id'],font=small,fill='#ffcf75')
 if col:
  for p in proposal['connectingRoutes']:
   if p['id']=='retail-front':continue
   d.line([point(v)for v in p['points']],fill='#7ce7d0',width=max(2,round(p['width']*s)),joint='curve')
 else:d.rectangle(rect([2220,3060,38,90]),fill='#ff3e64')
 d.text((ox,850),'Gold: contact / pink: visual envelope / grey: approved paths',font=font,fill='white')
 d.text((ox,878),'Mint: proposed links / quay is engineering geometry only'if col else'Bakery blocks 5 paths; projection overlaps carousel38x90',font=font,fill='#7ce7d0'if col else'#ff9aac')
 d.text((ox,920),'No source artwork shown or rescaled. Native Phaser screenshots are separate.',font=small,fill='#cad4dc')
 d.rectangle((0,0,899,47),fill='#17242e');d.text((ox,15),label,font=font,fill='white')
 board.paste(panel,(col*900,0))
board.save(D/'SITE_COMPARISON.png',optimize=True)
# Original-resolution door crop, no resizing/sharpening/overlay.
Image.open(R/'public/assets/gate3/registration/convenience.png').crop((96,375,198,512)).save(D/'maru-door-source-native.png')
print('PASS',len(rows),'native foreground regions, exact Canvas ground readback, integer phase/nearest')
