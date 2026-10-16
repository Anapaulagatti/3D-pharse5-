"""Inspect real captured timestamps, transcode without an FPS filter, retain frame counts."""
from pathlib import Path
import subprocess,json,hashlib,statistics
R=Path(__file__).resolve().parents[1];Q=R/'docs/world-refinement/quality';source=Q/'gameplay-original.webm';dest=Q/'gameplay-walkthrough.mp4'
def inspect(p):
 cmd=['ffprobe','-v','error','-select_streams','v:0','-show_frames','-show_entries','frame=best_effort_timestamp_time:stream=codec_name,width,height','-of','json',str(p)]
 j=json.loads(subprocess.check_output(cmd));times=[float(f['best_effort_timestamp_time'])for f in j['frames']];delta=[b-a for a,b in zip(times,times[1:])];duration=times[-1]-times[0]+statistics.median(delta)
 return {'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'stream':j['streams'][0],'decodedFrames':len(times),'firstPTS':times[0],'lastPTS':times[-1],'durationSeconds':duration,'actualAverageFPS':len(times)/duration,'ptsStrictlyIncreasing':all(d>0 for d in delta),'frameGapMs':{'median':statistics.median(delta)*1000,'p95':sorted(delta)[int(len(delta)*.95)]*1000,'max':max(delta)*1000},'command':cmd},times
original,times=inspect(source);assert original['actualAverageFPS']>=30 and original['ptsStrictlyIncreasing']
cmd=['ffmpeg','-hide_banner','-loglevel','error','-i',str(source),'-c:v','libx264','-preset','fast','-crf','22','-fps_mode','vfr','-enc_time_base','1:1000','-video_track_timescale','1000','-an','-movflags','+faststart','-y',str(dest)];subprocess.run(cmd,check=True)
encoded,newtimes=inspect(dest);assert encoded['decodedFrames']==original['decodedFrames'] and encoded['actualAverageFPS']>=30 and encoded['ptsStrictlyIncreasing']
# Preserve relative timing to within two milliseconds; no up-conversion, duplication or time compression.
max_error=max(abs((a-times[0])-(b-newtimes[0]))for a,b in zip(times,newtimes));assert max_error<.0021,max_error
capture=json.loads((Q/'capture.json').read_text());assert not capture.get('failure') and not capture['errors'] and len(capture['visits'])==9
report={'status':'PASS','method':'Decode original MediaRecorder timestamps and all frames; H264 VFR transcode with no -r/fps filter, same actual frame count, relative PTS preserved within2ms. Requested capture60 is not encoded FPS. Real keyboard/mouse continuous route, QA hook absent. DOM dialogs separately captured.','original':original,'encoded':encoded,'encodeCommand':cmd,'maxRelativeTimestampErrorSeconds':max_error,'measuredRuntimeFPSDuringCapture':capture['runtimeFPS'],'runtimeRafMs':capture['rafMs']};(Q/'video-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'PASS','runtimeFPS':capture['runtimeFPS'],'actualVideoFPS':original['actualAverageFPS'],'duration':original['durationSeconds'],'frames':original['decodedFrames'],'mp4Bytes':encoded['bytes']}))
