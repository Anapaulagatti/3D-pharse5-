from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,subprocess
import numpy as np
R=Path(__file__).resolve().parents[1];D=R/'docs/g3a-platform-restoration';old=R/'docs/g3a-controlled-finalization/before-station-native.png';before=Image.open(old).convert('RGB');after=Image.open(D/'restored-station-native.png').convert('RGB');rows=json.loads((D/'native-captures.json').read_text())['rows'];r=next(x for x in rows if x['name']=='restored-station-native');assert r['audit']['camera']['matrix'][:6]==[1,0,0,1,-1959,-2010]
rois={'station-artwork':(2274,2196,3040,2740),'platform':(2860,2190,3040,2750),'entrance':(2542,2619,2669,2688),'tactile':(2572,2613,2627,2726),'left-pavement':(2302,2669,2549,2726),'right-pavement':(2669,2669,2909,2726)};proof=[]
for name,box in rois.items():
 local=tuple(v-[1959,2010][i%2] for i,v in enumerate(box));a=before.crop(local);b=after.crop(local);n=int(np.any(np.array(a)!=np.array(b),axis=2).sum());assert n==0,(name,n);a.save(D/f'{name}-before-1x.png',optimize=True);b.save(D/f'{name}-restored-1x.png',optimize=True);proof.append({'roi':name,'worldBox':box,'differentPixels':n,'totalPixels':a.width*a.height})
a=Image.open(D/'platform-before-1x.png');b=Image.open(D/'platform-restored-1x.png');sheet=Image.new('RGB',(a.width*2+30,a.height+40),'#17242e');draw=ImageDraw.Draw(sheet);draw.text((10,8),'BEFORE / native 1:1',fill='white');draw.text((a.width+20,8),'RESTORED / native 1:1',fill='white');sheet.paste(a,(10,30));sheet.paste(b,(a.width+20,30));sheet.save(D/'BEFORE_RESTORED_1X.png',optimize=True)
m=json.loads((R/'public/assets/gate3/registration-working-v3/manifest.json').read_text());W,H=m['size'];mask=np.zeros((H,W),np.uint8)
for c in m['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];mask[y:y+h,x:x+w]=np.frombuffer((R/'public'/c['mask']).read_bytes(),np.uint8).reshape(h,w)
# Native overlay is explicitly annotated; original pixels remain separate above.
box=(2860,2590,3040,2790);local=(901,580,1081,780);im=after.crop(local).convert('RGBA');pixels=np.array(im);blocked=mask[2590:2790,2860:3040]==0;pixels[blocked,:3]=(pixels[blocked,:3].astype(float)*.65+np.array([255,30,30])*.35).astype('uint8');overlay=Image.fromarray(pixels).convert('RGB');d=ImageDraw.Draw(overlay);d.rectangle((90,36,97,164),outline='yellow');d.line((120,100,98,100),fill='cyan',width=1);d.rectangle((98,98,100,102),fill='cyan');overlay.save(D/'collision-overlay-native.png',optimize=True)
# Read the exact source edge and ownership provenance, not an inferred facade bbox.
src=np.array(Image.open(R/'public/assets/gate2/district-planter-repair/walk.png').convert('L'));assert np.all(src[713:842,3176:3184]==0);assert np.all(mask[2626:2755,2950:2958]==0)
locks=json.loads((R/'docs/g3a-controlled-finalization/protected-assets.json').read_text())['sha256'];bad=[p for p,h in locks.items()if hashlib.sha256((R/p).read_bytes()).hexdigest()!=h];assert not bad
refs=json.loads((R/'docs/g3a-controlled-finalization/protected-checkpoints.json').read_text());assert all(subprocess.check_output(['git','rev-parse',k],cwd=R,text=True).strip()==v for k,v in refs['existingRefs'].items());assert subprocess.check_output(['git','ls-remote','origin','refs/heads/main'],cwd=R,text=True).split()[0]==refs['mainBefore']
for layer in r['audit']['layers']:
 assert all(float(v).is_integer()for v in layer['position']+layer['screenOrigin']);assert layer['scale']==[1,1] and layer['scaleMode']==1
 if 'minFilter'in layer:assert layer['minFilter']==layer['magFilter']==9728
report={'nativePixelComparison':proof,'protectedAssetsVerified':len(locks),'protectedAssetMismatches':bad,'allHistoricalCheckpointRefsUnchanged':True,'mainUnchanged':True,'nativeIntegerNearestSampling':'PASS','legacy8pxGuard':'UNCHANGED / BLOCKING','transferMovement':'FAIL / blocked at x2958,y2690','newVisualConnectorActive':False,'canonicalForecourt':'UNCHANGED','acceptedV3PlanAndRegistrations':'EXACT','visualReview':'PENDING HUMAN REVIEW','physicalAndroidChrome':'NOT TESTED','physicalIPhoneSafari':'NOT TESTED','hardwareWebGLPerformance':'UNRESOLVED','G3B':'BLOCKED'}
(D/'qa-report.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS:',len(locks),'protected hashes; six native ROIs zero difference; historical refs unchanged')
