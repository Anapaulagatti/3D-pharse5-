"""Build the review only after actual full-suite completion; never infer PASS from a partial log."""
from pathlib import Path
from zipfile import ZipFile
import time,json,subprocess,hashlib
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a-identity-safeguard'
report=D/'full-e2e/e2e-results.json'
for attempt in range(600):
 if report.exists():
  q=json.loads(report.read_text());stats=q['stats']
  assert stats['expected']==69 and stats['unexpected']==0 and stats['flaky']==0 and stats['skipped']==0,stats
  if '69 passed' in (D/'full-e2e.log').read_text():break
 time.sleep(2)
else:raise RuntimeError('Full E2E did not complete; no final package produced')
for script in ['protect.py','status_docs.py','package.py']:
 subprocess.run(['python3',str(R/'tools/phase3a-identity-safeguard'/script)],check=True,cwd=R)
p=json.loads((D/'PACKAGE_PROOF.json').read_text());out=Path('/tmp/phase3a-identity-extracted')
with ZipFile(D/p['file']) as z:
 assert z.testzip() is None
 z.extractall(out)
 manifest=json.loads(z.read('PACKAGE_SHA256.json'))
 for n,h in manifest.items():assert hashlib.sha256((out/n).read_bytes()).hexdigest()==h,n
p['extraction']={'status':'PASS','files':len(manifest),'directory':str(out),'allExtractedSHA256':'PASS'};(D/'PACKAGE_PROOF.json').write_text(json.dumps(p,indent=2)+'\n');print('FINAL EXTRACTED REVIEW READY',len(manifest),'files',flush=True)
