"""Versioned, four-sided Hanok. Gate B neutral structure first; never rewrites old art.

Authoring functions accept runtime Y-up metres, converted explicitly into Blender Z-up.
Run: blender -b --factory-startup --python Studio/modeling/hanok-v05.py -- --graybox
"""
import sys, json, math
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import reset, material, box, cylinder, path, mesh, empty, join, bpy

ROOT=Path(__file__).resolve().parents[2]
GRAY='--graybox' in sys.argv
TAG='graybox' if GRAY else 'reforge'
reset()
M={k:material('V05_'+k,c,r,m) for k,c,r,m in [
 ('wood','8A6249',.75,0),('lightwood','BE9870',.75,0),('paper','EEE4CD',.95,0),
 ('stone','C1BCAB',.9,0),('ink','293C55',.68,0),('jade','72BEAC',.31,.05),
 ('brass','B59B64',.42,.5),('coral','CC776C',.83,0),('earth','698572',.95,0)]}
if GRAY:
 for k,m in M.items():
  v=.18 if k=='ink' else .28 if k=='wood' else .57 if k=='paper' else .42 if k=='stone' else .40
  p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(v,v,v,1)
  p.inputs['Metallic'].default_value=0
modules=[];colliders=[];connections=[]
def xyz(p):return (p[0],-p[2],p[1])
def bounds(o):
 bpy.context.view_layer.update()
 pts=[o.matrix_world@Vector(c) for c in o.bound_box]
 return {'min':[min(p.x for p in pts),min(p.z for p in pts),min(-p.y for p in pts)],'max':[max(p.x for p in pts),max(p.z for p in pts),max(-p.y for p in pts)]}
def register(o,category,collision=False):
 b=bounds(o);modules.append({'name':o.name,'category':category,**b})
 if collision:colliders.append({'id':o.name,**b})
 return o
def B(name,p,s,mat='wood',category='detail',collision=False,bevel=.018,parent=None):
 return register(box(name,xyz(p),(s[0],s[2],s[1]),M[mat],bevel,parent),category,collision)
def beam(name,a,b,r=.055,mat='wood',category='rafter'):
 return register(path(name,[xyz(a),xyz(b)],r,M[mat]),category)
def P(name,pts,r=.05,mat='wood',category='rafter'):
 return register(path(name,[xyz(p) for p in pts],r,M[mat]),category)
def C(name,p,r,h,mat='wood',category='column',collision=False):
 return register(cylinder(name,xyz(p),r,h,M[mat],12),category,collision)

# Ground and real floor levels; no legacy world meshes are loaded into this candidate.
B('CourtyardFoundation',(0,-.28,-.7),(12,.56,10),'stone','foundation',bevel=.12)
B('CourtyardGround',(0,-.035,-.7),(11.8,.07,9.8),'stone','ground',bevel=.05)
B('BuildingStoneFoundation',(0,.18,-2.075),(6.75,.36,4.85),'stone','foundation',bevel=.04)
B('FloorSubstructure',(0,.39,-2.075),(6.5,.12,4.75),'wood','floor')
for i in range(27):
 B('FloorPlank%02d'%i,(-3.2+(i+.5)*6.4/27,.45,-2.075),(6.4/27-.008,.055,4.75),'lightwood','floor',bevel=.004)
for i in range(3):
 h=.15*(3-i)
 B('EntryStep'+str(i),(0,h/2,.25+.32*(i+.5)),(1.28,h,.32),'stone','stair',bevel=.015)

XS=[-3.2,-1.1,1.1,3.2];ZS=[-4.4,-2.5,-.6,.25]
def roof_h(z):
 t=abs(z+2.5)/(2.45 if z<-2.5 else 3.30)
 return 3.08+1.07*(1-t)**1.25+.11*t**8
