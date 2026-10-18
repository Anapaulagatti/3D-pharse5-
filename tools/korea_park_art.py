"""First Namsan increment only: real Forge finishing of retained original sources."""
from korea_art import *
process('park-kit',[
 ('kr-directory',[0,0,740,345],160,'width'),('kr-overlook',[740,0,1536,345],288,'width'),('kr-telescope',[0,345,740,662],96,'height'),('kr-cliff',[740,345,1536,662],224,'width'),('kr-pine',[0,662,740,1024],304,'width'),('kr-rest',[740,662,1536,1024],144,'height')])
boxes=S/'boxes/tower.json';write(boxes,{'schema':'forge-crop-boxes/v1','items':[{'id':'tower-master','box':[0,0,1024,1536]}]});out=S/'keyed/tower'
if not out.exists():run(F/'skills/generate2dmap/scripts/extract_prop_pack.py','--input',S/'raw/tower.png','--boxes-file',boxes,'--output-dir',out,'--component-mode','all','--min-component-area',1,'--despill-radius',3,'--alpha-hygiene','both','--reject-edge-touch','--max-dropped-fraction','0.01')
source=out/'tower-master/prop.png';im=Image.open(source).convert('RGBA');cut=1090;recon=Image.new('RGBA',im.size);native=C/'native-tower';native.mkdir(exist_ok=True);rows=[]
for label,box,target,axis in [('kr-tower-shaft',[0,0,im.width,cut],340,'height'),('kr-tower-pavilion',[0,cut,im.width,im.height],400,'width')]:
 part=im.crop(box);recon.paste(part,(box[0],box[1]));frames=C/f'frames/{label}';frames.mkdir(parents=True,exist_ok=True);part.save(frames/'000.png');bb=part.getbbox();height=target if axis=='height'else round((bb[3]-bb[1])*target/(bb[2]-bb[0]));dest=C/f'finish/{label}-{height}'
 if not dest.exists():run(F/'skills/video2dsprite/scripts/finish_frames.py','hd','--frames',frames,'--output-dir',dest,'--target-height',height,'--display-sizes','1x','--role','prop','--clip',label)
 shutil.copyfile(dest/'frames/000.png',native/f'{label}.png');rows.append({'id':label,'source':str(source.relative_to(S)),'sourceBox':box,'nativeRecipe':{axis:target},'sourceSha256':sha(source),'purpose':'Independently sortable tower and readable visitor pavilion; not character rescaling'})
assert recon.tobytes()==im.tobytes();write(S/'tower-ownership.json',{'sourceSize':list(im.size),'sourceSha256':sha(source),'disjointReconstructionDifferences':0,'parts':rows})
quant=C/'quantized-tower'
if not quant.exists():run(F/'skills/generate2dsprite/scripts/palette_tool.py','apply','--input',native,'--palette',R/'assets-src/seoul-production/palette/palette.json','--orphans',0,'--output-dir',quant)
for row in rows:
 p=Image.open(quant/f'{row["id"]}.png').convert('RGBA');p=p.crop(p.getbbox());a=Image.new('RGBA',(p.width+4,p.height+4));a.paste(p,(2,2));path=S/f'props/{row["id"]}.png';a.save(path);row.update(image=str(path.relative_to(S)),size=list(a.size),anchor=[a.width//2,a.height-2],sha256=sha(path),art_source='host_image')
write(S/'tower-props.json',rows);print('6park props +2tower ownership components; no character animation generation')
