"""Planning diagrams only. Comparison is read separately AFTER V10 authoring."""
import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from v10_plan import sample_points
R=Path(__file__).resolve().parents[1];D=R/'docs/v10-city'
F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
font=lambda n:ImageFont.truetype(F,n)
def render(plan,title,labels=True):
    scale=0.28;w,h=plan['world'];ox,oy=64,148
    im=Image.new('RGB',(int(w*scale)+128,int(h*scale)+256),'#f3f1e9');q=ImageDraw.Draw(im)
    q.text((64,32),title,font=font(26),fill='#20394b')
    q.text((64,74),'DESIGN STUDY / PLACEHOLDERS — NOT FINAL ART',font=font(16),fill='#596e77')
    def p(pt):return (ox+round(pt[0]*scale),oy+round(pt[1]*scale))
    q.rectangle([p((0,0)),p((w,h))],fill='#b8d2d9')
    q.rectangle([p((0,0)),p((w,2240))],fill='#e5e2d5')
    q.text(p((180,600)),'PROTECTED HISTORICAL NORTH',font=font(23),fill='#617071')
    q.text(p((180,760)),'Native artwork + 273 placements unchanged',font=font(16),fill='#617071')
    q.line([p((0,2240)),p((w,2240))],fill='#ad6651',width=3)
    for key in ['mainland','island']:q.polygon([p(v)for v in plan[key]],fill='#d7dfcf')
    for road in plan['roads']:
        pts=[p(v)for v in sample_points(road)];width=max(3,round(road['width']*scale))
        q.line(pts,fill='#657c87',width=width+3,joint='curve');q.line(pts,fill='#eee9d8'if road['kind']in ['park','island']else'#f8f6ed',width=width,joint='curve')
    q.line([p((3280,2448)),p((4240,2448))],fill='#3d596b',width=4)
    q.line([p((3456,2424)),p((3456,2472))],fill='#e8d7aa',width=18)
    q.text(p((3560,2368)),'RAIL / PLATFORM',font=font(10),fill='#20394b')
    colors={'commons':'#8eabb8','transit':'#7292b2','namsan':'#739d86','entertainment':'#ba91a5','busan-coast':'#76a6aa','jeju':'#b0a77d'}
    for lot in plan['plots']:
        x,y,w,h=lot['rect'];q.rectangle([p((x,y)),p((x+w,y+h))],fill=colors[lot['district']],outline='#38525f',width=1)
        q.ellipse([p((lot['door'][0]-12,lot['door'][1]-12)),p((lot['door'][0]+12,lot['door'][1]+12))],fill='#d35f44')
        if labels:q.text(p((x+8,y+12)),lot['id'],font=font(10),fill='#20394b')
    for text,pt in [('01  NAMSAN / WEST HILL',(240,2304)),('02  HIGH STREET + BLOCKS',(1490,2280)),('03  EAST TRANSIT',(3504,2280)),('04  LEISURE CAMPUS',(240,3544)),('05  WATERFRONT',(2864,3592)),('06  JEJU / OLLE + VILLAGE',(2400,4790)),('CIVIC COURT',(2112,3160))]:
        q.text(p(pt),text,font=font(12),fill='#20394b')
    # Ferry is a route across water, never a walkable bridge.
    a=plan['travel']['mainlandTrigger'];b=plan['travel']['islandTrigger']
    for i in range(0,20,2):
        q.line([p([a[j]+(b[j]-a[j])*i/20 for j in [0,1]]),p([a[j]+(b[j]-a[j])*(i+1)/20 for j in [0,1]])],fill='#254c78',width=3)
    q.text(p((3500,4680)),'FERRY',font=font(13),fill='#254c78')
    q.text((64,im.height-76),'Primary 160px / streets 96–112px / trails 64–80px / Juni foot 16×8px',font=font(15),fill='#526874')
    q.text((64,im.height-48),'Red dots = entrances. Independent V10 plan; visual acceptance pending.',font=font(15),fill='#526874')
    # Focus this planning board on the new south; do not waste half on a blank north.
    band=im.crop((0,oy+round(2176*scale),im.width,im.height))
    focused=Image.new('RGB',(im.width,band.height+148),'#f3f1e9')
    focused.paste(im.crop((0,0,im.width,148)),(0,0));focused.paste(band,(0,148))
    return focused

if __name__=='__main__':
    D.mkdir(parents=True,exist_ok=True)
    plan=json.loads((R/'assets-src/v10-city/plan/city.json').read_text())
    im=render(plan,'V10 / GYEOL EAST–WEST NEIGHBORHOOD')
    im.save(D/'V10_NEW_URBAN_MASTERPLAN.png')
    roads=render(plan,'V10 / ROAD HIERARCHY + BUILDING PLOTS')
    schedule=Image.new('RGB',(roads.width,roads.height+276),'#f3f1e9');schedule.paste(roads,(0,0));q=ImageDraw.Draw(schedule)
    for i,r in enumerate(plan['roads']):
        q.text((48+(i//7)*430,roads.height+20+(i%7)*32),f"{r['id']} / {r['width']}px",font=font(14),fill='#20394b')
    schedule.save(D/'V10_ROAD_AND_PLOT_LAYOUT.png')
    print('V10 planning diagrams generated; no V9 input read.')
