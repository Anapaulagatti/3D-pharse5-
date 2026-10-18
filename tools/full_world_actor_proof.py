"""Compose one unchanged approved Juni frame with the actual full-world placements."""
from full_world_art import R,S,C,F,run,write
from PIL import Image
import json,os
j=json.loads((R/'public/review/juni-animation/juni.json').read_text());key=next(k for k in j['frames'] if k.startswith('idle-front'));r=j['frames'][key]['frame'];Image.open(R/'public/review/juni-animation/juni.png').crop((r['x'],r['y'],r['x']+r['w'],r['y']+r['h'])).save(S/'actor-proof.png')
p=json.loads((S/'map/placements.json').read_text())
for group in p.values():
 for o in group:o['image']=str((S/'map'/o['image']).resolve())
p['actors']=[{'id':'approved-juni-native','image':str(S/'actor-proof.png'),'x':2176,'y':832,'anchorPx':[48,100],'sortY':832}];write(S/'actor-proof-placements.json',p)
Q=R/'docs/full-world/quality/actor-compose';Q.mkdir(exist_ok=True)
run(F/'skills/generate2dmap/scripts/compose_layered_preview.py','--base',S/'map/layers/base.png','--placements',S/'actor-proof-placements.json','--output',Q/'preview.png','--report',Q/'composition.json','--bundle',S/'map/outdoor-bundle.json','--audit-out',Q/'audit.json')
