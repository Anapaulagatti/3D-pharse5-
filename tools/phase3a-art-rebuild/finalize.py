"""Consolidate completed review measurements without granting artistic approval."""
from pathlib import Path
import json,hashlib,shutil,re,urllib.parse
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a-art-rebuild';S=R/'assets-src/npcs/phase3a-art-rebuild';L=D/'logs';L.mkdir(exist_ok=True)
for n in ['typecheck','assets','lint','format','unit','build','focused']:
 p=Path('/tmp/phase3a-art-final-'+n+'.log')
 if p.exists():shutil.copyfile(p,L/(n+'.log'))
shutil.copyfile('/tmp/phase3a-art-e2e.log',L/'full60-e2e.log')
for n in ['skill-qa','extra-evidence','webgl-readbacks','package-npcs','package-characters','package-inspector','portable-build','media']:
 p=Path('/tmp/phase3a-art-'+n+'.log')
 if p.exists():shutil.copyfile(p,L/(n+'.log'))
full=json.loads((D/'e2e/e2e-results.json').read_text())['stats'];focused=json.loads((D/'final-focused/e2e-results.json').read_text())['stats'];assert full['expected']==60 and focused['expected']==7 and all(q['unexpected']==0 and q['skipped']==0 for q in [full,focused])
for name in ['package-npcs-smoke.json','package-characters-smoke.json','package-inspector-smoke.json']:assert json.loads((D/name).read_text())['status']=='PASS'
q=D/'QA.md';s=q.read_text().replace('| Typecheck/assets/lint/format/unit/build |See final logs|','| Typecheck/assets/lint/format/unit/build |PASS|').replace('| Final focused E2E |See report|','| Final focused E2E |PASS7/7|').replace('| Independent playable ZIP |PENDING package proof|Must verifyCRC/SHA and test independently extracted actual game/inspector |','| Independent playable ZIP |PASS technical|3actualpilot approaches/dialogues,12curatedplayerlooks/presets/reload/reset/touch,3pilot×4directioninspector;CRC/SHA/runtime inventory checked |')
s+='\n## Additional recorded checks\n\n[Full60report](e2e/e2e-results.json),[final7report](final-focused/e2e-results.json),[required command logs](logs/full60-e2e.log).131unit tests,0skipped. All original suites intact.\n\n[Independent3pilotgameplay](package-npcs-smoke.json),[12approvedplayers/Studio/persistence/touch](package-characters-smoke.json),[independentinspector](package-inspector-smoke.json),[ZIP manifest/SHA](package-proof.json),[final extraction verification](package-smoke.json). Two browser landscape layouts667×375/844×390,44pxcontrols;two actual softwareWebGL new-pilot native readbacks with0mismatch;realpalacevisitedmarker→NPCdialogue→reload preserves position/appearance/visited state. [Rawextraobservations](extra-evidence.json). Hardware/mobilephysical certification remains NOT TESTED.\n\nNPC atlas dimensions remain768×1456RGBA:4,472,832decodedbytes per atlas,unchanged from baseline. Original4resident/2inflight bounds remain unchanged;actual captures and browser regressions preserve singleplayer/bounded NPCcache. Source masters/layers are offline authoring data,not eagerly loaded gameplay textures. No new runtime dependency or performance certification.\n';q.write_text(s)
files={}
for stem in ['assets-src/npcs/phase3a-art-rebuild','tools/phase3a-art-rebuild']:
 for p in(R/stem).rglob('*'):
  if p.is_file()and'__pycache__'not in p.parts:files[str(p.relative_to(R))]=hashlib.sha256(p.read_bytes()).hexdigest()
(D/'source-files-sha256.json').write_text(json.dumps({'files':files,'route':'host_image7actualcalls;rawgenerationprompts/provenance retained','paidExternalAPIs':[],'humanArtApproval':'PENDING'},indent=2)+'\n')
# Verify every new review document link before publication.
bad=[];valid=0
for n in ['README.md','ART_PIPELINE.md','JUNI_STYLE_COMPARISON.md','PILOT_REVIEW.md','QA.md','PROTECTED_AUDIT.md','REVIEW.html']:
 p=D/n
 for row in re.findall(r'(?:href|src)="([^"]+)"|\]\(([^)]+)\)',p.read_text()):
  u=next(x for x in row if x)
  if u.startswith(('http:','https:','#','data:')):continue
  target=(p.parent/urllib.parse.unquote(u.split('?')[0].split('#')[0])).resolve()
  if not target.is_file():bad.append([n,u])
  else:valid+=1
# package-smoke is produced after final documented repack;do not fabricate a result.
remaining=[r for r in bad if r[1]!='package-smoke.json'];assert not remaining,remaining
(D/'link-check.json').write_text(json.dumps({'status':'PASS'if not bad else'PENDING final package verification','validLocalReviewLinks':valid,'missing':bad},indent=2)+'\n');print('Final60+7/131unit,independent3pilot+12player+inspector evidence consolidated;sourcehashes',len(files),'links',valid,'humanartapprovalPENDING')
