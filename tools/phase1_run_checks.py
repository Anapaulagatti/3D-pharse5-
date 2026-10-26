from pathlib import Path
import subprocess,json,time,os
R=Path(__file__).resolve().parents[1];D=R/'docs/phase1';rows=[]
for command in [['npm','run','typecheck'],['npm','run','assets:check'],['npm','run','lint'],['npm','test'],['npm','run','build'],['npm','run','test:e2e']]:
 print('RUN', ' '.join(command),flush=True);start=time.time();env=dict(os.environ)
 if command[-1]=="test:e2e":env.update(PIXEL_PREVIEW_PORT="4322",CI="1")
 p=subprocess.run(command,cwd=R,text=True,capture_output=True,env=env);row={'command':command,'exit':p.returncode,'elapsedSeconds':round(time.time()-start,2),'stdout':p.stdout,'stderr':p.stderr};rows.append(row);(D/'checks.json').write_text(json.dumps(rows,indent=2)+'\n');print('PASS'if p.returncode==0 else'FAIL',row['elapsedSeconds'],flush=True)
 if p.returncode:print(p.stdout[-5000:],p.stderr[-1500:],flush=True)
print('Checks complete; failures',sum(q['exit']!=0 for q in rows),flush=True)
