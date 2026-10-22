"""Apply only a retained entrance patch and local collision amendment; no scene regeneration."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import json,hashlib,shutil
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate2/access-fix';P=R/'public/assets/gate2/c';D=R/'docs/gate2/final-review'
source=S/'host-output.png' if (S/'host-output.png').exists() else Path('/workspace/generated_images/exec-8f19f539-5be4-4e23-a960-21fb5fd300ec.png')

if source.resolve()!=(S/'host-output.png').resolve():shutil.copy2(source,S/'host-output.png')
im=Image.open(source).convert('RGBA');assert im.size==(1024,1536)
# Exact binary technical mask: only the new side approach / gate opening is admitted.
poly=[(530,875),(575,890),(610,930),(655,975),(690,1030),(715,1080),(715,1140),(680,1190),(610,1225),(490,1235),(480,1180),(560,1165),(605,1125),(610,1060),(585,1010),(555,975),(535,940),(520,905)]
mask=Image.new('L',im.size);ImageDraw.Draw(mask).polygon(poly,fill=255)
# Keep the complete retained house silhouette / roof pixel-identical.
ImageDraw.Draw(mask).polygon([(190,1045),(230,1015),(300,970),(325,910),(490,910),(515,965),(570,1000),(622,1045),(595,1070),(580,1168),(220,1175),(210,1070)],fill=0)
# Original orchard foreground pixels remain above the path, unchanged.
box=mask.getbbox();patch=im.crop(box);patch.putalpha(mask.crop(box));patch.save(S/'entrance-paving.png');shutil.copy2(S/'entrance-paving.png',P/'entrance-paving.png')
scene=json.loads((P/'scene.json').read_text());scene['objects']=[o for o in scene['objects']if o['id']!='entrance-paving'];scene['objects'].append(dict(id='entrance-paving',image='c/entrance-paving.png',x=box[0],y=box[1],width=patch.width,height=patch.height,sortY=-90,alphaSoftening=1))
points=[[540,865],[560,915],[628,984],[650,1050],[650,1130],[635,1185],[560,1205],[500,1205],[410,1210],[410,1190]]
scene['routes']=[r for r in scene['routes']if r['id']!='house-direct-approach'];scene['routes'].append(dict(id='house-direct-approach',points=points,width=64))
scene['accessAmendment']='Only foreground paving patch and local foot-clearance amendment. Original foundation PNG unchanged. Exterior entrance approach; no interior gameplay.'
(P/'scene.json').write_text(json.dumps(scene,indent=2,ensure_ascii=False)+'\n')
# Union only this corridor's pre-eroded foot clearance into retained original mask.

if not (S/'walk-before.png').exists():shutil.copy2(P/'walk.png',S/'walk-before.png')
original=Image.open(S/'walk-before.png').convert('L')
add=Image.new('L',original.size);d=ImageDraw.Draw(add);d.line([tuple(p)for p in points],fill=255,width=64,joint='curve')
for x,y in points:d.ellipse((x-32,y-32,x+32,y+32),fill=255)
for solid in scene['solids']:
 x,y,w,h=solid['rect'];d.rectangle((x,y,x+w,y+h),fill=0)
add=add.filter(ImageFilter.MinFilter(17))
from PIL import ImageChops
result=ImageChops.lighter(original,add);result.save(P/'walk.png')
meta=dict(route='host_image',model=None,estimateUsd=None,paidProviderAPI=False,originalSource='assets-src/gate2/native/jeju.png',hostOutput='assets-src/gate2/access-fix/host-output.png',prompt='assets-src/gate2/access-fix/prompt.txt',maskPolygon=poly,patchBox=box,routePoints=points,routeWidthPx=64,footClearancePx=8,wholeSceneRebuilt=False,originalFoundationModified=False,interiorGameplay=False)
(S/'amendment.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps(meta))
