"""Serve the illustrated3pilot review locally;LAN is explicit opt-in."""
from argparse import ArgumentParser
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
import os
p=ArgumentParser(description=__doc__);p.add_argument('--port',type=int,default=4388);p.add_argument('--lan',action='store_true');a=p.parse_args();os.chdir(Path(__file__).resolve().parent);print(f'Open http://127.0.0.1:{a.port}/REVIEW.html',flush=True);print('3illustratedpilot ART APPROVAL PENDING;11remaining/Phase3B LOCKED. Physicaldevices NOTTESTED.',flush=True);ThreadingHTTPServer(('0.0.0.0'if a.lan else'127.0.0.1',a.port),SimpleHTTPRequestHandler).serve_forever()
