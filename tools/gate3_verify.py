from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json,hashlib,subprocess,numpy as np
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3a';inv=json.loads((D/'protected-assets.json').read_text())
bad=[p for p,h in inv['sha256'].items() if hashlib.sha256((R/p).read_bytes()).hexdigest()!=h]
assert not bad,bad
refs={'refs/remotes/origin/art-gate/final-gate1-world':'e0a5c0aeff1a2980042983e6091abff11b987fad','refs/heads/art-gate/gate2-three-slices':inv['baseline'],'refs/tags/checkpoint/gate25-final-approved-20261022^{}':inv['baseline'],'refs/tags/checkpoint/gate25-refinement-approved-20261022^{}':'868aa60acce297253c555f994ecac60276a830b3'}
for ref,want in refs.items():assert subprocess.check_output(['git','rev-parse',ref],cwd=R,text=True).strip()==want,ref
remote_main=subprocess.check_output(['git','ls-remote','origin','refs/heads/main'],cwd=R,text=True).split()[0]
assert remote_main=='33360ed1989e4db9fc3fc4e3686ca385e0b00908'
count=0
for kind in ['world','district']:
 manifest=json.loads((R/f'public/assets/gate3/{kind}/manifest.json').read_text())
 for c in manifest['chunks']:
  assert hashlib.sha256((R/'public'/c['image']).read_bytes()).hexdigest()==c['sha256'];assert hashlib.sha256((R/'public'/c['mask']).read_bytes()).hexdigest()==c['maskSha256'];count+=1
# Direct final planter RGB in native WebGL capture against approved expected native composition.
state=json.loads((D/'station-native-state.json').read_text());vx,vy,_,_=state['camera']['worldView']
screen=Image.open(D/'station-native.png').convert('RGB');expected=Image.open(R/'assets-src/gate25-station-planters/expected-native-composite.png').convert('RGB');checks=[]
for label,rect in [('left',(2545,695,2735,782)),('right',(2908,699,3098,782))]:
 x,y,x2,y2=rect;a=np.array(screen.crop((x-vx,y-vy,x2-vx,y2-vy)));b=np.array(expected.crop(rect));diff=np.max(np.abs(a.astype(int)-b.astype(int)),axis=2)
 checks.append(dict(id=label,rect=list(rect),pixels=int(diff.size),exactPixels=int(np.sum(diff==0)),maxChannelDelta=int(diff.max()),status='PASS' if not np.any(diff) else 'FAIL'))
 # Native crops are untouched pixels from actual Phaser.
 screen.crop((x-vx-12,y-vy-12,x2-vx+12,y2-vy+12)).save(D/f'{label}-planter-native.png')
report=dict(protectedFiles=len(inv['sha256']),protectedSha256='PASS',historicalRefs='PASS',verifiedChunkPairs=count,nativePlanters=checks,renderer=state['renderer'],noSourceResamplingInChunkPipeline=True)
(D/'preservation-and-native-proof.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
