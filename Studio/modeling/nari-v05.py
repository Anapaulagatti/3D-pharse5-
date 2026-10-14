"""Original Nari, approved concept A: continuous skinned body, real armature,
facial morphs and twenty authored bone performances. No legacy source modified.
Blender Z-up, character faces -Y; glTF is Y-up, front +Z. Units: metres.
"""
import bpy, math, sys, json
from pathlib import Path
from math import sin,cos,pi,acos,atan2,sqrt,exp
from mathutils import Vector,Quaternion,Euler
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import reset,material,box,sphere,path,mesh,join,color
ROOT=Path(__file__).resolve().parents[2]
ART='--art' in sys.argv
reset()
COL={'skin':'E4AD89','ivory':'F2E8D4','jade':'72B9A3','navy':'25384A','hair':'362820','coral':'D67F6C','brass':'C5A66D','white':'FFF6E7','eye':'442D21','pupil':'152335','cheek':'DA8E78'}
M={k:material('Nari_'+k,'FFFFFF',r,m) for k,r,m in [('skin',.50,0),('cloth',.85,0),('dark',.48,0),('accent',.34,.35)]}
for m in M.values():
 n=m.node_tree.nodes.new('ShaderNodeVertexColor');n.layer_name='Color';m.node_tree.links.new(n.outputs['Color'],m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'])
def paint(o,c,mat='cloth'):
 o.data.materials.clear();o.data.materials.append(M[mat]);rgba=color(COL.get(c,c));a=o.data.color_attributes.new(name='Color',type='FLOAT_COLOR',domain='CORNER')
 for d in a.data:d.color=rgba
 return o
def apply_world(o):
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
def S(name,p,s,c='skin',mat='skin',seg=20,rings=12):return paint(sphere(name,p,s,None,seg,rings),c,mat)
def B(name,p,s,c='ivory',mat='cloth',bevel=.008):return paint(box(name,p,s,None,bevel),c,mat)
def P(name,points,r,c='ivory',mat='cloth'):return paint(path(name,points,r,None),c,mat)
def capsule(name,a,b,r,depth=None):
 a,b=Vector(a),Vector(b);o=sphere(name,(a+b)/2,(r,depth or r,(b-a).length/2+r*.6),None,16,10);o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return o

# Build and voxel-union actual continuous anatomy. Sleeves/pants are material regions,
# with independent overlapping garment layers only where naturally appropriate.
parts=[sphere('Torso',(0,0,.865),(.155,.09,.19),None,24,16),sphere('Pelvis',(0,0,.675),(.15,.10,.105),None,24,12),sphere('Head',(0,0,1.23),(.165,.145,.20),None,32,20),capsule('Neck',(0,0,1.00),(0,0,1.10),.047)]
for side in [-1,1]:
 parts += [sphere('Ear',(side*.16,.006,1.235),(.024,.029,.047),None,16,10),capsule('Thigh',(side*.095,0,.67),(side*.108,0,.37),.082,.075),capsule('Shin',(side*.108,0,.37),(side*.115,0,.075),.052,.048),sphere('Foot',(side*.115,-.06,.052),(.064,.115,.051),None,20,12),capsule('UpperArm',(side*.165,0,.985),(side*.295,0,.795),.050,.048),capsule('Forearm',(side*.295,0,.795),(side*.35,0,.63),.041,.038),sphere('Hand',(side*.357,-.005,.591),(.037,.025,.049),None,16,10)]
 for i in range(4):
  x=side*(.334+i*.014);z=.541+(abs(i-1.3))*.007
  parts.append(capsule('Finger',(x,-.006,.57),(x,-.009,z),.0095,.009))
 parts.append(capsule('Thumb',(side*.333,-.003,.605),(side*.313,-.022,.575),.013,.012))
body=join('NariContinuousBody',parts);apply_world(body)
mod=body.modifiers.new('ContinuousAnatomyUnion','REMESH');mod.mode='VOXEL';mod.voxel_size=.009;mod.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=mod.name)
mod=body.modifiers.new('JointSurfaceRelax','SMOOTH');mod.factor=.65;mod.iterations=4;bpy.ops.object.modifier_apply(modifier=mod.name)
mod=body.modifiers.new('RealtimeTopology','DECIMATE');mod.ratio=.33 if ART else .34;bpy.ops.object.modifier_apply(modifier=mod.name)
for v in body.data.vertices:
 p=v.co
 if p.z<.003:p.z=.003
 # Soft planar face for eyes/lips; keep natural side/rear volume.
 if p.z>1.10 and p.y<0:p.y*=.90
