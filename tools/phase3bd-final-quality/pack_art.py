from pathlib import Path
from PIL import Image
import hashlib,json
S=Path('assets-src/farming/phase3bd-final-quality');O=Path('public/assets/farming/phase3bd-final-quality');F=S/'finished-final';O.mkdir(exist_ok=True)
def pack(names,cell,cols,name):
 w,h=cell;im=Image.new('RGBA',(w*cols,h*((len(names)+cols-1)//cols)));frames={}
 for i,n in enumerate(names):
  src=Image.open(F/(n+'.png')).convert('RGBA');assert src.size==cell
  x=i%cols*w;y=i//cols*h;im.paste(src,(x,y));frames[n]={'frame':{'x':x,'y':y,'w':w,'h':h},'rotated':False,'trimmed':False,'spriteSourceSize':{'x':0,'y':0,'w':w,'h':h},'sourceSize':{'w':w,'h':h}}
 im.save(O/(name+'.png'));(O/(name+'.json')).write_text(json.dumps({'frames':frames,'meta':{'image':name+'.png','size':{'w':im.width,'h':im.height},'scale':'1'}},indent=2)+'\n')
pack([f'{c}-{s}'for c in ['radish','scallion']for s in ['sown','sprout','young','growing','ready','ready-alt']],(40,44),6,'crops')
pack([f'{k}-{i}'for k in ['loam','tilled','wet']for i in range(12)]+['debris-stone','debris-straw','debris-rim'],(16,16),12,'soil-components')
(S/'PROVENANCE.json').write_text(json.dumps({'artSource':'host_image','actualProviderRoute':'builtin image_gen.imagegen; no external paid API','sourceCalls':2,'sourceFiles':['master.png','master-clean.png'],'prompt':'PROMPT.txt; second calltechnical cleanup retained same18props','referenceImageReuse':'Only own first newly generated sheet in second call; no third-party/game/map crop donors','processing':'art.py explicit ownership/shared fixed-scale root -> registered Forge palette_tool build/apply -> custom Phaser-native atlas packing. Original raw QC FAIL/WARN retained; not falsely called clean regular-grid art.','skillActuallyReadAndUsed':'/workspace/tooling-cache/agent-sprite-forge/skills/generate2dsprite/SKILL.md; skill pin5324342 from docs/ART_SKILL_REGISTRY.md','rights':'Original project generation; prior owner-confirmed personalChatGPT/Codexterms apply as between OpenAI/owner; not a third-party rights certification; exact public exposure pending','hashes':{str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in [S/'master.png',S/'master-clean.png',S/'REGISTRATION.json',*O.iterdir()]}},indent=2)+'\n')
preview=Image.open(O/'crops.png');preview.resize((preview.width*3,preview.height*3),Image.Resampling.NEAREST).save(S/'native-review-3x.png')
