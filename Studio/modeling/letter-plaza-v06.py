"""Approved T1: one complete Hanok and compact open Letter Plaza.
Original modular rounded geometry, palette materials, no external textures/assets.
Authoring API accepts runtime Y-up metres; Blender is Z-up. Prior outputs untouched.
"""
import bpy,sys,json,math,random
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import reset,material,box,cylinder,sphere,path,mesh,empty,join,animation
ROOT=Path(__file__).resolve().parents[2];reset();rng=random.Random(606)
M={k:material('Town_'+k,c,r,0) for k,c,r in [('paper','FFF0D8',.92),('stone','F1DCBA',.92),('paver','F9E8CC',.90),('wood','E9BB69',.80),('navy','3C5673',.73),('mint','88C9B3',.57),('coral','F18478',.85),('green','94C698',.86),('deepgreen','6FA989',.88),('glow','FFE8B5',.85),('soil','A19A76',.95)]}
p=M['glow'].node_tree.nodes.get('Principled BSDF');p.inputs['Emission Color'].default_value=(1,.67,.3,1);p.inputs['Emission Strength'].default_value=.45
def xyz(p):return (p[0],-p[2],p[1])
modules=[];colliders=[];supports=[];static=[]
def bounds(o):
 bpy.context.view_layer.update();pts=[o.matrix_world@Vector(v) for v in o.bound_box];return {'min':[min(v.x for v in pts),min(v.z for v in pts),min(-v.y for v in pts)],'max':[max(v.x for v in pts),max(v.z for v in pts),max(-v.y for v in pts)]}
def reg(o,kind,collision=False,moving=False):
 b=bounds(o);modules.append({'name':o.name,'kind':kind,**b})
 if collision:colliders.append({'id':o.name,**b})
 if not moving:static.append(o)
 return o
def B(n,p,s,m='wood',kind='detail',collision=False,moving=False,bevel=.02):return reg(box(n,xyz(p),(s[0],s[2],s[1]),M[m],bevel),kind,collision,moving)
def C(n,p,r,h,m='wood',kind='post',collision=False):return reg(cylinder(n,xyz(p),r,h,M[m],12),'post',collision)
def P(n,pts,r,m='wood',kind='beam'):return reg(path(n,[xyz(p) for p in pts],r,M[m]),kind)
def parent(o,e):w=o.matrix_world.copy();o.parent=e;o.matrix_world=w
B('PlazaPlinth',(0,-.20,-.45),(10.4,.40,8.5),'stone','ground',bevel=.14)
B('OpenSquare',(0,-.022,-.45),(10.15,.044,8.25),'paver','ground',bevel=.08)
# Broad, sparse crafted paving; four gentle rows keep the central play route clear.
for j in range(5):
 for i in range(8):
  x=-4.45+i*1.27+(j%2)*.10;z=-3.6+j*1.55
  B('BroadPaver',(x,.007,z),(1.22,.018,1.49),'paper' if (i+j)%6==0 else 'paver','ground',bevel=.035)
# Foundation -> continuous floor -> shoes -> columns -> beams -> purlins -> solid roof.
B('HouseFoundation',(-1.2,.12,-2.2),(4.85,.24,3.45),'stone','foundation')
floor=B('HouseContinuousFloor',(-1.2,.27,-2.15),(4.7,.06,3.30),'wood','floor')
for i in range(8):B('PorchPlank',(-3.35+i*.61,.308,-.83),(.60,.016,.65),'wood','floor',bevel=.006)
for i,(z,h) in enumerate([(-.33,.3),(-.03,.2),(.27,.1)]):B('EntryStep'+str(i),(-1.2,h/2,z),(1.5,h,.3),'paper','step',bevel=.018)
posts={}
for x in [-3.5,-1.2,1.1]:
 for z in [-3.8,-1.2,-.50]:
  if x==-1.2 and z!=-3.8:continue # Clear entrance; crossbeam spans the outer columns.
  shoe=C('StoneShoe',(x,.35,z),.13,.10,'stone');post=C('TimberColumn',(x,1.16,z),.073,1.62,'wood',collision=True);posts[x,z]=post
  supports.append({'supported':post.name,'support':shoe.name,'tolerance':.02})
