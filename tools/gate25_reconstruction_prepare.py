from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate25-reconstruction';D=R/'docs/gate25-reconstruction';im=Image.open(S/'original-ground.png').convert('RGB');W,H=im.size
# Source-coordinate architectural envelopes. Each preserves complete roofs, faces, signs and doors,
# including native attached balcony/rooftop garden furnishings, while excluding public side passages.
polys=[dict(id='muneum-cafe-bookshop-academy',points=[[35,200],[450,200],[450,235],[780,235],[780,195],[1045,195],[1085,245],[1085,755],[35,755]]),dict(id='muneum-convenience',points=[[1080,286],[1450,286],[1475,335],[1475,756],[1080,756]]),dict(id='bakery',points=[[1570,0],[2428,0],[2440,125],[2440,535],[2441,540],[2441,575],[2432,744],[2408,762],[1565,762],[1565,580],[1537,574],[1537,539],[1568,531],[1568,362],[1550,351],[1550,320],[1568,310]]),dict(id='station',points=[[2555,303],[2650,283],[3000,283],[3090,320],[3105,424],[3140,429],[3140,692],[3090,704],[2546,704],[2546,460],[2539,460],[2539,423]])]
polys.extend([dict(id='convenience-projecting-sign',points=[[1457,401],[1477,401],[1477,416],[1500,416],[1500,516],[1457,516]]),dict(id='station-platform-canopy',points=[[3110,300],[3183,300],[3183,735],[3110,735]])])
mask=Image.new('L',(W,H));draw=ImageDraw.Draw(mask)
for p in polys:draw.polygon([tuple(v)for v in p['points']],fill=255)
mask.save(S/'architecture-protection.png');(S/'architecture-envelopes.json').write_text(json.dumps(polys,indent=2)+'\n')
# Guide holes intentionally are not gameplay artwork; source architecture is restored exactly after authoring.
guide=im.copy();guide.paste((227,90,166),(0,0),mask);draw=ImageDraw.Draw(guide);draw.rectangle((0,835,W-1,955),outline='#20d5e3',width=3)
# A small empty paved planting socket off the through route, not on either technical seam.
draw.ellipse((1590,1065,1690,1145),outline='#20d5e3',width=4)
guide.save(S/'environment-authoring-guide.png')
# Full-height diagnosis: positions confirmed from current runtime metadata, no obsolete ownership assumption.
sc=json.loads((R/'public/assets/gate2/district-polish/scene.json').read_text());assert [g['x']for g in sc['grounds']]==[0,1512,2488]
defects=[('W1','MAJOR',[1300,0,285,330],'Rear paving scale changes and truncated background foliage','One rear promenade / complete low planting bays'),('W2','CRITICAL',[1400,300,200,360],'Baked tree/ivy reads as rootless stems behind convenience store','Clear side passage; remove obsolete baked greenery'),('W3','CRITICAL',[1370,610,260,220],'Restored tree overlaps unrelated baked tree, bikes and pot','Remove wrong derived placement; one properly rooted complete object'),('W4','MAJOR',[1300,820,450,150],'Road/pavement texture and shadow treatment changes','Unified street geometry and material plane'),('W5','CRITICAL',[1320,945,480,265],'Straight red/cream garden split, broken wall/cap construction','Connected terrace garden, deliberate path and continuous low walls'),('W6','MAJOR',[1400,1000,160,190],'Imported lamp belongs to old garden, not current wall/path','Remove/relocate furniture with coherent ground contact'),('E1','MAJOR',[2330,0,410,355],'Rear vegetation density and paving ownership edge','Shared rear promenade and planting rhythm'),('E2','CRITICAL',[2410,340,200,430],'Dark vertical side strip, floating/baked foliage between facades','Reconstruct open intentional service passage and contact shadows'),('E3','MAJOR',[2380,710,400,125],'Forecourt to sidewalk scale/contact discontinuity','Single paving grammar with connected station plaza'),('E4','MAJOR',[2260,825,550,150],'Curbs/road paint/asphalt and crossing transitions','One continuous street/curb profile; fixed crossing access'),('E5','CRITICAL',[2220,950,620,260],'Stacked lower garden composition, capstones and density disagree','Continuous terrace construction across source origin')]
(D/'diagnosis.json').write_text(json.dumps(dict(runtimeScene='district-polish',runtimeGrounds=sc['grounds'],joins=[1512,2488],defects=[dict(id=i,severity=s,rect=r,defect=d,correction=c)for i,s,r,d,c in defects],humanDecision='PRIOR POLISH REJECTED / technical PASS did not approve art'),indent=2)+'\n')
board=Image.open(R/'docs/gate25-polish/AFTER_NATIVE_1X.png').convert('RGB');dr=ImageDraw.Draw(board);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',25)
for i,severity,r,d,c in defects:
 x,y,w,h=r;color='#ff735e'if severity=='CRITICAL'else'#ffe18c';dr.rectangle((x,y,x+w,y+h),outline=color,width=4);dr.text((x+6,y+6),i,font=font,fill=color,stroke_width=2,stroke_fill='#173c49')
for x in [1512,2488]:dr.line((x,0,x,H),fill='#7ce5e5',width=3)
board.resize((1592,607)).save(D/'SEAM_DEFECT_MAP.jpg',quality=89,optimize=True)
# Architectural protection overlay for explicit mask review.
overlay=Image.new('RGB',(W,H),'#173c49');overlay.paste(im,(0,0),mask);overlay.resize((1592,607)).save(D/'PROTECTED_ARCHITECTURE.jpg',quality=90,optimize=True)
print('Confirmed runtime joins1512/2488;11 full-height defect regions and architecture guide saved')
