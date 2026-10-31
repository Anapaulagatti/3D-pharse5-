"""Encode every actual browser capture at original VFR timing; no cuts/retiming."""
from pathlib import Path
import json,subprocess,hashlib,sys,math
R=Path(__file__).resolve().parents[1];C=Path(sys.argv[1]if len(sys.argv)>1 else R/'.cache/v9-video-candidate').resolve();j=json.loads((C/'capture.json').read_text());assert j['status']=='PASS';frames=j['frames'];Q=R/'docs/v9-world/quality/video';Q.mkdir(parents=True,exist_ok=True);out=Q/'v9-gameplay.mp4'
assert all(b['timestamp']>a['timestamp']for a,b in zip(frames,frames[1:])), 'Non-increasing actual capture timestamp needs diagnosis, not silent dropping'
lines=['ffconcat version 1.0']
for i,f in enumerate(frames):
 path=C/f['file'];assert hashlib.sha256(path.read_bytes()).hexdigest()==f['sha256'];lines+=['file '+repr(f['file']),'option framerate 1000']
 if i+1<len(frames):lines+=['duration '+format(frames[i+1]['timestamp']-f['timestamp'],'.6f')]
concat=C/'encoding.ffconcat';concat.write_text('\n'.join(lines)+'\n');duration=j['elapsedSeconds'];rate=min(1800,max(400,math.floor(78*1024*1024*8/duration/1000)));cmd=['ffmpeg','-y','-safe','0','-i',str(concat),'-an','-c:v','libx264','-preset','fast','-threads','2','-crf','21','-maxrate',str(rate)+'k','-bufsize',str(rate*2)+'k','-pix_fmt','yuv420p','-fps_mode','passthrough','-enc_time_base','1:1000','-video_track_timescale','1000','-movflags','+faststart',str(out)]
with (C/'encoding.log').open('w')as log:subprocess.run(cmd,cwd=C,stdout=log,stderr=subprocess.STDOUT,check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','frame=best_effort_timestamp_time','-of','json',str(out)]));pts=[float(f['best_effort_timestamp_time'])for f in probe['frames']];assert len(pts)==len(frames),(len(pts),len(frames));start=frames[0]['timestamp'];max_error=max(abs(p-(f['timestamp']-start))for p,f in zip(pts,frames));assert max_error<=.0011,max_error
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out)]));assert out.stat().st_size<100000000
receipt={k:v for k,v in j.items()if k!='frames'};receipt.update(status='PASS',capturedFrames=len(frames),encodedFrames=len(pts),maxTimestampErrorSeconds=max_error,output={'file':'quality/video/v9-gameplay.mp4','bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'width':info['streams'][0]['width'],'height':info['streams'][0]['height'],'duration':float(info['format']['duration'])},encoding={'command':cmd,'capture':'JPEG78 browser frames, everyNthFrame2','lossless':False,'timing':'Every delivered original frame retained; actual timestamps quantized to1ms. No speed changes, cuts, interpolation or replacement footage.'},playbackVerified=False)
(Q/'encoding-verification.json').write_text(json.dumps(receipt,indent=2)+'\n');(Q/'source-frames.json').write_text(json.dumps(frames));print(json.dumps({k:receipt[k]for k in ['capturedFrames','encodedFrames','maxTimestampErrorSeconds','output']}))
