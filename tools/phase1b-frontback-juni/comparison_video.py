from pathlib import Path
import json,subprocess
R=Path(__file__).resolve().parents[2];D=R/'docs/phase1b-frontback-juni';rows=json.loads((D/'comparison-recordings.json').read_text())['rows']
for clip in ['walk-front','walk-back','run-front','run-back']:
 args=['ffmpeg','-y'];filters=[]
 for i,id in enumerate(['juni','haneul','bomi','minjun']):
  row=next(r for r in rows if r['id']==id and r['clip']==clip);args+=['-ss',str(row['from']),'-t','1.2','-i',str(D/f'{id}-comparison-original.webm')]
  filters.append(f'[{i}:v]crop=240:900:520:50,setpts=PTS-STARTPTS,drawtext=text={id} {clip}:x=8:y=8:fontsize=14:fontcolor=white:box=1:boxcolor=black@0.7[v{i}]')
 filters.append('[v0][v1][v2][v3]hstack=inputs=4:shortest=1[out]');args+=['-filter_complex',';'.join(filters),'-map','[out]','-c:v','libx264','-crf','16','-pix_fmt','yuv420p','-an','-movflags','+faststart',str(D/f'actual-comparison-{clip}.mp4')]
 subprocess.run(args,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
