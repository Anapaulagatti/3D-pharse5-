"""Validate preserved world asset graph and actor-footprint navigation."""
from pathlib import Path
from PIL import Image
import json,hashlib,collections
R=Path(__file__).resolve().parents[1];S=R/'assets-src/world';O=R/'public/assets/world';m=json.loads((S/'manifest.json').read_text());w=json.loads((S/'world.json').read_text());mp=json.loads((S/'plaza.json').read_text())
for r in m['files']:
 assert hashlib.sha256((S/r['name']).read_bytes()).hexdigest()==r['sha256']
 if r['name']!='world.json':assert (O/r['name']).read_bytes()==(S/r['name']).read_bytes()
for p in O.glob('*.png'):
 im=Image.open(p).convert('RGBA');assert set(im.getchannel('A').get_flattened_data())<={0,255};assert len(set(im.get_flattened_data()))<=129
for p in w['objects']:assert (O/(p['kind']+'.png')).exists(),p
assert hashlib.sha256((O/'plaza.json').read_bytes()).hexdigest()==w['mapSha256']
colliders=mp['layers'][2]['objects'];assert len(colliders)==77
# Same exact16x8-foot clearance model used in previous verified world source QA.
def free(x,y):return 40<=x<=984 and 40<=y<=728 and not any(o['x']-8<x<o['x']+o['width']+8 and o['y']-1<y<o['y']+o['height']+9 for o in colliders)
start=tuple(round(v/8)*8 for v in w['spawn']);assert free(*start);seen={start};q=collections.deque([start])
while q:
 x,y=q.popleft()
 for pt in [(x+8,y),(x-8,y),(x,y+8),(x,y-8)]:
  if pt not in seen and free(*pt):seen.add(pt);q.append(pt)
landmarks=[]
for p in w['objects']:
 if p['label']:
  assert any(abs(x-p['x'])<=16 and abs(y-(p['y']+20))<=16 for x,y in seen),('unreachable',p)
  landmarks.append(p['label'])
# All guest patrol rectangles, checked continuously along edges, not just endpoints.
for gx,gy in [(450,525),(595,528),(426,607),(650,574)]:
 for x in range(gx-10,gx+11):assert free(x,gy) and free(x,gy+12),('guest horizontal route',gx,gy,x)
 for y in range(gy,gy+13):assert free(gx-10,y) and free(gx+10,y),('guest vertical route',gx,gy,y)
r={'status':'PASS','preserved_source_files':len(m['files']),'objects':len(w['objects']),'colliders':len(colliders),'reachable_landmarks':landmarks,'guest_patrol_footprints_clear':True,'world_art_map_unchanged':True}
p=R/'.cache/current-qa';p.mkdir(parents=True,exist_ok=True);(p/'world.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,ensure_ascii=False))
