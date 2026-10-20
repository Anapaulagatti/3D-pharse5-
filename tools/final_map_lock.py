"""Small, editable ground-material finishing pass; no generation or tracing.

Authoring-only NumPy; the saved output is independently checked with Pillow.
The input is the original palette-finished V6 repair, on every rebuild.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import hashlib
import json
import numpy as np

R = Path(__file__).resolve().parents[1]
S = R / 'assets-src/final-map-lock'
OLD = R / 'assets-src/v6-path-fix'


def finish_ground(image):
    spec = json.loads((S / 'polish.json').read_text())
    source = np.array(image.convert('RGB'))
    result = source.copy()
    height, width = source.shape[:2]
    allowed = np.array(Image.open(OLD / 'edit-mask.png').convert('L')) > 0
    paths = json.loads((OLD / 'path-network.json').read_text())
    urban = np.array(Image.open(OLD / 'urban-mask.png')) > 0
    stone = np.array(Image.open(OLD / 'stone-mask.png')) > 0
    island = np.array(Image.open(OLD / 'island-mask.png')) > 0
    deck = np.array(Image.open(OLD / 'deck-mask.png')) > 0

    def mask_box(coords):
        mask = Image.new('L', (width, height))
        ImageDraw.Draw(mask).rectangle(tuple(coords), fill=255)
        return np.array(mask) > 0

    def rgb(mask, offset, saturation=1):
        mask = mask & allowed
        values = source[mask].astype(np.float32)
        luminance = values @ np.array([.2126, .7152, .0722])
        values = luminance[:, None] + (values - luminance[:, None])*saturation
        result[mask] = np.clip(np.rint(values + offset), 0, 255).astype(np.uint8)

    modern = urban & mask_box(spec['modernBounds'])
    rgb(modern, spec['modernTone']['offset'], spec['modernTone']['saturation'])
    # A restrained warm-to-cool stone handoff follows existing whole tile rows.
    x0, y0, x1, y1 = spec['connector']
    for y in range(y0, y1, 16):
        t = (y-y0)/(y1-y0)
        rgb(urban & mask_box([x0,y,x1,y+15]), [round(2-3*t), 1, round(3*t)])

    # Shared outer curb only: intersections never get an internal seam.
    paved = urban | stone
    inner = np.array(Image.fromarray(np.uint8(paved)*255).filter(ImageFilter.MinFilter(11))) > 0
    rgb(modern & ~inner, [-13,-10,-6])

    # Separate venue aprons through a native-texture variation and open inlays.
    route_openings = Image.new('L', (width,height))
    draw = ImageDraw.Draw(route_openings)
    for route in paths['paths']:
        if route['layer'] in ['urban','secondary']:
            draw.line([tuple(p) for p in route['points']], fill=255, width=route['clearWidth']+24, joint='curve')
    openings = np.array(route_openings)>0
    for venue in spec['courts']:
        court = next(c for c in paths['courts'] if c['id']==venue['id'])
        x0,y0,x1,y1 = court['box']
        area = mask_box(court['box']) & urban
        rgb(area, venue['tone'], 1.045)
        inset = mask_box([x0+4,y0+4,x1-4,y1-4])
        border = area & ~inset & ~openings
        rgb(border, [-20,-16,-9])

    # Round only the outer native sand corners, never the route cores/courts.
    sand = Image.fromarray(np.uint8(island)*255)
    rounded = sand.filter(ImageFilter.MinFilter(17)).filter(ImageFilter.MaxFilter(17))
    cut = island & ~(np.array(rounded)>0) & allowed
    # Clear-width envelopes are independently protected, not inferred visually.
    cores = Image.new('L',(width,height)); d = ImageDraw.Draw(cores)
    for route in paths['paths']:
        if route['layer']=='island':
            d.line([tuple(p)for p in route['points']],fill=255,width=route['clearWidth']+8,joint='curve')
    for court in paths['courts']:
        if court['box'][1]>=3968:
            d.rounded_rectangle(tuple(court['box']),radius=court.get('radius',0),fill=255)
    cut &= ~(np.array(cores)>0)
    tile = np.array(Image.open(R/'assets-src/v3-final/terrain/grass.png').convert('RGB'))
    yy,xx = np.nonzero(cut)
    result[yy,xx] = tile[yy%tile.shape[0],xx%tile.shape[1]]
    # Ease the inside of existing bends by at most eight native pixels, using
    # original sand pixels within the already-authorized shoulder envelope.
    closed = sand.filter(ImageFilter.MaxFilter(17)).filter(ImageFilter.MinFilter(17))
    basalt = np.array(Image.open(OLD/'basalt-mask.png'))>0
    add = (np.array(closed)>0) & ~island & allowed & ~urban & ~stone & ~basalt & ~deck
    tile = np.array(Image.open(R/'assets-src/v3-final/terrain/sand.png').convert('RGB'))
    yy,xx = np.nonzero(add)
    result[yy,xx] = tile[yy%tile.shape[0],xx%tile.shape[1]]
    # Literal three-pixel guide inlays on existing walking/deck material only.
    guides = Image.new('L',(width,height)); d=ImageDraw.Draw(guides)
    for name in ['mainland','island']:
        centre,start,end = spec['dockGuides'][name]
        for side in [-1,1]:
            x=centre+side*spec['dockGuides']['offsetFromCentre']
            d.line([(x,start),(x,end)],fill=255,width=spec['dockGuides']['width'])
    guide_mask = (np.array(guides)>0) & (urban|island|deck) & allowed
    rgb(guide_mask,[14,11,4])

    changed = np.any(result != source,axis=2)
    assert not np.any(changed & ~allowed)
    assert not np.any(changed[:2240]), 'Approved traditional upper half is frozen'
    out = Image.fromarray(result).convert('RGBA')
    Image.fromarray(np.uint8(changed)*255).save(S/'edit-mask.png')
    receipt={'baseline':spec['baseline'],'art_source':'existing','changedPixels':int(changed.sum()),'worldPixels':width*height,'fraction':float(changed.mean()),'northernPixelsChanged':0,'outsidePriorRepairMaskChanged':0,'resampling':'none','inputRGBSha256':hashlib.sha256(source.tobytes()).hexdigest(),'outputRGBSha256':hashlib.sha256(result.tobytes()).hexdigest(),'outsideEditMaskRGBSha256':hashlib.sha256(source[~changed].tobytes()).hexdigest(),'islandOuterCornerPixels':int(cut.sum()),'islandInnerCornerPixels':int(add.sum()),'guidePixels':int(guide_mask.sum())}
    (S/'processing.json').write_text(json.dumps(receipt,indent=2)+'\n')
    return out
