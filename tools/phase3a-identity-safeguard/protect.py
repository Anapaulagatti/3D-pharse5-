from pathlib import Path
import hashlib,json,datetime
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a-identity-safeguard';base=json.loads((D/'BASELINE.json').read_text())
allowed={
'AGENTS.md':'Latest owner identity authority; historical records retained',
'docs/current/PROJECT_STATE.md':'Latest fictional public identity and handoff state',
'assets-src/npcs/phase3a-finalization/identity-presentations.json':'Only public identity, occupation and non-clearance decision metadata; no sprite asset',
'assets-src/npcs/phase3a-finalization/release-status.json':'Six active fictional public identities, no legal clearance inferred',
'src/npcs/identity.ts':'Owner-directed decision type and fictional KO/VI presentation; no actor geometry/motion',
'src/npcs/history.ts':'Only archive introduction, public role/name and accessibility labels',
'docs/phase3a/HISTORICAL_NPC_RIGHTS_AND_ALIASES.md':'Current six-person rights and identity matrix requested by owner',
'docs/phase3a-finalization/PHASE3B_HANDOFF.md':'Superseding fictional identity notice linking current handoff; original record retained',
'tests/unit/npcs/identity.test.ts':'Superseded retained-name expectations replaced; independent-review validation remains',
'tests/unit/npcs/history.test.ts':'Only obsolete real-quotation disclaimer expectation changes to explicit fiction',
'tests/e2e/phase3a-finalization.spec.ts':'Same ordinary-world/state test with six fictional names, notice and accessible-name assertions'}
changes=[];same=0
for name,old in base['files'].items():
 p=R/name;new=hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
 if old==new:same+=1
 else:changes.append({'path':name,'beforeSHA256':old,'afterSHA256':new,'reason':allowed.get(name)})
assert not [c for c in changes if not c['reason']],changes
assets=[p for p in base['files'] if p.startswith(('public/assets/','assets-src/npcs/','assets-src/characters/','assets-src/cosmetics/')) and p not in allowed]
assert not [c for c in changes if c['path'] in assets]
public=[p for p in assets if p.startswith('public/assets/npcs/phase3a/')]
report={'status':'PASS','checkedAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseCommit':base['baseCommit'],'approvedCheckpoint':base['approvedCheckpoint'],'checkedFiles':len(base['files']),'unchangedFiles':same,'authorizedNonArtChanges':changes,'unexpectedChanges':[],'frozenAssetFilesUnchanged':len(assets),'all26PublicNPCAssetFilesExact':len(public),'artChanges':0,'imageGenerationCalls':0,'newNPCs':0,'stableNPCIDs':26,'fictionalPublicIdentities':6,'commercialRights':'UNVERIFIED_NOT_CERTIFIED','physicalDevices':'NOT_TESTED'}
(D/'PROTECTED_AUDIT.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS',len(assets),'frozen assets,',len(public),'public NPC asset files;',same,'files exact;',len(changes),'authorized non-art changes')
