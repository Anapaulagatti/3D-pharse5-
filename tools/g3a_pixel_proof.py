from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3a-corrections';manifest=json.loads((R/'public/assets/gate3/registration/manifest.json').read_text());rows=[]
for entry in ['station','retail','bakery','convenience']:
 state=json.loads((D/f'{entry}-state.json').read_text());shot=np.array(Image.open(D/f'{entry}-native.png').convert('RGB'));vx,vy,w,h=map(int,state['camera']['worldView']);claim=np.zeros((h,w),bool)
 # Exclude Juni and later depth-occluding source objects, exactly as in the actual Phaser layer order.
 actor=np.zeros((h,w),bool);px,py=round(state['x'])-vx,round(state['y'])-vy;actor[max(0,py-104):min(h,py+14),max(0,px-52):min(w,px+53)]=True
 for o in sorted(manifest['objects'],key=lambda o:o['sortY'],reverse=True):
  x,y=int(o['x'])-vx,int(o['y'])-vy;src=np.array(Image.open(R/'public'/o['image']).convert('RGBA'));hh,ww=src.shape[:2];x0,y0=max(0,x),max(0,y);x1,y1=min(w,x+ww),min(h,y+hh)
  if x1<=x0 or y1<=y0:continue
  local=src[y0-y:y1-y,x0-x:x1-x];opaque=local[:,:,3]==255;region=claim[y0:y1,x0:x1];usable=opaque&(~region)&(~actor[y0:y1,x0:x1]);diff=np.max(np.abs(shot[y0:y1,x0:x1].astype(int)-local[:,:,:3].astype(int)),axis=2)
  if o['id'].startswith('registration/') and usable.sum():rows.append(dict(capture=entry,object=o['id'],comparedOpaquePixels=int(usable.sum()),differentPixels=int(np.sum((diff>0)&usable)),maxChannelDelta=int(diff[usable].max()),status='PASS' if not np.any(diff[usable]) else 'FAIL'))
  region|=local[:,:,3]>0
 # Light review copies; never overwrite native PNGs.
 im=Image.fromarray(shot);im.thumbnail((960,675),Image.Resampling.NEAREST);im.save(D/f'{entry}-preview.jpg',quality=86,optimize=True)
# The protected district is also compared directly against the old approved station frontage.
s=json.loads((D/'preserved-district-state.json').read_text());vx,vy,_,_=s['camera']['worldView'];im=Image.open(D/'preserved-district-native.png').convert('RGB');expected=Image.open(R/'assets-src/gate25-station-planters/expected-native-composite.png').convert('RGB')
for name,box in [('left',(2545,695,2735,782)),('right',(2908,699,3098,782))]:
 x,y,x2,y2=box;a=np.array(im.crop((x-vx,y-vy,x2-vx,y2-vy)));b=np.array(expected.crop(box));assert np.array_equal(a,b),name
 im.crop((x-vx-12,y-vy-12,x2-vx+12,y2-vy+12)).save(D/f'{name}-preserved-planter-1x.png')
phase={'protectedLogicalSourceAnchor':[2238.5,2180],'explicitSourcePivot':[.5,0],'candidateRasterEdge':[2238,2180],'rasterOffsetFromLegacyEdge':[-.5,0],'logicalCollider':[2322.5,2380,555,210],'logicalThreshold':[2598.5,2610],'sourceColumn84RasterCell':[2322,2323],'sourceColumn84PixelCenter':2322.5,'sourceColumn360PixelCenter':2598.5,'roundingOfProtectedCoordinates':False,'approvedPlanChanged':False,'status':'CANDIDATE_ONLY / human approval of convention required'}
(D/'native-pixel-and-phase.json').write_text(json.dumps({'opaqueSourceReadback':rows,'preservedPlanters':'PASS exact RGB','phase':phase},indent=2)+'\n')
# Technical phase/geometry diagram is separate from untouched native evidence.
canvas=Image.new('RGB',(1100,380),'#17242e');d=ImageDraw.Draw(canvas);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
for i,x in enumerate(range(2318,2328)):
 sx=55+i*95;d.rectangle((sx,100,sx+95,210),outline='#69827a',width=2);d.text((sx+5,220),str(x),font=font,fill='white');d.ellipse((sx+44,150,sx+50,156),fill='#ffdc86')
edge=55+(2322.5-2318)*95;d.line((edge,50,edge,270),fill='#ff817d',width=3)
for i,t in enumerate(['Station logical anchor2238.5 is retained; candidate raster edge2238 via explicit0.5px pivot.','Red: unchanged logical collision edge2322.5. Gold: native pixel centres.','Column84 centre2322.5; column360 centre2598.5 matches the unchanged entrance axis.','Rendering offset -0.5px is declared and subject to final registration approval; no source resampling.']):d.text((15,10 if i==0 else 275+(i-1)*29),t,font=font,fill='white')
canvas.save(D/'PIXEL_PHASE_AND_COLLISION.png',optimize=True)
assert all(r['status']=='PASS' for r in rows),rows
print('Native source readback',len(rows),'regions PASS')
