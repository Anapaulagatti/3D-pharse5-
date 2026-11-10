from pathlib import Path
import json,hashlib,subprocess
R=Path.cwd();base='18babd92b45c67d9c766ce262ca7b689da910d4b';files={}
for name in subprocess.check_output(['git','diff','--name-only','--diff-filter=M',base,'--','src'],text=True).splitlines():
 p=R/name
 before=subprocess.check_output(['git','show',base+':'+name]);after=p.read_bytes()
 if before!=after:files[name]={'beforeSHA256':hashlib.sha256(before).hexdigest(),'afterSHA256':hashlib.sha256(after).hexdigest()}
(R/'docs/roadmap-v4/AUTHORIZED_AMENDMENTS.json').write_text(json.dumps({'base':base,'authority':'Owner MASTER PROMPT V4 2026-11-10; exact local gameplay/Hangul/rooms/farm/Jeju amendments. Original art masks atlases movement/camera immutable. No public approval implied.','files':files},indent=2)+'\n');print(len(files),'exact code amendments; original assets excluded')