for x in XS:
 for z in ZS:
  shoe=C(f'StoneShoe_{x}_{z}',(x,.51,z),.19,.13,'stone','foundation')
  post=C(f'Column_{x}_{z}',(x,1.66,z),.095,2.30,'wood','column',True)
  connections.append({'supported':post.name,'support':shoe.name,'type':'column-foot','tolerance_m':.02})
for z in ZS:
 b=B(f'Crossbeam_{z}',(0,2.77,z),(6.62,.24,.20),'wood','beam')
 for x in XS:
  connections.append({'supported':b.name,'support':f'Column_{x}_{z}','type':'beam-seat','tolerance_m':.02})
  B('BracketSeat',(x,2.88,z),(.40,.10,.29),'lightwood','bracket')
  top=roof_h(z)-.235
  strut=B(f'RoofStrut_{x}_{z}',(x,(top+2.89)/2,z),(.14,top-2.89,.14),'wood','strut',bevel=.01)
  connections.append({'supported':strut.name,'support':b.name,'type':'strut-seat','tolerance_m':.02})
 p=P(f'Purlin_{z}',[(-3.70,top,z),(3.70,top,z)],.095,'wood','purlin')
 for x in XS:
  connections.append({'supported':p.name,'support':f'RoofStrut_{x}_{z}','type':'purlin-seat','tolerance_m':.02})
for x in XS:
 B('DepthTieBeam',(x,2.77,-2.075),(.20,.24,4.85),'wood','beam')
 # Ridge posts sit on the centre crossbeam, fully connected to ridge purlin.
rafter_count=29 if GRAY else 21
rafter_samples=18 if GRAY else 12
for i in range(rafter_count):
 x=-3.70+7.40*i/(rafter_count-1)
 for side,reach in [(-1,2.45),(1,3.30)]:
  pts=[(x,roof_h(-2.5+side*reach*j/rafter_samples)-.14,-2.5+side*reach*j/rafter_samples) for j in range(rafter_samples+1)]
  r=P('Rafter_%s_%02d'%(side,i),pts,.060,'lightwood','rafter')
  for z in ZS:
   if (z+2.5)*side>=0:
    connections.append({'supported':r.name,'support':f'Purlin_{z}','type':'rafter-crossing','tolerance_m':.02})
 # Complete solid roof; outer sheet and underside share the curved profile.
for side,reach in [(-1,2.45),(1,3.30)]:
 verts=[];nx,nt=20,18
 for layer in [0,1]:
  for j in range(nt+1):
   z=-2.5+side*reach*j/nt
   for i in range(nx+1):
    x=-3.85+7.70*i/nx;verts.append(xyz((x,roof_h(z)-layer*.08,z)))
 n=(nx+1)*(nt+1);faces=[]
 for j in range(nt):
  for i in range(nx):
   k=j*(nx+1)+i;faces.append((k,k+1,k+nx+2,k+nx+1));faces.append((n+k+nx+1,n+k+nx+2,n+k+1,n+k))
 for j in range(nt):
  for i in [0,nx]:
   k=j*(nx+1)+i;faces.append((k,k+nx+1,k+nx+1+n,k+n))
 for j in [0,nt]:
  for i in range(nx):
   k=j*(nx+1)+i;faces.append((k,k+n,k+n+1,k+1))
 o=mesh('SolidRoof_'+str(side),verts,faces,M['ink']);register(o,'roof')
 # Recalculate consistent outward normals on the actual closed shell.
 bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.normals_make_consistent(inside=False);bpy.ops.object.mode_set(mode='OBJECT');o.select_set(False)
 P('EaveFascia',[(-3.85,roof_h(-2.5+side*reach)-.07,-2.5+side*reach),(3.85,roof_h(-2.5+side*reach)-.07,-2.5+side*reach)],.08,'wood','eave')
P('RidgePurlin',[(-3.75,3.915,-2.5),(3.75,3.915,-2.5)],.095,'wood','purlin')
P('RidgeCap',[(-3.9,4.18,-2.5),(3.9,4.18,-2.5)],.085,'ink','roof')

