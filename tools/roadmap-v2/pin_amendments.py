from pathlib import Path
import subprocess,hashlib,json
R=Path.cwd();base='c2240e5e963fe277734961f8eb3ecd97efad8e04';files={}
for name in subprocess.check_output(['git','diff','--name-only',base,'--','src'],text=True).splitlines():
 p=R/name
 if not p.exists():continue
 before=subprocess.check_output(['git','show',base+':'+name])
 files[name]={'beforeSHA256':hashlib.sha256(before).hexdigest(),'afterSHA256':hashlib.sha256(p.read_bytes()).hexdigest()}
Path('docs/roadmap-v2/AUTHORIZED_AMENDMENTS.json').write_text(json.dumps({'base':base,'authority':'Owner MASTER PROMPT V2 seven local workstreams, 2026-11-04. Exact additive integrations only; protected artwork bytes and original movement/camera unchanged. Historical checks retain exact predecessor bytes, new behavior separately tested.','files':files},indent=2)+'\n')
