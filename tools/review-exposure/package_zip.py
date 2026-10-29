"""One independently runnable PRIVATE restricted package, never a clearance claim."""
from pathlib import Path
import zipfile,json,hashlib,tempfile
R=Path.cwd();S=R/'.cache/exposure20-private';D=R/'docs/review-exposure';O=R/'.cache/phase3b-a-contemporary20-PRIVATE-terms-blocked.zip';m=json.loads((S/'export-manifest.json').read_text());prefix='KoreanPixelTown-20NPC-PrivateReview/'
start='''from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from pathlib import Path
import base64,secrets
root=Path(__file__).resolve().parent
password=secrets.token_urlsafe(18)
expected='Basic '+base64.b64encode(('review:'+password).encode()).decode()
class PrivateHandler(SimpleHTTPRequestHandler):
 def do_GET(self):
  if self.headers.get('Authorization')!=expected:
   self.send_response(401);self.send_header('WWW-Authenticate','Basic realm="Private review"');self.end_headers();return
  super().do_GET()
 def do_HEAD(self):
  if self.headers.get('Authorization')!=expected:
   self.send_response(401);self.send_header('WWW-Authenticate','Basic realm="Private review"');self.end_headers();return
  super().do_HEAD()
server=ThreadingHTTPServer(('127.0.0.1',0),partial(PrivateHandler,directory=str(root)))
print('PRIVATE review only. Creation terms UNKNOWN; NOT eligible for public upload.')
print('Open http://127.0.0.1:'+str(server.server_port)+'/3D-pharse5-review/')
print('Username: review; one-session password: '+password)
print('WASD / Shift on desktop. Landscape joystick on mobile emulation. Ctrl+C stops server.')
try:server.serve_forever()
except KeyboardInterrupt:server.server_close()
'''
readme='PRIVATE LOCAL REVIEW — NOT PUBLIC-ELIGIBLE\n\n20 real contemporary fictional NPCs; six era-inspired characters, old videos and all-26 snapshots excluded. Canonical 26-NPC project unchanged.\n\nExtract, run python3 start.py (Windows: py start.py), then open the printed local URL and enter the session password. Python3 required; no Node/npm/install or online asset download. This is not a published GitHub Pages URL.\n\nCreation-account/terms evidence remains UNKNOWN. Do not upload this package or assets publicly. 12 playable characters, 28 cosmetics and world pixels preserved; legacy game state isolated from v0.5. Physical Android/iPhone NOT TESTED.\n'
if O.exists():raise SystemExit('Do not overwrite a prior package')
with zipfile.ZipFile(O,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6)as z:
 z.writestr(prefix+'start.py',start);z.writestr(prefix+'README.txt',readme)
 for rel in [x['filename']for x in m['files']]+['export-manifest.json']:z.write(S/rel,prefix+'3D-pharse5-review/'+rel)
with zipfile.ZipFile(O)as z:
 assert z.testzip()is None
 with tempfile.TemporaryDirectory(prefix='restricted20-extract-',dir='/tmp')as t:
  z.extractall(t);T=Path(t)/prefix/'3D-pharse5-review'
  for row in m['files']:assert hashlib.sha256((T/row['filename']).read_bytes()).hexdigest()==row['sha256']
proof={'file':str(O.relative_to(R)),'bytes':O.stat().st_size,'sha256':hashlib.sha256(O.read_bytes()).hexdigest(),'manifestSHA256':hashlib.sha256((S/'export-manifest.json').read_bytes()).hexdigest(),'CRC':'PASS zipfile.testzip','extractionAndAllFileHashes':'PASS','launch':'Pending extracted-package smoke','publicEligible':False,'actualNPCs':20,'terms':'UNKNOWN; no public upload permitted'};(D/'PRIVATE_PACKAGE_PROOF.json').write_text(json.dumps(proof,indent=2)+'\n');print(proof['bytes'],proof['sha256'])
