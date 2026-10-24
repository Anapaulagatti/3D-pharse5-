from pathlib import Path
import json,hashlib,subprocess
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate3/residual-v1';D=R/'docs/gate3-residual';O=R/'public/assets/gate3/residual-world'
for p in [S,D,O]:p.mkdir(exist_ok=True)
m=json.loads((R/'public/assets/gate3/aligned-world/manifest.json').read_text());g=Image.new('RGBA',m['size'])
for c in m['chunks']:g.paste(Image.open(R/'public'/c['image']),(c['x'],c['y']))
over=g.copy()
for o in sorted(m['objects'],key=lambda o:o['sortY']):over.alpha_composite(Image.open(R/'public'/o['image']).convert('RGBA'),(o['x'],o['y']))
for n,box in [('palace',(1280,120,2816,1144)),('station',(1920,1920,3456,2944)),('retail',(320,1600,1856,2624)),('bridge',(2816,3072,4352,4096)),('coast-west',(0,3840,1536,4864)),('coast-middle',(1280,3840,2816,4864)),('coast-east',(2560,3840,4096,4864))]:over.crop(box).save(S/(n+'-before-context.png'))
for n,box in [('palace-entry',(1900,565,2190,840)),('station-tree',(2820,2470,3020,2720)),('station-rear',(2310,2160,3000,2290)),('retail-upper',(500,1960,1640,2200))]:over.crop(box).save(S/(n+'-native.png'))
lock={'baseline':'9827761 visual /2eb4d29 metadata','head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'sources':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for root in ['assets-src/gate3/alignment-v1','public/assets/gate3/aligned-world','public/assets/gate3/aligned-before','public/assets/gate3/aligned-road-proposal','docs/gate3-alignment']for p in sorted((R/root).rglob('*'))if p.is_file()and p.suffix not in ['.webm']}}
(S/'baseline-lock.json').write_text(json.dumps(lock,indent=2)+'\n')
print('Contexts captured; approved alignment sources locked:',len(lock['sources']))
