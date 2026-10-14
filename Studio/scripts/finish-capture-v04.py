"""Encode actual browser compositor frames at their original recorded intervals."""
from pathlib import Path
import json,subprocess,hashlib
root=Path(__file__).resolve().parents[2];directory=root/'quality-reports/v0.4/capture'
capture=json.loads((directory/'capture.json').read_text());frames=capture['frames'];assert not capture['errors']
lines=['ffconcat version 1.0']
for i,f in enumerate(frames):
 p=(directory/f['file']).resolve();assert p.is_relative_to(directory.resolve()) and p.exists()
 lines.append("file '"+str(p)+"'")
 if i+1<len(frames):
  duration=frames[i+1]['timestamp']-f['timestamp'];assert duration>=0
  lines.append('duration '+str(max(.001,duration)))
lines.append("file '"+str((directory/frames[-1]['file']).resolve())+"'")
concat=directory/'frames.ffconcat';concat.write_text('\n'.join(lines)+'\n')
final=root/'quality-reports/v0.4/living-hanok-v04-motion.mp4'
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(concat),'-an','-fps_mode','vfr','-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p','-movflags','+faststart',str(final)],check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(final)]))
duration=float(probe['format']['duration']);assert duration>15
selected={r['clip']:r for r in capture['samples']}
review=[]
for i,clip in enumerate(['Walk','Run','Jump','Happy','Thinking','Disappointed','Celebration']):
 record=selected[clip];index=min(record['firstFrame']+3,len(frames)-1);time=max(0,frames[index]['timestamp']-frames[0]['timestamp'])
 p=directory/f'review-{clip.lower()}.png'
 subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',str(time),'-i',str(final),'-frames:v','1',str(p)],check=True);review.append({'clip':clip,'time_seconds':time,'file':str(p.relative_to(root))})
report={'status':'RECORDED_AWAITING_VISUAL_INSPECTION','file':str(final.relative_to(root)),'bytes':final.stat().st_size,'sha256':hashlib.sha256(final.read_bytes()).hexdigest(),'duration_seconds':duration,'width':probe['streams'][0]['width'],'height':probe['streams'][0]['height'],'codec':probe['streams'][0]['codec_name'],'native_frame_count':len(frames),'review_frames':review,'timing':'Actual compositor timestamps; VFR, no accelerated playback or synthetic/interpolated frames','fps_note':'Cloud software/compositor recording is not a physical device FPS claim'}
(directory/'media-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
