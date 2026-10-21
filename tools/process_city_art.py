"""Actual host-image provenance and Forge extraction/finish; no provider API."""
from map_pipeline import *
from PIL import Image
import shutil
A=SOURCE/'art';A.mkdir(exist_ok=True);M=FORGE/'skills/generate2dmap/scripts';S=FORGE/'skills/generate2dsprite/scripts'
write(SOURCE/'originals/provenance.json',{'route':'host image_gen','model':None,'estimateUsd':None,'priceNote':'Host tool does not expose model/price. No billable provider API route invoked.','grayboxGateCommit':'bb8c9e763923edb59e7e44d2127098468810e4fc','sources':[{'file':str(p.relative_to(SOURCE)),'sha256':sha(p),'prompt':f'prompts/{p.stem}.txt','size':list(Image.open(p).size)}for p in (SOURCE/'originals').glob('*.png')],'referenceArtwork':['assets-src/library/native/v3-station.png','assets-src/library/native/rf-cafe.png'],'uses':'Materials/source props only. No original screenshot/map input and no character/NPC generation.'})
# Measured source rows, not a falsely declared uniform animation grid.
write(A/'shop-boxes.json',{'props':[{'label':k,'source_box':box}for k,box in zip(['new-grocery','new-bakery','new-language','new-gallery'],[[0,0,670,640],[670,0,1341,640],[0,640,670,1173],[670,640,1341,1173]])]})
run(M/'extract_prop_pack.py','--input',SOURCE/'originals/shops.png','--boxes-file',A/'shop-boxes.json','--background-mode','native_alpha','--component-mode','all','--alpha-hygiene','none','--component-padding','4','--art-source','host_image','--output-dir',A/'shops-extracted')
# Native-size registration: one uniform scale per building, transparent256×224 canvas.
props={};raw=A/'shops-native-raw';raw.mkdir(exist_ok=True)
for k in ['new-grocery','new-bakery','new-language','new-gallery']:
 im=Image.open(A/'shops-extracted'/k/'prop.png').convert('RGBA');box=im.getbbox();im=im.crop(box);ratio=min(248/im.width,216/im.height);size=[round(im.width*ratio),round(im.height*ratio)];scaled=im.resize(size,Image.Resampling.NEAREST);canvas=Image.new('RGBA',(256,224));canvas.paste(scaled,((256-size[0])//2,222-size[1]));canvas.save(raw/(k+'.png'))
run(S/'palette_tool.py','build','--input',raw,'--colors','192','--name','Korean Arena V9 original shop pixel palette','--output-dir',A/'shops-palette')
run(S/'palette_tool.py','apply','--palette',A/'shops-palette/palette.json','--input',raw,'--output-dir',A/'shops-finished','--alpha-threshold','128')
# Raw material cells become semantic native64px textures; nearest only, no blur.
im=Image.open(SOURCE/'originals/materials.png').convert('RGB');names=['city-stone','city-herringbone','concrete','civic-inset','park-grass','forest-grass','park-trail','mulch','leisure-paving','coastal-stone','basalt','jeju-trail','sea','shallows','jeju-grass','rail-gravel'];strip=Image.new('RGB',(64,64*16))
for i,k in enumerate(names):
 x=i%4;y=i//4;box=[round(x*im.width/4),round(y*im.height/4),round((x+1)*im.width/4),round((y+1)*im.height/4)];tile=im.crop(box).resize((64,64),Image.Resampling.NEAREST);strip.paste(tile,(0,i*64))
strip.save(A/'native-material-strip.png')
args=[]
for i,k in enumerate(names):args+=['--terrain-row',f'{k}={i}']
run(M/'extract_terrain_tiles.py','--input',A/'native-material-strip.png','--rows','16','--cols','1',*args,'--tile-size','64','--resampler','nearest','--background-mode','opaque','--edge-policy','isolated','--prompt',SOURCE/'prompts/materials.txt','--output-dir',A/'materials-extracted')
write(A/'materials-index.json',{'names':names,'edgePolicy':'isolated source swatches, not a false seamless claim','source':'originals/materials.png','finish':'64px nearest sampling, literal image pixels; see terrain QC','future':'Review repeat seams in real Phaser; fix visually before handoff'})
print('Host images adopted; real Forge prop extraction, palette finish and16native material extraction complete')
