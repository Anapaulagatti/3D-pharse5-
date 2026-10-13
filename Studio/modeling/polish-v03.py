"""Original additive Living Hanok details. Never rewrites approved v0.2 assets."""
import sys, json
from pathlib import Path
from math import sin, cos, pi
import random
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import *

# Read the real editable sources before creating the separate additive layer.
audit = []
for name in ('arena-hero', 'mascot-base'):
    bpy.ops.wm.open_mainfile(filepath=str(ROOT / 'assets/source-blend' / (name + '.blend')))
    audit.append({'file': f'assets/source-blend/{name}.blend',
                  'objects': len(bpy.context.scene.objects),
                  'materials': [m.name for m in bpy.data.materials],
                  'nla_clips': sorted({t.name for o in bpy.context.scene.objects if o.animation_data
                                       for t in o.animation_data.nla_tracks}),
                  'saved_or_modified': False})
(ROOT / 'quality-reports/v0.3/blender-source-audit.json').write_text(json.dumps(audit, indent=2) + '\n')
reset()
R = random.Random(303)
M = {
    'wood': material('V03WarmTimber', '91654B', .74),
    'jade': material('V03CeladonGlaze', '72BEAC', .27, .05),
    'deep': material('V03LeafCeladon', '528C79', .58),
    'brass': material('V03QuietBrass', 'CFAC67', .38, .55),
    'coral': material('V03PlumCoral', 'E57B69', .85),
    'paper': material('V03FoldedHanji', 'F5EFE1', .9),
    'stone': material('V03WarmStone', 'BDB7A3', .9),
    'soil': material('V03GardenEarth', '766552', 1),
    'haze': material('V03DistanceHaze', 'B8C7CD', .96),
}

def folded_leaf(name, center, size, angle, mat, parent=None):
    x, y, z = center
    local = [(0, 0, 0), (-size*.38, size*.45, size*.1), (0, size, size*.24),
             (size*.38, size*.45, size*.1), (0, size*.45, size*.21)]
    verts = [(x+a*cos(angle)-b*sin(angle), y+a*sin(angle)+b*cos(angle), z+c) for a,b,c in local]
    return mesh(name, verts, [(0,1,4), (1,2,4), (2,3,4), (3,0,4)], mat, parent)

def blossom(center, radius=.105, mat=None, parent=None):
    x,y,z = center
    for k in range(5):
        a = k/5*2*pi
        folded_leaf('PlumFoldedPetal', center, radius, a, mat or M['paper'], parent)
    sphere('PlumGoldenHeart', (x,y,z+.025), (.025,.025,.025), M['brass'], 8, 4, parent)

