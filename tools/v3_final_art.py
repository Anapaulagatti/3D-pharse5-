"""Actual pinned Forge processing of retained V3 host art; never invokes a provider/generator."""
from pathlib import Path
import json,hashlib,subprocess,sys,os,shutil
from PIL import Image
R=Path(__file__).resolve().parents[1];S=R/'assets-src/v3-final';C=R/'.cache/v3-final';F=Path(os.environ.get('SPRITE_FORGE_ROOT','/workspace/tooling-cache/agent-sprite-forge'));C.mkdir(parents=True,exist_ok=True)
def write(p,j):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(script,*args):
 cmd=[sys.executable,str(script),*map(str,args)];r=subprocess.run(cmd,cwd=R,env=dict(os.environ,FORGE_MAX_PAID_REQUESTS='0'),capture_output=True,text=True);p=S/'commands.json';j=json.loads(p.read_text())if p.exists()else[];j.append({'command':cmd,'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr});write(p,j);print(Path(script).name,r.returncode,flush=True)
 if r.returncode:raise RuntimeError(r.stdout+r.stderr)
def extract():
 assert subprocess.check_output(['git','-C',str(F),'rev-parse','HEAD'],text=True).strip()=='5324342fdfab72430f4e9604f3fe427009f8596d'
 specs=json.loads((S/'specs.json').read_text());native=C/'native-input';native.mkdir(exist_ok=True);rows=[]
 for name,items in specs.items():
  boxfile=S/f'boxes/{name}.json';write(boxfile,{'schema':'forge-crop-boxes/v1','items':[{'id':k,'box':b}for k,b,_,_ in items]});out=S/f'keyed/{name}'
  if not out.exists():
   layout=['--auto-boxes','--auto-box-gap',0,'--labels',','.join(k for k,_,_,_ in items)] if name in ['jeju','urban'] else ['--boxes-file',boxfile]
   run(F/'skills/generate2dmap/scripts/extract_prop_pack.py','--input',S/f'raw/{name}.png',*layout,'--output-dir',out,'--component-mode','all','--min-component-area',1,'--despill-radius',3,'--alpha-hygiene','both','--reject-edge-touch','--max-dropped-fraction','0.01')
  for key,box,target,axis in items:
   im=Image.open(out/key/'prop.png');b=im.getbbox();h=target if axis=='height'else round((b[3]-b[1])*target/(b[2]-b[0]));frames=C/f'frames/{key}';frames.mkdir(parents=True,exist_ok=True);shutil.copyfile(out/key/'prop.png',frames/'000.png');finish=C/f'finish/{key}-{h}'
   if not finish.exists():run(F/'skills/video2dsprite/scripts/finish_frames.py','hd','--frames',frames,'--output-dir',finish,'--target-height',h,'--display-sizes','1x','--role','prop','--clip',key)
   shutil.copyfile(finish/'frames/000.png',native/f'{key}.png');rows.append({'id':key,'raw':f'raw/{name}.png','sourceBox':box,'nativeRecipe':{axis:target},'art_source':'host_image'})
 write(S/'native-recipes.json',rows)
 #9material source panels, measured418px cells, real strict terrain extractor.
 im=Image.open(S/'raw/terrain.png').convert('RGBA');w,h=im.size;assert w==h and w%3==0;n=w//3;stack=Image.new('RGBA',(n,n*9))
 names=['forest','grass','sand','basalt','paver','concrete','asphalt','deep-water','shallow-water']
 for i in range(9):x=i%3*n;y=i//3*n;stack.paste(im.crop((x,y,x+n,y+n)),(0,i*n))
 stack.save(S/'terrain-source-rows.png');out=S/'terrain-extracted'
 args=[]
 for i,name in enumerate(names):args+=['--terrain-row',f'{name}={i}']
 if not out.exists():run(F/'skills/generate2dmap/scripts/extract_terrain_tiles.py','--input',S/'terrain-periodic-rows.png','--rows',9,'--cols',1,*args,'--tile-size',128,'--background-mode','opaque','--edge-policy','seamless','--strict-qc','--prompt',S/'terrain-prompt.txt','--output-dir',out)
 for name in names:shutil.copyfile(out/f'{name}-1.png',native/f'terrain-{name}.png')
def palette():
 native=C/'native-input';pal=S/'palette'
 if not pal.exists():run(F/'skills/generate2dsprite/scripts/palette_tool.py','build','--input',native,'--base',R/'assets-src/seoul-production/palette/palette.json','--colors',255,'--balance','--name','Korean Arena heritage + contemporary locked palette','--output-dir',pal)
 quant=C/'quantized'
 if not quant.exists():run(F/'skills/generate2dsprite/scripts/palette_tool.py','apply','--input',native,'--palette',pal/'palette.json','--orphans',0,'--output-dir',quant)
 rows=json.loads((S/'native-recipes.json').read_text());(S/'props').mkdir(exist_ok=True);(S/'terrain').mkdir(exist_ok=True)
 for row in rows:
  im=Image.open(quant/f'{row["id"]}.png').convert('RGBA');im=im.crop(im.getbbox());a=Image.new('RGBA',(im.width+4,im.height+4));a.paste(im,(2,2));dest=S/f'props/{row["id"]}.png';a.save(dest);row.update(image=str(dest.relative_to(S)),size=list(a.size),anchor=[a.width//2,a.height-2],sha256=sha(dest))
 for p in quant.glob('terrain-*.png'):shutil.copyfile(p,S/'terrain'/p.name.removeprefix('terrain-'))
 write(S/'props.json',rows);base=json.loads((R/'assets-src/seoul-production/palette/palette.json').read_text());new=json.loads((pal/'palette.json').read_text());assert [c['hex']for c in new['colors'][:len(base['colors'])]]==[c['hex']for c in base['colors']]
 print(json.dumps({'finishedProps':len(rows),'terrain':len(list((S/'terrain').glob('*.png'))),'lockedBaseColors':len(base['colors']),'totalColors':len(new['colors'])}))
if __name__=='__main__':
 {'extract':extract,'palette':palette}[sys.argv[1]]()
