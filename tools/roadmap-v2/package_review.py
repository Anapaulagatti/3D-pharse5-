"""Reproduce a NEW private candidate only; preserve frozen671d267e unchanged. Do not rerun against approved artifacts."""
from pathlib import Path
import json,hashlib,zipfile,subprocess
R=Path.cwd();D=R/'docs/roadmap-v2';O=Path(__import__('os').environ.get('V2_CANDIDATE','/workspace/roadmap-v2-clean/.cache/roadmap-v2-review-final'));h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();m=json.loads((O/'export-manifest.json').read_text());names=[r['filename']for r in m['files']]+['export-manifest.json']
assert len(names)==len(set(names));assert max(r['bytes']for r in m['files'])<99*1024**2
for r in m['files']:assert h(O/r['filename'])==r['sha256']
assert not(O/'.git').exists(),'Never amend an existing frozen artifact; choose a fresh candidate folder'
subprocess.run(['git','init','-b','artifact/roadmap-v2-local'],cwd=O,check=True,stdout=subprocess.DEVNULL)
subprocess.run(['git','add','--all'],cwd=O,check=True)
subprocess.run(['git','-c','user.name=Codex','-c','user.email=codex@openai.com','commit','-m','Freeze isolated Roadmap V2 candidate; exact public exposure approval pending'],cwd=O,check=True,stdout=subprocess.DEVNULL)
artifact=subprocess.check_output(['git','rev-parse','HEAD'],cwd=O,text=True).strip()
z=D/'ROADMAP_V2_PLAYABLE_REVIEW.zip';E=O.parent/('roadmap-v2-extracted-'+h(O/'export-manifest.json')[:8]);assert not E.exists()
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as a:
 for n in names:a.write(O/n,n)
with zipfile.ZipFile(z)as a:
 assert a.testzip()is None;assert len(a.infolist())==len(names);a.extractall(E)
for n in names:assert h(E/n)==h(O/n),n
p={'status':'PASS ZIP CRC/SHA/EXTRACTION; HTTP_BROWSER_PENDING','sourceCommit':m['gameCommit'],'artifactCommit':artifact,'artifactLocation':str(O),'manifestSHA256':h(O/'export-manifest.json'),'manifestFiles':len(m['files']),'zipEntries':len(names),'zip':str(z.relative_to(R)),'zipSHA256':h(z),'zipBytes':z.stat().st_size,'payloadBytes':sum(r['bytes']for r in m['files']),'extracted':str(E),'publicExposure':'PENDING_EXACT_OWNER_APPROVAL','physicalDevices':'NOT TESTED','rollbackArtifact':'1a6e5a58a8fb515730e553a30980d2ffb7274da6'};(D/'PACKAGE_PROOF.json').write_text(json.dumps(p,indent=2)+'\n');print(json.dumps(p,indent=2))
