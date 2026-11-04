import sys
from pathlib import Path
import json,hashlib,zipfile,shutil,sys
R=Path.cwd();D=R/'docs/phase3bd-final-quality';O=R/sys.argv[1];m=json.loads((O/'export-manifest.json').read_text());names=[r['filename']for r in m['files']]+['export-manifest.json'];assert len(names)==len(set(names))
for row in m['files']:assert hashlib.sha256((O/row['filename']).read_bytes()).hexdigest()==row['sha256'],row['filename']
z=D/'PHASE3BD_FINAL_QUALITY_REVIEW.zip';E=R/('.cache/phase3bd-final-quality-extracted-'+hashlib.sha256((O/'export-manifest.json').read_bytes()).hexdigest()[:8])
assert not E.exists(),'Preserve prior extraction or use a fresh path'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=6)as archive:
 for name in names:archive.write(O/name,name)
with zipfile.ZipFile(z)as archive:
 assert archive.testzip()is None
 assert len(archive.infolist())==len(names)
 archive.extractall(E)
for name in names:assert hashlib.sha256((E/name).read_bytes()).hexdigest()==hashlib.sha256((O/name).read_bytes()).hexdigest(),name
proof={'status':'CRC / SHA256 / EXTRACTION PASS; browser launch pending','zip':str(z.relative_to(R)),'sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'bytes':z.stat().st_size,'regularFiles':len(names),'manifestSHA256':hashlib.sha256((O/'export-manifest.json').read_bytes()).hexdigest(),'sourceCommit':m['gameCommit'],'candidate':str(O.relative_to(R)),'extracted':str(E.relative_to(R)),'publicExposure':'PENDING_EXACT_OWNER_APPROVAL','physicalDevices':'NOT TESTED'}
(D/'PACKAGE_PROOF.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps(proof,indent=2))
