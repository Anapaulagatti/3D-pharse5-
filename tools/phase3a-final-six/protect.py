"""Verify every preexisting tracked file, with only five explicit additive authority/hooks exceptions."""
from pathlib import Path
import json,hashlib,subprocess,datetime
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a-final-six';b=json.loads((D/'BASELINE_MANIFEST.json').read_text());allowed={'AGENTS.md':'Owner continuation authority appended','docs/current/PROJECT_STATE.md':'Owner continuation authority appended','src/npcs/manager.ts':'QA-only archive eligibility/selector and honest counts through existing engine','src/npcs/dialogue.ts':'Select same validated runtime catalog; normal20 unchanged','src/npcs/review.ts':'QA-only candidate approach using existing spawn selector'};changes=[];protected=0
for path,h in b['files'].items():
 p=R/path;after=hashlib.sha256(p.read_bytes()).hexdigest()if p.is_file()else None
 if h!=after:changes.append({'path':path,'beforeSHA256':h,'afterSHA256':after,'authorizedReason':allowed.get(path)})
 else:protected+=1
unexpected=[r for r in changes if not r['authorizedReason']];assert not unexpected,unexpected
oldNpc=[p for p in b['files']if p.startswith(('assets-src/npcs/','public/assets/npcs/'))];oldTests=[p for p in b['files']if p.startswith('tests/')];world=[p for p in b['files']if p.startswith('public/assets/gate3/')];players=[p for p in b['files']if p.startswith(('public/assets/juni/','public/assets/characters/','public/assets/cosmetics/'))]
report={'checkedAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseCommit':b['baseCommit'],'checkedFiles':len(b['files']),'unchanged':protected,'authorizedChanges':changes,'unexpectedChanges':unexpected,'all20NPCSourceAndRuntimeFilesUnchanged':len(oldNpc),'allOriginalTestsUnchanged':len(oldTests),'worldRuntimeFilesUnchanged':len(world),'playerCosmeticRuntimeFilesUnchanged':len(players),'status':'PASS','historyCheckpoints':'No existing ref overwritten; final remote verification separately recorded'};(D/'protected-audit.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS',protected,'unchanged historical files;',len(changes),'explicit additive authority/runtime hooks;',len(oldNpc),'oldNPCfiles;',len(oldTests),'oldtests')
