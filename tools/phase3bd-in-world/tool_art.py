from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
O=Path('public/assets/farming');S=Path('assets-src/farming/phase3bd-in-world');S.mkdir(parents=True,exist_ok=True)
names=['seed-pouch','water-can','water-can-pour','sickle','parcel','tangerine','coin','basket'];atlas=Image.new('RGBA',(128,20));frames={};instructions={}
for i,name in enumerate(names):
 im=Image.new('RGBA',(16,20));d=ImageDraw.Draw(im);ops=[]
 def rect(box,color):d.rectangle(box,fill='#'+color);ops.append([list(box),color])
 if name=='seed-pouch':
  rect((3,7,12,16),'514b37');rect((4,8,11,15),'b49a62');rect((4,8,5,12),'e0ca8f');rect((9,11,11,15),'897249');rect((6,5,9,6),'819452');rect((7,9,8,13),'687b45');rect((5,10,10,11),'687b45')
 elif name.startswith('water-can'):
  rect((3,6,10,14),'344e57');rect((4,7,9,13),'6d9298');rect((4,7,5,10),'a8c0bb');rect((1,8,3,8),'536d73');rect((1,9,1,12),'536d73');rect((1,13,3,13),'536d73');rect((10,9,12,10),'6d9298');rect((12,7,13,9),'8baaad');rect((13,6,14,7),'becac1');rect((5,5,8,6),'738f8f')
  if name.endswith('pour'):rect((14,9,14,10),'8dcbd4');rect((13,13,13,14),'6bb0c2')
 elif name=='sickle':
  rect((5,10,6,17),'544633');rect((5,10,5,15),'bb945c');rect((6,5,11,6),'394d51');rect((11,6,12,8),'829da1');rect((6,5,10,5),'d0d5b9');rect((5,6,6,9),'b7c6b4');rect((7,7,10,7),'778d89')
 elif name=='parcel':
  rect((2,6,13,15),'5b4939');rect((3,6,12,14),'bca16c');rect((3,6,12,7),'deca90');rect((10,8,12,14),'a38252');rect((7,6,8,14),'ddcda3');rect((3,10,12,11),'e1d1a6');rect((4,7,5,8),'f0e3b5')
 elif name=='tangerine':
  rect((4,8,11,15),'83542d');rect((3,9,12,13),'bf7835');rect((4,8,10,14),'e3a044');rect((5,8,7,9),'f6c670');rect((8,6,9,8),'466b3f');rect((9,6,11,6),'8b9d54')
 elif name=='coin':
  rect((3,8,12,13),'a27d41');rect((4,7,11,14),'d1a74c');rect((5,6,10,15),'d1a74c');rect((4,8,5,11),'f4d78a');rect((6,7,9,7),'f4d78a');rect((7,9,8,12),'9f7b39')
 else:
  rect((2,10,13,16),'5b4936');rect((3,11,12,15),'a78c56');rect((3,11,12,11),'d0b579');rect((4,13,11,13),'7f653f');rect((5,11,5,15),'c3a66b');rect((10,11,10,15),'c3a66b');rect((4,7,6,10),'de9b3f');rect((8,8,11,10),'d58c38');rect((5,6,6,6),'829a4d')
 atlas.paste(im,(i*16,0));frames[name]={'frame':{'x':i*16,'y':0,'w':16,'h':20},'rotated':False,'trimmed':False,'spriteSourceSize':{'x':0,'y':0,'w':16,'h':20},'sourceSize':{'w':16,'h':20}};instructions[name]=ops
atlas.save(O/'interaction-tools.png');(O/'interaction-tools.json').write_text(json.dumps({'frames':frames,'meta':{'image':'interaction-tools.png','size':{'w':128,'h':20},'scale':'1'}})+'\n')
for name in ['interaction-tools.png','interaction-tools.json']:(S/name).write_bytes((O/name).read_bytes())
(S/'native-instructions.json').write_text(json.dumps(instructions,indent=2)+'\n');(S/'PROVENANCE.json').write_text(json.dumps({'authoring':'Original explicitly authored native pixel-cluster props; Python3/Pillow integer rectangles, binaryalpha; no image model, external art or old character pixels','scope':'8small16x20props only; no body/face generation','source':'tools/phase3bd-in-world/tool_art.py','nativeCell':[16,20],'registeredHandAnchor':[8,12],'outputs':{n:hashlib.sha256((O/n).read_bytes()).hexdigest()for n in ['interaction-tools.png','interaction-tools.json']}},indent=2)+'\n')
