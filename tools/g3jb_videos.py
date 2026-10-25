"""Uninterrupted real recordings. Native PNGs, not lossy video, prove exact pixels."""
from pathlib import Path
import subprocess,json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-jeju-bridges';rows=[]
for key in ['world-traversal']:
 src=D/(key+'.webm')
 for label,vf,rate,crf in [('native','fps=12','800k','25'),('review','fps=8,scale=512:400:flags=neighbor','130k','30')]:
  out=D/(key+'-'+label+'.mp4')
  if not out.exists() or out.stat().st_mtime<src.stat().st_mtime:subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-threads','2','-i',str(src),'-an','-vf',vf,'-c:v','libx264','-threads','2','-preset','veryfast','-crf',crf,'-maxrate',rate,'-bufsize','1600k'if label=='native'else'260k','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],check=True)
  assert out.stat().st_size<100000000
  info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=width,height,codec_name','-of','json',str(out)]));rows.append({'file':out.name,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'probe':info,'spatialScale':'UNCHANGED1280x1000 UI/gameplay'if label=='native'else'Nearest512x400 review derivative','meaning':'Lossy temporal movement evidence. Untouched native PNGs are the pixel-fidelity evidence.','sequence':'Two explicitly separate bridge sessions after their own initial review spawn; four consecutive original-control walk-out/return/run-out/return legs each, native stops and left/right/toward-rail tests. No in-movement teleport, speed, source-frame or collision overrides.'if key=='world-traversal'else'Three explicitly separate scene comparisons: main wall blocked / hypothetical88px gate reaches door / platform8px strip blocked. Scene reloads declared.'})
 raw=hashlib.sha256(src.read_bytes()).hexdigest();rows.append({'raw':src.name,'sha256':raw,'rawStorage':'Locally preserved ignored WebM; MP4 delivery is reproducible. No position/collision/frame overrides.','physicalDevices':'NOT TESTED'})
(D/'video-provenance.json').write_text(json.dumps(rows,indent=2)+'\n');print('Videos encoded:',[(r['file'],r['bytes'])for r in rows if 'file'in r])