# Dancheong-inspired restrained jade/coral bands, brackets and carved beam clouds.
for cx,cy,s in [(-1.5,1.6,1), (2.5,1.55,.58)]:
    w,d = 3.5*s, 2.3*s
    z = .45+1.45*s
    for side in [-1,1]:
        y = cy+side*(d*.36+.075)
        for i in range(9):
            x = cx+(i-4)*w/9
            box('BeamPatternJade', (x,y,z-.015), (.18*s,.013,.025*s), M['jade'], 0)
            box('BeamPatternCoral', (x+.035*s,y+side*.004,z-.075*s), (.08*s,.014,.025*s), M['coral'], 0)
        for x in [-w*.41,w*.41]:
            points=[(-.22,0),(-.17,-.07),(-.09,-.10),(0,-.18),(.09,-.10),(.17,-.07),(.22,0)]
            verts=[(cx+x+a*s,y+b,z-.06+c*s) for b in [-.04,.04] for a,c in points]
            n=len(points)
            faces=[tuple(range(n-1,-1,-1)),tuple(range(n,n*2))]
            faces += [(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
            mesh('CarvedCloudBracket',verts,faces,M['wood'])
            cylinder('JoineryPeg', (cx+x,y-side*.045,z-.04), .035*s,.025,M['brass'],10).rotation_euler.x=pi/2
    # Readable decorative eave end discs: small floral carving rather than extra tile rows.
    for i in range(7):
        x = -((w+.75*s)/2)+(w+.75*s)*i/6
        t=1
        roof_z=z+.2*s+.19+.13*(abs(x)/((w+.75*s)/2))**5
        y=cy-d*.66-.035
        disc=cylinder('RoofEndCeladonSeal',(cx+x,y,roof_z),.055*s,.016,M['jade'],12)
        disc.rotation_euler.x=pi/2
        for k in range(5):
            a=k/5*2*pi
            sphere('RoofSealPetal',(cx+x+.021*s*cos(a),y-.014,roof_z+.021*s*sin(a)),(.016*s,.007,.01*s),M['paper'],6,3)
    # Lattice diamonds under the front beam retain the view into the pavilion.
    for side in [-1,1]:
        x=cx+side*w*.41
        path('EntranceLatticeDiamond',[(x-.15*s,cy-d*.36,z-.28*s),(x,cy-d*.36,z-.14*s),
                                     (x+.15*s,cy-d*.36,z-.28*s),(x,cy-d*.36,z-.42*s),
                                     (x-.15*s,cy-d*.36,z-.28*s)],.012*s,M['jade'])

# An irregular path leads from the entry around the dais, with no clutter at its center.
for i,(x,y) in enumerate([(1.85,.55),(1.65,.18),(1.50,-.21),(1.22,-.54),(.94,-.8),(.62,-1.22),(.5,-1.75)]):
    stone=cylinder('HandmadeSteppingStone',(x,y,.162),.23,.055,M['stone' if i%3 else 'paper'],7)
    stone.scale=(1,.65+.1*(i%2),1)
    stone.rotation_euler.z=i*.81
    box('SteppingStoneInlay',(x,y,.191),(.18,.018,.009),M['jade'],0).rotation_euler.z=i*.81

# Small pots with actual rim/interior, soil and asymmetric paper foliage.
for i,(x,y) in enumerate([(-3.65,-2.35),(-2.2,-2.85),(.9,2.58),(3.75,.60),(3.7,-2.75),(-.1,.02)]):
    pot=lathe('HandThrownPot',[(0,.09),(.035,.14),(.11,.20),(.25,.18),(.30,.15),(.30,.13),(.245,.13)],M['jade' if i%2 else 'paper'],16)
    pot.location=(x,y,.16)
    ring('PotBrassLip',.146,.46,.009,M['brass'],(x,y))
    cylinder('PotGardenSoil',(x,y,.425),.128,.018,M['soil'],12)
    for k in range(5):
        folded_leaf('PotFoldedLeaf',(x,y,.43),.25+R.random()*.1,k/5*2*pi+.3*i,M['deep' if k%2 else 'jade'])

# Low garden borders and an inviting tiny tea/storytelling vignette.
for i in range(7):
    x=-3.7+i*.21
    cylinder('GardenBorderPebble',(x,-2.76,.23),.11,.13,M['stone' if i%2 else 'paper'],7)
box('TeaTray',(-2.6,.10,.455),(.32,.23,.028),M['wood'],.01)
for x in [-2.66,-2.54]:
    lathe('TinyTeaCup',[(0,.035),(.025,.047),(.075,.05),(.08,.045),(.067,.036)],M['jade'],12).location=(x,.1,.474)
box('FoldedLetter',(-2.32,.08,.465),(.14,.17,.012),M['paper'],0).rotation_euler.z=.2
path('LetterFold',[(-2.39,.015,.478),(-2.31,.09,.478),(-2.26,.025,.478)],.004,M['brass'])
for x,y in [(-3.35,-2.35),(-2.65,-2.30),(3.85,-2.0),(1.2,2.65)]:
    for k in range(3):
        folded_leaf('LowGardenLeaf',(x,y,.22),.18,k*2.1,M['deep'])
    blossom((x+.07,y,.32),.07,M['coral'])

# Opaque distant layer on the back edge; no transparent skyline overdraw.
for i in range(9):
    h=.45+.15*(i%4)
    x=-3.5+i*.82
    box('DistantMiniatureSkyline',(x,3.54,.16+h/2),(.56,.14,h),M['haze'],.02)

# Merge all static props into material primitives; keep just three wind pivots separate.
static=[o for o in bpy.context.scene.objects if o.type=='MESH']
join('HanokPolishStatic',static)
for i,center in enumerate([(-3.50,-1.2,1.65),(-2.6,-1.22,1.8),(-3.15,-.62,1.98)]):
    pivot=empty(f'WindPlum{i+1:02d}',center)
    parts=[]
    for j in range(5):
        c=(R.uniform(-.3,.3),R.uniform(-.27,.27),R.uniform(-.12,.12))
        before=set(bpy.context.scene.objects)
        blossom(c,.12,M['paper' if j%2 else 'coral'],pivot)
        folded_leaf('PlumLeaf',(c[0],c[1],c[2]-.045),.19,j*1.9,M['deep'],pivot)
        parts.extend(o for o in bpy.context.scene.objects if o not in before and o.type=='MESH')
    obj=join(f'PlumCluster{i+1:02d}',parts)
    obj.parent=pivot
    animation(pivot,'GardenBreeze',[(f,{'rotation_euler':(.035*sin((f-1)/90*2*pi+i),.018*cos((f-1)/90*2*pi+i),0)}) for f in [1,16,31,46,61,76,91]])

for m in bpy.data.materials:
    m.use_backface_culling=False  # folded hanji/petals are deliberately two-sided
src=ROOT/'assets/v0.3/source-blend/hanok-polish.blend'
out=ROOT/'exports/v0.3/models/hanok-polish.glb'
src.parent.mkdir(parents=True,exist_ok=True)
out.parent.mkdir(parents=True,exist_ok=True)
bpy.context.scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(src))
bpy.ops.export_scene.gltf(filepath=str(out),export_format='GLB',export_yup=True,
                          export_animations=True,export_animation_mode='NLA_TRACKS',
                          export_nla_strips=True,export_force_sampling=True,export_cameras=False,export_lights=False)
print('V03_ADDITIVE_LAYER_SAVED',out.stat().st_size)
