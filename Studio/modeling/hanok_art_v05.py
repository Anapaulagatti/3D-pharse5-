"""Original courtyard dressing, roof craft and wind rigs for the verified v0.5 frame.
Called only by hanok-v05.py without --graybox. Graybox files stay untouched.
"""
import bpy, math, random
from math import sin,cos,pi
from common import material,mesh,path,cylinder,lathe,empty,join,animation,sphere
from reforge_materials import textured,surface_uv

def build_art(ctx):
 M=ctx['M'];B=ctx['B'];C=ctx['C'];P=ctx['P'];register=ctx['register'];xyz=ctx['xyz'];roof_h=ctx['roof_h']
 rng=random.Random(505);keep=[]
 for key,name,kind,h,seed in [
  ('wood','hanok-honeywood','wood','8A6249',51),('lightwood','hanok-lightwood','wood','BE9870',52),
  ('stone','hanok-warmstone','stone','C9C3AF',53),('paper','hanok-hanji','paper','EEE4CD',54),('ink','hanok-rooftile','tile','293C55',55)]:textured(M[key],name+'-v2',kind,h,seed)
 M['leaf']=material('V05_GardenSage','719A80',.9)
 M['glow']=material('V05_LanternHanjiGlow','FFE3AB',.86,emission=.8)
 M['haze']=material('V05_DistantTownHaze','8EA8AD',.95)
 M['haze2']=material('V05_DistantTownPale','B6C7C1',1)
 M['water']=material('V05_BasinWater','659D98',.28,.08)
 # Readable tile rolls and end caps; deliberately fewer than the structural rafters.
 for side,reach in [(-1,2.45),(1,3.30)]:
  for i in range(23):
   x=-3.82+7.64*i/22
   P('TileRoll',[(x,roof_h(-2.5+side*reach*j/12)+.025,-2.5+side*reach*j/12) for j in range(13)],.050,'ink','roof-detail')
   z=-2.5+side*reach
   o=cylinder('CarvedTileEnd',xyz((x,roof_h(z)+.012,z+side*.028)),.058,.045,M['ink'],10);o.rotation_euler.x=pi/2;register(o,'roof-detail')
   if i%2==0:
    o=sphere('CeladonTileSeal',xyz((x,roof_h(z)+.012,z+side*.055)),(.022,.009,.022),M['jade'],8,4);register(o,'roof-detail')
  for j in [3,6,9]:
   z=-2.5+side*reach*j/12
   P('TileCourseSeam',[(-3.8,roof_h(z)+.022,z),(3.8,roof_h(z)+.022,z)],.006,'lightwood','roof-detail')
 for side in [-1,1]:
  P('LiftedRidgeCrest',[(side*3.6,4.18,-2.5),(side*3.82,4.24,-2.5),(side*3.92,4.34,-2.5)],.045,'jade','roof-detail')
  C('CrestBrassBud',(side*3.92,4.34,-2.5),.043,.075,'brass','roof-detail')
 # Restrained carved/painted joinery, large enough to read at the hero camera.
 for z in [-4.4,-.6,.25]:
  for x in [-3.2,-1.1,1.1,3.2]:
   for side in [-1,1]:
    B('JoineryCorbel',(x+side*.13,2.71,z),(.26,.075,.30),'lightwood','joinery')
    B('JoineryCoralBand',(x+side*.10,2.76,z-.11),(.18,.035,.025),'coral','joinery',bevel=.004)
   o=cylinder('VisibleTenonPeg',xyz((x,2.78,z+.115)),.031,.024,M['brass'],8);o.rotation_euler.x=pi/2;register(o,'joinery')
 for z in [-.6,.25]:
  B('DancheongCeladonLine',(0,2.81,z+.11),(6.25,.035,.025),'jade','joinery',bevel=.004)
  for x in [-2.1,0,2.1]:
   P('BeamCloudCarving',[(x-.23,2.70,z+.12),(x-.16,2.65,z+.12),(x,2.61,z+.12),(x+.16,2.65,z+.12),(x+.23,2.70,z+.12)],.018,'lightwood','joinery')
 # Paving tops are2mm above the outdoor support plane, with natural asymmetry.
 for row,z in enumerate([3.45,2.65,1.87,1.10,.35]):
  for col,x in enumerate([-4.9,-4.08,-3.26,-2.44,-1.62,-.80,0,.80,1.62,2.44,3.26,4.08,4.9]):
   if x< -3.2 and z<2.2 or x>3.6 and z<1.8:continue
   o=B('CourtyardCraftSlab',(x+rng.uniform(-.025,.025),-.018,z+rng.uniform(-.025,.025)),(.74,.040,.69),'stone' if (col+row)%4 else 'paper','paving',bevel=.022)
   o.rotation_euler.z=rng.uniform(-.018,.018)
 # Outer low borders make the finite courtyard visually legible; rear route remains >1m.
 for x in [-5.94,5.94]:B('SideGardenBoundary',(x,.065,-.7),(.10,.13,9.85),'stone','border',True,bevel=.018)
 B('RearGardenBoundary',(0,.065,-5.64),(11.78,.13,.10),'stone','border',True,bevel=.018)
 for x in [-3.45,3.45]:B('FrontGardenBoundary',(x,.065,4.20),(4.65,.13,.10),'stone','border',True,bevel=.018)
 # Original folded five-petal blossoms. A whole flower is one small mesh, not five spheres.
 def flower(name,c,r,mat,parent=None):
  verts=[];faces=[]
  for k in range(5):
   a=k*2*pi/5;start=len(verts)
   pts=[(0,0,0),(.55*r*cos(a-.55),.55*r*sin(a-.55),.015),
        (r*cos(a),r*sin(a),.045),(.55*r*cos(a+.55),.55*r*sin(a+.55),.015),(.54*r*cos(a),.54*r*sin(a),.065)]
   verts.extend([xyz((c[0]+x,c[1]+h,c[2]+z)) for x,z,h in pts]);faces.extend([tuple(start+i for i in tri) for tri in [(0,1,4),(1,2,4),(2,3,4),(3,0,4)]])
  start=len(verts);verts.append(xyz((c[0],c[1]+.045,c[2])))
  for k in range(10):verts.append(xyz((c[0]+.024*cos(k*pi/5),c[1]+.05,c[2]+.024*sin(k*pi/5))))
  faces.extend([(start,start+1+k,start+1+(k+1)%10) for k in range(10)])
  o=mesh(name,verts,faces,mat,parent);o.data.materials.append(M['brass'])
  for p in list(o.data.polygons)[-10:]:p.material_index=1
  return o
 def leaf(c,r,a,parent=None):
  x,y,z=c;v=[(x,y,z),(x+r*.45*cos(a-.6),y+.01,z+r*.45*sin(a-.6)),(x+r*cos(a),y+.06,z+r*sin(a)),(x+r*.45*cos(a+.6),y+.01,z+r*.45*sin(a+.6)),(x+r*.45*cos(a),y+.10,z+r*.45*sin(a))]
  return mesh('FoldedSageLeaf',[xyz(p) for p in v],[(0,1,4),(1,2,4),(2,3,4),(3,0,4)],M['leaf'],parent)
 B('PlumPlantingBed',(-4.42,.055,1.12),(2.00,.11,2.05),'earth','garden',True,bevel=.08)
 for i in range(12):
  a=i*pi/6;x=-4.42+.96*cos(a);z=1.12+.98*sin(a)
  o=sphere('GardenBorderRock',xyz((x,.11,z)),(.13,.09,.11),M['stone'],8,4);register(o,'garden')
 P('PlumTrunk',[(-4.42,.06,.98),(-4.43,.70,1.01),(-4.30,1.32,1.04),(-4.44,1.90,1.10)],.085,'wood','garden')
 for i in range(6):
  a=i*2.4;P('PlumSupportingBranch',[(-4.36,1.20,1.04),(-4.40+.35*cos(a),1.58,1.03+.25*sin(a)),(-4.40+.68*cos(a),1.95+(i%2)*.20,1.03+.55*sin(a))],.026,'wood','garden')
 for i,center in enumerate([(-4.91,1.95,1.15),(-3.93,2.12,1.18),(-4.43,2.43,.85)]):
  pivot=empty('PlumWind'+str(i),xyz(center));keep.append(pivot)
  for detail,count in [(False,7),(True,4)]:
   parts=[]
   for j in range(count):
    a=j*2.4+i;rad=.15+.34*rng.random();c=(rad*cos(a),rng.uniform(-.12,.10),rad*sin(a)*.75)
    parts.append(flower('PlumBlossom',c,.14+.035*rng.random(),M['paper' if j%3 else 'coral'],pivot))
    parts.append(leaf((c[0],c[1]-.06,c[2]),.23,a,pivot))
   crown=join(('PlumDetail' if detail else 'PlumCore')+str(i),parts);crown.parent=pivot;register(crown,'foliage')
  animation(pivot,'GardenWind',[(f,{'rotation_euler':(.045*sin((f-1)/120*2*pi+i),.035*sin((f-1)/120*2*pi+i*.7),.025*cos((f-1)/120*2*pi+i))}) for f in range(1,122,15)])
 # Ground planting and glazed vessels, deliberately outside the central walking line.
 for i,(x,z) in enumerate([(-2.4,.9),(2.4,.85),(-5.05,3.35),(4.65,3.30),(4.85,-3.95),(-4.75,-4.15)]):
  o=lathe('CeladonGardenVessel',[(0,.13),(.04,.22),(.28,.24),(.40,.18),(.41,.16),(.34,.15)],M['jade'],16);o.location=xyz((x,.005,z));register(o,'planter')
  B('PlanterCollision',(x,.20,z),(.42,.40,.42),'jade','collision-proxy',True,bevel=.04).hide_render=True
  for j in range(5):
   register(leaf((x,.35,z),.27,j*2*pi/5+i),'plant')
  register(flower('PlanterBlossom',(x,.49,z),.12,M['paper' if i%2 else 'coral']),'plant')
 for x,z in [(-4.85,2.0),(-3.90,1.90),(4.75,2.8),(5.15,-2.6)]:
  for j in range(4):
   c=(x+rng.uniform(-.22,.22),.03,z+rng.uniform(-.22,.22));register(leaf(c,.20,j*2),'plant');register(flower('GroundFlower',(c[0],.11,c[2]),.09,M['paper' if j%2 else 'coral']),'plant')
 # A quiet bench and tea vignette; genuine small furniture supports storytelling.
 B('GardenBenchTop',(-4.40,.43,-.62),(1.1,.09,.44),'lightwood','furniture',True,bevel=.03)
 for x in [-4.79,-4.01]:B('BenchFoot',(x,.23,-.62),(.10,.40,.32),'wood','furniture')
 B('BenchFoldedCushion',(-4.61,.51,-.62),(.35,.08,.35),'paper','detail',bevel=.035)
 B('BenchLetter',(-4.13,.49,-.62),(.22,.02,.18),'paper','detail',bevel=.003)
 # Stone basin is ornamental/collidable; no unsupported walkable water/bridge surface.
 o=lathe('CarvedStoneBasin',[(0,.30),(.08,.39),(.34,.42),(.41,.40),(.41,.35),(.30,.32)],M['stone'],24);o.location=xyz((4.43,.005,.73));register(o,'basin')
 B('BasinCollider',(4.43,.20,.73),(.82,.40,.82),'stone','collision-proxy',True,bevel=.07).hide_render=True
 water=C('BasinWater',(4.43,.345,.73),.335,.018,'water','water');keep.append(water)
 for r in [.09,.16,.24]:
  ripple=P('BasinRipple',[(4.43+r*cos(j*pi/12),.355,.73+r*sin(j*pi/12)) for j in range(25)],.003,'paper','water');ripple.parent=None;keep.append(ripple)
  bpy.ops.object.select_all(action='DESELECT');ripple.select_set(True);bpy.context.view_layer.objects.active=ripple;bpy.context.scene.cursor.location=xyz((4.43,.355,.73));bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
 # Four real, restrained wind-driven lanterns. Poles/frame have visible attachments.
 for i,(x,z,h) in enumerate([(-1.25,3.45,1.60),(1.25,3.45,1.60),(-3.70,-.20,1.85),(3.85,-.15,1.85)]):
  C('LanternFoot',(x,.09,z),.14,.18,'stone','lantern-support')
  C('LanternPost',(x,(h+.08)/2,z),.035,h-.08,'wood','lantern-support',True)
  B('LanternArm',(x+.16,h,z),(.38,.055,.055),'wood','lantern-support')
  pivot=empty('LanternSwing'+str(i),xyz((x+.30,h,z)));keep.append(pivot);pieces=[]
  pieces.append(path('LanternHangingTie',[xyz((0,0,0)),xyz((0,-.06,0))],.006,M['brass'],pivot))
  pieces.append(cylinder('LanternHanji',xyz((0,-.22,0)),.12,.32,M['glow'],10,parent=pivot))
  for y in [-.055,-.385]:pieces.append(cylinder('LanternBrassRim',xyz((0,y,0)),.145,.035,M['brass'],10,parent=pivot))
  for k in range(5):
   a=k*2*pi/5;pieces.append(path('LanternTimberRib',[xyz((.13*cos(a),-.06,.13*sin(a))),xyz((.13*cos(a),-.39,.13*sin(a)))],.007,M['wood'],pivot))
  lantern=join('InteractiveLantern'+str(i),pieces);lantern.parent=pivot;register(lantern,'lantern')
  animation(pivot,'LanternBreeze',[(f,{'rotation_euler':(.065*sin((f-1)/90*2*pi+i),.04*cos((f-1)/90*2*pi+i),0)}) for f in range(1,92,15)])
 B('BannerMountingRod',(0,2.79,-.35),(.86,.035,.035),'brass','banner')
 for x in [-.33,.33]:B('BannerStandoff',(x,2.79,-.475),(.018,.04,.25),'wood','banner')
 banner=empty('PaperBannerWind',xyz((0,2.80,-.35)));keep.append(banner)
 B('FoldedWelcomeBanner',(0,-.15,0),(.76,.30,.018),'paper','banner',parent=banner,bevel=.004)
 fold=path('BannerBrassFold',[xyz((-.35,-.02,-.02)),xyz((0,-.14,-.03)),xyz((.35,-.02,-.02))],.008,M['brass'],banner);register(fold,'banner')
 animation(banner,'BannerWind',[(f,{'rotation_euler':(.04*sin((f-1)/120*2*pi),.018*cos((f-1)/120*2*pi),0)}) for f in range(1,122,15)])
 # Separate muted historic roof silhouettes: outside the playable courtyard, hideable
 # in architecture inspection so no scenery conceals the fully built rear facade.
 town=empty('DistantTownBackdrop');keep.append(town);parts=[]
 for i in range(8):
  x=-5.1+i*1.47;z=-7.4-(i%3)*.75;h=.58+.18*(i%3);w=1.30;d=.8
  o=B('FarHouse',(x,-.56+h/2,z),(w,h,d),'haze' if i%2 else 'haze2','backdrop',bevel=.015);parts.append(o)
  v=[xyz((x+a,-.56+h+b,z+c)) for a,b,c in [(-w*.60,0,-d*.65),(w*.60,0,-d*.65),(w*.60,0,d*.65),(-w*.60,0,d*.65),(-w*.60,.32,0),(w*.60,.32,0)]]
  o=mesh('FarGableRoof',v,[(0,1,5,4),(4,5,2,3),(0,4,3),(1,2,5),(0,3,2,1)],M['haze']);parts.append(o)
 backdrop=join('DistantTownHouses',parts);backdrop.parent=town
 for o in list(bpy.context.scene.objects):
  if o.type=='MESH':surface_uv(o)
 return {'keep':keep,'hide_meshes':[o for o in bpy.context.scene.objects if o.type=='MESH' and o.hide_render],
         'art_direction':'Original Joseon fantasy courtyard; muted historic roof silhouettes, not a new district','maps':'Original v0.5 procedural packed PBR maps'}
