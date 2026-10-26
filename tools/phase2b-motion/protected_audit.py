from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[2];D=R/'docs/phase2b-motion';report=json.loads((D/'protected-audit.json').read_text());rows=[]
for name,key in [('docs/phase2b/approved-six.json','files'),('docs/phase2b/approved-runtime-code.json','files'),('docs/phase1/protected-world.json','protectedFiles'),('docs/phase1/protected-juni.json','files')]:
 m=json.loads((R/name).read_text());f=m[key];assert f
 bad=[p for p,h in f.items()if hashlib.sha256((R/p).read_bytes()).hexdigest()!=h];snap=m.get('sourceSnapshots',{});sb=[p for p,h in snap.items()if hashlib.sha256((R/p).read_bytes()).hexdigest()!=h];assert not bad and not sb,(name,bad,sb);rows.append({'manifest':name,'verifiedFiles':len(f),'changed':bad,'definitionSnapshots':len(snap),'changedSnapshots':sb})
m=json.loads((R/'docs/phase1/protected-world.json').read_text())['worldDependencies'];assert m;assert all(hashlib.sha256((R/'public'/p).read_bytes()).hexdigest()==h for p,h in m.items());report['approvedManifests']=rows;report['canonicalWorldDependencyHashes']={'verified':len(m),'changed':0};report['status']='PASS';(D/'protected-audit.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS',[(r['manifest'],r['verifiedFiles'])for r in rows],len(m),'world dependencies')
