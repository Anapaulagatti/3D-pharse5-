"""Reuse the frozen illustrated NPC tooling through isolated source/output roots.

No old actor or tool is rewritten. Primary art is host imagegen, not code drawing.
Costumes remain explicitly speculative until independent sources are available.
"""
from pathlib import Path
import importlib.util,json,sys,hashlib,shutil
R=Path(__file__).resolve().parents[2]
S=R/'assets-src/npcs/phase3a-final-six';D=R/'docs/phase3a-final-six'
IDS=['history-seondeok','history-sejong','history-jang','history-saimdang','history-yi','history-yu']
CONFIG={
 'history-seondeok':{'hip':80,'knee':87,'shoe':95,'shoulder':49,'hem':95,'robe':True},
 'history-sejong':{'hip':80,'knee':87,'shoe':94,'shoulder':49,'hem':93,'robe':True},
 'history-jang':{'hip':76,'knee':86,'shoe':94,'shoulder':49,'hem':76},
 'history-saimdang':{'hip':88,'knee':93,'shoe':95,'shoulder':49,'hem':90},
 'history-yi':{'hip':80,'knee':89,'shoe':94,'shoulder':49,'hem':80},
 'history-yu':{'hip':87,'knee':92,'shoe':94,'shoulder':49,'hem':88},
}
def module(name):
 p=R/f'tools/phase3a-npc-expansion/{name}.py'
 spec=importlib.util.spec_from_file_location('history_reuse_'+name,p)
 m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 m.S=S;m.D=D
 return m
def finish(id):
 from PIL import Image
 p=S/id
 n=module('native');n.SPLIT[id]=Image.open(p/'turnaround-source.png').height//2;n.finish(id)
def rig(id):
 m=module('rig');m.CONFIG[id]=CONFIG[id];m.author(id)
 # Long robes leave a short visible ankle; shoe RGB belongs exclusively to
 # its native translated layer, never to a rotated shin a second time.
 from PIL import Image
 import numpy as np
 for path in (S/id/'layers').glob('*/*shin.png'):
  a=np.array(Image.open(path).convert('RGBA'));a[CONFIG[id]['shoe']:]=0
  Image.fromarray(a).save(path)
 if CONFIG[id].get('robe'):
  for view in ['front','back','left','right']:
   folder=S/id/'layers'/view;cfgv=json.loads((S/id/'rig.json').read_text())['views'][view]
   shoe_mask=np.zeros((112,96),dtype=bool)
   for side in ['L','R']:
    path=folder/(side+'shoe.png');a=np.array(Image.open(path).convert('RGBA'))
    if view in ['front','back']:
     if side=='L':a[:,46:]=0
     else:a[:,:51]=0
    Image.fromarray(a).save(path);shoe_mask|=a[:,:,3]>0
    for segment in ['thigh','shin']:
     path=folder/(side+segment+'.png');a=np.array(Image.open(path).convert('RGBA'));cx=cfgv['joints'][side][0][0]
     a[:,:cx-4]=0;a[:,cx+5:]=0;Image.fromarray(a).save(path)
   path=folder/'body.png';a=np.array(Image.open(path).convert('RGBA'))
   if view in ['left','right']:
    own=np.array(Image.open(S/id/'native'/f'{view}.png').convert('RGBA'));a[76:CONFIG[id]['hem']+1]=own[76:CONFIG[id]['hem']+1]
   a[shoe_mask]=0;Image.fromarray(a).save(path)
 cfg=json.loads((S/id/'rig.json').read_text());cfg['robeOwnership']='Whole illustrated robe remains body-owned; narrow under-robe legs, exclusive native shoes, no skirt pixels rotated as wide legs'
 cfg['shoeOwnership']='Shin mask excludes shoe rows, avoiding duplicate rotated shoe pixels under long robes'
 (S/id/'rig.json').write_text(json.dumps(cfg,indent=2)+'\n')
def animate(id):module('animate').build(id,False)
def audit(id):return module('audit').actor(id)
def export(id):
 p=S/id;report=audit(id)
 if report['errors']:raise RuntimeError(report['errors'])
 out=R/f'public/assets/npcs/phase3a/npc-{id}'
 for a,b in [('candidate-atlas.png','atlas.png'),('candidate-preview-native.png','preview-native.png')]:shutil.copyfile(p/a,out/b)
 files=[p/n for n in ['master-source.png','turnaround-source.png','rig.json','native-finish.json']]
 record={'id':'npc-'+id,'art_source':'host_image','tool':'image_gen.imagegen','sources':{str(q.relative_to(R)):hashlib.sha256(q.read_bytes()).hexdigest() for q in files},'nativeCell':[96,112],'footAnchor':[48,100],'nativeCells':104,'sourceOwnedLayers':44,'costumeStatus':'SPECULATIVE ERA-QUALIFIED PROPOSAL; institutional verification blocked','historicalContentVerified':False,'humanArtApproval':'PENDING','qa':report['status']}
 (out/'provenance.json').write_text(json.dumps(record,indent=2)+'\n')
def pack_metadata(id):
 out=R/f'public/assets/npcs/phase3a/npc-{id}';out.mkdir(exist_ok=True)
 m=json.loads((R/'public/assets/npcs/phase3a/npc-seoyeon/atlas.json').read_text());m['meta']['image']='atlas.png'
 (out/'atlas.json').write_text(json.dumps(m,indent=2)+'\n')
if __name__=='__main__':
 action=sys.argv[1]
 for id in sys.argv[2:]:
  assert id in IDS
  if action=='all':
   pack_metadata(id);finish(id);rig(id);animate(id);export(id)
  else:globals()[action](id)