for f in body.data.polygons:f.use_smooth=True
body.data.materials.clear()
for k in ['skin','cloth','dark']:body.data.materials.append(M[k])
attr=body.data.color_attributes.new(name='Color',type='FLOAT_COLOR',domain='CORNER')
for f in body.data.polygons:
 p=sum((body.data.vertices[i].co for i in f.vertices),Vector())/len(f.vertices)
 c,mat='ivory',1
 if p.z>1.025 or (abs(p.x)>.30 and p.z<.695):c,mat='skin',0
 elif p.z<.10:c,mat='navy',2
 elif p.z<.25:c,mat='ivory',1
 elif p.z<.72:c,mat='navy',1
 f.material_index=mat
 for i in f.loop_indices:
  # Vertex interpolation avoids saw-tooth polygon-centre color borders at cuffs.
  vp=body.data.vertices[body.data.loops[i].vertex_index].co
  vc=c
  if mat==1:
   if abs(vp.x)>.22:vc='ivory'
   elif vp.z<.25:vc='ivory'
   elif vp.z<.72:vc='navy'
   else:vc='ivory'
  attr.data[i].color=color(COL[vc])

# Rig: explicit bones, meaningful parents and deform groups, not node-pivot limbs.
arm=bpy.data.armatures.new('NariSkeleton');rig=bpy.data.objects.new('NariArmature',arm);bpy.context.collection.objects.link(rig);bpy.context.view_layer.objects.active=rig;rig.select_set(True);body.select_set(False);bpy.ops.object.mode_set(mode='EDIT')
REST={}
def headwarp(p):
 p=Vector(p)
 if p.z>1.075:
  blend=min(1,(p.z-1.075)/.06);p.x*=1-.10*blend;p.y*=1-.10*blend;p.z=1.075+(p.z-1.075)*.75
 return p
def bone(name,a,b,parent=None,connected=False):
 if name in ['Head','HairKnot','PaperPin']:a,b=headwarp(a),headwarp(b)
 o=arm.edit_bones.new(name);o.head=a;o.tail=b
 if parent:o.parent=arm.edit_bones[parent];o.use_connect=connected
 REST[name]=(Vector(a),Vector(b));return o
bone('Root',(0,0,0),(0,0,.10))
bone('Hips',(0,0,.67),(0,0,.76),'Root')
bone('Spine',(0,0,.76),(0,0,.89),'Hips',True)
bone('Chest',(0,0,.89),(0,0,1.015),'Spine',True)
bone('Neck',(0,0,1.015),(0,0,1.075),'Chest',True)
bone('Head',(0,0,1.075),(0,0,1.39),'Neck',True)
for side,suffix in [(1,'L'),(-1,'R')]:
 bone('Clavicle.'+suffix,(0,0,.985),(side*.165,0,.985),'Chest')
 bone('UpperArm.'+suffix,(side*.165,0,.985),(side*.295,0,.795),'Clavicle.'+suffix,True)
 bone('Forearm.'+suffix,(side*.295,0,.795),(side*.35,0,.63),'UpperArm.'+suffix,True)
 bone('Hand.'+suffix,(side*.35,0,.63),(side*.357,-.005,.55),'Forearm.'+suffix,True)
 bone('Fingers.'+suffix,(side*.357,-.005,.55),(side*.357,-.005,.525),'Hand.'+suffix,True)
 bone('Thigh.'+suffix,(side*.095,0,.67),(side*.108,0,.37),'Hips')
 bone('Shin.'+suffix,(side*.108,0,.37),(side*.115,0,.075),'Thigh.'+suffix,True)
 bone('Foot.'+suffix,(side*.115,0,.075),(side*.115,-.13,.045),'Shin.'+suffix,True)
 bone('Toe.'+suffix,(side*.115,-.13,.045),(side*.115,-.17,.045),'Foot.'+suffix,True)
bone('HairKnot',(-.09,.07,1.37),(-.09,.07,1.45),'Head')
bone('PaperPin',(-.10,.07,1.42),(-.16,.07,1.47),'HairKnot')
bone('LetterSatchel',(.21,-.01,.67),(.21,-.01,.57),'Hips')
bone('GoreumTie',(.035,-.12,.93),(.035,-.12,.81),'Chest')
bpy.ops.object.mode_set(mode='OBJECT');rig.show_in_front=True
for p in rig.pose.bones:p.rotation_mode='QUATERNION'
def distance(p,a,b):
 v=b-a;t=max(0,min(1,(p-a).dot(v)/v.length_squared));return (p-a-t*v).length
