"""Execute pinned third-party diagnostics unchanged; preserve every WARN/FAIL verbatim."""
from pathlib import Path
from PIL import Image
import json,subprocess
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a-art-rebuild/tooling';S=R/'assets-src/npcs/phase3a-art-rebuild';rows=[]
for id in ['seoyeon','minseo','harin']:
 for d in ['front','back','left','right']:
  out=D/f'forge-{id}-{d}';args=['python3','/workspace/tooling-cache/agent-sprite-forge/skills/generate2dsprite/scripts/sheet_qc.py','frames','--frames',*[str(S/id/'frames'/f'walk-{d}-{i}.png')for i in range(8)],'--cycle','walk','--key','none','--output-dir',str(out)]
  if d in ['left','right']:args+=['--facing',d]
  q=subprocess.run(args,capture_output=True,text=True);(D/f'forge-{id}-{d}.log').write_text(q.stdout+q.stderr);rows.append({'tool':'SpriteForge sheet_qc frames','id':id,'direction':d,'command':args,'exitCode':q.returncode,'report':str((out/'sheet-qc.json').relative_to(R)),'log':str((D/f'forge-{id}-{d}.log').relative_to(R))});print(id,d,'Forge',q.returncode,flush=True)
 board=Image.new('RGBA',(768,448))
 for row,d in enumerate(['front','back','left','right']):
  for i in range(8):board.alpha_composite(Image.open(S/id/'frames'/f'walk-{d}-{i}.png'),(i*96,row*112))
 sheet=D/f'{id}-rectangular-walk-native.png';board.save(sheet)
 args=['python3','/workspace/tooling-cache/character-animation-creator-skill/scripts/validate_sheet.py','--input',str(sheet),'--rows','4','--columns','8','--cell','96','--row-names','front,back,left,right','--json-out',str(D/f'creator-{id}-square-contract.json')];q=subprocess.run(args,capture_output=True,text=True);(D/f'creator-{id}-square-contract.log').write_text(q.stdout+q.stderr);rows.append({'tool':'CharacterAnimationCreator validate_sheet','id':id,'command':args,'exitCode':q.returncode,'scope':'Unmodified square-cell validator does not represent requested96x112;retain actual diagnostic,rectangular production audit is separate','log':str((D/f'creator-{id}-square-contract.log').relative_to(R))})
 args=['python3','/workspace/tooling-cache/character-animation-creator-skill/scripts/audit_sprite_motion.py','--input',str(sheet),'--rows','4','--columns','8','--cell','96','--row-names','front,back,left,right','--json-out',str(D/f'creator-{id}-motion-diagnostic.json')];q=subprocess.run(args,capture_output=True,text=True);(D/f'creator-{id}-motion-diagnostic.log').write_text(q.stdout+q.stderr);rows.append({'tool':'CharacterAnimationCreator motion diagnostic','id':id,'command':args,'exitCode':q.returncode,'scope':'Square-cell diagnostic only;not rectangular art acceptance','log':str((D/f'creator-{id}-motion-diagnostic.log').relative_to(R))})
(D/'execution-manifest.json').write_text(json.dumps({'executions':rows,'originalToolVersions':'Exact requested commits;tool source/thresholds unchanged','nativeContract':[96,112],'artisticApproval':'PENDING','videoGeneration':'UNAVAILABLE,NOT EXECUTED;no paidAPI;approved authored own-layer workflow used'},indent=2)+'\n')
