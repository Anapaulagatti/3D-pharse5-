from pathlib import Path
import subprocess,json
R=Path(__file__).resolve().parents[2];F=Path('/workspace/tooling-cache/agent-sprite-forge/skills');D=R/'docs/phase2b/forge-qa';D.mkdir(exist_ok=True);commands=[]
for id in __import__('sys').argv[1:]:
 for action in ['walk','run']:
  for direction in ['front','back','left','right']:
   name=f'{id}-{action}-{direction}';files=[str(R/f'assets-src/characters/phase2b/{id}/frames/{action}-{direction}-{i}.png')for i in range(8)];out=D/name
   cmd=['python',str(F/'codeart2d/scripts/pixel_qa.py'),'--input',*files,'--anchor','48,100','--onion','--review',str(out)+'.png','--scales','1,2','--bg','dark,light','--report',str(out)+'.json']
   if Path(str(out)+'.json').exists():continue
   p=subprocess.run(cmd,cwd=R,text=True,capture_output=True);commands.append({'command':cmd,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
   # Side-view motion diagnostics only: front/back are not side-view leading-leg tests.
   if direction in ['left','right']:
    cmd=['python',str(F/'generate2dsprite/scripts/sheet_qc.py'),'frames','--frames',*files,'--cycle',action,'--facing',direction,'--output-dir',str(out)+'-motion'];q=subprocess.run(cmd,cwd=R,text=True,capture_output=True);commands.append({'command':cmd,'exit':q.returncode,'stdout':q.stdout,'stderr':q.stderr})
(D/('commands-'+'-'.join(__import__('sys').argv[1:])+'.json')).write_text(json.dumps(commands,indent=2)+'\n');print('Commands:',len(commands),'nonzero:',sum(q['exit']!=0 for q in commands))
