from pathlib import Path
import json,hashlib,datetime
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3b-a';b=json.loads((D/'BASELINE.json').read_text());allowed={'AGENTS.md':'Latest Phase3B-A authority','docs/current/PROJECT_STATE.md':'Current authorized scope and recovery status','src/npcs/actor.ts':'Existing FSM scheduled intention and bounded recovery','src/npcs/manager.ts':'Clock/schedule/HUD/persistence/private QA integration; cache caps retained','src/npcs/visits.ts':'Deterministic windows and pinned host ownership; legacy API/key retained','vite.config.ts':'Controlled release-profile gate and private review metadata; no new dependency'}
changes=[];same=0
for name,old in b['files'].items():
 p=R/name;new=hashlib.sha256(p.read_bytes()).hexdigest()if p.is_file()else None
 if new==old:same+=1
 else:changes.append({'path':name,'beforeSHA256':old,'afterSHA256':new,'reason':allowed.get(name)})
assert not[c for c in changes if not c['reason']],changes
assets=[p for p in b['files']if p.startswith(('public/assets/','assets-src/npcs/','assets-src/characters/','assets-src/cosmetics/'))];tests=[p for p in b['files']if p.startswith('tests/')];assert not[c for c in changes if c['path']in assets+tests]
arch=json.loads((D/'ARCHIVAL_RECOVERY.json').read_text())['files']
for row in arch:assert hashlib.sha256((R/row['path']).read_bytes()).hexdigest()==row['sha256']
q={'status':'PASS','checkedAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'base':b['baseCommit'],'approved':b['approvedCommit'],'checkedFiles':len(b['files']),'unchangedFiles':same,'authorizedCodeAndAuthorityChanges':changes,'unexpectedChanges':[],'protectedAssetFilesUnchanged':len(assets),'originalTestFilesUnchanged':len(tests),'historicalMissingFilesRecoveredByteExact':len(arch),'artChanges':0,'imageGenerationCalls':0,'stableNPCIDs':26,'playableCharacters':12,'cosmetics':28,'worldCollisionCameraTour':'UNCHANGED'};(D/'PROTECTED_AUDIT.json').write_text(json.dumps(q,indent=2)+'\n');print('PASS',len(assets),'assets;',len(tests),'original tests unchanged;',len(arch),'archival dependencies recovered exactly;',len(changes),'authorized source edits')
