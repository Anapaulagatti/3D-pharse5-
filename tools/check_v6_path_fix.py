"""Offline exact preservation, path geometry and actual painted-path checks."""
from pathlib import Path
from PIL import Image, ImageChops
import json, hashlib, math

R = Path(__file__).resolve().parents[1]
S = R / 'assets-src/v6-path-fix'
P = R / 'assets-src/v6-restructure/map'


def read(p):
    return json.loads(p.read_text())


def sha(p):
    with p.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def digest(v):
    return hashlib.sha256(json.dumps(v, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


manifest = read(S / 'preservation.json')
bundle = read(P / 'outdoor-bundle.json')
for key, h in manifest['geometryHashes'].items():
    assert digest(bundle[key]) == h, ('Approved V6 geometry changed', key)
for name, h in manifest['files'].items():
    assert sha(R / name) == h, ('Approved character/prop changed', name)
assert sha(P / 'land-mask.png') == manifest['landHash']
assert sha(P / 'walk-mask.png') == manifest['walkHash']
mask = Image.open(S / 'edit-mask.png').convert('L')
assert sha(S / 'edit-mask.png') == manifest['editMaskSha256']
ground = Image.open(P / 'ground-native.png').convert('RGB')
# Hash exactly the same row-major unmasked RGB pixels as the baseline receipt,
# using contiguous runs. Offline setup/CI requires Pillow only, not authoring
# NumPy/Forge dependencies.
pixels, selected = ground.tobytes(), mask.tobytes()
assert set(selected) <= {0,255}, 'Repair mask must be binary'
outside = hashlib.sha256()
width,height = ground.size
for y in range(height):
    row = selected[y*width:(y+1)*width]
    pos = 0
    while pos < width:
        start = row.find(b'\x00',pos)
        if start < 0:
            break
        end = row.find(b'\xff',start)
        if end < 0:
            end = width
        outside.update(pixels[(y*width+start)*3:(y*width+end)*3])
        pos = end
assert outside.hexdigest() == manifest['outsideEditMaskRGBSha256'], 'Ground changed outside targeted repair mask'

spec = read(S / 'path-network.json')
painted = Image.new('L',mask.size)
for name in ['urban', 'secondary', 'nature', 'island', 'stone', 'basalt', 'deck']:
    painted = ImageChops.lighter(painted,Image.open(S / f'{name}-mask.png').convert('L'))
# The original V6 has decks beyond the land shoreline. Their exact walk/land
# masks are protected; only explicitly recorded original supports can receive
# reused timber surfacing. This must never create a new water corridor.
land = Image.open(P / 'land-mask.png').convert('L')
walk = Image.open(P / 'walk-mask.png').convert('L')
existing_decks = ImageChops.subtract(walk,land)
deck = Image.open(S / 'deck-mask.png').convert('L')
assert ImageChops.subtract(deck,walk).getbbox()is None, 'Deck surfacing must not enlarge walkable water'
assert ImageChops.subtract(ImageChops.multiply(mask,existing_decks),deck).getbbox()is None
painted_pixels = painted.load()
frontages = 0
objects = {o['id']:o for o in bundle['objects']}
for court in spec['courts']:
    if court.get('touchesObject'):
        obj = objects[court['touchesObject']]
        x0,y0,x1,y1 = court['box']
        assert x0 <= obj['x'] <= x1 and y0 <= obj['y'] <= y1, ('Court stops short of actual landmark feet',court['id'],obj['y'])
        assert painted_pixels[round(obj['x']),round(obj['y'])], ('Actual threshold is not visibly paved',court['id'])
        frontages += 1
failures = []
samples = 0
for route in spec['paths']:
    for a, z in zip(route['points'], route['points'][1:]):
        dx, dy = z[0]-a[0], z[1]-a[1]
        distance = math.hypot(dx,dy)
        if not distance:
            continue
        for i in range(math.ceil(distance/8)+1):
            t = min(1, i*8/distance)
            for off in [-(route['clearWidth']/2-8), 0, route['clearWidth']/2-8]:
                x, y = a[0]+dx*t-dy/distance*off, a[1]+dy*t+dx/distance*off
                samples += 1
                hit = next((q for q in bundle['collision']['solids'] if x+8>q['x'] and x-8<q['x']+q['w'] and y+4>q['y'] and y-4<q['y']+q['h']), None)
                if hit:
                    failures.append({'route':route['id'],'point':[x,y],'reason':hit['reason']})
                # Authored jetty decks remain literal source art outside the terrain mask.
                if not painted_pixels[round(x), round(y)]:
                    failures.append({'route':route['id'],'point':[x,y],'reason':'Route center/shoulder is not on its visible painted path'})

report = {'status':'PASS' if not failures else 'FAIL','baseline':manifest['baselineCommit'],'placementsUnchanged':len(bundle['objects']),'sourceImagesUnchanged':len(bundle['props']),'collidersUnchanged':len(bundle['collision']['solids']),'protectedFiles':len(manifest['files']),'paths':len(spec['paths']),'strictFootAndShoulderSamples':samples,'landmarkThresholdsTouchingPaving':frontages,'outsideMaskGroundExact':True,'landAndWalkMasksExact':True,'failures':failures,'method':'Original eight-by-four feet and declared shoulders sampled every8px against exact unchanged552collision rectangles; every route sample is on real path/deck material. Only existing walkable supports receive timber; no collision/speed/tolerance relaxation.'}
out = R / 'docs/v6-path-fix/quality/path-clearance.json'
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(report,indent=2)+'\n')
assert not failures, json.dumps(failures[:12])
print(json.dumps({k:v for k,v in report.items() if k!='failures'}))