def weights(p):
 x,y,z=p;side='L' if x>=0 else 'R'
 if z>1.10:return [('Head',1)]
 if z>1.015:return [('Head',max(0,min(1,(z-1.015)/.085))),('Neck',1-max(0,min(1,(z-1.015)/.085)))]
 if (abs(x)>.235 and z>.515) or (abs(x)>.12 and z>.72):
  candidates=['Spine','Chest','Clavicle.'+side,'UpperArm.'+side,'Forearm.'+side,'Hand.'+side,'Fingers.'+side]
 elif z<.71:candidates=['Hips','Thigh.'+side,'Shin.'+side,'Foot.'+side,'Toe.'+side]
 else:candidates=['Hips','Spine','Chest','Neck']
 ds=sorted([(distance(p,*REST[n]),n) for n in candidates])[:4]
 vals=[(n,1/(d*d+.00018)**2) for d,n in ds];total=sum(w for n,w in vals)
 return [(n,w/total) for n,w in vals if w/total>.0001]
def skin(o,rigid=None,torso=False):
 apply_world(o)
 if o.data.shape_keys:
  for key in o.data.shape_keys.key_blocks:
   for v in key.data:v.co=headwarp(v.co)
  for i,v in enumerate(o.data.vertices):v.co=o.data.shape_keys.key_blocks['Basis'].data[i].co
 else:
  for v in o.data.vertices:v.co=headwarp(v.co)
 if ART:o.data.update()
 groups={n:o.vertex_groups.get(n) or o.vertex_groups.new(name=n) for n in REST}
 for v in o.data.vertices:
  ws=[(rigid,1)] if rigid else weights(v.co)
  if torso:
   ds=sorted([(distance(v.co,*REST[n]),n) for n in ['Hips','Spine','Chest','Neck']])[:3]
   ws=[(n,1/(d*d+.00018)**2) for d,n in ds]
  total=sum(w for n,w in ws)
  for n,w in ws:
   if w>0:groups[n].add([v.index],w/total,'REPLACE')
 m=o.modifiers.new('NariSkin','ARMATURE');m.object=rig;o.parent=rig
skin(body)
# Bone-heat diffusion on the connected anatomical surface prevents underarm skin
# from being captured by nearby forearm/hand segments. Props retain explicit weights.
for m in list(body.modifiers):
 if m.type=='ARMATURE':body.modifiers.remove(m)
body.parent=None;body.vertex_groups.clear()
excluded=['Root','Fingers.L','Fingers.R','HairKnot','PaperPin','LetterSatchel','GoreumTie']
for n in excluded:arm.bones[n].use_deform=False
bpy.ops.object.select_all(action='DESELECT');body.select_set(True);rig.select_set(True);bpy.context.view_layer.objects.active=rig
bpy.ops.object.parent_set(type='ARMATURE_AUTO')
bpy.context.view_layer.objects.active=body;rig.select_set(False)
bpy.ops.object.vertex_group_limit_total(limit=4);bpy.ops.object.vertex_group_normalize_all(lock_active=False)
for n in excluded:arm.bones[n].use_deform=True
garments=[]
# Fabric vest, actual curved silhouette and crossed collar; all deform with skeleton.
verts=[];faces=[];nr=28
for z,rx,ry in [(.71,.162,.107),(.82,.153,.108),(.94,.177,.102),(1.005,.148,.092)]:
 for i in range(nr):
  a=2*pi*i/nr;verts.append((rx*cos(a),ry*sin(a),z))
for j in range(3):
 for i in range(nr):
  a=(i+.5)/nr*2*pi
  # Front V opening widens toward neck; upper armholes remain open.
  if sin(a)<-.75 and j>=1:continue
  if j==2 and abs(cos(a))>.92:continue
  k=j*nr+i;faces.append((k,j*nr+(i+1)%nr,(j+1)*nr+(i+1)%nr,k+nr))
vest=paint(mesh('CeladonMessengerVest',verts,faces,None,smooth=True),'jade');mod=vest.modifiers.new('FabricThickness','SOLIDIFY');mod.thickness=.006;bpy.context.view_layer.objects.active=vest;bpy.ops.object.modifier_apply(modifier=mod.name);garments.append(vest)
garments += [P('CrossedCollarLeft',[(-.075,-.105,1.018),(-.018,-.121,.958),(.036,-.116,.91)],.014),P('CrossedCollarRight',[(.075,-.105,1.018),(.025,-.121,.970),(-.025,-.119,.935)],.013)]
# Flat paper satchel and secured strap; no oversized floating prop.
bagparts=[B('LetterSatchelBody',(.215,-.02,.648),(.155,.095,.18),'navy'),B('IvorySatchelFlap',(.215,-.073,.692),(.155,.014,.082),'ivory'),B('LetterCorner',(.207,-.015,.751),(.105,.018,.09),'ivory',bevel=.002),S('SatchelButton',(.215,-.086,.680),(.013,.007,.013),'brass','accent',12,6)]
bag=join('LetterSatchel',bagparts);skin(bag,'LetterSatchel')
garments += [P('SatchelStrap',[(-.13,-.09,1.00),(-.055,-.115,.92),(.055,-.115,.82),(.19,-.092,.72)],.010,'navy')]
tieparts=[S('GoreumKnot',(.035,-.128,.944),(.017,.009,.014),'coral','cloth',12,6)]
for side in [-1,1]:
 tieparts.append(P('GoreumLoop',[(.035,-.127,.944),(.035+side*.047,-.13,.954),(.035+side*.040,-.133,.925),(.035,-.127,.944)],.009,'coral'))
 tieparts.append(B('GoreumTail',(.035+side*.013,-.126,.884),(.019,.008,.10),'coral',bevel=.002))
