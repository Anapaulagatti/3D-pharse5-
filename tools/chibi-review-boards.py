"""Review boards use actual Phaser canvas crops with no artwork insertion/resampling."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,subprocess
Q=Path('quality-reports/chibi-v1');v=Q/'render';samples=json.loads((v/'samples.json').read_text())
def crop(file,m):
 im=Image.open(v/file).convert('RGB');x,y=m['screenFoot']['x'],m['screenFoot']['y'];return im.crop((x-72,y-180,x+72,y+6))
def board(name,rows):
 im=Image.new('RGB',(len(rows)*180,230),'#ead8b5');d=ImageDraw.Draw(im)
 for i,(label,src) in enumerate(rows):im.paste(src,(i*180+18,16));d.text((i*180+10,209),label,fill='#302d3d')
 im.save(Q/name)
board('ACTUAL_FOUR_DIRECTIONS.png',[(s['metrics']['direction'],crop(s['file'],s['metrics'])) for s in samples[:4]])
board('ACTUAL_FOUR_EXPRESSIONS.png',[(s['metrics']['expression'],crop(s['file'],s['metrics'])) for s in samples[4:]])
# Same native3x crop, same camera and footpoint. Different dimensions are the intentional avatar-scale change.
old=Image.open('quality-reports/unified-v4/render/idle-closeup.png').convert('RGB').crop((440,388,584,574))
new=Image.open(v/'idle-closeup.png').convert('RGB').crop((440,388,584,574))
board('OLD_VS_NEW_ACTUAL.png',[('Previous unapproved',old),('New chibi candidate',new)])
board('ACTUAL_OUTFITS.png',[(f'Hair{h} Outfit{o}',Image.open(v/f'outfit-h{h}-o{o}.png').convert('RGB').crop((440,388,584,574))) for h,o in [(0,0),(0,1),(1,0),(1,1)]])
# Actual decoded movement panels, kept at native recorded size. No injected poses.
movie=Q/'chibi-avatar-gameplay.mp4';motion=json.loads((Q/'motion/capture.json').read_text());segments=[]
for name,phases in [('idle',['idle']),('walk',['walk-down','walk-right','walk-up','walk-left']),('run',['run-down','run-right','run-up','run-left']),('emotes',['wave','celebrate','pose'])]:
 frames=[f for f in motion['frames'] if f['phase'] in phases];start,end=frames[0]['at'],frames[-1]['at'];dest=Q/(name+'-preview.mp4')
 subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',str(start),'-i',str(movie),'-t',str(end-start),'-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart',str(dest)],check=True)
 segments.append({'file':dest.name,'source_start_seconds':start,'duration_seconds':end-start,'method':'Cut from actual original-time engine video; no retiming or pose replacement.'})
(Q/'preview-clips.json').write_text(json.dumps(segments,indent=2)+'\n')
print('Actual engine boards and native-time idle/walk/run/emote video clips saved.')
