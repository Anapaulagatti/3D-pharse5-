"""Read-only native audit. Failures are retained; numerical success is not art approval."""
from pathlib import Path
from PIL import Image
from scipy.ndimage import label
import json,hashlib,sys,numpy as np
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a-npc-expansion';S=R/'assets-src/npcs/phase3a-npc-expansion'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def protect():
 reports=[]
 for file in ['protected-baseline.json','approved-three-manifest.json']:
  b=json.loads((D/file).read_text());files=b.get('files',b.get('frozenFiles'));changes=[p for p,h in files.items()if not(R/p).is_file()or sha(R/p)!=h];reports.append({'manifest':file,'files':len(files),'changed':changes,'status':'FAIL'if changes else'PASS'})
 (D/'protected-audit.json').write_text(json.dumps(reports,indent=2)+'\n');assert not any(q['changed']for q in reports),reports
 return reports

def actor(id):
 p=S/id;atlas=Image.open(p/'candidate-atlas.png').convert('RGBA');meta=json.loads((R/f'public/assets/npcs/phase3a/npc-{id}/atlas.json').read_text());errors=[];clips=[]
 for d in ['front','back','left','right']:
  for kind,count in [('idle',2),('walk',8),('greet',8),('activity',8)]:
   hashes=[];changes=[]
   for i in range(count):
    name=f'{kind}-{d}-{i}';im=Image.open(p/'frames'/f'{name}.png').convert('RGBA');a=np.array(im);hashes.append(hashlib.sha256(im.tobytes()).hexdigest());f=meta['frames'][name]['frame'];bb=im.getbbox();components,n=label(a[:,:,3]>0,np.ones((3,3)));areas=np.bincount(components.ravel())[1:]
    if sum(v>=8 for v in areas)!=1:errors.append([name,'detached-major-component',sorted([int(v)for v in areas if v>=8],reverse=True)])
    if not bb or bb[0]<=0 or bb[1]<=0 or bb[2]>=96 or bb[3]>=112:errors.append([name,'bounds',bb])
    if set(np.unique(a[:,:,3]))-{0,255}:errors.append([name,'nonbinary-alpha'])
    if atlas.crop((f['x'],f['y'],f['x']+96,f['y']+112)).tobytes()!=im.tobytes():errors.append([name,'atlas-mismatch'])
    if kind=='walk':
     ys=np.where((a[:,:,3]>0)&(np.indices((112,96))[0]>=90))[0]
     if len(ys)==0 or ys.max()!=99:errors.append([name,'no-grounded-sole',int(ys.max())if len(ys)else None])
   if len(set(hashes))!=count:errors.append([kind,d,'duplicate-frames',len(set(hashes))])
   clips.append({'clip':f'{kind}-{d}','frames':count,'distinct':len(set(hashes))})
 row={'id':id,'status':'FAIL'if errors else'PASS TECHNICAL ONLY','cells':104,'errors':errors,'clips':clips,'humanArtApproval':'PENDING'};(D/f'{id}-native-qa.json').write_text(json.dumps(row,indent=2)+'\n');print(id,row['status'],len(errors));return row
if __name__=='__main__':
 protect();rows=[actor(id)for id in sys.argv[1:]];sys.exit(1 if any(q['errors']for q in rows)else 0)
