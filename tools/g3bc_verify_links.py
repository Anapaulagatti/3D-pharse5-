from pathlib import Path
import subprocess,json,hashlib,urllib.request,io,concurrent.futures
from PIL import Image
from zipfile import ZipFile
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-world';commit=subprocess.check_output(['git','rev-parse','checkpoint/g3c-full-world-prototype-20261023^{}'],cwd=R,text=True).strip();base=f'https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/{commit}/docs/gate3-world/';names=['world-overview-review.jpg','world-overview-phaser.png','README.md','VISUAL_INDEX.md','COVERAGE.md','technical-art-qa.json','performance-report.json','movement-report.json','G3D_CONSOLIDATED_PLAN.md','GATE3_WORLD_PROTOTYPE_REVIEW.zip','world-traversal-review.mp4']+[n+'-native.png'for n in ['palace','academy','archive','culture','transition','retail','station','platform','namsan','maru','amusement','market','waterfront','ferry','jeju','oreum','house']]
T=Path('/tmp/g3bc-verified-downloads');T.mkdir(exist_ok=True)
def verify(name):
 url=base+name;dst=T/name;h=hashlib.sha256()
 with urllib.request.urlopen(url,timeout=60)as resp,dst.open('wb')as f:
  while True:
   b=resp.read(1024*1024)
   if not b:break
   h.update(b);f.write(b)
 assert h.hexdigest()==hashlib.sha256((D/name).read_bytes()).hexdigest(),name
 if name.endswith(('.png','.jpg')):Image.open(dst).verify()
 if name.endswith('.zip'):
  with ZipFile(dst)as z:assert z.testzip()is None
 return {'file':name,'url':url,'bytes':dst.stat().st_size,'sha256':h.hexdigest(),'downloadAndContentValidation':'PASS'}
with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:rows=list(pool.map(verify,names))
(D/'published-links.json').write_text(json.dumps({'artifactCommit':commit,'links':rows},indent=2)+'\n');(D/'NATIVE_LINKS.md').write_text('# Verified immutable review links\n\nEvery file downloaded and matched local committed bytes. PNG/JPEG decoded; playable ZIP CRC verified. This is an incomplete prototype, not final artistic acceptance.\n\n'+''.join(f"- [{r['file']}]({r['url']})\n"for r in rows));print('Verified',len(rows),'immutable downloads at',commit)
