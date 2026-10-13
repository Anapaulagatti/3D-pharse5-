"""Reproducible original Hanok Rooftop Arena: Blender source + animated GLB."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import *
from math import sin, cos, pi
import random

reset()
M = materials()
R = random.Random(231)


def roof(name, center, width, reach, z):
    cx, cy = center
    def height(x, t):
        return z + .62*(1-t)**1.6 + .19*t**6 + .13*(abs(x)/(width/2))**5
    for side in [-1, 1]:
        verts = []
        nx, ny = 28, 12
        for j in range(ny+1):
            t = j/ny
            for i in range(nx+1):
                x = -width/2 + width*i/nx
                verts.append((cx+x, cy+side*t*reach, height(x, t)))
        faces = [(j*(nx+1)+i, j*(nx+1)+i+1, (j+1)*(nx+1)+i+1, (j+1)*(nx+1)+i)
                 for j in range(ny) for i in range(nx)]
        mesh(name+'RoofSurface', verts, faces, M['ink'], smooth=True)
        for i in range(25):
            x = -width/2+width*i/24
            pts = [(cx+x, cy+side*reach*j/16, height(x, j/16)+.035) for j in range(17)]
            path(name+'RoofTileRib', pts, .032, M['navy'])
            tip = pts[-1]
            cap = cylinder(name+'TileEnd', tip, .043, .06, M['ink'], 12)
            cap.rotation_euler.x = pi/2
            sphere(name+'TileStamp', (tip[0], tip[1]+side*.038, tip[2]), (.016, .01, .016), M['brass'], 8, 4)
        for t in [.25, .5, .75]:
            pts = [(cx-width/2+width*i/24, cy+side*reach*t, height(-width/2+width*i/24,t)+.025) for i in range(25)]
            path(name+'TileSeam', pts, .008, M['haze_dark'])
        pts = [(cx-width/2+width*i/24, cy+side*reach, height(-width/2+width*i/24,1)-.025) for i in range(25)]
        path(name+'CeladonEave', pts, .045, M['jade_dark'])
    path(name+'Ridge', [(cx-width/2, cy, z+.85), (cx-width*.4, cy, z+.69),
                       (cx, cy, z+.67), (cx+width*.4, cy, z+.69), (cx+width/2, cy, z+.85)], .075, M['ink'])
    for side in [-1, 1]:
        sphere(name+'RidgeFinial', (cx+side*width/2, cy, z+.87), (.1, .09, .13), M['brass'], 12, 6)


def pavilion(cx, cy, scale=1, gateway=False):
    floor = .2
    w, d = 3.5*scale, 2.3*scale
    box('PavilionStoneFoundation', (cx, cy, floor), (w+.35, d+.2, .24), M['stone'], .08)
    for i in range(14):
        box('TimberFloorPlank', (cx-w/2+(i+.5)*w/14, cy, floor+.145), (w/14-.015, d, .06), M['wood_light'], .01)
    for x in [-w*.41, w*.41]:
        for y in [-d*.36, d*.36]:
            cylinder('ColumnStoneShoe', (cx+x,cy+y,.4), .16*scale,.15,M['stone'],16)
            cylinder('TimberColumn', (cx+x,cy+y,.4+.75*scale), .075*scale,1.5*scale,M['wood'],16)
            for side in [-1, 1]:
                box('BracketBlock', (cx+x+side*.1*scale,cy+y,.45+1.4*scale),(.22*scale,.13*scale,.11*scale),M['coral'],.014)
                box('BracketCorbel',(cx+x+side*.07*scale,cy+y,.45+1.3*scale),(.17*scale,.12*scale,.07*scale),M['wood_light'],.01)
    z = .45+1.45*scale
    for y in [-d*.36,d*.36]:
        box('CrossBeam',(cx,cy+y,z),(w+.3,.14*scale,.17*scale),M['wood'],.025)
        box('CeladonBeamAccent',(cx,cy+y-.075,z+.035),(w+.24,.025,.035),M['jade'],.01)
    for x in [-w*.41,w*.41]:
        box('SideBeam',(cx+x,cy,z),(.16*scale,d+.25,.16*scale),M['wood'],.018)
    if not gateway:
        for x in [-w*.28, 0, w*.28]:
            box('PaperScreen',(cx+x,cy+d*.35, .45+.65*scale),(.85*scale,.04,1.05*scale),M['paper'],.01)
            for k in range(7):
                box('ScreenVerticalLattice',(cx+x+(k-3)*.13*scale,cy+d*.32,.45+.65*scale),(.016,.034,1.06*scale),M['wood'],.003)
            for k in range(6):
                box('ScreenHorizontalLattice',(cx+x,cy+d*.32,.45+(.18+k*.18)*scale),(.87*scale,.034,.016),M['wood'],.003)
        for step in range(3):
            box('EntryStep',(cx,cy-d/2-.11-step*.17,.24-step*.055),(1.4*scale,.28,.12),M['stone'],.035)
    roof('Hanok' if not gateway else 'Gateway', (cx,cy), w+.75*scale, d*.66, z+.2*scale)


box('FloatingDioramaBase',(0,0,-.35),(8.8,7.4,.7),M['jade_dark'],.22)
box('CeladonUpperRim',(0,0,.006),(8.75,7.35,.1),M['jade'],.13)
box('CourtyardSurface',(0,0,.06),(8.5,7.1,.07),M['stone'],.12)
# Stone paving deliberately stops at the water garden.
for x in range(10):
    for y in range(8):
        px, py = -3.9+x*.72, -3+y*.76
        if px>1.8 and py<.4:
            continue
        box('CourtyardPaving',(px,py,.115),(.69,.73,.045),M['stone' if (x+y)%4 else 'cream'],.018)
for i in range(13):
    box('PlinthInsetStone',(-3.9+i*.64,-3.65,-.32),(.53,.035,.28),M['jade'],.035)
pavilion(-1.5,1.6)
pavilion(2.5,1.55,.58,True)

# Ceramic arena dais, carved brass radial growth marks.
cylinder('DaisFoundation',(-.4,-1,.2),1.22,.19,M['stone'],64)
cylinder('CeladonDais',(-.4,-1,.34),1.15,.18,M['jade'],64)
cylinder('DaisPorcelainFace',(-.4,-1,.445),1.09,.035,M['cream'],64)
ring('DaisBrassInlay',1.03,.468,.016,M['brass'],(-.4,-1))
ring('DaisInnerRing',.77,.47,.008,M['jade_dark'],(-.4,-1))
for i in range(12):
    a=i/12*2*pi
    o=box('DaisRadialMark',(-.4+.92*cos(a),-1+.92*sin(a),.473),(.095,.018,.01),M['brass'],.003)
    o.rotation_euler.z=a

# Narrow jade water channel with solid stylized ripples.
box('GardenChannel',(2.85,-1.55,.1),(1.5,3.1,.12),M['jade_dark'],.12)
box('WaterSurface',(2.85,-1.55,.17),(1.32,2.9,.018),M['jade'],.09)
for i in range(5):
    ring('WaterRipple',.12+i*.023,.187,.004,M['cream'],(2.85,-2.2))
for side in [-1,1]:
    box('ChannelStoneEdge',(2.85+side*.78,-1.55,.18),(.16,3.2,.15),M['stone'],.04)
for i in range(11):
    t=i/10
    z=.32+.19*sin(t*pi)
    box('ArchedBridgePlank',(2.05+t*1.6,-1.3,z),(.15,.76,.065),M['wood_light'],.018)
for side in [-1,1]:
    pts=[(2.05+i/12*1.6,-1.3+side*.36,.55+.19*sin(i/12*pi)) for i in range(13)]
    path('BridgeHandrail',pts,.028,M['wood'])
    for i in [0,3,7,10]:
        cylinder('BridgeRailPost',(2.05+i/10*1.6,-1.3+side*.36,.43+.17*sin(i/10*pi)),.025,.36,M['wood'],10)

# Rock garden and a deliberately sparse five-petal plum tree.
box('PlumGardenBed',(-3,-1.6,.17),(1.6,2.2,.17),M['jade_dark'],.12)
for i in range(8):
    x,y=-3+R.uniform(-.5,.5),-1.6+R.uniform(-.85,.85)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=1,location=(x,y,.27))
    o=bpy.context.object
    o.scale=(R.uniform(.13,.28),R.uniform(.1,.2),R.uniform(.1,.22))
    finish(o,'GardenRock',M['stone'])
path('PlumTrunk',[(-3,-1.15,.22),(-3.05,-1.13,.65),(-2.98,-1.1,1.15),(-3.15,-1.15,1.65)],.065,M['wood'])
for i in range(8):
    a=i/8*2*pi
    tip=(-3+cos(a)*.7,-1.15+sin(a)*.6,1.45+R.uniform(-.1,.6))
    path('PlumBranch',[(-3,-1.12,.9),(-3+cos(a)*.35,-1.15+sin(a)*.25,1.35),tip],.025,M['wood'])
    for j in range(3):
        c=(tip[0]+R.uniform(-.15,.15),tip[1]+R.uniform(-.12,.12),tip[2]+R.uniform(-.1,.1))
        for k in range(5):
            t=k/5*2*pi
            petal=sphere('PlumPetal',(c[0]+.06*cos(t),c[1]+.06*sin(t),c[2]),(.062,.041,.022),M['coral' if j%2 else 'cream'],10,5)
            petal.rotation_euler.z=t
        sphere('PlumFlowerHeart',c,(.022,.022,.028),M['brass'],8,4)

# Potted ceramic seed shapes and wood benches.
for x,y in [(-2.3,.2),(1.6,-2.8),(.4,2.8)]:
    lathe('CeramicPlanter',[(0,.12),(.18,.2),(.36,.16)],M['jade'],24).location=(x,y,.15)
    for i in range(5):
        t=i/5*2*pi
        leaf=sphere('FoldedGardenLeaf',(x+.11*cos(t),y+.11*sin(t),.63),(.065,.025,.22),M['jade_dark'],10,5)
        leaf.rotation_euler=(.5*cos(t),.5*sin(t),t)
for x,y in [(1,-2.8),(-2.6,.1)]:
    box('TimberBench',(x,y,.39),(.85,.32,.08),M['wood_light'],.04)
    for s in [-1,1]: box('BenchFoot',(x+s*.28,y,.23),(.1,.21,.3),M['wood'],.02)

# Stylized opaque skyline; no copyrighted signage or architectural replicas.
for i in range(11):
    x=-3.6+i*.7
    h=.75+R.random()*1.25
    box('SeoulSkylineBlock',(x,3.35,.15+h/2),(.42,.3,h),M['haze' if i%2 else 'haze_dark'],.035)
    for k in range(3):
        box('SkylineFacadeBand',(x,3.17,.4+k*h/3),(.31,.014,.025),M['cream'],.004)
cylinder('HillObservatoryShaft',(2.6,3.35,1.75),.055,2.7,M['haze_dark'],12)
cylinder('HillObservatoryDeck',(2.6,3.35,2.52),.2,.2,M['haze'],16)
cylinder('HillObservatorySpire',(2.6,3.35,3.0),.025,.75,M['haze_dark'],8)

# Merge static geometry; animated lanterns remain separate nodes.
join('ArenaArchitecture',[o for o in bpy.context.scene.objects if o.type=='MESH'])
for i,(x,y,z) in enumerate([(-2.1,-2.5,1.25),(1.5,-2.2,1.25),(.9,.75,1.35),(-2.6,1.35,1.55)]):
    support=[]
    support.append(cylinder('LanternPole',(x-.2,y,z/2+.13),.035,z,M['wood'],12))
    support.append(box('LanternBracket',(x-.1,y,z+.12),(.4,.05,.06),M['wood'],.018))
    join('LanternSupport'+str(i),support)
    pivot=empty(f'LanternSwing{i+1:02d}',(x,y,z))
    bits=[]
    bits.append(cylinder('PaperLanternCore',(0,0,-.25),.125,.29,M['glow'],12,parent=pivot))
    for h in [-.1,-.4]:
        bits.append(cylinder('LanternRim',(0,0,h),.15,.045,M['brass'],12,parent=pivot))
    for k in range(6):
        a=k/6*2*pi
        bits.append(cylinder('LanternRib',(.133*cos(a),.133*sin(a),-.25),.008,.3,M['wood'],6,parent=pivot))
    joined=join(f'LanternMesh{i+1:02d}',bits)
    joined.parent=pivot
    # Joining keeps the common pivot-local coordinates.
    animation(pivot,'LanternSway',[(f,{'rotation_euler':(.055*sin((f-1)/90*2*pi+i),.035*sin((f-1)/90*2*pi+i*.6),0)}) for f in [1,16,31,46,61,76,91]])

lighting_camera(orthoscale=12.8)
save_export('arena-hero')
