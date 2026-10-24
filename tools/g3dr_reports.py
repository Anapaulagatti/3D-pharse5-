from pathlib import Path
import json,hashlib,subprocess
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-reconciliation';S=R/'assets-src/gate3/reconciliation-v1'
def rd(p):return json.loads(p.read_text())
def wr(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
qa=rd(D/'technical-qa.json');cap=rd(D/'native-captures.json');integ=rd(S/'integration-provenance.json');m=rd(R/'public/assets/gate3/reconciled-world/manifest.json')
assert len(cap['rows'])==30 and not cap['errors'];assert len(qa['pixelReadback'])==14;assert all(r['mismatched']==0 and r['integerCamera']and r['samplingScaleNative']for r in qa['pixelReadback']);assert qa['protectedHashes']['status']=='PASS'and qa['protectedHashes']['historicalTagsUnchanged']and all(qa['rendererCoreUnchanged'].values())
W,H=m['size'];f=np.zeros((H,W),np.uint8)
for c in m['chunks']:
 x,y,w,h=[c[k]for k in ['x','y','width','height']];f[y:y+h,x:x+w]=np.frombuffer((R/'public'/c['mask']).read_bytes(),np.uint8).reshape(h,w)
movement=rd(D/'movement-report.json');body=[]
for leg in movement['legs']:
 rows=[s for s in movement['samples']if s.get('leg')==leg['id']];bad=[]
 for s in rows:
  x,y=round(s['x']),round(s['y']);foot=f[y-8:y+9,x-24:x+25]
  if foot.shape!=(17,49)or np.any(foot==0):bad.append([round(s['x'],2),round(s['y'],2)])
 body.append({'leg':leg['id'],'actualFootMovement':leg['status'],'samples':len(rows),'body49x17EnvelopeFailures':len(bad),'firstFailures':bad[:12],'status':'FAIL_CONSERVATIVE_BODY_ENVELOPE'if bad else'PASS_SELECTED_49x17_GROUND_ENVELOPE','caveat':'Ground footprint only, not upper-body opacity/visual acceptance'})
wr(D/'body-clearance.json',{'method':'Every recorded movement sample checked against actual field using conservative native49x17 contact envelope; actual WASD video separately shows foreground/upper-body behavior. No sprite shrinking or collision clearing.','legs':body,'visibleUpperBody':'Native videos/frames require visual review; not inferred PASS from ground field','completeNetwork':'FAIL / inherited planned route and body conflicts remain'})
qa['checks']={'typecheck':'PASS','assetsPreservationChecks':'PASS','unitTests':'28 PASS /8 files','targetedLint':'PASS','privateViteBuild':'PASS','nativeFrames':30,'identicalBeforeAfterPairs':14,'pixelReadbackPixels':sum(r['opaqueGroundPixels']for r in qa['pixelReadback']),'mismatchedGroundPixels':0,'actualMovementLegs':len(movement['legs']),'actualMovementComplete':movement['complete'],'physicalAndroidChrome':'NOT TESTED','physicalIPhoneSafari':'NOT TESTED','hardwareWebGLPerformance':'NOT TESTED'}
qa['changedGroundChunks']=len(integ['changedGroundChunks']);qa['changedFieldChunks']=len(integ['changedMaskChunks']);qa['visualAxes']={'architecture':'PRESERVED / palace protected-source spatial conflicts remain','materials':'REVIEW / native common families; station residual baked/source joins remain FAIL','depth':'REVIEW / original fade retained; inherited tower/ride projection unresolved','lighting':'REVIEW / native source light/contact shadows; no automatic artistic PASS','composition':'FAIL_OPEN_P1 / no full-world acceptance','scale':'PASS_NATIVE1X_REGISTRATION / no building downscale','navigation':'FAIL_FULL_NETWORK / actual movement legs and body report separate','pixelClarity':'PASS_RUNTIME_READBACK / art/source details separately reviewed'};qa['exactEightMarkedScreenshots']='NOT PROVIDED / exact annotation matching NOT TESTED';qa['fullBody']=body
wr(D/'technical-qa.json',qa)
files=[{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':sha(p)}for p in sorted(S.rglob('*'))if p.is_file()and not p.name.endswith('-before-ground.png')];wr(D/'asset-provenance.json',{'authoring':'Built-in host imagegen for contextual environment trials; no external paid provider API. Original paths/prompts in authoring-jobs.json. Rejected contextual waternorth/watersouth RGB and court trial not installed; clean ocean-authored offshore family selected after128px sample repetition failed native review. Native extraction and explicit source masks used.','sources':files,'integration':'integration-provenance.json + preservation-details.json + ownership-audit.json describe actual ownership. No canonical source mutation, scaling, filtering, mirror donors or sharpening.','historicalSourcePreservation':'1440 protected files plus371 latest zoning artifacts verified','artAcceptance':'PENDING HUMAN'})
# Explicit collision-only diagnostic, not a gameplay substitute.
row=next(r for r in cap['rows']if r['name']=='station-right-after-native');sx,sy=row['audit']['camera']['scroll'];im=Image.open(D/'station-right-after-native.png').convert('RGBA');ol=Image.new('RGBA',im.size);dr=ImageDraw.Draw(ol);x,y,w,h=2950,2626,8,129;dr.rectangle((x-sx,y-sy,x+w-1-sx,y+h-1-sy),fill=(255,50,65,150));dr.text((x-sx-220,y-sy-20),'8px CLOSED / not cleared / no90x36 connector',fill=(255,255,255,255));Image.alpha_composite(im,ol).save(D/'station-collision-strip-native.png',optimize=True)
print('Consolidated QA complete; actual legs',len(movement['legs']),'body failures',sum(v['body49x17EnvelopeFailures']for v in body))
