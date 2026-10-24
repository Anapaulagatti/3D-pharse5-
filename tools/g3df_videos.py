"""Transcode actual uninterrupted recordings. Native PNGs, not lossy video, prove pixels."""
from pathlib import Path
import subprocess,json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-alignment';rows=[]
for key in ['world','bridge']:
 src=D/(key+'-traversal.webm');native=D/(key+'-traversal-native.mp4');review=D/(key+'-traversal-review.mp4')
 for out,vf,rate in [(native,'fps=12','900k'),(review,'fps=8,scale=512:400:flags=neighbor','220k')]:
  if not out.exists()or out.stat().st_mtime<src.stat().st_mtime:
   subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-threads','2','-i',str(src),'-an','-vf',vf,'-c:v','libx264','-threads','2','-preset','veryfast','-crf','25'if out==native else'28','-maxrate',rate,'-bufsize','1800k'if out==native else'440k','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],check=True)
  assert out.stat().st_size<100000000
  info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=width,height,codec_name','-of','json',str(out)]));rows.append({'file':out.name,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'bytes':out.stat().st_size,'probe':info,'spatialScale':('NO_SPATIAL_RESIZE /1280x1000 UI+gameplay'if out==native else'Nearest512x400 review derivative'),'lossyVideo':'Temporal movement evidence only. Actual pixel-fidelity proof uses untouched native PNGs.','cutsOrTeleports':'NONE / continuous recorded input sequence'})
rows.append({'source':'world-traversal.webm / bridge-traversal.webm','rawSHA256':{key:hashlib.sha256((D/(key+'-traversal.webm')).read_bytes()).hexdigest()for key in ['world','bridge']},'rawStorage':'Locally retained, ignored raw recordings; MP4s are delivery artifacts.','physicalDevices':'NOT TESTED'})
(D/'video-provenance.json').write_text(json.dumps(rows,indent=2)+'\n');print('Recorded video evidence encoded:',[(r['file'],r['bytes'])for r in rows if 'file'in r])
