"""Read-only canonical masks and metadata -> separate NPC bindings. Never writes world data."""
from pathlib import Path
import json,sys,math,hashlib,heapq
import numpy as np
from scipy.ndimage import minimum_filter1d
from art import SPECS
from dialogue_copy import COPY
R=Path(__file__).resolve().parents[2];S=R/'assets-src/npcs/phase3a';D=R/'docs/phase3a';m=json.loads((R/'public/assets/gate3/palace-cleanup-world/manifest.json').read_text());w,h=m['size'];field=np.zeros((h,w),np.uint8)
for c in m['chunks']:field[c['y']:c['y']+c['height'],c['x']:c['x']+c['width']]=np.fromfile(R/'public'/c['mask'],np.uint8).reshape(c['height'],c['width'])
for o in m['logicalSolids']:
 x,y,ww,hh=o['rect'];field[math.floor(y):math.ceil(y+hh),math.floor(x):math.ceil(x+ww)]=0
clear=minimum_filter1d(minimum_filter1d(field,size=29,axis=1,mode='constant'),size=9,axis=0,mode='constant')>127
PLAN={
 'seoyeon':([2190,940],[40,28],'production/palace','front'),'daehyun':([1870,945],[40,28],'production/gate','right'),
 'minseo':([650,2620],[32,10],'cafe','front'),'jiho':([1215,2620],[32,10],'bookshop','front'),
 'eunji':([2440,2660],[36,30],'station','front'),'junho':([2810,2690],[38,24],'station','back'),
 'harin':([3740,4070],[32,12],'tangerine-orchard','right'),'seojun':([3740,4396],[32,12],'production/jeju-culture','left'),
 'nayeon':([574,550],[10,50],'farmMetadata','right'),'cheolsu':([500,810],[32,24],'farmMetadata','back'),
 'yejin':([1510,3260],[32,24],'production/tower','left'),'sungmin':([2320,3280],[32,20],'production/carousel','back'),
 'donghae':([1630,3860],[36,16],'production/market','front'),'soobin':([2840,3760],[32,20],'production/ferry','front')}
def segment(a,b):
 n=max(1,math.ceil(math.dist(a,b)));return all(clear[round(a[1]+(b[1]-a[1])*i/n),round(a[0]+(b[0]-a[0])*i/n)]for i in range(n+1))
def routeFor(id):
 (x,y),(ww,hh),ref,d=PLAN[id];offsets=sorted([(dx*dx+dy*dy,dx,dy)for dx in range(-36,37,2)for dy in range(-36,37,2)])
 for _,dx,dy in offsets:
  xx=x+dx;yy=y+dy;pts=[[xx,yy],[xx+ww,yy],[xx+ww,yy+hh],[xx,yy+hh]]
  if all(segment(a,b)for a,b in zip(pts,pts[1:]+pts[:1])):return pts,{'requested':[x,y],'localizedOffset':[dx,dy],'sourceAnchor':ref,'reason':'Native full29x9footprint on actual canonical mask; no world/collision edits'}
 raise ValueError('No verified native route for '+id)
def approach(route):
 x,y=route[0]
 # Authoritative ground chooses an open approach on the SAME local connected surface.
 choices=[]
 for dx,dy in [(0,156),(0,-156),(-156,0),(156,0),(112,112),(-112,112),(112,-112),(-112,-112)]:
  end=[x+dx,y+dy]
  if segment([x,y],end):choices.append((int(dy<0)*10+int(dx!=0),end))
 if not choices:
  for dx in range(-160,161,8):
   for dy in range(-160,161,8):
    if 120<=math.hypot(dx,dy)<=170 and segment([x,y],[x+dx,y+dy]):choices.append((abs(dx)+abs(dy),[x+dx,y+dy]))
 if not choices:raise ValueError('No real player approach '+str(route[0]))
 return min(choices)[1]
records=[];proof=[];dialogues=[]
for spec in SPECS:
 id,ko,vi,zone,job,*_=spec;route,p=routeFor(id);p['id']='npc-'+id;p['route']=route;p['reviewSpawn']=approach(route);proof.append(p);clipsPath=S/id/'clips.json';clips=json.loads(clipsPath.read_text())if clipsPath.exists()else{};records.append({'id':'npc-'+id,'names':{'vi':vi,'ko':ko},'occupation':job,'homeZone':zone,'spawn':route[0],'interactionPosition':route[0],'reviewSpawn':p['reviewSpawn'],'direction':PLAN[id][3],'footprint':[14,4],'route':route,'idleBehavior':spec[-1],'walkSpeed':36+(SPECS.index(spec)%3)*2,'interactionRadius':92,'assets':{'texture':f'assets/npcs/phase3a/npc-{id}/atlas.png','atlas':f'assets/npcs/phase3a/npc-{id}/atlas.json','key':'npc-'+id},'animations':clips,'dialogueId':'npc-'+id+'-welcome','future':{'questProviderId':None,'shopProviderId':None,'learningTopicTags':[zone,'greetings',spec[-1]]}})
 for i,(koText,viText)in enumerate(COPY[id]):
  name='welcome'if i==0 else'place'if i==1 else'care';node={'id':f'npc-{id}-{name}','npcId':'npc-'+id,'content':{'ko':koText,'vi':viText},'hint':{'vi':job+' · '+vi,'ko':ko},'choices':[],'next':None,'conditions':[],'futureQuestHook':None,'lessonTopicTags':[zone,'greetings']}
  if i==0:node['choices']=[{'id':'place','label':{'vi':'Tìm hiểu nơi này','ko':'이곳에 대해 알려 주세요.'},'next':f'npc-{id}-place'},{'id':'care','label':{'vi':'Có điều gì cần lưu ý?','ko':'주의할 점이 있나요?'},'next':f'npc-{id}-care'}]
  if i==1:node['next']=f'npc-{id}-care'
  dialogues.append(node)
full='full'in sys.argv;pilot={'seoyeon','minseo','harin','eunji'};selected=[r for r in records if full or r['id'][4:]in pilot];assert all(r['animations']for r in selected),'Generate only the current wave artwork first'
(S/'registry.json').write_text(json.dumps({'schemaVersion':1,'worldId':m['id'],'npcs':selected},ensure_ascii=False,indent=2)+'\n');(S/'planned-bindings.json').write_text(json.dumps({'npcs':records},ensure_ascii=False,indent=2)+'\n');(S/'dialogues.json').write_text(json.dumps({'schemaVersion':1,'nodes':[n for n in dialogues if full or n['npcId'][4:]in pilot]},ensure_ascii=False,indent=2)+'\n');(D/'navigation-source-qa.json').write_text(json.dumps({'worldId':m['id'],'maskPolicy':'Original masks/logical solids; conservative whole29x9NPC native contact; every integer pixel along every route and review approach validated','changedWorldFiles':[],'routes':proof,'activeWave':'full14'if full else'pilot4'},ensure_ascii=False,indent=2)+'\n');print('PASS',len(proof),'planned native routes;active',len(selected))
for p in proof:print(p['id'],p['route'][0],p['localizedOffset'],p['reviewSpawn'])
