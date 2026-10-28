"""Bind exact prompts/references to retained host artifacts by SHA, without invented model/cost."""
from pathlib import Path
import hashlib,json,sys
R=Path(__file__).resolve().parents[2];S=R/'assets-src/npcs/phase3a-npc-expansion'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
raw={sha(p):str(p)for p in Path('/workspace/generated_images').glob('exec-*.png')}
for id in sys.argv[1:]:
 p=S/id;jobs=[]
 for kind in ['master','turnaround']:
  art=p/f'{kind}-source.png';prompt=p/f'actual-{kind}-prompt.txt';refs=[R/('docs/phase3a-art-rebuild/juni-style-review-6x.png'if id.startswith('modern-')else'assets-src/npcs/phase3a-art-rebuild/seoyeon/master-source.png')]
  if kind=='turnaround':refs.insert(0,p/'master-source.png')
  jobs.append({'kind':kind,'art_source':'host_image','route':'builtin image_gen.imagegen','actualPrompt':str(prompt.relative_to(R)),'promptSHA256':sha(prompt),'retainedSource':str(art.relative_to(R)),'SHA256':sha(art),'originalArtifact':raw.get(sha(art)),'references':[{'path':str(q.relative_to(R)),'SHA256':sha(q)}for q in refs],'model':'not exposed by host','cost':'not exposed by host; no external paid API','selection':'Internal technical selection; final human artistic review pending'})
 (p/'source-provenance.json').write_text(json.dumps({'jobs':jobs,'nativeFinish':'native-finish.json','ownRig':'rig.json','ownPoseKeys':'pose-keys.json'},ensure_ascii=False,indent=2)+'\n')
print('Exact host artifact provenance recorded for',len(sys.argv)-1,'identities')
