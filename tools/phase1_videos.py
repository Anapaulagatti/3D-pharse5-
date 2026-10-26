from pathlib import Path
import subprocess,json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'docs/phase1';rows=[]
for source in [D/'selection-juni-gameplay.webm',D/'bridge-regression/world-traversal.webm']:
 out=source.with_suffix('.mp4');review=source.with_name(source.stem+'-review.mp4')
 for target,filters,rate in [(out,'fps=12','650k'),(review,'fps=8,scale=iw/2:ih/2:flags=neighbor','170k')]:
  subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-an','-vf',filters,'-c:v','libx264','-threads','2','-preset','veryfast','-crf','25','-maxrate',rate,'-bufsize','1300k','-pix_fmt','yuv420p','-movflags','+faststart',str(target)],check=True)
  rows.append({'file':str(target.relative_to(D)),'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'probe':json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=width,height,codec_name','-of','json',str(target)])),'meaning':'Actual original-control motion recording, original duration. Lossy video is not pixel-exact proof; native PNGs separate. Review derivative uses exact2x nearest reduction. Only Juni playable.'})
(D/'video-provenance.json').write_text(json.dumps(rows,indent=2)+'\n');print([(q['file'],q['bytes'])for q in rows])
