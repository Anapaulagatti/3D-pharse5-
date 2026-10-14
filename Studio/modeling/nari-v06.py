"""Approved B: original large-eyed chibi messenger, new geometry/skin/morphs.
Uses original v0.5 rig/controller naming and adapted authoring, never old GLB scaling.
Blender Z-up/front-Y; GLB Y-up/front+Z. Flat vertex-color palette, no textures.
"""
import bpy,sys,json,math
from pathlib import Path
from math import sin,cos,pi,sqrt
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import reset,material,sphere,box,path,mesh,join,color
from chibi_motion_v06 import author
ROOT=Path(__file__).resolve().parents[2];reset()
COL={'skin':'F1C4A5','cream':'FFF0D8','mint':'88C9B3','navy':'293C55','hair':'292833','coral':'F18478','honey':'E9BB69','white':'FFFCF1','iris':'624335','pupil':'202837','cheek':'EDA090'}
M={k:material('Chibi_'+k,'FFFFFF',r,0) for k,r in [('skin',.78),('cloth',.88),('dark',.82),('accent',.55)]}
for m in M.values():
 n=m.node_tree.nodes.new('ShaderNodeVertexColor');n.layer_name='Color';m.node_tree.links.new(n.outputs['Color'],m.node_tree.nodes.get('Principled BSDF').inputs['Base Color']);m.node_tree.nodes.get('Principled BSDF').inputs['Specular IOR Level'].default_value=.25
def paint(o,c,mat='cloth'):
 o.data.materials.clear();o.data.materials.append(M[mat]);a=o.data.color_attributes.new(name='Color',type='FLOAT_COLOR',domain='CORNER')
 for d in a.data:d.color=color(COL.get(c,c))
 return o
def S(n,p,s,c='skin',mat='skin',seg=16,rings=10):return paint(sphere(n,p,s,None,seg,rings),c,mat)
def B(n,p,s,c='cream',mat='cloth',bevel=.012):return paint(box(n,p,s,None,bevel),c,mat)
def P(n,p,r,c='cream',mat='cloth'):return paint(path(n,p,r,None),c,mat)
def apply(o):
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
def capsule(n,a,b,r,d=None):
 a,b=Vector(a),Vector(b);o=sphere(n,(a+b)/2,(r,d or r,(b-a).length/2+r*.65),None,12,8);o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return o
parts=[sphere('Torso',(0,0,.515),(.157,.095,.13),None,16,10),sphere('Hips',(0,0,.397),(.148,.10,.085),None,16,10),capsule('Neck',(0,0,.60),(0,0,.68),.055)]
for side in [-1,1]:
 parts += [capsule('Thigh',(side*.085,0,.395),(side*.10,0,.215),.079,.077),capsule('Shin',(side*.10,0,.215),(side*.105,0,.065),.054,.052),sphere('Foot',(side*.105,-.045,.038),(.066,.099,.036),None,16,8),capsule('Sleeve',(side*.158,0,.59),(side*.245,0,.465),.057,.055),capsule('Forearm',(side*.245,0,.465),(side*.285,0,.34),.043,.040),sphere('Hand',(side*.29,-.006,.316),(.036,.026,.047),None,12,8),capsule('Thumb',(side*.27,-.012,.335),(side*.254,-.03,.313),.013)]
