"""Original versioned Hanok narrative/detail layer, complementary to preserved v0.3."""
import sys,random
from pathlib import Path
from math import sin,cos,pi
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
reset();R=random.Random(404)
# Hero-distance brass bands use 24 segments instead of the base helper's 64.
def ring(name,radius,z,thickness,mat,center=(0,0),waves=0,parent=None):
 return path(name,[(center[0]+radius*cos(i/24*2*pi),center[1]+radius*sin(i/24*2*pi),z) for i in range(25)],thickness,mat,parent)
M={'jade':material('V04Celadon','72BEAC',.28,.05),'wood':material('V04HoneyTimber','98714F',.72),'dark':material('V04CarvedInk','293C55',.68),'coral':material('V04BlossomCoral','E57B69',.82),'paper':material('V04IvoryHanji','F5EFE1',.93),'green':material('V04GardenSage','7AA582',.9),'brass':material('V04AgedBrass','CFAC67',.42,.45),'stone':material('V04WarmStone','BDB7A3',.9),'sky':material('V04DistantBlue','BCD2DB',1)}
def leaf(center,r,angle,mat,parent=None):
 x,y,z=center
 verts=[(x,y,z),(x+r*.55*cos(angle-.5),y+r*.55*sin(angle-.5),z+.015),(x+r*cos(angle),y+r*sin(angle),z+.07),(x+r*.55*cos(angle+.5),y+r*.55*sin(angle+.5),z+.015),(x+r*.52*cos(angle),y+r*.52*sin(angle),z+.065)]
 return mesh('CraftPetal',verts,[(0,1,4),(1,2,4),(2,3,4),(3,0,4)],mat,parent)
def flower(c,r=.12,mat=None,parent=None):
 for i in range(5):leaf(c,r,i*2*pi/5,mat or M['paper'],parent)
 sphere('FlowerHeart',c,(.022,.022,.027),M['brass'],8,4,parent)
# Larger crafted ridge crests, scalloped roof ornaments and entrance joinery read in hero view.
for cx,cy,s in [(-1.5,1.6,1),(2.5,1.55,.58)]:
 ridge=.45+1.45*s+.2*s+.67
 for offset in [-1.35,0,1.35]:
  x=cx+offset*s
  path('CeladonRidgeCrest',[(x-.15*s,cy,ridge),(x-.10*s,cy,ridge+.11*s),(x,cy,ridge+.22*s),(x+.10*s,cy,ridge+.11*s),(x+.15*s,cy,ridge)],.022*s,M['jade'])
  sphere('CrestBrassBud',(x,cy,ridge+.22*s),(.035*s,.035*s,.055*s),M['brass'],10,5)
 for side in [-1,1]:
  x=cx+side*1.43*s;y=cy-.80*s
  box('CarvedEntryFrame',(x,y,1.1*s+.35),(.10*s,.10*s,1.3*s),M['wood'],.016)
  for k in range(3):
   ring('CarvedColumnMedallion',.048*s,.48+k*.42*s,.007*s,M['jade'],(x,y))
  # Low side railing, keep the central entrance open.
  for k in range(5):box('PavilionRailSpindle',(x,cy+(-.65+k*.30)*s,.68),(.035*s,.035*s,.45),M['wood'],.004)
  box('PavilionSideHandrail',(x,cy,.93),(.07*s,1.45*s,.06),M['jade'],.008)
 for k in range(3):box('EntranceStep',(cx,cy-1.40*s-k*.13,.16+k*.043),(1.25*s,.18,.08),M['stone'],.015)
 # Folded paper valance with soft hanging ties under the beam, rear of character.
 for k in range(3):
  x=cx+(k-1)*.35*s
  box('FoldedPaperValance',(x,cy-.67*s,1.74*s+.35),(.27*s,.018,.17*s),M['paper'],.005)
  path('ValanceFold',[(x-.12*s,cy-.69*s,1.78*s+.35),(x,cy-.70*s,1.64*s+.35),(x+.12*s,cy-.69*s,1.78*s+.35)],.007,M['brass'])
# Pedestal lotus edge and elegant patterned promenade, keeping character footprint free.
for i in range(16):
 a=i/16*2*pi;x=-.4+1.20*cos(a);y=-1+1.20*sin(a)
 leaf((x,y,.325),.10,a,M['jade'])
for x,y in [(-1.5,-2.3),(-.7,-2.65),(.1,-2.75),(1.0,-2.25),(1.5,-1.0)]:
 box('PromenadeStone',(x,y,.163),(.43,.34,.025),M['stone'],.018).rotation_euler.z=.08*sin(x*4)
 for side in [-1,1]:leaf((x+side*.10,y,.18),.09,side*pi/2,M['jade'])
