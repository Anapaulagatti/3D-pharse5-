from pathlib import Path
from PIL import Image
import hashlib,json,subprocess
from collections import Counter
R=Path(__file__).resolve().parents[2];S=R/'assets-src/npcs/phase3a-npc-expansion';D=R/'docs/phase3a-npc-expansion'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
raw={sha(p):str(p)for p in Path('/workspace/generated_images').glob('exec-*.png')};jobs=[]
for p in sorted(S.glob('*/source-provenance.json')):
 for j in json.loads(p.read_text())['jobs']:
  f=R/j['retainedSource'];assert sha(f)==j['SHA256'];j.update(actualImageSize=Image.open(f).size);jobs.append(j)
for f,prompt,refs,kind in[(S/'activity-props-source.png',S/'activity-props-prompt.txt',[R/'assets-src/npcs/phase3a-art-rebuild/seoyeon/master-source.png'],'resident-props'),(S/'modern-props-source.png',S/'modern-props-prompt.txt',[R/'assets-src/npcs/phase3a-art-rebuild/seoyeon/master-source.png'],'modern-props-five-used-one-rejected'),(S/'modern-miram/activity-ball-source.png',S/'modern-miram/activity-ball-prompt.txt',[],'replacement-round-soccer-ball'),(S/'modern-daon/master-source-rejected-traditional-drift.png',S/'modern-daon/rejected-master-prompt.txt',[R/'assets-src/npcs/phase3a-art-rebuild/seoyeon/master-source.png'],'rejected-traditional-drift-master')]:
 jobs.append({'kind':kind,'art_source':'host_image','route':'builtin image_gen.imagegen','retainedSource':str(f.relative_to(R)),'SHA256':sha(f),'actualPrompt':str(prompt.relative_to(R)),'promptSHA256':sha(prompt),'references':[{'path':str(p.relative_to(R)),'SHA256':sha(p)}for p in refs],'actualImageSize':Image.open(f).size,'originalArtifact':raw.get(sha(f)),'model':'not exposed by host','cost':'not exposed; no external paid API invoked'})
assert len(jobs)==38 and len({j['SHA256']for j in jobs})==38
(D/'art-call-ledger.json').write_text(json.dumps({'actualHostCalls':38,'jobs':jobs,'approvedThreeRegenerated':False,'externalPaidAPIsInvoked':False,'AIvideoGeneration':'UNAVAILABLE,NOT EXECUTED','authoringRoute':'approved own-layer native rig workflow'},indent=2)+'\n')
checks=[];statuses=Counter()
for p in sorted((D/'tooling').glob('forge-*/sheet-qc.json')):
 x=json.loads(p.read_text());statuses[x['status']]+=1;checks.append({'report':str(p.relative_to(R)),'status':x['status'],'checks':x['checks'],'notProven':x.get('notProven',[])})
(D/'tooling/all-forge-checks.json').write_text(json.dumps({'directionReports':len(checks),'statusCounts':dict(statuses),'reports':checks,'thresholds':'Unmodified pinned tool; all FAIL/WARN retained','approvedJuniControl':'docs/phase3a-art-rebuild/tooling (immutable previous controls, not falsely claimed as new runs)'},indent=2)+'\n')
artFiles={str(p.relative_to(R)):sha(p)for p in S.rglob('*')if p.is_file()and'__pycache__'not in p.parts}
for p in(R/'public/assets/npcs/phase3a').rglob('*'):
 if p.is_file():artFiles[str(p.relative_to(R))]=sha(p)
(D/'candidate-art-manifest.json').write_text(json.dumps({'status':'REVIEW CANDIDATE,not artistic approval','files':artFiles},indent=2)+'\n');print('Verified38actual source calls;',dict(statuses),'Forge states;',len(artFiles),'candidate hashes')