body=join('ChibiContinuousBody',parts);apply(body)
mod=body.modifiers.new('ContinuousAnatomy','REMESH');mod.mode='VOXEL';mod.voxel_size=.013;mod.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=mod.name)
mod=body.modifiers.new('SoftSurface','SMOOTH');mod.factor=.65;mod.iterations=4;bpy.ops.object.modifier_apply(modifier=mod.name)
tris=sum(len(f.vertices)-2 for f in body.data.polygons);mod=body.modifiers.new('RealtimeBodyBudget','DECIMATE');mod.ratio=min(.9,3000/tris);bpy.ops.object.modifier_apply(modifier=mod.name)
body.data.materials.clear()
for k in ['skin','cloth','dark']:body.data.materials.append(M[k])
a=body.data.color_attributes.new(name='Color',type='FLOAT_COLOR',domain='CORNER')
for f in body.data.polygons:
 f.material_index=1;f.use_smooth=True
 for i in f.loop_indices:
  v=body.data.vertices[body.data.loops[i].vertex_index].co
  c='skin' if v.z>.625 or abs(v.x)>.245 and v.z<.44 else 'navy' if v.z<.13 and abs(v.x)<.205 else 'cream' if v.z<.415 and abs(v.x)<.205 else 'coral'
  a.data[i].color=color(COL[c])
arm=bpy.data.armatures.new('NariChibiSkeleton');rig=bpy.data.objects.new('NariChibiArmature',arm);bpy.context.collection.objects.link(rig);bpy.context.view_layer.objects.active=rig;bpy.ops.object.select_all(action='DESELECT');rig.select_set(True);bpy.ops.object.mode_set(mode='EDIT');REST={}
def bone(n,a,b,parent=None,connected=False):
 o=arm.edit_bones.new(n);o.head=a;o.tail=b
 if parent:o.parent=arm.edit_bones[parent];o.use_connect=connected
 REST[n]=(Vector(a),Vector(b))
bone('Root',(0,0,0),(0,0,.1));bone('Hips',(0,0,.395),(0,0,.45),'Root');bone('Spine',(0,0,.45),(0,0,.535),'Hips',True);bone('Chest',(0,0,.535),(0,0,.62),'Spine',True);bone('Neck',(0,0,.62),(0,0,.665),'Chest',True);bone('Head',(0,0,.665),(0,0,1.055),'Neck',True)
for side,suf in [(1,'L'),(-1,'R')]:
 bone('Clavicle.'+suf,(0,0,.59),(side*.158,0,.59),'Chest');bone('UpperArm.'+suf,(side*.158,0,.59),(side*.245,0,.465),'Clavicle.'+suf,True);bone('Forearm.'+suf,(side*.245,0,.465),(side*.285,0,.34),'UpperArm.'+suf,True);bone('Hand.'+suf,(side*.285,0,.34),(side*.29,0,.29),'Forearm.'+suf,True);bone('Fingers.'+suf,(side*.29,0,.29),(side*.29,0,.275),'Hand.'+suf,True)
 bone('Thigh.'+suf,(side*.085,0,.395),(side*.10,0,.215),'Hips');bone('Shin.'+suf,(side*.10,0,.215),(side*.105,0,.065),'Thigh.'+suf,True);bone('Foot.'+suf,(side*.105,0,.065),(side*.105,-.115,.035),'Shin.'+suf,True);bone('Toe.'+suf,(side*.105,-.115,.035),(side*.105,-.14,.035),'Foot.'+suf,True)
bone('HairKnot',(-.15,.135,.89),(-.15,.135,.98),'Head');bone('PaperPin',(-.16,.13,1.015),(-.20,.13,1.09),'Head');bone('LetterSatchel',(.221,-.035,.43),(.221,-.035,.34),'Hips');bone('GoreumTie',(.02,-.11,.56),(.02,-.11,.48),'Chest')
bpy.ops.object.mode_set(mode='OBJECT');rig.show_in_front=True
for p in rig.pose.bones:p.rotation_mode='QUATERNION'
excluded=['Root','Fingers.L','Fingers.R','HairKnot','PaperPin','LetterSatchel','GoreumTie']
for n in excluded:arm.bones[n].use_deform=False
bpy.ops.object.select_all(action='DESELECT');body.select_set(True);rig.select_set(True);bpy.context.view_layer.objects.active=rig;bpy.ops.object.parent_set(type='ARMATURE_AUTO');bpy.context.view_layer.objects.active=body;rig.select_set(False);bpy.ops.object.vertex_group_limit_total(limit=4);bpy.ops.object.vertex_group_normalize_all(lock_active=False)
for n in excluded:arm.bones[n].use_deform=True
def skin(o,n):
 apply(o);g=o.vertex_groups.get(n) or o.vertex_groups.new(name=n);g.add(list(range(len(o.data.vertices))),1,'REPLACE');m=o.modifiers.new('ChibiSkin','ARMATURE');m.object=rig;o.parent=rig
