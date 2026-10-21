"""New image-material composition over the APPROVED V10 geometry, plus authored landscaping."""
from pathlib import Path
import json,math
import numpy as np
from scipy.ndimage import maximum_filter,minimum_filter
from PIL import Image,ImageDraw,ImageFilter,ImageChops
from v10_plan import sample_points
R=Path(__file__).resolve().parents[1];S=R/'assets-src/v10-city';N=S/'native'
def surfaces(plan):
    w,h=plan['world'];ground=Image.new('RGB',(w,h));land=Image.new('L',(w,h));ld=ImageDraw.Draw(land)
    ld.polygon(plan['mainland'],fill=255);ld.polygon(plan['island'],fill=255)
    textures={}
    def fill(mask,key):
        if key not in textures:textures[key]=np.array(Image.open(N/(key+'-material.png')).convert('RGB'))
        tile=textures[key];pattern=Image.fromarray(np.tile(tile,(h//tile.shape[0]+1,w//tile.shape[1]+1,1))[:h,:w].copy());ground.paste(pattern,(0,0),mask)
    def mask_polygon(points):
        m=Image.new('L',(w,h));ImageDraw.Draw(m).polygon(points,fill=255);return m
    def rect(box):
        m=Image.new('L',(w,h));ImageDraw.Draw(m).rectangle(box,fill=255);return m
    def line(points,width):
        m=Image.new('L',(w,h));d=ImageDraw.Draw(m);d.line(points,fill=255,width=width,joint='curve')
        for x,y in [points[0],points[-1]]:d.ellipse((x-width/2,y-width/2,x+width/2,y+width/2),fill=255)
        return m
    def grow(mask,size,inset=False):
        # Sliding min/max gives the same native mask without quadratic rank-filter cost.
        op=minimum_filter if inset else maximum_filter
        return Image.fromarray(op(np.asarray(mask),size=size,mode='nearest'))
    fill(None,'sea');fill(grow(land,65),'shallows');fill(land,'grass')
    # Urban plots are framed by continuous contemporary paving, not isolated lawns.
    fill(mask_polygon([(1392,2240),(4320,2240),(4320,3568),(3456,3568),(2768,3568),(2016,3568),(1392,3504)]),'sidewalk')
    fill(mask_polygon([(200,2560),(640,2336),(1056,2432),(1352,2784),(1280,3192),(992,3440),(512,3440),(160,3120)]),'meadow')
    fill(mask_polygon(plan['island']),'meadow')
    shore=ImageChops.subtract(land,grow(land,17,True));fill(shore,'masonry')
    paving=Image.new('L',(w,h));road_masks=[]
    for road in plan['roads']:
        pts=sample_points(road);m=line(pts,road['width']);paving=ImageChops.lighter(paving,m);road_masks.append((road,pts,m));ImageDraw.Draw(land).bitmap((0,0),m,fill=255)
    fill(grow(paving,9),'masonry');fill(paving,'sidewalk')
    for road,pts,m in road_masks:
        kind=road['kind'];key={'park':'granite','island':'basalt','pier':'timber','lane':'brick','promenade':'coastal'}.get(kind)
        if road['id']=='leisure-circuit':key='leisure'
        if key:fill(m,key)
        elif road['id']!='heritage-gateway':fill(line(pts,max(32,road['width']-48)),'asphalt')
        else:fill(m,'civic')
    cx,cy,cw,ch=plan['civicCourt'];fill(rect((cx,cy,cx+cw,cy+ch)),'civic');fill(rect((cx+176,cy+80,cx+352,cy+160)),'soil')
    for lot in plan['plots']:
        x,y,pw,ph=lot['rect'];dx,dy=lot['door'];key='basalt'if lot['district']=='jeju'else'leisure'if lot['district']=='entertainment'else'civic'
        # Property forecourts/approaches are explicit, individually matched to doors.
        if lot['facing']=='south':fill(rect((dx-40,y+ph,dx+40,dy+24)),key)
        elif lot['facing']=='north':fill(rect((dx-40,dy-24,dx+40,y)),key)
        else:fill(rect((dx-24,dy-40,x,dy+40)),key)
        if lot['district']=='commons'and lot['id']!='civic-house':
            curb=2880 if dy<2960 else 3040
            fill(rect((dx-32,min(dy,curb),dx+32,max(dy,curb))),'sidewalk')
        if lot['district']in ['entertainment','namsan']:
            m=Image.new('L',(w,h));ImageDraw.Draw(m).ellipse((dx-112,dy-40,dx+112,dy+88),fill=255);fill(m,key if lot['district']=='entertainment'else'granite')
    # Correctly aligned railway/platform/crossing; utility markings are not building art.
    fill(rect((3280,2424,4240,2472)),'asphalt');fill(rect((3520,2472,4192,2504)),'civic');g=ImageDraw.Draw(ground)
    for y in [2432,2464]:g.line((3280,y,4240,y),fill='#aeb8ba',width=4)
    for x in range(3280,4240,24):g.line((x,2428,x,2468),fill='#647379',width=3)
    fill(rect((3424,2424,3488,2472)),'sidewalk')
    for x in [2016,2768,3456]:
        for yy in range(2916,3005,14):g.rectangle((x-34,yy,x+34,yy+6),fill='#e7e2d2')
    # Purposeful waiting deck and trail-linked observation spaces.
    fill(rect((3720,4192,3872,4296)),'coastal')
    for x,y in [(480,3040),(1008,3216),(3296,5216)]:fill(line([(x,y),(x+48,y+32)],72),'granite'if y<4000 else'basalt')
    # Short door approaches integrate the approved rides into the existing loop.
    access=[([[400,4056],[616,4072],[952,4080],[1264,4048]],96),([[800,4168],[800,4076]],80)]
    for pts,width in access:fill(line(pts,width),'leisure')
    road=next(r for r in plan['roads']if r['id']=='leisure-circuit');edge=[]
    for x,y in sample_points(road):
        ux,uy=x-832,y-4016;length=max(1,math.hypot(ux,uy));edge.append((round(x+ux/length*72),round(y+uy/length*72)))
    hedge=line(edge,40);ImageDraw.Draw(hedge).ellipse((1264,3776,1536,4048),fill=0)
    # Low curved planting uses pixels cropped from NEW V10 foliage, not flat-color fencing.
    leaf=Image.open(N/'deciduous.png').convert('RGB').crop((64,48,96,80))
    texture=Image.fromarray(np.tile(np.array(leaf),(h//32+1,w//32+1,1))[:h,:w].copy());ground.paste(texture,(0,0),hedge)
    (S/'production').mkdir(exist_ok=True)
    (S/'production/access-refinements.json').write_text(json.dumps(dict(reason='Door/landscape finishing allowed by production directive; approved road/plot/topology data unchanged',leisureDoorApproaches=access,urbanDoorFinish='Stop at sidewalk edge, no paving caps inside roadway',hedgeSource=dict(image='native/deciduous.png',box=[64,48,96,80])),indent=2)+'\n')
    north=Image.open(R/'assets-src/protected-north/ground-native.png').convert('RGB');ground.paste(north,(0,0))
    return ground,land.convert('1')

def decorations(plan):
    out=[]
    def add(asset,x,y,purpose,solid=False,anchor=None):
        out.append(dict(id=f'v10-detail-{len(out)+1}',asset=asset,x=round(x),y=round(y),purpose=purpose,solid=solid,anchor=anchor))
    for x,y in [(1504,2848),(1968,2848),(2704,2848),(3392,2848),(1504,3424),(1968,3424),(2672,3424),(3392,3424)]:add('deciduous'if x<2700 else'cherry',x,y,'Street-corner planted setback')
    for x,y in [(2192,3192),(2576,3192)]:add('bench',x,y,'Civic meeting-court seating')
    for x,y in [(2296,3208),(2456,3208),(2160,3432),(2600,3432)]:add('planter',x,y,'Civic planting island and community frontage')
    for x,y in [(1560,2864),(1944,2864),(2632,2864),(3336,2864),(3576,2880),(4104,2880),(3504,3440)]:add('lamp',x,y,'Sidewalk lighting outside door approaches')
    for x,y in [(1816,2832),(3224,3424),(4072,2864)]:add('bikes',x,y,'Shop/transit bicycle parking')
    for x,y in [(280,2552),(432,2472),(1008,2496),(1328,2672),(240,2976),(448,3160),(592,3432),(1120,3432),(1328,3280),(480,2864),(1016,3072)]:add('pine',x,y,'Namsan slope grove outside trail circulation')
    add('pergola',464,3040,'Trail-linked observation/rest terrace');add('view-deck',1032,3224,'Namsan viewpoint')
    for x,y in [(544,3104),(960,2624),(1184,3160)]:add('flowerbed',x,y,'Scenic rest pocket planting')
    for x,y in [(240,2768),(736,3416),(1336,2752)]:add('bench',x,y,'Hiking-loop rest point')
    for x,y in [(496,4120),(736,3760),(1128,4208),(1120,3840),(400,4016),(800,4416)]:add('flowerbed',x,y,'Amusement court/perimeter planted edge')
    for x,y in [(456,4160),(1056,4432),(1168,3920)]:add('bench',x,y,'Leisure resting space')
    for x,y in [(528,4104),(1064,4072)]:add('queue',x,y,'Ride-specific queue area outside the public circuit')
    add('campus-gate',1408,3992,'East-facing leisure arrival gate; clear horizontal passage')
    # Modular new rail sprites follow the approved leisure circuit's outward edge.
    road=next(r for r in plan['roads']if r['id']=='leisure-circuit');pts=sample_points(road);last=None
    for i,(x,y)in enumerate(pts[:-1]):
        if last and math.hypot(x-last[0],y-last[1])<92:continue
        ux,uy=x-832,y-4016;length=max(1,math.hypot(ux,uy));xx=x+ux/length*72;yy=y+uy/length*72
        if math.hypot(xx-1408,yy-3904)<140:continue
        nx,ny=pts[min(i+1,len(pts)-1)];vertical=abs(ny-y)>abs(nx-x)
        if not vertical and abs(ny-y)<abs(nx-x)*.35:add('rail',xx,yy,'Straight fence sections in continuous curved planted boundary')
        last=(x,y)
    coast=next(r for r in plan['roads']if r['id']=='park-to-sea')['points']
    for a,b in zip(coast,coast[1:]):
        if a[1]<3900:continue
        length=math.dist(a,b)
        for t in np.arange(0,1,112/max(1,length)):add('rail',a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t+80,'Continuous seafront safety rail')
    add('train',3856,2472,'Station train positioned on the signed east track, clear of crossing');add('ferry',4080,4608,'Moored ferry aligned against the east side of the boarding pier')
    for x,y in [(3904,4416),(3904,4528)]:add('rail-vertical',x,y,'Boarding-pier landward safety rail',anchor=[24,96])
    for x,y in [(3616,4224),(3712,4272)]:add('bench',x,y,'Ferry waiting forecourt')
    add('oreum',3000,5400,'Jeju volcanic oreum inside the scenic loop');add('view-deck',3520,5520,'Jeju coastal viewpoint')
    for x,y in [(2528,5248),(2592,5536),(2864,5120),(3072,5160),(3408,5328),(3408,5664)]:add('tangerine',x,y,'Jeju village/orchard grove')
    for x,y in [(2720,5000),(3024,5280),(3152,5344)]:add('basalt-wall',x,y,'Jeju dry-stone property edge with original gate opening')
    return out
