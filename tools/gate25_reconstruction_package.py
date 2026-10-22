from pathlib import Path
import shutil,json,hashlib,zipfile
R=Path(__file__).resolve().parents[1];root=R/'.cache/gate25-reconstruction/package';D=R/'docs/gate25-reconstruction'
if root.exists():shutil.rmtree(root)
app=root/'3D-pharse5-';shutil.copytree(R/'dist-gate2',app);shutil.copytree(R/'public/assets/gate2',app/'assets/gate2');shutil.copytree(R/'public/assets/juni',app/'assets/juni')
(root/'start.py').write_text('''from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
import argparse,os
p=argparse.ArgumentParser();p.add_argument('--lan',action='store_true');p.add_argument('--port',type=int,default=8065);args=p.parse_args()
os.chdir(Path(__file__).resolve().parent)
host='0.0.0.0' if args.lan else '127.0.0.1'
print(f"Open http://{'COMPUTER_LAN_IP' if args.lan else host}:{args.port}/3D-pharse5-/gate2-review.html?scene=district-reconstruction",flush=True)
print('Gate2.5 private test only / Gate3 locked / Ctrl-C stops the server',flush=True)
ThreadingHTTPServer((host,args.port),SimpleHTTPRequestHandler).serve_forever()
''')
(root/'README.txt').write_text('''GATE2.5 RECONSTRUCTED DISTRICT / HUMAN ART REVIEW PENDING / Gate3 LOCKED
Run python3 start.py and open the printed URL. For a physical phone on the same trusted Wi-Fi run python3 start.py --lan and substitute your computer's LAN IP. No public deployment.
Choose CURRENT reconstruction for the reconstructed environment / three native chunks / complete owned crates and bollards; prior polish is REJECTED history; C Jeju for4-stop tour at50% with distinct coast/oreum views and quiet gutter controls. Previous scenes retained as history.
WASD/arrows; Shift run; E explore; mobile joystick/Run/Explore.
Scenic: drag/pinch, Full scene, Start Tour. Tour: Pause/Resume, Skip landmark, Return to Juni. Paused tour permits manual camera exploration. Movement intent cancels auto camera; Return never teleports Juni. Reduced motion uses static selection. Regular follow remains native1:1.
Options (...) > Export test report downloads real client/viewport/raw update timing/chunk diagnostics; user must explicitly identify physical device. Emulation is not physical validation.
District retains3 bounded native ground chunks, adjacent prefetch, no repeat requests; not general full-world streaming. Shared environmental pavement/road/garden reconstruction surrounds retained facades at both joins, original facades/Juni/coordinates preserved. Tour controls collapse after2.4s; visible landmark Controls restores, or tap scene. Reduced motion/focus keeps controls visible.
Jeju bridge/mainland are labeled technical geometry, not final production bridge art. Water between landing areas is blocked. No train/ferry gameplay.
Read MOBILE_CHECKLIST.md, DEVICE_TESTING.md and REPORT.md. Human UX/visual review and physical acceptance pending. STOP / no Gate3, merge or public deployment.
''')
shutil.copy2(R/'docs/gate25/DEVICE_TESTING.md',root/'DEVICE_TESTING.md')
for n in ['REPORT.md','browser-qa.json','camera-pan.json','foreground-qa.json','evidence-checks.json','preservation.json','source-and-collision.json','VISUAL_INSPECTION.md','diagnosis.json','validation.json']:shutil.copy2(D/n,root/n)
(root/'REPORT.md').write_text((root/'REPORT.md').read_text().replace('(package.json)','(MANIFEST.json)').replace('(package-qa.json)','(https://github.com/Anapaulagatti/3D-pharse5-/blob/art-gate/gate2-three-slices/docs/gate25-reconstruction/package-qa.json)'))
(root/'MOBILE_CHECKLIST.md').write_text((D/'MOBILE_CHECKLIST.md').read_text().replace('../gate25/DEVICE_TESTING.md','DEVICE_TESTING.md'))
files=[dict(path=str(p.relative_to(root)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())for p in sorted(root.rglob('*'))if p.is_file()];(root/'MANIFEST.json').write_text(json.dumps(files,indent=2)+'\n')
out=D/'GATE25_RECONSTRUCTION_PLAYABLE.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,6)as z:
 for p in sorted(root.rglob('*')):
  if p.is_file():z.write(p,str(p.relative_to(root)))
with zipfile.ZipFile(out)as z:
 assert z.testzip()is None;ex=R/'.cache/gate25-reconstruction/extracted'
 if ex.exists():shutil.rmtree(ex)
 z.extractall(ex)
for row in files:assert hashlib.sha256((ex/row['path']).read_bytes()).hexdigest()==row['sha256']
(D/'package.json').write_text(json.dumps(dict(path=str(out.relative_to(R)),bytes=out.stat().st_size,sha256=hashlib.sha256(out.read_bytes()).hexdigest(),crc='PASS',manifest='PASS'),indent=2)+'\n');print('PASS Gate2.5 ZIP / extracted manifest')
