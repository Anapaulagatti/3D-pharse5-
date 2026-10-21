from map_pipeline import *
from PIL import Image
A=SOURCE/'art';S=FORGE/'skills/generate2dsprite/scripts'
run(FORGE/'skills/generate2dmap/scripts/extract_prop_pack.py','--input',SOURCE/'originals/fences.png','--rows','1','--cols','2','--labels','campus-fence,park-fence','--grid-rounding','nearest','--background-mode','native_alpha','--component-mode','all','--alpha-hygiene','none','--art-source','host_image','--output-dir',A/'fences-extracted')
raw=A/'fences-native-raw';raw.mkdir(exist_ok=True)
for k in ['campus-fence','park-fence']:
 im=Image.open(A/'fences-extracted'/k/'prop.png').convert('RGBA');im=im.crop(im.getbbox());ratio=min(140/im.width,44/im.height);size=[round(im.width*ratio),round(im.height*ratio)];scaled=im.resize(size,Image.Resampling.NEAREST);canvas=Image.new('RGBA',(144,48));canvas.paste(scaled,((144-size[0])//2,46-size[1]));canvas.save(raw/(k+'.png'))
run(S/'palette_tool.py','build','--input',raw,'--colors','96','--name','V9 original park campus infrastructure','--output-dir',A/'fences-palette')
run(S/'palette_tool.py','apply','--palette',A/'fences-palette/palette.json','--input',raw,'--output-dir',A/'fences-finished','--alpha-threshold','128')
write(SOURCE/'originals/fences-provenance.json',{'route':'host image_gen','model':None,'estimateUsd':None,'reference':'art/shops-finished/new-bakery.png','sha256':sha(SOURCE/'originals/fences.png'),'purpose':'Original two distinct low-boundary modules, replacing unsuitable maritime symbol in park/campus; no old art deleted'})
