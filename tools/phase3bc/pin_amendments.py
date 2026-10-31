from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[2];base='5ced846ca7df9ec3d8996ba0cfd256c55ec0afc7'
files=['src/characters/appearance.ts','src/gate3/WorldCache.ts','src/gate3/main.ts','src/npcs/manager.ts','src/npcs/dialogue.ts']
rows={}
for p in files:
 old=subprocess.check_output(['git','show',base+':'+p],cwd=R)
 rows[p]={'beforeSHA256':hashlib.sha256(old).hexdigest(),'afterSHA256':hashlib.sha256((R/p).read_bytes()).hexdigest()}
(R/'docs/phase3bc/AUTHORIZED_AMENDMENTS.json').write_text(json.dumps({'base':base,'authority':'HUMAN_DIRECTIVE.md Phase3BC explicit successor; historical baselines/art remain unchanged; current behavior independently tested','files':rows},indent=2)+'\n')