for z in [-3.8,-1.2,-.50]:
 beam=B('CrossBeam',(-1.2,1.98,z),(4.87,.20,.18),'wood','beam')
 for x in [-3.5,-1.2,1.1]:
  if (x,z) in posts:supports.append({'supported':beam.name,'support':posts[x,z].name,'tolerance':.02})
  B('JoinerySeat',(x,2.07,z),(.28,.10,.25),'wood','joinery')
for x in [-3.5,1.1]:B('DepthBeam',(x,1.98,-2.15),(.18,.20,3.45),'wood','beam')
# Complete rear/side walls; windows have real frames and recessed paper panels.
B('RearWall',(-1.2,1.15,-3.8),(4.55,1.70,.13),'paper','wall',True)
for x in [-3.5,1.1]:B('SideWall',(x,1.15,-2.5),(.13,1.70,2.60),'paper','wall',True)
for x in [-2.625,.225]:B('FrontWallSection',(x,1.15,-1.2),(1.70,1.70,.13),'paper','wall',True)
B('DoorHeader',(-1.2,1.91,-1.2),(1.05,.18,.16),'wood','wall')
def window(n,c,w,h,side=False,out=1):
 x,y,z=c
 B(n+'Recess',(x,y,z),(.04,h,w) if side else (w,h,.04),'paper','window')
 for dx in [-w/2,w/2]:B(n+'Frame',(x+out*.025 if side else x+dx,y,z+dx if side else z+out*.025),(.06,h+.08,.06),'wood','window')
 for dy in [-h/2,h/2]:B(n+'Frame',(x+out*.025,y+dy,z+out*.025),(.07,.055,w+.08) if side else (w+.08,.055,.07),'wood','window')
 for i in range(1,5):
  d=-w/2+w*i/5;B(n+'Lattice',(x+out*.035 if side else x+d,y,z+d if side else z+out*.035),(.025,h,.025),'wood','window',bevel=.003)
 for dy in [-h*.20,h*.20]:B(n+'Lattice',(x+out*.04,y+dy,z+out*.04),(.025,.025,w) if side else (w,.025,.025),'wood','window',bevel=.003)
for x in [-2.625,.225]:window('FrontWindow',(x,1.25,-1.105),1.14,.96)
window('RightWindow',(1.19,1.25,-2.5),1.30,.95,True);window('LeftWindow',(-3.59,1.25,-2.5),1.30,.95,True,-1);window('RearWindow',(-1.2,1.25,-3.89),1.5,.9,False,-1)
for side,n in [(-1,'DoorLeft'),(1,'DoorRight')]:
 e=empty(n,xyz((-1.2+side*.225,1.10,-1.13)));b=B(n+'Panel',(-1.2+side*.225,1.10,-1.13),(.45,1.60,.065),'coral','door',moving=True);parent(b,e)
 for offset in [-.19,.19]:
  b=B(n+'Rail',(-1.2+side*.225+offset,1.10,-1.085),(.035,1.60,.045),'wood','door',moving=True,bevel=.007);parent(b,e)
 b=B(n+'Grip',(-1.2+side*.085,1.08,-1.07),(.028,.13,.035),'navy','door',moving=True,bevel=.008);parent(b,e)
 # Merge each moving leaf by material, retain named group and closed base translation.
 for mat in ['wood','coral','navy']:
  objs=[o for o in list(e.children) if o.type=='MESH' and o.data.materials[0]==M[mat]]
  if len(objs)>1:join(n+'_'+mat,objs)
def roofh(z):
 t=abs(z+2.35)/(1.85 if z< -2.35 else 2.18)
 return 2.09+.67*(1-t)**1.3+.11*t**7
# Purlins have actual support struts, not floating ornament.
for z in [-3.8,-2.35,-.50]:
 if z==-2.35:base=B('CentralTie',(-1.2,1.98,z),(4.87,.2,.18),'wood','beam')
 for x in [-3.5,-1.2,1.1]:
  bottom=2.08;top=roofh(z)-.06;st=B('RoofStrut',(x,(bottom+top)/2,z),(.10,top-bottom,.10),'wood','support');supports.append({'supported':st.name,'support':base.name if z==-2.35 else next(m['name'] for m in modules if m['kind']=='beam' and abs((m['min'][2]+m['max'][2])/2-z)<.02),'tolerance':.02})
 P('Purlin',[(-3.88,roofh(z)-.10,z),(1.48,roofh(z)-.10,z)],.065,'wood','purlin')
