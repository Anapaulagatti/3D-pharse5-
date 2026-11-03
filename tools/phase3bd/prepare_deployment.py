import sys
"""Stage existing review-repo controls locally. No remote write, Actions dispatch or approval."""
from pathlib import Path
import json,subprocess,hashlib
R=Path.cwd();D=R/'docs/phase3bd';C=Path('/workspace/review-pages-destination');O=R/sys.argv[1];P=D/'deployment-prep';P.mkdir(exist_ok=True)
proof=json.loads((D/'PUBLIC_CANDIDATE_PROOF.json').read_text());m=json.loads((O/'export-manifest.json').read_text());artifact=subprocess.check_output(['git','rev-parse','HEAD'],cwd=O,text=True).strip();old=json.loads((C/'approved-releases/current.approved.json').read_text());config=json.loads((C/'review-source.json').read_text())
ids=sorted({r['npcId']for r in m['files']if r.get('npcId')});assert len(ids)==26;assert m['portalCommit']==proof['sourceCommit'];assert ids==sorted(old['npcReviews'])
config['acceptedBuildSourceCommits']=list(dict.fromkeys([*config['acceptedBuildSourceCommits'],m['portalCommit']]))
config['releaseProfiles']['phase3bd-farm26']={**config['releaseProfiles']['phase3bb-fictional26'],'manifestSHA256':proof['manifestSHA256'],'npcIds':ids,'scope':'26 unchanged fictionalNPC,12players,24activecosmetics,5original local-demo learning quests,6farmplots,2crops,Minseo shop,strictcanonicalassetallowlist and exact review media; public exposure PENDING'}
(P/'review-source.json').write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n')
receipt={**old,'profile':'phase3bd-farm26','manifestSHA256':proof['manifestSHA256'],'artifactCommit':artifact,'decision':'PENDING_OWNER_EXACT_PUBLIC_PREVIEW_APPROVAL','approvedBy':None,'approvedAt':None,'purpose':'Private prepared release receipt. Existing unchanged artwork eligibility inherits prior explicit26 decision; changed exact artifact NOT approved. No legal/commercial certification.'}
receipt['snapshotManifests']={str(p.relative_to(O)):hashlib.sha256(p.read_bytes()).hexdigest()for p in(O/'phases').glob('*/*/export-manifest.json')}
for group in receipt['groups'].values():group['decision']='PENDING_EXACT_OWNER_APPROVAL'
receipt['changeScope']={'activeCosmetics':24,'retiredHeadEquipment':4,'newQuests':2,'totalQuests':5,'farmPlots':6,'cropTypes':2,'shops':1,'learningMode':'LOCAL_DEMO_HUMAN_EDUCATIONAL_REVIEW_PENDING','newCollisionMasks':0,'protectedArtChanges':0,'newNativeCropFrames':6,'newApprovedSourcePostcardCrops':1}
(P/'review-candidates').mkdir(exist_ok=True);(P/'review-candidates/phase3bd-farm26.pending.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
for name in ['receipt.py','gate.py','history_gate.py']:(P/name).write_bytes((C/name).read_bytes())
# Existing old26 verifier remains unchanged by default. New profile checks ignored retired preferences.
s=(C/'verify_motion.mjs').read_text().replace('verifyMotion(browser,base)', 'verifyMotion(browser,base,retired=false)').replace('let trace=[];','let trace;').replace('a.state.appearance.accessoryIds[0]!==acc','(retired?a.state.appearance.accessoryIds.length!==0:a.state.appearance.accessoryIds[0]!==acc)');(P/'verify_motion.mjs').write_text(s)
s=(C/'verify_live.mjs').read_text().replace("if(manifest.profile==='phase3bb-fictional26') result.motionCosmetics=await verifyMotion(browser,base);", "if(manifest.profile==='phase3bb-fictional26') result.motionCosmetics=await verifyMotion(browser,base);\n  if(manifest.profile==='phase3bd-farm26') result.retiredHeadPreferencesAndMotion=await verifyMotion(browser,base,true);");(P/'verify_live.mjs').write_text(s)
# Keep current destination untouched. Validate only the new exact artifact's immutable contract.
for row in m['files']:assert hashlib.sha256((O/row['filename']).read_bytes()).hexdigest()==row['sha256']
blocked=subprocess.run(['python3','receipt.py','review-candidates/phase3bd-farm26.pending.json'],cwd=P,capture_output=True,text=True);assert blocked.returncode!=0 and'PENDING'in blocked.stdout+blocked.stderr
history=subprocess.run(['python3','history_gate.py',str(O),'review-candidates/phase3bd-farm26.pending.json'],cwd=P,capture_output=True,text=True);assert history.returncode==0,history.stderr
result={**proof,'artifactCommit':artifact,'controlRepository':'Anapaulagatti/3D-pharse5-review','preparedFilesOnly':True,'remoteWritten':False,'workflow':'existing review-pages.yml','lineageAndNPCManifestContract':'PASS','pendingReceiptBlockedBeforeArtFetch':True,'snapshotHistoryGate':'PASS','approval':'PENDING','livePagesUnchanged':True}
(D/'DEPLOYMENT_PREPARATION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
