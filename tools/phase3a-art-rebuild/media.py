"""Compression-only copies of actual canonical recordings and separately labelled inspector."""
from pathlib import Path
import subprocess,json,hashlib
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a-art-rebuild';rows=[]
for src in sorted((D/'gameplay').glob('*.webm'))+[D/'supplemental-clip-inspector-actual.webm']:
 if not src.exists():continue
 out=src.with_suffix('.mp4');subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-an','-c:v','libx264','-threads','1','-preset','fast','-crf','28','-pix_fmt','yuv420p','-fps_mode','passthrough','-movflags','+faststart',str(out)],check=True);q=json.loads(subprocess.check_output(['ffprobe','-v','quiet','-show_streams','-show_format','-of','json',str(out)],text=True));v=next(s for s in q['streams']if s['codec_type']=='video');assert[v['width'],v['height']]==[1280,900];rows.append({'file':str(out.relative_to(R)),'source':str(src.relative_to(R)),'sourceSHA256':hashlib.sha256(src.read_bytes()).hexdigest(),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'bytes':out.stat().st_size,'size':[1280,900],'durationSeconds':float(q['format']['duration']),'method':'Actual canonical gameplay;compression-only,no spatialresize/retiming.'if src.parent.name=='gameplay'else'Supplemental actual Phaser CLIP INSPECTOR,not canonical-world gameplay;compression-only,no spatialresize/retiming.'});print(out.name,out.stat().st_size,flush=True)
(D/'media-provenance.json').write_text(json.dumps(rows,indent=2)+'\n')
