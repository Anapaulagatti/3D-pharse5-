"""Review derivatives only; native Phaser originals remain untouched."""
from pathlib import Path
import json,html
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-reconciliation'
TAG='checkpoint/g3d-spatial-reconciliation-review-20261024';RAW='https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/refs/tags/'+TAG+'/'
def jpg(im,out,maxw=1600):
 im=im.convert('RGB')
 if im.width>maxw:im.resize((maxw,round(im.height*maxw/im.width)),Image.Resampling.NEAREST).save(out,quality=87,optimize=True)
 else:im.save(out,quality=87,optimize=True)
 while out.stat().st_size>=1000000:
  q=Image.open(out);q.save(out,quality=70,optimize=True)
 return out.name
cap=json.loads((D/'native-captures.json').read_text());groups=[]
for row in cap['rows']:
 if '-after-native'not in row['name']:continue
 name=row['name'].replace('-after-native','');before=D/(name+'-before-native.png');after=D/(name+'-after-native.png');a=Image.open(before).convert('RGB');b=Image.open(after).convert('RGB');board=Image.new('RGB',(a.width*2,a.height+36),'#172d30');board.paste(a,(0,36));board.paste(b,(a.width,36));d=ImageDraw.Draw(board);d.text((12,10),'BEFORE / previous zoning candidate',fill='white');d.text((a.width+12,10),'AFTER / reconciliation candidate - NOT APPROVED',fill='white');preview=jpg(board,D/(name+'-comparison.jpg'),1900);groups.append((name,preview,before.name,after.name))
for n in ['world-before-overview-phaser','world-after-overview-phaser','palace-approved-graybox-native','palace-runtime-registration-overlay','palace-compound-proposal-native','palace-court-proposal-native']:
 jpg(Image.open(D/(n+'.png')),D/(n+'-preview.jpg'))
# Same-scale source craftsmanship comparison; independent regions, no artificial sharpening.
paths=['docs/gate1/GATE1_STREET_NATIVE.png','docs/gate25-refinement/AFTER_NATIVE_1X.png','docs/gate3-reconciliation/station-forecourt-after-native.png','docs/gate3-reconciliation/palace-court-after-native.png'];board=Image.new('RGB',(2048,600),'#172d30');draw=ImageDraw.Draw(board)
for i,p in enumerate(paths):
 im=Image.open(R/p).convert('RGB');cx=im.width//2;cy=im.height//2;crop=im.crop((max(0,cx-256),max(0,cy-270),max(0,cx-256)+512,max(0,cy-270)+540));board.paste(crop,(i*512,50));draw.text((i*512+8,12),['Approved Muneum','Accepted Gate2.5 district','Current canonical forecourt','Current palace court'][i],fill='white')
