"""Current one-page review: real Phaser crops + explicitly labelled registered atlas views."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,shutil,hashlib
R=Path(__file__).resolve().parents[1];V=R/'.cache/review/render';Q=R/'docs/review';Q.mkdir(parents=True,exist_ok=True)
B=Image.new('RGB',(1600,1640),'#f2ebdc');d=ImageDraw.Draw(B);ink='#303e47';muted='#667369';accent='#527e76';sources=[]
def ft(n,b=False):return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold' if b else '')+'.ttf',n)
def txt(x,y,t,n=18,c=ink,b=False):d.text((x,y),t,font=ft(n,b),fill=c)
def center(x,y,t,n=16):d.text((x,y),t,font=ft(n),fill=ink,anchor='mt')
def panel(x,y,w,h):d.rounded_rectangle((x,y,x+w,y+h),radius=16,fill='#fffcf5',outline='#d5d1c4',width=2)
samples={s['file']:s['metrics'] for s in json.loads((V/'samples.json').read_text())['samples']}
def actual(name,actor=None):
 im=Image.open(V/name).convert('RGB');m=samples[name];x,y=m['screenFoot']['x'],m['screenFoot']['y'];z=m['cameraZoom']
 if actor:
  g=next(g for g in m['guests'] if g['id']==actor);x+=(g['x']-m['x'])*z;y+=(g['y']-m['y'])*z
 x,y=round(x),round(y);box=(x-24*z,y-64*z,x+24*z,y+4*z);assert min(box[:2])>=0 and box[2]<=im.width and box[3]<=im.height,(name,box)
 sources.append({'path':str((V/name).relative_to(R)),'sha256':hashlib.sha256((V/name).read_bytes()).hexdigest(),'crop':box,'kind':'actual Phaser canvas'})
 return im.crop(box)
def source(actor,dr):
 root=R/'assets-src/actors'/actor;f=json.loads((root/'atlas.json').read_text())['frames'][f'idle-{dr}-0']['frame'];im=Image.open(root/'sprite.png').crop((f['x'],f['y'],f['x']+48,f['y']+68));sources.append({'path':str((root/'sprite.png').relative_to(R)),'frame':f'idle-{dr}-0','kind':'registered source atlas, NOT engine capture'});return im.resize((96,136),Image.Resampling.NEAREST)
def paste_alpha(im,x,y):B.paste(im,(x,y),im if im.mode=='RGBA' else None)
d.rectangle((0,0,1600,125),fill=ink);txt(40,22,'KOREAN ARENA / LIVING PIXEL SEOUL',18,'#bfd0c1',True);txt(40,52,'CHIBI ANIMATION + HISTORICAL GUESTS',34,'#fff4dc',True);txt(40,99,'REVIEW CANDIDATE  •  accepted player identity retained  •  fictional educational guests',16,'#cbd7cc')
panel(40,150,1520,535);txt(64,172,'PLAYER / ACTUAL PHASER VIEWS',20,accent,True)
for i,dr in enumerate(['down','up','left','right']):
 im=actual('hero-'+dr+'.png');B.paste(im,(64+i*176,210));center(136+i*176,420,{'down':'FRONT','up':'BACK','left':'LEFT','right':'RIGHT'}[dr])
txt(64,463,'2 HAIRSTYLES × 2 OUTFITS / PHASER',18,accent,True)
for i,(h,o) in enumerate([(0,0),(0,1),(1,0),(1,1)]):
 im=actual(f'outfit-{h}-{o}.png').resize((96,136),Image.Resampling.NEAREST);B.paste(im,(75+i*170,496));center(123+i*170,642,f'Hair{h} / Outfit{o}',14)
txt(840,172,'FOUR EXPRESSIONS / PHASER',20,accent,True)
for i,e in enumerate(['neutral','happy','focused','surprised']):
 im=actual('expression-'+e+'.png').crop((24,12,120,144));B.paste(im,(840+i*164,224));center(888+i*164,379,e.upper(),13)
txt(840,438,'WALK ≠ RUN / REGISTERED SOURCE POSES',17,accent,True)
# Source poses are explicitly distinguished from actual engine crops and motion video.
from avatar_art import composite
for i,(a,j) in enumerate([('walk',0),('walk',4),('run',0),('run',4)]):
 im=composite(f'{a}-right-{j}').resize((96,136),Image.Resampling.NEAREST);paste_alpha(im,840+i*164,478);center(888+i*164,628,f'{a.upper()} / {j}',14)
panel(40,705,940,885);txt(64,726,'HISTORICAL GUESTS / ATLAS VIEWS + REAL GREETINGS',18,accent,True)
for x,t in [(258,'FRONT'),(378,'BACK'),(498,'LEFT'),(618,'RIGHT'),(798,'PHASER GREETING')]:center(x,758,t,12)
for row,(actor,name,role) in enumerate([('sejong','Sejong','Hangul / language'),('jang','Jang Yeong-sil','Science / inventions'),('saimdang','Shin Saimdang','Art / nature'),('yi','Yi Sun-sin','Strategy / teamwork')]):
 y=792+row*195;txt(60,y+35,name,16,ink,True);txt(60,y+62,role,11,muted)
 for i,dr in enumerate(['down','up','left','right']):paste_alpha(source(actor,dr),210+i*120,y)
 im=actual('greeting-'+actor+'.png',actor).resize((96,136),Image.Resampling.NEAREST);B.paste(im,(750,y))
 center(798,y+141,'happy / greeting',12)
panel(1004,705,556,885);txt(1028,726,'ACTUAL IN-GAME TOWN',20,accent,True)
im=Image.open(V/'town.png').convert('RGB').resize((512,320),Image.Resampling.NEAREST);B.paste(im,(1026,780))
txt(1028,1130,'ONE CURRENT PLAYABLE GAME',20,accent,True)
for j,t in enumerate(['Four local historical guests, from different eras.','Original costumes and props; no copied portraits.','Idle / blink / walk / greeting / themed gestures.','Vietnamese-first dialogue + beginner Korean.','One concept-only learning hook per guest.','','Player: start / stop / turn / distinct run,','wave / celebrate / think / social pose.','Motion is shown in the real before/after MP4.','','Transparent motion padding preserves identity.','World pixels and collision map retained.','No online players or full quests in this review.']):txt(1028,1170+j*25,t,15,muted)
txt(40,1605,'Native pixel art. Character crops use exact integer pixel display; atlas views are source, greetings/town are actual Phaser.',14,muted)
B.save(Q/'avatar-review-board.png',optimize=True)
for name in ['town.png','mobile.png']:shutil.copy2(V/name,Q/name)
(Q/'board-sources.json').write_text(json.dumps({'method':'Actual renderer crops and explicitly labelled source-atlas views; NEAREST only. No pose injection or regenerated illustration.','sources':sources},indent=2)+'\n');print('Current avatar/NPC board saved1600×1640; latest town/mobile screenshots retained.')
