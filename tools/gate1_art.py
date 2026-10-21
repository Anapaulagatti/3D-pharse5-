"""Finish new support sprites; main architecture/ground keep source pixels1:1."""
from pathlib import Path
import json,subprocess,shutil,hashlib
from PIL import Image
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate1';C=R/'.cache/gate1';F=Path('/workspace/tooling-cache/agent-sprite-forge/skills');N=S/'native';N.mkdir(exist_ok=True);log=[]
def run(*cmd):
 p=subprocess.run(list(map(str,cmd)),cwd=R,capture_output=True,text=True);log.append(dict(command=list(map(str,cmd)),exit=p.returncode,stdout=p.stdout,stderr=p.stderr));(S/'processing-log.json').write_text(json.dumps(log,indent=2)+'\n');assert p.returncode==0,p.stderr or p.stdout
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for name,height in [('bench-front',48),('bench-back',48),('light',190),('tree-planter',52),('bikes',68),('flowerbox',48)]:
 source=C/'furniture-extracted-custom'/name;out=C/('finish-'+name)
 run('python3',F/'video2dsprite/scripts/finish_frames.py','hd','--frames',source,'--output-dir',out,'--target-height',height,'--anchor','feet','--loop-policy','oneshot','--display-sizes','1x','--strict')
 files=list((out/'frames').glob('*.png'));assert len(files)==1
 shutil.copy2(files[0],N/(name+'.png'))
shutil.copy2(S/'originals/street-foundation.png',N/'street-foundation.png')
run('python3',F/'generate2dsprite/scripts/palette_tool.py','build','--input',N,'--colors','255','--balance','--name','Muneum-original-street','--output-dir',C/'palette255')
run('python3',F/'generate2dsprite/scripts/palette_tool.py','apply','--palette',C/'palette255/palette.json','--input',N,'--alpha-threshold','128','--output-dir',C/'palette-finished')
for f in(C/'palette-finished').glob('*.png'):shutil.copy2(f,N/f.name)
shutil.copy2(C/'palette255/palette.json',S/'palette.json')
rows=[]
for f in N.glob('*.png'):
 im=Image.open(f).convert('RGBA');assert set(im.getchannel('A').get_flattened_data())<={0,255};rows.append(dict(path=str(f.relative_to(S)),sha256=sha(f),size=im.size,colors=len(im.convert('RGB').getcolors(9999999)),source='originals/street-foundation.png'if f.stem=='street-foundation'else'originals/furniture.png',resized=False if f.stem=='street-foundation'else'Forge uniform support-prop finish to declared size; not major architecture'))
(S/'native-provenance.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(dict(nativeImages=len(rows),architectureSize=Image.open(N/'street-foundation.png').size,architectureSpatialScale=1)))
