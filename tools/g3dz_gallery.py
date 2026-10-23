from pathlib import Path
from PIL import Image,ImageDraw
import json,html
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-zoned-world'
shots=json.loads((D/'native-captures.json').read_text());records=[]
for row in shots['rows']:
 name=row['name'];im=Image.open(D/(name+'.png')).convert('RGB');assert im.size==(1280,900)
 im.resize((640,450),Image.Resampling.NEAREST).save(D/(name.replace('-native','-preview')+'.jpg'),quality=86,optimize=True)
 im.crop((320,250,960,650)).save(D/(name.replace('-native','-crop-1x')+'.png'),optimize=True)
 records.append({'source':name+'.png','cropRect':[320,250,640,400],'nativeCrop':name.replace('-native','-crop-1x')+'.png','preview':'640x450 nearest-neighbor viewing copy / not pixel proof'})
for phase in ['before','after']:Image.open(D/('world-'+phase+'-overview-phaser.png')).convert('RGB').save(D/('world-'+phase+'-overview-preview.jpg'),quality=89,optimize=True)
defects=[('Z01','Commercial service/public space','urban-service-west',[120,180,640,480]),('Z02','Station paving/rail landscape','station',[0,0,640,400]),('Z03','Station/amusement arrival','station-amusement',[180,240,900,420]),('Z04','Historic boundaries','culture',[100,150,920,500]),('Z05','City/Namsan threshold','namsan',[100,80,920,460]),('Z06','Harbor promenade','waterfront',[100,120,920,500]),('Z07','Western Jeju bridge/ocean','jeju-bridge',[480,0,640,600]),('Z08','External Jeju southern water','jeju-culture',[0,250,640,500])]
for key,title,frame,rect in defects:
 x,y,w,h=rect
 for phase in ['before','after']:
  im=Image.open(D/(frame+'-'+phase+'-native.png')).crop((x,y,x+w,y+h));im.save(D/(key+'-'+phase+'-crop-1x.png'),optimize=True)
  im=im.convert('RGB');im.thumbnail((640,450),Image.Resampling.NEAREST);im.save(D/(key+'-'+phase+'-preview.jpg'),quality=87,optimize=True)
 records.append({'defect':key,'title':title,'sourceFrame':frame,'nativeCrop':rect,'reference':'Human textual defect list; exact six marked reviewer images not received'})
