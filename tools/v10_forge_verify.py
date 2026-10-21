"""Run the unmodified pinned Forge browser verifier over HTTP with installed Chromium."""
import functools,hashlib,http.server,json,os,runpy,subprocess,sys,threading
from pathlib import Path
R=Path(__file__).resolve().parents[1];F=Path('/workspace/tooling-cache/agent-sprite-forge/skills/generate2dmap/scripts');O=R/os.environ.get('V10_FORGE_PREVIEW_DIR','.cache/v10-forge-preview')
sys.path.insert(0,str(F));up=runpy.run_path(str(F/'build_scene_preview.py'))
(O/'upstream-verifier.cjs').write_text(up['_VERIFY_SCRIPT'])
(O/'launch-host.cjs').write_text("const pw=require('playwright');const launch=pw.chromium.launch.bind(pw.chromium);pw.chromium.launch=options=>launch({...options,executablePath:'/usr/bin/chromium',args:['--no-sandbox','--disable-gpu-compositing']});\n")
class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path=='/favicon.ico':self.send_response(204);self.end_headers();return
        super().do_GET()
    def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(O)))
threading.Thread(target=server.serve_forever,daemon=True).start()
try:
    config=dict(url=f'http://127.0.0.1:{server.server_port}/preview.html',screen=str(O/'scene.png'),debug=str(O/'debug.png'),timeoutMs=120000)
    cmd=['node','--require',str(O/'launch-host.cjs'),str(O/'upstream-verifier.cjs')]
    result=subprocess.run(cmd,cwd=R,env=dict(os.environ,FORGE_SCENE_VERIFY=json.dumps(config),NODE_PATH=str(R/'node_modules')),capture_output=True,text=True,timeout=180)
    raw=dict(command=cmd,exit=result.returncode,stdout=result.stdout,stderr=result.stderr,upstreamScriptSha256=hashlib.sha256((F/'build_scene_preview.py').read_bytes()).hexdigest(),adapter='HTTP + Chromium launch only; unchanged route/keyboard/Y-sort assertions')
    target=R/'assets-src/v10-city/qa';target.mkdir(exist_ok=True)
    (target/'forge-browser-command.json').write_text(json.dumps(raw,indent=2)+'\n')
    data=json.loads(result.stdout.strip().splitlines()[-1]);(target/'scene-snapshot.json').write_text(json.dumps(data,indent=2)+'\n')
    assert result.returncode==0 and not any(data.get(k)for k in ['failure','error','skipped','pageErrors','consoleErrors','requests']),data
    assert data['routes']['ok'] and data['ysort']['status']=='pass',data
    assert all(not row['free']or row['moved']>0 for row in data['keyboard']),data
    print(json.dumps(dict(status='PASS',targets=len(data['routes']['results']),ysort=data['ysort']['status'])))
finally:server.shutdown();server.server_close()
