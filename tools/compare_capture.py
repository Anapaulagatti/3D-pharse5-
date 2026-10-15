"""Concatenate genuine archived before and current after footage, original speeds; label both."""
from pathlib import Path
import json,subprocess,hashlib
R=Path(__file__).resolve().parents[1];C=R/'.cache/review';Q=R/'docs/review';Q.mkdir(exist_ok=True);before=R/'.cache/before-3b62e9b.mp4';after=C/'after.mp4'
font='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf';clips=[]
for name,src,label,seek,duration in [('before',before,'BEFORE / archived 3b62e9b / original speed',30.716849,5.8),('after',after,'AFTER / animation + historical guests / original speed',0,None)]:
 dest=C/(name+'-labelled.mp4');cmd=['ffmpeg','-y','-loglevel','error']
 if seek:cmd+=['-ss',str(seek)]
 cmd+=['-i',str(src)]
 if duration:cmd+=['-t',str(duration)]
 cmd+=['-vf',f"drawbox=x=0:y=0:w=iw:h=58:color=0x303e47:t=fill,drawtext=fontfile={font}:text='{label}':x=28:y=16:fontsize=24:fontcolor=0xfff4dc",'-fps_mode','vfr','-c:v','libx264','-pix_fmt','yuv420p','-an',str(dest)];subprocess.run(cmd,check=True);clips.append(dest)
concat=C/'compare.ffconcat';concat.write_text('\n'.join("file '"+str(p)+"'" for p in clips)+'\n')
dest=Q/'animation-review.mp4';subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(concat),'-fps_mode','vfr','-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart',str(dest)],check=True)
meta={'method':'Genuine archived BEFORE excerpt then current actual Phaser AFTER. Label overlays only; original timestamps/speeds retained. No simulated sprite video or time scaling.','before_tag':'recovery/pixel-before-anim-cleanup-20261015','before_commit':'3b62e9b772e9d1e542d13b951ba67a0744c38c35','before_original_path':'quality-reports/chibi-v1/chibi-avatar-gameplay.mp4','before_sha256':hashlib.sha256(before.read_bytes()).hexdigest(),'before_excerpt_seconds':[30.716849,36.516849],'after_frames':len(json.loads((C/'motion/capture.json').read_text())['frames']),'after_seconds':json.loads((C/'motion/capture.json').read_text())['frames'][-1]['at'],'final_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'final_bytes':dest.stat().st_size}
(Q/'capture-provenance.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps(meta))