board.save(D/'craftsmanship-native-board.png',optimize=True);jpg(board,D/'craftsmanship-review.jpg',1800)
style='body{font:17px/1.5 system-ui;background:#162d30;color:#f2e8d3;max-width:1500px;margin:2em auto;padding:0 1em}a{color:#9ce1e0}img,video{max-width:100%;height:auto}figure{margin:2em 0}strong{color:#ffd28f}table{border-collapse:collapse}td,th{border:1px solid #6c8986;padding:.6em}'
intro='''<h1>G3-D spatial reconciliation · human review candidate</h1><p><strong>NOT APPROVED. Palace architecture/footprint conflicts, station residual joins, platform transfer, Bakery and device evidence remain open.</strong> Eight marked reviewer images were not provided; exact annotation coverage is NOT TESTED. No main merge or public deployment.</p><p>JPEGs below are lightweight review derivatives. Native PNG links are unmodified Phaser readback at 1:1 (1280×900; full palace/station 2048×1280). Browser display may shrink them; download/open at 100% for pixel inspection. Before/after pairs share camera coordinates. Technical captures at blocked review poses are not proof of playable entrances.</p><p><a href="README.md">Decision/status</a> · <a href="SPATIAL_FIDELITY.md">Geometry and planning conflicts</a> · <a href="QA.md">QA</a> · <a href="SOURCE_OWNERSHIP.md">Sources/alpha/chunk audit</a> · <a href="G3D_SPATIAL_RECONCILIATION_REVIEW.zip">PLAYABLE ZIP</a></p>'''
parts=[f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>G3-D spatial reconciliation review</title><style>{style}</style></head><body>',intro]
parts.append('<h2>Full-world framing</h2><p>Overview only; use native evidence below for detail.</p>')
for n in ['world-before-overview-phaser','world-after-overview-phaser']:parts.append(f'<figure><figcaption>{n} · <a href="{n}.png">original Phaser overview</a></figcaption><img loading="lazy" src="{n}-preview.jpg"></figure>')
parts.append('<h2>Approved geometry versus current visible scene</h2><p>Identical registered native world rectangle. Yellow: approved building support reservations. Cyan: wall supports. Pink: ceremonial court/axis. Roof projections are not footprints. Main-hall source plinth extends40px beyond approved support; source academy is cropped. No hidden plan amendment.</p>')
for n in ['palace-approved-graybox-native','palace-runtime-registration-overlay']:parts.append(f'<figure><a href="{n}.png">{n} · native</a><img loading="lazy" src="{n}-preview.jpg"></figure>')
parts.append('<h2>Native before/after</h2>')
for name,preview,before,after in groups:parts.append(f'<figure id="{name}"><figcaption><b>{name}</b> · <a href="{before}">BEFORE native</a> · <a href="{after}">AFTER native</a></figcaption><img loading="lazy" src="{preview}"></figure>')
parts.append('<h2>Separate main-hall derived proposal · NOT ADOPTED</h2><p>Native original facade pixels registered to plinth bottom750, roof retained. Main candidate remains unchanged. Collision/door support still requires final review. Academy clipped-source conflict remains separate.</p>')
for n in ['palace-compound-proposal-native','palace-court-proposal-native']:parts.append(f'<figure><a href="{n}.png">{n} · native</a><img loading="lazy" src="{n}-preview.jpg"></figure>')
parts.append('<h2>Craftsmanship reference at matching pixel scale</h2><p>Four512px native crops; approved references preserved. This comparison is not automatic art acceptance.</p><a href="craftsmanship-native-board.png">Native comparison board</a><img loading="lazy" src="craftsmanship-review.jpg">')
parts.append('<h2>Actual WASD traversal</h2><p>Continuous real keyboard movement; no teleport/collision overrides. Foot movement and visible-body clearance are reported separately. Failed attempts remain in the report.</p><video controls preload="metadata" src="world-traversal-review.mp4"></video><p><a href="world-traversal-native.mp4">Native-resolution recording</a> · <a href="movement-report.json">Actual movement</a> · <a href="body-clearance.json">Body clearance</a> · <a href="navigation-report.json">All planned route centerlines</a></p>')
parts.append('<h2>Preservation and limitations</h2><p><a href="protected-hashes.json">1440-source hash report</a> · <a href="preservation-details.json">Latest-checkpoint/registration/Jeju exception</a> · <a href="ownership-audit.json">Adjacent chunks/foreground inventory</a> · <a href="technical-qa.json">Native pixel readback</a> · <a href="COVERAGE.md">Coverage</a> · <a href="DEVICE_REVIEW.md">Physical-device handoff</a></p><p>Physical Android Chrome/iPhone Safari and hardware WebGL performance: NOT TESTED. Bakery remains required/unplaced; W0 rejected/Q1 land unallocated. Stop for consolidated human review.</p></body></html>')
(D/'VISUAL_REVIEW.html').write_text('\n'.join(parts));(D/'VISUAL_REVIEW.md').write_text('# Visual review\n\n[Open gallery](VISUAL_REVIEW.html). Native PNGs remain untouched; lightweight JPEGs are derivatives. Main-hall proposal is separate and not adopted. Physical hardware/device testing is NOT TESTED.\n\n'+'\n'.join(f'## {n}\n\n[Before native]({bef}) · [After native]({aft})\n\n![Before left / after right]({p})\n'for n,p,bef,aft in groups)+'\n')
print('Gallery:',len(groups),'pairs; previews under1MB')
