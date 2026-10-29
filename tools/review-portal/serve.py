"""Authenticated, allowlisted staging origin. TLS must terminate at a trusted proxy."""
import argparse,os,json,hashlib,hmac,base64
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from urllib.parse import unquote,urlsplit

def main():
 p=argparse.ArgumentParser();p.add_argument('--root',default='.cache/review-portal');p.add_argument('--port',type=int,default=4490);p.add_argument('--base',default='/');a=p.parse_args()
 if not a.base.startswith('/')or not a.base.endswith('/')or'..'in a.base:raise SystemExit('Invalid base')
 root=Path(a.root).resolve();manifest=json.loads((root/'export-manifest.json').read_text());allowed={x['filename']:x for x in manifest['files']};allowed['export-manifest.json']={}
 user=os.environ.get('REVIEW_USER','');password=os.environ.get('REVIEW_PASSWORD','')
 if not user or len(password)<16 or ':'in user:raise SystemExit('Set REVIEW_USER and REVIEW_PASSWORD (>=16 characters); never write credentials to static files.')
 expected=('Basic '+base64.b64encode((user+':'+password).encode()).decode()).encode()
 for name,row in allowed.items():
  file=root/name
  if file.is_symlink()or not file.resolve().is_relative_to(root):raise SystemExit('Unsafe exported file')
  if row and hashlib.sha256(file.read_bytes()).hexdigest()!=row['sha256']:raise SystemExit('Manifest integrity failure: '+name)
 class Handler(SimpleHTTPRequestHandler):
  def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(root),**kwargs)
  def log_message(self,*args):pass # never log credentials/query/saves
  def authorized(self):
   if not hmac.compare_digest(self.headers.get('Authorization','').encode(),expected):
    self.send_response(401);self.send_header('WWW-Authenticate','Basic realm="Korean Pixel Town Private Review", charset="UTF-8"');self.send_header('Cache-Control','no-store');self.end_headers();return False
   url=urlsplit(self.path);requested=unquote(url.path)
   if not requested.startswith(a.base):self.send_error(404);return False
   self.path='/'+requested[len(a.base):]+(('?'+url.query)if url.query else'')
   name=unquote(urlsplit(self.path).path).lstrip('/')
   if not name or name.endswith('/'):name+='index.html'
   if '..'in Path(name).parts or name not in allowed:self.send_error(404);return False
   return True
  def do_GET(self):
   if self.authorized():super().do_GET()
  def do_HEAD(self):
   if self.authorized():super().do_HEAD()
  def copyfile(self,source,outputfile):
   try:super().copyfile(source,outputfile)
   except (BrokenPipeError,ConnectionResetError):pass # ordinary canceled browser transfer
  def list_directory(self,path):self.send_error(404)
  def end_headers(self):
   self.send_header('Cache-Control','private, no-cache, must-revalidate');self.send_header('X-Content-Type-Options','nosniff');self.send_header('Referrer-Policy','no-referrer');self.send_header('X-Robots-Tag','noindex, nofollow, noarchive');self.send_header('X-Frame-Options','SAMEORIGIN');super().end_headers()
 print(f'Authenticated local origin: http://127.0.0.1:{a.port}/ — NOT a deployed public link. TLS reverse proxy required for remote use.',flush=True)
 ThreadingHTTPServer(('127.0.0.1',a.port),Handler).serve_forever()
if __name__=='__main__':main()
