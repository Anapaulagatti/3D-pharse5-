"""Only compose/crop real Phaser frames; nearest integer overview exports."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageChops
import hashlib
import json
import shutil

R=Path(__file__).resolve().parents[1]
D=R/'docs/final-map-lock'
Q=D/'quality'
before=R/'docs/v6-path-fix/quality/after'
after=Q/'after'
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',20)
def save(im,path):im.save(path)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
full=Image.open(after/'full-map-native.png').convert('RGB')
assert full.size==(4352,5312)
save(full,D/'FINAL_LOCK_OVERVIEW.png')
save(full.resize((2176,2656),Image.Resampling.NEAREST),D/'FINAL_LOCK_OVERVIEW_WEB.png')
save(full.resize((1088,1328),Image.Resampling.NEAREST),D/'FINAL_LOCK_OVERVIEW_SMALL.png')
names=['civic-transition','modern-forecourt','park-hall-passage','pier-approach','island-garden','island-coast-loop']
rows=[]
for name in names:
    old=Image.open(before/f'{name}-native.png').convert('RGB')
    new=Image.open(after/f'{name}-native.png').convert('RGB')
    assert old.size==new.size==(1024,768)
    board=Image.new('RGB',(2072,816),'#182829');draw=ImageDraw.Draw(board)
    draw.text((12,12),'APPROVED V6 / BEFORE',font=font,fill='white')
    draw.text((1048,12),'FINAL MAP LOCK / AFTER / NATIVE 1:1',font=font,fill='white')
    board.paste(old,(8,40));board.paste(new,(1040,40))
    save(board,D/f'{name.upper().replace("-","_")}_BEFORE_AFTER.png')
    rows.append({'name':name,'before':str((before/f'{name}-native.png').relative_to(R)),'beforeSha256':sha(before/f'{name}-native.png'),'after':str((after/f'{name}-native.png').relative_to(R)),'afterSha256':sha(after/f'{name}-native.png'),'nativeSize':[1024,768],'method':'Matched same-position/zoom/viewport/DPR/renderer real Phaser frames, no resampling; BEFORE inherited verbatim from approved2df01bf review. Paused native still framing, not traversal proof.'})
# Unchanged heritage must remain exact under the same normal capture method.
for renderer in ['canvas','webgl']:
    name=f'v6-{renderer}-native-1x-native.png'
    a=Image.open(before/name).convert('RGB');b=Image.open(after/name).convert('RGB')
    assert ImageChops.difference(a,b).getbbox()is None,('Unchanged heritage native frame changed',renderer)
(Q/'comparison-provenance.json').write_text(json.dumps({'status':'PASS','baseline':'2df01bf215e0355cc1fed20b58779d5d0b740683','nativeComparisons':rows,'heritageCanvasAndWebGLExact':True,'overviewMethod':'Actual native4352x5312Phaser frame; exact integer nearest2:1/4:1copies only.'},indent=2)+'\n')
print(json.dumps({'nativeBoards':len(rows),'full':list(full.size),'heritageExact':True}))
