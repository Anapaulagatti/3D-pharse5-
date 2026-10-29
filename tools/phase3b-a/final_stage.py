from pathlib import Path
from zipfile import ZipFile
import subprocess,json,time,hashlib
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3b-a';report=D/'full-e2e/e2e-results.json'
for attempt in range(600):
 if report.exists():
  q=json.loads(report.read_text());s=q['stats'];assert s['expected']==72 and s['unexpected']==0 and s['flaky']==0 and s['skipped']==0,s
  if '72 passed' in(D/'full-e2e.log').read_text():break
 time.sleep(2)
else:raise RuntimeError('Final full E2E incomplete; no final package produced')
for file in ['protect.py','status_docs.py','package.py']:subprocess.run(['python3',str(R/'tools/phase3b-a'/file)],cwd=R,check=True)
p=json.loads((D/'PACKAGE_PROOF.json').read_text());out=Path('/tmp/phase3ba-private-extracted')
with ZipFile(D/p['file'])as z:
 assert z.testzip()is None;z.extractall(out);manifest=json.loads(z.read('PACKAGE_SHA256.json'))
 for name,h in manifest.items():assert hashlib.sha256((out/name).read_bytes()).hexdigest()==h,name
p['extraction']={'status':'PASS','files':len(manifest),'directory':str(out),'allExtractedSHA256':'PASS'};(D/'PACKAGE_PROOF.json').write_text(json.dumps(p,indent=2)+'\n');print('FINAL PRIVATE EXTRACTION READY',len(manifest),'files',flush=True)
