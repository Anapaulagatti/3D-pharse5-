"""Actual terrain extraction and shared-palette finishing of original host swatches."""
from full_world_art import *
im=Image.open(S/'raw/terrain.png').convert('RGBA');w,h=im.size;assert w%2==0 and h%2==0
# The source2x2 contains four different materials, not two variants per row.
stack=Image.new('RGBA',(w//2,(h//2)*4))
for i,(x,y)in enumerate([(0,0),(w//2,0),(0,h//2),(w//2,h//2)]):stack.paste(im.crop((x,y,x+w//2,y+h//2)),(0,i*(h//2)))
stack.save(S/'terrain-source-rows.png')
out=S/'terrain-extracted'
if not out.exists():run(F/'skills/generate2dmap/scripts/extract_terrain_tiles.py','--input',S/'terrain-source-rows.png','--rows',4,'--cols',1,'--terrain-row','forest=0','--terrain-row','sand=1','--terrain-row','basalt=2','--terrain-row','brick=3','--tile-size',128,'--background-mode','opaque','--edge-policy','seamless','--strict-qc','--prompt',S/'prompts/terrain.txt','--output-dir',out)
native=C/'terrain-input';native.mkdir(exist_ok=True)
for name in ['forest','sand','basalt','brick']:shutil.copyfile(out/f'{name}-1.png',native/f'{name}.png')
quant=S/'terrain-native'
if not quant.exists():run(F/'skills/generate2dsprite/scripts/palette_tool.py','apply','--input',native,'--palette',R/'assets-src/seoul-production/palette/palette.json','--orphans',0,'--output-dir',quant)
