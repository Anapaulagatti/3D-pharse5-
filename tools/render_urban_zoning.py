"""Editable zoning/footprint diagrams only. No game art, runtime map or provider calls."""
from pathlib import Path
import json
import math
import html
import textwrap
from PIL import Image, ImageDraw, ImageFont
from check_urban_zoning import check

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/urban-zoning'
p=json.loads((OUT/'zoning-plan.json').read_text())
REGULAR='/usr/share/fonts/truetype/open-sans/OpenSans-Regular.ttf'
BOLD='/usr/share/fonts/truetype/open-sans/OpenSans-Bold.ttf'


class Diagram:
    def __init__(self,size):
        self.image=Image.new('RGB',size,'#f7f3e9');self.d=ImageDraw.Draw(self.image)
        self.svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{size[0]}" height="{size[1]}" viewBox="0 0 {size[0]} {size[1]}"><rect width="100%" height="100%" fill="#f7f3e9"/>']
    def group(self,name):self.svg.append(f'<g id="{html.escape(name)}">')
    def end(self):self.svg.append('</g>')
    def text(self,x,y,t,size=18,color='#263e3b',bold=False):
        t=t.replace('→','>');font=ImageFont.truetype(BOLD if bold else REGULAR,size)
        self.d.text((x,y),t,font=font,fill=color)
        self.svg.append(f'<text x="{x:.2f}" y="{y+size:.2f}" font-family="Open Sans,sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}">{html.escape(t)}</text>')
    def box(self,b,fill,outline=None,width=1):
        x,y,w,h=b;self.d.rectangle((x,y,x+w,y+h),fill=fill,outline=outline,width=width)
        self.svg.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{fill or "none"}" stroke="{outline or "none"}" stroke-width="{width}"/>')
    def poly(self,points,fill,outline=None,width=1):
        self.d.polygon(points,fill=fill)
        if outline:self.d.line(points+[points[0]],fill=outline,width=width,joint='curve')
        self.svg.append(f'<polygon points="{" ".join(f"{x:.2f},{y:.2f}" for x,y in points)}" fill="{fill}" stroke="{outline or "none"}" stroke-width="{width}"/>')
    def line(self,points,color,width=1,dash=False):
        if not dash:self.d.line(points,fill=color,width=max(1,round(width)),joint='curve')
        else:
            # Exact same centerline, visually dashed only; no new geometry/route implied.
            walked=0
            for (x,y),(u,v) in zip(points,points[1:]):
                length=math.hypot(u-x,v-y)
                if length:
                    for i in range(math.ceil(length)):
                        if (int(walked+i)//10)%2==0:
                            a=i/length;b=min(1,(i+1)/length);self.d.line([(x+(u-x)*a,y+(v-y)*a),(x+(u-x)*b,y+(v-y)*b)],fill=color,width=max(1,round(width)))
                    walked+=length
        self.svg.append(f'<polyline points="{" ".join(f"{x:.2f},{y:.2f}" for x,y in points)}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linejoin="round"'+(' stroke-dasharray="10 10"' if dash else '')+'/>')
    def dot(self,x,y,r,fill,outline=None):
        self.d.ellipse((x-r,y-r,x+r,y+r),fill=fill,outline=outline,width=1)
        self.svg.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{fill}" stroke="{outline or "none"}"/>')
    def save(self,stem):
        self.image.save(OUT/(stem+'.png'));(OUT/(stem+'.svg')).write_text('\n'.join(self.svg+['</svg>'])+'\n')


def draw_building(fig,b,point,scale,labels=True):
    fig.group('building-'+b['id'])
    for i,m in enumerate(b['masses']):
        x,y,w,h=m['bounds'];sx,sy=point((x,y));color=['#9b7e63','#af9476','#b7a48a'][min(i,2)]
        if b['id'] in ['gate','monument','museum','pavilion']:color=['#718080','#91a09c','#a1aaa1'][min(i,2)]
        fig.box([sx,sy,w*scale,h*scale],color,'#475651',2)
        roof=m['roof']
        if roof not in ['no roof','unroofed platform']:
            if m['ridgeDirection']=='east-west':r=[(sx+8,sy+h*scale*.43),(sx+w*scale-8,sy+h*scale*.43)]
            else:r=[(sx+w*scale*.5,sy+8),(sx+w*scale*.5,sy+h*scale-8)]
            if w*scale>20 and h*scale>20:fig.line(r,'#eadbc4',2)
            fig.line([(sx+3,sy+h*scale-3),(sx+w*scale-3,sy+h*scale-3)],'#4c5a56',3)
    if labels:
        x,y,w,h=b['masses'][0]['bounds'];sx,sy=point((x,y))
        label_fill='#718080' if b['id'] in ['gate','monument','museum','pavilion'] else '#9b7e63'
        fig.box([sx+3,sy+3,min(w*scale-6,170),42 if w*scale>70 else 20],label_fill)
        fig.text(sx+6,sy+5,b['code'],14,'#fff8e9',True)
        if w*scale>70:
            size=14
            while ImageFont.truetype(REGULAR,size).getlength(b['label'])>w*scale-12 and size>10:size-=1
            fig.text(sx+6,sy+25,b['label'],size,'#fff8e9')
    for platform in b.get('platforms',[]):
        x,y,w,h=platform['bounds'];sx,sy=point((x,y));fig.box([sx,sy,w*scale,h*scale],'#ded5bb','#8a9387')
    if b['door']:
        for a,z in [(b['door'],b['approach'])]+([(b['innerDoor'],b['door'])] if b.get('innerDoor') else []):fig.line([point(a),point(z)],'#a64f3e',2,dash=True)
        for q in [b['door']]+([b['innerDoor']] if b.get('innerDoor') else []):
            x,y=point(q);fig.box([x-5,y-3,10,6],'#923f31')
    fig.end()


fig=Diagram((2496,1880));S,OX,OY=.47,64,220
pt=lambda q:(OX+q[0]*S,OY+q[1]*S)
wp=lambda q:[pt(v) for v in q]
box=lambda b:(*pt(b[:2]),b[2]*S,b[3]*S)
fig.text(64,28,'LIVING SEOUL · TINH CHỈNH QUY HOẠCH',40,bold=True)
fig.text(64,88,'VÒNG DUYỆT 2 · Phân khu được chấp nhận sơ bộ; bản tinh chỉnh vẫn cần duyệt trước khi dựng map.',22,'#965c3c',True)
fig.text(64,130,'4096 × 3072 px đề xuất  |  Trục nghi lễ thẳng + phố theo khu đất  |  Juni giữ 80 px  |  Không đổi game hiện tại',20)
fig.text(64,168,'SƠ ĐỒ KHỐI NỀN / MÁI / ĐƯỜNG · Không phải pixel art hoàn thiện hoặc ảnh chạy Phaser',18,'#657069')
fig.box([OX,OY,4096*S,3072*S],'#e9e5d7','#a5ad9c',2)
for z in p['zones']:
    fig.group('zone-'+z['id']);fig.poly(wp(z['polygon']),z['color']);fig.end()
for l in p['landscapeParcels']:
    fig.group('landscape-'+l['id']);fig.poly(wp(l['polygon']),'#d2dcc3','#acbba0');fig.end()
for c in p['courts']:
    fig.group('court-'+c['id']);fig.poly(wp(c['polygon']),'#f1e4c8');fig.end()
for r in p['roads']:
    fig.group('road-'+r['id']);fig.line(wp(r['points']),'#c9bfa7',(r['clearWidth']+16)*S);fig.line(wp(r['points']),'#f5eacf',r['clearWidth']*S);fig.end()
w=p['water'];fig.group('stream-and-banks');fig.line(wp(w['centerline']),'#b0c1aa',(w['clearWidth']+48)*S);fig.poly(wp(w['pondPolygon']),'#79a3a5','#b0c1aa',round(48*S));fig.line(wp(w['centerline']),'#729ba5',w['clearWidth']*S);fig.poly(wp(w['pondPolygon']),'#729ba5');fig.end()
for bridge in p['bridges']:
    fig.group(bridge['id']);fig.box(box(bridge['bounds']),'#d8c6a3','#66766b',2)
    x,y,ww,hh=bridge['bounds']
    for xx in [x+8,x+ww-8]:fig.line(wp([[xx,y],[xx,y+hh]]),'#786e5e',2)
    fig.end()
# Closed palace is a specific compound, not a wall running through ordinary neighborhoods.
pal=p['palace'];fig.group('palace-context-closed');fig.box(box(pal['bounds']),'#d4d3c7')
for c in pal['contextCourts']:fig.box(box(c['bounds']),'#eee3c9')
fig.line(wp(pal['contextAxis']),'#b89d68',2,dash=True)
for c in pal['contextMasses']:
    fig.box(box(c['bounds']),'#acb1a7','#7b877a')
    x,y=pt(c['bounds'][:2]);fig.text(x+4,y+4,c['label'],12,'#46534b',True)
for seg in pal['segments']:fig.line(wp(seg['points']),'#4a6062',pal['wallThickness']*S)
for gate in pal['gates']:
    if 'bounds' in gate:
        fig.box(box(gate['bounds']),'#9a876b','#485a59',2)
        fig.line(wp(gate['boundaryLine']),'#6c573e',4)
fig.end()
for b in p['buildings']:draw_building(fig,b,pt,S)
# Exploration overlay stays on authored roads; it is not a shortcut across masses or water.
fig.group('exploration-main-loop');route=p['explorationRoutes'][1]['points'];fig.line(wp(route),'#a97939',2,dash=True)
for i in [1,5,10,13,17,22,25]:
    a,z=route[i],route[i+1];mx,my=pt(((a[0]+z[0])/2,(a[1]+z[1])/2));ang=math.atan2(z[1]-a[1],z[0]-a[0]);r=8
    fig.poly([(mx+math.cos(ang)*r,my+math.sin(ang)*r),(mx+math.cos(ang+2.5)*r,my+math.sin(ang+2.5)*r),(mx+math.cos(ang-2.5)*r,my+math.sin(ang-2.5)*r)],'#a97939')
fig.end()
# Zone labels are on explicit clear margins rather than at every parcel's top-left corner.
for z in p['zones']:
    x,y=pt(z['labelAt']);fig.text(x,y,z['label'],17,bold=True)
for n in p['npcs']:
    x,y=pt(n['point']);fig.dot(x,y,6,'#9b5670','#fff5db');fig.text(x+10,y-10,{'sejong':'Sejong','jang':'Jang','yi':'Yi','saimdang':'Saimdang'}[n['id']],14,bold=True)
for d in p['discoveries']:
    # Small hollow dots are places/uses to discover; none are generated props or quests.
    x,y=pt(d['point']);fig.dot(x,y,4,'#f9efd9','#967549')
x,y=pt(p['spawn']);fig.box([x-6,y-6,12,12],'#3e6b89','#fff7db',2);fig.text(x+10,y-12,'ĐẾN / GẶP GỠ',13,bold=True)
fig.text(*pt((64,2070)),'NƯỚC VÀO >',14,'#426874',True);fig.text(*pt((3584,2392)),'> NƯỚC RA',14,'#426874',True)
fig.text(*pt((1800,2450)),'HỒ THÔNG DÒNG',13,'#eaf1df',True)
fig.text(*pt((1344,656)),'TƯỜNG HỒI',11,'#4a6062',True)
for q,t in [([224,128],'VƯỜN HỌC VIỆN'),([3104,96],'SÂN VẬT LIỆU'),([1568,2976],'VƯỜN THẢO MỘC'),([192,2320],'VƯỜN BỜ SUỐI')]:fig.text(*pt(q),t,12,'#647858',True)
# Cardinal and scale legends.
fig.text(1855,165,'BẮC ↑'.replace('↑','^'),20,bold=True)
fig.line([(OX+12,OY+3072*S-24),(OX+12+320*S,OY+3072*S-24)],'#526c64',4);fig.text(OX+12,OY+3072*S-52,'320 px quy hoạch',13)
sidebar=[('ĐÃ SỬA THEO REVIEW',['Tường hồi bao khu cung riêng.','Cổng chính + hai cổng phục vụ.','Sân trong / cổng trong có thứ tự.','Không có thành bao khu dân cư.']),('ĐƯỜNG CÓ NGUYÊN NHÂN',['Trục nghi lễ giữ thẳng 160 px.','Phố chính 112 px men sân nhà.','Nhánh 80–96 px; ngõ/vườn 64 px.','Ngõ nối theo hiên, bếp, bờ nước.']),('CÔNG TRÌNH KHÁC NHAU',['U học viện; L xưởng dụng cụ.','Nhà sử liệu dài + tiền sảnh lệch.','Cửa hàng sâu, hiên trà mở.','Nhà U / L / hai nếp / giếng chung.','Mái / mặt tiền xem bảng chi tiết.']),('MẶT NƯỚC LIỀN MẠCH',['Suối qua hồ, vào tây / ra đông.','Bờ đá gần chợ; đất/cây bờ ở vườn.','Chỉ hai cầu nối vòng đi bộ.','Không dùng nước để chia ô phố.']),('KHÁM PHÁ & MẬT ĐỘ',['22 điểm sử dụng / khám phá.','Sân học, sân nghề, vườn rau bếp.','Đường vòng ngắn + vòng hai cầu.','Không tạo quest hay NPC mới.']),('CHÚ GIẢI',['Nâu/xám: khối nền + hướng mái.','Đỏ: cửa; nét đỏ đứt: tiếp cận.','Nét vàng đứt: vòng khám phá.','Chấm hồng: vị trí NPC dự kiến.','Chấm rỗng: góc khám phá.','Xanh nhạt: bờ bảo vệ mặt nước.']),('THAM KHẢO ĐÃ ĐỌC',['R1: KHS · Gyeongbokgung.','R2: UNESCO · Changdeokgung.','R3: UNESCO · Seowon.','R4: UNESCO · Hahoe/Yangdong.','Khu phố hư cấu; không phục dựng.'])]
x,y=2040,220
for title,lines in sidebar:
    fig.text(x,y,title,21,bold=True);y+=36
    for t in lines:fig.text(x,y,t,17);y+=29
    y+=27
fig.text(64,1702,'Duyệt lần này: ranh cung thành, hình khối/mái từng công trình, ngõ theo khu đất, hai cầu, sân và vòng khám phá.',22,bold=True)
fig.text(64,1744,'Chưa tạo buildings/tiles/NPC mới; chưa lắp map, merge main hay deploy. Giữ nguyên Juni và toàn bộ bản chơi đang hoạt động.',19,'#965c3c')
fig.text(64,1785,'JSON là dữ liệu quy hoạch; SVG có nhóm ID riêng để chỉnh sửa. Kiểm tra hình học sơ bộ không thay thế Forge nav hoặc Phaser.',18)
fig.save('district-zoning-plan')

# Same-scale footprint comparison, not a concept illustration or generated asset sheet.
board=Diagram((2400,1540));board.text(48,24,'15 HÌNH KHỐI · MÁI · CỬA · SÂN KHÁC NHAU',32,bold=True)
board.text(48,76,'Sơ đồ đặt chỗ kiến trúc cùng tỉ lệ · khối nền/mái, không phải sprites hoàn thiện · mặt tiền chính nằm ngang',19)
for i,b in enumerate(p['buildings']):
    col,row=i%5,i//5;cx,cy=32+col*474,124+row*450
    board.group('card-'+b['id']);board.box([cx,cy,458,430],'#eee8db','#c3c8b8')
    board.text(cx+14,cy+12,b['code']+' · '+b['label'],20,bold=True)
    # Place every card at the same0.36 world->diagram scale, centered on its reservation/court union.
    points=[v for c in [b['courtyard']] for v in c]
    points += [[m['bounds'][0],m['bounds'][1]] for m in b['masses']]+[[m['bounds'][0]+m['bounds'][2],m['bounds'][1]+m['bounds'][3]] for m in b['masses']]
    points += [b['approach']]
    xmin,ymin=min(q[0] for q in points),min(q[1] for q in points);xmax,ymax=max(q[0] for q in points),max(q[1] for q in points)
    scale=.36;dx=cx+229-(xmax+xmin)*scale/2;dy=cy+60-ymin*scale
    transform=lambda q:(dx+q[0]*scale,dy+q[1]*scale)
    board.poly([transform(q) for q in b['courtyard']],'#f8ebcd')
    draw_building(board,b,transform,scale,labels=False)
    board.text(cx+14,cy+320,'Cửa/sân riêng · '+', '.join(b['references']),14,'#785c3d')
    # Original planning descriptions are wrapped, not embedded into the final game artwork.
    for j,t in enumerate(textwrap.wrap(b['roofArrangement'],width=48)[:3]):board.text(cx+14,cy+346+j*21,t,13)
    board.end()
board.text(48,1504,'Đường trắng trên khối: hướng sống mái; nét đáy đậm: mặt trước. Tán mái/chiều cao/collider cuối sẽ được duyệt ở bước art sau.',16)
board.save('building-footprints')
report=check(p)
print(json.dumps({'diagram':'district-zoning-plan.png','footprints':'building-footprints.png','planningStatus':report['status'],'reachableTargets':sum(t['reachable'] for t in report['targets']),'targets':len(report['targets'])}))
if report['status']!='PASS':raise SystemExit(1)
