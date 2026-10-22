"""Build a portable private-review package, including the unmodified approved prototype."""
from pathlib import Path
import json, shutil, zipfile, hashlib
R=Path(__file__).resolve().parents[1];build=R/'dist-gate3';D=R/'docs/gate3a'
for kind in ['world','district']:
 manifest=json.loads((R/f'public/assets/gate3/{kind}/manifest.json').read_text())
 paths=[f'assets/gate3/{kind}/manifest.json',manifest['overview']]
 for c in manifest['chunks']:paths.extend([c['image'],c['mask']])
 paths.extend(o['image'] for o in manifest['objects'])
 for name in paths:
  target=build/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/'public'/name,target)
for name in ['juni.png','juni.json']:
 target=build/'assets/juni'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/'public/assets/juni'/name,target)
# Keep the prior package as a byte-identical nested archive: no rebundling its artwork/runtime.
p=build/'approved-prototype';p.mkdir(exist_ok=True)
shutil.copy2(R/'docs/gate25-station-planters/GATE25_STATION_PLANTERS_REVIEW.zip',p/'GATE25_APPROVED.zip')
(build/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>G3-A private review</title><h1>G3-A foundation</h1><p>Engineering terrain is not finished artwork. Station world-registration needs review.</p><ul><li><a href="gate3-review.html">World foundation</a></li><li><a href="gate3-review.html?scene=district">Approved district cache laboratory</a></li><li><a href="gate3-review.html?entry=north">Native northern entry</a></li><li><a href="gate3-review.html?entry=jeju">Native Jeju entry</a></li><li><a href="approved-prototype/GATE25_APPROVED.zip">Unmodified approved Gate2.5 package (unzip separately)</a></li><li><a href="DEVICE_CHECKLIST.md">Physical-device checklist</a></li></ul>')
(build/'START_REVIEW.txt').write_text('Private review only. Requires Python3.\nRun: python3 -m http.server 4261 --bind 127.0.0.1\nOpen http://127.0.0.1:4261/\nDo not open HTML with file://. No public deployment.\nFor a trusted private Wi-Fi device test only: --bind 0.0.0.0; use host private LAN address, then stop server after review.\nThe original approved prototype archive is unchanged in approved-prototype/.\n')
shutil.copy2(D/'DEVICE_CHECKLIST.md',build/'DEVICE_CHECKLIST.md')
proof=build/'review-data';proof.mkdir(exist_ok=True)
for name in ['REPORT.md','PROVENANCE.md','route-audit.json','chunk-generation-proof.json','preservation-and-native-proof.json','QA.json','controls-report.json','DEVICE_CHECKLIST.md','registration-conflict.png']:
 shutil.copy2(D/name,proof/name)
shutil.copy2(R/'assets-src/gate3/production-plan-v1.json',proof/'production-plan-v1.json')
sourcePaths=list((R/'src/gate3').rglob('*'))+[R/'gate3.vite.config.ts',R/'gate3-review.html',R/'src/engine/JuniMotion.ts',R/'src/engine/Joystick.ts',R/'src/gate2/style.css',R/'src/gate2/SessionMetrics.ts',R/'src/gate2/TourStops.ts',R/'tools/gate3_assets.py']
(build/'BUILD_SOURCES_SHA256.json').write_text(json.dumps({str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(sourcePaths) if p.is_file()},indent=2)+'\n')
files=sorted(x for x in build.rglob('*') if x.is_file() and x.name!='PACKAGE_SHA256.json')
(build/'PACKAGE_SHA256.json').write_text(json.dumps({str(p.relative_to(build)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2)+'\n')
out=D/'G3A_FOUNDATION_REVIEW.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(build.rglob('*')):
  if p.is_file():z.write(p,str(p.relative_to(build)))
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None
 for name,h in json.loads(z.read('PACKAGE_SHA256.json')).items():assert hashlib.sha256(z.read(name)).hexdigest()==h
(D/'package-proof.json').write_text(json.dumps(dict(file=out.name,bytes=out.stat().st_size,sha256=hashlib.sha256(out.read_bytes()).hexdigest(),zipCRC='PASS',perFileSha256='PASS',originalPrototypeSha256=hashlib.sha256((p:=R/'docs/gate25-station-planters/GATE25_STATION_PLANTERS_REVIEW.zip').read_bytes()).hexdigest()),indent=2)+'\n')
print(out, out.stat().st_size)
