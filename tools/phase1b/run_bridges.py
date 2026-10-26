from pathlib import Path
import subprocess,os,json
R=Path(__file__).resolve().parents[2];D=R/'docs/phase1b';rows=[];env=dict(os.environ,PLAYWRIGHT_BROWSERS_PATH='/tmp/phase1b-playwright')
for id in ['juni','haneul','bomi','minjun']:
 with (D/f'bridge-{id}-final.log').open('w')as out:
  p=subprocess.run(['node','tools/phase1b/bridges.mjs',id],cwd=R,env=env,stdout=out,stderr=subprocess.STDOUT)
  q=subprocess.run(['python','tools/phase1b/bridge_audit.py',id],cwd=R,stdout=out,stderr=subprocess.STDOUT)if p.returncode==0 else None
 rows.append({'id':id,'gameplayExit':p.returncode,'contactAuditExit':q.returncode if q else None});(D/'bridges-summary.json').write_text(json.dumps(rows,indent=2)+'\n');print(id,rows[-1],flush=True)
