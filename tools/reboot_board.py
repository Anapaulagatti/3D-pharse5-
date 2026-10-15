"""One review collage: generated masters and clearly labelled actual Phaser crops."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
Q=ROOT/'docs/character-reboot'
report=json.loads((Q/'browser-verification.json').read_text())
samples={s['name']:s['metrics'] for s in report['samples']}
board=Image.new('RGB',(1600,2060),'#eee8da');draw=ImageDraw.Draw(board)
sources=[]
ink='#2b403d';muted='#718174';accent='#557b68'
def font(size,bold=False):return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold' if bold else '')+'.ttf',size)
def text(x,y,s,size=17,color=ink,bold=False):draw.text((x,y),s,font=font(size,bold),fill=color)
def centered(x,y,s,size=17,color=ink,bold=False):draw.text((x,y),s,font=font(size,bold),fill=color,anchor='mt')
def source(path,kind,box=None):
    image=Image.open(path).convert('RGBA')
    sources.append({'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'kind':kind,'crop':box})
    return image.crop(box) if box else image
def engine(key,view,zoom=2,head=False):
    name='phaser-'+view if zoom==2 else 'phaser-native'
    m=samples[name];foot=next(c['foot'] for c in m['candidates'] if c['id']==key)
    x,y=round(foot['x']),round(foot['y'])
    if head:box=(x-45,y-160,x+45,y-94)
    else:box=(x-27*zoom,y-88*zoom,x+27*zoom,y+4*zoom)
    return source(Q/(name+'.png'),'actual Phaser canvas crop; no inserted sprite',box)

draw.rectangle((0,0,1600,128),fill=ink)
text(40,22,'KOREAN ARENA / CHARACTER REBOOT',18,'#b9cbbd',True)
text(40,53,'THREE ORIGINAL CHARACTERS',34,'#fff5df',True)
text(40,99,'USER APPROVAL PENDING  /  shared scale and town  /  static design proof, not an animation set',15,'#cad5c6')
names={'A':('Bori','EXPRESSIVE ADVENTURE','Sculpted cowlick / compact athletic shape'),
       'B':('Juni','PREMIUM SOCIAL RPG','Loop buns / diamond face / long fashion shape'),
       'C':('Nari','KOREAN FANTASY','Side braid / heart face / layered Korean styling')}
for i,key in enumerate('ABC'):
    left=40+i*520;cx=left+240
    draw.rounded_rectangle((left,150,left+480,645),radius=16,fill='#fffbf1',outline='#d0d0bf',width=2)
    text(left+22,170,key,30,accent,True);centered(cx,175,names[key][0],30,bold=True)
    centered(cx,216,names[key][1],14,accent,True)
    master=source(ROOT/f'assets-src/character-reboot/{key}/master-front/master_rgba.png','generated source master, NOT gameplay')
    master=master.crop(master.getbbox());w=round(master.width*355/master.height)
    master=master.resize((w,355),Image.Resampling.LANCZOS)
    board.paste(master,(cx-w//2,247),master)
    centered(cx,615,'GENERATED SOURCE MASTER',13,muted)
    centered(cx,659,names[key][2],15,accent)
    head=engine(key,'front',head=True).resize((180,132),Image.Resampling.NEAREST)
    board.paste(head,(cx-90,704))
    centered(cx,846,'4× PIXEL DETAIL / ACTUAL PHASER CROP',12,muted)
    for j,view in enumerate(['front','back','left','right']):
        frame=engine(key,view);board.paste(frame,(left+12+j*114,901))
        centered(left+66+j*114,1095,view.upper(),12)
    centered(cx,1124,'FOUR DIRECTIONS / ACTUAL PHASER 2×',12,accent,True)
    native=engine(key,'front',zoom=1);board.paste(native,(cx-native.width//2,1163))
    centered(cx,1266,'1× NATIVE / 80 PX BODY',12,muted)

text(40,1320,'ACTUAL PHASER / EXISTING CENTRAL PLAZA / CAMERA 2×',20,accent,True)
town=source(Q/'phaser-front.png','actual full Phaser canvas, pasted at original screenshot pixels')
board.paste(town,((1600-town.width)//2,1365))
text(40,2030,'Host image_gen → Forge master/finish/palette/export → Phaser. World and production actors unchanged. Choose A, B or C before motion/NPC production.',13,muted)
board.save(Q/'avatar-review-board.png',optimize=True)
(Q/'board-sources.json').write_text(json.dumps({'method':'Source masters explicitly labelled, all pixel-detail/direction/native/world panels are actual Phaser captures. NEAREST only for pixel-detail enlargement; source masters alone use LANCZOS downscale. No screenshot compositing of a replacement sprite into a scene.','sources':sources},indent=2)+'\n')
print('Saved avatar-review-board.png 1600×2060; generated source art and actual gameplay scale are labelled separately.')
