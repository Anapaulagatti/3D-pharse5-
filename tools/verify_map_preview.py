"""Run Forge's unmodified scene verifier via authorized local HTTP, not file://.

The cloud browser blocks file URLs. This adapts only transport and Chromium
selection; route, keyboard, asset and pixel/Y-sort checks are exactly Forge's.
The actor in THIS diagnostic is Forge's marker, not Juni or Phaser evidence.
"""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
import threading, subprocess, os, json, sys, hashlib, importlib.util, argparse
ap=argparse.ArgumentParser();ap.add_argument('--bundle',default='assets-src/gwanghwamun/map-bundle.json');ap.add_argument('--cache-dir',default='.cache/gwanghwamun');ap.add_argument('--output-dir',default='docs/gwanghwamun');ap.add_argument('--max-bytes',type=int,default=16000000);a=ap.parse_args()
R=Path(__file__).resolve().parents[1];C=R/a.cache_dir;Q=R/a.output_dir;Q.mkdir(parents=True,exist_ok=True);C.mkdir(parents=True,exist_ok=True);B=R/a.bundle
F=Path(os.environ.get('SPRITE_FORGE_ROOT','/workspace/tooling-cache/agent-sprite-forge'))/'skills/generate2dmap/scripts'
preview=C/'forge-final-preview'
if not preview.exists():subprocess.run([sys.executable,str(F/'build_scene_preview.py'),'--bundle',str(B),'--output-dir',str(preview),'--actor-height','80','--max-bytes',str(a.max_bytes),'--strict'],check=True)
sys.path.insert(0,str(F));spec=importlib.util.spec_from_file_location('forge_scene',F/'build_scene_preview.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
adapter=C/'chromium-selection.cjs';adapter.write_text("""const Module=require('node:module');const orig=Module._load;
Module._load=function(name,...args){const m=orig.call(this,name,...args);if((name==='playwright'||name==='playwright-core')&&m.chromium&&!m.chromium.__local){const launch=m.chromium.launch.bind(m.chromium);m.chromium.launch=o=>launch({...o,executablePath:process.env.PIXEL_CHROMIUM_PATH||'/usr/bin/chromium',args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader',...(o?.args??[])]});m.chromium.__local=true;}return m;};
""")
class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path=='/favicon.ico':self.send_response(204);self.end_headers()
        else:super().do_GET()
    def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(preview)));threading.Thread(target=server.serve_forever,daemon=True).start()
config={'url':f'http://127.0.0.1:{server.server_port}/preview.html','screen':str(C/'forge-screen.png'),'debug':str(C/'forge-debug.png'),'timeoutMs':60000}
try:
    result=subprocess.run(['node','-'],input=m._VERIFY_SCRIPT,text=True,capture_output=True,timeout=90,env=dict(os.environ,NODE_PATH=str(R/'node_modules'),NODE_OPTIONS=f'--require {adapter}',FORGE_SCENE_VERIFY=json.dumps(config)))
    data=json.loads(result.stdout.strip().splitlines()[-1])
finally:server.shutdown();server.server_close()
checks={'no_errors':not any(data.get(k)for k in ['pageErrors','consoleErrors','failure','error']), 'no_external_requests':not data.get('requests'), 'assets':data.get('assets',{}).get('loaded')==data.get('assets',{}).get('total') and not data.get('assets',{}).get('failed'), 'keyboard':bool(data.get('keyboard')) and all((x['moved']>0)==x['free'] for x in data.get('keyboard',[])), 'routes':data.get('routes',{}).get('ok') is True, 'y_sort':data.get('ysort',{}).get('status')=='pass'}
report={'status':'PASS' if all(checks.values())else'FAIL','method':'Unmodified official Sprite Forge _VERIFY_SCRIPT over HTTP. Only installed Chromium selection adapted; default CLI file:// verification failed because browser policy blocks that transport. Marker actor, not Juni/Phaser.','official_verifier_sha256':hashlib.sha256(m._VERIFY_SCRIPT.encode()).hexdigest(),'bundle_sha256':hashlib.sha256(B.read_bytes()).hexdigest(),'checks':checks,'result':data}
(Q/'forge-http-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':report['status'],'checks':checks,'routes':len(data.get('routes',{}).get('results',[]))}))
assert all(checks.values()),report
