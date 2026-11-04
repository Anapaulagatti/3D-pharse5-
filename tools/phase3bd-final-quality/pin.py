from pathlib import Path
import json,hashlib,subprocess
R=Path.cwd();D=R/'docs/phase3bd-final-quality';base=json.loads((D/'BASELINE.json').read_text())['base'];rows={}
for name in subprocess.check_output(['git','diff','--name-only',base],text=True).splitlines():
 if not name.startswith(('src/','tools/phase3bb/amendments.py','tools/phase3bd/runtime_assets.py','tests/unit/phase3bb-amendments.ts')):continue
 old=subprocess.run(['git','show',base+':'+name],capture_output=True)
 if old.returncode:continue
 rows[name]={'beforeSHA256':hashlib.sha256(old.stdout).hexdigest(),'afterSHA256':hashlib.sha256((R/name).read_bytes()).hexdigest()}
(D/'AUTHORIZED_AMENDMENTS.json').write_text(json.dumps({'base':base,'authority':'Owner final quality directive: native component/cell art, save-compatible per-cell farming and exact western-hanok mask correction; old approvals immutable','files':rows},indent=2)+'\n')
