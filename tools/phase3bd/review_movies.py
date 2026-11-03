from pathlib import Path
import subprocess,json,hashlib
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3bd';records=[]
for p in sorted(D.rglob('*.webm')):
 if p.name.startswith('page@') or len(p.stem)==32:continue
 out=p.with_suffix('.mp4')
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(p),'-an','-c:v','libx264','-preset','fast','-crf','27','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],check=True)
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(out)]))
 records.append({'file':str(out.relative_to(D)),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'bytes':out.stat().st_size,'sourceCaptureSHA256':hashlib.sha256(p.read_bytes()).hexdigest(),'nativeCapture':[960,640],'videoEncoding':'H264 lossy review encoding; PNGs are pixel-fidelity evidence; no resizing','audioStreams':sum(s['codec_type']=='audio'for s in probe['streams'])})
(D/'VIDEO_PROOF.json').write_text(json.dumps({'scope':'Actual local Phaser keyboard/touch recordings; no synthetic animation or soundtrack','videos':records},indent=2)+'\n')
print('Encoded',len(records),'real gameplay movies')
