from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
R=Path.cwd();O=R/'public/assets/roadmap-v4/ui';S=R/'assets-src/roadmap-v4/ui';O.mkdir(parents=True,exist_ok=True);S.mkdir(parents=True,exist_ok=True)
for name,bg,edge in [('frame-dark','#243e36','#bd9d60'),('frame-paper','#e5d5aa','#705b3c'),('slot','#344b3a','#a98b58')]:
 im=Image.new('RGBA',(24,24));d=ImageDraw.Draw(im);d.rectangle((2,0,21,23),fill=edge);d.rectangle((0,2,23,21),fill=edge);d.rectangle((2,2,21,21),fill='#332f24');d.rectangle((3,3,20,20),fill=bg);d.line((4,3,19,3),fill='#e9cf90');d.line((3,4,3,19),fill='#d0b073');d.line((4,20,20,20),fill='#152f2c');d.line((20,4,20,19),fill='#152f2c')
 for x,y in [(2,2),(20,2),(2,20),(20,20)]:d.rectangle((x,y,x+1,y+1),fill='#f2d99b')
 im.save(O/(name+'.png'));im.save(S/(name+'.png'))
(S/'PROVENANCE.json').write_text(json.dumps({'art_source':'original native code-art nine-slice UI','tool':'tools/roadmap-v4/hud_art.py','providerCalls':0,'thirdPartyReferences':[],'nativeScale':1,'review':'PENDING_HUMAN_REVIEW','sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in O.glob('*.png')}},indent=2)+'\n')
