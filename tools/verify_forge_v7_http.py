from pathlib import Path
import sys,runpy,os,json,subprocess,threading
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
R=Path.cwd();C=R/'.cache/v7-world';F=Path('/workspace/tooling-cache/agent-sprite-forge/skills/generate2dmap/scripts');sys.path.insert(0,str(F));mod=runpy.run_path(str(F/'build_scene_preview.py'),run_name='forge_module')
out=R/'docs/v7-world/quality/forge-scene-http';out.mkdir(parents=True,exist_ok=True)
class Handler(SimpleHTTPRequestHandler):
 def do_GET(self):
  if self.path=='/favicon.ico':self.send_response(204);self.end_headers()
  else:super().do_GET()
server=ThreadingHTTPServer(('127.0.0.1',4213),partial(Handler,directory=str(C/'forge-scene-preview-verified')));threading.Thread(target=server.serve_forever,daemon=True).start()
config={'url':'http://127.0.0.1:4213/preview.html','screen':str(out/'preview.png'),'debug':str(out/'debug.png'),'timeoutMs':96000}
env=dict(os.environ,PLAYWRIGHT_BROWSERS_PATH=str(C/'forge-browser'),FORGE_SCENE_VERIFY=json.dumps(config));r=subprocess.run(['node','-'],input=mod['_VERIFY_SCRIPT'],text=True,capture_output=True,env=env,timeout=120);server.shutdown();(out/'stdout.txt').write_text(r.stdout);(out/'stderr.txt').write_text(r.stderr);j=json.loads(r.stdout.strip().splitlines()[-1]);(out/'raw-result.json').write_text(json.dumps(j,indent=2)+'\n');assert r.returncode==0 and not j.get('skipped'),j
assert not j.get('pageErrors')and not j.get('consoleErrors')and not j.get('failure')and not j.get('error'),j
assert not j.get('requests'),j['requests'];assert j['assets']['loaded']==j['assets']['total']and not j['assets']['failed'];assert j['routes']['ok']is True
assert j['ysort']['status']=='pass';assert any(k['free']for k in j['keyboard'])and all((k['moved']>1e-6)==bool(k['free'])for k in j['keyboard'])
(out/'summary.json').write_text(json.dumps({'status':'PASS','method':'Unmodified upstream _VERIFY_SCRIPT on original Forge export served over local HTTP because host forbids file://. No checks removed.','routes':len(j['routes']['results']),'allRoutesOK':True,'assets':j['assets'],'ysort':j['ysort'],'errors':[]},indent=2)+'\n');print('Forge official HTTP runtime verification PASS',len(j['routes']['results']))
