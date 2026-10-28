"""Encode actual browser recordings, never manufacture gameplay from sprite frames."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess,json
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a-npc-expansion'
def convert(p):
 out=p.with_suffix('.mp4');
 if not out.exists():subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(p),'-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart','-threads','2',str(out)],check=True)
 q=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration,size','-of','json',str(out)],check=True,capture_output=True,text=True);return{'source':str(p.relative_to(R)),'file':str(out.relative_to(R)),'method':'Actual Playwright screen recording encoded directly;no image sequence or spatial rescale','probe':json.loads(q.stdout)}
if __name__=='__main__':
 files=sorted((D/'gameplay').glob('*.webm'))
 for name in ['supplemental-clip-inspector-actual.webm','urban-three-roundtrips-actual.webm']:
  if(D/name).exists():files.append(D/name)
 with ThreadPoolExecutor(max_workers=2)as pool:rows=list(pool.map(convert,files))
 (D/'video-provenance.json').write_text(json.dumps(rows,indent=2)+'\n');print('Encoded',len(rows),'actual browser videos')