# Analytic smooth head, separate natural neck join, oversized cheeks and little ears.
head=S('ChibiSkinSurface',(0,0,.85),(.214,.182,.205),seg=24,rings=16);skin(head,'Head')
for side in [-1,1]:
 o=S('Ear',(side*.209,.008,.846),(.030,.028,.043));skin(o,'Head')
 # Short rolled cuffs accent real sleeve contour; no free-floating limbs.
 bpy.ops.mesh.primitive_torus_add(major_segments=12,minor_segments=6,major_radius=.049,minor_radius=.007,location=(side*.251,0,.446));o=paint(bpy.context.object,'cream');o.rotation_euler=Vector((side*.04,0,-.125)).to_track_quat('Z','Y').to_euler();skin(o,'Forearm.'+('L' if side>0 else 'R'))
for points in [[(-.073,-.09,.63),(-.015,-.113,.574),(.035,-.113,.53)],[(.073,-.09,.63),(.022,-.114,.58),(-.024,-.113,.548)]]:skin(P('CrossedCreamCollar',points,.013),'Chest')
bag=join('MintEnvelopeSatchel',[B('Bag',(.222,-.035,.405),(.132,.081,.145),'mint',bevel=.02),B('Flap',(.222,-.084,.447),(.134,.012,.065),'mint',bevel=.009),P('EnvelopeSeam',[(.162,-.094,.466),(.222,-.096,.427),(.282,-.094,.466)],.0038,'cream'),S('HoneyClasp',(.222,-.101,.422),(.011,.005,.011),'honey','accent',10,6)]);skin(bag,'LetterSatchel')
skin(P('ShortSatchelStrap',[(-.12,-.078,.612),(-.04,-.115,.553),(.065,-.116,.48),(.192,-.097,.455)],.009,'navy'),'Chest')
tie=join('NavyGoreum',[S('Knot',(.02,-.127,.565),(.014,.008,.011),'navy','cloth',10,6),P('TieTail',[(.02,-.127,.565),(.032,-.132,.5)],.008,'navy')]);skin(tie,'GoreumTie')
# Physical collar/hem/cuffs give clean clothing edges over smoothly colored anatomy.
bpy.ops.mesh.primitive_torus_add(major_segments=20,minor_segments=6,major_radius=.057,minor_radius=.009,location=(0,0,.638));skin(paint(bpy.context.object,'cream'),'Neck')
bpy.ops.mesh.primitive_torus_add(major_segments=20,minor_segments=6,major_radius=.152,minor_radius=.008,location=(0,0,.419));o=paint(bpy.context.object,'coral');o.scale.y=.70;skin(o,'Hips')
for side,suf in [(1,'L'),(-1,'R')]:
 bpy.ops.mesh.primitive_torus_add(major_segments=12,minor_segments=6,major_radius=.052,minor_radius=.008,location=(side*.105,0,.115));skin(paint(bpy.context.object,'navy'),'Shin.'+suf)
# Coherent rounded cap with sculpted scalloped fringe and visible low hair loop.
verts=[];faces=[];nr=24;rr=9
for j in range(rr+1):
 for i in range(nr):
  a=2*pi*i/nr;limit=1.15 if -sin(a)>.2 else 1.85 if -sin(a)>-.5 else 2.22;t=.025+(limit-.025)*j/rr;verts.append((.224*sin(t)*cos(a),.194*sin(t)*sin(a),.85+.218*cos(t)))
