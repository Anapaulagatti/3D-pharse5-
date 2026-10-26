from pathlib import Path
import subprocess,os,json,time
R=Path(__file__).resolve().parents[2];D=R/'docs/phase1b';checks=[]
for name,cmd in [('typecheck',['npm','run','typecheck']),('assets',['npm','run','assets:check']),('lint',['npm','run','lint']),('unit',['npm','test']),('build',['npm','run','build']),('e2e',['npm','run','test:e2e'])]:
 env=dict(os.environ,CI='1',PIXEL_PREVIEW_PORT='4325',PIXEL_REPORT_DIR='docs/phase1b');t=time.time()
 with(D/(name+'-final.log')).open('w')as out:p=subprocess.run(cmd,cwd=R,env=env,stdout=out,stderr=subprocess.STDOUT)
 checks.append({'name':name,'command':cmd,'exit':p.returncode,'seconds':round(time.time()-t,2),'log':name+'-final.log','status':'PASS'if p.returncode==0 else'FAIL'});(D/'checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(name,checks[-1]['status'],flush=True)
 if p.returncode:raise SystemExit(p.returncode)
