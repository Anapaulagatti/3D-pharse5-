from pathlib import Path
from PIL import Image,ImageDraw
import json
R=Path(__file__).resolve().parents[1];D=R/'docs/gate3-palace-cleanup';cap=json.loads((D/'native-captures.json').read_text())
def crop(entry,phase,box):
 q=next(q for q in cap['rows']if q['entry']==entry and q['phase']==phase);sx,sy=map(round,q['audit']['camera']['scroll']);return Image.open(D/(q['name']+'.png')).convert('RGB').crop((box[0]-sx,box[1]-sy,box[2]-sx,box[3]-sy))
def review(im,path):
 for q in [88,80,72,60]:
  im.save(path,quality=q,optimize=True)
  if path.stat().st_size<1000000:return
 raise AssertionError('Review >1MB')
md=['# Final local palace cleanup','','Human artistic approval PENDING. Hanbit, BOTH Jeju bridges and western hanok remain locked. These PNGs are actual native1:1 Phaser readbacks, not authoring images. JPEGs are labelled review derivatives.','','[Playable ZIP](PALACE_CLEANUP_REVIEW.zip) · [QA](QA.md) · [Actual gameplay](world-traversal-review.mp4)',''];html=['<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Palace local cleanup</title><style>body{background:#183135;color:#fff;max-width:1500px;margin:auto;padding:20px;font:17px/1.6 system-ui}a{color:#aaffdd}img,video{max-width:100%;height:auto;image-rendering:pixelated}</style></head><body><h1>Palace local cleanup / human review pending</h1><p><a href="PALACE_CLEANUP_REVIEW.zip">Playable ZIP</a> · <a href="QA.md">QA</a></p>'];rows=[]
for name,entry,box in [('axis','palace-axis-local',(1820,1060,2220,1835)),('right-access','palace-access-local',(2080,1260,2730,1530)),('facade','palace-front-local',(1490,590,2220,765))]:
 ims=[crop(entry,p,box)for p in ['before','after']];w,h=ims[0].size;board=Image.new('RGB',(2*w,h+30),'#183135');dr=ImageDraw.Draw(board)
 for i,(im,p)in enumerate(zip(ims,['before','after'])):im.save(D/f'{name}-{p}-native-1x.png');board.paste(im,(i*w,30));dr.text((i*w+8,8),p.upper()+' / native1x',fill='white')
 board.save(D/f'{name}-before-after-native-board.png');review(board,D/f'{name}-comparison.jpg');md+=['## '+name,'',f'![Comparison]({name}-comparison.jpg)','',f'[BEFORE native1x]({name}-before-native-1x.png) · [AFTER native1x]({name}-after-native-1x.png) · [Native comparison board]({name}-before-after-native-board.png)',''];html.append(f'<h2>{name}</h2><img src="{name}-comparison.jpg"><p><a href="{name}-before-native-1x.png">BEFORE native1x</a> · <a href="{name}-after-native-1x.png">AFTER native1x</a></p>');rows.append({'name':name,'worldBox':box})
# One tall native palace proof assembled from TWO actual identically x-registered
# Phaser camera readbacks (no resize). No generated authoring image passed as game.
parts=[crop('palace-combined-local','after',(1100,150,2955,1040)),crop('palace-axis-local','after',(1100,1040,2955,1835))]
out=Image.new('RGB',(1855,1685));out.paste(parts[0],(0,0));out.paste(parts[1],(0,890));out.save(D/'combined-palace-after-native-1x.png');review(out,D/'combined-palace-review.jpg');md+=['## Combined palace zone','', '![Palace](combined-palace-review.jpg)','', '[Full combined native1x](combined-palace-after-native-1x.png). Two actual Phaser readbacks joined at integer worldy1040, without resizing or blending. Full untouched source frames retained.',''];html.append('<h2>Combined palace</h2><img src="combined-palace-review.jpg"><p><a href="combined-palace-after-native-1x.png">Combined native1x</a>: two exact in-engine camera readbacks at worldy1040, no scaling.</p><video controls src="world-traversal-review.mp4"></video></body></html>');(D/'VISUAL_REVIEW.md').write_text('\n'.join(md));(D/'VISUAL_REVIEW.html').write_text('\n'.join(html));(D/'gallery-manifest.json').write_text(json.dumps({'targets':rows,'native':'Actual Phaser readback / exact crop, no scaling','combined':'Two actual wide native Phaser frames joined at worldy1040; no overlap blending','reviewImages':[{'file':p.name,'bytes':p.stat().st_size}for p in D.glob('*.jpg')]},indent=2)+'\n')
