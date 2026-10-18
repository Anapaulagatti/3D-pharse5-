"""Editable SCHEMATIC zoning only, never runtime game artwork."""
from pathlib import Path
import json,math,collections
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1];D=R/'docs/living-korea';D.mkdir(exist_ok=True)
plan={'schema':'korean-arena.living-korea.masterplan.v1','fictionalGeography':True,'nativeActorHeight':80,'walk':60,'run':100,'activeIncrement':'north-repair + Namsan only','destinations':[
 {'id':'heritage','name':'Royal heritage & cultural street','state':'northern repair candidate','world':[2304,2240],'arrival':[1152,832],'travel':[1152,2080],'routes':[[[1152,832],[1152,1440],[1120,1664],[1152,1888],[1152,2080]],[[512,1872],[800,1920],[1152,2080]],[[1984,2032],[1640,2016],[1456,2080],[1152,2080]]],'landmarks':[{'id':'palace','rect':[384,64,1536,672],'label':'Royal court / main hall'},{'id':'academy','rect':[192,928,704,544],'label':'U-courtyard academy'},{'id':'workshop','rect':[1480,832,744,608],'label':'L-workshop / instruments'},{'id':'museum','rect':[1696,1696,544,224],'label':'Museum + open frontage'},{'id':'book-cafe','rect':[352,1680,320,144],'label':'Book & tea / culture transition'}],'transition':['granite ceremonial avenue','earth hanok paths','silver-stone cultural lane','contemporary transit garden']},
 {'id':'namsan','name':'Namsan-inspired Hill of Letters','state':'first playable increment, pending art review','world':[1408,1280],'arrival':[704,1056],'travel':[704,1120],'routes':[[[704,1120],[704,1024],[512,960],[384,816],[416,688],[576,688],[704,752],[832,752],[832,672]],[[704,1024],[928,1056],[1120,928],[1056,880],[992,864],[832,784],[832,752]]],'landmarks':[{'id':'tower','rect':[664,536,336,96],'label':'Original observation tower'},{'id':'overlook','rect':[976,688,288,128],'label':'View terrace / telescope','walkable':True},{'id':'arrival','rect':[544,1056,320,128],'label':'Park / travel gateway'}],'identity':['white shaft + turquoise observation disc + antenna','stone retaining terraces and wooded hill','shaded climb and accessible winding trail','전망 / view vocabulary stop'],'density':'two compact loops, three functional stops; no empty enlargement'},
 {'id':'entertainment','name':'Bora Bloom Park','state':'PLANNED ONLY — approval before production','world':[1280,1152],'arrival':[640,1056],'travel':[640,1056],'routes':[[[640,1056],[640,880],[384,768],[384,576],[640,608],[896,608],[896,768],[640,880]]],'landmarks':[{'id':'entrance','rect':[496,832,288,128],'label':'Playful arch + flower apron'},{'id':'wheel','rect':[176,288,288,224],'label':'Original garden wheel'},{'id':'carousel','rect':[784,352,288,192],'label':'Petal carousel'}],'identity':['original flower-and-kite silhouette, no protected brand','bright warm timber, flowering borders','circular festival loop and garden court'],'originalBrand':True},
 {'id':'busan-coast','name':'Blue Letter Coast','state':'PLANNED ONLY — approval before production','world':[1536,1152],'arrival':[256,528],'travel':[256,528],'routes':[[[256,528],[256,640],[640,664],[832,664],[1056,664],[1376,640]],[[256,528],[640,528],[1056,528],[1376,640]]],'landmarks':[{'id':'station','rect':[160,240,256,176],'label':'Small coastal station'},{'id':'train','rect':[640,304,224,80],'label':'Original sightseeing train'},{'id':'view-deck','rect':[1280,656,160,32],'label':'Sea lookout'}],'rail':[[128,384],[1440,384]],'platform':[128,416,1312,64],'shoreline':[[32,736],[608,736],[768,704],[1104,736],[1504,704]],'inlet':[800,560,96,144],'bridges':[{'rect':[784,632,128,64],'purpose':'coastal pedestrian inlet crossing'}],'water':{'seaStartsY':736,'noWalkThroughSea':True},'identity':['continuous scenic railway separate from pedestrian promenade','connected platforms, beach, water and seating','bridge spans actual inlet, rails never end in water']},
 {'id':'jeju','name':'Windstone Garden','state':'PLANNED ONLY — approval before production','world':[1408,1152],'arrival':[224,896],'travel':[224,896],'routes':[[[224,896],[416,832],[544,608],[704,480],[992,512],[1152,704],[1120,896],[832,960],[544,928],[224,896]]],'landmarks':[{'id':'dol-hareubang','rect':[352,672,64,80],'label':'Original basalt guardian'},{'id':'oreum','rect':[576,192,320,256],'label':'Volcanic low hill'},{'id':'stone-garden','rect':[960,640,128,128],'label':'Basalt / coastal garden'}],'identity':['basalt stone, wind-shaped vegetation and tangerine gardens','organic coast walk and low stone wall edges','peaceful observation and cultural interpretation, no copied sculpture asset']}
], 'travelLinks':[{'from':'heritage','to':'namsan','type':'signed fictional travel gateway','production':'first increment'},{'from':'heritage','to':'entertainment','type':'future regional travel','production':'planned'},{'from':'heritage','to':'busan-coast','type':'future regional rail travel','production':'planned'},{'from':'busan-coast','to':'jeju','type':'future ferry-inspired travel transition','production':'planned'},{'from':'jeju','to':'heritage','type':'future return gateway','production':'planned'}], 'stop':'No mass southern production until user review of repaired north + first Namsan playable increment'}
(D/'southern-masterplan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
# Validate planning routes only; this never pretends to prove future runtime collision/artwork.
checks=[]
for z in plan['destinations']:
 w,h=z['world'];rects=[a['rect']for a in z['landmarks']if a['id']not in ['arrival','view-deck','entrance']and not a.get('walkable')]
 samples=0
 for route in z['routes']:
  for (x,y),(xx,yy)in zip(route,route[1:]):
   n=math.ceil(math.hypot(xx-x,yy-y)/8)
   for i in range(n+1):
    px=x+(xx-x)*i/n;py=y+(yy-y)*i/n;assert 8<=px<w-8 and 8<=py<h-8,(z['id'],px,py)
    # North is real tested map with courtyard footprints, not solid enclosing schematic rects.
    if z['id']!='heritage':
     assert not any(rx-8<px<rx+rw+8 and ry-4<py<ry+rh+4 for rx,ry,rw,rh in rects),(z['id'],'route meets reserved physical mass',px,py)
    if z['id']=='busan-coast':
     assert py<736-4
     rx,ry,rw,rh=z['inlet'];bridge=z['bridges'][0]['rect'];bx,by,bw,bh=bridge
     if rx-8<px<rx+rw+8 and ry-4<py<ry+rh+4:assert bx+8<=px<=bx+bw-8 and by+4<=py<=by+bh-4,'bridge does not cover route'
    samples+=1
 checks.append({'zone':z['id'],'routeSamples':samples,'reservedMassClearance':'PASS','scope':'SCHEMATIC planning only; actual Phaser/Forge verification separate'})
assert len(plan['destinations'])==5 and len(plan['travelLinks'])==5
(D/'planning-check.json').write_text(json.dumps({'status':'PASS','checks':checks,'futureArtProduced':False,'geographicalAdjacencyClaim':False},indent=2)+'\n')
# One readable schematic atlas; SVG groups remain editable; PNG is same authored planning data.
W,H=1900,1450;im=Image.new('RGB',(W,H),'#142e2b');d=ImageDraw.Draw(im)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16);small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13);bold=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',25)
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="1900" height="1450" fill="#142e2b"/>']
def text(x,y,s,fill='#f4e6bf',size=16):
 d.text((x,y),s,font=bold if size==25 else small if size==13 else font,fill=fill);svg.append(f'<text x="{x}" y="{y+size}" font-family="sans-serif" font-size="{size}" fill="{fill}">{s.replace("&","&amp;")}</text>')
