"""Review every existing prop: visual purpose, painted occlusion and reachable approach.

Data/render audit only; actual Phaser screenshots remain the visual evidence.
"""
from pathlib import Path
import json
import math
import numpy as np
from PIL import Image

R=Path(__file__).resolve().parents[1];S=R/'assets-src/gwanghwamun'
b=json.loads((S/'map-bundle.json').read_text());nav=json.loads((S/'navigation/nav-grid.json').read_text())
points=np.array([[(x+.5)*4,(y+.5)*4] for y,row in enumerate(nav['reachable']) for x,c in enumerate(row) if c=='1'])
objects=sorted(b['objects'],key=lambda o:-60 if o['prop']=='bridge' else o['sortY'])
masks=[]
for o in objects:
    p=b['props'][o['prop']];im=Image.open(S/p['image']).convert('RGBA');mask=Image.new('L',(1024,768))
    mask.paste(im.getchannel('A'),(round(o['x']-p['anchor_px'][0]),round(o['y']-p['anchor_px'][1])))
    masks.append(np.array(mask)>=128)
purpose={
 'gate':'Northern palace focal landmark; open approach on the civic axis.',
 'pavilion':'Western reading courtyard and seating frontage.',
 'hall':'Eastern tea/reading hall; entrance approach retained.',
 'sejong':'Seated scholar landmark left of the open gathering axis.',
 'ginkgo':'Golden garden canopy framing edge spaces and resting pockets.',
 'tree':'Layered green perimeter/shade; trunk collision, opaque canopy Y-sort.',
 'bench':'Rest pocket beside a reading building or garden edge, outside central circulation.',
 'lantern':'Visible route marker at a courtyard connector or bridge landing.',
 'jars':'Onggi storage cluster against wooden building frontage.',
 'planter':'Frame entrance/seating edges without filling the central gathering space.',
 'bridge':'Walkable stone crossing at the only gap in water collision.',
 'wall':'Stone boundary element defining garden/architecture edges.'}
report=[]
for i,o in enumerate(objects):
    total=int(masks[i].sum());visible=masks[i].copy()
    for mask in masks[i+1:]:visible &= ~mask
    fraction=round(float(visible.sum())/max(1,total),4)
    d=np.linalg.norm(points-np.array([o['x'],o['y']]),axis=1);nearest=points[int(d.argmin())]
    report.append({'id':o['id'],'kind':o['prop'],'position':[o['x'],o['y']],
      'purpose':purpose[o['prop']],'solid':o.get('solid',b['props'][o['prop']]['solid']),
      'native_visible_fraction':fraction,'nearest_reachable_approach':nearest.tolist(),
      'approach_distance_px':round(float(d.min()),2),'within_existing140px_interact_range':bool(d.min()<140),
      'occlusion_note':'Painted alpha overlap at current feet sort; actual Phaser evidence verifies actor occlusion separately.'})
data={'status':'REQUIRES_VISUAL_REVIEW','props':report,'fully_hidden':[x['id']for x in report if x['native_visible_fraction']==0],
 'limits':'Visibility alone does not approve composition. Some intentional foliage/wall overlap is expected; no prop artwork changed.'}
(R/'docs/juni-animation/prop-audit.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps({'fully_hidden':data['fully_hidden'],'low_visibility':[(x['id'],x['native_visible_fraction'])for x in report if x['native_visible_fraction']<.4],
 'approach_inaccessible':[x['id']for x in report if not x['within_existing140px_interact_range']]}))
