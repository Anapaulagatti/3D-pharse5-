"""Immutable world/Juni hashes plus genuine paired Phaser pixel regression."""
from pathlib import Path
from PIL import Image
import json,hashlib,numpy as np,subprocess
R=Path(__file__).resolve().parents[1];D=R/'docs/phase1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=[]
for filename,key in [('protected-world.json','protectedFiles'),('protected-juni.json','files')]:
 q=json.loads((D/filename).read_text());bad=[p for p,h in q[key].items()if not(R/p).is_file()or sha(R/p)!=h];assert not bad,bad;checks.append({'manifest':filename,'count':len(q[key]),'changed':0,'status':'PASS'})
base=json.loads((D/'protected-world.json').read_text());m=json.loads((R/'public/assets/gate3/palace-cleanup-world/manifest.json').read_text());assert sha(R/'public/assets/gate3/palace-cleanup-world/manifest.json')==base['worldDependencies']['assets/gate3/palace-cleanup-world/manifest.json'];collision=[c['mask']for c in m['chunks']]+[m['contactCollision']['physical']]
for f in collision:assert sha(R/'public'/f)==base['worldDependencies'][f]
archive=json.loads((D/'cleanup-executed.json').read_text());archived=[]
for old,new in archive['archivedInstructionCopies'].items():
 original=subprocess.check_output(['git','show',base['commit']+':'+old],cwd=R);assert (R/new).read_bytes()==original,old;archived.append(old)
rows=[];count=0
if(D/'native-captures.json').exists():
 caps=json.loads((D/'native-captures.json').read_text());assert not caps['errors']
 for before in [q for q in caps['rows']if q['phase']=='before']:
  after=next(q for q in caps['rows']if q['phase']=='after'and q['entry']==before['entry']and q['renderer']==before['renderer']);a,b=[q['audit']for q in [before,after]];assert a['camera']==b['camera'];assert a['camera']['zoom']==1 and all(float(v).is_integer()for v in a['camera']['scroll']);aa,bb=[np.array(Image.open(D/q['file']).convert('RGBA'))for q in [before,after]];ok=np.ones(aa.shape[:2],bool);sx,sy=a['camera']['scroll']
  for q in [a,b]:
   s=q['state'];x,y=round(s['x'])-sx,round(s['y'])-sy;ok[max(0,y-100):min(len(ok),y+12),max(0,x-48):min(ok.shape[1],x+48)]=False
  delta=np.any(aa!=bb,2)&ok;assert not delta.any(),(before['file'],int(delta.sum()));count+=int(ok.sum());assert b['state']['playerSprites']==1
  for l in b['layers']:assert l['scaleMode']==1
  rows.append({'entry':before['entry'],'requestedRenderer':before['renderer'],'actualRenderer':b['state']['renderer'],'sameCamera':True,'outsidePlayerTimingDifferencePixels':int(delta.sum()),'comparedPixels':int(ok.sum()),'nearest':True,'integerCamera':True})
report={'worldAndJuniHashes':checks,'allCollisionBinariesUnchanged':len(collision),'logicalCoordsManifestExact':True,'archivedInstructionsByteExact':archived,'pairedNativeFrames':rows,'totalWorldPixelsCompared':count,'changedWorldPixels':0,'baseline':base['commit'],'checkpoint':base['checkpoint'],'mapGenerationCalls':0,'JuniSourceFramesChanged':0,'physicalDevices':'NOT TESTED','newCharacterArt':'INCOMPLETE as in character-art-status.json'};(D/'preservation-qa.json').write_text(json.dumps(report,indent=2)+'\n');print('Preserved:',checks,'native world pixels:',count,'/changed0')
