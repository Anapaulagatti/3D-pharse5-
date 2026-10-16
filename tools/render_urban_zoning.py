"""Render a zoning diagram and check reserved circulation. Never creates game art/data."""
from pathlib import Path
import json, math, html
from collections import deque
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/urban-zoning'
p = json.loads((OUT / 'zoning-plan.json').read_text())
W,H = p['world']
S,OX,OY = .375,64,192
im = Image.new('RGB',(1984,1536),'#f6f2e9'); d=ImageDraw.Draw(im)
regular='/usr/share/fonts/truetype/open-sans/OpenSans-Regular.ttf'
bold='/usr/share/fonts/truetype/open-sans/OpenSans-Bold.ttf'
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1984" height="1536" viewBox="0 0 1984 1536"><rect width="1984" height="1536" fill="#f6f2e9"/>']
def text(x,y,t,size=18,fill='#233b3a',weight=False):
    t=t.replace('→','>')
    d.text((x,y),t,font=ImageFont.truetype(bold if weight else regular,size),fill=fill)
    svg.append(f'<text x="{x}" y="{y+size}" font-family="sans-serif" font-size="{size}" font-weight="{700 if weight else 400}" fill="{fill}">{html.escape(t)}</text>')
def rect(box,fill,outline=None,width=1):
    d.rectangle(box,fill=fill,outline=outline,width=width)
    x,y,x2,y2=box;svg.append(f'<rect x="{x}" y="{y}" width="{x2-x}" height="{y2-y}" fill="{fill or "none"}" stroke="{outline or "none"}" stroke-width="{width}"/>')
def line(points,fill,width):
    d.line(points,fill=fill,width=width,joint='curve')
    svg.append(f'<polyline points="{" ".join(f"{x},{y}" for x,y in points)}" fill="none" stroke="{fill}" stroke-width="{width}" stroke-linejoin="round"/>')
def pt(q):return OX+q[0]*S,OY+q[1]*S
def worldrect(b,fill,outline=None,width=1):
    x,y,w,h=b;rect((*pt((x,y)),*pt((x+w,y+h))),fill,outline,width)
def worldline(points,fill,width):line([pt(q) for q in points],fill,max(1,round(width*S)))
text(64,32,'LIVING SEOUL · QUY HOẠCH KHU PHỐ',34,weight=True)
text(64,86,'ĐỀ XUẤT CẦN DUYỆT · sơ đồ phân khu, không phải ảnh game hay bản đồ đã dựng',21,fill='#986340',weight=True)
text(64,126,'4096 × 3072 px đề xuất  |  Juni giữ 80 px  |  Bắc ở trên  |  Không đổi bản chơi hiện tại',18)
worldrect([0,0,W,H],'#e9e4d7','#83928b',2)
worldrect(p['wall']['closedNorthReserve'],'#d8d7d0')
text(*pt((64,32)),'PHÍA CUNG THÀNH · DỰ TRỮ / CHƯA MỞ',15,fill='#70756d')
for z in p['zones']:
    worldrect(z['bounds'],z['color'],'#a3aa9c')
    x,y,_,_=z['bounds']
    if z['id']!='plaza':text(*pt((x+24,y+18)),z['label'],15,weight=True)
for c in p['courts']:worldrect(c['bounds'],'#efe3ca')
for r in p['roads']:
    worldline(r['points'],'#c0b49e',r['clearWidth']+16)
    worldline(r['points'],'#f2e7d1',r['clearWidth'])
water=p['water'];worldline(water['centerline'],'#a1b7a4',112);worldline(water['centerline'],'#618f9b',64)
worldrect(water['pondBounds'],'#618f9b','#a1b7a4',6)
for b in p['bridges']:
    worldrect(b['bounds'],'#e3d9be','#605c51',2)
    x,y,w,h=b['bounds'];worldline([[x,y+16],[x+w,y+16]],'#756b59',6);worldline([[x,y+h-16],[x+w,y+h-16]],'#756b59',6)