tie=join('GoreumBow',tieparts);skin(tie,'GoreumTie')
for o in garments:skin(o,torso=True)
for side,suffix in [(1,'L'),(-1,'R')]:
 bpy.ops.mesh.primitive_torus_add(major_segments=20,minor_segments=8,major_radius=.039,minor_radius=.009,location=(side*.330,0,.690))
 cuff=paint(bpy.context.object,'ivory');cuff.name='RolledSleeveCuff'+suffix;cuff.rotation_euler=Vector((side*.055,0,-.165)).to_track_quat('Z','Y').to_euler();skin(cuff,'Forearm.'+suffix)
 bpy.ops.mesh.primitive_torus_add(major_segments=20,minor_segments=6,major_radius=.052,minor_radius=.008,location=(side*.110,0,.245))
 cuff=paint(bpy.context.object,'ivory');cuff.name='SockWrapCuff'+suffix;skin(cuff,'Shin.'+suffix)

# Sculpted dark hair cap with original asymmetric knot/paper pin.
verts=[];faces=[];n=32;rings=10
for j in range(rings+1):
 for i in range(n):
  a=2*pi*i/n;front=-sin(a);limit=1.20 if front>.15 else 1.78 if front>-.6 else 2.08
  theta=.035+(limit-.035)*j/rings
  verts.append((.173*sin(theta)*cos(a),.152*sin(theta)*sin(a),1.23+.208*cos(theta)))
for j in range(rings):
 for i in range(n):
  k=j*n+i;faces.append((k,j*n+(i+1)%n,(j+1)*n+(i+1)%n,k+n))
hair=paint(mesh('SweptHairCap',verts,faces,None,smooth=True),'hair','dark');skin(hair,'Head')
for side in [-1,1]:
 o=P('TempleHair',[(side*.135,-.061,1.356),(side*.166,-.063,1.304),(side*.163,-.045,1.232)],.021,'hair','dark');skin(o,'Head')
for i in range(4):
 o=P('SweptFringe',[(.095-i*.032,-.10,1.397),(.065-i*.035,-.139,1.358),(-.025-i*.025,-.143,1.315)],.014,'hair','dark');skin(o,'Head')
bpy.ops.mesh.primitive_torus_add(major_segments=24,minor_segments=8,major_radius=.047,minor_radius=.026,location=(-.085,.07,1.390),rotation=(pi/2,0,-.2));bun=paint(bpy.context.object,'hair','dark');bun.name='LowLoopedHairKnot';skin(bun,'HairKnot')
pin=paint(mesh('FoldedHanjiHairPin',[(-.11,.061,1.43),(-.19,.054,1.48),(-.175,.052,1.407),(-.14,.035,1.435),(-.12,.056,1.405)],[(0,1,3),(1,2,3),(2,4,3),(4,0,3)],None),'ivory');skin(pin,'PaperPin')

# Real facial mesh/morph controls. Every piece is skinned to Head, not billboard art.
faceparts=[]
def facepart(o,region):
 apply_world(o);g=o.vertex_groups.new(name=region);g.add(list(range(len(o.data.vertices))),1,'REPLACE');faceparts.append(o);return o
for side,suffix in [(-1,'L'),(1,'R')]:
 x=side*.062
 for name,p,s,c,mat in [
  ('EyeWhite',(x,-.124,1.255),(.035,.012,.021),'white','skin'),
  ('Iris',(x,-.137,1.255),(.014,.007,.018),'eye','dark'),
  ('Pupil',(x,-.143,1.255),(.007,.004,.012),'pupil','dark'),
  ('EyeLight',(x-.004,-.148,1.262),(.0045,.002,.005),'white','skin')]:facepart(S(name+suffix,p,s,c,mat,16,10),'RegionEye'+suffix)
 pts=[(x+.035*t,-.139+.006*t*t,1.255+.020*sqrt(max(0,1-t*t))) for t in [-1,-.66,-.33,0,.33,.66,1]]
 facepart(P('UpperLid'+suffix,pts,.0035,'hair','dark'),'RegionEye'+suffix)
 facepart(P('Brow'+suffix,[(x-.030,-.126,1.297),(x,-.131,1.305),(x+.030,-.126,1.297)],.0045,'hair','dark'),'RegionBrow'+suffix)
 facepart(S('Cheek'+suffix,(side*.103,-.118,1.213),(.025,.004,.010),'cheek','skin',14,8),'RegionCheek')
