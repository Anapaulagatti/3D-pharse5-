from pathlib import Path
from PIL import Image,ImageDraw
import json,html
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-station-clean';S=R/'assets-src/gate3/station-clean-v1';cap=json.loads((D/'native-captures.json').read_text());TAG='checkpoint/g3d-station-clean-review-20261025';RAW='https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/refs/tags/'+TAG+'/'
def jpeg(im,name,width=1800):
 im=im.convert('RGB')
 if im.width>width:im=im.resize((width,round(im.height*width/im.width)),Image.Resampling.NEAREST)
 q=88
 while True:
  im.save(D/name,quality=q,optimize=True)
  if(D/name).stat().st_size<1000000 or q<=45:break
  q-=5
 return name
def crop(entry,phase,box):
 row=next(r for r in cap['rows']if r['entry']==entry and r['phase']==phase);sx,sy=row['audit']['camera']['scroll'];return Image.open(D/(row['name']+'.png')).crop(tuple(round(v-(sx if i%2==0 else sy))for i,v in enumerate(box)))
trip=[]
for entry in ['station-all','station-facade','station-top','station-east','station-base']:
 frames=[Image.open(D/f'{entry}-{phase}-native.png').convert('RGB')for phase in ['before','clean','after']];w,h=frames[0].size;assert all(im.size==(w,h)for im in frames);board=Image.new('RGB',(w*3,h+40),'#183133');dr=ImageDraw.Draw(board)
 for i,(im,label)in enumerate(zip(frames,['ARCHIVED BEFORE / legacy','CLEAN SITE / no station art','AFTER / entirely FRESH active station'])):board.paste(im,(i*w,40));dr.text((i*w+10,12),label,fill='white')
 preview=entry+'-triptych.jpg';jpeg(board,preview,2100);trip.append({'entry':entry,'preview':preview,'native':[f'{entry}-{phase}-native.png'for phase in ['before','clean','after']]})
# Compact original-resolution native triptych around the exact same world box.
box=(2250,2100,3060,2825);parts=[crop('station-all',p,box)for p in ['before','clean','after']];native=Image.new('RGB',(2430,765),'#183133');dr=ImageDraw.Draw(native)
for i,(im,label)in enumerate(zip(parts,['BEFORE / archived','CLEAN EMPTY SITE','AFTER / fresh station'])):native.paste(im,(i*810,40));dr.text((i*810+10,12),label,fill='white')
native.save(D/'before-clean-after-native-triptych.png');jpeg(native,'before-clean-after-review.jpg',2100)
close=[]
for entry,box,title in [('station-facade',(2280,2340,2940,2640),'Front facade / original pixel scale'),('station-top',(2260,2130,2960,2440),'Complete NEW roof / clock / upper floor'),('station-east',(2850,2240,3060,2740),'Open-air platform-side approach / no old canopy'),('station-base',(2274,2570,2996,2825),'Fresh forecourt / step / road edge')]:
 im=crop(entry,'after',box);fn=entry+'-after-crop-1x.png';im.save(D/fn);jpg=entry+'-detail-review.jpg';jpeg(im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST),jpg,1800);close.append({'title':title,'native':fn,'preview':jpg})
# Live Juni at actual arrival, original source PNG remains untouched.
name='walk-fresh-station-entrance';a=json.loads((D/(name+'-audit.json')).read_text());cx,cy=a['state']['x'],a['state']['y'];sx,sy=a['camera']['scroll'];im=Image.open(D/(name+'-native.png')).crop((round(cx-sx-240),round(cy-sy-260),round(cx-sx+240),round(cy-sy+100)));im.save(D/'juni-at-new-entrance-native-crop.png');jpeg(im.resize((960,720),Image.Resampling.NEAREST),'juni-at-new-entrance-review.jpg',960)
# Genuine declared platform1 arrival, not just crossing the ownership strip.
name='walk-platform-transfer-out';a=json.loads((D/(name+'-audit.json')).read_text());cx,cy=a['state']['x'],a['state']['y'];sx,sy=a['camera']['scroll'];im=Image.open(D/(name+'-native.png')).crop((round(cx-sx-180),round(cy-sy-220),round(cx-sx+180),round(cy-sy+100)));im.save(D/'juni-at-platform1-native-crop.png');jpeg(im.resize((720,640),Image.Resampling.NEAREST),'juni-at-platform1-review.jpg',720)
# Independent new source parts, explicitly NOT a gameplay screenshot.
asset=Image.open(S/'fresh-station-independent.png').convert('RGBA');asset.save(D/'fresh-station-source-native.png');board=Image.new('RGB',(1368,1040),'#183133');dr=ImageDraw.Draw(board)
for i,name in enumerate(['roof','upper','facade']):
 im=Image.open(R/'public/assets/gate3/station-clean-world'/('fresh-'+name+'.png')).convert('RGBA');x=i%2*684;y=i//2*500+40;board.paste(im,(x,y),im);dr.text((x+10,y+8),name+' / FRESH source ownership',fill='white')
