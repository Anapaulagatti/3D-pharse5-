"""Lossy video REVIEW copies: native-pixel crops, never resizes; full originals unchanged."""
from pathlib import Path
import json,subprocess,hashlib,concurrent.futures
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a-final-six';q=json.loads((D/'actual-gameplay.json').read_text());out=D/'review-clips';out.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def make(row):
 id=row['id'];src=D/'gameplay'/(id+'-actual.mp4');dst=out/(id+'-native-crop.mp4');first=min(c['seconds']for c in q['captures']if c['id']==id and c['audit']['actualFrame'].startswith('walk'));start=max(0,first-1.2)
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(start),'-i',str(src),'-vf','crop=960:640:160:130','-an','-c:v','libx264','-crf','24','-preset','veryfast','-threads','2','-pix_fmt','yuv420p','-movflags','+faststart',str(dst)],check=True)
 return {'id':id,'source':str(src.relative_to(D)),'sourceSHA256':sha(src),'reviewFile':str(dst.relative_to(D)),'reviewSHA256':sha(dst),'reviewBytes':dst.stat().st_size,'startSeconds':start,'crop':[160,130,960,640],'spatialResampling':False,'description':'One continuous excerpt from first visible walk through greeting,source notice,vocabulary,close. Native crop preserves dialogue and Juni; original1280x900fullrecording remains versioned.'}
with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:rows=list(pool.map(make,q['rows']))
(D/'REVIEW_CLIP_PROVENANCE.json').write_text(json.dumps({'rows':rows,'purpose':'Portable review ZIP underGitHub100MiB cap without removing gameplay evidence or changing source art','originalsChanged':False},indent=2)+'\n');print('Native crop review clips',sum(r['reviewBytes']for r in rows),'bytes')