facepart(S('Nose',(0,-.132,1.217),(.019,.018,.025),'skin','skin',16,10),'RegionNose')
verts=[(0,-.131,1.168)]+[(.035*cos(i/28*2*pi),-.132,1.168+.006*sin(i/28*2*pi)) for i in range(28)]
facepart(paint(mesh('Mouth',verts,[(0,i+1,(i+1)%28+1) for i in range(28)],None),'pupil','dark'),'RegionMouth')
face=join('NariFacialControls',faceparts)
regions={g.name:{v.index for v in face.data.vertices if any(x.group==g.index and x.weight>.5 for x in v.groups)} for g in face.vertex_groups if g.name.startswith('Region')}
face.shape_key_add(name='Basis')
EXPRESSIONS=['Happy','Excited','Curious','Thinking','Confused','Sad','Surprised','Determined','Celebrating','Blink']
spec={
 'Happy':(.45,.45,.043,.019,.014,0), 'Excited':(1.08,1.08,.044,.032,.008,0),
 'Curious':(1.18,.88,.020,.012,0,.006),'Thinking':(.72,.86,.022,.004,-.002,.009),
 'Confused':(.80,1.12,.029,.005,-.007,-.009),'Sad':(.70,.70,.032,.004,-.021,0),
 'Surprised':(1.40,1.40,.025,.031,0,0),'Determined':(.64,.64,.031,.004,.002,0),
 'Celebrating':(.36,.36,.047,.032,.014,0),'Blink':(.05,.05,.035,.006,0,0)}
for mood in EXPRESSIONS:
 key=face.shape_key_add(name=mood);el,er,rx,rz,corner,offset=spec[mood]
 for side,suffix,factor in [(-1,'L',el),(1,'R',er)]:
  for i in regions['RegionEye'+suffix]:key.data[i].co.z=1.255+(face.data.vertices[i].co.z-1.255)*factor
  for i in regions['RegionBrow'+suffix]:
   p=face.data.vertices[i].co;tilt=(-side*.38 if mood=='Sad' else side*.32 if mood=='Determined' else .30 if mood in ['Thinking','Confused'] else 0)
   lift=.018 if mood in ['Surprised','Excited','Celebrating'] else .010 if mood in ['Happy','Curious'] else -.005 if mood=='Determined' else 0
   key.data[i].co.z=p.z+lift+tilt*(p.x-side*.062)
 for i in regions['RegionMouth']:
  p=face.data.vertices[i].co;xn=p.x/.035;zn=(p.z-1.168)/.006
  key.data[i].co.x=rx*xn+offset;key.data[i].co.z=1.168+rz*zn+corner*xn*xn
 # Static neutral reset is the Basis; Blink affects eyes only.
 if mood=='Blink':
  for i in regions['RegionMouth']|regions['RegionBrowL']|regions['RegionBrowR']:key.data[i].co=face.data.vertices[i].co

skin(face,'Head')
# Merge non-morph meshes while retaining the same normalized deform groups.
costume=join('NariSkinnedBodyAndCostume',[o for o in bpy.context.scene.objects if o.type=='MESH' and o!=face])
if ART:
 # Separate skin shading from cloth/hair without changing the continuous anatomy
 # or rig. This lets the stylized face avoid coarse received feature shadows.
 bpy.ops.object.select_all(action='DESELECT');costume.select_set(True);bpy.context.view_layer.objects.active=costume
 bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='DESELECT');bpy.ops.object.mode_set(mode='OBJECT')
 bpy.context.tool_settings.mesh_select_mode=(False,False,True)
 for f in costume.data.polygons:f.select=costume.data.materials[f.material_index]==M['skin']
 before=set(bpy.context.scene.objects)
 bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.separate(type='SELECTED');bpy.ops.object.mode_set(mode='OBJECT')
 skin_surface=next(o for o in bpy.context.scene.objects if o not in before);skin_surface.name='NariSkinSurface'
 from reforge_materials import textured,surface_uv
 textured(M['cloth'],'nari-wovencloth','cloth','FFFFFF',56,vertex_color=True)
 for o in bpy.context.scene.objects:
  if o.type=='MESH':surface_uv(o,4)

