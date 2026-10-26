from pathlib import Path
import json,hashlib,subprocess,io,math
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[2];D=R/'docs/phase1b-frontback-juni';BASE='4dfa807f26a19d8602143421a9f6886cc1c08e28'
def digest(b):return hashlib.sha256(b).hexdigest()
protected=[]
for name in ['protected-world','protected-juni']:
 raw=json.loads((R/f'docs/phase1/{name}.json').read_text());m=raw.get('files',raw.get('protectedFiles',{}));assert m;bad=[p for p,h in m.items()if digest((R/p).read_bytes())!=h];assert not bad,bad;protected.append({'manifest':name,'files':len(m),'changed':bad})
# All tracked files under protected identity sources and runtime/UI/controller remain identical.
paths=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'assets-src/characters/phase1b','src','public/assets/juni'],cwd=R,text=True).splitlines();bad=[]
for p in paths:
 old=subprocess.check_output(['git','show',f'{BASE}:{p}'],cwd=R)
 if (R/p).read_bytes()!=old:bad.append(p)
assert not bad,bad
frames=[]
for id in ['haneul','bomi','minjun']:
 p=f'public/assets/characters/{id}/atlas.png';old=Image.open(io.BytesIO(subprocess.check_output(['git','show',f'{BASE}:{p}'],cwd=R))).convert('RGBA');new=Image.open(R/p).convert('RGBA');m=json.loads((R/f'public/assets/characters/{id}/atlas.json').read_text())['frames'];changed=[];same=[]
 for n,r in m.items():
  f=r['frame'];box=(f['x'],f['y'],f['x']+f['w'],f['y']+f['h']);a,b=old.crop(box),new.crop(box)
  (same if a.tobytes()==b.tobytes()else changed).append(n)
 assert len(changed)==32 and all(n.startswith(('walk-front-','walk-back-','run-front-','run-back-'))for n in changed)
 for path in ['atlas.json','preview-native.png']:
  p=f'public/assets/characters/{id}/{path}';assert (R/p).read_bytes()==subprocess.check_output(['git','show',f'{BASE}:{p}'],cwd=R)
 for name in changed:
  im=Image.open(R/f'assets-src/characters/phase1b-frontback-juni/{id}/frames/{name}.png').convert('RGBA');box=im.getbbox();assert box and box[0]>0 and box[1]>0 and box[2]<96 and box[3]<112;assert set(np.unique(np.array(im)[:,:,3])) <= {0,255}
 frames.append({'id':id,'changed':changed,'unchanged':same,'other80Frames':'PASS','atlasLayoutAndPreview':'unchanged'})
q=json.loads((D/'gameplay-qa.json').read_text());reads=[]
for row in q['rows']:
 a=row['audit'];id=row['id'];state=a['state'];asset='assets/juni/juni'if id=='juni'else f'assets/characters/{id}/atlas';m=json.loads((R/'public'/f'{asset}.json').read_text())['frames'];im=Image.open(R/'public'/f'{asset}.png').convert('RGBA');f=m[state['frame']]['frame'];sprite=np.array(im.crop((f['x'],f['y'],f['x']+96,f['y']+112)));sx,sy=a['camera']['scroll'];x=math.floor(state['x']+.5)-48-sx;y=math.floor(state['y']+.5)-100-sy;shot=Image.open(D/f'{id}-{row["clip"]}-phaser-native.png').convert('RGB');crop=shot.crop((x,y,x+96,y+112));crop.save(D/f'{id}-{row["clip"]}-gameplay-crop-native.png');actual=np.array(crop);mask=sprite[:,:,3]==255;diff=int((mask&np.any(actual!=sprite[:,:,:3],2)).sum());assert diff==0,(id,row['clip'],diff);assert a['camera']['zoom']==1 and all(float(v).is_integer()for v in [sx,sy]);assert all(l['scaleMode']==1 for l in a['layers']);reads.append({'id':id,'clip':row['clip'],'actualFrame':state['frame'],'opaqueNativePixels':int(mask.sum()),'readbackPixelMismatch':diff,'observedFrameCount':len(row['observedFrames'])})
(D/'scope-and-pixel-qa.json').write_text(json.dumps({'baseline':BASE,'protected':protected,'identityAndRuntimeFilesUnchanged':len(paths),'frames':frames,'nativePhaserReadbacks':reads,'sourceClipMapping':'All four clips use the explicit same-index Juni landmark table, eight real distinct poses each. Human locomotion acceptance PENDING.','physicalDevices':'NOT TESTED'},indent=2)+'\n');print('PASS',len(paths),'source/runtime files; protected',protected,'native readbacks',len(reads))
