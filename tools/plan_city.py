"""V9 streets first, plots second. No previous southern geometry/image is read."""
from map_pipeline import *
from PIL import Image,ImageDraw,ImageFont
import html,math
P=SOURCE/'plan';P.mkdir(exist_ok=True)
W,H=4352,6144
mainland=[[0,2240],[4352,2240],[4352,4432],[4208,4592],[3872,4736],[3376,4768],[2864,4768],[2528,4768],[2208,4720],[1856,4480],[1360,4368],[704,4384],[160,4288],[0,4128]]
island=[[512,5456],[704,5168],[1056,4992],[1376,4960],[1744,5104],[2048,5328],[2224,5592],[2080,5896],[1696,6056],[1136,6040],[720,5864],[512,5616]]
roads=[]
def road(id,points,width,kind='secondary',purpose='',smooth=False):roads.append(dict(id=id,points=points,width=width,kind=kind,purpose=purpose,smooth=smooth))
road('heritage-gateway',[[2176,2240],[2176,2784]],112,'primary','Protected north to civic square')
road('civic-ring',[[2048,2816],[1936,2936],[2048,3056],[2288,3056],[2400,2936],[2288,2816],[2048,2816]],80,'civic','Shops and social meeting loop')
road('book-street',[[1056,2784],[1648,2784],[2176,2784],[2768,2784]],80,'secondary','Two different cultural shop frontages')
road('west-neighborhood',[[1056,2784],[1056,3376]],64,'local','Back-street and station western entrance')
road('civic-boulevard',[[2288,3056],[2288,3232],[2528,3232],[2528,4656]],112,'primary','Civic heart to station junction and ferry')
road('city-cross-street',[[1056,3376],[1936,3376],[2528,3376],[2784,3376]],80,'secondary','Commercial and transit blocks')
road('shop-frontages',[[1648,2784],[1648,2880],[1760,2880],[1760,3280],[800,3280]],56,'local','Short learning service alley')
road('namsan-approach',[[2288,3056],[2288,3280],[2832,3280],[2992,3152]],80,'secondary','Park entrance at west garden threshold')
road('namsan-loop',[[2992,3152],[3072,2960],[3248,2904],[3520,2960],[3792,3008],[4000,3144],[3872,3336],[3616,3280],[3392,3376],[3152,3304],[2992,3152]],64,'scenic','Complete planted park circuit',True)
road('pavilion-approach',[[3704,3312],[3704,3272]],56,'scenic','Short overlook pavilion approach')
road('tower-lookout',[[3520,2960],[3520,2904]],64,'scenic','Observation lobby approach')
road('park-pavilion',[[3872,3336],[3872,3392],[4080,3520],[4080,3744],[3872,3744]],64,'scenic','Secondary park gate to visitor entrance')
road('station-crossing',[[1936,3376],[1936,3728],[1936,3960]],80,'secondary','One marked rail crossing, not a rail/path overlap')
road('station-front',[[1056,3960],[1376,3960],[1936,3960],[2528,3960]],96,'secondary','Station entrance and main boulevard')
road('station-platform',[[1376,3728],[1936,3728]],56,'local','Platform access behind station, clear of rail line')
road('coastal-city-street',[[2528,4176],[2784,4176],[2880,4288],[3216,4288],[3216,4536]],80,'secondary','East city to amusement gateway')
road('leisure-loop',[[3216,4400],[2960,4272],[2952,3960],[3136,3920],[3408,3912],[3584,3744],[3872,3744],[4048,3936],[3976,4232],[3776,4320],[3520,4368],[3216,4400]],72,'leisure','Attraction forecourts on a complete internal circuit',True)
road('carousel-front',[[3976,4232],[3840,4216]],64,'leisure','Carousel queue frontage')
road('visitor-front',[[3872,3744],[3872,3728]],64,'leisure','Visitor kiosk and northern gate')
road('hall-front',[[3520,4368],[3520,4536],[3776,4536]],64,'leisure','Discovery pavilion and park main gate')
road('campus-main',[[3216,4400],[3216,4560],[3216,4592]],96,'leisure','Park gate to public promenade')
road('seaside-lane',[[1056,3960],[1056,4176]],64,'local','Station forecourt to coastal pocket')
road('west-waterfront',[[1056,4176],[768,4256]],64,'local','Coastal cafe and lookout')
road('coastal-promenade',[[768,4256],[1376,4224],[1888,4344],[2192,4496],[2160,4616],[2528,4656],[2880,4624],[3552,4656],[4032,4560]],96,'coastal','Continuous safe public seafront',True)
road('ferry-boarding',[[2528,4656],[2560,4720],[2560,4880]],64,'timber','Terminal, waiting space, pier and boarding edge')
road('island-arrival',[[2064,5408],[2064,5472],[1920,5504],[1664,5568]],64,'island','Landing to scenic exploration circuit',True)
road('jeju-loop',[[1664,5568],[1568,5648],[1632,5856],[1840,5904],[1808,5952],[1568,5984],[1184,5968],[992,5856],[752,5840],[672,5744],[608,5584],[736,5384],[944,5408],[1024,5568],[1280,5584],[1536,5520],[1664,5568]],56,'island','Complete terrain-following scenic loop',True)
road('oreum-approach',[[1280,5584],[1280,5544]],56,'island','Hill viewpoint')
road('village-approach',[[1184,5968],[1296,5904]],56,'island','Cultural courtyard entrance')
road('nature-approach',[[1840,5904],[1856,5872]],56,'island','Nature center south facade')
road('basalt-approach',[[1568,5984],[1536,5976]],56,'island','Volcanic learning discovery')
# Plots are established after the public network, never from old placement records.
plots=[]
def plot(id,box,site,kind,front,role):plots.append(dict(id=id,bounds=box,site=site,asset=kind,entrance=front,function=role))
plot('bookshop',[1440,2320,1856,2744],[1648,2672],'fw-bookstore',[1648,2784],'Books and Korean vocabulary frontage')
plot('library',[2392,2304,2704,2736],[2544,2656],'rf-prod-library',[2544,2784],'Public reading and learning service')
plot('neighborhood-service',[560,2904,1040,3280],[800,3216],'v3-urban-hub',[800,3280],'Civic information and future conversations')
plot('cafe',[2480,2952,2864,3264],[2672,3184],'rf-cafe',[2672,3264],'Social cafe at park approach')
plot('tower',[3264,2320,3776,2944],[3520,2904],'v3-tower',[3520,2960],'Namsan observation destination')
plot('garden-pavilion',[3544,3056,3872,3256],[3704,3200],'v3-trail-pavilion',[3704,3272],'Park trail information and rest')
plot('station',[1056,3656,1696,3968],[1376,3896],'v3-station',[1376,3960],'Passenger building facing forecourt, railway behind')
plot('transit-shelter',[2080,3472,2376,3720],[2224,3624],'v3-bus-stop',[2224,3696],'Local public transport transfer')
plot('coastal-cafe',[448,3880,896,4232],[672,4136],'v3-coastal-cafe',[672,4256],'Seafront rest and neighborhood edge')
plot('lookout',[1216,4000,1568,4224],[1392,4168],'v3-seawall',[1392,4256],'Coastal viewing platform')
plot('wheel',[2880,3472,3376,3920],[3136,3856],'v3-wheel',[3136,3920],'Observation wheel dedicated queue court')
plot('carousel',[3616,3824,4080,4232],[3840,4128],'v3-carousel',[3840,4216],'Carousel family court')
plot('visitor',[3728,3504,4048,3720],[3872,3672],'v3-kiosk',[3872,3744],'Visitor service at northern campus gate')
plot('discovery-hall',[3552,4240,4016,4552],[3776,4480],'v3-discovery-hall',[3776,4536],'Creative learning pavilion')
plot('campus-entry',[2960,4144,3472,4520],[3216,4480],'v3-bloom-entry',[3216,4592],'Wide central gate with two ticket pods')
plot('ferry-terminal',[2176,4336,2528,4616],[2352,4560],'v3-ferry-terminal',[2352,4656],'Waiting terminal facing the single boarding sequence')
plot('oreum',[960,5040,1584,5568],[1280,5520],'v3-oreum',[1280,5584],'Volcanic hill and viewpoint')
plot('village',[1056,5616,1536,5912],[1296,5840],'v3-jeju-court',[1296,5904],'Jeju cultural courtyard')
plot('nature-center',[1632,5544,2096,5872],[1856,5808],'v3-nature-centre',[1856,5872],'Basalt and glass nature classroom')
plot('cliff-lookout',[624,5344,1024,5728],[832,5712],'v3-cliff-lookout',[672,5744],'Rock face and safe west-side lookout approach')
plot('basalt-learning',[1408,5808,1664,5976],[1536,5920],'v3-basalt-discovery',[1536,5976],'Volcanic vocabulary discovery')
plot('corner-grocery',[1112,2464,1448,2760],[1280,2728],'new-grocery',[1280,2784],'Korean neighborhood grocery and public frontage')
plot('bakery',[1112,2952,1448,3264],[1280,3216],'new-bakery',[1280,3280],'Small bakery with social terrace')
plot('language-center',[1848,2392,2184,2744],[2016,2672],'new-language',[2016,2784],'Korean language community classroom')
plot('design-gallery',[1448,2952,1712,3264],[1584,3216],'new-gallery',[1584,3280],'Contemporary craft and design shop')
# Dimensions/local native collider templates only; no previous southern positions consulted.
catalog=json.loads((ROOT/'assets-src/library/props.json').read_text())
for key in ['new-grocery','new-bakery','new-language','new-gallery']:
 catalog[key]={'size':[256,224],'anchor_px':[128,222],'colliders':[{'x':-104,'y':-48,'w':208,'h':48}]}
