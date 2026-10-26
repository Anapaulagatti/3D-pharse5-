"""Execute only pre-inventoried disposable Vite directories; no source cleanup."""
from pathlib import Path
import json,shutil
import sys
R=Path(__file__).resolve().parents[1];D=R/'docs/phase1';inv=json.loads((D/'cleanup-inventory.json').read_text());removed=[]
if (D/'cleanup-executed.json').exists():
 print('Cleanup already audited; no second deletion or archive overwrite.');sys.exit(0)
for q in inv['disposableBuilds']:
 p=R/q['path'];assert q['path']in ['dist','dist-gate1','dist-gate2','dist-gate3','dist-world-gate1'];assert p.parent==R and not p.is_symlink()
 if p.exists():shutil.rmtree(p);removed.append(q)
# Preserve exact earlier instructions with provenance before consolidating roots.
archive=R/'docs/history/pre-phase1';hashes={}
for name in ['AGENTS.md','README.md','STUDIO_TASKS.md','STUDIO_PROGRESS.md','STUDIO_DECISIONS.md','STUDIO_ASSETS.md','docs/ART_SKILL_REGISTRY.md']:
 p=R/name;out=archive/('AGENTS.historical.md' if name=='AGENTS.md' else name.replace('/','--'));out.write_bytes(p.read_bytes());hashes[name]=str(out.relative_to(R))
(D/'cleanup-executed.json').write_text(json.dumps({'baseline':inv['baseline'],'removed':removed,'archivedInstructionCopies':hashes,'categoryCSourceAndArt':'KEPT: dependency/reference chains cannot be safely discarded','categoryD':'KEPT: uncertain caches/tooling never removed','historyRecovery':'checkpoint/world-art-approved-phase1-20261026'},indent=2)+'\n')
print('Removed disposable build files:',sum(q['files']for q in removed),'bytes:',sum(q['bytes']for q in removed))
