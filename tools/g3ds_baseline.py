"""Freeze residual candidate, source hashes, registrations and review poses."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,subprocess,copy
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate3/final-surgical-v1';D=R/'docs/gate3-final';S.mkdir(exist_ok=True);D.mkdir(exist_ok=True)
def wr(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
m=json.loads((R/'public/assets/gate3/residual-world/manifest.json').read_text())
entries={'farm':[500,810],'western-house':[800,1390],'western-courtyard':[900,1400],'house-court':[800,1500],'station-standalone':[2598.5,2760]}
frames={'farm':[640,500],'western-house':[850,1090],'western-courtyard':[1070,1510],'house-court':[1050,1220],'station-standalone':[2598,2460]}
p=copy.deepcopy(m);p['reviewEntries'].update(entries);p['nativeFrames'].update(frames)
for name in ['final-before','final-world','final-station-candidate']:
 q=copy.deepcopy(p);q['id']=name;q['artStatus']='SURGICAL REVIEW / HUMAN APPROVAL PENDING';O=R/'public/assets/gate3'/name;O.mkdir(exist_ok=True);wr(O/'manifest.json',q)
lock=S/'baseline-lock.json'
if not lock.exists():
 sources={}
 for root in ['assets-src','public']:
  for f in sorted((R/root).rglob('*')):
   if not f.is_file()or'/final-surgical-v1/'in str(f)or'/gate3/final-'in str(f):continue
   sources[str(f.relative_to(R))]=hashlib.sha256(f.read_bytes()).hexdigest()
 wr(lock,{'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'baseline':'residual-world / review1cd50c2 / metadataaad3b3c','files':sources,'registrations':m['objects'],'logicalSolids':m['logicalSolids'],'chunks':m['chunks'],'contactCollision':m['contactCollision']})
# Bounds from source A placement640,650 and its clipped left edge, exact garden;
# farm lies west of wall1107, north of academy source; station derives registration.
targets=[
 {'name':'western-house','rect':[550,880,510,385],'sourceAssets':['public/assets/gate2/a/ground.png','assets-src/gate3/recovery-world-v1/academywest-authored.png'],'runtimeLayers':['ground'],'approvedObjects':['Original academy facade/door/stairs; source A below roof'],'allowed':['Missing left roof/eave/support continuation only','native source ownership repair'],'protectedNeighbors':['Palace western wall1107','tea roof1190','academy door/stairs'],'maximumIntendedChangeArea':85000},
 {'name':'western-courtyard','rect':[580,1370,585,370],'sourceAssets':['public/assets/gate2/a/ground.png','public/assets/gate2/a/foreground-pine.png'],'runtimeLayers':['ground','a/foreground-pine only if diagnosed'],'approvedObjects':['Garden pine/enclosure/bench native source'],'allowed':['Missing western boundary and southern source-edge completion','native fixture/ground contact repair'],'protectedNeighbors':['Tea courtyard','academy-lane centerline1500','main palace compound'],'maximumIntendedChangeArea':55000},
 {'name':'northwestern-farm','rect':[300,230,760,570],'sourceAssets':['assets-src/gate3/recovery-world-v1/northwest-authored.png','public/assets/gate3/recovery-world/tree-07.png'],'runtimeLayers':['ground','recovery-world/planted-tree-01','local farm plot metadata and bounded collision'],'approvedObjects':['Useful mature border pines outside bed and paths'],'allowed':['Local unprotected forest-to-six-plot farm','short accessible path link within envelope','remove tree01 inside farm only'],'protectedNeighbors':['Coast160','palace western wall1107','historical roof below880','no new land'],'maximumIntendedChangeArea':433200},
 {'name':'station-replacement-candidate','rect':[2274,2140,742,575],'sourceAssets':[o['image']for o in m['objects']if o['id'].startswith('registration/station')or o['id']=='residual/station-potted-tree'],'runtimeLayers':['ground','registration/station','separate new architecture/roof/shadow','existing planters/canopy/tree'],'approvedObjects':['Restored forecourt2274,2603,684,210','left/right planters','original canopy roof/posts','old station coordinates/sourcePivot.5'],'allowed':['Separate new station at same native footprint and entrance','retire old active facade in isolated candidate','local underlying obsolete pixels only'],'protectedNeighbors':['Road/curb/crosswalk','rail platforms/reservation','8px strip','amusement rides'],'maximumIntendedChangeArea':240000},
 {'name':'mainland-bridge-landing','rect':[3090,3430,160,160],'sourceAssets':['assets-src/gate3/alignment-v1/bridge-mainland-derived.png'],'runtimeLayers':['ground','existing bridge foreground'],'approvedObjects':['Bridge endpoints, rails, piers'],'allowed':['Bounded water/source-edge and stone-contact ownership correction only'],'protectedNeighbors':['Canonical island/nearshore','ferry/public paths'],'maximumIntendedChangeArea':9000},
 {'name':'island-bridge-landing','rect':[3370,3520,180,160],'sourceAssets':['public/assets/gate2/c/ground.png'],'runtimeLayers':['ground','existing foreground bridge rail'],'approvedObjects':['Canonical Jeju land/basalt/foam/internal path'],'allowed':['External shared-water source-edge correction only; protected bitmap always wins'],'protectedNeighbors':['Original Jeju PNG and all canonical land artwork'],'maximumIntendedChangeArea':9000},
 {'name':'southern-promenade-asphalt-join','rect':[1930,3770,250,95],'sourceAssets':['assets-src/gate3/recovery-world-v1/harboreast-authored.png','assets-src/gate3/recovery-world-v1/harborwest-authored.png'],'runtimeLayers':['ground'],'approvedObjects':['Existing road alignment, curb, promenade'],'allowed':['Proven asphalt ownership line only; retain markings and curb'],'protectedNeighbors':['Ferry/promenade/shoreline/coast footprint'],'maximumIntendedChangeArea':8000},
 {'name':'palace-minor-inspection','rect':[1830,685,430,150],'sourceAssets':['public/assets/gate3/residual-world/palace-front-corner-ownership.png'],'runtimeLayers':['ground','alignment/palace-native-front'],'approvedObjects':['Door axis2048 threshold685 roof rails'],'allowed':['Proven remaining contact defect only; unchanged if no defect'],'protectedNeighbors':['All palace walls and royal hall registration'],'maximumIntendedChangeArea':3000},
 {'name':'retail-minor-inspection','rect':[540,1960,1100,230],'sourceAssets':['public/assets/gate3/residual-world/cafe-owned.png','public/assets/gate3/residual-world/bookshop-owned.png','public/assets/gate3/residual-world/learning-owned.png'],'runtimeLayers':['upper alpha of retail only'],'approvedObjects':['Every original facade RGB/door/sign/window/roof'],'allowed':['Proven nonarchitectural remnant alpha only; unchanged if none'],'protectedNeighbors':['Street/tower/main circulation/retail ground'],'maximumIntendedChangeArea':3000}
]
wr(D/'REGION_TARGETS.json',{'authority':'docs/current/G3D_FINAL_SURGICAL.md','basis':'Exact source registrations and plan geometry; not screenshot marks. Rectangles are maximum envelopes; actual change masks are narrower and enforced separately.','worldSize':m['size'],'regions':targets})
(D/'BASELINE.md').write_text('''# Immutable surgical baseline

HEAD `aad3b3c`; latest complete visual candidate `residual-world` at review `1cd50c2`. Preserved checkpoint `checkpoint/g3d-before-final-surgical-20261025`.

Canonical source hashes, exact source bounds, source anchors/pivots, sort planes, logical solids, chunk collision ownership and native contact field are frozen in [baseline-lock](../../assets-src/gate3/final-surgical-v1/baseline-lock.json). Review-only entry poses and matching native camera frames are added to separate final-before/final-world/final-station-candidate manifests. No default production or historical source is edited.

[Discovered region targets](REGION_TARGETS.json) constrain all edits. The western house is the clipped original A house at the left edge of the native source registered640,650; its garden is directly south, not the royal court. The farm occupies unprotected woodland west of wall1107 and above academy/house, wholly inside existing mainland. Station source registration2313,2196,645,453 (anchor2313.5,2196 / pivot.5,0); main logical reservation2320,2380,560,210, current actual public entry2598,2610 and canonical floor2274,2603,684,210 remain. Current canopy/platform and8px strip remain separate.

Full-world and native BEFORE views are captured in actual Phaser before any art construction. STATIC native compositing plus matched Phaser overview compare all out-of-envelope pixels; live Juni pixels are excluded for fair comparisons. Any unrelated difference fails the candidate. No broad ocean ownership changes are authorized in this pass.
''')
print('Baseline source files',len(json.loads(lock.read_text())['files']))
