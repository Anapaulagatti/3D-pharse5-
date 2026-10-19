"""Terrain-layer-only V6 repairs from the approved native source textures.

This edits route masks and material placement, never source sprites, physics,
world extent, spawns, landmark positions, or character rendering/movement.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import json
import math
import numpy as np

R = Path(__file__).resolve().parents[1]
S = R / 'assets-src/v6-path-fix'
W, H = 4352, 5312


def blank():
    return Image.new('L', (W, H))


def union(*images):
    return Image.fromarray(np.maximum.reduce([np.array(im) for im in images]))


def polyline(points, width, soft=False, cap='default'):
    m = blank()
    d = ImageDraw.Draw(m)
    points = [tuple(p) for p in points]
    if cap == 'butt':
        # Cover rounded integer samples at a diagonal butt edge without adding
        # a large square endpoint jut. This extends terrain by only two pixels.
        for index, neighbor in [(0, 1), (-1, -2)]:
            x,y = points[index]
            dx,dy = x-points[neighbor][0],y-points[neighbor][1]
            length = math.hypot(dx,dy)
            points[index] = (round(x+2*dx/length),round(y+2*dy/length))
    d.line(points, fill=255, width=width, joint='curve')
    # Soft paths have a constant-width rounded envelope; urban ends are square.
    if cap == 'butt':
        return m
    if soft:
        for x, y in points:
            r = width // 2
            d.ellipse((x-r, y-r, x+r-1, y+r-1), fill=255)
    else:
        for x, y in points:
            r = width // 2
            d.rectangle((x-r, y-r, x+r-1, y+r-1), fill=255)
    return m


def box(coords, radius=0):
    m = blank()
    ImageDraw.Draw(m).rounded_rectangle(tuple(coords), radius=radius, fill=255)
    return m


def repair_ground(base, land, walk, old_roads):
    spec = json.loads((S / 'path-network.json').read_text())
    layers = {key: blank() for key in ['urban', 'secondary', 'nature', 'island', 'stone', 'basalt']}
    for row in spec['paths']:
        key = row['layer']
        layers[key] = union(layers[key], polyline(row['points'], row['width'], row.get('soft', False), row.get('cap', 'default')))
    for row in spec['courts']:
        key = row['layer']
        layers[key] = union(layers[key], box(row['box'], row.get('radius', 0)))

    # Remove inherited island road envelopes before painting one coherent network.
    # The previous V6 pasted old Jeju ground AND drew new paths over it.
    inherited = blank()
    for filename in ['nature-path-mask.png', 'modern-paving-mask.png']:
        p = R / 'assets-src/v3-final/map' / filename
        im = Image.open(p).convert('L').crop((0, 3648, W, 4800))
        shifted = blank()
        shifted.paste(im, (0, 3968))
        inherited = union(inherited, shifted)
    for row in spec['eraseBoxes']:
        inherited = union(inherited, box(row))
    inherited = union(inherited, old_roads)
    # Erase inherited stone/path envelopes, not the connecting traditional sand
    # streets. In particular, never surround a new butt join with a grass moat.
    old_materials = Image.new('L',(W,2240))
    old_materials.paste(Image.open(R/'assets-src/living-korea/north/semantic-materials.png'),(1024,0))
    materials = np.array(old_materials)
    old = np.array(inherited)>0
    old[:2240] &= materials == 4
    erase_image = Image.fromarray(np.uint8(old)*255).filter(ImageFilter.MaxFilter(17))
    erase = np.array(erase_image)>0
    erase[:2240] &= ~np.isin(materials,[1,2,3])
    # New road geometry is overlaid directly. Only the OLD path has shoulders
    # cleared, so existing streets meet a repaired endpoint without a gap.
    new_edges = union(*layers.values()).filter(ImageFilter.MaxFilter(9))
    shoulder = union(Image.fromarray(np.uint8(erase)*255),new_edges)
    la = np.array(land) > 0
    edit = (np.array(shoulder) > 0) & la
    # Existing shore geometry, every island/mainland jetty, and open water stay exact.
    protect = np.zeros((H, W), dtype=bool)
    protect[3776:3937, 2432:2561] = True
    protect[3968:4225, 2432:2561] = True
    edit &= ~protect
    erase &= la & ~protect
    masks = {k: (np.array(v) > 0) & la & ~protect for k, v in layers.items()}
    # Surface the existing approved deck supports, not open water. Their exact
    # walk envelope/physics remains unchanged. Original pier sprites stay exact.
    deck_regions = union(*(box(q) for q in spec['deckSurface']['regions']))
    deck = (np.array(deck_regions)>0) & (np.array(walk)>0)
    masks['deck'] = deck
    edit |= deck
    textures = {}

    def material(name):
        if name not in textures:
            if name in ['jetty-wood','jetty-fascia']:
                section = 'floorBox' if name=='jetty-wood' else 'fasciaBox'
                im = Image.open(R/spec['deckSurface']['source']).convert('RGBA').crop(spec['deckSurface'][section])
                assert np.array(im)[:,:,3].min()==255, 'Deck source crop must be entirely original opaque pixels'
                a = np.array(im.convert('RGB'))
            else:
                p = R / f'assets-src/modern-streets/terrain/{name}.png'
                if not p.exists():
                    p = R / f'assets-src/v3-final/terrain/{name}.png'
                a = np.array(Image.open(p).convert('RGB'))
            textures[name] = Image.fromarray(a[(np.arange(H) % a.shape[0])[:,None], (np.arange(W) % a.shape[1])[None,:]])
        return textures[name]

    def fill(mask, name):
        base.paste(material(name), (0,0), Image.fromarray(np.uint8(mask) * 255))

    fill(erase, 'grass')
    for key in ['nature', 'island']:
        fill(masks[key], 'sand')
    # One union per material: curbs follow outer street edges, never seam across joins.
    urban = masks['urban'] | masks['stone']
    edge = np.array(Image.fromarray(np.uint8(urban)*255).filter(ImageFilter.MaxFilter(9))) > 0
    edge &= edit
    fill(edge, 'concrete')
    fill(urban, 'paver')
    fill(masks['secondary'], 'concrete')
    fill(masks['basalt'], 'basalt')
    fill(deck, 'jetty-wood')
    inset = np.array(Image.fromarray(np.uint8(deck)*255).filter(ImageFilter.MinFilter(9)))>0
    fill(deck & ~inset, 'jetty-fascia')
    # All modifications are recorded at pixel resolution for an exact locality guard.
    S.mkdir(exist_ok=True)
    Image.fromarray(np.uint8(edit)*255).save(S / 'edit-mask.png')
    for key, mask in masks.items():
        Image.fromarray(np.uint8(mask)*255).save(S / f'{key}-mask.png')
    return base
