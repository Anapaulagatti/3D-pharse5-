from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[2];base=json.loads((R/'docs/phase3bd/BASELINE.json').read_text())['base'];files={}
for name in ['src/gate3/main.ts','src/npcs/manager.ts','src/quests/content.ts','src/quests/manager.ts','src/quests/ui.ts','vite.config.ts','tools/check_preservation.py','tools/g3d_prepare.py','tools/g3d_build_pilots.py','tools/g3d_validate.py']:
 before=subprocess.check_output(['git','show',base+':'+name],cwd=R);after=(R/name).read_bytes();files[name]={'beforeSHA256':hashlib.sha256(before).hexdigest(),'afterSHA256':hashlib.sha256(after).hexdigest()}
(R/'docs/phase3bd/AUTHORIZED_AMENDMENTS.json').write_text(json.dumps({'base':base,'authority':'HUMAN_DIRECTIVE.md Phase3BD; exact code changes and historical reconstruction only after matching current pins. Artwork and current world checked independently.','files':files},indent=2)+'\n')
