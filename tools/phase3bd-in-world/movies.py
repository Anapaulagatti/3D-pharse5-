from pathlib import Path
import subprocess,json,hashlib
D=Path('docs/phase3bd-in-world');rows=[]
for p in (D/'videos').glob('*.webm'):
 if len(p.stem)==32 or p.name.startswith('page@'):continue
 out=p.with_suffix('.mp4');subprocess.run(['ffmpeg','-v','error','-y','-i',str(p),'-an','-c:v','libx264','-preset','veryfast','-threads','1','-crf','28','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],check=True)
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out)]));assert not any(s['codec_type']=='audio'for s in probe['streams'])
 rows.append({'file':str(out.relative_to(D)),'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'captureSHA256':hashlib.sha256(p.read_bytes()).hexdigest(),'seconds':probe['format']['duration'],'recording':'Actual Phaser WASD/touch, no synthetic animation or soundtrack','compression':'H264 lossy review, no resizing; PNG is native pixel evidence','audioStreams':0})
(D/'VIDEO_PROOF.json').write_text(json.dumps({'videos':rows,'physicalDevices':'NOT TESTED'},indent=2)+'\n')
