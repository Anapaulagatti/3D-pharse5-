"""Check proposed zoning reservations, not Forge navigation or runtime game collision."""
from pathlib import Path
from collections import deque, Counter
import json
import math
import hashlib
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/urban-zoning'
STEP = 8


def check(plan, write=True):
    w, h = plan['world']
    size = (w // STEP, h // STEP)
    def layer(): return Image.new('L', size)
    def poly(d, points, fill=255): d.polygon([(x / STEP, y / STEP) for x, y in points], fill=fill)
    def box(d, bounds, fill=255):
        x, y, a, b = bounds
        d.rectangle((x / STEP, y / STEP, (x + a) / STEP, (y + b) / STEP), fill=fill)
    def stroke(d, points, width):
        pts = [(x / STEP, y / STEP) for x, y in points]
        d.line(pts, fill=255, width=max(1, round(width / STEP)), joint='curve')
        rad = width / STEP / 2
        for x, y in pts: d.ellipse((x-rad, y-rad, x+rad, y+rad), fill=255)
    def mask(im): return np.array(im) > 0
    masses = layer(); md = ImageDraw.Draw(masses)
    building_masks = {}
    for b in plan['buildings']:
        one = layer(); od = ImageDraw.Draw(one)
        for m in b['masses']: box(md, m['bounds']); box(od, m['bounds'])
        building_masks[b['id']] = mask(one)
    palace = layer(); pd = ImageDraw.Draw(palace)
    box(pd, plan['palace']['bounds'])
    for g in plan['palace']['gates']:
        if 'bounds' in g: box(pd, g['bounds'])
    solids = mask(masses.filter(ImageFilter.MaxFilter(3))) | mask(palace.filter(ImageFilter.MaxFilter(3)))
    water = layer(); wd = ImageDraw.Draw(water)
    stroke(wd, plan['water']['centerline'], plan['water']['clearWidth']); poly(wd, plan['water']['pondPolygon'])
    wet = mask(water)
    banks = mask(water.filter(ImageFilter.MaxFilter(9)))  # 24px bank plus conservative8px foot half-width
    bridges = layer(); bd = ImageDraw.Draw(bridges)
    for bridge in plan['bridges']:
        x,y,bh,bv=bridge['bounds'];box(bd,[x+8,y+8,bh-16,bv-16])
    decks = mask(bridges)
    roads = layer(); rd = ImageDraw.Draw(roads)
    for r in plan['roads']: stroke(rd,r['points'],r['clearWidth']-16)
    road_mask = mask(roads)
    courts = layer(); cd=ImageDraw.Draw(courts)
    for c in plan['courts']: poly(cd,c['polygon'])
    for b in plan['buildings']:
        if b['door']:stroke(cd,[b['door'],b['approach']],b['entranceWidth'])
        if b.get('innerDoor'):stroke(cd,[b['innerDoor'],b['door']],b['entranceWidth'])
        for platform in b.get('platforms',[]):box(cd,platform['bounds'])
    court_mask=mask(courts.filter(ImageFilter.MinFilter(3)))
    walk=(road_mask | court_mask | decks) & ~solids & (~banks | decks)
    # Expose road crossings that would be hidden if water/masses were only subtracted.
    road_obstructions=[]
    for r in plan['roads']:
        one=layer();stroke(ImageDraw.Draw(one),r['points'],r['clearWidth']-16);m=mask(one)
        body=int(np.count_nonzero(m & solids));bank=int(np.count_nonzero(m & banks & ~decks))
        if body or bank:
            yy,xx=np.nonzero(m & (solids | (banks & ~decks)))
            road_obstructions.append({'road':r['id'],'massOrClosedPalaceCells':body,'protectedBankOutsideDeckCells':bank,'blockedBounds':[int(xx.min()*STEP),int(yy.min()*STEP),int(xx.max()*STEP),int(yy.max()*STEP)]})
    cells=set(zip(*np.nonzero(walk)))
    def nearest(point):return min(cells,key=lambda q:((q[1]+.5)*STEP-point[0])**2+((q[0]+.5)*STEP-point[1])**2)
    start=nearest(plan['spawn']);seen={start};todo=deque([start])
    while todo:
        y,x=todo.popleft()
        for q in [(y-1,x),(y+1,x),(y,x-1),(y,x+1)]:
            if q in cells and q not in seen:seen.add(q);todo.append(q)
    targets=[]
    for id,point in [(b['id'],b['approach']) for b in plan['buildings']]+[(n['id'],n['point']) for n in plan['npcs']]+[(d['id'],d['point']) for d in plan['discoveries']]:
        near=nearest(point);dist=math.hypot((near[1]+.5)*STEP-point[0],(near[0]+.5)*STEP-point[1])
        ix,iy=min(size[0]-1,max(0,int(point[0]/STEP))),min(size[1]-1,max(0,int(point[1]/STEP)))
        targets.append({'id':id,'point':point,'nearestWalkDistance':round(dist,2),'onClosedMass':bool(solids[iy,ix]),'inWaterOrBank':bool(banks[iy,ix] and not decks[iy,ix]),'reachable':near in seen and dist<=32 and not solids[iy,ix] and (not banks[iy,ix] or decks[iy,ix])})
    overlaps=[]
    ids=list(building_masks)
    for i,a in enumerate(ids):
        for b in ids[i+1:]:
            if np.any(building_masks[a] & building_masks[b]):overlaps.append([a,b])
    # Wall+classified gate spans must form a closed palace perimeter with no floating endpoints.
    boundary=[s['points'] for s in plan['palace']['segments']]+[g['boundaryLine'] for g in plan['palace']['gates']]
    degree=Counter(tuple(v) for line in boundary for v in [line[0],line[-1]])
    bad_ends=[{'point':list(k),'degree':v} for k,v in degree.items() if v!=2]
    # Ensure the one perimeter component is a ring, not two independent closed fragments.
    graph={}
    for line in boundary:
        a,b=map(tuple,[line[0],line[-1]]);graph.setdefault(a,set()).add(b);graph.setdefault(b,set()).add(a)
    reached={next(iter(graph))};queue=list(reached)
    while queue:
        for n in graph[queue.pop()]:
            if n not in reached:reached.add(n);queue.append(n)
    ring_ok=not bad_ends and len(reached)==len(graph)
    wall_layer=layer();wall_draw=ImageDraw.Draw(wall_layer)
    for seg in plan['palace']['segments']:stroke(wall_draw,seg['points'],plan['palace']['wallThickness'])
    ordinary=layer();ordinary_draw=ImageDraw.Draw(ordinary)
    for z in plan['zones']:
        if z['id'] in ['homes-north','homes-south','market']:poly(ordinary_draw,z['polygon'])
    domestic_wall_cells=int(np.count_nonzero(mask(wall_layer)&mask(ordinary)))
    # Identical normalized filled footprint silhouettes are flagged independently of color.
    signatures={};clones=[]
    for b in plan['buildings']:
        a=Image.fromarray((building_masks[b['id']]*255).astype('uint8'));crop=a.crop(a.getbbox());normalized=crop.resize((64,64),Image.Resampling.NEAREST)
        sig=hashlib.sha256(normalized.tobytes()).hexdigest()
        if sig in signatures:clones.append([signatures[sig],b['id']])
        signatures[sig]=b['id']
    # Roofless sculpture is intentionally a simple block; other repeated outlines still fail.
    clones=[pair for pair in clones if not ('monument' in pair or 'gate' in pair)]
    route_lengths=[]
    for r in plan['explorationRoutes']:
        length=sum(math.dist(a,b) for a,b in zip(r['points'],r['points'][1:]));route_lengths.append({'id':r['id'],'centerlineLength':round(length,1),'walkSecondsEstimate':round(length/plan['juni']['walkSpeed'],1),'runSecondsEstimate':round(length/plan['juni']['runSpeed'],1),'measuredInGame':False})
    bridge_checks=[]
    for b in plan['bridges']:
        x,y=b['crossing'];ix,iy=int(x/STEP),int(y/STEP)
        road=next(r for r in plan['roads'] if r['id']==b['road'])
        at=[q for q in road['points'] if q[0]==x]
        bridge_checks.append({'id':b['id'],'centerInContinuousWater':bool(wet[iy,ix]),'declaredRoad':road['id'],'straightAlignedApproach':len(at)>=2,'spansWaterAndBanks':b['bounds'][3]>=plan['water']['clearWidth']+2*plan['water']['bankReserveEachSide']+16})
    flags=[all(t['reachable'] for t in targets),not overlaps,not road_obstructions,ring_ok,not clones,all(all(b[k] for k in ['centerInContinuousWater','straightAlignedApproach','spansWaterAndBanks']) for b in bridge_checks),len(plan['bridges'])==2,len(seen)==len(cells),domestic_wall_cells==0]
    report={'kind':'PLANNING_ONLY_NOT_RUNTIME_OR_FORGE_NAV','status':'PASS' if all(flags) else 'FAIL','sampleCell':STEP,'walkCells':len(cells),'connectedCells':len(seen),'targets':targets,'overlappingBuildingMasses':overlaps,'roadObstructions':road_obstructions,'palaceBoundary':{'closedSingleRingIncludingClassifiedGates':ring_ok,'unmatchedEndpoints':bad_ends,'wallCellsInResidentialOrMarketZones':domestic_wall_cells},'normalizedFootprintClones':clones,'bridges':bridge_checks,'routeLengths':route_lengths,'limits':['Schematic ground reservations, not generated art, roof alpha, final collision, terrain hydrology or real gameplay.','No proposed map assembled; no new Forge bundle/nav/Tiled export or Phaser proof of proposal.','Road/court accessibility is approximate, with conservative8px radius; final16x8foot collision/occlusion/mobile checks await map authorization.']}
    if write:
        (OUT/'planning-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
        debug=Image.new('RGB',size,'#e9e5db');arr=np.array(debug);arr[solids]=[100,95,88];arr[banks]=[153,190,180];arr[wet]=[75,125,145];arr[walk]=[238,201,121]
        Image.fromarray(arr).resize((w//2,h//2),Image.Resampling.NEAREST).save(OUT/'planning-clearance.png')
    return report

if __name__=='__main__':
    p=json.loads((OUT/'zoning-plan.json').read_text());r=check(p)
    print(json.dumps({'status':r['status'],'unreachable':[t for t in r['targets'] if not t['reachable']],'overlaps':r['overlappingBuildingMasses'],'roadObstructions':r['roadObstructions'],'palace':r['palaceBoundary'],'clones':r['normalizedFootprintClones'],'connected':r['connectedCells'],'walkCells':r['walkCells']},ensure_ascii=False))
    if r['status']!='PASS':raise SystemExit(1)
