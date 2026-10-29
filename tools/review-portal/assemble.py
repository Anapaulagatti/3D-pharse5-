"""Allowlisted private portal assembly. No art authoring or runtime source edits."""
from pathlib import Path
import json,sys,hashlib,shutil,subprocess,importlib.util
from PIL import Image
R=Path.cwd(); O=Path(sys.argv[1]); args=json.loads((O/'build-input.json').read_text()); sha=lambda b:hashlib.sha256(b).hexdigest()
spec=importlib.util.spec_from_file_location('inventory',R/'tools/phase3a-npc-expansion/inventory.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
names=m.runtime_names(); origins={}
def put(name,b,origin,category):
 p=O/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);origins[name]={'origin':origin,'category':category}
for name in sorted(names):
 if name.endswith('provenance.json'):continue
 put('play/'+name,(R/'public'/name).read_bytes(),'public/'+name,'runtime-protected')
for name in ['LICENSE','LICENSES.md']:
 put(name,(R/name).read_bytes(),name,'license-notice')
for p in (R/'public/licenses').glob('*'):
 if p.is_file():put('licenses/'+p.name,p.read_bytes(),str(p.relative_to(R)),'license-notice')
rights={x['stableId']:x for x in json.loads((R/'assets-src/rights/npc-inventory.json').read_text())['assets']};identities={x['npcId']:x for x in json.loads((R/'assets-src/npcs/phase3a-finalization/identity-presentations.json').read_text())['identities']};plans={x['npcId']:x for x in json.loads((R/'assets-src/npcs/daily-life/schedules.json').read_text())['schedules']}
actors=[]
for name in ['phase3a/registry.json','phase3a-npc-expansion/modern-definitions.json','phase3a-final-six/definitions.json']:
 actors+=json.loads((R/'assets-src/npcs'/name).read_text())['npcs']
assert len(actors)==26 and len({x['id']for x in actors})==26
npcs=[]
for a in actors:
 id=a['id'];ident=identities.get(id);name=ident['publicName']if ident else a['names'];role=ident['role']['vi']if ident else a['occupation'];right=rights[id]
 atlas=R/'public'/a['assets']['texture'];desc=json.loads((R/'public'/a['assets']['atlas']).read_text());f=desc['frames']['idle-front-0']['frame'];pic=Image.open(atlas).convert('RGBA').crop((f['x'],f['y'],f['x']+f['w'],f['y']+f['h']));p=O/'thumbs'/f'{id}.png';p.parent.mkdir(exist_ok=True);pic.save(p);origins[str(p.relative_to(O))]={'origin':str(atlas.relative_to(R))+'#idle-front-0 native crop','category':'native-derived-no-resampling'}
 npcs.append({'id':id,'name':name,'role':role,'zone':a['homeZone'],'archive':bool(ident),'schedule':plans[id]['entries'],'risk':right['risk'],'publication':right['publication']})
comparisons=[]
for id in ['npc-minseo','npc-seoyeon','npc-eunji','npc-history-sejong']:
 a=next(a for a in actors if a['id']==id);native='thumbs/'+id+'.png';old=subprocess.check_output(['git','show','6dbee381:'+('public/'+a['assets']['texture'])]);assert sha(old)==sha((R/'public'/a['assets']['texture']).read_bytes());comparisons.append({'title':next(n['name']['vi']for n in npcs if n['id']==id),'before':native,'after':native,'assertion':'approved3A and3BA atlas SHA256 identical','atlasSHA256':sha(old)})
movies=[]
for stem,title in [('cafe-morning','Lịch phố thương mại · checkpoint3B-A'),('full-day','Một ngày đầy đủ · 60× · checkpoint3B-A'),('archive-story','Truyện xưa / host-slot · checkpoint3B-A'),('mobile-touch','Mobile touch emulation · checkpoint3B-A')]:
 name='media/'+stem+'.mp4';put(name,(R/'docs/phase3b-a/media'/f'{stem}.mp4').read_bytes(),f'docs/phase3b-a/media/{stem}.mp4','checkpoint-gameplay-evidence');movies.append({'title':title,'file':name})
