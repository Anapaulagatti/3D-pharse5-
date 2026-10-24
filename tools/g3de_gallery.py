"""Light review copies/crops; never modify original native Phaser PNGs."""
from pathlib import Path
import json,html
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-residual';S=R/'assets-src/gate3/residual-v1';cap=json.loads((D/'native-captures.json').read_text());m=json.loads((R/'public/assets/gate3/residual-world/manifest.json').read_text());old=json.loads((R/'public/assets/gate3/aligned-world/manifest.json').read_text())
def jpg(im,name,w=1600):
 im=im.convert('RGB')
 if im.width>w:im=im.resize((w,round(im.height*w/im.width)),Image.Resampling.NEAREST)
 for q in [88,80,70,60]:
  im.save(D/name,quality=q,optimize=True)
  if(D/name).stat().st_size<1000000:return name
 raise ValueError(name)
def pair(a,b,name,labels=('BEFORE /9827761','AFTER /candidate, HUMAN REVIEW PENDING')):
 a=Image.open(a).convert('RGB');b=Image.open(b).convert('RGB');assert a.size==b.size;out=Image.new('RGB',(a.width*2,a.height+30),'#172d30');out.paste(a,(0,30));out.paste(b,(a.width,30));dr=ImageDraw.Draw(out);dr.text((8,8),labels[0],fill='white');dr.text((a.width+8,8),labels[1],fill='white');return jpg(out,name,1900)
groups=[]
for row in cap['rows']:
 if row['scene']!='residual-world':continue
 n=row['entry'];groups.append((n,pair(D/(n+'-before-native.png'),D/(n+'-after-native.png'),n+'-comparison.jpg')))
proposalPairs=[]
for n,kind in [('station-front','road'),('station-precinct','road'),('archive-corridor','gate'),('palace-east','gate')]:
 preview=pair(D/(n+'-after-native.png'),D/(n+'-'+kind+'-proposal-native.png'),n+'-'+kind+'-comparison.jpg',('CURRENT /protected state','PROPOSAL ONLY /NOT ADOPTED'))
 proposalPairs.append((n,kind,preview))
# Original-resolution crops taken from real native Phaser screenshots.
for phase in ['before','after']:
 row=next(r for r in cap['rows']if r['entry']=='station-tree'and r['phase']==phase);sx,sy=row['audit']['camera']['scroll'];im=Image.open(D/(row['name']+'.png'));im.crop((2820-sx,2490-sy,3000-sx,2710-sy)).save(D/('tree-'+phase+'-native-crop.png'))
pair(D/'tree-before-native-crop.png',D/'tree-after-native-crop.png','tree-detail-comparison.jpg');a=Image.open(D/'tree-before-native-crop.png');b=Image.open(D/'tree-after-native-crop.png');out=Image.new('RGB',(a.width*6,a.height*3+30),'#172d30');out.paste(a.resize((a.width*3,a.height*3),Image.Resampling.NEAREST),(0,30));out.paste(b.resize((b.width*3,b.height*3),Image.Resampling.NEAREST),(a.width*3,30));jpg(out,'tree-detail-enlarged.jpg',1800)
# Same registered approved graybox/axis as native current screenshots.
approved=json.loads((R/'assets-src/world-gate1/plan.json').read_text());row=next(r for r in cap['rows']if r['entry']=='palace-compound'and r['phase']=='after');sx,sy=row['audit']['camera']['scroll'];im=Image.open(D/(row['name']+'.png')).convert('RGB');Image.open(R/'docs/world-gate1/GRAYBOX_NATIVE_4096x4608.png').crop((sx,sy,sx+im.width,sy+im.height)).save(D/'palace-approved-graybox-native.png');dr=ImageDraw.Draw(im)
for q in approved['boundaries']:
 x,y,w,h=q['rect'];dr.rectangle((x-sx,y-sy,x+w-1-sx,y+h-1-sy),outline='#65e4ef',width=2)