# Authored bone poses use world-axis intent, conjugated into each bone's rest basis.
def rot(name,rx=0,ry=0,rz=0):
 b=rig.data.bones[name].matrix_local.to_quaternion();q=Euler((rx,ry,rz),'XYZ').to_quaternion();rig.pose.bones[name].rotation_quaternion=b.conjugated()@q@b
def arm_ik(side,target,pole):
 suffix='L' if side>0 else 'R';names=['UpperArm.'+suffix,'Forearm.'+suffix,'Hand.'+suffix]
 s,e=REST[names[0]];_,w=REST[names[1]];target=Vector(target);pole=Vector(pole)
 l1=(e-s).length;l2=(w-e).length;d=min((target-s).length,l1+l2-.001);u=(target-s).normalized();v=pole-s-u*(pole-s).dot(u);v.normalize();a=(l1*l1-l2*l2+d*d)/(2*d);k=s+u*a+v*sqrt(max(0,l1*l1-a*a))
 q1=(e-s).rotation_difference(k-s);q2=(w-e).rotation_difference(target-k)
 b1=arm.bones[names[0]].matrix_local.to_quaternion();b2=arm.bones[names[1]].matrix_local.to_quaternion()
 rig.pose.bones[names[0]].rotation_quaternion=b1.conjugated()@q1@b1
 rig.pose.bones[names[1]].rotation_quaternion=b2.conjugated()@q1.conjugated()@q2@b2
def leg(side,foot_y,foot_z,root_z=0,tilt=0):
 suffix='L' if side>0 else 'R';l1=(REST['Thigh.'+suffix][1]-REST['Thigh.'+suffix][0]).length;l2=(REST['Shin.'+suffix][1]-REST['Shin.'+suffix][0]).length
 dz=.67+root_z-foot_z;d=min(sqrt(dz*dz+foot_y*foot_y),l1+l2-.001);theta=atan2(foot_y,dz);alpha=acos(max(-1,min(1,(l1*l1+d*d-l2*l2)/(2*l1*d))));knee=pi-acos(max(-1,min(1,(l1*l1+l2*l2-d*d)/(2*l1*l2))))
 thigh=theta-alpha;rot('Thigh.'+suffix,thigh);rot('Shin.'+suffix,knee);rot('Foot.'+suffix,-thigh-knee+tilt)

