from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,html
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-final';S=R/'assets-src/gate3/final-surgical-v1';TAG='checkpoint/g3d-final-surgical-review-20261025';RAW='https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/refs/tags/'+TAG+'/'
def jpeg(im,n,width=1800):
 im=im.convert('RGB')
 if im.width>width:im=im.resize((width,round(im.height*width/im.width)),Image.Resampling.NEAREST)
 q=88
 while True:
  im.save(D/n,quality=q,optimize=True)
  if (D/n).stat().st_size<1000000 or q<=45:break
  q-=5
 return n
entries=['farm','western-house','western-courtyard','house-court','station-precinct','station-upper','station-front','station-right','bridge-mainland','bridge-island','bridge-full','coast-middle','palace-entrance','retail-block'];comparisons=[]
def pair(left,right,title,name):
 a=Image.open(D/left);b=Image.open(D/right);assert a.size==b.size;out=Image.new('RGB',(a.width*2,a.height+36),'#163235');out.paste(a,(0,36));out.paste(b,(a.width,36));dr=ImageDraw.Draw(out);dr.text((12,10),'BEFORE / residual baseline',fill='white');dr.text((a.width+12,10),title,fill='white');jpeg(out,name);comparisons.append({'title':title,'preview':name,'before':left,'after':right})
for e in entries:pair(e+'-before-native.png',e+'-after-native.png',e+' / final MAIN retains old station',e+'-comparison.jpg')
for e in ['station-precinct','station-upper','station-front','station-right']:pair(e+'-before-native.png',e+'-station-candidate-native.png',e+' / NEW candidate NOT ADOPTED',e+'-candidate-comparison.jpg')
pair('world-before-overview-phaser.png','world-after-overview-phaser.png','AFTER MAIN / overview context only','world-overview-comparison.jpg');pair('world-before-overview-phaser.png','world-station-candidate-overview-phaser.png','NEW STATION candidate / overview context only','world-station-candidate-comparison.jpg')
for name in ['station-precinct-station-ground-native','station-front-station-ground-native','station-upper-station-ground-native']:
 jpeg(Image.open(D/(name+'.png')),name+'-preview.jpg',1400)
