"""Lossless semantic layer ownership of original courtyard PNG, not image synthesis or repainting."""
from v3_final_art import *
import numpy as np
im=Image.open(S/'props/v3-jeju-court.png').convert('RGBA');a=np.asarray(im).copy();h,w=a.shape[:2];yy,xx=np.indices((h,w))
# Actual foreground side walls / open door leaves. Centre path/yard belongs to back layer.
front=((yy>=140)&(xx<171))|((yy>=148)&(xx>=215))
a0=a.copy();a1=a.copy();a0[front]=0;a1[~front]=0
out=S/'prop-layers';out.mkdir(exist_ok=True)
Image.fromarray(a0).save(out/'jeju-yard-back.png');Image.fromarray(a1).save(out/'jeju-yard-front.png')
assert not np.any((a0[:,:,3]>0)&(a1[:,:,3]>0));reconstructed=np.where((a1[:,:,3]>0)[:,:,None],a1,a0);assert np.array_equal(reconstructed[a[:,:,3]>0],a[a[:,:,3]>0]);assert np.array_equal(reconstructed[:,:,3],a[:,:,3])
rows=json.loads((S/'props.json').read_text());row=next(q for q in rows if q['id']=='v3-jeju-court');row['image']='prop-layers/jeju-yard-back.png';row['sha256']=sha(out/'jeju-yard-back.png');row['layerSource']='props/v3-jeju-court.png'
if not any(q['id']=='v3-jeju-court-front'for q in rows):rows.append(dict(row,id='v3-jeju-court-front',image='prop-layers/jeju-yard-front.png',sha256=sha(out/'jeju-yard-front.png')))
write(S/'props.json',rows);write(S/'prop-layers/ownership-qa.json',{'status':'PASS','source':'props/v3-jeju-court.png','sourceSha256':sha(S/'props/v3-jeju-court.png'),'method':'Two disjoint alpha ownership masks on unchanged registered native pixels; original retained. Back/floor atsort4330, foreground walls/leaves at4440. No RGB painting, scaling, mirrored pixels, or generated replacement.','size':[w,h],'anchor':row['anchor'],'overlapVisiblePixels':0,'reconstructionDifferentVisiblePixels':0,'transparentRGB':'Normalized0 only outside owned pixels','outputs':{p.name:sha(p)for p in out.glob('*.png')}})
# Reuse an actual generated stair at native scale to cross the station retaining face.
im=Image.open(S/'props/v3-seawall.png').convert('RGBA');box=(92,48,233,127);crop=im.crop(box);pad=Image.new('RGBA',(crop.width+4,crop.height+4));pad.paste(crop,(2,2));dest=out/'platform-stairs.png';pad.save(dest)
rows=json.loads((S/'props.json').read_text());row={'id':'v3-platform-stairs','image':'prop-layers/platform-stairs.png','size':list(pad.size),'anchor':[pad.width//2,pad.height-2],'sha256':sha(dest),'art_source':'host_image','raw':'raw/coast.png','nativeRecipe':{'source':'props/v3-seawall.png','crop':list(box),'scale':1,'operation':'Lossless literal native stair crop; transparent registration padding only.'}}
rows=[q for q in rows if q['id']!=row['id']]+[row];write(S/'props.json',rows);write(out/'stairs-qa.json',{'status':'PASS','sourceSha256':sha(S/'props/v3-seawall.png'),'sourceBox':list(box),'outputSha256':row['sha256'],'sameNativeVisiblePixels':True,'resampled':False})
