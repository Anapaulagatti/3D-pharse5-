"""Explicit host-illustration provenance and pinned Sprite Forge master preparation.
Never calls an external paid API; never writes approved pilot source directories.
"""
from pathlib import Path
import json,hashlib,subprocess,sys
R=Path(__file__).resolve().parents[2];S=R/'assets-src/npcs/phase3a-npc-expansion';D=R/'docs/phase3a-npc-expansion';FORGE=Path('/workspace/tooling-cache/agent-sprite-forge/skills/generate2dsprite/scripts/master_still.py')
IDS=list(json.loads((S/'resident-art-directions.json').read_text()))
RAW={'daehyun':'exec-20aa8325-ea09-4005-88da-2dd0eaa2f513.png','jiho':'exec-27f477ca-8f05-48a9-b207-4f8b0fe7753a.png','eunji':'exec-87ffac35-6d93-4aff-bbc2-32109cc48ace.png','seojun':'exec-e2e8438f-4370-41f9-b18b-80da8dcb4da2.png'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def stage(id):
 p=S/id;identity=(p/'identity.txt').read_text().strip()
 spec=json.loads((R/'assets-src/npcs/phase3a-art-rebuild/seoyeon/master-job/spec.json').read_text());spec.update(name=id,subject='Independently illustrated Korean NPC',identity=identity);spec['style_ref']={'path':'../../phase3a-art-rebuild/seoyeon/master-source.png','sha256':sha(R/'assets-src/npcs/phase3a-art-rebuild/seoyeon/master-source.png')};(p/'master-spec.json').write_text(json.dumps(spec,indent=2)+'\n')
 if not(p/'master-job').exists():subprocess.run([sys.executable,str(FORGE),'prompt','--spec',str(p/'master-spec.json'),'--output-dir',str(p/'master-job')],check=True,capture_output=True)
 if(p/'master-source.png').exists():
  if not(p/'master-prepared').exists():
   proc=subprocess.run([sys.executable,str(FORGE),'approve','--still',str(p/'master-source.png'),'--run',str(p/'master-job'),'--prompt-file',str(p/'actual-master-prompt.txt'),'--route','host-image_gen','--output-dir',str(p/'master-prepared')],text=True,capture_output=True);(p/'master-prepare.log').write_text(proc.stdout+proc.stderr);assert proc.returncode==0,proc.stderr
  refs=[R/'assets-src/npcs/phase3a-art-rebuild/seoyeon/master-source.png'];record={'route':'builtin image_gen.imagegen','art_source':'host_image','model':'not exposed by host tool','cost':'not exposed; no external API invoked','promptSHA256':sha(p/'actual-master-prompt.txt'),'sourceSHA256':sha(p/'master-source.png'),'originalArtifact':str(Path('/workspace/generated_images')/RAW[id])if id in RAW else None,'references':[{'path':str(q.relative_to(R)),'sha256':sha(q)}for q in refs],'masterSelection':'internal technical selection, not human artistic approval','nativePixels':'not authored yet'};(p/'source-provenance.json').write_text(json.dumps(record,indent=2)+'\n')
  prompt=f'''Create FOUR independently drawn orthographic animator rest views of EXACT {id} in FIRST attached image. SECOND approved Seoyeon is finish/proportions reference ONLY, never identity. Strict 2x2 layout: TOP LEFT straight FRONT facing viewer; TOP RIGHT straight BACK no face; BOTTOM LEFT true LEFT PROFILE facing screenLEFT; BOTTOM RIGHT true RIGHT PROFILE facing screenRIGHT. No text. Identity: {identity}\nPreserve exact face, hair silhouette, costume layers and anatomical accessory ownership from first source. Every view same body height and shoe baseline in its quadrant. Full body generous MAGENTA margins, no overlap. Neutral relaxed A pose, arms20degrees from body, bare hands separate from clothes, feet separate. Both profile legs/feet visible; near arm slightly forward, far arm slightly back. No walk poses, no3/4views, no mirrored accessory ownership. Sophisticated hand-illustrated pixel-game source finish with readable fabric, eyes, hair and material highlights; about three heads tall, upper-left light. Flat pure #FF00FF background, NO ground/shadow/held prop/logo/grid. This is large source artwork for later native finish, NOT an animation sheet or claimed logical pixel grid.\n'''
  (p/'actual-turnaround-prompt.txt').write_text(prompt)
for id in sys.argv[1:]or IDS:stage(id)
print('Prepared jobs/source provenance; protected artwork untouched.')