# Source-layer sheet explicitly labelled source, never passed off as gameplay.
asset=Image.open(S/'station-independent-complete.png').convert('RGBA');asset.save(D/'station-independent-source-native.png');board=Image.new('RGB',(asset.width*2,asset.height*2+65),'#223739');dr=ImageDraw.Draw(board);dr.text((12,12),'NATIVE SOURCE OWNERSHIP / not Phaser gameplay',fill='white')
for i,name in enumerate(['roof','upper','facade']):
 im=Image.open(R/'public/assets/gate3/final-station-candidate'/('station-'+name+'.png')).convert('RGBA');x=(i%2)*asset.width;y=(i//2)*asset.height+60;board.paste(im,(x,y),im);dr.text((x+12,y+5),name,fill='white')
board.paste(asset,(asset.width,asset.height+60),asset);board.save(D/'station-source-layers-native.png');jpeg(board,'station-source-layers-preview.jpg',1400)
# Farm IDs/anchors overlay ONLY a diagnostic copy, original native view untouched.
meta=json.loads((D/'FARM_PLOTS.json').read_text());cap=json.loads((D/'native-captures.json').read_text());row=next(r for r in cap['rows']if r['entry']=='farm'and r['phase']=='after');sx,sy=row['audit']['camera']['scroll'];farm=Image.open(D/'farm-after-native.png').convert('RGB');dr=ImageDraw.Draw(farm)
for p in meta['plots']:
 x,y,w,h=p['worldRect'];dr.rectangle((x-sx,y-sy,x+w-1-sx,y+h-1-sy),outline='#ffcf63',width=1);dr.text((x-sx+4,y-sy+3),p['id'],fill='white');x,y=p['interactionAnchor'];dr.ellipse((x-sx-4,y-sy-4,x-sx+4,y-sy+4),fill='#70ffd5')
farm.save(D/'farm-plot-registration-overlay.png');jpeg(farm,'farm-plot-overlay-preview.jpg',1280)
# Original-resolution close crops, no resampling. Registration read from actual
# native screenshot; source art is not substituted for in-engine evidence.
for e,phase,box in [('western-house','after',(550,880,720,1140)),('western-house','before',(550,880,720,1140)),('western-courtyard','after',(590,1400,740,1685)),('western-courtyard','before',(590,1400,740,1685)),('station-front','station-candidate',(2490,2450,2710,2630)),('bridge-mainland','after',(3090,3430,3250,3590))]:
 row=next(r for r in cap['rows']if r['entry']==e and r['phase']==phase);sx,sy=row['audit']['camera']['scroll'];im=Image.open(D/(row['name']+'.png'));im.crop((round(box[0]-sx),round(box[1]-sy),round(box[2]-sx),round(box[3]-sy))).save(D/(e+'-'+phase+'-crop-1x.png'))
for p in D.glob('*-pose*-native.png'):
 # Existing actual pose PNGs remain original. Extra readable copy only.
 jpeg(Image.open(p),p.stem+'-preview.jpg',900)
styles='body{background:#152f32;color:#f5ead3;font:17px/1.6 system-ui;max-width:1400px;margin:auto;padding:1em}a{color:#8ee4d8}img{max-width:100%;height:auto;image-rendering:pixelated}video{max-width:100%}section{margin:2em 0}strong{color:#ffda85}'
md=['# Final surgical native review','', '**Human visual acceptance pending.** Main retains old station; new station is isolated. No main merge/deployment. All previews<1MB, native originals untouched. No missing-reviewer-image dependency in this self-contained directive.','', '[Playable ZIP](G3D_FINAL_SURGICAL_REVIEW.zip) · [QA](QA.md) · [Source/scope](out-of-scope-audit.json) · [Farm metadata](FARM_PLOTS.json) · [Actual movement video](world-traversal-review.mp4)','']
ht=[f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Final G3-D surgical review</title><style>{styles}</style></head><body><h1>Final G3-D surgical review</h1><p><strong>Human artistic acceptance pending.</strong> New station NOT adopted. No main merge/deployment. Cropped source art is identified separately from actual Phaser screenshots.</p><p><a href="README.md">Decisions / handoff</a> · <a href="QA.md">QA</a> · <a href="FARM_PLOTS.json">Six farm plots</a> · <a href="G3D_FINAL_SURGICAL_REVIEW.zip">Playable ZIP</a></p>']
# Approved original craftsmanship against current1x detail; no artwork scaling.
board=Image.new('RGB',(2560,680),'#172d30');dr=ImageDraw.Draw(board)
refs=[('Approved Muneum','docs/gate1/GATE1_STREET_NATIVE.png'),('Approved Gate2.5','docs/gate25-refinement/AFTER_NATIVE_1X.png'),('New station CANDIDATE','docs/gate3-final/station-precinct-station-candidate-native.png'),('Same western historical house','docs/gate3-final/house-court-after-native.png')]
for i,(title,path)in enumerate(refs):
 im=Image.open(R/path).convert('RGB')
 if i<2:x=im.width//2-320;y=im.height//2-320
 else:
  entry='station-precinct'if i==2 else'house-court';phase='station-candidate'if i==2 else'after';row=next(q for q in cap['rows']if q['entry']==entry and q['phase']==phase);sx,sy=row['audit']['camera']['scroll'];wx,wy=(2260,2110)if i==2 else(500,850);x=round(wx-sx);y=round(wy-sy)
 board.paste(im.crop((x,y,x+640,y+640)),(i*640,40));dr.text((i*640+8,12),title+' /native1x crop',fill='white')
board.save(D/'craftsmanship-native-board.png');jpeg(board,'craftsmanship-preview.jpg',1800)
md+=['## Approved craftsmanship / native1x detail comparison','', 'Original Muneum and Gate2.5 references beside current isolated station and same historical house. This does not grant artistic approval.','', '![Craftsmanship](craftsmanship-preview.jpg)','', '[Original native1x board](craftsmanship-native-board.png)',''];ht.append('<section><h2>Approved craftsmanship / native1x detail</h2><img src="craftsmanship-preview.jpg"><p><a href="craftsmanship-native-board.png">Original native1x board</a>. Reference detail crops, not a new single gameplay scene.</p></section>')
for c in comparisons:
 md +=['## '+c['title'],'',f"![Before/after]({c['preview']})",'',f"[Original BEFORE]({c['before']}) · [Original candidate]({c['after']})",'']
 ht.append(f'<section><h2>{html.escape(c["title"])}</h2><img loading="lazy" src="{c["preview"]}" alt="Matched before/after"><p><a href="{c["before"]}">Original BEFORE</a> · <a href="{c["after"]}">Native candidate</a></p></section>')
for title,n in [('Ground stage: no OLD or NEW architecture, canonical props retained','station-precinct-station-ground-native-preview.jpg'),('Source roof / upper architecture / facade owners, NOT gameplay','station-source-layers-preview.jpg'),('Six plot reservations and interaction anchors: diagnostic overlay','farm-plot-overlay-preview.jpg')]:
 md+=['## '+title,'',f'![Review]({n})',''];ht.append(f'<section><h2>{html.escape(title)}</h2><img loading="lazy" src="{n}"></section>')
# Genuine stop/turn samples and red unsupported contact overlays.
body=json.loads((D/'body-clearance.json').read_text());motion=json.loads((D/'movement-report.json').read_text());contacts={q['frame']:q for q in body.get('capturedPoseContact',[])}
md+=['## Actual native stop/turn evidence','', 'Red diagnostic dots indicate unsupported projected native foot-contact pixels. These are real observed poses, not manually selected sprite frames. Bridge complete contact remains FAIL.','']
ht.append('<section><h2>Actual native stop/turn contacts: FAIL remains</h2><p>Red dots = unsupported contact; green = existing support. Source atlas/frame/scale unchanged.</p>')
for q in motion.get('poseShots',[]):
 name=q['name'];cx,cy=q['state']['x'],q['state']['y'];sx,sy=q['camera']['scroll'];box=(round(cx-sx-120),round(cy-sy-160),round(cx-sx+120),round(cy-sy+80))
 clean=Image.open(D/(name+'.png')).crop(box);clean.save(D/(name+'-crop-1x.png'));ov=Image.open(D/(name+'-body-overlay.png')).crop(box);ov.save(D/(name+'-contact-crop-1x.png'));preview=name+'-pose-review.jpg';jpeg(ov.resize((720,720),Image.Resampling.NEAREST),preview,720)
 status=contacts.get(name,{}).get('status','NOT TESTED');title=name+' /'+q['actualFrame']+' /'+status
 md +=[f'**{title}**','',f'![Actual pose]({preview})','',f'[Clean native1x]({name}-crop-1x.png) · [Native contact overlay]({name}-contact-crop-1x.png)','']
 ht.append(f'<h3>{html.escape(title)}</h3><img loading="lazy" src="{preview}" alt="Actual observed stop/turn pose"><p><a href="{name}-crop-1x.png">Clean native1x</a> · <a href="{name}-contact-crop-1x.png">Native contact overlay</a></p>')
ht.append('</section>')
for title,fn in [('Unadopted25px shoulder /4866px² proposal on current native bridge','bridge-support-proposal-native-overlay.png'),('Actual8px station transfer block','station-platform-strip-blocked-native.png')]:
 preview=fn.removesuffix('.png')+'-preview.jpg';jpeg(Image.open(D/fn),preview,1280);md+=['## '+title,'',f'![Technical evidence]({preview})','',f'[Original native]({fn})',''];ht.append(f'<section><h2>{html.escape(title)}</h2><img src="{preview}"><p><a href="{fn}">Native evidence</a></p></section>')
ht.append('<section><h2>Actual controls / declared independent cases</h2><p>One recording includes explicit scene reloads before farm, house, courtyard, station and bridge cases. Continuous input within each case; final bridge outward/return continuous. No teleport/collision/clock overrides. Emulation is not physical hardware.</p><video controls preload="metadata" src="world-traversal-review.mp4"></video><p><a href="world-traversal-native.mp4">1280x1000 movement recording</a> · <a href="movement-report.json">Control trace</a> · <a href="body-clearance.json">Native foot/body results</a></p></section></body></html>')
(D/'VISUAL_REVIEW.md').write_text('\n'.join(md));(D/'VISUAL_REVIEW.html').write_text('\n'.join(ht));(D/'gallery-manifest.json').write_text(json.dumps({'comparisons':comparisons,'previews':[{'file':p.name,'bytes':p.stat().st_size}for p in D.glob('*.jpg')],'nativePNGsUnmodified':True},indent=2)+'\n')
(D/'NATIVE_LINKS.md').write_text('# Direct immutable native PNG evidence\n\n'+'\n'.join(f'- [{p.name}]({RAW}docs/gate3-final/{p.name})'for p in sorted(D.glob('*.png')))+'\n');print('Gallery:',len(comparisons),'matched comparisons; previews<1MB')
