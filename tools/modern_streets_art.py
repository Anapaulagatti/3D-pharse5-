"""Process the single original infrastructure kit through actual pinned Forge. Never generates."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,shutil
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parents[1];S=R/'assets-src/modern-streets';C=R/'.cache/modern-streets';F=Path(os.environ.get('SPRITE_FORGE_ROOT','/workspace/tooling-cache/agent-sprite-forge'))
C.mkdir(parents=True,exist_ok=True)
def write(p,j):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(script,*args):
 cmd=[sys.executable,str(script),*map(str,args)];r=subprocess.run(cmd,cwd=R,env=dict(os.environ,FORGE_MAX_PAID_REQUESTS='0'),capture_output=True,text=True)
 p=S/'commands.json';rows=json.loads(p.read_text())if p.exists()else[];rows.append({'command':cmd,'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr});write(p,rows);print(Path(script).name,r.returncode,flush=True)
 if r.returncode:raise RuntimeError(r.stdout+r.stderr)
def main():
 assert subprocess.check_output(['git','-C',str(F),'rev-parse','HEAD'],text=True).strip()=='5324342fdfab72430f4e9604f3fe427009f8596d'
 boxes=[('curb',[12,516,475,674],64),('tactile',[496,516,956,674],48),('grate',[984,512,1437,687],40),('crossing',[22,749,469,1057],64),('drain',[493,785,957,982],96),('cover',[1024,750,1385,1047],24)]
 write(S/'boxes.json',{'schema':'forge-crop-boxes/v1','items':[{'id':k,'box':b}for k,b,_ in boxes]})
 out=S/'extracted-props'
 if not out.exists():run(F/'skills/generate2dmap/scripts/extract_prop_pack.py','--input',S/'raw/infrastructure.png','--boxes-file',S/'boxes.json','--output-dir',out,'--component-mode','all','--min-component-area',1,'--despill-radius',3,'--alpha-hygiene','both','--reject-edge-touch','--max-dropped-fraction','0.01')
 native=C/'native';native.mkdir(exist_ok=True)
 recipes=[]
 for key,box,width in boxes:
  im=Image.open(out/key/'prop.png');b=im.getbbox();height=round((b[3]-b[1])*width/(b[2]-b[0]));frames=C/f'frames-{key}';frames.mkdir(exist_ok=True);shutil.copyfile(out/key/'prop.png',frames/'000.png');finish=C/f'finish-{key}'
  if not finish.exists():run(F/'skills/video2dsprite/scripts/finish_frames.py','hd','--frames',frames,'--output-dir',finish,'--target-height',height,'--display-sizes','1x','--role','prop','--clip',key)
  shutil.copyfile(finish/'frames/000.png',native/f'{key}.png');recipes.append({'id':key,'sourceBox':box,'targetWidth':width,'targetHeight':height,'art_source':'host_image','finish':'actual Forge single still, not animation'})
 sys.path.insert(0,str(F/'skills/generate2dmap/scripts'));import extract_terrain_tiles as e,forge_core
 raw=Image.open(S/'raw/infrastructure.png').convert('RGBA');stack=Image.new('RGBA',(128,384));terrain=[]
 for i,(name,box)in enumerate([('asphalt',[8,8,476,476]),('concrete',[491,8,959,476]),('paver',[974,8,1442,476])]):
  cell=raw.crop(box);best=None
  for size in range(468,198,-8):
   opts=list(range(0,469-size,8));opts+=([468-size]if 468-size not in opts else[])
   for y in opts:
    for x in opts:
     crop=(x,y,x+size,y+size);a=e.resize_tile(np.array(cell.crop(crop)),(128,128),resampler='lanczos',opaque=True,wrap=True)
     qa=[forge_core.edge_seam_report(a,a,gate=1.25),forge_core.edge_seam_report(a.transpose(1,0,2),a.transpose(1,0,2),gate=1.25)]
     if all(q['verdict']not in ['seam','duplicate_edge']and q['seam_ratio']<=1.12 for q in qa):best=(crop,a,qa);break
    if best:break
   if best:break
  assert best,name
  crop,a,qa=best;stack.paste(Image.fromarray(a),(0,i*128));terrain.append({'id':name,'sourceBox':[box[0]+crop[0],box[1]+crop[1],box[0]+crop[2],box[1]+crop[3]],'wrap':qa,'method':'Largest passing measured source crop and actual Forge wrap-aware resize; no threshold changes or painted RGB.'});print(name,crop,[q['seam_ratio']for q in qa],flush=True)
 stack.save(S/'terrain-periodic-rows.png');write(S/'terrain-crops.json',terrain)
 out=S/'terrain-extracted'
 if not out.exists():run(F/'skills/generate2dmap/scripts/extract_terrain_tiles.py','--input',S/'terrain-periodic-rows.png','--rows',3,'--cols',1,'--terrain-row','asphalt=0','--terrain-row','concrete=1','--terrain-row','paver=2','--tile-size',128,'--background-mode','opaque','--edge-policy','seamless','--strict-qc','--prompt',S/'prompts/infrastructure.txt','--output-dir',out)
 for name in ['asphalt','concrete','paver']:shutil.copyfile(out/f'{name}-1.png',native/f'terrain-{name}.png')
 q=C/'quantized'
 if not q.exists():run(F/'skills/generate2dsprite/scripts/palette_tool.py','apply','--input',native,'--palette',R/'assets-src/v3-final/palette/palette.json','--orphans',0,'--output-dir',q)
 for row in recipes:
  im=Image.open(q/(row['id']+'.png')).convert('RGBA');im=im.crop(im.getbbox());p=S/'overlays'/(row['id']+'.png');p.parent.mkdir(exist_ok=True);im.save(p);row.update(size=list(im.size),sha256=sha(p))
 write(S/'overlay-recipes.json',recipes)
 qa=[]
 for name in ['asphalt','concrete','paver']:
  p=S/'terrain'/(name+'.png');p.parent.mkdir(exist_ok=True);shutil.copyfile(q/f'terrain-{name}.png',p);a=np.array(Image.open(p).convert('RGBA'));tests=[forge_core.edge_seam_report(a,a,gate=1.25),forge_core.edge_seam_report(a.transpose(1,0,2),a.transpose(1,0,2),gate=1.25)]
  qa.append({'material':name,'tests':tests});assert all(t['verdict']not in ['seam','duplicate_edge']and t['seam_ratio']<=1.25 for t in tests),(name,tests)
 write(S/'post-palette-terrain-qa.json',qa)
 print('Finished6flush ground overlays/3strict swatches; existing255palette/Juni unchanged.')
if __name__=='__main__':main()