CLIPS={'Idle':3.2,'Walk':.9,'Run':.666667,'WalkStart':.3,'WalkStop':.3,'RunStart':.3,'RunStop':.366667,'JumpStart':.2,'JumpAir':.6,'JumpLand':.333333,'TurnLeft':.5,'TurnRight':.5,'Greeting':2.0,'Happy':1.8,'Thinking':2.4,'Sad':2.4,'Celebration':2.2,'Surprised':1.4,'Curious':2.2,'InteractionReaction':1.4}
EMOTION={'Idle':None,'Walk':'Curious','Run':'Determined','Greeting':'Happy','Happy':'Happy','Thinking':'Thinking','Sad':'Sad','Celebration':'Celebrating','Surprised':'Surprised','Curious':'Curious','InteractionReaction':'Excited','JumpStart':'Determined','JumpAir':'Surprised','JumpLand':'Determined','WalkStart':'Curious','RunStart':'Determined','TurnLeft':'Curious','TurnRight':'Curious'}
for clip,seconds in CLIPS.items():
 end=round(seconds*30);frames=sorted(set(list(range(0,end+1,2))+[end]));duration=end/30
 action=bpy.data.actions.new(clip);rig.animation_data_create();rig.animation_data.action=action
 facekeys=face.data.shape_keys;facekeys.animation_data_create();fa=bpy.data.actions.new(clip+'_Face');facekeys.animation_data.action=fa
 for frame in frames:
  u=frame/end;t=frame/30;p=2*pi*u;pulse=sin(pi*u)**2
  for pb in rig.pose.bones:pb.location=(0,0,0);pb.rotation_quaternion=(1,0,0,0);pb.scale=(1,1,1)
  root_z=.004*(1-cos(p));lean=.012*sin(p);rot('Chest',lean);rot('Head',-.005,.04*sin(p),.015*sin(p))
  for side,suf in [(1,'L'),(-1,'R')]:rot('UpperArm.'+suf,0,side*.08,0);rot('Forearm.'+suf,-.12)
  if clip in ['Walk','Run']:
   run=clip=='Run';stance=.32 if run else .60;reach=.26 if run else .22
   root_z=(-.05+.04*cos(2*p)) if run else (-.043+.006*cos(2*p))
   for side,suf,phase in [(1,'L',u%1),(-1,'R',(u+.5)%1)]:
    if phase<stance:fy=-reach+2*reach*phase/stance;fz=.075
    else:q=(phase-stance)/(1-stance);fy=reach*cos(pi*q);fz=.075+(.13 if run else .065)*sin(pi*q)
    leg(side,fy,fz,root_z,.08*sin(2*pi*phase) if run else .03*sin(2*pi*phase))
    rot('UpperArm.'+suf,(.75 if run else .40)*sin(2*pi*phase),side*.06,0);rot('Forearm.'+suf,-(.75 if run else .20)+.12*sin(2*pi*phase))
   rot('Chest',.16 if run else .035,0,.04*sin(p));rot('Head',-.08 if run else -.02,.025*sin(p),-.02*sin(p));rot('Hips',0,0,-.045*sin(p))
  elif clip in ['WalkStart','RunStart','WalkStop','RunStop']:
   gain=(u if 'Start' in clip else 1-u);root_z=-.04*gain
   leg(1,-.10*gain,.075,root_z);leg(-1,.10*gain,.075,root_z);rot('Chest',(.18 if clip.startswith('Run') else .06)*gain)
   rot('UpperArm.L',.27*gain,.05,0);rot('UpperArm.R',-.27*gain,-.05,0)
  elif clip=='JumpStart':
   root_z=-.115*sin(u*pi/2);leg(1,-.025,.075,root_z);leg(-1,-.025,.075,root_z);rot('Chest',.16*u)
   rot('UpperArm.L',.35*u,.12,0);rot('UpperArm.R',.35*u,-.12,0)
  elif clip=='JumpAir':
   root_z=0;leg(1,-.08,.18,0,-.16);leg(-1,.06,.16,0,-.12)
   arm_ik(1,(.29,-.06,1.17),(.36,.02,.96));arm_ik(-1,(-.29,-.06,1.17),(-.36,.02,.96));rot('Chest',-.04)
  elif clip=='JumpLand':
   root_z=-.10*(1-u)**2;leg(1,0,.075,root_z);leg(-1,0,.075,root_z);rot('Chest',.14*(1-u));rot('UpperArm.L',-.25*(1-u),-.25*(1-u));rot('UpperArm.R',-.25*(1-u),.25*(1-u))
  elif clip in ['TurnLeft','TurnRight']:
   sign=1 if clip=='TurnLeft' else -1;rot('Hips',0,0,sign*.20*sin(pi*u));rot('Chest',0,0,sign*.18*sin(pi*u));rot('Head',0,0,sign*.16*sin(pi*u));leg(1,sign*.07*sin(pi*u),.075,0);leg(-1,-sign*.07*sin(pi*u),.075,0)
  elif clip=='Greeting':
   arm_ik(-1,(-.27-.025*sin(6*pi*u),-.09,1.29+.015*sin(6*pi*u)),(-.39,-.03,1.06));rot('Hand.R',0,0,.25*sin(6*pi*u));rot('Head',-.03,.05*sin(p),-.09*pulse);root_z=.008*pulse
  elif clip in ['Happy','Celebration']:
   celebration=clip=='Celebration';root_z=(.14 if celebration else .025)*(1-cos(p))
   for side in [-1,1]:arm_ik(side,(side*(.28+.02*sin(p)),-.08,1.30 if celebration else 1.12),(side*.37,-.03,1.02))
   rot('Chest',0,0,.08*sin(p));rot('Head',-.05,0,-.05*sin(p))
   if celebration:leg(1,-.02,.10,0);leg(-1,.02,.10,0)
  elif clip=='Thinking':
   arm_ik(-1,(-.055,-.180,1.08),(-.33,-.13,.84));rot('Head',.08,.08,.13*pulse);rot('Chest',.025)
  elif clip=='Sad':
   rot('Chest',.13*pulse);rot('Head',.24*pulse,-.03,.035);root_z=-.015*pulse;rot('UpperArm.L',.07,.12);rot('UpperArm.R',.07,-.12)
  elif clip in ['Surprised','InteractionReaction']:
   root_z=.025*pulse;rot('Chest',-.11*pulse);rot('Head',-.06*pulse)
   for side in [-1,1]:arm_ik(side,(side*.28,-.18,1.01+.08*pulse),(side*.38,-.04,.91))
  elif clip=='Curious':rot('Head',.03,.18*sin(p)*pulse,.17*pulse);rot('Chest',0,0,-.035*pulse)
  rig.pose.bones['Root'].location.z=root_z
  rot('HairKnot',.045*sin(p-.5),.04*sin(p-.7),.025*sin(p));rot('PaperPin',.035*sin(p-.9));rot('LetterSatchel',.04*sin(p-.6),.025*sin(p-.3));rot('GoreumTie',.065*sin(p-.4))
  for pb in rig.pose.bones:
   pb.keyframe_insert(data_path='rotation_quaternion',frame=frame+1,group=pb.name)
   if pb.name=='Root':pb.keyframe_insert(data_path='location',frame=frame+1,group='Root')
  for mood in EXPRESSIONS:
   val=(.70+.30*sin(pi*u)) if EMOTION.get(clip)==mood else 0
   if mood=='Blink':val=max(0,1-abs(t-2.85)/.075) if clip=='Idle' else 0
   facekeys.key_blocks[mood].value=val;facekeys.key_blocks[mood].keyframe_insert(data_path='value',frame=frame+1)
 for a in [action,fa]:
  for fc in a.fcurves:
   for k in fc.keyframe_points:k.interpolation='LINEAR' if clip in ['Walk','Run'] else 'BEZIER'
 for obj,a in [(rig,action),(facekeys,fa)]:
  ad=obj.animation_data;track=ad.nla_tracks.new();track.name=clip;track.strips.new(clip,1,a);ad.action=None

