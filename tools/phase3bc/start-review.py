"""Offline local review launcher. Python3 only; no npm/download/account required."""
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from urllib.parse import urlsplit,unquote
import hashlib,json,argparse
root=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=4483);a=p.parse_args()
m=json.loads((root/'export-manifest.json').read_text());allowed={r['filename']for r in m['files']}|{'export-manifest.json'}
for row in m['files']:
 f=root/row['filename']
 if f.is_symlink()or not f.resolve().is_relative_to(root)or hashlib.sha256(f.read_bytes()).hexdigest()!=row['sha256']:raise SystemExit('Integrity failure: '+row['filename'])
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(root),**kwargs)
 def do_GET(self):
  name=unquote(urlsplit(self.path).path).lstrip('/')
  if not name or name.endswith('/'):name+='index.html'
  if '..'in Path(name).parts or name not in allowed:self.send_error(404);return
  super().do_GET()
 def list_directory(self,path):self.send_error(404)
 def log_message(self,*args):pass
print(f'PRIVATE LOCAL REVIEW: http://127.0.0.1:{a.port}/review/ — stop with Ctrl+C. Public Pages remains unchanged.',flush=True)
ThreadingHTTPServer(('127.0.0.1',a.port),Handler).serve_forever()
