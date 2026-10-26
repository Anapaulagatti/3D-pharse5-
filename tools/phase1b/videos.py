from pathlib import Path
import subprocess,json
R=Path(__file__).resolve().parents[2];D=R/'docs/phase1b';rows=[]
for source,stem in [(D/'four-character-gameplay.webm','four-character-gameplay'),(D/'progress-switch-refresh.webm','progress-switch-refresh')]+[(D/'bridges'/id/'world-traversal.webm',f'bridges-{id}')for id in ['juni','haneul','bomi','minjun']]:
 for review in [False,True]:
  out=D/(stem+('-review'if review else'')+'.mp4');cmd=['ffmpeg','-y','-loglevel','error','-threads','1','-i',str(source)]
  if review:cmd+=['-vf','scale=640:-2:flags=neighbor']
  cmd+=['-c:v','libx264','-preset','veryfast','-threads','1','-crf','26'if review else'21','-pix_fmt','yuv420p','-movflags','+faststart','-an',str(out)];subprocess.run(cmd,check=True)
  data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(out)]));stream=next(q for q in data['streams']if q['codec_type']=='video');rows.append({'source':str(source.relative_to(R)),'file':out.name,'bytes':out.stat().st_size,'duration':float(data['format']['duration']),'size':[stream['width'],stream['height']],'method':'Actual Playwright browser recording, no retiming or fabricated sprite/position/frames. H264 is lossy review evidence, not pixel proof; native PNG readbacks remain authoritative. Review movie is smaller nearest-sampled presentation copy.'});print(out.name,out.stat().st_size,flush=True)
(D/'videos.json').write_text(json.dumps(rows,indent=2)+'\n')
