"""Validate fixed approved north, retained source art and shared actor engine offline."""
from pathlib import Path
from PIL import Image,ImageChops
import json,hashlib
R=Path(__file__).resolve().parents[1];N=R/'assets-src/protected-north';L=R/'assets-src/library';S=R/'assets-src/v9-world';read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();proof=read(N/'protection.json')
for file,key in [('ground-native.png','groundSha256'),('land-mask.png','landMaskSha256'),('district.json','layoutSha256')]:assert sha(N/file)==proof[key],file
for row in read(L/'native-provenance.json'):assert sha(R/row['preservedAt'])==row['sha256'],row['kind']
for row in read(L/'originals-provenance.json'):assert sha(R/row['preserved'])==row['sha256'],row['from']
if (N/'shared-system-protection.json').exists():
 for path,want in read(N/'shared-system-protection.json').items():assert sha(R/path)==want,path
north=read(N/'district.json');b=read(S/'map/bundle.json');now={o['id']:o for o in b['objects']}
for o in north['objects']:
 for k in ['prop','x','y','sortY','scale','anchor_px']:assert now[o['id']][k]==o[k],(o['id'],k)
for o in b['objects']:
 if o['id']not in {n['id']for n in north['objects']}:assert o['y']-b['props'][o['prop']]['anchor_px'][1]>=2240,('New artwork overlaps protected north',o['id'])
assert ImageChops.difference(Image.open(N/'ground-native.png').convert('RGBA'),Image.open(S/'map/ground-native.png').crop((0,0,4352,2240)).convert('RGBA')).getbbox(alpha_only=False)is None,'Historical ground changed'
for key,want in proof['nativeImages'].items():assert sha(L/read(L/'props.json')[key]['image'])==want,key
actual=read(R/'public/assets/world/plaza.json');coll=next(l for l in actual['layers']if l['name']=='Collision')['objects'];assert [[o[k]for k in ['x','y','width','height']]for o in coll]==[[o[k]for k in ['x','y','w','h']]for o in b['collision']['solids']]
for name in ['world','academy']:
 nav=read(S/(name+'-navigation/nav-report.json'));assert nav['status']=='pass',[(c['id'],c['status'],c['value'])for c in nav['checks']if c['status']!='pass']
# No old revision HTML/modules or live dependency paths survive cleanup.
for folder in ['src/v8-city','src/v7-world','src/v6-world','src/v3-world','public/review','assets-src/v8-city','assets-src/v7-world','assets-src/v6-restructure']:
 assert not (R/folder).exists(),('Obsolete active root',folder)
r={'status':'PASS','northObjects':len(north['objects']),'northGroundExact':[4352,2240],'nativeArtKinds':len(read(L/'native-provenance.json')),'priorSourceArtworkRetained':True,'runtimeCollisionExact':True,'oldSouthernRootsRemoved':True};(R/'.cache/v9-world').mkdir(parents=True,exist_ok=True);(R/'.cache/v9-world/preservation.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))

# Current final candidate proofs are stored artifacts; setup never needs Forge or authors art.
if b.get('art_source')=='host_image':
 proof=read(S/'scene-snapshot.json');assert proof['status']=='PASS'and proof['sourceBundleSha256']==sha(S/'map/bundle.json')
 geometry=read(S/'plan/route-geometry-check.json');assert geometry['status']=='PASS'
 semantic=hashlib.sha256(json.dumps({'collision':b['collision'],'roads':read(S/'plan/city.json')['roads']},sort_keys=True).encode()).hexdigest();assert geometry['semanticSha256']==semantic
 for kind,p in b['props'].items():assert sha(R/'public/assets/world'/(kind+'.png'))==sha(S/'map'/p['image']),kind
 assert sha(R/'public/assets/world/tiles.png')==sha(S/'map/tiles.png')
 water=read(S/'water.json');assert water['frames']and all(len(frames)==6 for frames in water['frames'])
 print(json.dumps({'v9RuntimeImagesExact':len(b['props']),'sourceSceneProof':'PASS','routeSemanticsExact':True,'waterGroups':len(water['frames'])}))
