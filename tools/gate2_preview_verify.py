from pathlib import Path
import subprocess,json,os
R=Path(__file__).resolve().parents[1];F=Path('/workspace/tooling-cache/agent-sprite-forge/skills/generate2dmap/scripts/build_scene_preview.py');rows=[]
for id in ['a','b','c','transition','station']:
 cmd=['python3',str(F),'--bundle',f'assets-src/gate2/maps/{id}/hashed-bundle.json','--output-dir',f'.cache/gate2/forge-preview/{id}','--verify','--verify-timeout','180']
 p=subprocess.run(cmd,cwd=R,env={**os.environ,'NODE_PATH':str(R/'node_modules')},capture_output=True,text=True);rows.append(dict(scene=id,command=cmd,exit=p.returncode,stdout=p.stdout,stderr=p.stderr));(R/'docs/gate2/scene-preview-commands.json').write_text(json.dumps(rows,indent=2)+'\n');print(id,p.returncode,p.stdout,p.stderr,flush=True)
