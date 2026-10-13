"""Ceramic Seed Spirit: original geometry, editable source, six transform clips."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
from math import sin, cos, pi

reset()
M=materials()
root=empty('MascotRoot')
body=empty('BodyPivot',(0,0,0),root)
lathe('PearCeramicBody',[(.14,.16),(.2,.28),(.35,.4),(.55,.43),(.76,.4),(.92,.32),(1.0,.3)],M['jade'],48,body)
ring('ScallopedCollar',.35,.98,.033,M['cream'],waves=.024,parent=body)
ring('CollarBrassEdge',.35,1.005,.009,M['brass'],waves=.024,parent=body)
head=empty('HeadPivot',(0,0,1),body)
lathe('SeedHead',[(0,.29),(.13,.3),(.3,.25),(.44,.16),(.54,.055),(.57,.01)],M['jade'],48,head)
# Soft face, actual inset eyes and highlights, not a painted/generated image.
eyes=[]
for side in [-1,1]:
    eye=sphere('EyeLeft' if side<0 else 'EyeRight',(side*.125,-.257,.21),(.031,.021,.045),M['navy'],20,10,head)
    eyes.append(eye)
    sphere('EyeCatchlight',(side*.125-.008,-.277,.226),(.009,.006,.01),M['cream'],10,5,head)
    sphere('CoralBlush',(side*.195,-.232,.13),(.047,.012,.022),M['coral'],16,8,head)
path('Smile',[(-.034,-.302,.145),(0,-.31,.125),(.034,-.302,.145)],.009,M['navy'],head)
sphere('TinyBrassNose',(0,-.305,.175),(.017,.009,.012),M['brass'],12,6,head)
# One sculpted ceramic hollow-leaf ornament and one angular folded-paper leaf.
ear=empty('CeramicLeafPivot',(.15,0,.42),head)
shell=sphere('CeladonLeafShell',(0,0,.16),(.14,.065,.25),M['jade_dark'],24,12,ear)
shell.rotation_euler.y=-.3
inner=sphere('CeladonLeafInner',(-.01,-.048,.17),(.1,.02,.185),M['jade'],20,10,ear)
inner.rotation_euler.y=-.3
path('LeafBrassVein',[(-.03,-.065,.02),(-.05,-.072,.18),(-.1,-.06,.34)],.007,M['brass'],ear)
paper=empty('HanjiLeafPivot',(-.19,-.08,.4),head)
verts=[(0,0,0),(-.21,0,.3),(-.2,0,.45),(-.055,0,.35),(.055,0,.14),(-.08,-.052,.22),(-.08,.014,.22)]
faces=[(0,1,5),(1,2,5),(2,3,5),(3,4,5),(4,0,5),(1,0,6),(2,1,6),(3,2,6),(4,3,6),(0,4,6)]
faces=[tuple(reversed(face)) for face in faces]
mesh('FoldedHanjiLeaf',verts,faces,M['paper'],paper)
path('PaperLeafFold',[(0,-.006,0),(-.08,-.056,.22),(-.2,-.006,.45)],.004,M['brass'],paper)
# Brass growth seams and tiny inlaid blossom ornaments.
profile=[(.14,.16),(.2,.28),(.35,.4),(.55,.43),(.76,.4),(.92,.32),(1.0,.3)]
seam=[]
for i in range(25):
    z=.23+i/24*.61
    x=-.21+i/24*.45+.035*sin(i/24*pi*2)
    low,high=next((a,b) for a,b in zip(profile,profile[1:]) if a[0]<=z<=b[0])
    radius=low[1]+(high[1]-low[1])*(z-low[0])/(high[0]-low[0])
    y=-max(.0001,radius*radius-x*x)**.5-.007
    seam.append((x,y,z))
path('BodyGrowthSeam',seam,.008,M['brass'],body)
for cx,cz in [(-.22,.57),(.21,.35)]:
    for i in range(5):
        a=i/5*2*pi
        sphere('CeramicFlowerInlay',(cx+.035*cos(a),-.39,cz+.035*sin(a)),(.028,.01,.019),M['cream'],10,5,body)
    sphere('InlayHeart',(cx,-.409,cz),(.012,.008,.012),M['brass'],8,4,body)
arms=[]
for side in [-1,1]:
    arm=empty('ArmLeftPivot' if side<0 else 'ArmRightPivot',(side*.375,0,.77),body)
    sphere('CeramicMitten',(side*.055,-.01,-.12),(.11,.105,.2),M['jade'],24,12,arm)
    ring('MittenSeam',.07,-.24,.006,M['brass'],center=(side*.055,-.01),parent=arm)
    arms.append(arm)
    sphere('CeramicFoot',(side*.17,-.015,.11),(.125,.15,.105),M['jade_dark'],24,12,root)

clips=['Idle','Happy','Thinking','Celebration','Disappointed','Greeting']
frames=[1,16,31,46,61]
for clip in clips:
    root_keys=[]; head_keys=[]; left=[]; right=[]; leaf=[]
    for index,f in enumerate(frames):
        phase=(f-1)/60*2*pi
        wave=sin(phase)
        height=.014*(1-cos(phase))
        tilt=0; turn=.015*wave
        arm_l=.04*wave;arm_r=-.04*wave; head_tilt=.015*wave
        scale=(1,1,1)
        if clip=='Happy':
            height=.1*(1-cos(phase))
            arm_l=-.3*(1-cos(phase));arm_r=.3*(1-cos(phase))
            scale=(1+.02*cos(phase),1+.02*cos(phase),1-.02*cos(phase))
        elif clip=='Thinking':
            head_tilt=.16*sin(phase/2)
            arm_r=.9*sin(phase/2)
            turn=.2*sin(phase/2)
        elif clip=='Celebration':
            height=.18*(1-cos(phase))
            arm_l=-.8*sin(phase/2);arm_r=.8*sin(phase/2)
            turn=.16*wave
            scale=(1+.04*cos(phase),1+.04*cos(phase),1-.035*cos(phase))
        elif clip=='Disappointed':
            tilt=.13*sin(phase/2); head_tilt=.18*sin(phase/2)
            height=-.035*sin(phase/2)
            arm_l=.12*sin(phase/2);arm_r=-.12*sin(phase/2)
        elif clip=='Greeting':
            arm_r=(.95+.18*wave)*sin(phase/2)
            turn=.09*wave; head_tilt=-.05*sin(phase/2)
        root_keys.append((f,{'location':(0,0,height),'rotation_euler':(tilt,0,turn),'scale':scale}))
        head_keys.append((f,{'rotation_euler':(head_tilt,.025*wave,0)}))
        left.append((f,{'rotation_euler':(0,arm_l,0)}));right.append((f,{'rotation_euler':(0,arm_r,0)}))
        leaf.append((f,{'rotation_euler':(0,.04*wave,0)}))
    animation(root,clip,root_keys);animation(head,clip,head_keys)
    animation(arms[0],clip,left);animation(arms[1],clip,right)
    animation(paper,clip,leaf)
    for eye in eyes:
        animation(eye,clip,[(f,{'scale':(1,1,.18 if clip in ['Happy','Celebration'] and i==2 else 1)}) for i,f in enumerate(frames)])

lighting_camera(loc=(3,-6,3),target=(0,0,.95),orthoscale=2.75)
bpy.context.scene.render.resolution_x=800
bpy.context.scene.render.resolution_y=1000
save_export('mascot-base')