for x in [-3.98,1.58]:
 for side,reach in [(-1,1.85),(1,2.18)]:P('EaveFascia',[(x,roofh(-2.35+side*reach*j/12)-.04,-2.35+side*reach*j/12) for j in range(13)],.070,'mint','roof-trim')
for side,reach in [(-1,1.85),(1,2.18)]:
 verts=[];faces=[];steps=14
 for layer in [0,1]:
  for i in range(2):
   for j in range(steps+1):z=-2.35+side*reach*j/steps;verts.append((-3.98+i*5.56,roofh(z)-layer*.075,z))
 n=steps+1
 for j in range(steps):
  faces.extend([(j,j+1,n+j+1,n+j),(2*n+j,3*n+j,3*n+j+1,2*n+j+1)])
 for j in range(steps):faces.extend([(j,2*n+j,2*n+j+1,j+1),(n+j,n+j+1,3*n+j+1,3*n+j)])
 faces.extend([(0,n,3*n,2*n),(n-1,3*n-1,4*n-1,2*n-1)])
 reg(mesh('SolidRoof',[xyz(v) for v in verts],faces,M['navy'],smooth=True),'roof')
 # Broad curved ribs, not thousands of separate tiny tiles.
 for i in range(19):
  x=-3.9+i*.30;P('RoofRoll',[(x,roofh(-2.35+side*reach*j/12)+.025,-2.35+side*reach*j/12) for j in range(13)],.043,'navy','roof')
for x in [-3.53,1.13]:
 reg(mesh('ClosedGable',[xyz((x+d,y,z)) for d in [-.04,.04] for y,z in [(2.05,-3.8),(2.05,-.5),(2.72,-2.35)]],[(0,2,1),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],M['paper']),'gable')
P('RoofRidge',[(-4.04,2.79,-2.35),(-1.2,2.80,-2.35),(1.64,2.79,-2.35)],.083,'navy','roof')
# Rounded planting modules, asymmetry kept at plaza edge, never on the run route.
for x,z,w,d in [(-4.15,-1.2,1.25,3.5),(3.65,-2.7,1.6,2.2),(-3.85,2.7,1.8,1.0),(3.55,2.7,1.7,.8)]:
 B('GardenBed',(x,.07,z),(w,.14,d),'stone','garden',True,bevel=.12);B('Soil',(x,.145,z),(w-.1,.025,d-.1),'deepgreen','garden',bevel=.10)
 for i in range(8):
  xx=x+rng.uniform(-w*.38,w*.38);zz=z+rng.uniform(-d*.36,d*.36)
  stem=C('FlowerStem',(xx,.24,zz),.012,.20,'green')
  for j in range(5):
   a=j*math.tau/5;o=sphere('Petal',xyz((xx+.045*math.cos(a),.34,zz+.045*math.sin(a))),(.035,.035,.020),M['coral'] if i%3 else M['wood'],8,4);reg(o,'flower')
  reg(sphere('FlowerHeart',xyz((xx,.345,zz)),(.022,.022,.018),M['paper'],8,4),'flower')
for i,(x,z) in enumerate([(-4.1,-1.7),(3.65,-3.1),(-4.0,2.8)]):
 C('TreeTrunk',(x,.80,z),.075,1.38,'wood',collision=True)
 e=empty('TreeWind'+str(i),xyz((x,1.35,z)))
 for j,(dx,dy,dz,s) in enumerate([(-.34,1.65,.04,.48),(.23,1.82,-.09,.52),(.03,2.12,.08,.47)]):
  bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=s,location=xyz((x+dx,dy,z+dz)));o=bpy.context.object;o.name='RoundedCrown';o.scale=(1,1,.90);o.data.materials.append(M['green'] if j%2 else M['mint'])
  for f in o.data.polygons:f.use_smooth=True
  reg(o,'foliage',moving=True);parent(o,e)
 animation(e,'GardenWind',[(1,{'rotation_euler':(0,-.025,0)}),(61,{'rotation_euler':(0,.025,0)}),(121,{'rotation_euler':(0,-.025,0)})])
for i,(x,z) in enumerate([(-3.25,1.7),(3.1,2.7)]):
 for dx in [-.50,.50]:B('BenchLeg',(x+dx,.18,z),(.09,.36,.32),'navy','bench',True)
 for k in range(3):B('BenchSlat',(x,.39,z+(k-1)*.105),(1.38,.10,.095),'wood','bench',True,bevel=.025)
