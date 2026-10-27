from pathlib import Path
import subprocess,json,hashlib
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a';rows=[]
previous={r['source']:r for r in json.loads((D/'media-provenance.json').read_text())}if(D/'media-provenance.json').exists()else{}
files=list((D/'gameplay').glob('*-actual-gameplay.webm'))+list((D/'pilot').glob('*-actual-patrol.webm'))+[D/'cross-zone-actual.webm',D/'stability-actual.webm']
for src in files:
 if not src.exists():continue
 out=src.with_suffix('.mp4');old=previous.get(str(src.relative_to(R)));sourceSHA=hashlib.sha256(src.read_bytes()).hexdigest()
 if old and old['sourceSHA256']==sourceSHA and out.exists()and hashlib.sha256(out.read_bytes()).hexdigest()==old['sha256']:
  rows.append(old);continue
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-an','-c:v','libx264','-threads','1','-preset','fast','-crf','28','-pix_fmt','yuv420p','-fps_mode','passthrough','-movflags','+faststart',str(out)],check=True)
 info=json.loads(subprocess.check_output(['ffprobe','-v','quiet','-show_streams','-show_format','-of','json',str(out)],text=True));v=next(s for s in info['streams']if s['codec_type']=='video');assert[v['width'],v['height']]==[1280,900];rows.append({'file':str(out.relative_to(R)),'source':str(src.relative_to(R)),'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'sourceSHA256':hashlib.sha256(src.read_bytes()).hexdigest(),'size':[v['width'],v['height']],'durationSeconds':float(info['format']['duration']),'method':'Genuine canonical Phaser recording,original input/AI/time; compression-only review copy,no resizing or retiming. Native PNGs remain pixel authority.'});print(out.name,out.stat().st_size,flush=True)
(D/'media-provenance.json').write_text(json.dumps(rows,indent=2)+'\n')
