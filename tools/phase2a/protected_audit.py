from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[2]
rows=[]
for name,key in [('docs/phase2a/approved-four-characters.json','files'),('docs/phase1/protected-world.json','protectedFiles'),('docs/phase1/protected-juni.json','files')]:
    m=json.loads((R/name).read_text()); files=m[key];bad=[]
    for p,h in files.items():
        if hashlib.sha256((R/p).read_bytes()).hexdigest()!=h:bad.append(p)
    snapshots=m.get('definitionSnapshots',{}); snapshot_bad=[p for p,h in snapshots.items()if hashlib.sha256((R/p).read_bytes()).hexdigest()!=h]
    rows.append({'manifest':name,'verifiedFiles':len(files),'changed':bad,'definitionSnapshots':len(snapshots),'changedSnapshots':snapshot_bad})
    assert not bad and not snapshot_bad,(bad,snapshot_bad)
(R/'docs/phase2a/protected-audit.json').write_text(json.dumps({'status':'PASS','checks':rows,'note':'Character semantic registrations and RegistryMotion.step also asserted by unit tests; new metadata/integration outside these immutable file lists is reviewed separately.'},indent=2)+'\n')
print('PASS protected approved4/world/Juni and frozen definition snapshots')
