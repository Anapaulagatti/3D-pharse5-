"""Acceptance review derivatives and factual preservation/fit/source checks."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,subprocess,numpy as np
R=Path(__file__).resolve().parents[1];D=R/'docs/gate2/acceptance';S=R/'assets-src/gate2/acceptance';P=R/'public/assets/gate2'
font=lambda n:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',n)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,o):p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
def jpg(src,name,size=(1200,900)):
 im=Image.open(src).convert('RGB');im.thumbnail(size,Image.Resampling.LANCZOS);im.save(D/name,quality=86,optimize=True,subsampling=0)
for src,name,size in [('ORIGINAL_NATIVE_1X.png','ORIGINAL_REVIEW.jpg',(1024,1024)),('STATION_NATIVE_1X.png','STATION_REVIEW.jpg',(720,720)),('SEAM_NATIVE_1X.png','JOIN_REVIEW.jpg',(1280,720)),('JEJU-FIT_NATIVE_1X.png','JEJU_FIT_REVIEW.jpg',(1100,900)),('MOBILE_C_FOLLOW.png','MOBILE_FOLLOW.jpg',(844,390)),('MOBILE_C_SCENIC.png','MOBILE_SCENIC.jpg',(844,390)),('MOBILE_C_OVERVIEW.png','MOBILE_OVERVIEW.jpg',(844,390)),('MOBILE_NORTH_EDGE.png','MOBILE_NORTH_EDGE.jpg',(844,390))]:jpg(D/src,name,size)
crops=[]
for source,box,name in [('ORIGINAL_NATIVE_1X.png',(288,480,736,816),'ORIGINAL_PIXELS_1X.png'),('STATION_NATIVE_1X.png',(136,200,584,536),'STATION_PIXELS_1X.png'),('SEAM_NATIVE_1X.png',(1200,150,1968,662),'JOIN_PIXELS_1X.png')]:
 Image.open(D/source).crop(box).save(D/name,optimize=True);assert Image.open(D/name).convert('RGBA').tobytes()==Image.open(D/source).crop(box).convert('RGBA').tobytes();crops.append(dict(path=name,source=source,box=box,sourcePixelEquality=True))
for id in ['C','B']:
 board=Image.new('RGB',(1280,610),'#20383c');d=ImageDraw.Draw(board);d.text((12,10),f'Desktop {id} /1280x900 / native follow',font=font(20),fill='#f2ead7');d.text((784,10),'Mobile /844x390 / native follow',font=font(18),fill='#f2ead7');d.text((784,290),'Mobile Scenic / reduced scale',font=font(18),fill='#f2ead7')
 for p,box in [(D/f'DESKTOP_{id}_FOLLOW.png',(0,40,768,540)),(D/f'MOBILE_{id}_FOLLOW.png',(774,40,506,234)),(D/f'MOBILE_{id}_SCENIC.png',(774,330,506,234))]:
  x,y,w,h=box;board.paste(Image.open(p).convert('RGB').resize((w,h),Image.Resampling.LANCZOS),(x,y))
 board.save(D/f'DESKTOP_MOBILE_{id}.jpg',quality=85,optimize=True,subsampling=0)
# Collision illustration over actual native station capture; sources stay unchanged.
im=Image.new('RGB',(1440,770),'#20383c');d=ImageDraw.Draw(im)
for side in [0,1]:
 x=side*720;im.paste(Image.open(D/'STATION_NATIVE_1X.png').convert('RGB'),(x,50));d.text((x+12,12),'BEFORE:555x220'if not side else'AFTER:555x210 / south edge unchanged',font=font(20),fill='#f2ead7');d.rectangle((x+84,50+190,x+639,50+410),outline='#f18973',width=2)
 if side:d.rectangle((x+84,50+200,x+639,50+410),outline='#59d6b2',width=3)
im.save(D/'STATION_COLLISION_BEFORE_AFTER.jpg',quality=85,optimize=True,subsampling=0)
# Two native source views at equal scale for architectural comparison (not new art).
board=Image.new('RGB',(1024,570),'#20383c');dr=ImageDraw.Draw(board);dr.text((12,10),'Muneum benchmark / retained source',font=font(19),fill='#f2ead7');dr.text((524,10),'ONE NEW building / 오월제과',font=font(19),fill='#f2ead7')
for x,p in [(0,R/'docs/gate1/GATE1_STREET_NATIVE.png'),(512,D/'ORIGINAL_NATIVE_1X.png')]:
 image=Image.open(p).convert('RGB');box=(0,0,1024,1024) if x else(250,0,1274,1024);image=image.crop(box).resize((512,512),Image.Resampling.LANCZOS);board.paste(image,(x,50))
board.save(D/'ORIGINAL_VS_MUNEUM.jpg',quality=85,optimize=True,subsampling=0)
# Protected baseline and localized candidate checks.
protected=json.loads((D/'protected-before.json').read_text())
for path,h in protected.items():assert sha(R/path)==h,path
baseline=json.loads((R/'assets-src/world-gate1/plan.json').read_text());candidate=json.loads((S/'world-fit-candidate.json').read_text())
for b in baseline['buildings']:
 if b['id']!='jeju-culture':assert b==next(x for x in candidate['buildings']if x['id']==b['id']),b['id']
assert baseline['land'][0]==candidate['land'][0]
rect=candidate['gate2LocalizedFit']['stationCollisionWorld'];reserved=next(b['rect']for b in baseline['buildings']if b['id']=='civic');x,y,w,h=rect;rx,ry,rw,rh=reserved;assert x>=rx and y>=ry and x+w<=rx+rw and y+h<=ry+rh
for platform in baseline['station']['platforms']:
 a,b,c,d=platform['rect'];assert x+w<=a or a+c<=x or y+h<=b or b+d<=y
assert candidate['station']==baseline['station'];assert candidate['gate2LocalizedFit']['nativeFrame']==[3180,3200,1024,1536]
frame=candidate['gate2LocalizedFit']['nativeFrame'];assert frame[0]+frame[2]<=candidate['size'][0]and frame[1]+frame[3]<=candidate['size'][1]
# Source pixel identity for the real independent join.
left=Image.open(P/'seam/street-native-chunk.png').convert('RGBA');assert left.tobytes()==Image.open(P/'b/ground.png').convert('RGBA').crop((0,80,1536,800)).tobytes()
right=Image.open(P/'seam/station-native-chunk.png').convert('RGBA');raw=Image.open(P/'station/ground.png').convert('RGBA');assert right.convert('RGB').tobytes()==raw.convert('RGB').tobytes();assert set(right.getchannel('A').get_flattened_data())<={0,255}
combined=Image.new('RGBA',(2208,720));combined.alpha_composite(left,(0,0));combined.alpha_composite(right,(1488,0));assert set(combined.getchannel('A').get_flattened_data())=={255}
assert subprocess.check_output(['git','rev-parse','checkpoint/gate1-approved-planning-20261022^{}'],cwd=R,text=True).strip()=='e0a5c0aeff1a2980042983e6091abff11b987fad'
write(D/'source-and-fit-verification.json',dict(protectedFiles=len(protected),allProtectedHashesMatch=True,approvedMasterplanModified=False,nonJejuBuildingGeometryUnchanged=True,mainlandLandUnchanged=True,stationFootprintContained=True,stationPlazaAndPlatformsUnchanged=True,stationPlatformOverlap=False,jejuFrameFitsCandidateCanvas=True,joinOriginalRGBPixels=True,joinNoTransparentGaps=True,joinSourceScale=1,joinOwnership='binary alpha /48px native overlap',crops=crops,checkpointUnchanged=True))
def entry(p):return dict(path=str(p.relative_to(R)),sha256=sha(p),bytes=p.stat().st_size)
write(D/'new-art-provenance.json',dict(hostImageCallsThisDirective=1,buildingCount=1,route='host_image',model=None,estimateUsd=None,modelAndPriceNotExposed=True,paidProviderAPIUsed=False,prompt=entry(S/'original-prompt.txt'),references=[entry(S/'original-guide.png'),entry(R/'docs/gate1/GATE1_STREET_NATIVE.png')],hostOriginal=entry(S/'original-host.png'),native=entry(S/'original-native.png'),sourceDimensions=list(Image.open(S/'original-host.png').size),nativeDimensions=[1024,1024],uniformAuthoringFinish=1024/1254,approvedAssetsResized=False,originalCommercialFacade='Distinct terracotta ceramic fins, offset massing and glazed stairwell; no Muneum facade pixel reuse; source is generated/finished, not claimed hand-drawn',processing=entry(S/'processing.json')))
write(D/'evidence-files.json',[entry(p)for p in sorted(D.iterdir())if p.suffix in ['.png','.jpg']])
print('PASS protected source / native pixel / localized fit / independent join checks; lightweight copies exported')
