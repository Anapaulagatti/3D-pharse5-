from pathlib import Path
from PIL import Image,ImageDraw
import subprocess,json
R=Path(__file__).resolve().parents[2];D=R/'docs/phase2b-motion/walk-front';ids=['ara','doyun','sori','jiwon','nari','taeyang','yuna','hyunwoo'];rows=[]
def encode(frames,out):
 p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pixel_format','rgb24','-video_size','384x272','-framerate','60','-i','-','-an','-c:v','libx264','-threads','1','-preset','fast','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],stdin=subprocess.PIPE)
 for q in frames:p.stdin.write(q.tobytes())
 p.stdin.close();assert p.wait()==0
for id in ids:
 frames=[]
 for n in range(24):
  loop,i=divmod(n,8);panel=Image.new('RGB',(384,272),(28,30,38));dr=ImageDraw.Draw(panel)
  for col,who in enumerate(['juni',id]):
   panel.paste(Image.open(D/f'{who}-loop{loop}-{i}-context-native.png'),(col*192,32));dr.text((col*192+4,16),who,fill='white')
  dr.text((4,2),f'PHASER walk-front loop{loop+1}/3 phase{i}',fill='white');dr.text((4,258),'Actual captures; matched phase; normal cadence',fill='white');step=44/8;frames.extend([panel]*(round((n+1)*step)-round(n*step)))
 encode(frames,D/f'juni-vs-{id}-front-phaser.mp4')
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(D/f'{id}-actual-gameplay.webm'),'-an','-c:v','libx264','-threads','1','-preset','fast','-crf','24','-pix_fmt','yuv420p','-movflags','+faststart',str(D/f'{id}-front-gameplay.mp4')],check=True)
 rows.append({'id':id,'comparison':f'juni-vs-{id}-front-phaser.mp4','actual':f'{id}-front-gameplay.mp4','comparisonMethod':'24 actual native Phaser contexts:3consecutive cycles aligned to original index0..7, displayed at nominal44/60s gait duration; not a simultaneous unretimed recording.','actualMethod':'Unretimed1280x1000 gameplay recording, real Studio/input, canonical world; no video scaling or frame manipulation. Lossless PNGs are pixel-fidelity authority.'});print(id,'comparison+gameplay encoded',flush=True)
(D/'media-provenance.json').write_text(json.dumps(rows,indent=2)+'\n')
