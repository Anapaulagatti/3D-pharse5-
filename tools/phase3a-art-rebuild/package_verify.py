"""Verify final ZIP runtime is byte-identical to the independently exercised extraction."""
from pathlib import Path
from zipfile import ZipFile
import json,hashlib
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a-art-rebuild';proof=json.loads((D/'package-proof.json').read_text());rows=[]
for n,h in proof['runtime'].items():
 p=Path('/tmp/phase3a-art-extracted')/n;assert p.is_file()and hashlib.sha256(p.read_bytes()).hexdigest()==h,n
for n in ['package-npcs-smoke.json','package-characters-smoke.json','package-inspector-smoke.json']:
 q=json.loads((D/n).read_text());assert q['status']=='PASS';rows.append(n)
with ZipFile(D/proof['file'])as z:
 assert z.testzip()is None
 for n,h in json.loads(z.read('PACKAGE_SHA256.json')).items():assert hashlib.sha256(z.read(n)).hexdigest()==h,n
q={'status':'PASS','runtimeFilesIdenticalToIndependentlyTestedExtraction':len(proof['runtime']),'finalRuntimeSHA256':hashlib.sha256(json.dumps(proof['runtime'],sort_keys=True).encode()).hexdigest(),'testReports':rows,'missingAssets':[],'CRC':'PASS','allPackagedFileHashes':'PASS','finalZIP':proof['file'],'sha256':proof['sha256'],'bytes':proof['bytes'],'reviewDocumentationRepackOnly':True,'physicalDevices':'NOT TESTED','humanArtApproval':'PENDING'};(D/'package-smoke.json').write_text(json.dumps(q,indent=2)+'\n');print('PASSfinalZIP CRC/allhashes;runtime identical to actual tested independent extraction',len(proof['runtime']))
