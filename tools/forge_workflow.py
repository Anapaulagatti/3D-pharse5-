"""Run actual free Forge diagnostics/registration/clip/pixelQA. Never invokes media generation."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,subprocess,json,sys,uuid,hashlib
p=argparse.ArgumentParser();p.add_argument('--forge-root',default='/workspace/tooling-cache/agent-sprite-forge');a=p.parse_args();F=Path(a.forge_root);R=Path(__file__).resolve().parents[1];out=R/'.cache/forge-current'/uuid.uuid4().hex[:8];out.mkdir(parents=True);commands=[]
ref=subprocess.check_output(['git','-C',str(F),'rev-parse','HEAD'],text=True).strip();assert ref=='5324342fdfab72430f4e9604f3fe427009f8596d',ref
for skill in ['generate2dsprite','video2dsprite','generate2dmap','generate2dmedia','codeart2d']:assert (F/'skills'/skill/'SKILL.md').is_file()
def run(skill,script,args,expected=(0,)):
 cmd=[sys.executable,str(F/'skills'/skill/'scripts'/script)]+[str(s) for s in args];r=subprocess.run(cmd,cwd=R,capture_output=True,text=True);commands.append({'skill':skill,'script':script,'command':cmd,'exit_code':r.returncode,'stdout':r.stdout.strip(),'stderr':r.stderr.strip()});assert r.returncode in expected,(cmd,r.stdout,r.stderr);return r
run('generate2dmedia','forge_doctor.py',['--host-tools','image_gen','--json','--save',out/'doctor.json'])
run('generate2dmedia','route_media.py',['resolve','--kind','video'],(3,))
run('video2dsprite','video2dsprite.py',['doctor'])
run('generate2dmap','map_nav.py',['--help']) # Execution capability only; no new map/art requested.
for action in ['walk','run']:
 job=out/(action+'-job');reg=out/(action+'-registered')
 run('video2dsprite','prepare_i2v_input.py',['prepare','--master','assets-src/actors/hero/master-right.png','--action',action,'--output-dir',job,'--anchor','24,64','--canvas','48,68','--root','24,64','--scale','1','--pixel-art','--margin','0','--action-padding','0,0,0,0','--subject','original Korean Arena chibi courier with swept charcoal hair, celadon coat, coral scarf and satchel','--facing','right'])
 run('video2dsprite','register_clip.py',['apply','--job',job/'registration_job.json','--frames',R/f'.cache/actor-frames/hero/{action}/right','--output-dir',reg,'--resampler','nearest'])
 run('codeart2d','pixel_qa.py',['--input',str(reg/'frames/*.png'),'--palette','assets-src/actors/palette.json','--anchor','24,64','--onion','--scales','1,3','--bg','light,dark','--review',out/(action+'-review.png'),'--report',out/(action+'-qa.json')])
 for i,png in enumerate(sorted((reg/'frames').glob('*.png'))):
  from PIL import Image
  src=R/f'.cache/actor-frames/hero/{action}/right/{i:02d}.png';assert Image.open(png).tobytes()==Image.open(src).tobytes(),'Registration altered authored pixels'
# Use native registered source clips directly; no model/source regeneration.
m={'schema':'generate2dsprite.animation_clips.v2','frames':[],'anchor_px':[24,64],'art_source':'code','pixel_art':True,'sampling':'nearest','placeholder':False,'body_height_px':54,'clips':{}}
for action in ['walk','run']:
 ids=[]
 for i in range(12):ids.append(len(m['frames']));m['frames'].append({'name':f'{action}-{i}','file':str(R/f'.cache/actor-frames/hero/{action}/right/{i:02d}.png')})
 m['clips'][action]={'frames':ids,'ticks':2,'loop_policy':'cycle','role':'player','events':[{'at':0,'name':'step_r'},{'at':6,'name':'step_l'}]}
manifest=out/'clips-input.json';manifest.write_text(json.dumps(m,indent=2)+'\n')
run('generate2dsprite','build_animation_clips.py',['--manifest',manifest,'--output-dir',out/'clips','--preview-scale','3','--strict'])
for actor in ['sejong','jang','saimdang','yi']:
 run('codeart2d','pixel_qa.py',['--input',str(R/f'.cache/actor-frames/{actor}/walk/down/*.png'),'--palette','assets-src/actors/palette.json','--anchor','24,64','--onion','--scales','1,3','--bg','light,dark','--review',out/(actor+'-review.png'),'--report',out/(actor+'-qa.json')])
qa=[]
for f in out.glob('*-qa.json'):
 d=json.loads(f.read_text());qa.append({'file':f.name,'status':d['status'],'warn_or_fail':[c for c in d['checks'] if c['status'] in ['warn','fail']],'skipped':[c for c in d['checks'] if c['status']=='skipped'],'notProven':d.get('notProven',[])})
result={'status':'EXECUTED_PENDING_VISUAL_REVIEW','forge_commit':ref,'art_route':'Existing accepted master + authored native pixel frames; code-drawn, no image model. Video resolve exits3/no-route. No generation/billable request invoked.','commands':commands,'qa':qa,'reports_dir':str(out),'map_scope':'generate2dmap CLIhelp executed/capability inspected; no map generation because world preserved unchanged. Existing Tiled navigation validated separately.','dependency_limit':'resvg-py absent, not used by PNG pipelines.'}
(out/'usage.json').write_text(json.dumps(result,indent=2)+'\n');(R/'.cache/forge-latest.json').write_text(json.dumps({'folder':str(out)},indent=2)+'\n');print(json.dumps({'status':result['status'],'folder':str(out),'commands':len(commands),'qa':qa}))
