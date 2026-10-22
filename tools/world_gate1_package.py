"""Package only the isolated graybox and explicit art-bible references, never old worlds."""
import hashlib,json,pathlib,shutil,zipfile
root=pathlib.Path(__file__).resolve().parents[1]
work=root/'.cache/world-gate1-package';shutil.rmtree(work,ignore_errors=True)
folder=work/'Korean-Arena-World-Gate1';site=folder/'3D-pharse5-'
shutil.copytree(root/'dist-world-gate1',site)
for name in ['juni.png','juni.json']:
 dest=site/'assets/juni'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(root/'public/assets/juni'/name,dest)
for name in ['GATE1_NORTH_REFERENCE.png','GATE1_STREET_NATIVE.png']:
 dest=site/'docs/gate1'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(root/'docs/gate1'/name,dest)
for f in (root/'docs/world-gate1').glob('*'):
 if f.is_file() and f.suffix not in ['.zip'] and f.name not in ['package.json','package-verification.json','github-verification.json']:
  dest=site/'docs/world-gate1'/f.name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,dest)
(folder/'start.py').write_text('''import argparse,http.server,pathlib
p=argparse.ArgumentParser();p.add_argument("--port",type=int,default=0);a=p.parse_args()
root=pathlib.Path(__file__).resolve().parent
handler=lambda *args,**kw:http.server.SimpleHTTPRequestHandler(*args,directory=str(root),**kw)
server=http.server.ThreadingHTTPServer(("127.0.0.1",a.port),handler)
print(f"http://127.0.0.1:{server.server_port}/3D-pharse5-/world-gate1.html",flush=True)
try:server.serve_forever()
except KeyboardInterrupt:server.server_close()
''')
(folder/'README.txt').write_text('KOREAN ARENA — NEW WORLD GATE 1 ONLY\nUnzip, run python3 start.py (Windows: py start.py), open the printed URL.\nWASD/arrows walk; Shift run; E inspect. Mobile landscape touch joystick.\nUse Overview link for zoning. All geometry is planning graybox, NOT final art.\nStyle-bible link includes old street/north reference images, not old-world runtime.\nNo Gate2/Gate3 work, no approval, no deployment.\n')
(folder/'fresh-plan.json').write_bytes((root/'assets-src/world-gate1/plan.json').read_bytes())
files=[]
for f in sorted(folder.rglob('*')):
 if f.is_file():files.append({'path':str(f.relative_to(folder)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
(folder/'files.json').write_text(json.dumps(files,indent=2)+'\n')
archive=root/'docs/world-gate1/WORLD_GATE1_PLAYABLE.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted(folder.rglob('*')):
  if f.is_file():z.write(f,str(f.relative_to(work)))
receipt={'files':len(files)+1,'bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'build':'dist-world-gate1','source':'New plan + unchanged Juni; two reference-only images in art bible','noOldWorldRuntime':True}
(root/'docs/world-gate1/package.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
