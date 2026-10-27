"""Local Phase3A review server; LAN exposure is explicit opt-in."""
from argparse import ArgumentParser
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
import os
p=ArgumentParser(description=__doc__);p.add_argument('--port',type=int,default=4378);p.add_argument('--lan',action='store_true');a=p.parse_args();os.chdir(Path(__file__).resolve().parent)
print(f'Open http://127.0.0.1:{a.port}/REVIEW.html',flush=True)
print('Phase3A living NPC review; human artistic approval pending. Physical devices NOT TESTED. Phase3B locked.',flush=True)
ThreadingHTTPServer(('0.0.0.0'if a.lan else'127.0.0.1',a.port),SimpleHTTPRequestHandler).serve_forever()
