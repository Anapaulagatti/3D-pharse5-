from pathlib import Path
import json,sys,hashlib,zipfile,shutil
R=Path.cwd();S=Path(sys.argv[1]).resolve();D=R/'docs/phase3bb-hotfix';m=json.loads((S/'export-manifest.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert{r['filename']for r in m['files']}=={str(p.relative_to(S))for p in S.rglob('*')if p.is_file()and p!=S/'export-manifest.json'and '.git'not in p.parts}
for r in m['files']:assert sha(S/r['filename'])==r['sha256'],r['filename']
out=D/'PHASE3BB_REVIEW.zip';assert not out.exists(),'Never overwrite packaged artifact'
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 for r in m['files']:z.write(S/r['filename'],r['filename'])
 z.write(S/'export-manifest.json','export-manifest.json')
 z.writestr('START_REVIEW.txt','Private review candidate. Requires owner exact-manifest public exposure approval before Pages publication.\nExtract ZIP, open a terminal here and run:\npython3 -m http.server 4500 --bind 127.0.0.1\nOpen http://127.0.0.1:4500/ in a browser. Node/npm not required, no internet runtime dependency. Do not open via file://.\nHotfix evidence: http://127.0.0.1:4500/hotfix/\n')
extract=R/'.cache/phase3bb-zip-extracted';assert not extract.exists()
with zipfile.ZipFile(out)as z:
 assert z.testzip()is None;z.extractall(extract)
for r in m['files']:assert sha(extract/r['filename'])==r['sha256']
proof={'zip':str(out.relative_to(R)),'sha256':sha(out),'bytes':out.stat().st_size,'manifestSHA256':sha(S/'export-manifest.json'),'manifestFiles':len(m['files']),'archiveEntries':len(m['files'])+2,'crc':'PASS','extractionHashes':'PASS','extractRoot':str(extract.relative_to(R)),'launchSmoke':'PENDING','physicalDevices':'NOT TESTED'};(D/'PACKAGE_PROOF.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps(proof,indent=2))
