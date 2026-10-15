"""Encode real CDP compositor frames with their original timestamps. No speed-up."""
from pathlib import Path
import json,subprocess,argparse
p=argparse.ArgumentParser();p.add_argument('folder');p.add_argument('movie');a=p.parse_args();d=Path(a.folder);dest=Path(a.movie);dest.parent.mkdir(parents=True,exist_ok=True);m=json.loads((d/'capture.json').read_text());f=m['frames'];assert not m['errors'] and not m['missing'];lines=[]
for i,r in enumerate(f):
 lines.append("file '"+str((d/f"{r['index']:04d}.jpg").resolve())+"'")
 if i<len(f)-1:lines.append('duration '+str(max(.001,f[i+1]['at']-r['at'])))
(d/'timing.ffconcat').write_text('\n'.join(lines)+'\n')
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(d/'timing.ffconcat'),'-fps_mode','vfr','-vf','pad=ceil(iw/2)*2:ceil(ih/2)*2','-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart',str(dest)],check=True)
for phase in ['idle','wave','celebrate','think','pose','walk-down','run-down','run-left','outfit-change']:
 seq=[r for r in f if r['phase']==phase]
 if not seq:continue
 r=seq[min(3,len(seq)-1) if phase in ['wave','celebrate','think','pose'] else len(seq)//2]
 subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',str(r['at']),'-i',str(dest),'-frames:v','1',str(d/(phase+'.png'))],check=True)
print(json.dumps({'frames':len(f),'seconds':f[-1]['at'],'movie':str(dest),'method':'Original compositor timestamps; decoded stills saved for inspection.'}))
