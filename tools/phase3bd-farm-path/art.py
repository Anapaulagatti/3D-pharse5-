"""Additive native crop stages and reversible managed-bed pixels; never rewrites originals."""
from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parents[2];S=R/'assets-src/farming/phase3bd-farm-path';O=R/'public/assets/farming/phase3bd-farm-path';S.mkdir(parents=True,exist_ok=True);O.mkdir(parents=True,exist_ok=True)
b=json.loads((R/'assets-src/farming/phase3bd/patterns.json').read_text());patterns=dict(b['patterns']);palette=b['palette']
# Independently finished native leaves at two intermediate growth scales.
patterns.update({
'radish-young':['................']*7+['......ghh.......','.....gHHh.hg....','......ghiHhg....','......giiiig....','.......giig.....','.......ii.......','......cDDc......','......cWDc......','.......cc.......']+['................']*4,
'radish-growing':['................']*5+['......ghhg......','....gHHHh.hg....','.....gHhiHHhg...','.....gghiHHhg...','.......giiig....','......cDDDdc....','......cWWDdc....','......cWWDdc....','.......cDdc.....','........cc......']+['................']*5,
'scallion-young':['................']*5+['......hg.hg.....','......Hi.Hi.....','....g.Hi.Hi.g...','....HiHi.Hi.Hi..','.....HiHiHiHi...','.....HiHiHiHi...','......HiHiHi....','......cWWDc.....','.......cDc......','.......b.b......']+['................']*5,
'scallion-growing':['................']*3+['.....hg...hg....','.....Hi...Hi....','.....Hi.g.Hi.g..','...g.Hi.HiHi.Hi.','...HiHi.HiHi.Hi.','....HiHiHiHi.Hi.','....HiHiHiHiHi..','.....HiHiHiHi...','.....cWWWDDc....','.....cWWWDc.....','......cDDc......','.......cc.......']+['................']*5})
im=Image.new('RGBA',(16*len(patterns),20));frames={}
for n,(name,rows) in enumerate(patterns.items()):
 assert len(rows)==20,(name,len(rows))
 for y,row in enumerate(rows):
  assert len(row)==16,(name,y,len(row))
  for x,ch in enumerate(row):
   if ch!='.':im.putpixel((n*16+x,y),(*bytes.fromhex(palette[ch]),255))
 frames[name]={'frame':{'x':n*16,'y':0,'w':16,'h':20},'rotated':False,'trimmed':False,'spriteSourceSize':{'x':0,'y':0,'w':16,'h':20},'sourceSize':{'w':16,'h':20}}
# Native pixel soil, three visibly cultivated ridges; no interpolation or reference-image resampling.
soil=Image.new('RGBA',(280,88));colors=['786044','82694b','8d7350','987c55','a88a61']
for wet in range(2):
 for y in range(88):
  for x in range(140):
   ridge=y%28;idx=1 if ridge<3 else 3 if ridge in (5,6) else 2
   v=(x*17+y*31+(x//7)*11)%83
   if v<5:idx=max(0,idx-1)
   elif v>77:idx=min(4,idx+1)
   rgb=list(bytes.fromhex(colors[idx]))
   if wet:rgb=[round(rgb[0]*.77),round(rgb[1]*.79),round(rgb[2]*.83)]
   soil.putpixel((x+wet*140,y),(*rgb,255))
for folder in (S,O):
 im.save(folder/'crops.png');soil.save(folder/'soil.png')
 (folder/'crops.json').write_text(json.dumps({'frames':frames,'meta':{'image':'crops.png','size':{'w':im.width,'h':20},'scale':'1'}},indent=2)+'\n')
(S/'patterns.json').write_text(json.dumps({'palette':palette,'patterns':patterns},indent=2)+'\n')
(S/'PROVENANCE.json').write_text(json.dumps({'creator':'Original native pixel finishing by Codex','toolActuallyUsed':'Python/Pillow exact pixel export; no image API','derivedFrom':'Six unchanged approved native crop frames from assets-src/farming/phase3bd/patterns.json; four newly authored intermediate frames; original patterned soil','nativeScale':1,'sampling':'No resize or filtering; binary alpha','scope':'Reversible overlay only inside six approved cropDisplayRect rectangles; no source world pixels modified','hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in O.iterdir()}},indent=2)+'\n')
