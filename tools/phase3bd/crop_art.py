"""Original hand-authored native crop pixel clusters; not generated NPC/body artwork."""
from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parents[2];S=R/'assets-src/farming/phase3bd';O=R/'public/assets/farming';S.mkdir(parents=True,exist_ok=True);O.mkdir(parents=True,exist_ok=True)
patterns={
'radish-sown':['................','................','................','................','................','................','................','................','................','................','................','................','................','................','.......ab.......','......acba......','.......ba.......','................','................','................'],
'scallion-sown':['................','................','................','................','................','................','................','................','................','................','................','................','................','......ab.ab.....','......ba.ba.....','................','................','................','................','................'],
'radish-sprout':['................','................','................','................','................','................','................','................','................','................','......ghh.......','.....gHhh.h.....','......ghhHh.....','.......gig......','.......ii.......','......acba......','.......ba.......','................','................','................'],
'scallion-sprout':['................','................','................','................','................','................','................','.......hg.......','.....h.hi.......','.....hHiig......','......hiig......','......hiig......','.......ii.......','.......ii.......','......bcba......','.......ba.......','................','................','................','................'],
'radish-ready':['................','................','................','................','......ghh.......','.....gHHh..hg...','...gHHHhi.gHhg..','....gHhhigHHhg..','.....gghiiHhg...','.......giihg....','......cDDDdc....','.....cDWWDDdc...','.....cWWWWWdc...','.....cWWWWDdc...','......cWWWdc....','.......cDdc.....','........cc......','........b.......','................','................'],
'scallion-ready':['................','.....hg...hg....','.....Hig..Hi....','.....Hii..Hi.g..','...g.Hii.gHi.hg.','...HigHi.HHi.Hi.','...Hi.Hi.HHi.Hi.','...Hi.Hi.HHi.Hi.','....HiHi.Hii.Hi.','....HiHi.HiiHi..','....HiHiiHiiHi..','.....HiHiHiHi...','.....cWWWDDc....','.....cWWWWWc....','......cWWDc.....','.......cDc......','.......b.b......','................','................','................']}
palette={'a':'b99b57','b':'806343','c':'5b543d','g':'385d37','h':'678542','H':'91a252','i':'476c3c','D':'d8ceb0','W':'f4ead0','d':'a39778'}
im=Image.new('RGBA',(96,20));frames={}
for n,(name,rows)in enumerate(patterns.items()):
 assert len(rows)==20
 for y,row in enumerate(rows):
  assert len(row)==16,(name,y,len(row))
  for x,ch in enumerate(row):
   if ch!='.':im.putpixel((n*16+x,y),(*bytes.fromhex(palette[ch]),255))
 frames[name]={'frame':{'x':n*16,'y':0,'w':16,'h':20},'rotated':False,'trimmed':False,'spriteSourceSize':{'x':0,'y':0,'w':16,'h':20},'sourceSize':{'w':16,'h':20}}
for folder in [S,O]:im.save(folder/'crops.png');(folder/'crops.json').write_text(json.dumps({'frames':frames,'meta':{'image':'crops.png','size':{'w':96,'h':20},'scale':'1'}},indent=2)+'\n')
(S/'patterns.json').write_text(json.dumps({'palette':palette,'patterns':patterns},indent=2)+'\n')
(S/'PROVENANCE.json').write_text(json.dumps({'creator':'Original authored native pixel patterns, Codex Phase3BD','tool':'Python/Pillow for exact native raster export; no image-generation API, reference image or third-party sprite','lighting':'upper-left, muted soil/leaf shades matched to existing farm; no source terrain overwrite','dimensions':[96,20],'nativeCells':[16,20],'alpha':'binary','sha256':hashlib.sha256((S/'crops.png').read_bytes()).hexdigest()},indent=2)+'\n')
print('Original native crop atlas exported;6authored16x20frames')