for i,(x,z) in enumerate([(-3.65,.6),(2.45,-.35)]):
 C('LanternFoot',(x,.06,z),.17,.12,'stone');C('LanternPost',(x,.82,z),.042,1.55,'navy',collision=True)
 B('LanternBracket',(x+.13,1.72,z),(.30,.055,.055),'navy','lamp')
 e=empty('InteractiveLantern'+str(i),xyz((x+.23,1.73,z)))
 for n,p,s,m in [('LanternCore',(x+.23,1.50,z),(.22,.30,.22),'glow'),('LanternCap',(x+.23,1.69,z),(.29,.065,.29),'navy'),('LanternBase',(x+.23,1.31,z),(.27,.055,.27),'navy')]:o=B(n,p,s,m,'lamp',moving=True,bevel=.025);parent(o,e)
 animation(e,'LanternBreeze',[(1,{'rotation_euler':(.025,0,0)}),(46,{'rotation_euler':(-.025,0,0)}),(91,{'rotation_euler':(.025,0,0)})])
# Mint mailbox, envelope icon; safe low platform adds readable jump destination.
B('MailboxBase',(2.70,.29,.48),(.52,.58,.40),'mint','prop',True,bevel=.15);B('MailboxTop',(2.70,.64,.48),(.54,.20,.42),'mint','prop',True,bevel=.10)
B('MailSlot',(2.70,.60,.705),(.29,.035,.018),'navy','prop',bevel=.01)
P('EnvelopeIcon',[(2.55,.47,.701),(2.70,.36,.701),(2.85,.47,.701)],.011,'paper','prop')
B('SafeStepPlatform',(3.1,.08,1.35),(1.35,.16,.90),'wood','platform',True,bevel=.09)
for x,z in [(-2.15,2.45),(1.05,1.3),(3.6,2.0)]:
 reg(mesh('FoldedPaver',[xyz((x-.20,.035,z-.15)),xyz((x+.21,.035,z-.13)),xyz((x+.18,.035,z+.18)),xyz((x,.065,z))],[(0,1,3),(1,2,3),(2,0,3)],M['mint']),'ground')
for i in range(5):B('PorchSteppingStone',(-1.2+rng.uniform(-.1,.1),.028,.65+i*.39),(.54,.05,.30),'paper','ground',bevel=.08)
# Source semantic records saved before merging; renderer only pays shared material groups.
data={'units':'metres/Y-up','modules':modules,'supports':supports,'colliders':colliders,'bounds':{'x':[-4.85,4.85],'z':[-4.35,3.5]},'floors':[{'min':[-3.55,-3.85],'max':[1.15,-.48],'height':.316},{'min':[-1.95,-.48],'max':[-.45,-.18],'height':.30},{'min':[-1.95,-.18],'max':[-.45,.12],'height':.20},{'min':[-1.95,.12],'max':[-.45,.42],'height':.10},{'min':[2.425,.90],'max':[3.775,1.80],'height':.16}],'door':{'center':[-1.2,-1.13],'min':[-1.65,.30,-1.23],'max':[-.75,1.9,-1.03],'travel':.45},'spawn':[.45,0,1.60]}
groups={mat:[o for o in static if len(o.data.materials)==1 and o.data.materials[0]==mat] for mat in M.values()}
for mat,objs in groups.items():
 if objs:join('Static_'+mat.name,objs)
src=ROOT/'assets/v0.6/source-blend/letter-plaza.blend';dst=ROOT/'exports/v0.6/models/letter-plaza.glb';scene=bpy.context.scene;scene.frame_set(1);scene.frame_end=121
src.parent.mkdir(parents=True,exist_ok=True);dst.parent.mkdir(parents=True,exist_ok=True);bpy.ops.wm.save_as_mainfile(filepath=str(src));bpy.ops.export_scene.gltf(filepath=str(dst),export_format='GLB',export_yup=True,export_animations=True,export_animation_mode='NLA_TRACKS',export_nla_strips=True,export_force_sampling=True,export_cameras=False,export_lights=False)
(ROOT/'exports/v0.6/plaza-structure.json').write_text(json.dumps(data,indent=2)+'\n');runtime={k:v for k,v in data.items() if k not in ['modules','supports']};(ROOT/'exports/v0.6/collision-world.json').write_text(json.dumps(runtime,indent=2)+'\n');print('PLAZA_SAVED',dst.stat().st_size,len(modules),'modules',len(supports),'support connections')
