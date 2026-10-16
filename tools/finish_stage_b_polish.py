"""Encode actual Playwright recording at its native25fps and label decoded frames."""
from pathlib import Path
import subprocess,json
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];Q=R/'docs/stage-b-polish/quality';C=R/'.cache/stage-b-polish'
source=R/'.cache/production/walkthrough.webm';output=Q/'gameplay-walkthrough.mp4'
raw=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=avg_frame_rate,r_frame_rate,nb_frames','-show_entries','format=duration','-of','json',str(source)],text=True))
subprocess.run(['ffmpeg','-v','error','-i',str(source),'-an','-c:v','libx264','-preset','medium','-crf','30','-pix_fmt','yuv420p','-movflags','+faststart','-y',str(output)],check=True)
meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration,size','-show_entries','stream=width,height,avg_frame_rate,nb_frames','-of','json',str(output)],text=True))
(Q/'video-metadata.json').write_text(json.dumps({'input':raw,'encoded':meta,'note':'Native Playwright25fps recording, no FPS up-conversion, no speedup; encoded FPS is NOT measured game FPS. New world-refinement request requires separate >=30fps genuine capture.'},indent=2)+'\n')
duration=float(meta['format']['duration']);board=Image.new('RGB',(2048,960),'#eee7d6');d=ImageDraw.Draw(board)
for i,f in enumerate([.045,.12,.255,.37,.55,.68,.84,.96]):
 t=round(duration*f,2);p=C/f'video-{i}.png';subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',str(output),'-frames:v','1','-y',str(p)],check=True);im=Image.open(p).resize((512,450),Image.Resampling.NEAREST);x=i%4*512;y=i//4*480;board.paste(im,(x,y));d.text((x+8,y+455),f'Actual recorded Phaser / {t}s',fill='#203c32')
board.save(Q/'gameplay-contact.png');print(json.dumps(meta))
