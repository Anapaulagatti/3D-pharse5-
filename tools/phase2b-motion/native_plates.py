"""Readable review-only plate labels; no character frames or atlas writes."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,subprocess,io
D=Path('docs/phase2b-motion');base=json.loads((D/'before-manifest.json').read_text())['commit']
for id in ['sori','jiwon','nari','taeyang','yuna','hyunwoo']:
 stem=f'public/assets/characters/{id}/atlas';m=json.loads(Path(stem+'.json').read_text())['frames'];before=Image.open(io.BytesIO(subprocess.check_output(['git','show',base+':'+stem+'.png']))).convert('RGBA');after=Image.open(stem+'.png').convert('RGBA')
 for action in ['walk','run']:
  out=Image.new('RGB',(768,840),(28,30,38));dr=ImageDraw.Draw(out)
  for v,view in enumerate(['front','back','right']):
   for row,(label,atlas)in enumerate([('BEFORE',before),('AFTER',after)]):
    y=(v*2+row)*140;dr.text((4,y+2),f'{id} {action}-{view} {label} | source-only native1:1',fill='white')
    for i in range(8):
     f=m[f'{action}-{view}-{i}']['frame'];im=atlas.crop((f['x'],f['y'],f['x']+96,f['y']+112));out.paste(im,(i*96,y+16),im);dr.text((i*96+44,y+127),str(i),fill='white')
  out.save(D/f'{id}-{action}-before-after-native.png')
print('12 native review plates labeled; source frame/atlas files untouched')
