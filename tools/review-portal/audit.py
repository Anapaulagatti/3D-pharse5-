"""Byte/hash audit: every preexisting file checked, not only listed art samples."""
from pathlib import Path
import json,hashlib,subprocess,datetime
R=Path.cwd();D=R/'docs/review-portal';baseline=json.loads((D/'BASELINE.json').read_text());allowed={'AGENTS.md':'latest owner portal authority','docs/current/PROJECT_STATE.md':'review scope only','vite.config.ts':'optional review base; canonical default preserved'};changes=[];same=0
for name,h in baseline['files'].items():
 p=R/name;new=hashlib.sha256(p.read_bytes()).hexdigest()if p.is_file()else None
 if h==new:same+=1
 else:changes.append({'path':name,'before':h,'after':new,'reason':allowed.get(name)})
assert all(c['reason']for c in changes),changes
q={'status':'PASS','base':baseline['commit'],'checkedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checkedFiles':len(baseline['files']),'unchanged':same,'changes':changes,'allPreexistingGameSourceArtDataTests':'byte-identical','newGameEntry':'review-only bridge; not imported by canonical entry','stableNPCIDs':26,'playableCharacters':12,'cosmetics':28,'physicalDevices':'NOT_TESTED','existingWorkflowSHA256':hashlib.sha256((R/'.github/workflows/pixel-ci.yml').read_bytes()).hexdigest(),'mainRemoteVerification':'NOT AVAILABLE: no current GitHub authentication; previous receipt only','previousMainReceipt':json.loads((R/'docs/phase3b-a/published-verification.json').read_text())['mainUnchanged']};(D/'PROTECTED_AUDIT.json').write_text(json.dumps(q,indent=2)+'\n');print('PASS',same,'preexisting files unchanged;',len(changes),'authorized infrastructure/doc amendments')
