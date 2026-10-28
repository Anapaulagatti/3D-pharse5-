"""Short direct excerpts from actual canonical-world recordings, no scale/composite/synthetic frames."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess,json,hashlib
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a-npc-expansion';O=D/'review-clips';O.mkdir(exist_ok=True);rows=json.loads((D/'after-capture.json').read_text())['rows']
def clip(row):
 id=row['id'][4:];source=D/f'gameplay/after-{id}-actual.webm';greet=next(e['seconds']for e in row['events']if e['prefix'].startswith('greet'));start=max(0,greet-4);duration=max(3,min(8,row['seconds']-start));out=O/f'{id}-actual-approach.mp4';subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(start),'-i',str(source),'-t',str(duration),'-an','-vf','crop=640:512:320:192','-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p','-movflags','+faststart','-threads','2',str(out)],check=True);return{'id':id,'source':str(source.relative_to(R)),'sourceSHA256':hashlib.sha256(source.read_bytes()).hexdigest(),'file':str(out.relative_to(R)),'startSeconds':start,'durationSeconds':duration,'pixelDimensions':'640x512 native crop from original1280x900; no spatial resampling','nativeCrop':[320,192,640,512],'provenance':'Direct actual Juni approach, conversation and return excerpt; canonical world, original controls'}
with ThreadPoolExecutor(max_workers=2)as pool:proof=list(pool.map(clip,rows))
(D/'review-clips-provenance.json').write_text(json.dumps(proof,indent=2)+'\n');print('Created17direct real gameplay excerpts,MiB',sum(p.stat().st_size for p in O.glob('*.mp4'))/1048576)
