"""Narrow, retained-image Forge processing; no generators/APIs/setup side effects."""
from pathlib import Path
import json, os, sys, subprocess, shutil, hashlib
from PIL import Image

R=Path(__file__).resolve().parents[1]
S=R/'assets-src/stage-b-polish'
F=Path(os.environ.get('SPRITE_FORGE_ROOT','/workspace/tooling-cache/agent-sprite-forge'))
C=R/'.cache/stage-b-polish'
C.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,data):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,indent=2)+'\n')
def run(script,*args):
    cmd=[sys.executable,str(F/script),*map(str,args)]
    p=subprocess.run(cmd,cwd=R,env=dict(os.environ,FORGE_MAX_PAID_REQUESTS='0'),capture_output=True,text=True)
    log=S/'commands.json';rows=json.loads(log.read_text())if log.exists()else[]
    rows.append(dict(command=cmd,exit=p.returncode,stdout=p.stdout,stderr=p.stderr));write(log,rows)
    print(json.dumps(dict(tool=Path(script).name,exit=p.returncode)),flush=True)
    if p.returncode:raise RuntimeError(p.stdout+p.stderr)

if __name__=='__main__':
    assert subprocess.check_output(['git','-C',str(F),'rev-parse','HEAD'],text=True).strip()=='5324342fdfab72430f4e9604f3fe427009f8596d'
    if not (S/'terrain').exists():
        run(Path('skills/generate2dmap/scripts/extract_terrain_tiles.py'),'--input',S/'raw/terrain.png','--output-dir',S/'terrain','--rows',3,'--cols',2,'--terrain-row','academy=0','--terrain-row','workshop=1','--terrain-row','museum=2','--tile-size',128,'--resampler','lanczos','--background-mode','opaque','--prompt',S/'raw/terrain.prompt.txt','--strict-qc')
    if not (S/'verge').exists():
        run(Path('skills/generate2dmap/scripts/extract_terrain_tiles.py'),'--input',S/'raw/verge.png','--output-dir',S/'verge','--rows',2,'--cols',2,'--grid-rounding','nearest','--cell-shape','crop-square','--terrain-row','soil=0','--terrain-row','turf=1','--tile-size',128,'--resampler','lanczos','--background-mode','opaque','--prompt',S/'raw/verge.prompt.txt','--strict-qc')
    labels=['polish-folio','polish-bamboo','polish-tools','polish-chart','polish-stele','polish-flowers']
    if not (S/'keyed').exists():
        run(Path('skills/generate2dmap/scripts/extract_prop_pack.py'),'--input',S/'raw/courtyard-kit.png','--rows',2,'--cols',3,'--labels',','.join(labels),'--output-dir',S/'keyed','--component-mode','all','--min-component-area',1,'--despill-radius',3,'--alpha-hygiene','both','--reject-edge-touch','--max-dropped-fraction','0.01')
    native=C/'native';native.mkdir(exist_ok=True)
    for label,width in zip(labels,[96,64,88,100,68,64]):
        source=S/f'keyed/{label}/prop.png';im=Image.open(source);b=im.getbbox();height=round((b[3]-b[1])*width/(b[2]-b[0]))
        frames=C/f'frames/{label}';frames.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,frames/'000.png')
        target=C/f'finished/{label}'
        if not target.exists():run(Path('skills/video2dsprite/scripts/finish_frames.py'),'hd','--frames',frames,'--output-dir',target,'--target-height',height,'--display-sizes','1x','--role','prop','--clip',label)
        shutil.copyfile(target/'frames/000.png',native/f'{label}.png')
    quant=C/'quantized'
    if not quant.exists():run(Path('skills/generate2dsprite/scripts/palette_tool.py'),'apply','--input',native,'--palette',R/'assets-src/seoul-production/palette/palette.json','--orphans',0,'--output-dir',quant)
    manifest=[]
    for label in labels:
        im=Image.open(quant/f'{label}.png').convert('RGBA');im=im.crop(im.getbbox());out=Image.new('RGBA',(im.width+4,im.height+4));out.paste(im,(2,2))
        dest=S/f'props/{label}.png';dest.parent.mkdir(exist_ok=True);out.save(dest)
        manifest.append(dict(id=label,image=str(dest.relative_to(S)),sha256=sha(dest),size=list(out.size),anchor=[out.width//2,out.height-2],art_source='host_image',palette='../seoul-production/palette/palette.json'))
    write(S/'props.json',manifest)
    print('Targeted six materials / six small props processed; visual/runtime review still required.')
