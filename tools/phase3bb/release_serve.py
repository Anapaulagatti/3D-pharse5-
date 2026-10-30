"""Serve the immutable play directory under existing E2E base, loopback only."""
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
root=Path('.cache/phase3bb-26-exposure-candidate/play').resolve()
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(root),**kwargs)
 def do_GET(self):
  prefix='/3D-pharse5-/'
  if not self.path.startswith(prefix):self.send_error(404);return
  self.path='/'+self.path[len(prefix):];super().do_GET()
ThreadingHTTPServer(('127.0.0.1',4502),Handler).serve_forever()
