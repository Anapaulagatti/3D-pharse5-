"""Freeze subset QA and its own snapshot, retaining old canonical all-26 checkpoint privately."""
from pathlib import Path
import json,hashlib,shutil,datetime
R=Path.cwd();O=R/'.cache/exposure20-private';D=R/'docs/review-exposure';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
qa=json.loads((D/'runtime20/LIVE_QA.json').read_text());assert qa['status'].startswith('PASS PRIVATE LOCAL')and len(qa['actors'])==20
p=O/'qa.json';p.write_text(json.dumps({'status':'PASS LOCAL BROWSER; RIGHTS STILL BLOCKED','summary':'20/20 actual Phaser NPC approaches, dialogues, return controls and daily-life clock passed. 656 initial URLs loaded, no console/resource errors; landscape joystick moved Juni 37.30px. Six era-inspired NPCs, all old videos and unapproved all-26 snapshots omitted. Shared account/creation terms remain UNKNOWN. Physical devices and live HTTPS NOT TESTED.'},ensure_ascii=False,indent=2)+'\n')
p=O/'version.json';v=json.loads(p.read_text());v['builtAt']=datetime.datetime.now(datetime.timezone.utc).isoformat();v['exposure']='UNAPPROVED_RESTRICTED_PREVIEW_CANDIDATE';p.write_text(json.dumps(v,indent=2)+'\n')
# Correct count description across line-wrapped original template without restyling portal.
p=O/'index.html';t=p.read_text();import re
t=re.sub(r'14 cư dân \+ 6 khách hư cấu \+ 6 nhân vật truyện xưa hư cấu\.', '14 cư dân + 6 khách hư cấu. Sáu nhân vật theo thời kỳ bị loại khỏi bản này.',t);p.write_text(t)
snap='phases/3b-a/contemporary20-'+sha(O/'play/index.html')[:8]+'/'
(O/'history.json').write_text(json.dumps({'snapshots':[{'phase':'Phase 3B-A · contemporary20 restricted candidate','sha':v['gameCommit'],'path':snap}]},ensure_ascii=False)+'\n')
old=json.loads((O/'export-manifest.json').read_text());base={r['filename']:r for r in old['files']}
T=O/snap
if T.exists():raise SystemExit('Do not overwrite an existing snapshot')
T.mkdir(parents=True)
for p in list(O.iterdir()):
 if p.name in ['phases','export-manifest.json']:continue
 if p.is_dir():shutil.copytree(p,T/p.name)
 else:shutil.copy2(p,T/p.name)
v2={**v,'archived':True,'currentPath':'../../../'};(T/'version.json').write_text(json.dumps(v2,indent=2)+'\n');(T/'history.json').write_text(json.dumps({'snapshots':[{'phase':'Phase 3B-A · contemporary20 restricted candidate','sha':v['gameCommit'],'path':'./'}]},ensure_ascii=False)+'\n')
def manifest(root):
 files=[]
 for p in sorted(root.rglob('*')):
  if not p.is_file()or p==root/'export-manifest.json':continue
  rel=str(p.relative_to(root));key=rel[len(snap):]if rel.startswith(snap)else rel;x=dict(base.get(key,{'npcId':None,'origin':'Restricted20 snapshot metadata'}));x.update(filename=rel,sha256=sha(p),bytes=p.stat().st_size);files.append(x)
 return{**old,'files':files}
(T/'export-manifest.json').write_text(json.dumps(manifest(T),ensure_ascii=False,indent=2)+'\n');(O/'export-manifest.json').write_text(json.dumps(manifest(O),ensure_ascii=False,indent=2)+'\n')
proof=json.loads((D/'RESTRICTED20_PACKAGE.json').read_text());proof.update(manifestSHA256=sha(O/'export-manifest.json'),files=len(manifest(O)['files']),bytes=sum(x['bytes']for x in manifest(O)['files']),snapshotManifests={snap+'export-manifest.json':sha(T/'export-manifest.json')},localRuntimeQA='PASS 20 actual NPCs / daily-life / mobile emulator; not live HTTPS',initialRuntimeAssetURLChecks=656);(D/'RESTRICTED20_PACKAGE.json').write_text(json.dumps(proof,indent=2)+'\n');print(proof['manifestSHA256'],proof['files'])