board.paste(asset,(684,540),asset);board.save(D/'fresh-source-layer-board-native.png');jpeg(board,'fresh-source-layer-review.jpg',1400)
# Original Gate1 benchmark alongside fresh actual Phaser at equal pixel scale.
ref=Image.open(R/'docs/gate1/GATE1_STREET_NATIVE.png').convert('RGB').crop((500,220,1140,860));now=crop('station-all','after',(2280,2110,2920,2750)).convert('RGB');out=Image.new('RGB',(1280,680),'#183133');out.paste(ref,(0,40));out.paste(now,(640,40));dr=ImageDraw.Draw(out);dr.text((10,12),'Approved Muneum / native1x DETAIL crop',fill='white');dr.text((650,12),'Fresh Hanbit / actual Phaser native1x',fill='white');out.save(D/'muneum-fresh-station-native-board.png');jpeg(out,'muneum-fresh-station-review.jpg',1280)
styles='body{font:17px/1.6 system-ui;background:#153034;color:#f1e6cc;max-width:1400px;margin:auto;padding:1em}a{color:#91e1d5}img{max-width:100%;height:auto;image-rendering:pixelated}video{max-width:100%}section{margin:2em 0}'
md=['# Hanbit — full clean rebuild review','', '**The active world uses ONLY the fresh station.** Old facade/roof/sign/canopy/planters/tree/owned ground/shadows are purged, not patched or retained. Archived BEFORE images are evidence only. Human artistic approval remains pending.','', '[Playable ZIP](HANBIT_CLEAN_REBUILD_REVIEW.zip) · [QA](QA.md) · [Purge/scope](purge-and-scope.json) · [Actual continuous controls](world-traversal-review.mp4)','', '![Before / clean / new](before-clean-after-review.jpg)','', '[Original native triptych](before-clean-after-native-triptych.png)',''];ht=[f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Fresh Hanbit — clean rebuild</title><style>{styles}</style></head><body><h1>Hanbit: full clean rebuild</h1><p>OLD visual assets are absent from active runtime. Fresh source is authored only from the completely clean plot and Muneum Gate1 reference. No old station donor or previous candidate. Human artistic acceptance pending.</p><p><a href="README.md">Handoff</a> · <a href="QA.md">QA / remaining limits</a> · <a href="HANBIT_CLEAN_REBUILD_REVIEW.zip">Playable ZIP</a></p><img src="before-clean-after-review.jpg"><p><a href="before-clean-after-native-triptych.png">Original native1x triptych</a></p>']
for q in trip:
 md+=['## '+q['entry'],'',f'![Triptych]({q["preview"]})','', ' · '.join(f'[{p}]({p})'for p in q['native']),''];ht.append('<section><h2>'+q['entry']+'</h2><img loading="lazy" src="'+q['preview']+'"><p>'+' · '.join(f'<a href="{p}">{p}</a>'for p in q['native'])+'</p></section>')
for q in close:
 md+=['## '+q['title'],'',f'![Detail]({q["preview"]})','',f'[Original native1x crop]({q["native"]})',''];ht.append(f'<section><h2>{html.escape(q["title"])}</h2><img loading="lazy" src="{q["preview"]}"><p><a href="{q["native"]}">Original native1x crop</a></p></section>')
for title,preview,original in [('Juni reaches the NEW station entrance — real controls','juni-at-new-entrance-review.jpg','juni-at-new-entrance-native-crop.png'),('Actual declared platform1 arrival2970,2530 / original E target confirmed','juni-at-platform1-review.jpg','juni-at-platform1-native-crop.png'),('Approved craftsmanship — same pixel scale','muneum-fresh-station-review.jpg','muneum-fresh-station-native-board.png'),('SOURCE ownership — not gameplay / all parts from one fresh painting','fresh-source-layer-review.jpg','fresh-source-layer-board-native.png')]:
 md+=['## '+title,'',f'![Review]({preview})','',f'[Native original]({original})',''];ht.append(f'<section><h2>{title}</h2><img src="{preview}"><p><a href="{original}">Native original</a></p></section>')
ht.append('<section><h2>Actual continuous station movement</h2><p>Original WASD/native joystick; four consecutive legs after initial review spawn. Entrance, genuine formerly-blocked platform transfer, side passage/return and crosswalk. No teleport, forced sprite frame, speed/collision/clock override. Physical phones NOT TESTED.</p><video controls preload="metadata" src="world-traversal-review.mp4"></video><p><a href="world-traversal-native.mp4">1280x1000 recording</a> · <a href="movement-report.json">Actual controls</a> · <a href="body-clearance.json">Native foot/body readback</a></p></section></body></html>')
(D/'VISUAL_REVIEW.md').write_text('\n'.join(md));(D/'VISUAL_REVIEW.html').write_text('\n'.join(ht));(D/'NATIVE_LINKS.md').write_text('# Direct native originals\n\n'+'\n'.join(f'- [{p.name}]({RAW}docs/gate3-station-clean/{p.name})'for p in sorted(D.glob('*.png')))+'\n');(D/'gallery-manifest.json').write_text(json.dumps({'actualNativeFrames':15,'triptychs':trip,'nativeCloseups':close,'previews':[{'name':p.name,'bytes':p.stat().st_size}for p in D.glob('*.jpg')],'originalPNGsUnmodified':True},indent=2)+'\n');assert all(p.stat().st_size<1000000 for p in D.glob('*.jpg'));print('Gallery complete:before/clean/new native triptychs,4 closeups,Juni,Muneum and real movement')
