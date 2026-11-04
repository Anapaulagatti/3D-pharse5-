from pathlib import Path
import json,hashlib,subprocess
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3bd-in-world';base=json.loads((D/'BASELINE.json').read_text())['base'];rows={}
for n in subprocess.check_output(['git','diff','--name-only',base],cwd=R,text=True).splitlines():
 if not n.startswith(('src/','review-portal/','tools/phase3bb/amendments.py','tools/phase3bd/runtime_assets.py','tests/unit/phase3bb-amendments.ts')):continue
 old=subprocess.run(['git','show',base+':'+n],cwd=R,capture_output=True)
 if old.returncode:continue
 rows[n]={'beforeSHA256':hashlib.sha256(old.stdout).hexdigest(),'afterSHA256':hashlib.sha256((R/n).read_bytes()).hexdigest()}
(D/'AUTHORIZED_AMENDMENTS.json').write_text(json.dumps({'base':base,'authority':'HUMAN_DIRECTIVE.md: physical interaction/UI redesign. Art/camera/movement/collision checked separately; exact preimages required.','files':rows},indent=2)+'\n')
