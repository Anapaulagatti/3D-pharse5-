"""Actual pinned Forge processing of retained original images; NO generation/API."""
from pathlib import Path
import os,json,sys,subprocess,shutil,hashlib
from PIL import Image
R=Path(__file__).resolve().parents[1];S=R/'assets-src/world-refinement';C=R/'.cache/world-refinement';C.mkdir(parents=True,exist_ok=True);F=Path(os.environ.get('SPRITE_FORGE_ROOT','/workspace/tooling-cache/agent-sprite-forge'))
def write(p,j):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(script,*args):
 cmd=[sys.executable,str(script),*map(str,args)];r=subprocess.run(cmd,cwd=R,env=dict(os.environ,FORGE_MAX_PAID_REQUESTS='0'),capture_output=True,text=True);file=S/'commands.json';rows=json.loads(file.read_text())if file.exists()else[];rows.append({'command':cmd,'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr});write(file,rows);print(json.dumps({'tool':Path(script).name,'exit':r.returncode}),flush=True)
 if r.returncode:raise RuntimeError(r.stdout+r.stderr)
if __name__=='__main__':
 assert subprocess.check_output(['git','-C',str(F),'rev-parse','HEAD'],text=True).strip()=='5324342fdfab72430f4e9604f3fe427009f8596d'
 specs=[('hall',[('rf-royal-hall',None,640,'width')]),('inner',[('rf-inner-gate',None,240,'width')]),('cafe',[('rf-cafe',None,360,'width')]),('court',[('rf-banner',[0,0,670,700],120,'width'),('rf-stone-lantern',[670,0,1254,700],64,'width'),('rf-exhibit',[0,700,650,1254],112,'width'),('rf-cafe-seating',[650,700,1254,1254],104,'width')]),('boundary',[('rf-scholar-wall',[0,0,985,543],144,'width'),('rf-scholar-return',[985,0,1448,543],176,'height'),('rf-work-rail',[0,543,985,1086],144,'width'),('rf-work-return',[985,543,1448,1086],160,'height')])]
 native=C/'native';native.mkdir(exist_ok=True);manifest=[]
 for name,items in specs:
  raw=S/f'raw/{name}.png';size=list(Image.open(raw).size);boxes=S/f'boxes/{name}.json';write(boxes,{'schema':'forge-crop-boxes/v1','note':'Measured complete separated object boxes, not assumed nominal grid; no clipped pixels repaired by cropping.','items':[{'id':label,'box':box or[0,0,*size]}for label,box,_,_ in items]});dest=S/f'keyed/{name}'
  if not dest.exists():run(F/'skills/generate2dmap/scripts/extract_prop_pack.py','--input',raw,'--boxes-file',boxes,'--output-dir',dest,'--component-mode','all','--min-component-area',1,'--despill-radius',3,'--alpha-hygiene','both','--reject-edge-touch','--max-dropped-fraction','0.01')
  for label,box,target,axis in items:
   source=dest/label/'prop.png';im=Image.open(source);b=im.getbbox();height=target if axis=='height'else round((b[3]-b[1])*target/(b[2]-b[0]));frames=C/f'frames/{label}';frames.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,frames/'000.png');finished=C/f'finished/{label}-{height}'
   if not finished.exists():run(F/'skills/video2dsprite/scripts/finish_frames.py','hd','--frames',frames,'--output-dir',finished,'--target-height',height,'--display-sizes','1x','--role','prop','--clip',label)
   shutil.copyfile(finished/'frames/000.png',native/f'{label}.png');manifest.append({'id':label,'raw':str(raw.relative_to(S)),'sizeRecipe':{axis:target},'heightRecipe':height})
 quant=C/('quantized-'+hashlib.sha256(''.join(sha(p)for p in sorted(native.glob('*.png'))).encode()).hexdigest()[:16])
 if not quant.exists():run(F/'skills/generate2dsprite/scripts/palette_tool.py','apply','--input',native,'--palette',R/'assets-src/seoul-production/palette/palette.json','--orphans',0,'--output-dir',quant)
 for item in manifest:
  im=Image.open(quant/f'{item["id"]}.png').convert('RGBA');im=im.crop(im.getbbox());canvas=Image.new('RGBA',(im.width+4,im.height+4));canvas.paste(im,(2,2));dest=S/f'props/{item["id"]}.png';dest.parent.mkdir(exist_ok=True);canvas.save(dest)
  ax=canvas.width//2
  if item['id']in ['rf-scholar-return','rf-work-return']:
   a=canvas.getchannel('A');pts=[x for y in range(canvas.height-10,canvas.height-2)for x in range(canvas.width)if a.getpixel((x,y))];ax=round(sum(pts)/len(pts))
  item.update(image=str(dest.relative_to(S)),size=list(canvas.size),anchor=[ax,canvas.height-2],sha256=sha(dest),art_source='host_image',palette='../seoul-production/palette/palette.json')
 write(S/'props.json',manifest);print('11new isolated props processed; inspect native scale and real Phaser before acceptance.')
