"""Compose labelled evidence from actual native Phaser PNGs and decoded MP4 frames."""
from pathlib import Path
import json
import subprocess
import hashlib
from PIL import Image, ImageDraw, ImageFont

R=Path(__file__).resolve().parents[1];D=R/'docs/juni-animation'
C=R/'.cache/juni-animation/video-inspection';C.mkdir(exist_ok=True)
report=json.loads((D/'browser-verification.json').read_text())
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
title=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',28)
frames=[]
for action in ['walk','run']:
    for direction in ['right','back','left','front']:
        rows=[x for x in report['frameLog']if x['action']==action and x['direction']==direction]
        assert len(set(x['frame']for x in rows))==8
        frames.append((f'{action} / {direction}',rows[0]['t']/1000+.35,f'{action}-{direction}'))
for action in ['idle','wave','celebrate','social']:
    rows=[x for x in report['frameLog']if x['action']==action]
    frames.append((action,rows[0]['t']/1000+(.35 if action!='idle' else 1),f'{action}-gesture'))
video_board=Image.new('RGB',(1280,1020),'#eee8da');draw=ImageDraw.Draw(video_board)
draw.text((16,14),'DECODED REAL PHASER VIDEO / 2x gameplay camera',font=font,fill='#29443c')
for i,(label,t,name) in enumerate(frames):
    path=C/f'{name}.png'
    if not path.exists():
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-ss',str(t),'-i',str(D/'juni-gameplay.mp4'),'-frames:v','1',str(path)],check=True)
    x=(i%4)*320;y=54+(i//4)*320
    crop=Image.open(path).crop((442,555,742,845))
    video_board.paste(crop,(x+10,y+22));draw.text((x+12,y),f'{label} / {t:.2f}s',font=font,fill='#29443c')
video_board.save(D/'video-contact.png')
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration,size','-show_entries','stream=width,height,avg_frame_rate,nb_frames','-of','json',str(D/'juni-gameplay.mp4')]))
report['video']={'file':'juni-gameplay.mp4','sha256':hashlib.sha256((D/'juni-gameplay.mp4').read_bytes()).hexdigest(),
 'ffprobe':probe,'method':'Unsped actual Playwright browser recording; FFmpeg H264/yuv420p conversion.25fps encoding is NOT a hardware60FPS claim.',
 'decoded_inspection_frames':[{'action':a,'time_s':t,'file':str(C/f'{name}.png')}for a,t,name in frames]}

board=Image.new('RGB',(2108,1450),'#eee8da');draw=ImageDraw.Draw(board)
draw.text((24,14),'JUNI / REAL ACTION ANIMATION + GWANGHWAMUN COMPOSITION',font=title,fill='#29443c')
draw.text((24,56),'BEFORE / actual Phaser, static direction avatar',font=font,fill='#29443c')
draw.text((1080,56),'AFTER / actual Phaser, native1x; original architecture retained',font=font,fill='#29443c')
before=Image.open(R/'docs/gwanghwamun/phaser-native-day.png').convert('RGB')
after=Image.open(D/'native-after-map.png').convert('RGB');assert before.size==after.size==(1024,768)
board.paste(before,(24,86));board.paste(after,(1080,86))
draw.text((24,875),'4x NEAREST CROPS OF REAL NATIVE PHASER PIXELS / no character overpaint or synthetic poses',font=font,fill='#29443c')
panels=[('Old static',before,512,600)]
for pose in report['nativePoses']:
    image=Image.open(D/f"{pose['name']}.png")
    assert image.size==(1024,768)
    foot=pose['game']['screenFoot'];panels.append((pose['review']['frame'],image,foot['x'],foot['y']))
for i,(label,image,x,y) in enumerate(panels):
    left=24+i*416;draw.text((left,914),label,font=font,fill='#29443c')
    crop=image.crop((x-48,y-100,x+48,y+12)).resize((384,448),Image.Resampling.NEAREST)
    board.paste(crop,(left,947))
draw.text((24,1410),'Review candidate. No new NPCs/districts, no paid provider calls or public game release. Small idle/gesture detector warnings retained.',font=font,fill='#53645c')
board.save(D/'animation-world-review-board.png')
(D/'browser-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'video':probe,'boards':['animation-world-review-board.png','video-contact.png']}))
