"""Packaging-only encoding; original review recordings are immutable inputs."""
from pathlib import Path
import subprocess,json,hashlib
R=Path(__file__).resolve().parents[2];D=R/'docs/phase2b-motion';O=Path('/tmp/phase2b-motion-compact-videos');O.mkdir(exist_ok=True);rows=[]
for id in ['sori','jiwon','nari','taeyang','yuna','hyunwoo']:
 src=D/f'{id}-actual-gameplay.mp4';out=O/src.name;h=hashlib.sha256(src.read_bytes()).hexdigest()
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-map','0:v:0','-an','-c:v','libx264','-threads','1','-preset','fast','-crf','29','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],check=True)
 assert hashlib.sha256(src.read_bytes()).hexdigest()==h
 def probe(p):
  q=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]));s=q['streams'][0];return {'size':[s['width'],s['height']],'frames':int(s['nb_frames']),'fps':s['r_frame_rate'],'duration':q['format']['duration']}
 a,b=probe(src),probe(out);assert a==b,(id,a,b);rows.append({'file':src.name,'originalSHA256':h,'originalBytes':src.stat().st_size,'packagedSHA256':hashlib.sha256(out.read_bytes()).hexdigest(),'packagedBytes':out.stat().st_size,'nativeRegistration':a,'policy':'Compression-only derivative; no scaling,cropping,frame removal,retiming or approved-art edit. Original MP4 unchanged; lossless native PNG remains fidelity authority.'});print(id,out.stat().st_size,flush=True)
(D/'packaged-video-provenance.json').write_text(json.dumps(rows,indent=2)+'\n')
