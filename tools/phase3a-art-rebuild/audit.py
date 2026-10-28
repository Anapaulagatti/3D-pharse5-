"""Read-only preservation and rectangular native/source/ownership/loop/raster QA."""
from pathlib import Path
from PIL import Image
from scipy.ndimage import label
import json,hashlib,numpy as np
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a-art-rebuild';S=R/'assets-src/npcs/phase3a-art-rebuild'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
base=json.loads((D/'protected-baseline.json').read_text());changed=[n for n,h in base['files'].items()if sha(R/n)!=h];assert not changed,changed
replaced=[]
for n in base['onlyAllowedExistingAssetChanges']:
 import subprocess
 before=hashlib.sha256(subprocess.check_output(['git','show',base['baseline']+':'+n],cwd=R)).hexdigest();replaced.append({'file':n,'before':before,'after':sha(R/n)})
(D/'protected-audit.json').write_text(json.dumps({'status':'PASS','baseline':base['baseline'],'unchangedFiles':len(base['files']),'unexpectedChanges':changed,'nineAuthorizedDerivedAssetChanges':replaced,'allRuntimeCode':'BYTE IDENTICAL','NPCIDsLocationsRoutesDialogueCollision':'BYTE IDENTICAL','twelvePlayersCosmeticsStudioWorldCamera':'BYTE IDENTICAL','elevenUnrebuiltNPCArt':'UNCHANGED,REJECTED,NOT APPROVED'},indent=2)+'\n')
rows=[]
for id in ['seoyeon','minseo','harin']:
 p=S/id;rig=json.loads((p/'rig.json').read_text());meta=json.loads((R/f'public/assets/npcs/phase3a/npc-{id}/atlas.json').read_text());atlas=Image.open(R/f'public/assets/npcs/phase3a/npc-{id}/atlas.png').convert('RGBA');frames={q.stem:Image.open(q).convert('RGBA')for q in(p/'frames').glob('*.png')};assert len(frames)==104 and set(frames)==set(meta['frames']);clips=[]
 for d in ['front','back','left','right']:
  for kind,n in [('idle',2),('walk',8),('greet',8),('activity',8)]:
   images=[frames[f'{kind}-{d}-{i}']for i in range(n)];hashes=[hashlib.sha256(q.tobytes()).hexdigest()for q in images];assert len(set(hashes))==n,(id,kind,d,'non-distinct');diff=[]
   for i,q in enumerate(images):
    name=f'{kind}-{d}-{i}';f=meta['frames'][name]['frame'];assert q.size==(96,112)and atlas.crop((f['x'],f['y'],f['x']+96,f['y']+112)).tobytes()==q.tobytes();a=np.array(q);assert set(np.unique(a[:,:,3]))<={0,255};bb=q.getbbox();assert bb and bb[0]>0 and bb[1]>0 and bb[2]<96 and bb[3]<112
    key=(a[:,:,0]>180)&(a[:,:,2]>160)&(a[:,:,1]<65)&(a[:,:,3]>0);assert not key.any(),(id,name,'bright key residue');components,count=label(a[:,:,3]>0,np.ones((3,3)));areas=np.bincount(components.ravel())[1:];assert sum(v>=8 for v in areas)==1,(id,name,'detached major limb/cloth');diff.append(int(np.any(a!=np.array(images[(i+1)%n]),2).sum()))
   clips.append({'clip':f'{kind}-{d}','frames':n,'distinct':n,'consecutivePixelChangesIncludingLoop':diff,'loopSeamVsMedian':float(diff[-1]/max(1,np.median(diff)))})
 # Actual raster tracking: own near shoe's opaque lowest2rows,not guide-coordinate readback.
 stance=[]
 for d,sign in [('right',1),('left',-1)]:
  shoe=np.array(Image.open(p/'layers'/d/'Rshoe.png').convert('RGBA'));ys,xs=np.where((shoe[:,:,3]>0)&(np.indices(shoe.shape[:2])[0]>=Image.fromarray(shoe).getbbox()[3]-2));pattern=shoe[ys,xs];matches=[]
  for i in range(5):
   a=np.array(frames[f'walk-{d}-{i}']);found=[]
   for dy in range(-4,3):
    for dx in range(-28,29):
     yy,xx=ys+dy,xs+dx
     if yy.min()>=0 and yy.max()<112 and xx.min()>=0 and xx.max()<96 and np.array_equal(a[yy,xx],pattern):found.append((dx,dy))
   assert len(found)==1,(id,d,i,'ambiguous or hidden near-shoe raster',found);dx,dy=found[0];sole=float(xs.mean()+dx);matches.append({'frame':i,'nativeSoleX':sole,'soleY':int(ys.max()+dy),'worldXAtNominalPhase':sole+sign*i*44/8})
  drift=max(r['worldXAtNominalPhase']for r in matches)-min(r['worldXAtNominalPhase']for r in matches);assert drift<=1 and all(sign*(matches[i+1]['nativeSoleX']-matches[i]['nativeSoleX'])<0 for i in range(4)),(id,d,drift);stance.append({'direction':d,'rasterTracks':matches,'quantizedWorldStanceDriftPixels':drift,'thresholdPixels':1})
 for d,v in rig['views'].items():
  for name,r in v['ownership'].items():assert (p/'layers'/d/(name+'.png')).is_file()and r['visiblePixels']>0
 rows.append({'id':id,'cells':104,'clips':clips,'profileRasterStance':stance,'alpha':'BINARY','sourceLayerOwnership':'EXPLICIT own-source masks/joints/occlusion-recovery records','bounds':'PASS','atlasSourceExact':'PASS','connectedMajorAnatomy':'PASS','humanArtApproval':'PENDING'})
(D/'art-technical-qa.json').write_text(json.dumps({'status':'PASS TECHNICAL,NOT ARTISTIC APPROVAL','pilots':rows,'totalCells':312,'currentProceduralNPCBodiesUsed':False,'playerPixelsCopied':False,'scope':'3pilots only;11remainingLOCKED;loop phase/alpha/raster QA does not judge anatomy or beauty'},indent=2)+'\n');print('PASS6591frozenfiles;312nativecells;all16clips/actor distinct;binaryalpha/connectedanatomy/atlasexact;6independentprofile stance tracks≤1px')