for seg in p['wall']['segments']:worldline(seg,'#4c5960',p['wall']['thickness'])
for b in p['buildings']:
    worldrect(b['groundReservation'],'#69777b' if b['scaleClass'] in ['civic','ceremonial'] else '#9a7d62','#354a4a',2)
    x,y,w,h=b['groundReservation'];text(*pt((x+12,y+12)),b['code'],14,fill='#fff9e9',weight=True)
    if w>=256:
        size=12
        while ImageFont.truetype(regular,size).getlength(b['label'])>(w-24)*S and size>9:size-=1
        text(*pt((x+12,y+70)),b['label'],size,fill='#fff9e9')
    if b['door']:
        worldline([b['door'],b['approach']],'#faf0c9',40)
        dx,dy=pt(b['door']);rect((dx-4,dy-3,dx+4,dy+3),'#9a472f')
        ax,ay=pt(b['approach']);rect((ax-3,ay-3,ax+3,ay+3),'#9a472f')
text(*pt((1496,600)),'03 · QUẢNG TRƯỜNG',13,weight=True)
text(*pt((1496,650)),'TRUNG TÂM',13,weight=True)
for n in p['npcs']:
    x,y=pt(n['point']);rect((x-5,y-5,x+5,y+5),'#954b5b','#fdf3dc',1)
    text(x+8,y-5,{'sejong':'Sejong','jang':'Jang','yi':'Yi','saimdang':'Saimdang'}[n['id']],12,weight=True)
x,y=pt(p['spawn']);rect((x-6,y-6,x+6,y+6),'#406e91','#fff7de',2);text(x+10,y-8,'ĐIỂM ĐẾN',12,weight=True)
text(*pt((300,2360)),'NƯỚC VÀO →',13,fill='#294b57',weight=True)
text(*pt((3470,2376)),'→ NƯỚC RA',13,fill='#294b57',weight=True)
text(*pt((1450,2570)),'BỜ VƯỜN · ĐƯỜNG ĐI TÁCH MẶT NƯỚC',12)
# Sidebar uses readable short lines, not decorative art pretending to be a playable world.
x=1640
items=[('CẤU TRÚC ĐỀ XUẤT',['Trục cổng → quảng trường.','Đường ngang nối học viện','với phố danh nhân.','Vòng hai cầu tránh đi cụt.']),('ĐƯỜNG & NGÕ',['Chính: 128–160 px thông.','Phố nhánh: 80–96 px.','Ngõ / vườn: 64 px.','Cửa có hành lang riêng.']),('TƯỜNG & NƯỚC',['Tường nối mép bản đồ','vào hai bên cổng cung.','Suối chảy tây → đông.','Chỉ hai cầu được vượt.']),('NHỊP SỐNG KHU PHỐ',['Chợ bám phố, có sân sau.','Học viện có sân yên tĩnh.','Nhà ở dùng ngõ chung.','NPC thuộc sân công trình.']),('CHÚ GIẢI',['Khối xám/nâu: đặt chỗ nhà.','Đường kem: khoảng đi bộ.','Đỏ nhỏ: cửa / điểm tiếp cận.','Hồng: vị trí NPC dự kiến.','Xanh đậm: điểm đến.']),('GIỚI HẠN CỔNG DUYỆT',['Chưa vẽ tài sản mới.','Chưa lắp bản đồ cuối.','Chưa tạo NPC mới.','Chưa merge / deploy.'])]
y=198
for title,lines in items:
    text(x,y,title,18,weight=True);y+=33
    for t in lines:text(x,y,t,15);y+=26
    y+=24
text(64,1378,'Vòng khám phá: Quảng trường → phố danh nhân → cầu đông → ngõ phía nam → sân hội họa → cầu tây → phố sách → học viện.',18,weight=True)
text(64,1418,'Khối nhà thể hiện vị trí & công năng; mái, tán cây, pixel art và collider cuối sẽ được duyệt sau. Sơ đồ không phải bằng chứng chạy Phaser.',17)
text(64,1454,'Đề nghị duyệt: phân khu · mạng đường · hai cầu · ranh cung thành · vị trí từng công trình. Giữ nguyên main và Pages.',17,fill='#986340')
im.save(OUT/'district-zoning-plan.png')
svg.append('</svg>');(OUT/'district-zoning-plan.svg').write_text('\n'.join(svg)+'\n')

