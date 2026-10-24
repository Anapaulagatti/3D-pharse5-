"""Review-only native facade proposal. Never modifies the main reconciliation manifest."""
from pathlib import Path
from PIL import Image
import copy,json,hashlib
R=Path(__file__).resolve().parents[1];O=R/'public/assets/gate3/reconciled-palace-proposal';O.mkdir(exist_ok=True);S=R/'assets-src/gate3/reconciliation-v1';m=json.loads((R/'public/assets/gate3/reconciled-world/manifest.json').read_text());p=copy.deepcopy(m);p['id']='reconciled-palace-proposal';p['artStatus']='PROPOSAL ONLY / NO APPROVED REGISTRATION CHANGE / main-hall plinth40px / academy remains unresolved'
W,H=m['size'];g=Image.new('RGBA',(W,H))
for c in m['chunks']:g.paste(Image.open(R/'public'/c['image']),(c['x'],c['y']))
# Only retired main-hall source body, using the same native paving component under it.
paving=Image.open(S/'ceremonial-native-paving.png').convert('RGBA')
for x in range(1510,2520,430):
 w=min(430,2520-x);g.paste(paving.crop((0,0,w,140)),(x,650))
source=Image.open(R/'public/assets/gate2/a/ground.png').convert('RGBA');facade=Image.new('RGBA',(1010,140));facade.paste(source.crop((870,0,1536,140)),(0,0));facade.paste(source.crop((1145,0,1489,140)),(666,0));facade.save(O/'native-main-hall-facade.png',optimize=True)
p['objects']=[o for o in p['objects']if o['id']not in ['recovery-world/palace-upper-timber','recovery-world/palace-right-continuation']]
p['objects'].append({'id':'proposal/native-main-hall-facade','image':'assets/gate3/reconciled-palace-proposal/native-main-hall-facade.png','x':1530,'y':610,'width':1010,'height':140,'sortY':750,'alphaSoftening':.35,'bytes':1010*140*4})
changed=[]
for c in p['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']]
 if x<2520 and x+w>1510 and y<790 and y+h>650:
  out=O/(c['id']+'.png');g.crop((x,y,x+w,y+h)).save(out,optimize=True);c['image']=str(out.relative_to(R/'public'));c['sha256']=hashlib.sha256(out.read_bytes()).hexdigest();changed.append(c['id'])
# Collision is intentionally not loosened to fake approval of moved art.
over=g.copy()
for ob in sorted(p['objects'],key=lambda ob:ob['sortY']):over.alpha_composite(Image.open(R/'public'/ob['image']).convert('RGBA'),(ob['x'],ob['y']))
over.thumbnail((870,973),Image.Resampling.NEAREST);over.save(O/'overview.png',optimize=True)
p['overview']='assets/gate3/reconciled-palace-proposal/overview.png';(O/'manifest.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
(S/'palace-localized-proposal.json').write_text(json.dumps({'status':'PROPOSAL ONLY / NOT ADOPTED IN MAIN CANDIDATE','approvedSupport':[1510,290,1050,460],'currentPaintedPlinthBottom':790,'proposedNativeFacade':[1530,610,1010,140],'newPlinthBottom':750,'nativeRGB':'Original A source crops copied exactly, no resize/repaint','roof':'Complete existing native roof retained at protected current source placement','retiredDerivedObjects':['palace-upper-timber','palace-right-continuation'],'currentApprovedSourcePNG':'UNCHANGED','mainManifest':'UNCHANGED','collision':'UNCHANGED in proposal; full entry/support ownership requires approval and new movement QA','sourceRects':[[870,0,666,140],[1145,0,344,140]],'changedProposalChunks':changed,'otherConflicts':[{'id':'academy','decision':'Cropped approved source lacks its west silhouette. Recover a verified complete source or explicitly approve a localized completion/registration; no new architecture is silently generated.'},{'id':'gate-pavilion','decision':'Native painted threshold and approved support front must be measured separately; do not infer ground placement from roof bbox. Preserve current architecture pending an approved derived extraction.'}]},ensure_ascii=False,indent=2)+'\n')
print('Isolated native main-hall proposal prepared; main candidate unchanged')
