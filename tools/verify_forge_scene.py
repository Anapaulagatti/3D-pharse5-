"""Run unchanged upstream Forge browser program via HTTP + installed Chromium.
File-URL sandbox and browser discovery are host concerns; no route assertions modified.
"""
from map_pipeline import *
import runpy,time,threading,http.server,functools
M=FORGE/'skills/generate2dmap/scripts';source=SOURCE/'map/bundle.json';out=CACHE/('scene-'+sha(source)[:16])
if not out.exists():run(M/'build_scene_preview.py','--bundle',source,'--actor-height','55','--max-bytes','32000000','--output-dir',out)
sys.path.insert(0,str(M));upstream=runpy.run_path(str(M/'build_scene_preview.py'));program=upstream['_VERIFY_SCRIPT'];(out/'upstream-verifier.cjs').write_text(program)
# Only launch resolution is adapted; all original route/movement/Y-sort code is unchanged.
(out/'launch-host.cjs').write_text("const pw=require('playwright');const launch=pw.chromium.launch.bind(pw.chromium);pw.chromium.launch=(options)=>launch({...options,executablePath:'/usr/bin/chromium',args:['--no-sandbox','--disable-gpu-compositing']});\n")
class Handler(http.server.SimpleHTTPRequestHandler):
 def do_GET(self):
  if self.path=='/favicon.ico':self.send_response(204);self.end_headers();return
  super().do_GET()
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(out)));threading.Thread(target=server.serve_forever,daemon=True).start()
try:
 config={'url':f'http://127.0.0.1:{server.server_port}/preview.html','screen':str(out/'scene.png'),'debug':str(out/'debug.png'),'timeoutMs':120000};cmd=['node','--require',str(out/'launch-host.cjs'),str(out/'upstream-verifier.cjs')]
 result=subprocess.run(cmd,cwd=ROOT,env=dict(os.environ,FORGE_SCENE_VERIFY=json.dumps(config),NODE_PATH=str(ROOT/'node_modules')),capture_output=True,text=True,timeout=180)
 rows=json.loads((SOURCE/'forge-commands.json').read_text());rows.append({'command':cmd,'exit':result.returncode,'stdout':result.stdout,'stderr':result.stderr,'adapter':'HTTP URL + installed Chromium only; upstream verifier body unchanged'});write(SOURCE/'forge-commands.json',rows)
 data=json.loads(result.stdout.strip().splitlines()[-1]);write(out/'actual-browser-result.json',data)
 failed=data.get('failure')or data.get('skipped')or data.get('error')or not data.get('routes',{}).get('ok')or data.get('ysort',{}).get('status')!='pass'or any(data.get(k)for k in ['pageErrors','consoleErrors','requests'])
 for row in data.get('keyboard',[]):
  if row['free']and row['moved']<=0:failed=True
 proof={'status':'FAIL'if failed else'PASS','tool':'Real unchanged upstream build_scene_preview._VERIFY_SCRIPT over HTTP','toolSha256':sha(M/'build_scene_preview.py'),'sourceBundleSha256':sha(source),'launchAdapter':'Installed /usr/bin/chromium, CPU compositor, no physics/assertion edits','browser':data.get('browser'),'routeResults':data.get('routes'),'keyboard':data.get('keyboard'),'ysort':data.get('ysort'),'errors':{k:data.get(k)for k in ['failure','skipped','error','pageErrors','consoleErrors','requests']}}
 write(SOURCE/'scene-snapshot.json',proof);assert not failed,proof;print('Actual upstream Forge browser routes PASS',len(data['routes'].get('results',[])))
finally:server.shutdown();server.server_close()
