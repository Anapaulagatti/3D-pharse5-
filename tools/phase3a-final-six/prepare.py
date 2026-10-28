from pathlib import Path
import json,subprocess,sys,hashlib
R=Path(__file__).resolve().parents[2];S=R/'assets-src/npcs/phase3a-final-six';F=Path('/workspace/tooling-cache/agent-sprite-forge/skills/generate2dsprite/scripts/master_still.py')
for id in sys.argv[1:]:
 p=S/id;spec=json.loads((R/'assets-src/npcs/phase3a-art-rebuild/seoyeon/master-job/spec.json').read_text());style=R/'assets-src/npcs/phase3a-art-rebuild/seoyeon/master-source.png';spec.update(name=id,subject='Independent speculative historical reconstruction art proposal',identity=(p/'actual-master-prompt.txt').read_text());spec['style_ref']={'path':str(style),'sha256':hashlib.sha256(style.read_bytes()).hexdigest()};(p/'master-spec.json').write_text(json.dumps(spec,indent=2)+'\n')
 for args,log in [(['prompt','--spec',str(p/'master-spec.json'),'--output-dir',str(p/'master-job')],'forge-prompt.log'),(['approve','--still',str(p/'master-source.png'),'--run',str(p/'master-job'),'--prompt-file',str(p/'actual-master-prompt.txt'),'--route','host-image_gen','--output-dir',str(p/'master-prepared')],'forge-prepare.log')]:
  if (p/('master-job'if'prompt'in args else'master-prepared')).exists():continue
  q=subprocess.run([sys.executable,str(F),*args],capture_output=True,text=True);(p/log).write_text(q.stdout+q.stderr);assert q.returncode==0,q.stderr
 print(id,'actual Forge prompt/approve executed; prepared framing not used as native source; not human art approval')
