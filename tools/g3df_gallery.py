"""Review copies only. Original Phaser PNGs are immutable outputs."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,html,shutil
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-alignment';S=R/'assets-src/gate3/alignment-v1'
cap=json.loads((D/'native-captures.json').read_text());m=json.loads((R/'public/assets/gate3/aligned-world/manifest.json').read_text());old=json.loads((R/'public/assets/gate3/reconciled-world/manifest.json').read_text())
def jpg(im,name,w=1600):
 im=im.convert('RGB')
 if im.width>w:im=im.resize((w,round(im.height*w/im.width)),Image.Resampling.NEAREST)
 for q in [88,80,70,60]:
  im.save(D/name,quality=q,optimize=True)
  if (D/name).stat().st_size<1000000:return name
 raise ValueError(name)
def compare(name):
 a=Image.open(D/(name+'-before-native.png')).convert('RGB');b=Image.open(D/(name+'-after-native.png')).convert('RGB');out=Image.new('RGB',(a.width*2,a.height+30),'#172d30');out.paste(a,(0,30));out.paste(b,(a.width,30));d=ImageDraw.Draw(out);d.text((8,8),'BEFORE /06b718a',fill='white');d.text((a.width+8,8),'AFTER / local candidate / NOT HUMAN APPROVED',fill='white');return jpg(out,name+'-comparison.jpg',1900)
groups=[]
for row in cap['rows']:
 if '-after-native' in row['name']:
  n=row['name'].replace('-after-native','');groups.append((n,compare(n)))
# Approved historical Phaser graybox is cropped, never rerendered as invented final art.
row=next(x for x in cap['rows']if x['name']=='palace-compound-after-native');sx,sy=row['audit']['camera']['scroll'];size=Image.open(D/'palace-compound-after-native.png').size
Image.open(R/'docs/world-gate1/GRAYBOX_NATIVE_4096x4608.png').crop((sx,sy,sx+size[0],sy+size[1])).save(D/'palace-approved-graybox-native.png')
plan=json.loads((R/'assets-src/gate3/production-plan-v3.1-restored.json').read_text())['plan']
for phase in ['before','after']:
 im=Image.open(D/('palace-compound-'+phase+'-native.png')).convert('RGB');dr=ImageDraw.Draw(im)
 for o in plan['buildings']:
  if o['kind']=='heritage':
   x,y,w,h=o['rect'];dr.rectangle((x-sx,y-sy,x+w-1-sx,y+h-1-sy),outline='#ffe080',width=2)
 for b in plan['boundaries']:
  x,y,w,h=b['rect'];dr.rectangle((x-sx,y-sy,x+w-1-sx,y+h-1-sy),outline='#00ffff',width=2)
 dr.line((2048-sx,290-sy,2048-sx,1140-sy),fill='#ff55cf',width=2);im.save(D/('palace-'+phase+'-geometry-overlay.png'))
# Source alpha separation proof at EXACT native scale, no resized architecture.
for key in ['station','cafe','bookshop','learning']:
 a=next(o for o in old['objects']if o['id']=='registration/'+key);b=next(o for o in m['objects']if o['id']==a['id']);left=min(a['x'],b['x']);top=min(a['y'],b['y']);right=max(a['x']+a['width'],b['x']+b['width']);bottom=max(a['y']+a['height'],b['y']+b['height']);w=right-left;h=bottom-top;board=Image.new('RGB',(w*3,h+30),'#824d74');d=ImageDraw.Draw(board)
 for i,ob in enumerate([a,b]):
  im=Image.open(R/'public'/ob['image']).convert('RGBA');board.paste(im,(i*w+ob['x']-left,30+ob['y']-top),im);d.text((i*w+5,8),['BEFORE alpha','AFTER alpha'][i],fill='white')
 al=Image.open(R/'public'/b['image']).getchannel('A').convert('RGB');board.paste(al,(2*w+b['x']-left,30+b['y']-top));d.text((2*w+5,8),'Ownership alpha /native1x',fill='white');board.save(D/(key+'-source-alpha-native.png'));jpg(board,key+'-source-alpha-preview.jpg')
# Native bridge repair masks & old source edge on the same native world rectangle.
row=next(x for x in cap['rows']if x['name']=='bridge-full-after-native');sx,sy=row['audit']['camera']['scroll'];im=Image.open(D/'bridge-full-after-native.png').convert('RGB');pix=Image.new('RGBA',im.size);dd=ImageDraw.Draw(pix);dd.line((3180-sx,3200-sy,3180-sx,4000-sy),fill='#ff55cf',width=2)
for name in ['bridge-mainland','bridge-island','bridge-water-ownership']:
 mask=Image.open(S/(name+('-repair-mask.png'if name!='bridge-water-ownership'else'.png'))).convert('L');layer=Image.new('RGBA',mask.size,(50,255,210,70));layer.putalpha(mask.point(lambda x:70 if x else 0));pix.alpha_composite(layer,(2816-sx,3072-sy))
Image.alpha_composite(im.convert('RGBA'),pix).save(D/'bridge-source-ownership-overlay.png')
# Native support vs current blocking strip; not a transfer PASS.
row=next(x for x in cap['rows']if x['name']=='station-right-after-native');sx,sy=row['audit']['camera']['scroll'];im=Image.open(D/'station-right-after-native.png').convert('RGB');d=ImageDraw.Draw(im);d.rectangle((2950-sx,2626-sy,2957-sx,2754-sy),fill='#ff3045');d.text((2950-sx-270,2626-sy-20),'8px CLOSED / no90x36 connector / transfer NOT accepted',fill='white',stroke_width=1,stroke_fill='black');im.save(D/'station-collision-strip-native.png')
extra=['world-before-overview-phaser','world-after-overview-phaser','palace-approved-graybox-native','palace-before-geometry-overlay','palace-after-geometry-overlay','palace-compound-registration-overlay','palace-east-registration-overlay','station-front-registration-overlay','bridge-full-registration-overlay','bridge-source-ownership-overlay','archive-access-proposal-overlay','station-road-proposal-native','station-collision-strip-native']
for n in extra:jpg(Image.open(D/(n+'.png')),n+'-preview.jpg')
# Side-by-side craftsmanship at EXACT scale, original references remain unchanged.
paths=['docs/gate1/GATE1_STREET_NATIVE.png','docs/gate25-refinement/AFTER_NATIVE_1X.png','docs/gate3-alignment/station-front-after-native.png','docs/gate3-alignment/palace-entrance-after-native.png'];board=Image.new('RGB',(2048,550),'#162d30');dr=ImageDraw.Draw(board)
for i,p in enumerate(paths):
 im=Image.open(R/p).convert('RGB');x=im.width//2-256;y=im.height//2-250;board.paste(im.crop((x,y,x+512,y+500)),(i*512,45));dr.text((i*512+6,12),['Approved Muneum','Approved Gate2.5','Current station','Current palace'][i],fill='white')
board.save(D/'craftsmanship-native-board.png');jpg(board,'craftsmanship-review.jpg',1800)
style='body{font:17px/1.55 system-ui;max-width:1500px;margin:2em auto;padding:0 1em;background:#162d30;color:#f3e8d4}a{color:#9ce1e0}img,video{max-width:100%;height:auto}figure{margin:2em 0}strong{color:#ffcf8b}table{border-collapse:collapse}td,th{border:1px solid #698a87;padding:.5em}'
parts=[f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>G3-D final alignment review</title><style>{style}</style></head><body><h1>G3-D · five-area architectural alignment candidate</h1>', '<p><strong>Human artistic/spatial approval pending. Station complete border erasure remains FAIL: protected road softness/material phase and a clipped right tree crown are recorded. No full-world acceptance.</strong> Bridge full stop/turn clearance also remains FAIL despite successful locomotion crossing. Seven annotated screenshots were not attached; exact annotation matching is NOT TESTED.</p>', '<p>These JPEGs are review copies under1MB. Native links are actual unchanged Phaser POST_RENDER PNGs at zoom1, DPR1. Browser display can shrink images: open/download at100% for pixel review. Wide native scenes2048×1280, detail1280×900. Source/geometry overlays are labelled technical diagrams, not gameplay.</p>', '<p><a href="G3D_FINAL_ALIGNMENT_REVIEW.zip">PLAYABLE ZIP</a> · <a href="README.md">Decisions / remaining issues</a> · <a href="QA.md">QA</a> · <a href="measurements.json">Measured geometry</a> · <a href="SOURCE_OWNERSHIP.md">Ownership / provenance</a></p>']
def figure(n,caption=''):
 return f'<figure><figcaption>{html.escape(caption or n)} · <a href="{n}.png">native PNG</a></figcaption><img loading="lazy" src="{n}-preview.jpg"></figure>'
parts.append('<h2>Full-world context · scaled overview only</h2>')
for n in extra[:2]:parts.append(figure(n))
parts.append('<h2>Fifteen identical-camera BEFORE / AFTER pairs</h2>')
for n,p in groups:parts.append(f'<figure id="{n}"><figcaption><b>{n}</b> · <a href="{n}-before-native.png">BEFORE native1x</a> · <a href="{n}-after-native.png">AFTER native1x</a></figcaption><img loading="lazy" src="{p}"></figure>')
parts.append('<h2>Approved graybox / current / corrected registration</h2><p>Yellow=approved support reservations; cyan=wall supports; magenta=axis/threshold. Roof projections are distinct from physical footprints. Historical plan unchanged.</p>')
for n in extra[2:10]:parts.append(figure(n))
parts.append('<h2>Source crop / alpha ownership at native scale</h2><p>Magenta is transparent background, not new paving. Facade RGB and source files are preserved.</p>')
for key in ['station','cafe','bookshop','learning']:parts.append(f'<figure><a href="{key}-source-alpha-native.png">{key}: native source/alpha comparison</a><img loading="lazy" src="{key}-source-alpha-preview.jpg"></figure>')
parts.append('<h2>Two unimplemented protected decisions</h2><p>Archive:20px front corridor is technically traversed, but remains a poor public-space clearance. Proposed88px secondary gate is ONLY an overlay; wall unchanged. Station: canonical asphalt is immutable in main candidate. Separate native material candidate requires explicit approval and does not resolve the8px transfer.</p>')
for n in extra[10:]:parts.append(figure(n))
jpg(Image.open(D/'bridge-stop-contact-failures-overlay.png'),'bridge-stop-contact-failures-overlay-preview.jpg')
parts.append(figure('bridge-stop-contact-failures-overlay','FAIL: sampled original stop-pose ground contacts / strict model'))
parts.append('<h2>Craftsmanship comparison · same source pixel scale</h2><a href="craftsmanship-native-board.png">Native four-way crop board</a><img loading="lazy" src="craftsmanship-review.jpg">')
parts.append('<h2>Actual movement, not scripted coordinates</h2><p>Continuous WASD plus captured native joystick for fine corners; real collision and original movement speed. No teleport/direct position setter or collision override. Chromium touch emulation is NOT physical-device evidence. Failed driver attempts retained.</p>')
for key in ['world','bridge']:parts.append(f'<h3>{key} traversal</h3><video controls preload="metadata" src="{key}-traversal-review.mp4"></video><p><a href="{key}-traversal-native.mp4">Native-resolution continuous video</a> · <a href="{("movement-report"if key=="world"else"bridge-movement-report")}.json">Movement report</a></p>')
parts.append('<p><a href="body-clearance.json">Actual native foot contacts / sprite readback / near-rail occlusion</a> · <a href="protected-hashes.json">Protected hash report</a> · <a href="asset-provenance.json">Sources / exact changed asset inventory</a> · <a href="navigation-report.json">Route audit</a> · <a href="COVERAGE.md">Actual production coverage</a> · <a href="DEVICE_REVIEW.md">Physical-device handoff</a></p><p>Hardware WebGL, Android Chrome and iPhone Safari: NOT TESTED. Bakery required/unplaced; W0 rejected/Q1 unallocated. No main merge or public deployment. STOP for consolidated human review.</p></body></html>')
(D/'VISUAL_REVIEW.html').write_text('\n'.join(parts))
(D/'VISUAL_REVIEW.md').write_text('# Native visual review\n\n[Open full gallery](VISUAL_REVIEW.html) · [Decision/status](README.md) · [QA](QA.md). All JPEGs are review derivatives under1MB; original Phaser PNGs are unchanged. Human acceptance pending; station residuals and protected planning decisions remain.\n\n'+'\n'.join(f'## {n}\n\n[Before native]({n}-before-native.png) · [After native]({n}-after-native.png)\n\n![BEFORE left / AFTER right]({p})\n'for n,p in groups))
print('Gallery:',len(groups),'pairs; native originals retained; previews<1MB')