x,y,w,h=1510,290,1050,460;dr.rectangle((x-sx,y-sy,x+w-sx,y+h-sy),outline='#ffe180',width=2);dr.line((2048-sx,290-sy,2048-sx,1120-sy),fill='#ff70c3',width=2);im.save(D/'palace-registered-axis-overlay.png')
# Source alpha ownership boards at native scale, labelled source evidence.
for key in ['station','cafe','bookshop','learning','station-platform-canopy']:
 a=next(o for o in old['objects']if o['id']=='registration/'+key);b=next(o for o in m['objects']if o['id']==a['id']);left=Image.open(R/'public'/a['image']).convert('RGBA');right=Image.open(R/'public'/b['image']).convert('RGBA');w,h=left.size;out=Image.new('RGBA',(w*3,h+30),'#875473');out.alpha_composite(left,(0,30));out.alpha_composite(right,(w,30));out.paste(right.getchannel('A').convert('RGB'),(w*2,30));dr=ImageDraw.Draw(out);dr.text((6,8),'SOURCE /before alpha',fill='white');dr.text((w+6,8),'SOURCE /derived alpha',fill='white');dr.text((w*2+6,8),'ownership mask',fill='white');out.convert('RGB').save(D/(key+'-source-alpha-native.png'));jpg(out,key+'-source-alpha-preview.jpg')
# Explicit collision proposal/retained platform-strip overlays, actual native scene underlay.
for entry,phase in [('archive-corridor','after'),('archive-corridor','gate-proposal'),('station-right','after')]:
 row=next(r for r in cap['rows']if r['entry']==entry and r['phase']==phase);sx,sy=row['audit']['camera']['scroll'];im=Image.open(D/(row['name']+'.png')).convert('RGBA');ol=Image.new('RGBA',im.size);dr=ImageDraw.Draw(ol)
 if entry=='archive-corridor':
  rect=(2536,1040,88,25);colour=(80,255,170,130)if phase=='gate-proposal'else(255,50,90,150);text='88px hypothetical opening /NOT ADOPTED'if phase=='gate-proposal'else'CURRENT protected wall /blocked'
 else:rect=(2950,2626,8,129);colour=(255,50,90,170);text='8px remains CLOSED /no90x36 connector'
 x,y,w,h=rect;dr.rectangle((x-sx,y-sy,x+w-1-sx,y+h-1-sy),fill=colour);dr.text((x-sx-160,y-sy-25),text,fill='white',stroke_width=1,stroke_fill='black');Image.alpha_composite(im,ol).save(D/(entry+'-'+phase+'-collision-overlay.png'))
# Shared material wrap/source provenance board, not gameplay.
a=Image.open(R/'assets-src/gate3/reconciliation-v1/ocean-authored.png').convert('RGB');b=Image.open(S/'ocean-native-wrap-repaired.png').convert('RGB');out=Image.new('RGB',(768,290),'#172d30');dr=ImageDraw.Draw(out)
for i,im in enumerate([a,b]):
 band=Image.new('RGB',(384,256));band.paste(im.crop((1344,700,1536,956)),(0,0));band.paste(im.crop((0,700,192,956)),(192,0));out.paste(band,(i*384,30));dr.text((i*384+6,8),['SOURCE wrap BEFORE','SOURCE wrap AFTER /native texels'][i],fill='white')
out.save(D/'ocean-native-source-wrap-board.png');jpg(out,'ocean-source-wrap-preview.jpg')
# Same-scale approved craftsmanship references; not a new-building authorship claim.
paths=['docs/gate1/GATE1_STREET_NATIVE.png','docs/gate25-refinement/AFTER_NATIVE_1X.png','docs/gate3-residual/station-front-road-proposal-native.png','docs/gate3-residual/palace-entrance-after-native.png'];out=Image.new('RGB',(2048,550),'#172d30');dr=ImageDraw.Draw(out)
for i,path in enumerate(paths):
 im=Image.open(R/path).convert('RGB');x=im.width//2-256;y=im.height//2-250;out.paste(im.crop((x,y,x+512,y+500)),(i*512,45));dr.text((i*512+6,10),['Approved Muneum','Approved Gate2.5','Station road PROPOSAL','Palace current'][i],fill='white')
out.save(D/'craftsmanship-native-board.png');jpg(out,'craftsmanship-preview.jpg',1800)
extras=['world-before-overview-phaser','world-after-overview-phaser','palace-approved-graybox-native','palace-registered-axis-overlay','archive-corridor-after-collision-overlay','archive-corridor-gate-proposal-collision-overlay','station-right-after-collision-overlay','bridge-full-geometry-proposal-native']
for n in extras:jpg(Image.open(D/(n+'.png')),n+'-preview.jpg')
# Actual pose crops, original resolution plus native context. Never synthesize a pose.
poses=[]
if(D/'movement-report.json').exists():
 motion=json.loads((D/'movement-report.json').read_text())
 for row in motion.get('poseShots',[]):
  sx,sy=row['camera']['scroll'];cx,cy=round(row['state']['x']),round(row['state']['y']);im=Image.open(D/(row['name']+'.png')).convert('RGB');im.crop((cx-sx-120,cy-sy-170,cx-sx+120,cy-sy+70)).save(D/(row['name']+'-crop.png'))
  crop=Image.open(D/(row['name']+'-crop.png'));jpg(crop.resize((720,720),Image.Resampling.NEAREST),row['name']+'-pose-preview.jpg',720);poses.append(row)