# Reuse the original approved Phaser benchmark at its native pixel scale.
reference=Image.open(R/'docs/gate2/B_NATIVE_1X.png');w,h=reference.size
cells=[('Approved Muneum',reference.crop((w//2-192,h//2-150,w//2+192,h//2+150)))]
for key in ['retail','station','urban-service-west','amusement','jeju-culture']:
 cells.append((key,Image.open(D/(key+'-after-native.png')).crop((448,300,832,600))))
board=Image.new('RGB',(1152,652),'#163033');bd=ImageDraw.Draw(board)
for i,(title,im)in enumerate(cells):
 x=(i%3)*384;y=(i//3)*326;bd.text((x+8,y+7),title,fill='white');board.paste(im.convert('RGB'),(x,y+26))
board.save(D/'native-benchmark-board.png',optimize=True);board.save(D/'native-benchmark-preview.jpg',quality=86,optimize=True)
records.append({'benchmarkSource':'docs/gate2/B_NATIVE_1X.png','crop':[w//2-192,h//2-150,384,300],'boardCells':'All384x300 original-scale crops; labels outside art; no resampling'})
core=[('palace','01 Historic palace'),('academy','02 Academy/hanok'),('culture','03 Cultural compound'),('transition','04 Historic/modern threshold'),('retail','05 Modern commercial'),('station','06 Hanbit railway'),('namsan','07 Namsan/Maru'),('amusement','08 Amusement'),('market','09 Harbor/market'),('jeju-culture','10 Canonical Jeju')]
md='''# G3-D coordinated urban / landscape correction

**Human artistic acceptance is pending.** [Playable ZIP](G3D_ZONED_WORLD_REVIEW.zip) · [QA/decisions](README.md) · [Landscape masterplan](LANDSCAPE_MASTERPLAN.md) · [Coverage](COVERAGE.md) · [Native capture registry](native-captures.json).

Six marked reviewer screenshots were not attached or found. Exact marked-region acceptance is **NOT TESTED**. Z01–Z08 map the textual defects to real native evidence, not invented screenshot markings.

## Identical-framing actual Phaser overviews

| Before | After |
|---|---|
| ![Before](world-before-overview-preview.jpg) | ![After](world-after-overview-preview.jpg) |

[Before original overview](world-before-overview-phaser.png) · [After original overview](world-after-overview-phaser.png). These are actual Phaser scaled proxies with existing wayfinding overlays; they do not prove pixel quality.

## All ten regions — actual native Phaser

Click the untouched1280×900 original PNGs for1:1 inspection. JPEGs are lightweight nearest-neighbor review copies under1MB.
'''
body='<h1>G3-D coordinated urban/landscape review</h1><p>Human artistic/spatial acceptance pending. Six marked reviewer images NOT PROVIDED.</p><p><a href="README.md">QA / remaining decisions</a> · <a href="LANDSCAPE_MASTERPLAN.md">Landscape plan</a> · <a href="DEVICE_REVIEW.md">Device handoff</a></p><h2>Identical framing / scaled Phaser overview</h2><div class="pair">'+''.join(f'<figure><img src="world-{p}-overview-preview.jpg"><figcaption>{p} / scaled overview</figcaption></figure>'for p in ['before','after'])+'</div>'
for key,title in core+[(a,b)for a,b,_,_ in defects]+[('urban-service-west','Modern density / western service space'),('urban-service-east','Modern density / eastern service space'),('urban-density','Historic-to-commercial planting boundary')]:
 suffix='crop-1x'if key.startswith('Z')else'native'
 md+=f'\n### {key} — {title}\n\n| Before | After |\n|---|---|\n| ![Before]({key}-before-preview.jpg) | ![After]({key}-after-preview.jpg) |\n\n[Before1:1]({key}-before-{suffix}.png) · [After1:1]({key}-after-{suffix}.png)\n'
 body+=f'<h2>{html.escape(title)}</h2><div class="pair">'
 for phase in ['before','after']:
  native=f'{key}-{phase}-{suffix}.png';body+=f'<figure><a href="{native}"><img loading="lazy" src="{key}-{phase}-preview.jpg"></a><figcaption>{phase} · <a href="{native}">original1:1 pixels</a></figcaption></figure>'
 body+='</div>'
md+='''
## Native Muneum craftsmanship benchmark

[![Original-scale comparison](native-benchmark-preview.jpg)](native-benchmark-board.png)

Six384×300 cells preserve source pixels at1:1. Protected facades are reused, not newly generated buildings.

## Landscape density and navigation

Density was decided by public-space function and available land, not an arbitrary vegetation percentage. Seven noncanonical urban/harbor trees were removed and four visible low-bed bases received explicit contacts; protected garden/park trees remain. [Native ownership registry](../../assets-src/gate3/zoned-world-v1/integration-provenance.json).

[Actual continuous gameplay](world-traversal-review.mp4) · [Native-resolution viewing encode](world-traversal-native-resolution.mp4) · [Movement report](movement-report.json) · [Station/amusement native](station-amusement-after-native.png) · [Bridge native](jeju-bridge-after-native.png) · [Rail/coast native](rail-coast-after-native.png) · [Bookshop visibility](bookshop-occlusion-after-native.png).

The station8px strip, tower/retail and ride/road projection, inherited routes/body clearance, required Bakery and real hardware/device requirements remain explicit. No main merge, deployment or physical-device PASS.
'''
body+='<h2>Actual continuous gameplay</h2><video controls preload="metadata" src="world-traversal-review.mp4"></video><p>Compressed viewing encode; original PNGs establish pixel fidelity. Physical Android/iPhone NOT TESTED.</p>'
(D/'VISUAL_REVIEW.md').write_text(md)
(D/'VISUAL_REVIEW.html').write_text('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>G3-D zoned world</title><style>body{background:#163033;color:#f4e9d1;font:17px/1.5 system-ui;max-width:1350px;margin:2em auto;padding:0 1em}a{color:#9be2dc}.pair{display:flex;gap:12px;flex-wrap:wrap}figure{margin:0;flex:1;min-width:290px}img,video{max-width:100%;image-rendering:pixelated}figcaption{margin:8px 0 22px}video{width:100%}</style>'+body)
(D/'review-derivatives.json').write_text(json.dumps({'derivatives':records,'pixelProof':'Original native Phaser PNGs, not JPEG/video/overview'},indent=2)+'\n')
assert all(p.stat().st_size<1000000 for p in D.glob('*.jpg'))
print('Gallery ready: native crops unscaled; all JPEGs <1MB')
