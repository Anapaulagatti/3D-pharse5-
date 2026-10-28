from pathlib import Path
import json,subprocess
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a-final-six';rows=json.loads((D/'actual-gameplay.json').read_text())['rows'];S=R/'assets-src/npcs/phase3a-final-six'
for row in rows:
 id=row['id'];dest=D/'gameplay'/(id+'-actual.mp4')
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',row['videoSource'],'-an','-c:v','libx264','-crf','24','-preset','fast','-pix_fmt','yuv420p','-movflags','+faststart',str(dest)],check=True)
 q=Image.open(D/'gameplay'/(id+'-with-juni-native.png'));q.save(D/'gameplay'/(id+'-with-juni-native.png')) if False else None
 q.resize((853,600),Image.Resampling.BOX).convert('RGB').save(D/'gameplay'/(id+'-review.jpg'),quality=86)
 # Native world crop, no scale; source original above remains untouched.
 a=next(c['audit'] for c in json.loads((D/'actual-gameplay.json').read_text())['captures'] if c['id']==id and c['audit']['actualFrame'].startswith('greet'))
 x=round(a['sprite']['x']-a['camera']['scroll'][0]);y=round(a['sprite']['y']-a['camera']['scroll'][1]);left=max(0,min(q.width-480,x-240));top=max(0,min(q.height-400,y-190));q.crop((left,top,left+480,top+400)).save(D/'gameplay'/(id+'-context-native.png'))
 for name in ['master','turnaround']:
  src=S/id[4:]/(name+'-source.png');q=Image.open(src).convert('RGB');q.thumbnail((560,560),Image.Resampling.BOX);q.save(D/(id+'-'+name+'-review.jpg'),quality=84)
 print(id,'actual MP4, native context, lightweight review copies')
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(D/'supplemental-clip-inspector-actual.webm'),'-an','-c:v','libx264','-crf','24','-preset','fast','-pix_fmt','yuv420p','-movflags','+faststart',str(D/'supplemental-clip-inspector-actual.mp4')],check=True)
# Preserve the original recording outside the portable runtime instead of committing duplicate video codecs.
