from pathlib import Path
import json,hashlib,re,subprocess,io
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[2];D=R/'docs/phase2b-motion';m=json.loads((D/'before-manifest.json').read_text());ids=m['allowedMotionCharacters'];changed=[];bad=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def allowed(p):
 return any(p==f'public/assets/characters/{id}/atlas.png'or re.fullmatch(rf'assets-src/characters/phase2b/{id}/frames/(walk|run|start|stop)-(front|back|right)-\d+\.png',p)for id in ids)
for p,h in m['files'].items():
 if sha(R/p)!=h:
  changed.append(p)
  if not allowed(p):bad.append(p)
assert not bad,bad
cells=[]
for id in ids:
 stem=f'public/assets/characters/{id}/atlas';a=Image.open(io.BytesIO(subprocess.check_output(['git','show',m['commit']+':'+stem+'.png']))).convert('RGBA');b=Image.open(R/(stem+'.png')).convert('RGBA');meta=json.loads((R/(stem+'.json')).read_text())['frames'];deltas=[];same=[]
 for name,f in meta.items():
  r=f['frame'];box=(r['x'],r['y'],r['x']+96,r['y']+112);old=np.array(a.crop(box));new=np.array(b.crop(box));delta=int(np.any(old!=new,2).sum())
  if delta:
   assert re.fullmatch(r'(walk|run|start|stop)-(front|back|right)-\d+',name),name
   # The accepted head/hair raster is not redesigned even in repaired poses.
   if name.startswith(('walk-','run-')):assert np.array_equal(old[:45],new[:45]),(id,name,'head changed')
   deltas.append({'frame':name,'changedPixels':delta,'beforeSHA256':hashlib.sha256(old.tobytes()).hexdigest(),'afterSHA256':hashlib.sha256(new.tobytes()).hexdigest()})
  else:same.append(name)
 assert len(deltas)==66,(id,len(deltas));assert len(same)==46
 cells.append({'id':id,'changedCells':deltas,'unchangedCells':same,'unchangedCount':len(same),'leftAllIdleEmotesAndDesignSources':'EXACT','headHairPixelsInAllRepairedGaits':'EXACT'})
report={'beforeCommit':m['commit'],'baselineTrackedAssetsAndRuntimeFiles':len(m['files']),'modifiedFiles':changed,'afterFileSHA256':{p:sha(R/p)for p in changed},'outsideScopeChanges':bad,'unchangedFiles':len(m['files'])-len(changed),'atlasCells':cells,'atlasJSONClipsAndRuntime':'UNCHANGED','sourceDesignsAllApprovedCharactersWorldUIProgressCameraCollision':'UNCHANGED'};(D/'frame-change-manifest.json').write_text(json.dumps(report,indent=2)+'\n');print('Scope PASS:',len(changed),'motion files;396cells changed,276cells exact;0outside scope')
