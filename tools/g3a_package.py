"""Portable targeted-registration review, with the immutable approved district package retained."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,shutil,hashlib
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3a-corrections';B=R/'dist-gate3'
for kind in ['world','district','registration']:
 p=json.loads((R/f'public/assets/gate3/{kind}/manifest.json').read_text());paths=[f'assets/gate3/{kind}/manifest.json',p['overview']]+[v for c in p['chunks'] for v in [c['image'],c['mask']]]+[o['image']for o in p['objects']]
 for name in paths:
  dest=B/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/'public'/name,dest)
for n in ['juni.png','juni.json']:
 dest=B/'assets/juni'/n;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/'public/assets/juni'/n,dest)
(B/'approved-prototype').mkdir(exist_ok=True);shutil.copy2(R/'docs/gate25-station-planters/GATE25_STATION_PLANTERS_REVIEW.zip',B/'approved-prototype/GATE25_APPROVED.zip')
(B/'index.html').write_text('''<!doctype html><meta charset="utf-8"><title>G3-A targeted registration review</title><h1>G3-A registration candidate</h1><p>Human approval pending. Existing full-size art only; grey surroundings are engineering geometry. No G3-B production artwork.</p><ul><li><a href="gate3-review.html?scene=registration">Limited registration proof / station</a></li><li><a href="gate3-review.html?scene=registration&entry=retail">Cafe, bookshop and learning</a></li><li><a href="gate3-review.html?scene=registration&entry=bakery">Proposed waterfront bakery</a></li><li><a href="gate3-review.html?scene=registration&entry=convenience">Proposed Namsan-approach convenience store</a></li><li><a href="gate3-review.html?scene=district">Unchanged native district / current engine</a></li><li><a href="gate3-review.html?scene=world">Unchanged approved world planning foundation</a></li><li><a href="approved-prototype/GATE25_APPROVED.zip">Byte-identical approved prototype archive</a></li><li><a href="DEVICE_CHECKLIST.md">Physical-device handoff</a></li></ul>''')
(B/'START_REVIEW.txt').write_text('Private review only. Python3: python3 -m http.server 4271 --bind 127.0.0.1\nOpen http://127.0.0.1:4271/\nFor a trusted private LAN device review only, bind0.0.0.0 and use the host private LAN address. Stop the server afterward. No public deployment.\nNative screenshots: add &native to a selected candidate entry. This changes framing only, not Juni or architecture scale.\nOptions: Export test report. Physical results require real recorded device evidence.\n')
shutil.copy2(D/'DEVICE_CHECKLIST.md',B/'DEVICE_CHECKLIST.md')
review=B/'review-data';review.mkdir(exist_ok=True)
for name in ['REPORT.md','REGISTRATION.md','PERFORMANCE.md','PROVENANCE.md','registration-proposal.json','static-validation.json','native-pixel-and-phase.json','QA.json','CURRENT_VS_PROPOSED.png','FOOTPRINT_COMPARISON.png','PIXEL_PHASE_AND_COLLISION.png','ENTRANCE_COORDINATES.md','DEVICE_CHECKLIST.md','spatial-conflicts.json','context-native-proof.json','performance-summary.json','culling-ablation.json','trace-summary.json','render-isolation.json','diagnostics-baseline.json','diagnostics-optimized.json','resilience-report.json','NATIVE_SOURCE_COMPARISON.png','historical-ref-proof.json','preserved-frame-proof.json']:
 shutil.copy2(D/name,review/name)
(B/'current').mkdir(exist_ok=True);shutil.copy2(R/'docs/current/G3A_TARGETED_CORRECTIONS.md',B/'current/G3A_TARGETED_CORRECTIONS.md')
sources=list((R/'src/gate3').rglob('*'))+[R/'gate3.vite.config.ts',R/'tools/g3a_registration.py',R/'src/engine/JuniMotion.ts',R/'src/engine/Joystick.ts',R/'src/gate2/SessionMetrics.ts',R/'src/gate2/style.css',R/'src/gate2/TourStops.ts']
(B/'BUILD_SOURCES_SHA256.json').write_text(json.dumps({str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in sources if p.is_file()},indent=2)+'\n')
(B/'PACKAGE_SHA256.json').write_text(json.dumps({str(p.relative_to(B)):hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted(B.rglob('*'))if p.is_file()and p.name!='PACKAGE_SHA256.json'},indent=2)+'\n')
out=D/'G3A_TARGETED_REVIEW.zip'
with ZipFile(out,'w',ZIP_DEFLATED,compresslevel=6)as z:
 for p in sorted(B.rglob('*')):
  if p.is_file():z.write(p,str(p.relative_to(B)))
with ZipFile(out)as z:
 assert z.testzip()is None
 for name,h in json.loads(z.read('PACKAGE_SHA256.json')).items():assert hashlib.sha256(z.read(name)).hexdigest()==h,name
 nested=hashlib.sha256(z.read('approved-prototype/GATE25_APPROVED.zip')).hexdigest();assert nested==hashlib.sha256((R/'docs/gate25-station-planters/GATE25_STATION_PLANTERS_REVIEW.zip').read_bytes()).hexdigest()
(D/'package-proof.json').write_text(json.dumps({'file':out.name,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'zipCRC':'PASS','packageSha256':'PASS','approvedPrototypeSha256':nested},indent=2)+'\n');print(out,out.stat().st_size)
