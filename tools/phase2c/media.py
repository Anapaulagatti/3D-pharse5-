from core import *
import subprocess
rows=[]
for folder in ['gameplay','foundation']:
 q=json.loads((D/folder/'actual-gameplay.json').read_text())
 for mode in q['modes']:
  src=D/folder/(mode['name']+'-actual-gameplay.webm');out=src.with_suffix('.mp4')
  if not src.exists():continue
  if not out.exists():subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-an','-c:v','libx264','-threads','1','-preset','fast','-crf','28','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],check=True)
  rows.append({'mode':mode['name'],'folder':folder,'file':str(out.relative_to(R)),'bytes':out.stat().st_size,'sha256':sha(out),'method':'Actual canonical Phaser, real input,unretimed1280x1000; no source-sheet animation substitution. Lossy compression-only copy; PNGs are pixel-fidelity authority.'});print(folder,mode['name'],out.stat().st_size,flush=True)
src=D/'studio-session-actual.webm';out=D/'studio-session-actual.mp4'
subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-an','-c:v','libx264','-threads','1','-preset','fast','-crf','28','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],check=True);rows.append({'mode':'studio-long-session','file':str(out.relative_to(R)),'bytes':out.stat().st_size,'sha256':sha(out),'method':'Unretimed real60switch/100preview-apply/preset workflow; no video retiming'});(D/'media-provenance.json').write_text(json.dumps(rows,indent=2)+'\n')
