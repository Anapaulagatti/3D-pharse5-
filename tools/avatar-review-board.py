"""One-page documentary collage. Uses existing actual Phaser screenshots/video frames only."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json,hashlib
R=Path(__file__).resolve().parents[1];Q=R/'quality-reports/chibi-v1';V=Q/'render'
B=Image.new('RGB',(1600,1300),'#f4eddf');d=ImageDraw.Draw(B)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def font(n,b=False):return ImageFont.truetype(BOLD if b else FONT,n)
ink='#303b43';muted='#67726b';accent='#527e76';sources=[]
def text(x,y,s,n=20,c=ink,b=False):d.text((x,y),s,font=font(n,b),fill=c)
def center(x,y,s,n=18,c=ink):d.text((x,y),s,font=font(n),fill=c,anchor='mt')
def panel(x,y,w,h,num,title,sub):
 d.rounded_rectangle((x,y,x+w,y+h),radius=16,fill='#fffcf5',outline='#d7d3c5',width=2)
 text(x+24,y+19,num,16,accent,True);text(x+64,y+16,title,24,ink,True);text(x+24,y+49,sub,15,muted)
def crop(path,box):
 p=R/path if isinstance(path,str) else path
 im=Image.open(p).convert('RGB');out=im.crop(box)
 assert 0<=box[0]<box[2]<=im.width and 0<=box[1]<box[3]<=im.height
 sources.append({'path':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'crop':box,'display_size':list(out.size),'resampling':'none'})
 return out
# Header: straightforward review metadata; the artwork remains untouched.
d.rectangle((0,0,1600,126),fill='#303e47')
text(40,22,'KOREAN ARENA',18,'#b7cec2',True)
text(40,48,'CHIBI AVATAR / REVIEW BOARD',36,'#fff7e4',True)
text(40,98,'Player-only rebuild  •  Original pixel artwork  •  Actual Phaser renders',17,'#c4d0c6')
d.rounded_rectangle((1240,36,1560,84),radius=12,fill='#e6d5b4');center(1400,47,'AWAITING VISUAL APPROVAL',16)
# Old vs new at exactly the same native3x display scale.
panel(40,150,480,300,'01','OLD → NEW','Same camera scale · native 3× crops')
for i,(path,label) in enumerate([('quality-reports/unified-v4/render/idle-closeup.png','OLD / 32×48'),('quality-reports/chibi-v1/render/idle-closeup.png','NEW / 40×56')]):
 x=88+i*218;B.paste(crop(path,(440,388,584,574)),(x,222));center(x+72,417,label,17)
# Authored orientations: front, back, left, right, each from actual keyboard-driven idle.
panel(544,150,1016,300,'02','FOUR DIRECTIONS','Front / back / profiles · actual idle in the town')
samples=json.loads((V/'samples.json').read_text());byfile={s['file']:s['metrics'] for s in samples}
for i,(dr,label) in enumerate([('down','FRONT'),('up','BACK'),('left','LEFT'),('right','RIGHT')]):
 m=byfile[f'direction-{dr}.png'];x,y=m['screenFoot']['x'],m['screenFoot']['y'];pos=590+i*238
 B.paste(crop(V/f'direction-{dr}.png',(x-72,y-180,x+72,y+6)),(pos,222));center(pos+72,417,label,17)
# All four combinations show both hairstyles and both constructed outfits together.
panel(40,474,744,300,'03','2 HAIRSTYLES × 2 OUTFITS','Cloud crop / chestnut knots · courier / academy')
for i,(h,o) in enumerate([(0,0),(0,1),(1,0),(1,1)]):
 pos=58+i*180;B.paste(crop(V/f'outfit-h{h}-o{o}.png',(440,388,584,574)),(pos,546));center(pos+72,741,('Cloud' if h==0 else 'Chestnut')+' / '+('Courier' if o==0 else 'Academy'),13)
# Four exact facial selections with a stationary player and reduced-motion presentation.
panel(808,474,752,300,'04','FOUR EXPRESSIONS','Same avatar, same position · in-engine face layers')
for i,mood in enumerate(['neutral','happy','focused','surprised']):
 m=byfile[f'expression-{mood}.png'];x,y=m['screenFoot']['x'],m['screenFoot']['y'];pos=831+i*180
 B.paste(crop(V/f'expression-{mood}.png',(x-72,y-180,x+72,y+6)),(pos,546));center(pos+72,741,mood.upper(),14)
# Recorded movement and a visible raised-hand celebration; no sprite sheet replacements.
panel(40,798,940,420,'05','IDLE / WALK / RUN / EMOTE','Recorded gameplay poses · motion video included in the review package')
for i,(path,box,label,note) in enumerate([
 (V/'idle-closeup.png',(440,388,584,574),'IDLE','Relaxed stance + blink'),
 (Q/'video-walk-down.png',(502,682,646,868),'WALK','Grounded stepping'),
 (Q/'video-run-left.png',(502,682,646,868),'RUN','Longer stride + lean'),
 (Q/'video-celebrate.png',(502,682,646,868),'EMOTE','Happy face + raised arms')]):
 pos=80+i*220;B.paste(crop(path,box),(pos,896));center(pos+72,1100,label,19);center(pos+72,1135,note,13,muted)
text(64,1182,'Still frames show poses; the accompanying MP4 shows actual movement.',14,muted)
# Smaller actual gameplay view. Exact2:1 nearest reduction of a native2x screenshot.
panel(1004,798,556,420,'06','IN THE CURRENT TOWN','Actual Phaser canvas · normal gameplay view')
p=V/'gameplay-2x.png';im=Image.open(p).convert('RGB');assert im.size==(1024,640)
small=im.resize((512,320),Image.Resampling.NEAREST);B.paste(small,(1026,880));sources.append({'path':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'crop':[0,0,1024,640],'display_size':[512,320],'resampling':'exact2:1 NEAREST reduction for small scene inset'})
text(40,1245,'CHARACTER-CHIBI-001  /  ONE AVATAR, ONE TOWN',17,accent,True)
text(40,1272,'Native avatar pixels retained in all character crops. Town and NPC artwork unchanged.',15,muted)
center(1400,1250,'REVIEW CANDIDATE',16,accent)
out=Q/'avatar-review-board.png';B.save(out,optimize=True)
(Q/'avatar-review-board.sources.json').write_text(json.dumps({'image':out.name,'size':list(B.size),'composition':'Existing actual Phaser screenshots and decoded gameplay frames. No artwork regeneration or pose insertion. Only scene inset reduced2:1 NEAREST.','sources':sources,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()},indent=2)+'\n')
print(str(out));print('Dimensions:',B.size,'bytes:',out.stat().st_size)
