"""Encode actual recorded gameplay and label decoded frames; never generate game art."""
from pathlib import Path
from PIL import Image,ImageDraw
import subprocess,json
R=Path(__file__).resolve().parents[1];Q=R/'docs/seoul-production/quality';C=R/'.cache/production'
subprocess.run(['ffmpeg','-v','error','-i',str(C/'walkthrough.webm'),'-vf','fps=15','-an','-c:v','libx264','-preset','medium','-crf','30','-pix_fmt','yuv420p','-movflags','+faststart','-y',str(Q/'gameplay-walkthrough.mp4')],check=True)
meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration,size','-show_entries','stream=width,height,avg_frame_rate,nb_frames','-of','json',str(Q/'gameplay-walkthrough.mp4')],text=True));(Q/'video-metadata.json').write_text(json.dumps(meta,indent=2)+'\n');duration=float(meta['format']['duration'])
board=Image.new('RGB',(2048,960),'#f0e8d2');d=ImageDraw.Draw(board)
for i,fraction in enumerate([.045,.12,.255,.37,.55,.68,.84,.96]):
 t=round(duration*fraction,2);p=C/f'decoded-final-{i}.png';subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',str(Q/'gameplay-walkthrough.mp4'),'-frames:v','1','-y',str(p)],check=True);im=Image.open(p).resize((512,450),Image.Resampling.NEAREST);x=i%4*512;y=i//4*480;board.paste(im,(x,y));d.text((x+8,y+454),f'Actual decoded video / {t}s',fill='#23483d')
board.save(Q/'gameplay-video-contact.png')
board=Image.new('RGB',(1152,320),'#f0e8d2');d=ImageDraw.Draw(board)
for i,t in enumerate([6,6.2,6.4,6.6,6.8,7]):
 p=C/f'action-final-{i}.png';subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',str(Q/'gameplay-walkthrough.mp4'),'-frames:v','1','-y',str(p)],check=True);im=Image.open(p).crop((464,365,560,509)).resize((192,288),Image.Resampling.NEAREST);board.paste(im,(i*192,0));d.text((i*192+8,296),f'Actual decoded {t}s',fill='#23483d')
board.save(Q/'juni-live-animation-contact.png')
a=Image.open(R/'docs/living-seoul/academy-native.png');b=Image.open(Q/'academy-native.png');board=Image.new('RGB',(2048,840),'#f0e8d2');d=ImageDraw.Draw(board);d.text((24,20),'BEFORE / preserved earlier Academy',fill='#23483d');d.text((1048,20),'AFTER / actual Stage B Phaser at native1x',fill='#23483d');board.paste(a,(0,60));board.paste(b,(1024,60));board.save(Q/'before-after-native.png');b.crop((190,40,446,296)).resize((1024,1024),Image.Resampling.NEAREST).save(Q/'pixel-detail-4x.png')
print(json.dumps({'actualDuration':duration,'encodedFrames':meta['streams'][0]['nb_frames'],'encodedFPS':15,'gameFPSClaimed':False}))