for j in range(rr):
 for i in range(nr):k=j*nr+i;faces.append((k,j*nr+(i+1)%nr,(j+1)*nr+(i+1)%nr,k+nr))
skin(paint(mesh('RoundedHairCap',verts,faces,None,smooth=True),'hair','dark'),'Head')
for x,z,tilt in [(-.125,.979,-.3),(-.055,.992,-.3),(.025,1.000,.22),(.103,.983,.35)]:
 o=S('ScallopedFringe',(x,-.15,z),(.052,.041,.066),'hair','dark',14,8);o.rotation_euler.y=tilt;skin(o,'Head')
for side in [-1,1]:skin(S('TempleLock',(side*.19,-.071,.899),(.026,.035,.079),'hair','dark',12,8),'Head')
bpy.ops.mesh.primitive_torus_add(major_segments=16,minor_segments=8,major_radius=.049,minor_radius=.019,location=(-.15,.14,.91),rotation=(pi/2,0,-.2));skin(paint(bpy.context.object,'hair','dark'),'HairKnot')
pin=paint(mesh('FoldedHanjiPin',[(-.145,.119,1.01),(-.195,.116,1.105),(-.236,.113,1.02),(-.185,.09,1.035),(-.168,.117,.989)],[(0,1,3),(1,2,3),(2,4,3),(4,0,3)],None),'cream');skin(pin,'PaperPin')
parts=[]
def feature(o,region):
 apply(o);g=o.vertex_groups.new(name=region);g.add(list(range(len(o.data.vertices))),1,'REPLACE');parts.append(o)
for side,suf in [(-1,'L'),(1,'R')]:
 x=side*.079
 for n,p,s,c,mat in [('EyeWhite',(x,-.166,.86),(.052,.018,.060),'white','skin'),('Iris',(x,-.184,.857),(.031,.010,.045),'iris','dark'),('Pupil',(x,-.193,.86),(.021,.006,.033),'pupil','dark'),('EyeLight',(x-.010,-.200,.881),(.009,.003,.011),'white','skin')]:feature(S(n+suf,p,s,c,mat,14,8),'Eye'+suf)
 feature(P('Brow'+suf,[(x-.037,-.164,.94),(x,-.169,.950),(x+.035,-.164,.94)],.005,'hair','dark'),'Brow'+suf)
 feature(S('Cheek'+suf,(side*.132,-.147,.796),(.031,.005,.013),'cheek','skin',12,6),'Cheek')
feature(S('ButtonNose',(0,-.182,.803),(.014,.014,.017),'skin','skin',12,8),'Nose')
v=[(0,-.163,.753)]+[(.035*cos(i/20*2*pi),-.165,.753+.006*sin(i/20*2*pi)) for i in range(20)];feature(paint(mesh('Smile',v,[(0,i+1,(i+1)%20+1) for i in range(20)],None),'pupil','dark'),'Mouth')
face=join('NariFacialControls',parts);regions={g.name:{v.index for v in face.data.vertices if any(q.group==g.index for q in v.groups)} for g in face.vertex_groups};face.shape_key_add(name='Basis')
EXPRESSIONS=['Happy','Excited','Curious','Thinking','Confused','Sad','Surprised','Determined','Celebrating','Blink']
spec={'Happy':(.62,.62,.044,.022,.017,0),'Excited':(1.05,1.05,.046,.032,.013,0),'Curious':(1.13,.88,.023,.010,0,.005),'Thinking':(.78,.88,.025,.004,-.002,.008),'Confused':(.80,1.10,.029,.004,-.007,-.008),'Sad':(.72,.72,.030,.004,-.018,0),'Surprised':(1.16,1.16,.023,.031,0,0),'Determined':(.72,.72,.032,.004,.001,0),'Celebrating':(.48,.48,.047,.031,.018,0),'Blink':(.06,.06,.035,.006,0,0)}
for mood in EXPRESSIONS:
 key=face.shape_key_add(name=mood);el,er,rx,rz,corner,offset=spec[mood]
 for side,suf,factor in [(-1,'L',el),(1,'R',er)]:
  for i in regions['Eye'+suf]:key.data[i].co.z=.86+(face.data.vertices[i].co.z-.86)*factor
  for i in regions['Brow'+suf]:
   p=face.data.vertices[i].co;tilt=-side*.4 if mood=='Sad' else side*.3 if mood=='Determined' else .28 if mood in ['Thinking','Confused'] else 0;lift=.018 if mood in ['Surprised','Excited','Celebrating'] else .008 if mood in ['Happy','Curious'] else 0;key.data[i].co.z=p.z+lift+tilt*(p.x-side*.079)
 if mood!='Blink':
  for i in regions['Mouth']:
   p=face.data.vertices[i].co;xn=p.x/.035;zn=(p.z-.753)/.006;key.data[i].co.x=rx*xn+offset;key.data[i].co.z=.753+rz*zn+corner*xn*xn
