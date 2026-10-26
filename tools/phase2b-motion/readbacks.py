from pathlib import Path
import json,math
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];D=R/'docs/phase2b-motion';rows=[]
for id in __import__('sys').argv[1:]:
 q=json.loads((D/f'{id}-gameplay.json').read_text());stem='assets/juni/juni'if id=='juni'else f'assets/characters/{id}/atlas';m=json.loads((R/'public'/f'{stem}.json').read_text())['frames'];atlas=Image.open(R/'public'/f'{stem}.png').convert('RGBA')
 for clip in q['rows']:
  board=Image.new('RGB',(768,132),(28,30,38));dr=ImageDraw.Draw(board)
  for s in clip['samples']:
   a=s['audit'];st=a['state'];name=a['actualFrame'];f=m[name]['frame'];src=np.array(atlas.crop((f['x'],f['y'],f['x']+96,f['y']+112)));sx,sy=a['camera']['scroll'];x=math.floor(st['x']+.5)-48-sx;y=math.floor(st['y']+.5)-100-sy;shot=Image.open(s['sourcePath']).convert('RGB');crop=shot.crop((x,y,x+96,y+112));diff=int(((src[:,:,3]==255)&np.any(src[:,:,:3]!=np.array(crop),2)).sum())
   # A gait quality crop must be unobscured, not excused with a foreground mask.
   if diff:print('OCCLUDED/DIFF',id,clip['clip'],s['loop'],s['index'],diff)
   dest=f'{id}-{clip["clip"]}-loop{s["loop"]}-{s["index"]}-body-native.png';crop.save(D/dest);shot.crop((x-48,y-56,x+144,y+168)).save(D/dest.replace('body-native','context-native'))
   if s['loop']==0:board.paste(crop,(96*s['index'],20));dr.text((96*s['index']+2,2),str(s['index']),fill='white')
   rows.append({'id':id,'clip':clip['clip'],'loop':s['loop'],'index':s['index'],'frame':name,'diffPixels':diff,'nearest':st['samplingMode']==1,'integerCamera':all(float(v).is_integer()for v in[sx,sy]),'nativeZoom':a['camera']['zoom'],'body':dest})
  board.save(D/f'{id}-{clip["clip"]}-actual-native.png')
(D/('readbacks-'+'-'.join(__import__('sys').argv[1:])+'.json')).write_text(json.dumps(rows,indent=2)+'\n');print('Readbacks',len(rows),'mismatch',sum(r['diffPixels']for r in rows))
