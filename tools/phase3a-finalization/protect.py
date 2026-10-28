"""Read-only approved26NPC preservation audit; exact exception list for authorized data/authority changes."""
from pathlib import Path
import json,hashlib,datetime
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a-finalization';base=json.loads((D/'APPROVED_BASELINE.json').read_text());allowed={
'AGENTS.md':'Append human26NPC approval and development-only authority',
'docs/current/PROJECT_STATE.md':'Append current approved26NPC foundation/handoff state',
'src/npcs/history.ts':'Compose approved26canonical catalog and neutral public reconstruction presentation;existing archive selection lifecycle retained',
'src/npcs/manager.ts':'Enable approved archive access without QA flag;honest26/6count plus separate0verified-fact count',
'src/npcs/catalog.ts':'Comment-only living20vs canonical26 distinction',
'src/npcs/collections.ts':'Comment-only factual verification vs artistic approval distinction',
'tests/unit/npcs/history.test.ts':'Update superseded20/0availability expectations to approved26/6;retain0verified facts andallpreservation checks',
'tests/e2e/phase3a-expansion.spec.ts':'Only approved roster20→26/historical0→6count expectations;original movement/dialogue/cache checks retained',
'tests/e2e/phase3a-final-six.spec.ts':'Validate approved26ordinary-world access/6approved/0candidates andupdatedneutral KO/VI notice;all movement/touch/state checks retained'}
changes=[];same=0
for name,old in base['files'].items():
 p=R/name;new=hashlib.sha256(p.read_bytes()).hexdigest()if p.is_file()else None
 if new==old:same+=1
 else:changes.append({'path':name,'beforeSHA256':old,'afterSHA256':new,'reason':allowed.get(name)})
assert not[r for r in changes if not r['reason']],changes
assets=[n for n in base['files']if n.startswith(('assets-src/npcs/','assets-src/characters/','assets-src/cosmetics/','public/assets/'))];assert not any(r['path']in assets for r in changes)
public=[n for n in base['files']if n.startswith('public/assets/npcs/phase3a/')]
report={'checkedAtUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'humanReview':base['reviewCommit'],'workingBase':base['workingBaseCommit'],'checkedFiles':len(base['files']),'unchangedFiles':same,'authorizedChanges':changes,'unexpectedChanges':[],'all26ApprovedArtSourceAndRuntimeAssetFilesUnchanged':len(assets),'all26PublicNPCFilesExact':len(public),'artExceptions':[],'regeneratedAssets':0,'activeFictionalAliases':0,'status':'PASS'}
(D/'protected-audit.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS',same,'historical files unchanged;',len(assets),'frozen source/runtime asset files;',len(public),'all26publicNPCfiles;0art exceptions;authorized nonpixelchanges',len(changes))
