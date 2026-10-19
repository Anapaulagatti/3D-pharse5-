"""Scoped original boundary kit; real Forge processing, no provider generation."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,shutil
from PIL import Image
R=Path(__file__).resolve().parents[1];S=R/'assets-src/v6-restructure';C=R/'.cache/v6-restructure';F=Path(os.environ.get('SPRITE_FORGE_ROOT','/workspace/tooling-cache/agent-sprite-forge'));C.mkdir(parents=True,exist_ok=True)
def write(p,j):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(script,*args):
 cmd=[sys.executable,str(script),*map(str,args)];r=subprocess.run(cmd,cwd=R,env=dict(os.environ,FORGE_MAX_PAID_REQUESTS='0'),capture_output=True,text=True)
 p=S/'commands.json';rows=json.loads(p.read_text())if p.exists()else[];rows.append({'command':cmd,'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr});write(p,rows);print(Path(script).name,r.returncode,flush=True)
 if r.returncode:raise RuntimeError(r.stdout+r.stderr)