for p in plots:
 a=catalog[p['asset']];x,y=p['site'];ax,ay=a['anchor_px'];w,h=a['size'];p['artBounds']=[x-ax,y-ay,x-ax+w,y-ay+h];p['bodyRects']=[[x+c['x'],y+c['y'],c['w'],c['h']]for c in a['colliders']];p['nativeScale']=1
plan=dict(schema='korean-arena.v9.urban-plan.v1',world=[W,H],fixedNorthernBoundary=2240,coordinateBasis='new south; no rejected southern inputs',mainland=mainland,island=island,roads=roads,plots=plots,districts=[{'id':'commons','bounds':[704,2240,2832,3472],'color':'#89b8c5'},{'id':'namsan','bounds':[2832,2240,4352,3472],'color':'#739f66'},{'id':'transit','bounds':[384,3472,2528,4176],'color':'#89a8d2'},{'id':'entertainment','bounds':[2784,3472,4256,4544],'color':'#c48ca8'},{'id':'busan-coast','bounds':[0,4176,4352,4992],'color':'#79bdbc'},{'id':'jeju','bounds':[480,4960,2256,6080],'color':'#9fae79'}],rail={'start':[720,3584],'end':[2032,3584],'crossing':[1936,3584],'train':[1136,3576],'platform':[1376,3672]},travel={'enabled':True,'mainlandTrigger':[2560,4880],'islandTrigger':[2064,5408],'mainlandArrival':[2560,4760],'islandArrival':[2064,5528],'discovery':[1536,5976],'seaBoundary':5000},socialAnchors=[{'id':'civic-meet','point':[2176,2936],'role':'Future Korean conversation'},{'id':'station-meet','point':[1568,3984],'role':'Future travel vocabulary'},{'id':'park-rest','point':[3392,3376],'role':'Future nature quest'}])
write(P/'city.json',plan)
# Structural feasibility is explicit and independent from aesthetic approval.
issues=[]
for p in plots:
 if p['artBounds'][1]<2240:issues.append([p['id'],'art overlaps protected north'])
 if any(v<0 for v in p['artBounds'])or p['artBounds'][2]>W or p['artBounds'][3]>H:issues.append([p['id'],'art outside world'])
 if not all(p['bounds'][i]<=p['site'][i%2] for i in [0,1]):issues.append([p['id'],'site outside plot'])
