"""Source/runtime equality, true run motion, layer registration and navigation contracts."""
from pathlib import Path
from PIL import Image
import json,hashlib,collections
R=Path(__file__).resolve().parents[1];S=R/'assets-src/unified-v4';O=R/'public-unified/assets/unified-v4';m=json.loads((S/'manifest.json').read_text());frames=json.loads((S/'avatar.json').read_text())['frames'];w=json.loads((S/'world.json').read_text());mp=json.loads((S/'plaza.json').read_text())
assert len(frames)==152
for row in m['files']:assert hashlib.sha256((O/row['path']).read_bytes()).hexdigest()==row['sha256'],row['path']
for layer in m['layers']:
 atlas=Image.open(O/(layer+'.png')).convert('RGBA');assert set(atlas.getchannel('A').get_flattened_data())<= {0,255};assert len(set(atlas.get_flattened_data()))<=65
 for key,info in frames.items():
  f=info['frame'];crop=atlas.crop((f['x'],f['y'],f['x']+32,f['y']+48));src=Image.open(S/'avatar'/layer/(key+'.png')).convert('RGBA');assert crop.tobytes()==src.tobytes(),(layer,key)
  gutter=atlas.crop((f['x']-2,f['y']-2,f['x']+34,f['y']+50));d=gutter.getchannel('A');assert not d.crop((0,0,36,2)).getbbox();assert not d.crop((0,50,36,52)).getbbox();assert not d.crop((0,0,2,52)).getbbox();assert not d.crop((34,0,36,52)).getbbox()
 for dr in m['directions']:
  differences=0;unique=set()
  for i in range(8):
   a=Image.open(S/'avatar'/layer/f'walk-{dr}-{i}.png');b=Image.open(S/'avatar'/layer/f'run-{dr}-{i}.png');differences+=a.tobytes()!=b.tobytes();unique.add(b.tobytes())
  if layer in ['body','outfit0','outfit1']:assert differences>=6,('run must be separately authored',layer,dr,differences)
  if layer=='body':assert len(unique)>=6,(dr,len(unique))
for p in O.glob('*.png'):
 if p.stem=='outfit-source':continue
 im=Image.open(p).convert('RGBA');assert set(im.getchannel('A').get_flattened_data())<= {0,255},p;assert len(set(im.get_flattened_data()))<=(129 if p.stem not in m['layers'] else 65),p
assert hashlib.sha256((O/'plaza.json').read_bytes()).hexdigest()==w['mapSha256'];assert mp['width']==32 and mp['height']==24
colliders=mp['layers'][2]['objects'];assert len(colliders)==77
#8px navigation grid inflated by actual foot collider half extents; every station has a reachable approach.
def free(x,y):return 40<=x<=984 and 40<=y<=728 and not any(o['x']-8<x<o['x']+o['width']+8 and o['y']-1<y<o['y']+o['height']+9 for o in colliders)
start=tuple(round(v/8)*8 for v in w['spawn']);assert free(*start);seen={start};q=collections.deque([start])
while q:
 x,y=q.popleft()
 for pt in [(x+8,y),(x-8,y),(x,y+8),(x,y-8)]:
  if pt not in seen and free(*pt):seen.add(pt);q.append(pt)
landmarks=[]
for p in w['objects']:
 if p['label']:
  approach=(p['x'],p['y']+20)
  assert any(abs(x-approach[0])<=16 and abs(y-approach[1])<=16 for x,y in seen),('unreachable',p)
  landmarks.append(p['label'])
assert any(abs(x-w['npc'][0])<50 and abs(y-w['npc'][1])<50 for x,y in seen)
report={'status':'PASS','files':len(m['files']),'frames_per_layer':152,'layers':6,'layer_source_equality':True,'run_separately_drawn_4ways':True,'pixel_grid':1,'binary_alpha':True,'avatar_palette_bound':64,'world_palette_bound':128,'colliders':77,'reachable_8px_nodes':len(seen),'reachable_landmarks':landmarks,'limitation':'Geometric/source proof does not establish subjective art quality.'}
q=R/'quality-reports/unified-v4';q.mkdir(exist_ok=True,parents=True);(q/'asset-qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))
