"""Versioned Ceramic Seed Spirit: preserved geometry, independent limbs and 12 authored performances."""
import sys, math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
from math import sin,cos,pi,exp

bpy.ops.wm.open_mainfile(filepath=str(ROOT/'assets/source-blend/mascot-base.blend'))
for o in bpy.context.scene.objects:
    o.animation_data_clear()
for a in list(bpy.data.actions): bpy.data.actions.remove(a)
root=bpy.data.objects['MascotRoot']; body=bpy.data.objects['BodyPivot']; head=bpy.data.objects['HeadPivot']
left=bpy.data.objects['ArmLeftPivot'];right=bpy.data.objects['ArmRightPivot']
ears=[bpy.data.objects['CeramicLeafPivot'],bpy.data.objects['HanjiLeafPivot']]
root.location=(0,0,0);root.rotation_euler=(0,0,0);root.scale=(1,1,1)
head.rotation_euler=(0,0,0);left.rotation_euler=(0,0,0);right.rotation_euler=(0,0,0)
M={n:bpy.data.materials[n] for n in ['CeladonEnamel','DeepCeladon','navy','cream','coral','BrassInlay']}
# Keep the original sculpted body, growth seams, collar, ears and mitten silhouette.
feet=sorted([o for o in bpy.context.scene.objects if o.name.startswith('CeramicFoot')],key=lambda o:o.location.x)
legs=[]
for i,side in enumerate([-1,1]):
    leg=empty('LegLeftPivot' if side<0 else 'LegRightPivot',(side*.17,0,.23),root)
    feet[i].parent=leg;feet[i].location=(0,-.015,-.12)
    sphere('CeramicAnkle',(0,0,-.04),(.065,.065,.095),M['DeepCeladon'],12,6,leg)
    legs.append(leg)
# Facial geometry remains editable/exportable, rather than a texture sprite overlay.
bpy.data.objects.remove(bpy.data.objects['Smile'],do_unlink=True)
mouth=empty('FaceMouthPivot',(0,-.31,.137),head)
face={}
face['Smile']=path('FaceSmile',[(-.052,0,.016),(-.025,-.01,-.014),(0,-.012,-.024),(.025,-.01,-.014),(.052,0,.016)],.010,M['navy'],mouth)
face['Frown']=path('FaceFrown',[(-.051,0,-.008),(-.027,-.01,.018),(0,-.012,.028),(.027,-.01,.018),(.051,0,-.008)],.010,M['navy'],mouth)
face['Thought']=path('FaceThought',[(-.025,-.012,0),(.027,-.012,0),(.044,-.008,.012)],.009,M['navy'],mouth)
face['Open']=sphere('FaceOpen',(0,-.015,-.002),(.064,.012,.054),M['navy'],16,8,mouth)
face['Tongue']=sphere('FaceTongue',(0,-.029,-.024),(.039,.008,.018),M['coral'],12,6,mouth)
face['O']=sphere('FaceO',(0,-.015,0),(.027,.012,.039),M['navy'],16,8,mouth)
eyes=[bpy.data.objects['EyeLeft'],bpy.data.objects['EyeRight']]; eye_pivots=[]; happy_eyes=[]; brows=[]
catch=sorted([o for o in bpy.context.scene.objects if o.name.startswith('EyeCatchlight')],key=lambda o:o.location.x)
cheeks=sorted([o for o in bpy.context.scene.objects if o.name.startswith('CoralBlush')],key=lambda o:o.location.x)
for i,side in enumerate([-1,1]):
    pivot=empty('FaceEyeLeftPivot' if side<0 else 'FaceEyeRightPivot',eyes[i].location,head)
    catch[i].location-=eyes[i].location;catch[i].parent=pivot
    eyes[i].location=(0,0,0);eyes[i].parent=pivot
    arch=path('FaceHappyEyeLeft' if side<0 else 'FaceHappyEyeRight',[(-.035,-.023,-.007),(-.02,-.026,.018),(0,-.028,.025),(.02,-.026,.018),(.035,-.023,-.007)],.009,M['navy'],pivot)
    happy_eyes.append(arch);eye_pivots.append(pivot)
    brow=path('FaceBrowLeft' if side<0 else 'FaceBrowRight',[(-.038,0,0),(0,-.003,.011),(.038,0,0)],.007,M['DeepCeladon'])
    brow.parent=head;brow.location=(side*.125,-.264,.303);brows.append(brow)