def lattice(name,c,w,h,axis='front',sliding=None):
 x,y,z=c
 def piece(n,dx,dy,sx,sy,mat='wood'):
  return B(name+n,(x+dx if axis=='front' else x,y+dy,z if axis=='front' else z+dx),(sx,sy,.065) if axis=='front' else (.065,sy,sx),mat,'door' if sliding else 'window',parent=sliding,bevel=.005)
 piece('Hanji',0,0,w-.055,h-.055,'paper')
 for dx in [-w/2,w/2]:piece('Stile',dx,0,.045,h+.04)
 for dy in [-h/2,h/2]:piece('Rail',0,dy,w+.04,.045)
 for i in range(1,7):piece('LatticeV',-w/2+w*i/7,0,.014,h)
 for i in range(1,6):piece('LatticeH',0,-h/2+h*i/6,w,.014)

def windowwall(name,center,width,height=2.22,axis='front',opening=1.1):
 x,y,z=center;wy=1.66;wh=1.03;floor=.477;top=2.70
 def part(suffix,offsetY,sizeY,offsetW,sizeW):
  p=(x+offsetW,offsetY,z) if axis=='front' else (x,offsetY,z+offsetW)
  s=(sizeW,sizeY,.14) if axis=='front' else (.14,sizeY,sizeW)
  B(name+suffix,p,s,'paper','wall',True,bevel=.008)
 part('Below',(floor+wy-wh/2)/2,wy-wh/2-floor,0,width)
 part('Above',(wy+wh/2+top)/2,top-wy-wh/2,0,width)
 for side in [-1,1]:part('Pier', (floor+top)/2,top-floor,side*(opening/2+(width-opening)/4),(width-opening)/2)
 lattice(name+'Window',(x,wy,z),opening,wh,axis)
 B(name+'Sill',(x,wy-wh/2-.035,z),(opening+.15,.08,.22) if axis=='front' else (.22,.08,opening+.15),'wood','window')

# Real walls on all four sides. Framed openings are actual apertures in solid geometry.
for x in [-2.15,2.15]:windowwall('FrontBay',(x,0,-.6),2.10)
for x in [-2.15,0,2.15]:windowwall('RearBay',(x,0,-4.4),2.1 if x else 2.2)
for x in [-3.2,3.2]:
 for z in [-3.45,-1.55]:windowwall('SideBay',(x,0,z),1.9,axis='side',opening=.95)
 # Closed gables extend from wall plate to the actual roof underside.
 pts=[(x,2.70,-4.4),(x,2.70,-.6)]+[(x,roof_h(-.6-3.8*i/16)-.08,-.6-3.8*i/16) for i in range(17)]
 verts=[xyz((a+offset,b,c)) for offset in [-.06,.06] for a,b,c in pts];n=len(pts)
 faces=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 register(mesh('SolidGable',verts,faces,M['paper']),'gable')
for side in [-1,1]:
 B('EntryDoorPier',(side*.825,1.59,-.6),(.55,2.22,.14),'paper','wall',True)
B('EntryDoorHeader',(0,2.61,-.6),(1.1,.18,.18),'wood','wall')
B('Threshold',(0,.49,-.6),(1.16,.035,.20),'wood','floor')
door_objects=[]
for side,name in [(-1,'DoorLeft'),(1,'DoorRight')]:
 before=set(bpy.context.scene.objects)
 lattice(name,(side*.275,1.49,-.53),.55,1.98)
 if not GRAY:B(name+'Handle',(side*.15,1.35,-.475),(.035,.14,.025),'brass','detail')
 for o in list(bpy.context.scene.objects):
  if o not in before:o.select_set(False)
 panel=join(name,[o for o in bpy.context.scene.objects if o not in before and o.type=='MESH'])
 # Shared panel-local origin at world zero; runtime slides ±.56m along X.
 bpy.context.scene.cursor.location=(0,0,0);bpy.context.view_layer.objects.active=panel;bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
 door_objects.append(panel)
 if GRAY:B(name+'Handle',(side*.15,1.35,-.475),(.035,.14,.025),'brass','detail')
