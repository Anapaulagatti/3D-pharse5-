"""Full-field equality, protected-source hashes and actual native Phaser readback."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,numpy as np,hashlib
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate3/west-hanok-v1';D=R/'docs/gate3-west-hanok'
def rd(p):return json.loads((R/p).read_text())
def wr(p,q):p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def world(m):
 g=Image.new('RGBA',m['size']);f=np.zeros(m['size'][::-1],np.uint8)
 for c in m['chunks']:
  x,y,w,h=[c[k]for k in ['x','y','width','height']];g.paste(Image.open(R/'public'/c['image']),(x,y));f[y:y+h,x:x+w]=np.fromfile(R/'public'/c['mask'],np.uint8).reshape(h,w)
 return g,f
def static(m,g):
 im=g.copy()
 for o in sorted(m['objects'],key=lambda o:o['sortY']):im.alpha_composite(Image.open(R/'public'/o['image']).convert('RGBA'),(o['x'],o['y']))
 return im
lock=rd('assets-src/gate3/west-hanok-v1/baseline-lock.json');b=lock['manifest'];m=rd('public/assets/gate3/west-hanok-world/manifest.json');spec=rd('assets-src/gate3/west-hanok-v1/scope.json');mask=np.array(Image.open(S/'edit-scope-mask.png'))>0;bg,bf=world(b);g,f=world(m);gd=np.any(np.array(bg)!=np.array(g),2);sd=np.any(np.array(static(b,bg))!=np.array(static(m,g)),2);assert not np.any(gd&~mask);assert not np.any(sd&~mask);assert np.array_equal(f,bf)
for key in ['logicalSolids','contactCollision','targets','stops','workingPlan','deferredContent','farmMetadata']:assert m[key]==b[key],key
for o in b['objects']:
 if o['id']in spec['retiredTargetObjects']:continue
 assert o==next(q for q in m['objects']if q['id']==o['id']),o['id']
for p,h in lock['files'].items():assert sha(R/p)==h,p
for o in m['objects']:
 if o['id'].startswith('west-hanok/'):
  a=np.array(Image.open(R/'public'/o['image']).getchannel('A'));assert not np.any((a>0)&(a<255));assert float(o['x']).is_integer()and float(o['y']).is_integer()
wr(D/'protected-hashes.json',{'status':'PASS','count':len(lock['files']),'files':lock['files'],'Hanbit':'APPROVED LOCKED / exact object, source pixels, registration, forecourt, platform and collision','JejuBothBridges':'VISUALLY APPROVED LOCKED / all source/art/object/ground/physical fields exact','mainPalaceCommercialNamsanFarmRoadsIslandJuni':'UNCHANGED'})
Image.fromarray(sd.astype('uint8')*255).save(D/'native-world-difference.png');wr(D/'scope-and-collision.json',{'status':'PASS','baseline':lock['HEAD'],'changedGroundPixels':int(gd.sum()),'changedStaticPixels':int(sd.sum()),'outOfScopeGroundPixels':0,'outOfScopeStaticPixels':0,'worldCollisionCellChanges':int((f!=bf).sum()),'logicalSolids':'EXACT','nativeContactSpecAndData':'EXACT','nonTargetObjects':'EXACT','scope':spec,'artAcceptance':'PENDING HUMAN'})
cap=rd('docs/gate3-west-hanok/native-captures.json');man={};grounds={};total=0;rows=[];pairs=[]
for scene in ['west-hanok-before','west-hanok-world']:man[scene]=rd('public/assets/gate3/'+scene+'/manifest.json');grounds[scene]=world(man[scene])[0]
for row in cap['rows']:
 a=row['audit'];cam=a['camera'];assert cam['zoom']==1 and all(float(v).is_integer()for v in cam['scroll']);sx,sy=map(round,cam['scroll']);shot=Image.open(D/(row['name']+'.png')).convert('RGB');sw,sh=shot.size;want=grounds[row['scene']].crop((sx,sy,sx+sw,sy+sh)).convert('RGB');ok=np.ones((sh,sw),bool)
 for l in a['layers']:
  assert l['scaleMode']==1 and all(float(v).is_integer()for v in l['position'])
  if not l['key'].startswith('f/')or not l['visible']or l['alpha']<=0:continue
  ob=next(o for o in man[row['scene']]['objects']if'f/'+o['id']==l['key']);im=Image.open(R/'public'/ob['image']).convert('RGBA');x,y=ob['x'],ob['y'];lx=max(x,sx);ly=max(y,sy);rx=min(x+im.width,sx+sw);ry=min(y+im.height,sy+sh)
  if lx<rx and ly<ry:ok[ly-sy:ry-sy,lx-sx:rx-sx]&=np.array(im.getchannel('A').crop((lx-x,ly-y,rx-x,ry-y)))==0
 s=row['state'];cx,cy=round(s['x'])-sx,round(s['y'])-sy;ok[max(0,cy-102):min(sh,cy+14),max(0,cx-50):min(sw,cx+50)]=False;diff=np.any(np.array(shot)!=np.array(want),2)&ok;assert not diff.any(),row['name'];total+=int(ok.sum());rows.append({'frame':row['name'],'exactGroundPixels':int(ok.sum()),'mismatches':0,'zoom':1,'integerCameraAndPlacement':True,'nearest':True})
 if row['phase']=='after':
  before=next(q for q in cap['rows']if q['phase']=='before'and q['entry']==row['entry']);assert cam==before['audit']['camera'];bi=Image.open(D/(before['name']+'.png')).convert('RGB');allow=Image.fromarray(mask.astype('uint8')*255).crop((sx,sy,sx+sw,sy+sh));dr=ImageDraw.Draw(allow)
  for rr in [row,before]:
   x,y=round(rr['state']['x'])-sx,round(rr['state']['y'])-sy;dr.rectangle((x-50,y-102,x+50,y+14),fill=255)
  assert not np.any(np.any(np.array(bi)!=np.array(shot),2)&(np.array(allow)==0)),('NATIVE OUTSIDE',row['entry']);pairs.append({'entry':row['entry'],'sameCamera':True,'outOfScopePixels':0})
wr(D/'native-render-qa.json',{'status':'PASS','frames':rows,'matchedPairs':pairs,'exactGroundPixels':total,'mismatches':0,'sourceResampling':'NONE','originalRendererJuniCamera':'UNCHANGED','humanArtAcceptance':'PENDING'})
wr(D/'asset-provenance.json',{'integration':rd('assets-src/gate3/west-hanok-v1/integration-provenance.json'),'sourceFiles':[{'path':str(p.relative_to(R)),'sha256':sha(p),'bytes':p.stat().st_size}for p in sorted(S.glob('*'))if p.is_file()]});print('PASS',len(lock['files']),'protected assets;',total,'actual native pixels;',len(pairs),'matched pairs; collision0 /outside0')