# Two inhabited corners: folded cushion / tea utensils, glazed vessels / paper keepsake.
for x,y in [(-2.6,.12),(1,-2.8)]:
 box('BenchIvoryCushion',(x,y,.46),(.33,.28,.065),M['paper'],.035)
 box('CushionCoralRibbon',(x,y,.495),(.035,.275,.008),M['coral'],.003)
for i,(x,y) in enumerate([(-3.45,-2.35),(-2.70,-2.54),(3.85,-.3),(3.72,-2.72)]):
 lathe('GlazedGardenVessel',[(0,.13),(.03,.18),(.21,.20),(.31,.16),(.32,.14),(.27,.14)],M['jade' if i%2 else 'paper'],16).location=(x,y,.18)
 ring('VesselNeckBand',.163,.47,.01,M['brass'],(x,y))
 for k in range(7):leaf((x,y,.47),.23+.08*R.random(),k*pi*2/7,M['green'])
 flower((x,y,.61),.11,M['coral'])
# Front garden clusters make the foreground feel inhabited, without a wall of particles.
for x,y in [(-3.70,-2.62),(-3.05,-2.72),(-2.3,-2.8),(3.78,-2.55),(3.65,.18)]:
 for k in range(4):
  c=(x+R.uniform(-.17,.17),y+R.uniform(-.12,.12),.22+R.uniform(0,.055))
  for angle in [0,2.1,4.2]:leaf(c,.17,angle,M['green'])
  flower((c[0],c[1],c[2]+.09),.08,M['paper' if k%2 else 'coral'])
# Guard rails and petal-stamped bridge endcaps retain the existing bridge silhouette.
for x in [2.06,3.65]:
 for y in [-1.70,-.90]:
  sphere('BridgeFinial',(x,y,.68),(.05,.05,.073),M['jade'],10,5)
  cylinder('BridgeBrassRing',(x,y,.62),.049,.014,M['brass'],10)
# Layered distant facades: muted silhouettes + sparse tiny warm windows, opaque and merged.
for i in range(8):
 x=-3.65+i*.88;h=.45+.18*(i%3)
 box('FarCityLayer',(x,3.72,.15+h/2),(.72,.15,h),M['sky'],.01)
 for k in range(2):box('WarmCityWindow',(x-.15+k*.3,3.625,.30+h*.3),(.05,.015,.07),M['paper'],0)
join('HanokV04NarrativeStatic',[o for o in bpy.context.scene.objects if o.type=='MESH'])
# Fuller asymmetrical plum canopy: three independently animated, material-merged clusters.
for i,center in enumerate([(-3.5,-1.16,1.90),(-2.75,-1.23,2.04),(-3.15,-.78,2.35)]):
 pivot=empty('V04PlumCrown'+str(i),center);parts=[]
 for j in range(14):
  a=j*2.4;r=.13+.34*R.random();c=(r*cos(a),r*sin(a)*.72,R.uniform(-.10,.13))
  before=set(bpy.context.scene.objects);flower(c,.13+R.random()*.05,M['paper' if j%3 else 'coral'],pivot)
  if j%2:leaf((c[0],c[1],c[2]-.06),.24,a,M['green'],pivot)
  parts.extend(o for o in bpy.context.scene.objects if o not in before and o.type=='MESH')
 crown=join('PlumCrown'+str(i),parts);crown.parent=pivot
 animation(pivot,'CanopyWind',[(f,{'rotation_euler':(.045*sin((f-1)/120*2*pi+i),.025*cos((f-1)/120*2*pi+i),.018*sin((f-1)/120*2*pi+i*.5))}) for f in range(1,122,15)])
for m in bpy.data.materials:m.use_backface_culling=False
src=ROOT/'assets/v0.4/source-blend/hanok-living.blend';dst=ROOT/'exports/v0.4/models/hanok-living.glb'
src.parent.mkdir(parents=True,exist_ok=True);dst.parent.mkdir(parents=True,exist_ok=True)
bpy.context.scene.frame_set(1);bpy.context.scene.frame_end=121
bpy.ops.wm.save_as_mainfile(filepath=str(src))
bpy.ops.export_scene.gltf(filepath=str(dst),export_format='GLB',export_yup=True,export_animations=True,export_animation_mode='NLA_TRACKS',export_nla_strips=True,export_force_sampling=True,export_cameras=False,export_lights=False)
print('V04_HANOK_SAVED',dst.stat().st_size)
