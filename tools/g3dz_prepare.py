from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,subprocess
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate3/zoned-world-v1';D=R/'docs/gate3-zoned-world'
m=json.loads((R/'public/assets/gate3/recovery-world/manifest.json').read_text());p=json.loads((R/'assets-src/gate3/production-plan-v3.1-restored.json').read_text())['plan'];ground=Image.new('RGBA',m['size'])
for c in m['chunks']:ground.paste(Image.open(R/'public'/c['image']),(c['x'],c['y']))
regions={
 'urbanwest':[160,1760,1536,1024],
 'transit':[1664,1760,1536,1024],
 'amusement':[1664,2680,1536,1024],
 'harborwest':[160,3280,1536,1024],
 'harboreast':[1664,3280,1536,1024],
 'heritageeast':[1664,736,1536,1024],
 'railcoast':[2816,1792,1536,1024],
 'jejunorth':[2816,3072,1536,1024],
 'jejusouth':[2816,3840,1536,1024]}
zones=[
 {'id':'A','name':'Historic north','boundary':[[160,80],[3160,80],[3160,1740],[160,1740]],'publicSpace':'Bounded stone courtyards, gates and garden paths; keep facade sightlines','vegetation':'Composed pines and garden beds outside courts, not on access','materials':['HERITAGE_STONE','GARDEN_EARTH','STONE_BOUNDARY']},
 {'id':'B','name':'Modern commercial','boundary':[[160,1740],[1952,1740],[1952,2760],[160,2760]],'publicSpace':'Open commercial sidewalks/plazas and service passages; generous clear facade approaches','vegetation':'Small formal beds and spaced street trees in defined planters only; no forest carpet','materials':['URBAN_STONE','ASPHALT','URBAN_CURB']},
 {'id':'C','name':'Namsan','boundary':[[180,2760],[1952,2760],[1952,3340],[180,3340]],'publicSpace':'Accepted terraced trail/entrance and stone park threshold','vegetation':'Layered forest on hillside retained; planted setbacks at city edge','materials':['GARDEN_EARTH','PARK_STEPS','STONE_BOUNDARY']},
 {'id':'D','name':'Rail district','boundary':[[2144,1740],[3160,1740],[3160,2090],[4096,2090],[4096,2340],[3390,2340],[3390,2790],[2144,2790]],'publicSpace':'Fine urban entrance plaza, visible tactile access and organized railway surfaces','vegetation':'Low peripheral beds away from canopy/track/entrance','materials':['URBAN_STONE','PLATFORM_STONE','ASPHALT','URBAN_CURB']},
 {'id':'E','name':'Amusement','boundary':[[2144,2790],[3160,2790],[3160,3360],[2144,3360]],'publicSpace':'Open paved arrival/queue courts and continuous perimeter pedestrian paths; ride contacts fixed','vegetation':'Low framed flowerbeds and restrained perimeter trees; no greenery across circulation','materials':['URBAN_STONE','PARK_STEPS','STONE_BOUNDARY']},
 {'id':'F','name':'Harbor','boundary':[[160,3340],[3160,3340],[3160,3980],[160,3980]],'publicSpace':'Continuous public quay, market forecourt, terminal approach and safe stone/timber edge; no extra quay land','vegetation':'Low salt-tolerant planting in deliberate coastal beds','materials':['URBAN_STONE','QUAY_STONE','TIMBER','COAST_BASALT','OFFSHORE_WATER']},
 {'id':'G','name':'Jeju','boundary':[[3180,3200],[4204,3200],[4204,4736],[3180,4736]],'publicSpace':'Canonical island/nearshore image immutable; external water and bridge alignment only','vegetation':'All original orchard/volcanic scenery unchanged','materials':['CANONICAL_JEJU','OFFSHORE_WATER']}
]
materials={
 'URBAN_STONE':'Warm gray/beige fine granite pavers 12–28px wide, 8–16px tall, crisp 1px joints; shared with canonical forecourt and Muneum sidewalk; no huge slabs',
 'HERITAGE_STONE':'Warm traditional irregular fine stone, restrained seams, original north source authority',
 'ASPHALT':'Existing native asphalt, curbs and road centerline registrations retained; continuous logical approaches, no isolated fragments',
 'URBAN_CURB':'Native narrow dressed granite curb, tactile path continuity and crosswalks at existing alignment',
 'GARDEN_EARTH':'Compacted warm earth, exposed stone and low irregular grass only within garden/park boundaries',
 'STONE_BOUNDARY':'Low Korean stone retaining edge or garden border with actual openings at public paths, no arbitrary rectangular ownership edge',
 'PARK_STEPS':'Existing accepted Namsan stairs/trails and park entrance retained',
 'PLATFORM_STONE':'Fine open platform paving, clear track/edge ownership; original canopy and 8px strip unchanged',
 'QUAY_STONE':'Fine gray stone promenade with low coastal wall/railing at real shore, no new land',
 'TIMBER':'Native existing bridge/jetty plank pitch; no stretching, approaches meet existing geometry',
 'COAST_BASALT':'Natural irregular dark rock/foam grounding of unchanged planned shoreline, not straight texture cutoff',
 'OFFSHORE_WATER':'Single coherent offshore blue light/wave scale, native authored turquoise-to-blue transition OUTSIDE canonical Jeju; canonical foam and turquoise untouched',
 'CANONICAL_JEJU':'Exact original ground and foreground PNGs and runtime coordinates; no filters or repaints'}
