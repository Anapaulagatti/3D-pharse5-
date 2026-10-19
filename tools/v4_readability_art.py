"""Scoped original boundary kit; real Forge processing, no provider generation."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,shutil
from PIL import Image
R=Path(__file__).resolve().parents[1];S=R/'assets-src/v4-readability';C=R/'.cache/v4-readability';F=Path(os.environ.get('SPRITE_FORGE_ROOT','/workspace/tooling-cache/agent-sprite-forge'));C.mkdir(parents=True,exist_ok=True)
def write(p,j):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(script,*args):
 cmd=[sys.executable,str(script),*map(str,args)];r=subprocess.run(cmd,cwd=R,env=dict(os.environ,FORGE_MAX_PAID_REQUESTS='0'),capture_output=True,text=True)
 p=S/'commands.json';rows=json.loads(p.read_text())if p.exists()else[];rows.append({'command':cmd,'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr});write(p,rows);print(Path(script).name,r.returncode,flush=True)
 if r.returncode:raise RuntimeError(r.stdout+r.stderr)
def main():
 assert subprocess.check_output(['git','-C',str(F),'rev-parse','HEAD'],text=True).strip()=='5324342fdfab72430f4e9604f3fe427009f8596d'
 boxes=[('stone',[80,40,750,300],144),('hedge',[785,40,1475,300],144),('rail',[80,330,750,530],144),('park',[790,330,1470,530],144),('planter',[230,540,580,980],64),('sign',[940,535,1310,980],48)]
 write(S/'boxes.json',{'schema':'forge-crop-boxes/v1','items':[{'id':k,'box':b}for k,b,_ in boxes]})
 out=S/'extracted-props'
 if not out.exists():run(F/'skills/generate2dmap/scripts/extract_prop_pack.py','--input',S/'raw/boundaries.png','--boxes-file',S/'boxes.json','--output-dir',out,'--component-mode','all','--min-component-area',1,'--despill-radius',3,'--alpha-hygiene','both','--reject-edge-touch','--max-dropped-fraction','0.01')
 native=C/'native';native.mkdir(exist_ok=True);recipes=[]
 for key,box,width in boxes:
  im=Image.open(out/key/'prop.png');b=im.getbbox();height=round((b[3]-b[1])*width/(b[2]-b[0]));frames=C/f'frames-{key}';frames.mkdir(exist_ok=True);shutil.copyfile(out/key/'prop.png',frames/'000.png');finish=C/f'finish-{key}'
  if not finish.exists():run(F/'skills/video2dsprite/scripts/finish_frames.py','hd','--frames',frames,'--output-dir',finish,'--target-height',height,'--display-sizes','1x','--role','prop','--clip',key)
  shutil.copyfile(finish/'frames/000.png',native/f'{key}.png');(S/'finishing-qa').mkdir(exist_ok=True);shutil.copyfile(finish/'finish.json',S/f'finishing-qa/finish-{key}.json')
  recipes.append({'id':key,'sourceBox':box,'targetWidth':width,'targetHeight':height,'art_source':'host_image','finish':'actual Forge single still, not animation'})
 (S/'palette').mkdir(exist_ok=True);shutil.copyfile(R/'assets-src/v3-final/palette/palette.json',S/'palette/palette.json')
 q=C/'quantized'
 if not q.exists():run(F/'skills/generate2dsprite/scripts/palette_tool.py','apply','--input',native,'--palette',S/'palette/palette.json','--orphans',0,'--output-dir',q)
 (S/'props').mkdir(exist_ok=True)
 for row in recipes:
  im=Image.open(q/(row['id']+'.png')).convert('RGBA');im=im.crop(im.getbbox());p=S/'props'/('v4-'+row['id']+'.png');im.save(p);row.update(size=list(im.size),sha256=sha(p))
 write(S/'prop-recipes.json',recipes);print(recipes)
if __name__=='__main__':main()
