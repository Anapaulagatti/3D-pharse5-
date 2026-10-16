"""Process retained source pixels with pinned Forge; NEVER generate media or call APIs."""
from pathlib import Path
import json,subprocess,sys,os,shutil,hashlib
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parents[1];S=R/'assets-src/seoul-production';C=R/'.cache/production';F=Path(os.environ.get('SPRITE_FORGE_ROOT','/workspace/tooling-cache/agent-sprite-forge'))
C.mkdir(parents=True,exist_ok=True)
def write(p,j):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(script,*a):
 cmd=[sys.executable,str(script),*map(str,a)];r=subprocess.run(cmd,cwd=R,env=dict(os.environ,FORGE_MAX_PAID_REQUESTS='0'),capture_output=True,text=True)
 file=S/'commands.json';log=json.loads(file.read_text()) if file.exists() else [];log.append({'command':cmd,'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr});write(file,log)
 print(json.dumps({'tool':Path(script).name,'exit':r.returncode,'output':str(a[-1]) if a else ''}),flush=True)
 if r.returncode:raise RuntimeError(r.stdout+r.stderr)
def separators(values):
 groups=[]
 for x in values:
  if not groups or x>groups[-1][-1]+1:groups.append([int(x)])
  else:groups[-1].append(int(x))
 return groups
def extract_studies():
 specs=[('bible-institutions',['gate-study','academy-study','workshop-study','museum-study','art-study','pavilion-study'],[232,384,244,292,292,192],3,2),('bible-civil',['bookshop-study','stationery-study','teahouse-study','craft-study','home-u-study','home-l-study','home-two-study','home-well-study'],[200,192,240,200,192,240,232,184],3,3)]
 native=C/'study-native';native.mkdir(exist_ok=True)
 for name,labels,widths,cols,rows in specs:
  im=Image.open(S/f'raw/{name}.png').convert('RGB');ar=np.array(im);white=np.all(ar>245,axis=2);vx=separators(np.where(np.mean(white,axis=0)>.8)[0]);hy=separators(np.where(np.mean(white,axis=1)>.8)[0]);assert len(vx)==cols-1 and len(hy)==rows-1,(vx,hy)
  xsp=list(zip([0]+[g[-1]+1 for g in vx],[g[0] for g in vx]+[im.width]));ysp=list(zip([0]+[g[-1]+1 for g in hy],[g[0] for g in hy]+[im.height]))
  items=[]
  for i,label in enumerate(labels):
   x,x2=xsp[i%cols];y,y2=ysp[i//cols];x+=3;y+=3;x2-=3;y2-=3;items.append({'id':label,'box':[x,y,x2,y2]})
  boxes=S/f'studies/{name}-boxes.json';write(boxes,{'schema':'forge-crop-boxes/v1','sourceGridLinesMeasured':{'x':vx,'y':hy},'items':items})
  dest=S/f'studies/{name}'
  if not dest.exists():run(F/'skills/generate2dmap/scripts/extract_prop_pack.py','--input',S/f'raw/{name}.png','--boxes-file',boxes,'--output-dir',dest,'--component-mode','all','--min-component-area',1,'--despill-radius',3,'--alpha-hygiene','both','--reject-edge-touch','--max-dropped-fraction','0.01')
  for label,width in zip(labels,widths):
   source=dest/label/'prop.png';src=Image.open(source).convert('RGBA');bbox=src.getbbox();height=round((bbox[3]-bbox[1])*width/(bbox[2]-bbox[0]));frames=C/'study-frames'/label;frames.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,frames/'000.png');finished=C/'study-finished'/label
   if not finished.exists():run(F/'skills/video2dsprite/scripts/finish_frames.py','hd','--frames',frames,'--output-dir',finished,'--target-height',height,'--display-sizes','1x','--role','prop','--clip',label)
   shutil.copyfile(finished/'frames/000.png',native/f'{label}.png')
 if not (S/'studies/palette').exists():run(F/'skills/generate2dsprite/scripts/palette_tool.py','build','--input',native,'--colors',192,'--balance','--name','Living Seoul architecture studies','--output-dir',S/'studies/palette')
 if not (C/'study-quantized').exists():run(F/'skills/generate2dsprite/scripts/palette_tool.py','apply','--input',native,'--palette',S/'studies/palette/palette.json','--orphans',0,'--output-dir',C/'study-quantized')
 manifest=[]
 for path in sorted((C/'study-quantized').glob('*.png')):
  im=Image.open(path).convert('RGBA');im=im.crop(im.getbbox());canvas=Image.new('RGBA',(im.width+4,im.height+4));canvas.paste(im,(2,2));dest=S/'studies/native'/path.name;dest.parent.mkdir(exist_ok=True);canvas.save(dest);manifest.append({'id':path.stem,'image':str(dest.relative_to(S)),'size':list(canvas.size),'sha256':sha(dest),'artSource':'host_image','scope':'concept study ONLY; not final map production','relativeWorldScale':0.5})
 write(S/'studies/manifest.json',{'studies':manifest,'note':'Concepts placed at declared approximate world-relative scale; building/eave width recipes, not finished runtime footprint approval. Generated white panel rules were measured and excluded by actual Forge crop boxes; raw unchanged.'})
if __name__=='__main__':
 assert subprocess.check_output(['git','-C',str(F),'rev-parse','HEAD'],text=True).strip()=='5324342fdfab72430f4e9604f3fe427009f8596d'
 if '--studies' in sys.argv:extract_studies()

def extract_production():
 specs=[('gate',[('prod-gate',None,464)]),('academy-hall',[('prod-hall',None,640)]),('academy-wings',[('prod-study',[0,0,768,1024],176),('prod-library',[768,0,1536,1024],176)]),('workshop',[('prod-workshop',None,488)]),('museum-volume',[('prod-museum',None,584)]),('wall-kit',[('prod-wall',[0,0,745,535],160),('prod-wall-ns',[745,0,1000,535],48),('prod-service',[1000,0,1536,535],128),('prod-court-gate',[0,535,630,1024],144),('prod-doors',[630,535,940,1024],88),('prod-low-wall',[940,535,1536,1024],160)]),('science-kit',[('prod-armillary',[0,0,520,533],96),('prod-sundial',[520,0,1030,533],88),('prod-clock',[1030,0,1536,533],110),('prod-strategy',[0,533,570,1024],120),('prod-ship',[570,533,1040,1024],120),('prod-writing',[1040,533,1536,1024],100)])]
 native=C/'production-native';native.mkdir(exist_ok=True)
 metadata=[]
 for name,items in specs:
  raw=S/f'raw/{name}.png';size=Image.open(raw).size;boxes=S/f'boxes/{name}.json';write(boxes,{'schema':'forge-crop-boxes/v1','items':[{'id':label,'box':box or [0,0,*size]}for label,box,w in items]})
  dest=S/f'keyed/{name}'
  if not dest.exists():run(F/'skills/generate2dmap/scripts/extract_prop_pack.py','--input',raw,'--boxes-file',boxes,'--output-dir',dest,'--component-mode','all','--min-component-area',1,'--despill-radius',3,'--alpha-hygiene','both','--reject-edge-touch','--max-dropped-fraction','0.01')
  for label,box,width in items:
   source=dest/label/'prop.png';im=Image.open(source).convert('RGBA');b=im.getbbox();height=round((b[3]-b[1])*width/(b[2]-b[0]));frames=C/'production-frames'/label;frames.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,frames/'000.png');finished=C/'production-finished'/label
   if not finished.exists():run(F/'skills/video2dsprite/scripts/finish_frames.py','hd','--frames',frames,'--output-dir',finished,'--target-height',height,'--display-sizes','1x','--role','prop','--clip',label)
   shutil.copyfile(finished/'frames/000.png',native/f'{label}.png');metadata.append({'id':label,'raw':str(raw.relative_to(S)),'widthRecipe':width,'heightRecipe':height})
 if not (S/'palette').exists():run(F/'skills/generate2dsprite/scripts/palette_tool.py','build','--input',native,'--colors',192,'--balance','--name','Living Seoul production stone jade walnut slate','--output-dir',S/'palette')
 if not (C/'production-quantized').exists():run(F/'skills/generate2dsprite/scripts/palette_tool.py','apply','--input',native,'--palette',S/'palette/palette.json','--orphans',0,'--output-dir',C/'production-quantized')
 for item in metadata:
  im=Image.open(C/f'production-quantized/{item["id"]}.png').convert('RGBA');im=im.crop(im.getbbox());canvas=Image.new('RGBA',(im.width+4,im.height+4));canvas.paste(im,(2,2));dest=S/f'props/{item["id"]}.png';dest.parent.mkdir(exist_ok=True);canvas.save(dest);item.update(image=str(dest.relative_to(S)),size=list(canvas.size),sha256=sha(dest))
 write(S/'props.json',metadata)
if __name__=='__main__' and '--production' in sys.argv:extract_production()
