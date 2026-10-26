"""Copied to the review ZIP root; private local server by default."""
from argparse import ArgumentParser
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import os

parser = ArgumentParser(description=__doc__)
parser.add_argument('--lan', action='store_true', help='Allow private LAN device review')
parser.add_argument('--port', type=int, default=4300)
args = parser.parse_args()
os.chdir(Path(__file__).resolve().parent)
print(f'Open http://127.0.0.1:{args.port}/REVIEW.html')
print('Phase 1B four-character review candidate. Human art approval pending.')
print('Physical devices NOT TESTED. Phase 2 remains locked.')
ThreadingHTTPServer(('0.0.0.0' if args.lan else '127.0.0.1', args.port), SimpleHTTPRequestHandler).serve_forever()
