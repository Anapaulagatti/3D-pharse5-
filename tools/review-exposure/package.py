"""Asset allowlist and exact subset manifest; no image edits, no public approval."""
from pathlib import Path
import json,hashlib,sys,shutil,importlib.util,datetime
R=Path.cwd();S=Path('/workspace/review-pages-compiled');O=Path(sys.argv[1]);D=R/'docs/review-exposure'
spec=importlib.util.spec_from_file_location('notices',R/'tools/review-exposure/notices.py');n=importlib.util.module_from_spec(spec);spec.loader.exec_module(n)
m=json.loads((S/'export-manifest.json').read_text());origins={x['filename']:x for x in m['files']};excluded=[]
for x in m['files']:
 rel=x['filename'];p=S/rel
 if rel.startswith('phases/')or rel.startswith('media/')or rel.startswith('play/')and not rel.startswith('play/assets/'):continue
 if rel.startswith('play/assets/')and not rel.endswith(('.png','.json','.bin')):continue
 if x.get('npcId','')and x['npcId'].startswith('npc-history-'):excluded.append(rel);continue
 if rel in ['catalog.json','version.json','qa.json','history.json','index.html','portal.mjs']:continue
 target=O/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
catalog=json.loads((S/'catalog.json').read_text());catalog['npcs']=[a for a in catalog['npcs']if not a['archive']];catalog['comparisons']=[c for c in catalog['comparisons']if 'npc-history-'not in str(c)];catalog['movies']=[];assert len(catalog['npcs'])==20
(O/'catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
for filename in ['index.html','portal.mjs']:
 t=(S/filename).read_text()
 if filename=='index.html':
  t=t.replace('26 NPC','20 NPC · bản giới hạn').replace('14 cư dân + 6 khách hư cấu + 6 nhân vật truyện xưa hư cấu.','14 cư dân + 6 khách hư cấu. Sáu nhân vật theo thời kỳ bị loại khỏi bản này.').replace('DEVELOPMENT REVIEW','PRIVATE RESTRICTED STAGING').replace('Bản phát triển để đánh giá; không phải bản phát hành thương mại.','Bản giới hạn riêng tư; điều khoản asset chưa đủ. Không được xuất bản. Không phải bản 26 NPC.')
 else:t=t.replace('"ARTISTIC REVIEW": "PENDING"','"ARTISTIC REVIEW": "APPROVED PHASE 3B-A; NOT PUBLIC EXPOSURE"')
 (O/filename).write_text(t)
version=json.loads((S/'version.json').read_text());version.update(phase='Phase 3B-A · 20-NPC private restricted candidate',exposure='PRIVATE_STAGING_TERMS_BLOCKED',publicExposure='NOT_APPROVED',artisticReview='APPROVED_PHASE_3B_A',archived=False,restrictedProfile='contemporary20',actualNPCCatalog=20,excludedHistoricalInspired=6,sourceGameUnchanged=True,adapterOnlyRuntime=True)
(O/'version.json').write_text(json.dumps(version,indent=2)+'\n');(O/'history.json').write_text('{"snapshots":[]}\n')
(O/'qa.json').write_text(json.dumps({'status':'PENDING subset runtime QA','summary':'20 actual living NPCs; six era-inspired NPCs, their thumbnails/atlases/metadata, all videos and old all-26 snapshots excluded. Shared creation-account evidence remains UNKNOWN; NOT ELIGIBLE FOR PUBLICATION. Canonical 26-NPC game untouched.'},ensure_ascii=False,indent=2)+'\n')
# Reuse existing namespace wrapper; preserve v0.5 and existing saves.
p=O/'play/index.html';p.write_text(p.read_text().replace('<head>','<head><script type="module" src="./pages-saves.mjs"></script>'));shutil.copy2(S/'play/pages-saves.mjs',O/'play/pages-saves.mjs')
notices=n.write_notices(O)
# No old snapshot may leak excluded artwork or the old compiled 26 registry.
assert not(O/'phases').exists()and not(O/'media').exists()
for p in O.rglob('*'):
 if not p.is_file():continue
 assert 'npc-history-'not in str(p),p
 if p.suffix in ['.js','.json','.mjs','.html']:
  text=p.read_text()
  for id in ['seondeok','sejong','jang','saimdang','yi','yu']:assert ('npc-history-'+id)not in text,(p,id)
files=[]
for p in sorted(O.rglob('*')):
 if not p.is_file():continue
 rel=str(p.relative_to(O));o=origins.get(rel,{});files.append({'filename':rel,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'origin':o.get('origin','Isolated restricted20 adapter or retained third-party notice'),'npcId':o.get('npcId'),'publicPreviewDecision':'NOT_APPROVED','termsEligibility':'UNKNOWN_SHARED_ACCOUNT_EVIDENCE','commercialRelease':'BLOCKED_PENDING_REVIEW'})
manifest={'schemaVersion':2,'profile':'contemporary20','scope':'PRIVATE restricted staging; not a cleared/sanitized public release','base':'/3D-pharse5-review/','gameCommit':m['gameCommit'],'portalCommit':m['portalCommit'],'npcIds':[a['id']for a in catalog['npcs']],'excludedNPCs':6,'files':files};(O/'export-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
proof={'candidate':str(O.relative_to(R)),'manifestSHA256':hashlib.sha256((O/'export-manifest.json').read_bytes()).hexdigest(),'files':len(files),'bytes':sum(x['bytes']for x in files),'actualCatalog':20,'excluded':excluded,'oldSnapshots':'Kept in canonical private checkpoint; never previously public, intentionally not included in restricted distribution','removedVideos':4,'sourceArtEdits':0,'publicEligible':False,'terms':'UNKNOWN; public gate must reject','noticesAdded':notices,'adapterSHA256':hashlib.sha256((R/'tools/review-exposure/build20.mjs').read_bytes()).hexdigest(),'checkedAt':datetime.datetime.now(datetime.timezone.utc).isoformat()};(D/'RESTRICTED20_PACKAGE.json').write_text(json.dumps(proof,indent=2)+'\n');print('Restricted package:',len(files),'files; manifest',proof['manifestSHA256'])
