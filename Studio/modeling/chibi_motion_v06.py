"""v0.6 short-limb performances adapted from original v0.5 authoring, with new
rest-length IK, .6s/.5s gait, measured stride contract and true world-up root bob.
No existing clip or source file overwritten. Blender authoring helper only.
"""
import bpy
from math import sin,cos,pi,acos,atan2,sqrt
from mathutils import Vector,Euler
def author(rig,arm,REST,face,EXPRESSIONS):
 def motionpoint(p):return Vector((p[0]*.85,p[1]*.9,.395+(p[2]-.67)*.65))
 def rot(name,rx=0,ry=0,rz=0):
  b=rig.data.bones[name].matrix_local.to_quaternion();q=Euler((rx,ry,rz),'XYZ').to_quaternion();rig.pose.bones[name].rotation_quaternion=b.conjugated()@q@b
 def arm_ik(side,target,pole):
  suffix='L' if side>0 else 'R';names=['UpperArm.'+suffix,'Forearm.'+suffix,'Hand.'+suffix]
  s,e=REST[names[0]];_,w=REST[names[1]];target=motionpoint(target);pole=motionpoint(pole)
  l1=(e-s).length;l2=(w-e).length;d=min((target-s).length,l1+l2-.001);u=(target-s).normalized();v=pole-s-u*(pole-s).dot(u);v.normalize();a=(l1*l1-l2*l2+d*d)/(2*d);k=s+u*a+v*sqrt(max(0,l1*l1-a*a))
  q1=(e-s).rotation_difference(k-s);q2=(w-e).rotation_difference(target-k)
  b1=arm.bones[names[0]].matrix_local.to_quaternion();b2=arm.bones[names[1]].matrix_local.to_quaternion()
  rig.pose.bones[names[0]].rotation_quaternion=b1.conjugated()@q1@b1
  rig.pose.bones[names[1]].rotation_quaternion=b2.conjugated()@q1.conjugated()@q2@b2
 def leg(side,foot_y,foot_z,root_z=0,tilt=0):
  suffix='L' if side>0 else 'R';l1=(REST['Thigh.'+suffix][1]-REST['Thigh.'+suffix][0]).length;l2=(REST['Shin.'+suffix][1]-REST['Shin.'+suffix][0]).length
  dz=REST['Thigh.'+suffix][0].z+root_z-foot_z;d=min(sqrt(dz*dz+foot_y*foot_y),l1+l2-.001);theta=atan2(foot_y,dz);alpha=acos(max(-1,min(1,(l1*l1+d*d-l2*l2)/(2*l1*d))));knee=pi-acos(max(-1,min(1,(l1*l1+l2*l2-d*d)/(2*l1*l2))))
  thigh=theta-alpha;rot('Thigh.'+suffix,thigh);rot('Shin.'+suffix,knee);rot('Foot.'+suffix,-thigh-knee+tilt)
 
 CLIPS={'Idle':3.2,'Walk':.6,'Run':.5,'WalkStart':.3,'WalkStop':.3,'RunStart':.3,'RunStop':.366667,'JumpStart':.2,'JumpAir':.6,'JumpLand':.333333,'TurnLeft':.5,'TurnRight':.5,'Greeting':2.0,'Happy':1.8,'Thinking':2.4,'Sad':2.4,'Celebration':2.2,'Surprised':1.4,'Curious':2.2,'InteractionReaction':1.4}
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
    run=clip=='Run';stance=.32 if run else .60;reach=.19 if run else .16
    root_z=(-.055+.025*cos(2*p)) if run else (-.034+.005*cos(2*p))
    for side,suf,phase in [(1,'L',u%1),(-1,'R',(u+.5)%1)]:
     if phase<stance:fy=-reach+2*reach*phase/stance;fz=.065
     else:q=(phase-stance)/(1-stance);fy=reach*cos(pi*q);fz=.065+(.08 if run else .045)*sin(pi*q)
     leg(side,fy,fz,root_z,.08*sin(2*pi*phase) if run else .03*sin(2*pi*phase))
     rot('UpperArm.'+suf,(.75 if run else .40)*sin(2*pi*phase),side*.06,0);rot('Forearm.'+suf,-(.75 if run else .20)+.12*sin(2*pi*phase))
    rot('Chest',.16 if run else .035,0,.04*sin(p));rot('Head',-.08 if run else -.02,.025*sin(p),-.02*sin(p));rot('Hips',0,0,-.045*sin(p))
   elif clip in ['WalkStart','RunStart','WalkStop','RunStop']:
    gain=(u if 'Start' in clip else 1-u);root_z=-.04*gain
    leg(1,-.10*gain,.065,root_z);leg(-1,.10*gain,.065,root_z);rot('Chest',(.18 if clip.startswith('Run') else .06)*gain)
    rot('UpperArm.L',.27*gain,.05,0);rot('UpperArm.R',-.27*gain,-.05,0)
   elif clip=='JumpStart':
    root_z=-.060*sin(u*pi/2);leg(1,-.025,.065,root_z);leg(-1,-.025,.065,root_z);rot('Chest',.16*u)
    rot('UpperArm.L',.35*u,.12,0);rot('UpperArm.R',.35*u,-.12,0)
   elif clip=='JumpAir':
    root_z=0;leg(1,-.08,.18,0,-.16);leg(-1,.06,.16,0,-.12)
    arm_ik(1,(.29,-.06,1.17),(.36,.02,.96));arm_ik(-1,(-.29,-.06,1.17),(-.36,.02,.96));rot('Chest',-.04)
   elif clip=='JumpLand':
    root_z=-.055*(1-u)**2;leg(1,0,.065,root_z);leg(-1,0,.065,root_z);rot('Chest',.14*(1-u));rot('UpperArm.L',-.25*(1-u),-.25*(1-u));rot('UpperArm.R',-.25*(1-u),.25*(1-u))
   elif clip in ['TurnLeft','TurnRight']:
    sign=1 if clip=='TurnLeft' else -1;rot('Hips',0,0,sign*.20*sin(pi*u));rot('Chest',0,0,sign*.18*sin(pi*u));rot('Head',0,0,sign*.16*sin(pi*u));leg(1,sign*.07*sin(pi*u),.065,0);leg(-1,-sign*.07*sin(pi*u),.065,0)
   elif clip=='Greeting':
    arm_ik(-1,(-.27-.025*sin(6*pi*u),-.09,1.29+.015*sin(6*pi*u)),(-.39,-.03,1.06));rot('Hand.R',0,0,.25*sin(6*pi*u));rot('Head',-.03,.05*sin(p),-.09*pulse);root_z=.008*pulse
   elif clip in ['Happy','Celebration']:
    celebration=clip=='Celebration';root_z=(.075 if celebration else .018)*(1-cos(p))
    for side in [-1,1]:arm_ik(side,(side*(.28+.02*sin(p)),-.08,1.30 if celebration else 1.12),(side*.37,-.03,1.02))
    rot('Chest',0,0,.08*sin(p));rot('Head',-.05,0,-.05*sin(p))
    if celebration:leg(1,-.02,.10,0);leg(-1,.02,.10,0)
   elif clip=='Thinking':
    arm_ik(-1,(-.055,-.180,1.18),(-.33,-.13,.84));rot('Head',.08,.08,.13*pulse);rot('Chest',.025)
   elif clip=='Sad':
    rot('Chest',.13*pulse);rot('Head',.24*pulse,-.03,.035);root_z=-.015*pulse;rot('UpperArm.L',.07,.12);rot('UpperArm.R',.07,-.12)
   elif clip in ['Surprised','InteractionReaction']:
    root_z=.025*pulse;rot('Chest',-.11*pulse);rot('Head',-.06*pulse)
    for side in [-1,1]:arm_ik(side,(side*.28,-.18,1.01+.08*pulse),(side*.38,-.04,.91))
   elif clip=='Curious':rot('Head',.03,.18*sin(p)*pulse,.17*pulse);rot('Chest',0,0,-.035*pulse)
   rig.pose.bones['Root'].location=arm.bones['Root'].matrix_local.to_quaternion().conjugated()@Vector((0,0,root_z))
   rig.pose.bones['Chest'].scale=(1+.012*pulse,1-.008*pulse,1+.012*pulse)
   rot('HairKnot',.045*sin(p-.5),.04*sin(p-.7),.025*sin(p));rot('PaperPin',.035*sin(p-.9));rot('LetterSatchel',.04*sin(p-.6),.025*sin(p-.3));rot('GoreumTie',.065*sin(p-.4))
   for pb in rig.pose.bones:
    pb.keyframe_insert(data_path='rotation_quaternion',frame=frame+1,group=pb.name)
    if pb.name=='Root':pb.keyframe_insert(data_path='location',frame=frame+1,group='Root')
    if pb.name=='Chest':pb.keyframe_insert(data_path='scale',frame=frame+1,group=pb.name)
   for mood in EXPRESSIONS:
    val=(.70+.30*sin(pi*u)) if EMOTION.get(clip)==mood else 0
    if mood=='Blink':val=max(0,1-abs(t-2.85)/.065) if clip=='Idle' else 0
    facekeys.key_blocks[mood].value=val;facekeys.key_blocks[mood].keyframe_insert(data_path='value',frame=frame+1)
  for a in [action,fa]:
   for fc in a.fcurves:
    for k in fc.keyframe_points:k.interpolation='LINEAR' if clip in ['Walk','Run'] else 'BEZIER'
  for obj,a in [(rig,action),(facekeys,fa)]:
   ad=obj.animation_data;track=ad.nla_tracks.new();track.name=clip;track.strips.new(clip,1,a);ad.action=None
 
 return CLIPS
