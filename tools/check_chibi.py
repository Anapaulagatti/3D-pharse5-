"""Avatar anatomy/registration/4way animation and immutable town contracts."""
from pathlib import Path
from PIL import Image
import hashlib,json,os
R=Path(__file__).resolve().parents[1];S=R/'assets-src/chibi-v1';O=R/'public-unified/assets/chibi-v1';m=json.loads((S/'manifest.json').read_text());frames=json.loads((S/'avatar.json').read_text())['frames'];assert len(frames)==152
for r in m['files']:assert hashlib.sha256((O/r['path']).read_bytes()).hexdigest()==r['sha256'],r['path']
for r in json.loads((R/'quality-reports/chibi-v1/preserved-foundation.json').read_text())['files']:assert hashlib.sha256((R/r['path']).read_bytes()).hexdigest()==r['sha256'],('World/NPC/lock must remain untouched',r['path'])
for layer in m['layers']:
 atlas=Image.open(O/(layer+'.png')).convert('RGBA');assert len(set(atlas.get_flattened_data()))<=65;assert set(atlas.getchannel('A').get_flattened_data())<={0,255}
 for key,f in frames.items():
  f=f['frame'];x,y=f['x'],f['y'];src=Image.open(S/'frames'/layer/(key+'.png')).convert('RGBA');assert src.size==(40,56);assert atlas.crop((x,y,x+40,y+56)).tobytes()==src.tobytes(),(layer,key)
  g=atlas.crop((x-2,y-2,x+42,y+58)).getchannel('A');assert not any(g.crop(b).getbbox() for b in [(0,0,44,2),(0,58,44,60),(0,0,2,60),(42,0,44,60)]),(layer,key,'gutter')
 for dr in m['directions']:
  if layer in ['body','outfit0','outfit1']:
   walk=[Image.open(S/'frames'/layer/f'walk-{dr}-{i}.png').tobytes() for i in range(8)];run=[Image.open(S/'frames'/layer/f'run-{dr}-{i}.png').tobytes() for i in range(8)];assert sum(a!=b for a,b in zip(walk,run))>=6,(layer,dr,'not distinct run')
   if layer=='body':assert len(set(run))>=6,(dr,'run unique phases')
# Four expression overlays differ in all face-visible views, and back never has eyes.
for dr in ['down','left','right']:
 faces=[Image.open(S/'frames'/('face-'+e)/f'idle-{dr}-0.png').tobytes() for e in ['neutral','happy','focused','surprised']];assert len(set(faces))==4,dr
for e in ['neutral','happy','focused','surprised']:assert not Image.open(S/'frames'/('face-'+e)/'idle-up-0.png').getbbox()
# Asymmetric profile, back and front genuinely have different pixels, silhouettes and hair details.
for layer in ['body','outfit0','outfit1','hair0','hair1','satchel']:
 assert len({Image.open(S/'frames'/layer/f'idle-{dr}-0.png').tobytes() for dr in m['directions']})==4,(layer,'directions')
q=R/os.environ.get('CHIBI_REPORT_DIR','quality-reports/chibi-v1');q.mkdir(parents=True,exist_ok=True)
report={'status':'PASS','frame_size':[40,56],'frames_per_layer':152,'layers':11,'binary_alpha':True,'native_grid':1,'palette_limit':64,'registered_source_atlas_equality':True,'four_moods_three_face_views':True,'true_fourway_run':True,'world_and_original_npc_and_lock_unchanged':True,'limitation':'Technical source contracts do not establish visual approval.'};(q/'asset-qa.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