reg={'baselineCommit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'baselineCheckpoint':'checkpoint/g3d-world-recovery-review-20261023','worldSize':m['size'],'regions':regions,'zones':zones,'materials':materials,'boundaryPolicy':'One world registry; adjacent authors receive this same program and actual shared geometry. Native binary ownership; roads and canonical sources win. No independent palette generation or generic repeating terrain tiles.','protectedGround':json.loads((R/'assets-src/gate3/recovery-world-v1/panel-registry.json').read_text())['protectedGround'],'planningAmendments':[],'reviewerImages':{'status':'NOT PROVIDED','countReceived':0,'exactMarkedDefectAcceptance':'NOT TESTED; textual defect list used, reattachment requested'}}
(S/'land-use-registry.json').write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n')
for name,(x,y,w,h)in regions.items():
 crop=ground.crop((x,y,x+w,y+h));crop.save(S/(name+'-before-ground.png'),optimize=True)
 guide=crop.copy();d=ImageDraw.Draw(guide)
 for path in p['paths']:
  d.line([(qx-x,qy-y)for qx,qy in path['points']],fill='#35dce7',width=2,joint='curve')
 for b in p['buildings']:
  bx,by,bw,bh=b['rect'];d.rectangle((bx-x,by-y,bx+bw-x-1,by+bh-y-1),outline='#ff9bb7',width=2)
 guide.save(S/(name+'-guide.png'),optimize=True)
# Native style reference is NOT resized. No buildings are painted into the ground plates.
Image.open(R/'docs/gate3-recovery-world/station-after-native.png').crop((370,560,1054,770)).save(S/'canonical-paving-reference.png')
# Geometry-only whole-world zoning board, explicitly not gameplay evidence.
b=ground.copy();bd=ImageDraw.Draw(b)
for i,z in enumerate(zones):
 bd.line([tuple(v)for v in z['boundary']+[z['boundary'][0]]],fill=['#d4a85b','#64c8ec','#82ba68','#e7a5b4','#c0a4e9','#ecc588','#6ed8d0'][i],width=6)
 bd.text(tuple(z['boundary'][0]),z['id']+' '+z['name'],fill='white',stroke_width=2,stroke_fill='black')
b.thumbnail((1088,1216),Image.Resampling.NEAREST);b.save(D/'zoning-board.png',optimize=True)
print('Prepared',len(regions),'native edit guides / single zoning and material registry')
