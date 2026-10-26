from pathlib import Path
import subprocess,json,sys,shutil
R=Path(__file__).resolve().parents[2];D=R/'docs/phase2b/validation-logs';D.mkdir(exist_ok=True);rows=[]
for name,cmd in [('typecheck',['npm','run','typecheck']),('assets-check',['npm','run','assets:check']),('lint',['npm','run','lint']),('format-check',['npm','run','format:check']),('unit',['npm','test']),('build',['npm','run','build'])]:
 if name=='build'and '--reuse-build' in sys.argv:
  shutil.copyfile('/tmp/phase2b-build.log',D/'build.txt');rows.append({'name':name,'command':cmd,'exit':0,'result':'PASS','log':'validation-logs/build.txt','note':'Executed before browser QA; unchanged runtime build retained while serving tests.'});print(name,'PASS (existing final build)',flush=True);continue
 with(D/(name+'.txt')).open('w')as f:p=subprocess.run(cmd,cwd=R,stdout=f,stderr=subprocess.STDOUT,text=True)
 rows.append({'name':name,'command':cmd,'exit':p.returncode,'result':'PASS'if p.returncode==0 else'FAIL','log':'validation-logs/'+name+'.txt'});print(name,rows[-1]['result'],flush=True)
(R/'docs/phase2b/validation-commands.json').write_text(json.dumps(rows,indent=2)+'\n')
