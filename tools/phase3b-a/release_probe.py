from pathlib import Path
import subprocess,json,tempfile
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3b-a';out=Path(tempfile.mkdtemp(prefix='phase3ba-public-probe-',dir='/tmp'));rows=[]
for name,cmd,want in [('private-preflight',['node','tools/rights-gate.mjs'],0),('public-preflight',['node','tools/rights-gate.mjs','--public'],1),('public-vite',['node','node_modules/vite/bin/vite.js','build','--mode','public','--outDir',str(out)],1)]:
 q=subprocess.run(cmd,cwd=R,capture_output=True,text=True);(D/(name+'.log')).write_text(q.stdout+q.stderr);assert q.returncode==want,(name,q.stdout,q.stderr)
 if want:assert 'public build BLOCKED' in q.stdout+q.stderr
 rows.append({'command':cmd,'exitCode':q.returncode,'expected':want,'status':'PASS expected release behavior'})
files=[str(p.relative_to(out))for p in out.rglob('*')if p.is_file()];assert not files,files
(D/'RELEASE_GATE_PROOF.json').write_text(json.dumps({'status':'PASS','privateAllowed':True,'publicBlocked':True,'publicFilesEmitted':files,'rows':rows,'publicProfileSource':'Vite mode/build environment only; query/localStorage cannot modify permission','commercialClearance':False},indent=2)+'\n');print('PASS private permitted; public preflight and direct Vite blocked before emitting any assets')
