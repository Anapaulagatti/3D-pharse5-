from pathlib import Path
import subprocess,json,hashlib
R=Path(__file__).resolve().parents[2];D=R/'docs/phase2a';q=json.loads((D/'actual-gameplay.json').read_text());rows=[]
for mode in q['modes']:
 name=mode['name'];src=D/f'{name}-actual-gameplay.webm';out=D/f'{name}-actual-gameplay.mp4'
 subprocess.run(['ffmpeg','-y','-i',str(src),'-vf',f'crop=480:900:400:50,drawtext=text={name} - ACTUAL PHASER:x=10:y=10:fontcolor=white:fontsize=16:box=1:boxcolor=black@0.7','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-an','-movflags','+faststart',str(out)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 rows.append({'mode':name,'source':src.name,'sourceSHA256':hashlib.sha256(src.read_bytes()).hexdigest(),'review':out.name,'reviewSHA256':hashlib.sha256(out.read_bytes()).hexdigest(),'method':'Native-scale480x900 vertical crop of actual1280x1000 browser recording; full900px game-canvas height, no retiming or artificial frames. Lossy video is review evidence; native PNGs are authoritative pixel proof.'})
(D/'video-provenance.json').write_text(json.dumps(rows,indent=2)+'\n');print('Encoded',len(rows),'actual gameplay review videos')
