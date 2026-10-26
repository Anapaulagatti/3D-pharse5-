"""Local Phase2A review server. LAN exposure is explicitly opt-in."""
from argparse import ArgumentParser
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
import os
p=ArgumentParser(description=__doc__);p.add_argument('--port',type=int,default=4340);p.add_argument('--lan',action='store_true');args=p.parse_args();os.chdir(Path(__file__).resolve().parent)
print(f'Open http://127.0.0.1:{args.port}/REVIEW.html')
print('Phase2A six-character Studio review candidate. Physical devices NOT TESTED. Phase2B locked.')
ThreadingHTTPServer(('0.0.0.0'if args.lan else'127.0.0.1',args.port),SimpleHTTPRequestHandler).serve_forever()
