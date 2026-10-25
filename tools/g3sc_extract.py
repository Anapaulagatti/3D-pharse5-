"""Native contour ownership for the entirely fresh station painting only."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json
from scipy.ndimage import label,binary_dilation
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate3/station-clean-v1';O=R/'public/assets/gate3/station-clean-world'
def poly(pts):
 im=Image.new('L',(1536,1024));ImageDraw.Draw(im).polygon(pts,fill=255);return np.array(im)>0
src=Image.open(S/'fresh-station-authored.png').convert('RGBA');assert src.size==(1536,1024);a=np.array(src)
pts=[(673,224),(684,224),(686,243),(689,246),(704,257),(914,257),(914,253),(926,253),(927,267),(948,285),(973,303),(983,308),(983,317),(994,325),(994,337),(977,346),(977,352),(970,352),(970,449),(978,449),(978,490),(976,490),(976,564),(978,564),(978,616),(982,616),(982,670),(952,671),(764,671),(764,686),(590,686),(590,671),(374,671),(374,655),(376,655),(376,491),(372,491),(372,451),(379,451),(379,353),(366,353),(366,345),(358,339),(358,329),(365,324),(365,311),(372,311),(389,297),(420,274),(429,265),(429,253),(442,253),(442,257),(653,257),(670,244),(671,228)]
mask=poly(pts);Image.fromarray(mask.astype('uint8')*255).save(S/'fresh-architecture-contour-mask.png')
# Contour coordinates refer only to this fresh1536x1024 painting, never old station masks.
yy,xx=np.indices(mask.shape);parts=[]
for name,part in [('roof',yy<355),('upper',(yy>=355)&(yy<488)),('facade',yy>=488)]:
 ar=a.copy();ar[:,:,3]=np.where(mask&part,255,0);im=Image.fromarray(ar).crop((354,220,1038,720));fp=O/('fresh-'+name+'.png');im.save(fp);parts.append({'id':'clean-station/'+name,'image':str(fp.relative_to(R/'public')),'x':2274,'y':2140,'width':684,'height':500,'sortY':2590,'alphaSoftening':.35,'sourceAnchor':[2313.5,2196],'sourcePivot':[39.5,56],'bytes':684*500*4})
full=a.copy();full[:,:,3]=np.where(mask,255,0);Image.fromarray(full).crop((354,220,1038,720)).save(S/'fresh-station-independent.png')
# New shadow ownership only. No legacy floor/old shadow is a possible donor.
base=np.array(Image.open(S/'fresh-empty-site-authored.png').convert('RGBA'));shape=poly([(971,353),(1005,382),(1028,417),(1033,655),(994,694),(438,704),(371,685),(371,654),(590,665),(590,684),(768,684),(768,664),(982,659),(980,615),(976,615),(976,490),(978,490),(978,449),(971,449)])
dark=(base[:,:,:3].mean(2)-a[:,:,:3].mean(2))>14;shadow=shape&dark&~mask;lab,_=label(shadow);sizes=np.bincount(lab.ravel());shadow&=(lab>0)&(sizes[lab]>=22);Image.fromarray(shadow.astype('uint8')*255).save(S/'fresh-contact-shadow-mask.png')
(S/'fresh-station-layers.json').write_text(json.dumps({'source':'fresh-station-authored.png','sourceOrigin':[1920,1920],'sourceScale':1,'resampling':'NONE','legacyStationInputs':[],'objects':parts,'nativeSourceCrop':[354,220,684,500],'physicalSideReturns':[[2294,2380,29,210],[2878,2380,24,210]],'doorPublicTarget':[2598.5,2610],'shadowSource':'Same fresh painting only, never old ground'},indent=2)+'\n');print('Fresh native layer masks ready; no legacy donors')
