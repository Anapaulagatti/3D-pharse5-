from pathlib import Path
from PIL import Image,ImageDraw
import json,math,hashlib,shutil
D=Path('docs/phase2b-motion');IDS=['sori','jiwon','nari','taeyang','yuna','hyunwoo'];qa=json.loads((D/'readbacks-juni-sori-jiwon-nari-taeyang-yuna-hyunwoo.json').read_text());assert len(qa)==1008;assert all(r['diffPixels']==0 and r['nearest']and r['integerCamera']and r['nativeZoom']==1 for r in qa)
tracks=json.loads((D/'directional-pixel-qa.json').read_text())['rows'];rows=[];proof=[]
for id in ['juni']+IDS:
 q=json.loads((D/f'{id}-gameplay.json').read_text());assert not q['errors'];assert len(q['rows'])==6
 for row in q['rows']:
  clip=row['clip'];stride=44 if row['action']=='walk'else 64;assert len(row['samples'])==24;assert [(s['loop'],s['index'])for s in row['samples']]==[(l,i)for l in range(3)for i in range(8)]
  starts=[next(s for s in row['samples']if s['index']==0 and s['loop']==l)['audit']['state']for l in range(3)];dist=[math.hypot(starts[l]['x']-starts[l-1]['x'],starts[l]['y']-starts[l-1]['y'])for l in [1,2]];assert all(abs(d-stride)<=stride/8+.01 for d in dist),(id,clip,dist)
  for s in row['samples']:
   src=Path(s['sourcePath']);h=hashlib.sha256(src.read_bytes()).hexdigest();proof.append({'id':id,'clip':clip,'loop':s['loop'],'index':s['index'],'fullNativePNG_SHA256':h,'body':f'{id}-{clip}-loop{s["loop"]}-{s["index"]}-body-native.png','context':f'{id}-{clip}-loop{s["loop"]}-{s["index"]}-context-native.png'})
  # One unmodified full-canvas1:1 proof per clip; all other native body/context
  # crops retained, plus SHA for every local full frame.
  first=row['samples'][0];shutil.copyfile(first['sourcePath'],D/f'{id}-{clip}-full-phaser-native.png')
  rec={'id':id,'clip':clip,'completeConsecutiveLoops':3,'distanceBetweenIndex0Samples':dist,'movement':[row['end']['x']-row['start']['x'],row['end']['y']-row['start']['y']],'nativeFrames':24,'pixelMismatches':0,'sampling':'NEAREST','camera':'INTEGER /1:1'}
  if row['view']=='right':
   assert row['end']['x']>row['start']['x']+stride*3;assert row['stop']['matched']and row['turn']['matched'];rec['realStopAndTurn']='OBSERVED'
   if id in IDS:
    track=next(t for t in tracks if t['id']==id and t['action']==row['action']);drifts=[];board=Image.new('RGB',(960,172),(28,30,38));dr=ImageDraw.Draw(board)
    for loop in range(3):
     pts=[]
     for i in range(5):
      s=next(s for s in row['samples']if s['loop']==loop and s['index']==i);st=s['audit']['state'];native=track['after'][i]['nativeSole'];world=[math.floor(st['x']+.5)+native[0]-48,math.floor(st['y']+.5)+native[1]-100];pts.append(world)
      if loop==0:
       before=track['before'][i]['nativeSole'];nativeim=Image.open(D/f'{id}-{clip}-loop0-{i}-body-native.png');board.paste(nativeim,(i*192,30));dr.text((i*192+3,2),f'phase{i} near planted',fill='white');x=i*192+native[0];y=30+native[1];dr.line((x-4,y,x+4,y),fill='#ffba5a');dr.line((x,y-4,x,y+4),fill='#ffba5a');dr.text((i*192+3,148),f'world x {world[0]:.1f}',fill='white')
     delta=max(p[0]for p in pts)-min(p[0]for p in pts);assert delta<=stride/8+2,(id,clip,loop,delta);drifts.append(delta)
    board.save(D/f'{id}-{clip}-actual-contact-native.png');rec['actualPhaseSampleStanceDriftPixels']=drifts;rec['contactTolerance']='One held8-pose interval stride/8 +2px integer placement. Not continuous subpixel foot lock; no runtime frame holds changed.'
  rows.append(rec)
(D/'actual-frame-provenance.json').write_text(json.dumps(proof,indent=2)+'\n');(D/'actual-motion-qa.json').write_text(json.dumps({'rows':rows,'nativeReadbacks':1008,'unexplainedPixels':0,'humanMotionApproval':'PENDING','scope':'42 actual Phaser clips /126 complete sampled loops;24 samples each; no forced animation frames','physicalDevices':'NOT TESTED','visualLimits':'Eight-pose held-frame quantization remains. Front/back naturalness, loop feel, contact impression and no-moonwalk perception require human review; numerical PASS is not artistic approval.'},indent=2)+'\n');print('PASS1008exact opaque readbacks,42clips126loops, positiveX/stop/turn; source+actualcontact bounds verified')
