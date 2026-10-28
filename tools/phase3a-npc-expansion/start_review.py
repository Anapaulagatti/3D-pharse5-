"""Serve the20NPC review locally; LAN access is explicit opt-in,never a public deployment."""
from argparse import ArgumentParser
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
import os
p=ArgumentParser(description=__doc__);p.add_argument('--port',type=int,default=4396);p.add_argument('--lan',action='store_true');a=p.parse_args();os.chdir(Path(__file__).resolve().parent);print(f'Open http://127.0.0.1:{a.port}/REVIEW.html',flush=True);print('Actual20/26NPC;6history/indexsourceBLOCKED;artistic approval pending;physicaldevicesNOTTESTED;Phase3BLOCKED.',flush=True);ThreadingHTTPServer(('0.0.0.0'if a.lan else'127.0.0.1',a.port),SimpleHTTPRequestHandler).serve_forever()
