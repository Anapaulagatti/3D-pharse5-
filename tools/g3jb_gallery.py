"""Original-scale Phaser crops and separately labelled technical overlays."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,html,numpy as np
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-jeju-bridges';S=R/'assets-src/gate3/jeju-bridges-v1';cap=json.loads((D/'native-captures.json').read_text());plan=json.loads((D/'walk-plan.json').read_text());RAW='https://raw.githubusercontent.com/Anapaulagatti/3D-pharse5-/refs/tags/checkpoint/g3d-jeju-two-bridges-review-20261025/'
def crop(entry,phase,box):
 q=next(q for q in cap['rows']if q['entry']==entry and q['phase']==phase);sx,sy=map(round,q['audit']['camera']['scroll']);return Image.open(D/(q['name']+'.png')).convert('RGB').crop((box[0]-sx,box[1]-sy,box[2]-sx,box[3]-sy))
def jpg(im,name,width=1500):
 if im.width>width:im=im.resize((width,round(im.height*width/im.width)),Image.Resampling.NEAREST)
 for quality in [88,80,72,64,56,48]:
  im.convert('RGB').save(D/name,quality=quality,optimize=True)
  if(D/name).stat().st_size<1000000:break
 assert(D/name).stat().st_size<1000000
rows=[]
for key,box in [('a',(2980,3340,3620,3720)),('b',(2980,3860,3640,4160))]:
 frames=[crop(f'bridge-{key}-full',phase,box)for phase in ['before','after']]
 for im,phase in zip(frames,['before','after']):im.save(D/f'bridge-{key}-{phase}-crop-1x.png')
 w,h=frames[0].size;out=Image.new('RGB',(w*2,h+35),'#153136');dr=ImageDraw.Draw(out)
 for i,(im,title)in enumerate(zip(frames,['BEFORE / native1x','AFTER / native1x / human art review'])):out.paste(im,(i*w,35));dr.text((i*w+8,10),key.upper()+' '+title,fill='white')
 out.save(D/f'bridge-{key}-before-after-native-board.png');jpg(out,f'bridge-{key}-comparison.jpg')
 # Overlay is diagnostic only; never replaces unannotated native evidence.
 overlay=frames[1].copy();dr=ImageDraw.Draw(overlay);x,y=box[:2];pol=json.loads((S/'scope.json').read_text())['polygons'][key.upper()];p=[(a-x,b-y)for a,b in pol];dr.line(p+[p[0]],fill='#ed84c1',width=1)
 for leg in plan['legs']:
  if leg['id']==f'bridge-{key}-walk-out':dr.line([(a-x,b-y)for a,b in leg['points']],fill='#63ffbc',width=2)
 pa=np.array(Image.open(S/f'{key.upper()}-visible-deck-mask.png').crop(box))>0
 from scipy.ndimage import binary_erosion
 edge=pa&~binary_erosion(pa);arr=np.array(overlay);arr[edge]=[100,215,255];overlay=Image.fromarray(arr);overlay.save(D/f'bridge-{key}-alignment-overlay-native.png');jpg(overlay.resize((overlay.width*2,overlay.height*2),Image.Resampling.NEAREST),f'bridge-{key}-alignment-review.jpg')
 rows.append({'bridge':key.upper(),'before':f'bridge-{key}-before-crop-1x.png','after':f'bridge-{key}-after-crop-1x.png','comparison':f'bridge-{key}-comparison.jpg','overlay':f'bridge-{key}-alignment-overlay-native.png','worldBox':box})
for key,box in [('a-mainland',(3000,3380,3260,3575)),('a-island',(3400,3550,3590,3710)),('b-mainland',(3020,3890,3250,4050)),('b-island',(3440,3990,3630,4140))]:
 for phase in ['before','after']:
  im=crop('bridge-'+key,phase,box);im.save(D/f'bridge-{key}-{phase}-detail-1x.png')
  if phase=='after':jpg(im.resize((im.width*3,im.height*3),Image.Resampling.NEAREST),f'bridge-{key}-detail-review.jpg')
md=['# TWO separate Jeju crossings — native Phaser review','','Hanbit Station is HUMAN APPROVED AND LOCKED. Bridge artistic acceptance remains pending. All unannotated native PNGs are actual Phaser readbacks; only review JPEGs are resized.','','[Playable ZIP](JEJU_TWO_BRIDGES_REVIEW.zip) · [QA](QA.md) · [Gameplay video](world-traversal-review.mp4) · [Physical device checklist](DEVICE_REVIEW.md)','']
ht=['<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Two Jeju crossings review</title><style>body{background:#153136;color:#f7eed9;font:17px/1.6 system-ui;max-width:1400px;margin:auto;padding:1em}a{color:#9ee9db}img,video{max-width:100%;height:auto;image-rendering:pixelated}section{margin:2em 0}</style></head><body><h1>Two Jeju crossings</h1><p>Hanbit APPROVED AND LOCKED. Native Phaser before/after; human bridge artistic approval pending.</p><p><a href="JEJU_TWO_BRIDGES_REVIEW.zip">Playable ZIP</a> · <a href="QA.md">QA</a> · <a href="DEVICE_REVIEW.md">Physical device handoff</a></p>']
for q in rows:
 k=q['bridge'].lower();md+=['## Bridge '+q['bridge']+' — '+('upper / northern'if k=='a'else'lower / southern'),'',f'![Before / after]({q["comparison"]})','',f'[BEFORE native1x]({q["before"]}) · [AFTER native1x]({q["after"]}) · [Full native frame](bridge-{k}-full-after-native.png)','',f'![Measured overlay](bridge-{k}-alignment-review.jpg)','',f'[Native geometry overlay]({q["overlay"]}) — cyan: actual top plane; green: selected safe corridor; pink: maximum edit boundary. Gameplay validation is separate.',''];ht.append(f'<section><h2>Bridge {q["bridge"]}</h2><img src="{q["comparison"]}"><p><a href="{q["before"]}">BEFORE native1x</a> · <a href="{q["after"]}">AFTER native1x</a> · <a href="bridge-{k}-full-after-native.png">Full native frame</a></p><img src="bridge-{k}-alignment-review.jpg"><p><a href="{q["overlay"]}">Native technical overlay</a>: cyan top plane, green selected corridor, pink edit scope.</p></section>')
 for side in ['mainland','island']:
  stem=f'bridge-{k}-{side}';md +=[f'### {side} landing','',f'![Native detail review]({stem}-detail-review.jpg)','',f'[BEFORE native1x]({stem}-before-detail-1x.png) · [AFTER native1x]({stem}-after-detail-1x.png)',''];ht.append(f'<section><h3>{side} landing</h3><img src="{stem}-detail-review.jpg"><p><a href="{stem}-before-detail-1x.png">Before1x</a> · <a href="{stem}-after-detail-1x.png">After1x</a></p></section>')
ht.append('<h2>Original-control walk/run and stop/turn</h2><p>Two separate bridge review spawns, each followed by four uninterrupted walk-out/return/run-out/return legs. No in-route teleport, speed, pose, clock or collision override. Physical phones NOT TESTED.</p><video controls preload="metadata" src="world-traversal-review.mp4"></video><p><a href="world-traversal-native.mp4">Original-size recording</a> · <a href="body-clearance.json">Native contact/body QA</a></p><h2>Approved Hanbit remains exact</h2><p><a href="approved-hanbit-preserved-native.png">Native current station proof</a> · <a href="protected-hashes.json">Protected source/registration hashes</a></p></body></html>');md+=['## Actual gameplay','', '[Continuous video](world-traversal-review.mp4) · [Original-size video](world-traversal-native.mp4) · [Actual original-control records](movement-report.json) · [Native contacts and occlusion](body-clearance.json)','', '## Approved station','', '[Native Hanbit preservation proof](approved-hanbit-preserved-native.png) · [Protected assets](protected-hashes.json)','']
(D/'VISUAL_REVIEW.md').write_text('\n'.join(md));(D/'VISUAL_REVIEW.html').write_text('\n'.join(ht));(D/'NATIVE_LINKS.md').write_text('# Immutable native originals\n\n'+'\n'.join(f'- [{p.name}]({RAW}docs/gate3-jeju-bridges/{p.name})'for p in sorted(D.glob('*.png')))+'\n');(D/'gallery-manifest.json').write_text(json.dumps({'bridges':rows,'originalPNGsUnmodified':True,'reviews':[{'file':p.name,'bytes':p.stat().st_size}for p in D.glob('*.jpg')]},indent=2)+'\n');print('Native bridge gallery ready')
