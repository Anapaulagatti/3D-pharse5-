from pathlib import Path
from PIL import Image
import json,hashlib,subprocess,io,re
import numpy as np
R=Path(__file__).resolve().parents[2];D=R/'docs/phase2b-motion/walk-front';before=json.loads((D/'before.json').read_text());ids=before['targets'];bad=[];changed=[];cells=[]
def permitted(path):
 for id in ids:
  p='phase2a'if id in ['ara','doyun']else'phase2b'
  if path==f'public/assets/characters/{id}/atlas.png'or re.fullmatch(rf'assets-src/characters/{p}/{id}/frames/walk-front-[0-7]\.png',path):return True
 return False
for p,h in before['files'].items():
 now=hashlib.sha256((R/p).read_bytes()).hexdigest()
 if now!=h:
  changed.append({'file':p,'beforeSHA256':h,'afterSHA256':now})
  if not permitted(p):bad.append(p)
assert not bad,bad;assert len(changed)==72,len(changed)
for id in ids:
 stem=f'public/assets/characters/{id}/atlas';m=json.loads((R/(stem+'.json')).read_text())['frames'];old=Image.open(io.BytesIO(subprocess.check_output(['git','show',before['commit']+':'+stem+'.png']))).convert('RGBA');new=Image.open(R/(stem+'.png')).convert('RGBA');delta=[];same=[];heads=[]
 for key,r in m.items():
  f=r['frame'];box=(f['x'],f['y'],f['x']+96,f['y']+112);a=np.array(old.crop(box));b=np.array(new.crop(box))
  if np.array_equal(a,b):same.append(key)
  else:
   assert re.fullmatch(r'walk-front-[0-7]',key),key;assert np.array_equal(a[:47],b[:47]),(id,key,'head');assert set(np.unique(b[:,:,3]))<={0,255}
   delta.append({'frame':key,'pixels':int(np.any(a!=b,2).sum()),'beforeRGBA_SHA256':hashlib.sha256(a.tobytes()).hexdigest(),'afterRGBA_SHA256':hashlib.sha256(b.tobytes()).hexdigest()})
 assert len(delta)==8 and len(same)==104,(id,len(delta),len(same));assert all(f'walk-right-{i}'in same for i in range(8));cells.append({'id':id,'changed':delta,'unchanged':same,'headHairFirst47Rows':'EXACT','walkRight':'EXACT HUMAN-APPROVED','other104Cells':'EXACT'})
q={'beforeCommit':before['commit'],'baseline':'checkpoint/phase2b-motion-corrected-review-20261027','filesChecked':len(before['files']),'modifiedFiles':changed,'unexpected':bad,'characters':cells,'timingClipJSONAtlasJSONEngineUIWorldCosmetics':'UNCHANGED','juniHaneulBomiMinjun':'UNCHANGED','araDoyunAuthorization':'Latest human explicitly names both active identities; exception applies only their8 default walk-front cells. Original Phase2A manifests stay immutable.','humanWalkFrontApproval':'PENDING','walkRightApproval':'APPROVED AND UNCHANGED'};tmp=D/('audit-'+str(__import__('os').getpid())+'.tmp');tmp.write_text(json.dumps(q,indent=2)+'\n');tmp.replace(D/'audit.json');print('PASS72files/64 walk-front cells;832other cells exact incl64right poses; head/hair exact')
