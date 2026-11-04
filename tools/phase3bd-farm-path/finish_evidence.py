from pathlib import Path
from PIL import Image
import json,hashlib,subprocess
D=Path('docs/phase3bd-farm-path');q=json.loads((D/'GAMEPLAY_QA.json').read_text());assert q['status'].startswith('PASS');atlas=Image.open('public/assets/farming/phase3bd-farm-path/crops.png').convert('RGBA');frames=json.load(open('public/assets/farming/phase3bd-farm-path/crops.json'))['frames'];out=[]
for s in q['stages']:
 a=s['audit'];im=Image.open(D/(s['name']+'-native.png')).convert('RGBA');soil=next(p for p in a['farmSprites']if p['key']=='farm-soil'and p['position']==[394,535]);x,y=map(round,soil['screen']);im.crop((x-8,y-8,x+148,y+100)).save(D/(s['name']+'-crop-1x.png'))
 if not s.get('expected'):continue
 p=next(p for p in a['farmSprites']if p['key']=='farm-crops'and p['visible']and p['position']==[408,555]);r=frames[p['frame']]['frame'];source=atlas.crop((r['x'],r['y'],r['x']+16,r['y']+20));x,y=round(p['screen'][0]-8),round(p['screen'][1]-17);total=match=0
 for yy in range(20):
  for xx in range(16):
   rgba=source.getpixel((xx,yy))
   if rgba[3]:total+=1;match+=im.getpixel((x+xx,y+yy))[:3]==rgba[:3]
 out.append({'stage':s['name'],'frame':p['frame'],'opaqueNativePixels':total,'exactMatches':match,'status':'PASS'if total==match else'FAIL'})
assert all(r['status']=='PASS'for r in out)
(D/'PIXEL_READBACK.json').write_text(json.dumps(out,indent=2)+'\n')
rows=[]
for p in [D/'videos/farm-lifecycle-paths.webm',D/'mobile/videos/mobile-touch.webm']:
 dest=D/'videos'/p.with_suffix('.mp4').name
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(p),'-an','-c:v','libx264','-preset','veryfast','-threads','1','-crf','28','-pix_fmt','yuv420p','-movflags','+faststart',str(dest)],check=True)
 a=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(dest)]));assert not any(s['codec_type']=='audio'for s in a['streams']);rows.append({'file':str(dest.relative_to(D)),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'rawCaptureSHA256':hashlib.sha256(p.read_bytes()).hexdigest(),'seconds':a['format']['duration'],'actualGameplay':True,'audioStreams':0,'nativePNGForPixels':True,'testedOrigin':'http://127.0.0.1:4455/play/','buildSource':'79f29058'})
(D/'VIDEO_PROOF.json').write_text(json.dumps(rows,indent=2)+'\n')
b=json.loads((D/'BASELINE.json').read_text());bad=[n for n,h in b['files'].items()if not Path(n).is_file()or hashlib.sha256(Path(n).read_bytes()).hexdigest()!=h];assert not bad
print('PASS',len(b['files']),'protected originals;',len(out),'exact crop pixel readbacks;',len(rows),'actual frozen game videos')