clips={'Idle':3.2,'Walk':1.5,'Run':.86,'Jump':1.8,'Greeting':2.1,'Happy':1.9,'Thinking':2.5,'Celebration':2.2,'Disappointed':2.4,'Curious':2.2,'ClickReaction':1.35,'ReturnToIdle':.8}
for clip,duration in clips.items():
    end=round(duration*30); duration=end/30
    tracks={o:[] for o in [root,body,head,left,right,*legs,*ears,*eyes,*catch,*happy_eyes,*brows,*cheeks,*face.values()]}
    # Dense deliberate authored samples preserve arcs and prevent interpolated feet sliding.
    for frame in range(0,end+1,3):
        t=frame/30;u=t/duration;p=2*pi*u;w=sin(p);pulse=sin(pi*u)**2
        lift=.026*(1-cos(p)); lean=(.015*w,0,.028*w);head_rot=(0,.045*w,.04*w)
        squash=(1+.016*cos(p),1+.016*cos(p),1-.025*cos(p));bodyrot=(0,0,0)
        arm_l=(.045*w,.08*w,0);arm_r=(-.045*w,-.08*w,0)
        pos_l=(-.375,0,.77);pos_r=(.375,0,.77)
        leg_l=(0,0,0);leg_r=(0,0,0);leg_pos=[(-.17,0,.23),(.17,0,.23)]
        x=0; turn=0; ear_gain=.07; smile='Smile'; eye_scales=[(1,1,1),(1,1,1)]; browtilts=[0,0]
        blush=1;happy=False
        if clip in ['Walk','Run']:
            run=clip=='Run';a=.95 if run else .57
            leg_l=(a*w,0,-.05*w);leg_r=(-a*w,0,-.05*w)
            leg_pos=[(-.17,0,.23+(.12 if run else .055)*max(0,w)),(.17,0,.23+(.12 if run else .055)*max(0,-w))]
            arm_l=(-a*.8*w,.14,0);arm_r=(a*.8*w,-.14,0)
            lift=(.12 if run else .035)*(1-cos(p*2))*.5
            lean=(-.22 if run else -.055,.055*w,.035*w);head_rot=(.10 if run else 0,.06*w,-.025*w)
            squash=(1-.045*cos(2*p),1-.045*cos(2*p),1+.075*cos(2*p));x=(.30 if run else .18)*w
            ear_gain=.19 if run else .10;smile='Open' if run else 'Smile';blush=1.15
            eye_scales=[(1.16,1,1.10)]*2 if run else [(1.06,1,.85)]*2;browtilts=[.12,-.12]
        elif clip in ['Jump','ClickReaction']:
            # Clear crouch -> stretch launch -> floating arc -> squash landing -> settle.
            anticipation=max(0,1-abs(u-.13)/.13);air=max(0,sin(pi*(u-.23)/.47)) if .23<u<.70 else 0
            landing=max(0,1-abs(u-.77)/.10)
            lift=.58*air-.065*anticipation-.04*landing
            z=1-.16*anticipation+.13*air-.12*landing;squash=(1+(1-z)*.45,1+(1-z)*.45,z)
            arm_l=(0,.20+1.00*air,0);arm_r=(0,-.20-1.0*air,0)
            leg_l=(-.45*air,0,.15*air);leg_r=(.45*air,0,-.15*air)
            lean=(.08*anticipation,0,.06*air);head_rot=(-.08*air,.03*w,0)
            ear_gain=.26;smile='O' if clip=='Jump' else 'Open';eye_scales=[(1.18,1,1.17)]*2;blush=1.2
        elif clip=='Greeting':
            arm_r=(.12,-(1.6+.30*sin(6*pi*u))*pulse,.08*sin(6*pi*u)*pulse)
            arm_l=(0,.18*pulse,0);head_rot=(0,-.13*pulse,.16*pulse)
            lean=(0,-.07*pulse,-.04*pulse);blush=1.12;browtilts=[-.12,.08]
            eye_scales=[(1,1,1),(1,1,.45 if .38<u<.62 else 1)]
        elif clip=='Happy':
            lift=.14*(1-cos(p));arm_l=(0,.8*pulse,0);arm_r=(0,-.8*pulse,0)
            lean=(0,.10*w,.11*w);smile='Open';happy=True;blush=1.32;ear_gain=.16
            leg_l=(.15*w,0,.08*pulse);leg_r=(-.15*w,0,-.08*pulse)
        elif clip=='Thinking':
            pos_r=(.22,-.32,.96+.08*pulse);arm_r=(0,-.75*pulse,-.15*pulse)
            head_rot=(.07*pulse,-.20*pulse,.12*pulse);lean=(0,-.035*pulse,0)
            smile='Thought';eye_scales=[(.9,1,.58),(1,1,.84)];browtilts=[.24,-.20];blush=.83
        elif clip=='Celebration':
            lift=.38*(1-cos(p));squash=(1+.065*cos(p),1+.065*cos(p),1-.09*cos(p))
            arm_l=(.12,1.25+.18*w,0);arm_r=(-.12,-1.25+.18*w,0)
            leg_l=(.34*w,0,.22*pulse);leg_r=(-.34*w,0,-.22*pulse)
            lean=(0,.10*w,.16*w);head_rot=(0,.12*w,.12*w);smile='Open';happy=True;blush=1.42;ear_gain=.24
        elif clip=='Disappointed':
            lift=-.035*pulse;lean=(.16*pulse,0,0);head_rot=(.22*pulse,.06*w,0)
            arm_l=(.12,.02,0);arm_r=(.12,-.02,0);smile='Frown';eye_scales=[(1.1,1,.76)]*2;browtilts=[-.35,.35];blush=.68;ear_gain=.025
        elif clip=='Curious':
            head_rot=(0,.28*sin(p)*pulse,.22*pulse);lean=(0,-.07*pulse,-.06*pulse)
            arm_r=(0,-.45*pulse,0);smile='O';eye_scales=[(1.22,1,1.25),(.88,1,.82)];browtilts=[-.18,.22]
        elif clip=='ReturnToIdle':
            envelope=exp(-5*u);lift=.04*sin(p)*envelope
            lean=(0,.15*sin(p)*envelope,.12*sin(p)*envelope)
            squash=(1+.04*cos(p)*envelope,1+.04*cos(p)*envelope,1-.08*cos(p)*envelope)
            arm_l=(0,.3*envelope,0);arm_r=(0,-.3*envelope,0);ear_gain=.10*envelope
            eye_scales=[(1,1,.74)]*2
        tracks[root].append((frame+1,{'location':(x,0,lift),'rotation_euler':lean,'scale':squash}))
        tracks[body].append((frame+1,{'rotation_euler':bodyrot}))
        tracks[head].append((frame+1,{'rotation_euler':head_rot}))
        for o,rot,pos in [(left,arm_l,pos_l),(right,arm_r,pos_r),(legs[0],leg_l,leg_pos[0]),(legs[1],leg_r,leg_pos[1])]:
            tracks[o].append((frame+1,{'rotation_euler':rot,'location':pos}))
        for i,o in enumerate(ears):tracks[o].append((frame+1,{'rotation_euler':(ear_gain*sin(p-.45+i*.8),ear_gain*.65*sin(p-.8+i),ear_gain*.3*w)}))
        for i in range(2):
            tracks[eyes[i]].append((frame+1,{'scale':(.001,.001,.001) if happy else eye_scales[i]}))
            tracks[catch[i]].append((frame+1,{'scale':(.001,.001,.001) if happy else (1,1,1)}))
            tracks[happy_eyes[i]].append((frame+1,{'scale':(1,1,1) if happy else (.001,.001,.001)}))
            tracks[brows[i]].append((frame+1,{'rotation_euler':(0,browtilts[i],0),'scale':(1,1,1.08 if clip=='Curious' else .65)}))
            tracks[cheeks[i]].append((frame+1,{'scale':(blush,1,blush)}))
        for key,o in face.items():
            show=key==smile or (key=='Tongue' and smile=='Open')
            shape=(1.24,1,1.25) if clip=='Celebration' and key in ['Open','Tongue'] else (1.12,1,1) if clip=='Walk' else (.82,1,.75) if clip=='ReturnToIdle' else (1,1,1)
            tracks[o].append((frame+1,{'scale':shape if show else (.001,.001,.001)}))
    for o,keys in tracks.items():animation(o,clip,keys)
    bpy.context.scene.frame_end=max(bpy.context.scene.frame_end,end+1)
# Source stores all editable NLA tracks. Export uses the same names/samples, no decoder.
bpy.context.scene.frame_set(1)
src=ROOT/'assets/v0.4/source-blend/mascot-living.blend';dst=ROOT/'exports/v0.4/models/mascot-living.glb'
src.parent.mkdir(parents=True,exist_ok=True);dst.parent.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(src))
bpy.ops.export_scene.gltf(filepath=str(dst),export_format='GLB',export_yup=True,export_animations=True,export_animation_mode='NLA_TRACKS',export_nla_strips=True,export_force_sampling=True,export_optimize_animation_keep_anim_object=True,export_cameras=False,export_lights=False)
print('V04_MASCOT_SAVED',dst.stat().st_size,'clips',list(clips))
