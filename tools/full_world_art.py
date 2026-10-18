"""Process retained host-generated Korea art through pinned Forge; never generates/API."""
from pathlib import Path
import json,hashlib,subprocess,sys,os,shutil
from PIL import Image
R=Path(__file__).resolve().parents[1];S=R/'assets-src/full-world';C=R/'.cache/full-world';F=Path(os.environ.get('SPRITE_FORGE_ROOT','/workspace/tooling-cache/agent-sprite-forge'))
C.mkdir(parents=True,exist_ok=True)
def write(p,j):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(script,*args):
 cmd=[sys.executable,str(script),*map(str,args)];r=subprocess.run(cmd,cwd=R,env=dict(os.environ,FORGE_MAX_PAID_REQUESTS='0'),capture_output=True,text=True);p=S/'commands.json';j=json.loads(p.read_text())if p.exists()else[];j.append({'command':cmd,'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr});write(p,j);print(Path(script).name,r.returncode,flush=True)
 if r.returncode:raise RuntimeError(r.stdout+r.stderr)
def process(name,specs):
 assert subprocess.check_output(['git','-C',str(F),'rev-parse','HEAD'],text=True).strip()=='5324342fdfab72430f4e9604f3fe427009f8596d'
 raw=S/f'raw/{name}.png';boxes=S/f'boxes/{name}.json';write(boxes,{'schema':'forge-crop-boxes/v1','items':[{'id':k,'box':box}for k,box,_,_ in specs]});out=S/f'keyed/{name}'
 if not out.exists():run(F/'skills/generate2dmap/scripts/extract_prop_pack.py','--input',raw,'--boxes-file',boxes,'--output-dir',out,'--component-mode','all','--min-component-area',1,'--despill-radius',3,'--alpha-hygiene','both','--reject-edge-touch','--max-dropped-fraction','0.01')
 manifest=[];native=C/f'native-{name}';native.mkdir(exist_ok=True)
 for label,box,target,axis in specs:
  im=Image.open(out/label/'prop.png');b=im.getbbox();height=target if axis=='height'else round((b[3]-b[1])*target/(b[2]-b[0]));frames=C/f'frames/{label}';frames.mkdir(parents=True,exist_ok=True);shutil.copyfile(out/label/'prop.png',frames/'000.png');finish=C/f'finish/{label}-{height}'
  if not finish.exists():run(F/'skills/video2dsprite/scripts/finish_frames.py','hd','--frames',frames,'--output-dir',finish,'--target-height',height,'--display-sizes','1x','--role','prop','--clip',label)
  shutil.copyfile(finish/'frames/000.png',native/f'{label}.png');manifest.append({'id':label,'raw':str(raw.relative_to(S)),'nativeRecipe':{axis:target}})
 quant=C/f'quantized-{name}'
 if not quant.exists():run(F/'skills/generate2dsprite/scripts/palette_tool.py','apply','--input',native,'--palette',R/'assets-src/seoul-production/palette/palette.json','--orphans',0,'--output-dir',quant)
 for row in manifest:
  im=Image.open(quant/f'{row["id"]}.png').convert('RGBA');im=im.crop(im.getbbox());a=Image.new('RGBA',(im.width+4,im.height+4));a.paste(im,(2,2));dest=S/f'props/{row["id"]}.png';dest.parent.mkdir(exist_ok=True);a.save(dest);row.update(image=str(dest.relative_to(S)),size=list(a.size),anchor=[a.width//2,a.height-2],sha256=sha(dest),art_source='host_image')
 write(S/f'{name}-props.json',manifest)
if __name__=='__main__':
 name=sys.argv[1]
 specs=json.loads((S/'specs.json').read_text())[name]
 process(name,specs)
