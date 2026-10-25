"""Fresh station-owned ground and architecture. No legacy station art donors."""
from pathlib import Path
from PIL import Image
import numpy as np,json,copy,hashlib,math
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate3/station-clean-v1';D=R/'docs/gate3-station-clean'
def rd(p):return json.loads((R/p).read_text())
def wr(p,q):p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=rd('public/assets/gate3/station-clean-before/manifest.json');spec=rd('assets-src/gate3/station-clean-v1/scope.json');legacy={o['id']for o in spec['legacyObjectsRemoved']};W,H=m['size'];g=Image.new('RGBA',m['size']);f=np.zeros((H,W),np.uint8)
for c in m['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];g.paste(Image.open(R/'public'/c['image']),(x,y));f[y:y+h,x:x+w]=np.fromfile(R/'public'/c['mask'],np.uint8).reshape(h,w)
old=g.copy();oldf=f.copy();fresh=Image.open(S/'fresh-empty-site-authored.png').convert('RGBA');assert fresh.size==(1536,1024)
for x,y,w,h in [spec['plot'],spec['extraGround']]:
 g.paste(fresh.crop((x-1920,y-1920,x-1920+w,y-1920+h)),(x,y))
# Purge old prop/source collision ownership only within the land parcel. The
# approved continuous station contact reservation remains exact and blocking.
x,y,w,h=spec['plot'];f[y:y+h,x:x+w]=255
for q in m['logicalSolids']:
 sx,sy,sw,sh=q['rect'];lx=max(x,math.ceil(sx));ly=max(y,math.ceil(sy));rx=min(x+w,math.ceil(sx+sw));ry=min(y+h,math.ceil(sy+sh))
 if lx<rx and ly<ry:f[ly:ry,lx:rx]=0
site=copy.deepcopy(m);site['id']='station-clean-site';site['objects']=[o for o in m['objects']if o['id']not in legacy];site['artStatus']='FRESH EMPTY SITE / NO OLD STATION';assert not any(o['id']in legacy for o in site['objects'])
def publish(q,ground,field,folder):
 O=R/'public/assets/gate3'/folder;O.mkdir(exist_ok=True);changed=[];fields=[]
 for c in q['chunks']:
  x,y,w,h=[c[k]for k in ['x','y','width','height']];part=ground.crop((x,y,x+w,y+h))
  if part.tobytes()!=Image.open(R/'public'/c['image']).convert('RGBA').tobytes():
   fp=O/(c['id']+'.png');part.save(fp);c['image']=str(fp.relative_to(R/'public'));c['sha256']=sha(fp);changed.append(c['id'])
  if not np.array_equal(field[y:y+h,x:x+w],np.fromfile(R/'public'/c['mask'],np.uint8).reshape(h,w)):
   fp=O/(c['id']+'.bin');fp.write_bytes(field[y:y+h,x:x+w].tobytes());c['mask']=str(fp.relative_to(R/'public'));fields.append(c['id'])
 over=ground.copy()
 for ob in sorted(q['objects'],key=lambda o:o['sortY']):over.alpha_composite(Image.open(R/'public'/ob['image']).convert('RGBA'),(ob['x'],ob['y']))
 context=over.crop((1920,1920,3456,2944))
 over.thumbnail((870,973),Image.Resampling.NEAREST);over.save(O/'overview.png');q['overview']=str((O/'overview.png').relative_to(R/'public'));wr(O/'manifest.json',q);return changed,fields,context
changes,fields,context=publish(site,g,f,'station-clean-site');context.save(S/'clean-map-context.png')
world=copy.deepcopy(site);world['id']='station-clean-world';world['artStatus']='FRESH NEW HANBIT / ACTIVE REVIEW / HUMAN APPROVAL PENDING'
# Fresh architecture is intentionally absent until the empty site is captured.
# Never use the old station or previous recomposed candidates as source donors.
parts=[]
if(S/'fresh-station-layers.json').exists():
 layers=rd('assets-src/gate3/station-clean-v1/fresh-station-layers.json');world['objects']+=layers['objects'];parts=layers['objects']
 # New grounded side returns fit inside the unchanged approved district; no
 # old prop collision remains. Original core logical footprint stays exact.
 nf=f.copy()
 for x,y,w,h in layers['physicalSideReturns']:nf[y:y+h,x:x+w]=0
 new=Image.open(S/'fresh-station-authored.png').convert('RGBA');sm=Image.open(S/'fresh-contact-shadow-mask.png');g.paste(new,(1920,1920),sm)
 f=nf
wc,wf,_=publish(world,g,f,'station-clean-world')
Image.fromarray((f!=oldf).astype('uint8')*255).save(S/'collision-change-mask.png')
wr(S/'integration-provenance.json',{'baseline':'e935e2a / final-world','authority':'docs/current/G3D_STATION_CLEAN_REBUILD.md','legacyObjectsFullyRemoved':spec['legacyObjectsRemoved'],'allStationGroundOwnership':'100% fresh-empty-site-authored.png selected at1:1 inside plot/extension; NO old station floor/shadow survives','groundSourceOrigin':[1920,1920],'freshSource':'fresh-empty-site-authored.png','groundChunksChanged':changes,'collisionChunksChanged':fields,'newArchitectureParts':parts,'activeGroundDeltaChunksBeyondSite':wc,'activeCollisionDeltaChunksBeyondSite':wf,'logicalSolids':'EXACT unchanged approved contact reservation','allOtherObjects':'EXACT except6 retired old station objects','stationPlatformStrip':{'rect':[2950,2626,8,129],'beforeBlockedCells':int((oldf[2626:2755,2950:2958]==0).sum()),'afterBlockedCells':int((f[2626:2755,2950:2958]==0).sum()),'reason':'Legacy source/prop collision ownership retired on visible fresh paving. No layout move/new land; actual transfer must be tested.'},'historicalSources':'Immutable, not active donors','artAcceptance':'PENDING HUMAN'})
print('Clean site:',changes,'ground chunks;',fields,'collision chunks;',len(parts),'FRESH architecture parts')
