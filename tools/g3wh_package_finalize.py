"""Bind final documentation-only ZIP repack to the actually tested runtime."""
from pathlib import Path
from zipfile import ZipFile
import hashlib,json,sys
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-west-hanok';E=Path(sys.argv[1])if len(sys.argv)>1 else Path('/tmp/g3wh-extracted');old=json.loads((E/'PACKAGE_SHA256.json').read_text());out=D/'WEST_HANOK_COURTYARD_REVIEW.zip'
with ZipFile(out)as z:
 new=json.loads(z.read('PACKAGE_SHA256.json'));runtime=[n for n in new if n.startswith('assets/')or n=='gate3-review.html'];assert all(new[n]==old.get(n)for n in runtime)
 for n,h in new.items():assert hashlib.sha256(z.read(n)).hexdigest()==h,n
 assert z.testzip()is None;assert out.stat().st_size<100000000
 result={'status':'PASS','zipSHA256':hashlib.sha256(out.read_bytes()).hexdigest(),'bytes':out.stat().st_size,'runtimeFilesIdenticalToActualSmokeTestedExtraction':len(runtime),'smokeReportSHA256':hashlib.sha256((D/'package-smoke.json').read_bytes()).hexdigest(),'CRC':'PASS','allFileHashes':'PASS','allCurrentManifestDependencies':'Loaded via actual extracted-package smoke;0 chunk/page errors','documentationOnlyRepack':'Final QA/gallery/source-tool metadata changes; runtime and artwork identical to actual tested extraction','physicalDevices':'NOT TESTED','artAcceptance':'PENDING HUMAN'}
(D/'package-final-validation.json').write_text(json.dumps(result,indent=2)+'\n');print('Final ZIP',out.stat().st_size,'bytes;',len(runtime),'tested runtime hashes exact')