put('catalog.json',json.dumps({'npcs':npcs,'comparisons':comparisons,'movies':movies},ensure_ascii=False,indent=2).encode(),'allowlisted presented registry + schedules + rights','generated-public-summary-private-only')
qa_path=R/'docs/review-portal/QA_RESULT.json';qa=json.loads(qa_path.read_text())if qa_path.exists()else{'status':'NOT TESTED','summary':'Portal candidate: validation pending. Prior checkpoint171unit/72E2E is historical evidence only, not a current run.'}
put('qa.json',json.dumps(qa,ensure_ascii=False,indent=2).encode(),'docs/review-portal/QA_RESULT.json','qa-summary')
version={**args,'phase':args.get('phase','Phase 3B-A'),'artisticReview':'PENDING','commercialRelease':'BLOCKED_PENDING_REVIEW','publicExposure':'NOT_APPROVED','physicalDevices':'NOT_TESTED','archived':False,'currentPath':'./'}
put('version.json',json.dumps(version,indent=2).encode(),'actual Git + UTC build clock','build-metadata')
snap='phases/'+args.get('slug','3b-a')+'/'+args['gameCommit'][:8]+'/'
put('history.json',json.dumps({'snapshots':[{'phase':args.get('phase','Phase 3B-A'),'sha':args['gameCommit'],'path':snap}]}).encode(),'actual snapshot catalog','build-metadata')
for p in (R/'review-portal').glob('*'):
 if p.is_file():put(p.name,p.read_bytes(),str(p.relative_to(R)),'portal-source')
# Manifest does not include itself (avoids circular hashes). Snapshots refer to exact same content-addressed metadata.
def manifest(root):
 files=[]
 for p in sorted(root.rglob('*')):
  if not p.is_file()or p==root/'export-manifest.json'or p.name=='build-input.json':continue
  rel=str(p.relative_to(root));key=rel[len(snap):]if rel.startswith(snap)else rel;o=origins.get(key,{'origin':'Vite compilation of checked game source / private review bridge','category':'compiled-game'})
  asset_id=next((id for id in rights if('/'+id+'/')in ('/'+key)),None);asset_id=asset_id or(next((id for id in rights if Path(key).stem==id),None));asset=rights.get(asset_id,{})
  files.append({'npcId':asset_id,'likenessRisk':asset.get('risk','UNREVIEWED_RUNTIME_CATEGORY'),'generationTool':asset.get('creatorTool',{}).get('recordedRoute','runtime/project provenance; not independently licensed here'),'filename':rel,'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size,**o,'knownTerms':'repository notices retained; asset-specific generation/account/third-party evidence incomplete'if o['category']not in ['portal-source','build-metadata','qa-summary']else'project-authored review tooling; repository license','publicPreviewDecision':'NOT_APPROVED','commercialRelease':'BLOCKED_PENDING_REVIEW','risk':'NPC depiction/branding/source terms require review; other runtime categories not cleared by NPC audit','missingEvidence':'asset-specific exposure approval; applicable upstream terms and review'})
 return {'schemaVersion':1,'gameCommit':args['gameCommit'],'portalCommit':args['portalCommit'],'scope':'PRIVATE ONLY; includes no raw prompts/source masters/full sensitive audit records; manifest hashes all exported files except itself and local build input','files':files}
(O/'build-input.json').unlink()
# Snapshot is write-once. Rebuilding same game SHA with different portal must preserve old snapshot or fail.
T=O/snap
if T.exists():
 old=json.loads((T/'version.json').read_text())
 if old['portalCommit']!=args['portalCommit']or old.get('dirty')or args['dirty']:raise SystemExit('Immutable snapshot already exists; choose fresh output, retain old snapshot before promotion')
else:
 current=[p for p in O.iterdir()if p.name!='phases']
 T.mkdir(parents=True)
 for p in current:
  if p.is_dir():shutil.copytree(p,T/p.name)
  else:shutil.copy2(p,T/p.name)
 v={**version,'archived':True,'currentPath':'../../../'};(T/'version.json').write_text(json.dumps(v,indent=2));(T/'history.json').write_text(json.dumps({'snapshots':[{'phase':args.get('phase','Phase 3B-A'),'sha':args['gameCommit'],'path':'./'}]}))
 (T/'export-manifest.json').write_text(json.dumps(manifest(T),indent=2))
(O/'export-manifest.json').write_text(json.dumps(manifest(O),indent=2))
print('Private portal assembled:',len(npcs),'NPCs,',len(manifest(O)['files']),'files; NO PUBLIC APPROVAL')