# A planning-space clearance check only; no source/runtime colliders or art are generated.
def dist_seg(x,y,a,b):
    vx,vy=b[0]-a[0],b[1]-a[1]; q=((x-a[0])*vx+(y-a[1])*vy)/(vx*vx+vy*vy) if vx or vy else 0
    q=max(0,min(1,q));return math.hypot(x-a[0]-q*vx,y-a[1]-q*vy)
def inrect(x,y,b,margin=0):
    a,c,w,h=b;return a-margin<=x<=a+w+margin and c-margin<=y<=c+h+margin
def near(x,y,points,r):return any(dist_seg(x,y,a,b)<=r for a,b in zip(points,points[1:]))
step=16;walk=set()
for iy in range(H//step):
 for ix in range(W//step):
    x,y=(ix+.5)*step,(iy+.5)*step
    open_=any(near(x,y,r['points'],r['clearWidth']/2-8) for r in p['roads']) or any(inrect(x,y,c['bounds'],-8) for c in p['courts'])
    open_=open_ or any(b['door'] and near(x,y,[b['door'],b['approach']],24) for b in p['buildings'])
    onbridge=any(inrect(x,y,b['bounds'],-8) for b in p['bridges'])
    wet=near(x,y,water['centerline'],56+8) or inrect(x,y,water['pondBounds'],32)
    solid=any(inrect(x,y,b['groundReservation'],8) for b in p['buildings'])
    if (open_ or onbridge) and not solid and (not wet or onbridge):walk.add((ix,iy))
def nearest(q):return min(walk,key=lambda c:((c[0]+.5)*step-q[0])**2+((c[1]+.5)*step-q[1])**2)
start=nearest(p['spawn']);seen={start};todo=deque([start])
while todo:
 x,y=todo.popleft()
 for c in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
    if c in walk and c not in seen:seen.add(c);todo.append(c)
targets=[]
for id,q in [(b['id'],b['approach']) for b in p['buildings']]+[(n['id'],n['point']) for n in p['npcs']]:
 c=nearest(q);offset=math.hypot((c[0]+.5)*step-q[0],(c[1]+.5)*step-q[1]);targets.append({'id':id,'point':q,'nearestCellDistance':round(offset,2),'reachable':c in seen and offset<=32})
# Reserve rectangles of all major buildings must not overlap one another.
overlaps=[]
for i,a in enumerate(p['buildings']):
 for b in p['buildings'][i+1:]:
    x,y,w,h=a['groundReservation'];u,v,s,t=b['groundReservation']
    if x<u+s and u<x+w and y<v+t and v<y+h:overlaps.append([a['id'],b['id']])
invalid_npcs=[n['id'] for n in p['npcs'] if any(inrect(*n['point'],b['groundReservation'],8) for b in p['buildings'])]
report={'npcInsideBuildingReservation':invalid_npcs,'kind':'ZONING_SPACE_ONLY_NOT_RUNTIME_NAV','status':'PASS' if all(t['reachable'] for t in targets) and not overlaps and not invalid_npcs else 'FAIL','sampleCell':step,'walkCells':len(walk),'connectedCells':len(seen),'targets':targets,'overlappingBuildingReservations':overlaps,'limits':['Approximate future ground reservations only; roof alpha, final collision and real Phaser traversal untested for proposed map.','No Forge bundle/nav/Tiled export was executed for this planning gate.','Current game and approved assets are unchanged.']}
(OUT/'planning-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':report['status'],'targets':len(targets),'unreachable':[t for t in targets if not t['reachable']],'overlaps':overlaps,'output':str(OUT/'district-zoning-plan.png')}))
if report['status']!='PASS':raise SystemExit(1)