skin(face,'Head')
costume=join('NariSkinnedBodyAndCostume',[o for o in bpy.context.scene.objects if o.type=='MESH' and o!=face and o!=head]);skin_names=list(REST)
# Join preserves existing weights/modifier; no second skin modifier.
CLIPS=author(rig,arm,REST,face,EXPRESSIONS)
for p in rig.pose.bones:p.location=(0,0,0);p.rotation_quaternion=(1,0,0,0);p.scale=(1,1,1)
for k in face.data.shape_keys.key_blocks:k.value=0
scene=bpy.context.scene;scene.frame_set(1);scene.frame_end=97
src=ROOT/'assets/v0.6/source-blend/nari-chibi.blend';dst=ROOT/'exports/v0.6/models/nari-chibi.glb';src.parent.mkdir(parents=True,exist_ok=True);dst.parent.mkdir(parents=True,exist_ok=True)
report=[]
for o in scene.objects:
 if o.type!='MESH':continue
 ids={g.index for g in o.vertex_groups if g.name in REST};counts=[sum(g.group in ids and g.weight>0 for g in v.groups) for v in o.data.vertices];totals=[sum(g.weight for g in v.groups if g.group in ids) for v in o.data.vertices];assert min(counts)>0 and max(counts)<=4 and max(abs(n-1) for n in totals)<.00001
 report.append({'mesh':o.name,'vertices':len(o.data.vertices),'triangles':sum(len(f.vertices)-2 for f in o.data.polygons),'unweighted':0,'max_influences':max(counts)})
bpy.ops.wm.save_as_mainfile(filepath=str(src))
for o in scene.objects:
 if o.type=='MESH':o.parent=None
bpy.ops.export_scene.gltf(filepath=str(dst),export_format='GLB',export_yup=True,export_animations=True,export_animation_mode='NLA_TRACKS',export_nla_strips=True,export_force_sampling=True,export_optimize_animation_keep_anim_object=True,export_optimize_animation_keep_anim_armature=True,export_try_sparse_sk=True,export_cameras=False,export_lights=False)
out=ROOT/'quality-reports/v0.6/prototype/rig-authoring.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps({'approved':'B+T1','meshes':report,'bones':len(REST),'clips':CLIPS,'morphs':EXPRESSIONS,'height_m':1.105,'head_height_m':.41,'walk_speed_mps':.888889,'run_speed_mps':2.375,'authoring':'Original new continuous short-limb body/analytic large head/scalloped hair/coral collar/mint envelope bag/large facial geometry. Bone-heat body weights and rigid natural layers, reused naming and adapted analytic IK authoring. No old GLB imported/scaled.','acceptance':'PENDING_ACTUAL_RENDER'},indent=2)+'\n');print('CHIBI_SAVED',dst.stat().st_size,sum(x['triangles'] for x in report))
