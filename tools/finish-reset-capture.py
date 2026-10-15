from pathlib import Path
import json,subprocess
q=Path('quality-reports/pixel-reset-v2');d=q/'motion';m=json.loads((d/'capture.json').read_text());assert not m['errors'] and not m['missing'];f=m['frames'];assert len(f)>40
lines=[]
for i,r in enumerate(f):
 lines.append("file '"+str((d/f"{r['index']:04d}.jpg").resolve())+"'")
 if i<len(f)-1:lines.append('duration '+str(max(.001,f[i+1]['at']-r['at'])))
(d/'original-timing.ffconcat').write_text('\n'.join(lines)+'\n')
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(d/'original-timing.ffconcat'),'-fps_mode','vfr','-vf','pad=ceil(iw/2)*2:ceil(ih/2)*2','-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart',str(q/'premium-pixel-reset-motion.mp4')],check=True)
for k in 'ABC':
 for action in ['idle','walk-down','emote']:
  seq=[x for x in f if x['label']==k+'-'+action];assert seq,(k,action);r=seq[min(2,len(seq)-1)]
  subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',str(r['at']),'-i',str(q/'premium-pixel-reset-motion.mp4'),'-frames:v','1',str(q/f'video-{k}-{action}.png')],check=True)
print('Encoded original-timing motion and decoded9review frames; visual inspection pending.')
