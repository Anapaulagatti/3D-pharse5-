"""Add missing software notices and accepted-review status; reuse compiled game bytes."""
from pathlib import Path
import shutil,json,hashlib,importlib.util
R=Path.cwd();S=Path('/workspace/review-pages-compiled');O=R/'.cache/exposure26-private';D=R/'docs/review-exposure'
if O.exists():raise SystemExit('Use fresh destination; keep candidates recoverable')
m=json.loads((S/'export-manifest.json').read_text());O.mkdir(parents=True)
for x in m['files']:
 p=O/x['filename'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(S/x['filename'],p)
spec=importlib.util.spec_from_file_location('notices',R/'tools/review-exposure/notices.py');n=importlib.util.module_from_spec(spec);spec.loader.exec_module(n);n.write_notices(O)
p=O/'portal.mjs';p.write_text(p.read_text().replace('"ARTISTIC REVIEW": "PENDING"','"ARTISTIC REVIEW": "APPROVED PHASE 3B-A; NOT PUBLIC EXPOSURE"'))
p=O/'version.json';q=json.loads(p.read_text());q.update(artisticReview='APPROVED_PHASE_3B_A',publicExposure='NOT_APPROVED');p.write_text(json.dumps(q,indent=2)+'\n')
p=O/'LICENSES.md';p.write_text(p.read_text()+'\nAdditional installed dependency/vendor notices: licenses/THIRD_PARTY_ADDITIONS.txt. These notices do not license generated art or clear likeness rights.\n')
files=[];old={x['filename']:x for x in m['files']}
for p in sorted(O.rglob('*')):
 if not p.is_file():continue
 rel=str(p.relative_to(O));x=dict(old.get(rel,{'filename':rel,'origin':'Retained installed dependency/vendor notices','npcId':None}));x.update(sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size,publicPreviewDecision='NOT_APPROVED');files.append(x)
q={**m,'profile':'full26','scope':'Exact privately staged full26 candidate, software notices repaired; UNKNOWN asset creation terms; no public approval','files':files};(O/'export-manifest.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
changed=[]
for x in files:
 rel=x['filename']
 if rel not in old or x['sha256']!=old[rel]['sha256']:changed.append(rel)
assert set(changed)=={'licenses/THIRD_PARTY_ADDITIONS.txt','portal.mjs','version.json','LICENSES.md'},changed
proof={'candidate':str(O.relative_to(R)),'manifestSHA256':hashlib.sha256((O/'export-manifest.json').read_bytes()).hexdigest(),'files':len(files),'changedOnly':changed,'compiledGameChanged':False,'allImagesAndSnapshotsUnchanged':True,'actualCatalog':26,'publicEligible':False,'terms':'UNKNOWN; public gate must reject'};(D/'FULL26_PACKAGE.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps(proof,indent=2))
