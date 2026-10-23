from pathlib import Path
import subprocess,json,hashlib,urllib.request,io
from PIL import Image
from zipfile import ZipFile
R=Path(__file__).resolve().parents[1];D=R/'docs/g3a-platform-restoration';commit=subprocess.check_output(['git','rev-parse','checkpoint/g3a-platform-appearance-restored-20261023^{}'],cwd=R,text=True).strip();base=f'https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/{commit}/docs/g3a-platform-restoration/';rows=[]
for name in ['restored-station-native.png','restored-station-juni-native.png','BEFORE_RESTORED_1X.png','collision-overlay-native.png','platform-before-1x.png','platform-restored-1x.png','qa-report.json','COLLISION_PROPOSAL.md','G3A_PLATFORM_RESTORED_REVIEW.zip']:
 url=base+name;data=urllib.request.urlopen(url,timeout=60).read();assert data==(D/name).read_bytes()
 if name.endswith('.png'):Image.open(io.BytesIO(data)).verify()
 if name.endswith('.zip'):
  with ZipFile(io.BytesIO(data))as z:assert z.testzip()is None
 rows.append({'file':name,'url':url,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'downloadAndDecode':'PASS'})
(D/'published-links.json').write_text(json.dumps({'artifactCommit':commit,'links':rows},indent=2)+'\n')
(D/'NATIVE_LINKS.md').write_text('# Verified immutable review links\n\nAll links downloaded and matched committed bytes; PNG decode / ZIP CRC verified.\n\n'+'\n'.join(f"- [{r['file']}]({r['url']})"for r in rows)+'\n\nG3-B blocked. Station transfer blocked. Human review pending.\n')
print('Verified',len(rows),'immutable review downloads at',commit)
