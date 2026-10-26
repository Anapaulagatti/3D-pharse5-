"""Lossless atlas review animations; explicitly source previews, not gameplay."""
from pathlib import Path
from PIL import Image
import json,math
R=Path(__file__).resolve().parents[2];D=R/'docs/phase1b';ids=['juni','haneul','bomi','minjun'];assets={};rows=[];poses=[]
for id in ids:
 stem=R/('public/assets/juni/juni'if id=='juni'else f'public/assets/characters/{id}/atlas');assets[id]=(Image.open(stem.with_suffix('.png')).convert('RGBA'),json.loads(stem.with_suffix('.json').read_text())['frames'])
for action,duration in [('walk',92),('run',80)]:
 frames=[]
 for i in range(8):
  board=Image.new('RGBA',(384,448),(30,28,38,255))
  for col,id in enumerate(ids):
   sheet,atlas=assets[id]
   for row,direction in enumerate(['front','back','left','right']):
    q=atlas[f'{action}-{direction}-{i}']['frame'];im=sheet.crop((q['x'],q['y'],q['x']+q['w'],q['y']+q['h']));board.alpha_composite(im,(96*col,112*row))
  frames.append(board)
 for scale,label in [(1,'native'),(2,'review-2x')]:
  out=D/f'{action}-four-directions-{label}-preview.png';seq=[im.resize((384*scale,448*scale),Image.Resampling.NEAREST)for im in frames];seq[0].save(out,save_all=True,append_images=seq[1:],duration=[duration]*8,loop=0,disposal=0,blend=0,optimize=False);rows.append({'file':out.name,'format':'lossless animated PNG','bytes':out.stat().st_size,'size':seq[0].size,'scale':scale,'columns':ids,'rows':['front','back','left','right'],'warning':'Atlas-driven source review, not an in-engine screenshot or gameplay video. Source PNGs and actual Phaser evidence remain separate.'})
for id in ids[1:]:
 cfg=json.loads((R/f'assets-src/characters/phase1b/{id}/rig.json').read_text());keyframes=[]
 for i in range(8):
  phase=i/8*math.tau;far=48+round(math.cos(phase)*6);near=48+round(math.cos(phase+math.pi)*6);keyframes.append({'frameIndex':i,'profileWalkFarAnkleX':far,'profileWalkNearAnkleX':near,'crossingPose':far==near})
 poses.append({'id':id,'nativeAnchor':[48,100],'rigLayerConvention':'profile L=FAR, R=NEAR; not a claim of anatomical left/right in all four views','profileWalkKeys':keyframes,'oppositeContacts':[0,4],'interpretation':'Contact keys0/4 swap the projected ankles.2/6 are crossing poses. This source-ownership record explains the intended keys; it does not override Forge auto-luminance WARNs or certify human motion appeal.'})
(D/'motion-preview-provenance.json').write_text(json.dumps({'previews':rows,'sourcePoseKeys':poses},indent=2)+'\n');print(rows)
