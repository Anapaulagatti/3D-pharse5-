from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,numpy as np
R=Path(__file__).resolve().parents[1];D=R/'docs/gate25-polish';S=R/'assets-src/gate25-polish';font=lambda n:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',n)
def jpeg(name,size):
 im=Image.open(D/name).convert('RGB');im.thumbnail(size,Image.Resampling.LANCZOS);im.save(D/(Path(name).stem+'_REVIEW.jpg'),quality=86,optimize=True,subsampling=0)
for name in ['BEFORE_NATIVE_1X.png','AFTER_NATIVE_1X.png']:jpeg(name,(1592,607))
# All before/after comparisons originate from actual native Phaser canvases, not the editing reference.
crops=[]
for x,label in [(1488,'WEST'),(2464,'EAST')]:
 box=(x-256,610,x+256,1214)
 board=Image.new('RGB',(1024,650),'#20383c');dr=ImageDraw.Draw(board)
 for col,phase in enumerate(['BEFORE','AFTER']):
  source=D/(phase+'_NATIVE_1X.png');crop=Image.open(source).crop(box);p=D/(label+'_'+phase+'_CROP_1X.png');crop.save(p,optimize=True);assert Image.open(p).tobytes()==Image.open(source).crop(box).tobytes();board.paste(crop.convert('RGB'),(col*512,46));dr.text((col*512+12,10),phase+' / native1:1 / '+label+' join',font=font(19),fill='#f3e9d0');crops.append(dict(path=p.name,source=source.name,box=box,nativePixelsExact=True))
 board.save(D/(label+'_BEFORE_AFTER.jpg'),quality=87,optimize=True,subsampling=0)
for n in ['TOUR_1','TOUR_2','TOUR_3','TOUR_4','TOUR_COLLAPSED','TOUR_EXPANDED']:
 jpeg(n+'.png',(844,390))
board=Image.new('RGB',(1120,620),'#20383c');dr=ImageDraw.Draw(board)
for x,y,file,title in [(0,0,R/'docs/gate25/TOUR_1.png','Before / Coastal'),(560,0,R/'docs/gate25/TOUR_2.png','Before / Oreum'),(0,310,D/'TOUR_1.png','After / Coastal /50%'),(560,310,D/'TOUR_2.png','After / Oreum /50%')]:
 im=Image.open(file).convert('RGB');im.thumbnail((550,260));board.paste(im,(x+5,y+40));dr.text((x+10,y+8),title,font=font(19),fill='#f3e9d0')
board.save(D/'TOUR_COMPOSITION_BEFORE_AFTER.jpg',quality=87,optimize=True,subsampling=0)
# Whole original foreground layers restored exactly; quantify the actual former alpha clipping.
old=json.loads((R/'public/assets/gate2/district/scene.json').read_text());new=json.loads((R/'public/assets/gate2/district-polish/scene.json').read_text());props=[]
for ob in new['objects']:
 prev=next(o for o in old['objects']if o['id']==ob['id']);a=np.array(Image.open(R/'public/assets/gate2'/prev['image']).convert('RGBA'));b=np.array(Image.open(R/'public/assets/gate2'/ob['image']).convert('RGBA'));assert [prev[k]for k in ['x','y','sortY','width','height']]==[ob[k]for k in ['x','y','sortY','width','height']];props.append(dict(id=ob['id'],restoredAlphaPixels=int(np.count_nonzero(a[:,:,3]!=b[:,:,3])),coordsAndNativeDimensionsUnchanged=True,source=ob['image']))
(D/'foreground-restoration.json').write_text(json.dumps(props,indent=2)+'\n')
a=np.array(Image.open(S/'before-background.png').convert('RGB'));b=np.array(Image.open(S/'finished-background.png').convert('RGB'));missing=np.array(Image.open(S/'missing-mask.png'))>0;guard=~missing;guard[787:]=False;assert np.array_equal(a[guard],b[guard]);assert not np.any((b==[32,56,60]).all(axis=2)&missing)
(D/'evidence-checks.json').write_text(json.dumps(dict(crops=crops,allOriginalUpperPixelsExact=True,originalUpperPixelCount=int(guard.sum()),missingFlatRegionsFilled=True,sourceArtProvenance='assets-src/gate25-polish/provenance.json'),indent=2)+'\n')
print('PASS native comparison/crop equality, whole foreground registration and upper facade preservation')
