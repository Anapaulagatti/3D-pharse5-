"""Build private local review packages, no deployment and no source regeneration."""
from pathlib import Path
import shutil,json,hashlib,zipfile
R=Path(__file__).resolve().parents[1];D=R/'docs/gate2';cache=R/'.cache/gate2/packages';cache.mkdir(parents=True,exist_ok=True)
rows=[]
for name,ids in [('A',['a','transition']),('B',['b','station','transition']),('C',['c'])]:
 root=cache/name
 if root.exists():shutil.rmtree(root)
 app=root/'3D-pharse5-';shutil.copytree(R/'dist-gate2',app)
 shutil.copytree(R/'public/assets/juni',app/'assets/juni')
 assets=app/'assets/gate2';assets.mkdir(parents=True)
 catalog=json.loads((R/'public/assets/gate2/catalog.json').read_text());(assets/'catalog.json').write_text(json.dumps([c for c in catalog if c['id'] in ids],indent=2)+'\n')
 for id in ids:shutil.copytree(R/'public/assets/gate2'/id,assets/id)
 (root/'start.py').write_text('''from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import os,sys
os.chdir(Path(__file__).resolve().parent)
port=int(sys.argv[1]) if len(sys.argv)>1 else 8062
print(f"Open http://127.0.0.1:{port}/3D-pharse5-/gate2-review.html",flush=True)
ThreadingHTTPServer(("127.0.0.1",port),SimpleHTTPRequestHandler).serve_forever()
''')
 (root/'README.txt').write_text(f'''GATE 2 / slice {name} / human artistic approval pending
Run: python3 start.py
Open: http://127.0.0.1:8062/3D-pharse5-/gate2-review.html?scene={ids[0]}
Only a local static server; no network install, no public deployment.
WASD/arrows move, Shift runs, E explores, Space greets; mobile landscape joystick + buttons.
Canvas is native 1:1; screenshot URLs append &native&overview.
Includes: {', '.join(ids)}. Juni atlas unchanged. No QA hook on normal entry.
Jeju native-scale reservation FAIL: localized proposal only, approved map unchanged.
B deliberately retains approved Muneum artwork; station is new supporting study.
This package does not unlock Gate3 or integrate/replace the full world.
''')
 manifest=[dict(path=str(p.relative_to(root)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(root.rglob('*')) if p.is_file()]
 (root/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
 out=D/f'{name}_PLAYABLE.zip'
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,6) as z:
  for p in sorted(root.rglob('*')):
   if p.is_file():z.write(p,str(p.relative_to(root)))
 with zipfile.ZipFile(out) as z:assert z.testzip() is None
 rows.append(dict(slice=name,scenes=ids,path=str(out.relative_to(R)),bytes=out.stat().st_size,sha256=hashlib.sha256(out.read_bytes()).hexdigest(),zipCRC='PASS'))
(D/'packages.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows))
