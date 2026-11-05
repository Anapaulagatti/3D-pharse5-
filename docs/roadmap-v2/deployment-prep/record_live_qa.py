"""Selected nonsecret actual hosted QA evidence. Never fabricates a live PASS."""
from pathlib import Path
import sys,json,os,datetime
p=Path(sys.argv[1]);receipt=json.loads(Path(sys.argv[2]).read_text());config=json.loads(Path('review-source.json').read_text());spec=config['releaseProfiles'][receipt['profile']]
q=json.loads(p.read_text())if p.is_file()else{'status':'NOT TESTED','reason':'The deployment job produced no actual browser verification report'}
expected='https://anapaulagatti.github.io/3D-pharse5-review/'
passed=(q.get('status')=='PASS ACTUAL DEPLOYED HTTPS GAME'and q.get('url')==expected and q.get('liveManifestSHA256')==receipt['manifestSHA256']and {r.get('id')for r in q.get('actors',[])}==set(spec['npcIds'])and not q.get('errors')and not q.get('missing')and q.get('mobileJoystickDistance',0)>1 and len(q.get('assetURLs',[]))>0 and all(200<=r.get('status',0)<400 for r in q.get('assetURLs',[])))
if receipt['profile']=='phase3bb-fictional26':passed=passed and q.get('motionCosmetics',{}).get('status')=='PASS ACTUAL BROWSER POSE/INPUT CHECKS'
if receipt['profile'] in ['phase3bd-in-world26','phase3bd-farm-path26','phase3bd-final-quality26']:passed=passed and q.get('physicalWorld',{}).get('status')=='PASS ACTUAL HOSTED PHYSICAL PHASE3BD' and q.get('retiredHeadPreferencesAndMotion',{}).get('status')=='PASS ACTUAL BROWSER POSE/INPUT CHECKS'
if receipt['profile']=='phase3bd-farm-path26':passed=passed and q.get('farmPathHotfix',{}).get('status')=='PASS ACTUAL FARM LIFECYCLE / QUEST / PATHS'
if receipt['profile']=='phase3bd-final-quality26':passed=passed and q.get('finalQuality',{}).get('status')=='PASS ACTUAL FINAL QUALITY'
if receipt['profile']=='roadmap-v2-local26':passed=passed and q.get('roadmapV2',{}).get('status')=='PASS EXACT V2 GAME / ALL HTTP HASHES / FARM / THREE ROOMS / VIDEO'
report={'recordedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runId':os.environ['GITHUB_RUN_ID'],'runAttempt':os.environ['GITHUB_RUN_ATTEMPT'],'runURL':'https://github.com/'+os.environ['GITHUB_REPOSITORY']+'/actions/runs/'+os.environ['GITHUB_RUN_ID'],'status':'PASS ACTUAL DEPLOYED HTTPS GAME'if passed else'NOT VERIFIED / '+q.get('status','NO REPORT'),'url':q.get('url'),'expectedAssetManifestSHA256':receipt['manifestSHA256'],'actualLiveManifestSHA256':q.get('liveManifestSHA256'),'artifactCommit':receipt['artifactCommit'],'profile':receipt['profile'],'actorChecks':q.get('actors',[]),'assetURLsChecked':len(q.get('assetURLs',[])),'errors':q.get('errors',[]),'missing':q.get('missing',[]),'mobileJoystickDistance':q.get('mobileJoystickDistance'),'failure':q.get('failure',q.get('reason')),'physicalDevices':'NOT TESTED','hardwareGPU':'NOT TESTED'}
report['roadmapV2']=q.get('roadmapV2')
report['motionCosmetics']=q.get('motionCosmetics')
report['physicalWorld']=q.get('physicalWorld')
report['farmPathHotfix']=q.get('farmPathHotfix')
report['finalQuality']=q.get('finalQuality')
report['retiredHeadPreferencesAndMotion']=q.get('retiredHeadPreferencesAndMotion')
report['transientAssetRetries']=q.get('transientAssetRetries',[])
report['verificationMode']=os.environ.get('VERIFICATION_MODE','release-job')
report['deploymentRunId']=os.environ.get('DEPLOYMENT_RUN_ID',os.environ['GITHUB_RUN_ID'])
Path('live-verification.json').write_text(json.dumps(report,indent=2)+'\n')