def rect(box,fill,stroke=None):
 d.rectangle(box,fill=fill,outline=stroke,width=2);x,y,xx,yy=box;svg.append(f'<rect x="{x}" y="{y}" width="{xx-x}" height="{yy-y}" fill="{fill}" stroke="{stroke or fill}" stroke-width="2"/>')
def line(points,fill,width=4):
 d.line(points,fill=fill,width=width,joint='curve');svg.append(f'<polyline points="'+ ' '.join(f'{x},{y}'for x,y in points)+f'" fill="none" stroke="{fill}" stroke-width="{width}"/>')
text(30,22,'LIVING KOREA / SOUTHERN TRAVEL MASTERPLAN',size=25);text(30,66,'Fictional condensed educational travel world — NOT geographically adjacent real Seoul locations.',size=16)
panels=[(30,120,650,600),(740,120,600,600),(30,820,540,520),(620,820,620,520),(1290,820,580,520)]
for z,(x,y,pw,ph)in zip(plan['destinations'],panels):
 svg.append(f'<g id="zone-{z["id"]}">');rect((x,y,x+pw,y+ph),'#28453b','#70846b');text(x+14,y+12,z['name']);text(x+14,y+40,z['state'],fill='#ddbd73',size=13)
 scale=min((pw-50)/z['world'][0],(ph-112)/z['world'][1]);ox=x+25;oy=y+86
 tr=lambda p:(round(ox+p[0]*scale),round(oy+p[1]*scale))
 if z['id']=='busan-coast':
  p1=tr((0,736));p2=tr((1536,1152));rect((*p1,*p2),'#3d8390');line([tr(p)for p in z['rail']],'#a8c0c0',5);rx,ry,rw,rh=z['inlet'];rect((*tr((rx,ry)),*tr((rx+rw,ry+rh))),'#3d8390')
 for a in z['landmarks']:
  rx,ry,rw,rh=a['rect'];p1=tr((rx,ry));p2=tr((rx+rw,ry+rh));rect((*p1,*p2),'#6d8472','#b0c29a');text(p1[0]+3,p1[1]+4,a['id'],size=13)
 for route in z['routes']:line([tr(p)for p in route],'#dfc68c',6)
 ax,ay=tr(z['travel']);d.ellipse((ax-6,ay-6,ax+6,ay+6),fill='#ffdb82');svg.append(f'<circle cx="{ax}" cy="{ay}" r="6" fill="#ffdb82"/>')
 text(x+14,y+ph-23,f"{z['world'][0]} x {z['world'][1]} units | Juni 80px | editable footprint / route data",size=13);svg.append('</g>')
line([(680,560),(710,560),(710,680),(1040,680),(1040,720)],'#f5ce78',5);text(740,734,'ACTIVE FIRST INCREMENT: signed heritage-to-Namsan travel',size=13)
line([(330,720),(330,780),(1580,780),(1580,820)],'#778f88',3);line([(330,780),(900,780),(900,820)],'#778f88',3);line([(330,780),(300,820)],'#778f88',3)
text(30,1380,'Gold paths: local pedestrian routes. Travel links: regional transitions. Grey future areas are NOT produced game maps.',size=16);text(30,1410,'Review gate: repaired north + ONE Namsan playable environment + landscape mobile, then STOP before mass production.',size=16)
svg.append('</svg>');(D/'southern-masterplan.svg').write_text('\n'.join(svg)+'\n');im.save(D/'southern-masterplan.png');print(json.dumps(checks))