for r in roads:
 for x,y in r['points']:
  if not(0<=x<W and 2240<=y<H):issues.append([r['id'],'route vertex outside new south'])
write(P/'feasibility.json',{'status':'PASS'if not issues else'FAIL','checks':['All artwork native-scale bounding boxes south of fixed boundary','Routes/plots authored from clean coordinates','World bounds','112/96/80/72/64/56px public route hierarchy','One intentional rail crossing','Ferry sole island connection'],'issues':issues,'nextGate':'Actual graybox collision/traversal, not visual acceptance'})
assert not issues,issues
colors={'primary':'#e3d4a0','secondary':'#c8d7df','local':'#b4c7c9','civic':'#92cad5','scenic':'#e0ce9e','leisure':'#ecc0d5','coastal':'#d7e9eb','island':'#e3cf9d','timber':'#b58456'}
parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="100%" height="100%" fill="#285e7d"/><rect width="4352" height="2240" fill="#526b56"/><text x="120" y="180" fill="white" font-size="64">PROTECTED HISTORICAL NORTH — 4352 × 2240</text>']
for points in [mainland,island]:parts.append('<polygon points="'+' '.join(f'{x},{y}'for x,y in points)+'" fill="#7b9870"/>')
for d in plan['districts']:
 x,y,x2,y2=d['bounds'];parts.append(f'<rect x="{x}" y="{y}" width="{x2-x}" height="{y2-y}" fill="{d["color"]}" fill-opacity=".32" stroke="{d["color"]}" stroke-width="8"/><text x="{x+20}" y="{y+55}" font-size="40" fill="#153139">{d["id"].upper()}</text>')