style='body{font:17px/1.55 system-ui;max-width:1500px;margin:2em auto;padding:0 1em;background:#162d30;color:#f3e8d4}a{color:#9ce1e0}img,video{max-width:100%;height:auto}figure{margin:2em 0}strong{color:#ffcf8b}'
parts=[f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>G3-D residual correction review</title><style>{style}</style></head><body><h1>G3-D · consolidated residual correction</h1>', '<p><strong>Human artistic acceptance withheld. Main bridge stop/turn clearance remains FAIL; road restoration,88px gate and bridge support shoulders are explicitly separate proposals.</strong> Six marked reviewer images were not attached/requested; annotation matching NOT TESTED. No main merge or public deployment.</p>','<p>All previews under1MB. Actual native PNGs are unmodified Phaser POST_RENDER at zoom1,DPR1 (detail1280×900, wide2048×1280). Open/download at100% for pixel inspection. Enlargements use nearest neighbor. Source/geometry boards are labelled technical evidence, never substituted for gameplay.</p>','<p><a href="G3D_RESIDUAL_REVIEW.zip">PLAYABLE ZIP</a> · <a href="README.md">Decisions / remaining issues</a> · <a href="QA.md">QA</a> · <a href="SOURCE_OWNERSHIP.md">Sources / exact masks</a></p>']
def fig(n,caption=''):return f'<figure><figcaption>{html.escape(caption or n)} · <a href="{n}.png">native original</a></figcaption><img loading="lazy" src="{n}-preview.jpg"></figure>'
parts.append('<h2>Complete world · same overview framing, scaled context only</h2>')
for n in extras[:2]:parts.append(fig(n))
parts.append('<h2>Twenty matched native BEFORE / AFTER views</h2>')
for n,preview in groups:parts.append(f'<figure id="{n}"><figcaption><b>{n}</b> · <a href="{n}-before-native.png">BEFORE1x</a> · <a href="{n}-after-native.png">AFTER1x</a></figcaption><img loading="lazy" src="{preview}"></figure>')
parts.append('<h2>Station crown · original-resolution crops and3x nearest enlargement</h2><p>Native pot/trunk/shadow/forecourt preserved; only missing crown outside2958 completed. Foreground ownership fixed; no oversized foliage cover.</p><p><a href="tree-before-native-crop.png">Before native crop</a> · <a href="tree-after-native-crop.png">After native crop</a></p><img loading="lazy" src="tree-detail-enlarged.jpg">')
parts.append('<h2>Explicit unadopted road and gateway candidates</h2><p>Left is CURRENT; right is PROPOSAL. Canonical road/approved wall stay unchanged in main. Real keyboard tests show the current wall blocks and proposed88px opening reaches the archive threshold; that is not architectural approval. Original8px platform strip stays closed.</p>')
for n,kind,preview in proposalPairs:parts.append(f'<figure><figcaption>{n} · <a href="{n}-after-native.png">CURRENT native</a> · <a href="{n}-{kind}-proposal-native.png">PROPOSED native</a></figcaption><img loading="lazy" src="{preview}"></figure>')
for n in extras[2:7]:parts.append(fig(n))
parts.append('<h2>Bridge geometry proposal · NO live geometry/collision amendment</h2><p>Cyan=current modeled physical edge; magenta=proposed visible support area; yellow=model route. Conservative native feet keep below-anchor toe offsets. Three bounded areas total4866px²; maximum search shoulder25px. These are floor-clearance quantities, not production bridge artwork/railing-engineering acceptance. Any new structural surface must be visibly authored and reviewed before collision expansion. Source endpoints/Juni/actual bridge stay unchanged.</p>')
parts.append(fig(extras[7]));parts.append('<p><a href="bridge-clearance-proposal.json">Exact dimensions, method and path</a> · <a href="body-clearance.json">Actual current contacts / failure samples / rendered-body evidence</a> · <a href="gate-movement.json">Real current/proposed gateway and retained strip behavior</a></p>')
parts.append('<h2>Native source ownership · original files immutable</h2>')
for key in ['station','station-platform-canopy','cafe','bookshop','learning']:parts.append(f'<figure><a href="{key}-source-alpha-native.png">{key} source/alpha1x board</a><img loading="lazy" src="{key}-source-alpha-preview.jpg"></figure>')
parts.append('<h2>Shared ocean source wrap · native source board, not gameplay</h2><p>The1536×1024 source was not periodic. Both sides of visible3180 seam already used that same source. Minimum-error native overlap ownership repairs its X/Y edges with original integer-coordinate texels; period/phase stay exact. No blur/recolor/mirror/scale; approved Jeju protection bitmap remains exact. A broader water-mask trial was rejected/not installed.</p><a href="ocean-native-source-wrap-board.png">Native source board</a><img loading="lazy" src="ocean-source-wrap-preview.jpg">')
parts.append('<h2>Approved craftsmanship at the same pixel scale</h2><a href="craftsmanship-native-board.png">Native reference board</a><img loading="lazy" src="craftsmanship-preview.jpg">')
parts.append('<h2>Actual continuous gameplay</h2><p>Original WASD plus captured original joystick for fine corner control. Continuous route, no teleport/collision override/animation forcing. Full bridge outward and return legs included. Chromium touch emulation is NOT physical-device evidence. Video is lossy movement evidence; untouched PNGs prove pixels.</p><video controls preload="metadata" src="world-traversal-review.mp4"></video><p><a href="world-traversal-native.mp4">Native-resolution video</a> · <a href="movement-report.json">Recorded controls / poses / full route</a> · <a href="video-provenance.json">Recording provenance</a></p>')
parts.append('<h2>Genuine native stop/turn captures · both directions</h2><p>Read-only POST_RENDER listener observed these original atlas poses. No sprite/frame/clock mutation. Physical support remains a separate FAIL/proposal; a visible pose is not a clearance PASS.</p>')
for row in poses:parts.append(f'<figure><figcaption>{html.escape(row["leg"])} · {html.escape(row["actualFrame"])} · <a href="{row["name"]}.png">full native</a> · <a href="{row["name"]}-crop.png">native1x crop</a></figcaption><img loading="lazy" src="{row["name"]}-pose-preview.jpg"></figure>')
parts.append('<p><a href="protected-hashes.json">Protected source/tag hashes</a> · <a href="asset-provenance.json">Exact changed derived files</a> · <a href="technical-qa.json">Native technical report</a> · <a href="navigation-report.json">Retained route failures</a> · <a href="COVERAGE.md">Coverage</a> · <a href="DEVICE_REVIEW.md">Physical-device review/export</a></p><p>Bakery required/unplaced,W0 rejected,Q1 unallocated. Station8px transfer/projections/inherited route issues remain. Hardware WebGL and physical Android Chrome/iPhone Safari NOT TESTED. STOP for consolidated human artistic/spatial review.</p></body></html>')
(D/'VISUAL_REVIEW.html').write_text('\n'.join(parts));(D/'VISUAL_REVIEW.md').write_text('# Consolidated native visual review\n\n[Playable ZIP](G3D_RESIDUAL_REVIEW.zip) · [Full gallery](VISUAL_REVIEW.html) · [Decisions](README.md) · [QA](QA.md). JPEG previews under1MB; native PNGs unchanged. No human acceptance inferred from tests.\n\n'+'\n'.join(f'## {n}\n\n[Before native]({n}-before-native.png) · [After native]({n}-after-native.png)\n\n![BEFORE left / AFTER right]({preview})\n'for n,preview in groups)+'\n## Unadopted proposals\n\n'+'\n'.join(f'### {n} / {kind}\n\n[Current native]({n}-after-native.png) · [Proposed native]({n}-{kind}-proposal-native.png)\n\n![Current left / proposal right]({preview})\n'for n,kind,preview in proposalPairs)+'\n[Bridge support geometry overlay, not applied](bridge-full-geometry-proposal-native.png) · [Exact proposal](bridge-clearance-proposal.json) · [Actual video](world-traversal-review.mp4).\n')
print('Gallery:',len(groups),'matched pairs,4 isolated comparisons,',len(poses),'real pose captures; previews<1MB')
