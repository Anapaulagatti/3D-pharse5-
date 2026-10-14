"""Encode actual compositor JPEGs using their original intervals, with no speedup."""
from pathlib import Path
import json,subprocess,hashlib
root=Path(__file__).resolve().parents[2];d=root/'quality-reports/v0.6/prototype/capture';j=json.loads((d/'capture.json').read_text());frames=j['frames'];assert not j['errors']
lines=['ffconcat version 1.0']
for i,f in enumerate(frames):
 p=(d/f['file']).resolve();assert p.is_relative_to(d.resolve()) and p.exists();lines.append("file '"+str(p)+"'")
 if i+1<len(frames):
  duration=frames[i+1]['timestamp']-f['timestamp'];assert duration>=0;lines.append('duration '+str(max(.001,duration)))
lines.append("file '"+str((d/frames[-1]['file']).resolve())+"'");concat=d/'frames.ffconcat';concat.write_text('\n'.join(lines)+'\n');dst=root/'quality-reports/v0.6/playful-hangeul-town-v06-prototype.mp4'
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(concat),'-an','-fps_mode','vfr','-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p','-movflags','+faststart',str(dst)],check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(dst)]));review=[]
for e in ['walk','run','jump','greeting','celebration','happy-emotion','face-happy','face-surprised','face-celebrating']:
 s=next(x for x in j['samples'] if x['event']==e);next_sample=next((x for x in j['samples'] if x['firstFrame']>s['firstFrame']),{'firstFrame':len(frames)});idx=min(len(frames)-1,s['firstFrame']+max(0,(next_sample['firstFrame']-s['firstFrame'])//2));p=d/('review-'+e+'.png')
 # Prefer a known genuine gesture frame; a long interval until the next event
 # may include later native locomotion after a one-shot gesture completes.
 if e in ['greeting','celebration','jump']:idx=min(len(frames)-1,s['firstFrame']+1)
 # Decode the exact source timestamp's video frame; preserve the raw frame list.
 time=max(0,frames[idx]['timestamp']-frames[0]['timestamp']);subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',str(time),'-i',str(dst),'-frames:v','1',str(p)],check=True);review.append({'event':e,'source_frame':idx,'time_seconds':time,'file':str(p.relative_to(root))})
report={'status':'RECORDED_PENDING_VISUAL_REVIEW','file':str(dst.relative_to(root)),'bytes':dst.stat().st_size,'sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'duration_seconds':float(probe['format']['duration']),'width':probe['streams'][0]['width'],'height':probe['streams'][0]['height'],'native_frame_count':len(frames),'timing':'Native compositor VFR timestamps. No interpolation, retiming, accelerated gameplay or synthetic frames.','renderer':'Cloud SwiftShader. This video is not a physical-device FPS claim.','review_frames':review};(d/'media-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
