"""Gate2 isolated scene compiler. No approved plan/source edits, no media generation."""
from pathlib import Path
import json,hashlib,subprocess,shutil,sys
from PIL import Image,ImageDraw,ImageFilter
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate2';P=R/'public/assets/gate2';C=R/'.cache/gate2';F=Path('/workspace/tooling-cache/agent-sprite-forge/skills');P.mkdir(exist_ok=True);C.mkdir(exist_ok=True);(S/'native').mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda p,o:p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
logs=[]
def run(*args):
 p=subprocess.run(list(map(str,args)),cwd=R,capture_output=True,text=True);logs.append({'command':list(map(str,args)),'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr});write(S/'processing-log.json',logs);assert p.returncode==0,p.stderr or p.stdout
if '--finish' in sys.argv:
 # Source pixels stay1:1 except the explicitly supersampled square station, finished to native720.
 for n in ['north','jeju','transition']:shutil.copy2(S/'originals'/('jeju-culture-corrected.png' if n=='jeju' else f'{n}.png'),S/'native'/f'{n}.png')
 run('python3',F/'generate2dmap/scripts/conform_background.py','conform','--input',S/'originals/station.png','--size','720x720','--mode','cover','--resampler','box','--strict','--output-dir',C/'station-background-finish')
 shutil.copy2(C/'station-background-finish/background.png',S/'native/station.png')
 run('python3',F/'generate2dsprite/scripts/palette_tool.py','build','--input',S/'native','--colors','255','--balance','--name','Gate2-Muneum-compatible','--output-dir',C/'palette')
 run('python3',F/'generate2dsprite/scripts/palette_tool.py','apply','--input',S/'native','--palette',C/'palette/palette.json','--alpha-threshold','128','--output-dir',C/'pixel-finished')
 for f in (C/'pixel-finished').glob('*.png'):shutil.copy2(f,S/'native'/f.name)
 shutil.copy2(C/'palette/palette.json',S/'palette.json')
scenes=[];world=json.loads((R/'assets-src/world-gate1/plan.json').read_text())
def scene(id,label,src,spawn,camera):
 folder=P/id;folder.mkdir(exist_ok=True);image=Image.open(src).convert('RGBA');image.save(folder/'ground.png');w,h=image.size
 return dict(id=id,label=label,size=[w,h],spawn=spawn,camera=camera,ground=f'{id}/ground.png',mask=f'{id}/walk.png',objects=[],targets=[],routes=[],walkAreas=[],solids=[],source=str(src.relative_to(R)),sourceSha256=sha(src),depthPolicy='Native semantic masks / support roots Y-sorted; same RGB as base art')
def area(s,rect):s['walkAreas'].append(rect)
def route(s,name,points,width=80):s['routes'].append(dict(id=name,points=points,width=width))
def target(s,id,x,y,label):s['targets'].append(dict(id=id,x=x,y=y,label=label))
def solid(s,rect,reason):s['solids'].append(dict(rect=rect,reason=reason))
def overlay(s,name,poly,root,green=False):
 image=Image.open(P/s['id']/'ground.png').convert('RGBA');mask=Image.new('L',image.size);ImageDraw.Draw(mask).polygon(poly,fill=255)
 if green:
  import numpy as np
  a=np.asarray(image);m=np.asarray(mask).copy();keep=((a[:,:,1].astype(float)>a[:,:,2]*1.4)&(a[:,:,1]>60)&(a[:,:,0]<230))|((a[:,:,0]>140)&(a[:,:,1]>70)&(a[:,:,1]<190)&(a[:,:,2]<80));m[~keep]=0;mask=Image.fromarray(m)
 box=mask.getbbox();assert box;crop=image.crop(box);crop.putalpha(mask.crop(box));file=f'{name}.png';crop.save(P/s['id']/file);s['objects'].append(dict(id=name,image=f"{s['id']}/{file}",x=box[0],y=box[1],width=crop.width,height=crop.height,sortY=root,alphaSoftening=.65))
a=scene('a','A · Palace / hanok courtyard',S/'native/north.png',[1100,790],[1000,650]);a['registration']={'approvedWorldOrigin':[640,650],'scale':1,'approvedBuildingAndWallCollidersRetained':True}
for b in world['buildings']:
 if b['kind']=='heritage':x,y,w,h=b['rect'];x-=640;y-=650
 else:continue
 if x<1536 and x+w>0 and y<1024 and y+h>0:solid(a,[x,y,w,h],'Approved historic '+b['id'])
for b in world['boundaries']:
 x,y,w,h=b['rect'];solid(a,[x-640,y-650,w,h],'Approved '+b['id'])
area(a,[0,720,1536,160]);area(a,[1240,90,280,934]);area(a,[80,710,300,160]);area(a,[560,710,360,160])
route(a,'academy-entrance',[[1100,790],[160,790],[160,750]],96);route(a,'tea-entrance',[[1100,790],[730,790],[730,750]],96);route(a,'palace-gate',[[1100,790],[1408,790],[1408,440],[1408,290]],96)
for row in [('academy',160,750,'Hanok academy'),('tea',730,750,'Tea courtyard'),('palace',1408,290,'Palace entrance')]:target(a,*row)
overlay(a,'foreground-pine',[(0,760),(390,760),(535,850),(500,1024),(0,1024)],1000,True)
overlay(a,'tea-roof',[(550,445),(655,395),(810,410),(960,460),(940,540),(900,650),(580,660)],710)
scenes.append(a)
b=scene('b','B · Muneum commercial street',R/'assets-src/gate1/native/street-foundation.png',[192,590],[850,540]);area(b,[0,0,1536,1024]);old=json.loads((R/'assets-src/gate1/map/bundle.json').read_text())
for v in old['collision']['solids']:solid(b,[v['x'],v['y'],v['w'],v['h']],v.get('reason','Approved Muneum physical support'))
for v in json.loads((R/'assets-src/gate1/map/venues.json').read_text()):target(b,v['id'],v['x'],v['y'],v['label'])
route(b,'street',[[192,590],[1288,590]],50);route(b,'crossing',[[992,590],[992,928],[1120,928]],56)
for o in old['objects']:
 if o['prop']=='architecture':continue
 p=old['props'][o['prop']];src=R/'assets-src/gate1/map'/p['image'];dst=P/'b'/('prop-'+p['image']);shutil.copy2(src,dst);im=Image.open(src);anchor=p['anchor_px'];b['objects'].append(dict(id=o['id'],image='b/'+dst.name,x=o['x']-anchor[0],y=o['y']-anchor[1],width=im.width,height=im.height,sortY=o['sortY'],alphaSoftening=.65))
scenes.append(b)
c=scene('c','C · Jeju / volcanic coast',S/'native/jeju.png',[320,855],[540,850]);c['reservation']='CONFLICT: native1024x1536 study exceeds approved720x1260; separate localized proposal, approved map unchanged'
route(c,'ferry-arrival',[[20,820],[170,840],[320,855],[540,865]],76)
route(c,'main-coast',[[320,410],[412,450],[520,630],[545,750],[540,865],[605,880],[630,940],[650,1050],[650,1210],[500,1290],[410,1300],[410,1210]],72)
route(c,'bridge-arrival',[[20,360],[165,390],[320,410]],66)
route(c,'oreum-approach',[[412,450],[405,340],[430,260],[480,190],[550,135]],62)
route(c,'oreum-rim',[[550,135],[675,105],[815,150],[880,230],[875,310],[800,365],[680,390],[550,350],[470,265],[480,190]],62)
route(c,'oreum-descent',[[800,365],[750,420],[740,480],[700,540],[630,590],[520,630]],62)
route(c,'orchard',[[540,865],[605,880],[900,880],[900,1005],[630,1005],[630,1010]],58)
area(c,[270,1180,320,65]);route(c,'cultural-stairs',[[410,1300],[410,1210],[410,1190]],66)
for row in [('arrival',320,855,'Jeju ferry landing · future crossing'),('basalt',460,570,'Basalt coastal exploration'),('oreum',550,135,'Oreum rim lookout'),('orchard',780,880,'Tangerine orchard'),('culture',410,1210,'Jeju stone culture pavilion')]:
 if row[0]=='basalt':route(c,'basalt-stop',[[412,450],[460,570],[520,630]],64)
 target(c,*row)
solid(c,[220,960,390,210],'Painted cultural pavilion ground contact')
for i,(x,y)in enumerate([(650,815),(755,815),(865,815),(650,925),(755,925),(865,925)]):
 overlay(c,f'tangerine-{i}',[(x-43,y-50),(x+43,y-50),(x+47,y+30),(x-40,y+35)],y+40,True)
 solid(c,[x-6,y+32,12,10],'Tangerine trunk only, canopy remains walk-behind')
overlay(c,'cultural-roof',[(205,1000),(300,900),(500,900),(620,1030),(590,1100),(220,1100)],1170)
scenes.append(c)
t=scene('transition','Transition · heritage garden to city',S/'native/transition.png',[850,630],[850,520]);area(t,[0,600,1536,155]);area(t,[0,900,1536,124]);area(t,[935,660,150,364]);route(t,'heritage-door',[[850,630],[480,630],[480,560],[480,480]],80)
route(t,'city-door',[[850,630],[1100,630]],74);route(t,'crosswalk',[[1010,630],[1010,940],[1150,940]],90)
for row in [('heritage',480,560,'Traditional threshold'),('garden',850,630,'Shared stone / planted transition'),('modern',1100,630,'Modern bookshop frontage')]:target(t,*row)
solid(t,[0,0,650,305],'Historical architecture');solid(t,[920,0,616,600],'Modern frontage');solid(t,[330,300,290,215],'Traditional gate piers and roof; door approach south')
overlay(t,'garden-canopy',[(560,150),(920,150),(935,430),(755,530),(570,390)],575,True);scenes.append(t)
s=scene('station','Station · native architectural scale study',S/'native/station.png',[360,460],[360,330]);area(s,[0,415,720,140]);area(s,[0,560,720,160]);area(s,[255,440,140,280]);area(s,[645,300,70,160]);solid(s,[84,190,555,220],'Measured station ground footprint after uniform authoring finish')
route(s,'station-entrance',[[360,460],[360,430]],70);route(s,'forecourt-crossing',[[360,460],[360,650]],84);target(s,'station',360,430,'한빛역 · station ticket hall');target(s,'forecourt',360,650,'Station forecourt / crossing');s['authoringScale']=720/1254;s['measuredDoorHeightPx']=120;s['footprintFit']=[555,220];scenes.append(s)
for s in scenes:
 w,h=s['size'];mask=Image.new('L',(w,h));d=ImageDraw.Draw(mask)
 for x,y,ww,hh in s['walkAreas']:d.rectangle((x,y,x+ww,y+hh),fill=255)
 for route_ in s['routes']:
  pts=[tuple(pt) for pt in route_['points']];d.line(pts,fill=255,width=route_['width'],joint='curve')
  rr=route_['width']/2
  for x,y in pts:d.ellipse((x-rr,y-rr,x+rr,y+rr),fill=255)
 for so in s['solids']:
  x,y,ww,hh=so['rect'];d.rectangle((x,y,x+ww,y+hh),fill=0)
 mask=mask.filter(ImageFilter.MinFilter(17));mask.save(P/s['id']/'walk.png')
 # Technical collision cells from the exact walk mask, conservatively at8px pitch.
 blocked=[]
 for y in range(0,h,8):
  start=None
  for x in range(0,w+8,8):
   off=x>=w or mask.getpixel((min(x+4,w-1),min(y+4,h-1)))<128
   if off and start is None and x<w:start=x
   if not off and start is not None:blocked.append(dict(shape='rect',x=start,y=y,w=x-start,h=8));start=None
   if x>=w and start is not None:blocked.append(dict(shape='rect',x=start,y=y,w=w-start,h=8));start=None
 folder=S/'maps'/s['id'];folder.mkdir(parents=True,exist_ok=True);shutil.copy2(P/s['id']/'ground.png',folder/'ground.png')
 bundle=dict(schema='generate2dmap.map_bundle.v2',id='gate2-'+s['id'],world=dict(width=w,height=h,unit='px'),art_source='existing'if s['id']=='b'else'host_image',layers=[dict(name='authored-foundation',kind='image',image='ground.png',x=0,y=0)],props={},objects=[],collision=dict(actorRadius=0,ySquash=1,solids=blocked),spawns=[dict(id='entry',x=s['spawn'][0],y=s['spawn'][1],facing='front')],anchors={v['id']:dict(point=[v['x'],v['y']],approach=[v['x'],v['y']])for v in s['targets']})
 write(folder/'bundle.json',bundle);write(P/s['id']/'scene.json',s)
write(P/'catalog.json',[dict(id=s['id'],label=s['label'])for s in scenes]);write(S/'scenes.json',scenes)
write(S/'native-provenance.json',[dict(id=s['id'],size=s['size'],source=s['source'],sha256=s['sourceSha256'],spatialScale=s.get('authoringScale',1),doorTarget=120 if s['id']=='station' else 100)for s in scenes])
print(json.dumps({'scenes':len(scenes),'noApprovedPlanEdit':True,'jejuFit':'CONFLICT_REPORTED','stationAuthoringScale':720/1254}))