for p in rig.pose.bones:p.location=(0,0,0);p.rotation_quaternion=(1,0,0,0);p.scale=(1,1,1)
for k in face.data.shape_keys.key_blocks:k.value=0
# Save full editable rig/weights/NLA/morphs. Geometry stays in-place; world movement is runtime.
scene=bpy.context.scene;scene.frame_set(1);scene.frame_end=97;scene.unit_settings.system='METRIC'
stem='nari-messenger-art' if ART else 'nari-messenger'
src=ROOT/f'assets/v0.5/source-blend/{stem}.blend';dst=ROOT/f'exports/v0.5/models/{stem}.glb';src.parent.mkdir(parents=True,exist_ok=True);dst.parent.mkdir(parents=True,exist_ok=True)
skin_report=[]
for o in scene.objects:
 if o.type!='MESH':continue
 boneids={g.index for g in o.vertex_groups if g.name in REST};counts=[len([g for g in v.groups if g.group in boneids and g.weight>0]) for v in o.data.vertices];totals=[sum(g.weight for g in v.groups if g.group in boneids) for v in o.data.vertices]
 skin_report.append({'mesh':o.name,'vertices':len(o.data.vertices),'unweighted_vertices':sum(c==0 for c in counts),'max_influences':max(counts),'max_weight_error':max(abs(v-1) for v in totals),'morphs':[k.name for k in o.data.shape_keys.key_blocks] if o.data.shape_keys else []})
 assert max(counts)<=4 and min(counts)>=1 and max(abs(v-1) for v in totals)<.00001
bpy.ops.wm.save_as_mainfile(filepath=str(src))
# glTF skinned meshes are scene roots, with skeleton roots as siblings. Keep the
# editable Blender outliner parented; export identity root meshes to avoid ignored
# parent-transform semantics and Validator NODE_SKINNED_MESH_NON_ROOT warnings.
for o in scene.objects:
 if o.type=='MESH':o.parent=None
bpy.ops.export_scene.gltf(filepath=str(dst),export_format='GLB',export_yup=True,export_animations=True,export_animation_mode='NLA_TRACKS',export_nla_strips=True,export_force_sampling=True,export_optimize_animation_keep_anim_object=True,export_optimize_animation_keep_anim_armature=True,export_try_sparse_sk=True,export_tangents=ART,export_cameras=False,export_lights=False)
report={'concept':'A — Nari, user approved','bone_count':len(REST),'bones':list(REST),'meshes':skin_report,'clips':CLIPS,'expressions':['Neutral']+EXPRESSIONS[:-1],'blink':'Blink morph plus native Idle channel','authoring':'Original continuous voxel-unioned body with Blender bone-heat anatomical weights, normalized maximum4 influences; explicit torso/accessory/face weights and deformation armature. Analytic two-bone leg/arm IK authored into quaternion keyframes; editable NLA in source. No image is used as a mesh.','limitations':'Requires actual browser pose/motion/side/rear deformation inspection and physics/controller verification before acceptance.'}
report_dir=ROOT/('quality-reports/v0.5/gate-d' if ART else 'quality-reports/v0.5/gate-c');report_dir.mkdir(parents=True,exist_ok=True)
(report_dir/('rig-authoring-art.json' if ART else 'rig-authoring.json')).write_text(json.dumps(report,indent=2)+'\n')
print('NARI_ACTUAL_SKIN_SAVED',len(REST),'bones',dst.stat().st_size,'bytes')
