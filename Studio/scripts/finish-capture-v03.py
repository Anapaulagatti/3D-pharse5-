"""Trim loading from real browser recordings, concatenate and inspect media metadata."""
import json,pathlib,subprocess,hashlib
root=pathlib.Path(__file__).resolve().parents[2]
directory=root/'quality-reports/v0.3/capture'
capture=json.loads((directory/'capture.json').read_text())
reviewed=json.loads((directory/'visual-trims.json').read_text()) if (directory/'visual-trims.json').exists() else {}
parts=[]
for record in capture['records']:
    path=pathlib.Path(record['path']).resolve()
    if not path.is_relative_to(directory.resolve()):raise SystemExit('Unexpected recording path')
    if record['errors']:raise SystemExit('Browser recording had page errors')
    output=directory/(record['scene']+'-trimmed.mp4')
    trim=reviewed.get(record['scene'],{})
    limit=['-t',str(trim['duration_seconds'])] if 'duration_seconds' in trim else []
    subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',str(record['trimStart']+trim.get('additional_start_seconds',0)),'-i',str(path),*limit,
                    '-an','-c:v','libx264','-preset','fast','-crf','22','-pix_fmt','yuv420p','-movflags','+faststart',str(output)],check=True)
    parts.append(output)
concat=directory/'concat.txt';concat.write_text(''.join("file '"+str(p)+"'\n" for p in parts))
final=root/'quality-reports/v0.3/living-hanok-motion.mp4'
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(concat),'-c','copy','-movflags','+faststart',str(final)],check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(final)]))
duration=float(probe['format']['duration'])
if duration<12:raise SystemExit('Actual movement recording is too short')
for i,fraction in enumerate([.08,.26,.52,.78]):
    subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',str(duration*fraction),'-i',str(final),'-frames:v','1',str(directory/f'review-frame-{i+1}.png')],check=True)
report={'status':'RECORDED','file':str(final.relative_to(root)),'bytes':final.stat().st_size,
        'sha256':hashlib.sha256(final.read_bytes()).hexdigest(),'duration_seconds':duration,
        'width':probe['streams'][0]['width'],'height':probe['streams'][0]['height'],
        'codec':probe['streams'][0]['codec_name'],'playback':'Real-time browser capture, only loading trimmed; no speed-up or interpolated frames',
        'fps_note':'Encoder/container FPS is not measured GPU or physical-phone FPS',
        'reviewed_startup_trims':reviewed,
        'visual_inspection':'Review extracted real video frames before claiming visual inspection complete'}
(directory/'media-report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