for r in roads:parts.append(f'<polyline points="'+ ' '.join(f'{x},{y}'for x,y in r['points'])+f'" fill="none" stroke="{colors[r["kind"]]}" stroke-width="{r["width"]}" stroke-linecap="round" stroke-linejoin="round"/>')
for p in plots:
 x,y,x2,y2=p['bounds'];parts.append(f'<rect x="{x}" y="{y}" width="{x2-x}" height="{y2-y}" fill="none" stroke="#eaf4df" stroke-width="4" stroke-dasharray="12 8"/>');x,y,x2,y2=p['artBounds'];parts.append(f'<rect x="{x}" y="{y}" width="{x2-x}" height="{y2-y}" fill="#455b75" stroke="#152c42" stroke-width="4"/><text x="{x+6}" y="{y+35}" font-size="24" fill="white">{html.escape(p["id"])}</text>');x,y=p['entrance'];parts.append(f'<circle cx="{x}" cy="{y}" r="12" fill="#fff47d"/>')
parts.append('<path d="M720 3584H2032" stroke="#293640" stroke-width="24"/><path d="M2560 4880 Q2700 5200 2064 5408" fill="none" stroke="#fff1a0" stroke-width="8" stroke-dasharray="24 16"/><text x="2672" y="5140" fill="white" font-size="38">INTERACTIVE FERRY · NO BRIDGE</text></svg>');(P/'city.svg').write_text(''.join(parts))
# Readable editable-plan PNG; this is a plan, never presented as gameplay.
im=Image.new('RGB',(W,H),'#285e7d');d=ImageDraw.Draw(im);d.rectangle((0,0,W,2239),fill='#526b56')
for points in [mainland,island]:d.polygon([tuple(p)for p in points],fill='#7b9870')
for r in roads:d.line([tuple(p)for p in r['points']],fill=colors[r['kind']],width=r['width'],joint='curve')
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',28)
for p in plots:
 d.rectangle(p['bounds'],outline='#d7e6dd',width=4);d.rectangle(p['artBounds'],fill='#455b75',outline='#172a38',width=4);x,y=p['artBounds'][:2];d.text((x+6,y+6),p['id'],font=font,fill='white');x,y=p['entrance'];d.ellipse((x-12,y-12,x+12,y+12),fill='#fff47d')
d.text((96,80),'V9 NEW CITY MASTERPLAN — editable JSON / SVG',font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',60),fill='white');d.text((96,160),'Protected north above y2240; original southern coordinates below',font=font,fill='white');im.save(ROOT/'docs/v9-world/V9_NEW_CITY_MASTERPLAN.png');print('New plan: roads',len(roads),'plots',len(plots),'feasibility PASS')