# Interior room partitions have actual apertures facing the maru.
for x in [-1.1,1.1]:
 for z,length in [(-3.325,2.15),(-.825,.45)]:B('RoomPartition',(x,1.59,z),(.12,2.22,length),'paper','wall',True)
 B('InteriorDoorLintel',(x,2.57,-1.70),(.14,.26,1.10),'wood','wall')
 # Small lintel gap and opening bounded coherently by the two real partition pieces.
for x in [-2.15,2.15]:
 B('LowWritingDesk',(x,.77,-3.35),(.95,.09,.52),'wood','furniture',True)
 for dx in [-.38,.38]:B('DeskLeg',(x+dx,.62,-3.35),(.07,.30,.39),'wood','furniture')
 B('FloorCushion',(x,.54,-2.6),(.52,.12,.48),'jade','furniture',False,bevel=.05)
 B('PaperBook',(x,.84,-3.35),(.30,.045,.23),'paper','furniture',False,bevel=.008)

art={'keep':[],'hide_meshes':[]}
if not GRAY:
 from hanok_art_v05 import build_art
 art=build_art(globals())
 # MikkTSpace cannot calculate tangents on mixed/ngon curve caps. Triangulate
 # the editable art meshes explicitly; glTF already requires triangles.
 for o in list(bpy.context.scene.objects):
  if o.type=='MESH':
   bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
   mod=o.modifiers.new('PortableTangentTriangulation','TRIANGULATE');mod.keep_custom_normals=True;bpy.ops.object.modifier_apply(modifier=mod.name)
# Keep source modules editable and manifest derived from their actual world bounds.
src=ROOT/f'assets/v0.5/source-blend/hanok-{TAG}.blend';dst=ROOT/f'exports/v0.5/models/hanok-{TAG}.glb'
src.parent.mkdir(parents=True,exist_ok=True);dst.parent.mkdir(parents=True,exist_ok=True)
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.frame_set(1)
if not GRAY:scene.frame_end=121
bpy.ops.wm.save_as_mainfile(filepath=str(src))
# Merge static render geometry per material; keep real sliding doors independent.
def kept(o):
 while o:
  if o in art['keep']:return True
  o=o.parent
 return False
static=[o for o in scene.objects if o.type=='MESH' and o not in door_objects and o not in art['hide_meshes'] and not kept(o)]
join('HanokStaticStructure',static)
for o in art['hide_meshes']:bpy.data.objects.remove(o,do_unlink=True)
bpy.ops.export_scene.gltf(filepath=str(dst),export_format='GLB',export_yup=True,export_animations=not GRAY,export_animation_mode='NLA_TRACKS',export_nla_strips=True,export_force_sampling=True,export_tangents=not GRAY,export_cameras=False,export_lights=False)
manifest={'version':'0.5.0','stage':'Gate B graybox' if GRAY else 'Gate D art','coordinate_system':'runtime Y-up metres, front +Z','source':str(src.relative_to(ROOT)),'glb':str(dst.relative_to(ROOT)),'bounds_contract':{'courtyard':[-6,6,-5.7,4.3],'building':[-3.2,3.2,-4.4,-.6],'floor_y':.4775,'person_height':1.45,'door_width':1.10},'modules':modules,'support_connections':connections,'colliders':colliders,'sliding_doors':{'nodes':['DoorLeft','DoorRight'],'travel_m':.56,'opening':{'min':[-.55,.477,-.67],'max':[.55,2.48,-.46]}},'provenance':'original-project-owned procedural geometry','limitations':'Not a certified historical/engineering reconstruction. Connection bounds require actual render inspection.'}
(ROOT/f'exports/v0.5/hanok-{TAG}-structure.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('V05_HANOK',TAG,'modules',len(modules),'connections',len(connections),'bytes',dst.stat().st_size)
