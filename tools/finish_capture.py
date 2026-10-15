from pathlib import Path
import json,subprocess
r=Path('quality-reports/pixel-v3.1');d=r/'animation';m=json.loads((d/'capture.json').read_text());assert not m['errors'] and not m['missing'];frames=m['frames'];assert len(frames)>15
lines=[]
for i,f in enumerate(frames):
 lines.append("file '"+str((d/f"{f['index']:04d}.jpg").resolve())+"'")
 if i<len(frames)-1:lines.append('duration '+str(frames[i+1]['at']-f['at']))
(d/'original-timing.ffconcat').write_text('\n'.join(lines)+'\n')
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(d/'original-timing.ffconcat'),'-fps_mode','vfr','-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart',str(r/'pixel-town-art-preview.mp4')],check=True)
# Decode actual video frames for visual review, rather than relabel source PNG.
for label in ['down','up','left','right','run','wave']:
 f=next(f for f in frames if f['label']==label)
 subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',str(f['at']),'-i',str(r/'pixel-town-art-preview.mp4'),'-frames:v','1',str(r/f'video-{label}.png')],check=True)
print('Original-timing video created; inspect decoded frames before claiming visual verification.')
