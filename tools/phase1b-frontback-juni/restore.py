"""Narrow, offline front/back pose correction. Juni supplies landmarks, never pixels."""
from pathlib import Path
import json,sys,hashlib,subprocess
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/phase1b'))
from animate import bone,translate
S=ROOT/'assets-src/characters/phase1b-frontback-juni';D=ROOT/'docs/phase1b-frontback-juni'
S.mkdir(exist_ok=True,parents=True);D.mkdir(exist_ok=True,parents=True)
# Screen-left/right shoe sole centers read directly from the 96x112 approved frames.
# These are observed poses, not an imposed textbook symmetrical 0/4 cycle.
feet={
'walk-front':[[[41,89],[49,98]],[[45,98],[54,89]],[[44,98],[53,85]],[[43,88],[49,98]],[[41,90],[49,98]],[[45,98],[54,89]],[[44,98],[52,87]],[[43,91],[49,98]]],
'walk-back':[[[44,84],[52,98]],[[45,85],[54,98]],[[44,94],[54,88]],[[46,94],[53,99]],[[44,85],[52,98]],[[45,98],[54,87]],[[46,84],[54,97]],[[44,94],[54,88]]],
'run-front':[[[42,81],[49,98]],[[44,98],[54,86]],[[44,79],[51,98]],[[46,79],[51,84]],[[43,98],[51,82]],[[44,88],[52,98]],[[44,83],[51,98]],[[46,84],[53,87]]],
'run-back':[[[44,88],[53,98]],[[45,87],[54,96]],[[43,82],[52,98]],[[44,85],[54,91]],[[44,86],[52,96]],[[44,98],[54,84]],[[44,79],[52,98]],[[43,81],[53,92]]],
}
tops={'walk-front':[20,20,20,20,20,21,20,21],'walk-back':[20,21,20,21,20,20,21,20],'run-front':[20,25,17,13,19,25,17,13],'run-back':[20,22,18,15,22,24,16,15]}
# Actual screen hand ends from Juni, frame-index matched. Coordinates absolute native.
hands={
'walk-front':[[[40,70],[60,67]],[[35,70],[59,67]],[[34,69],[58,68]],[[41,69],[62,71]],[[41,69],[60,67]],[[36,70],[60,69]],[[35,70],[58,68]],[[41,70],[61,68]]],
'walk-back':[[[37,67],[56,66]],[[36,70],[57,67]],[[37,68],[56,65]],[[37,68],[62,69]],[[37,68],[56,67]],[[41,68],[61,67]],[[37,68],[57,66]],[[37,67],[56,64]]],
'run-front':[[[40,69],[59,54]],[[38,71],[56,66]],[[36,60],[59,60]],[[39,53],[58,52]],[[38,67],[58,58]],[[37,75],[60,63]],[[37,62],[57,59]],[[39,53],[58,55]]],
'run-back':[[[38,70],[60,69]],[[37,69],[58,69]],[[37,60],[57,64]],[[38,56],[59,60]],[[35,66],[59,69]],[[39,60],[60,70]],[[38,57],[58,62]],[[36,58],[59,58]]],
}
J=Image.open(ROOT/'public/assets/juni/juni.png').convert('RGBA');JA=json.loads((ROOT/'public/assets/juni/juni.json').read_text())['frames']
def crop(im,meta):
 f=meta['frame'];return im.crop((f['x'],f['y'],f['x']+f['w'],f['y']+f['h']))
def getj(name):return crop(J,JA[name])
def sheet(frames,path,scale=1):
 im=Image.new('RGBA',(8*96,4*132),(29,28,36,255));dr=ImageDraw.Draw(im)
 for row,key in enumerate(feet):
  for i in range(8):im.alpha_composite(frames[f'{key}-{i}'],(i*96,row*132+20));dr.text((i*96+2,row*132+3),f'{key} {i}',fill='white')
 im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST).save(path)
 return im
reference={f'{key}-{i}':getj(f'{key}-{i}')for key in feet for i in range(8)}
sheet(reference,D/'juni-reference-native.png');
# Integer lateral shift measured from each reference head silhouette (top26 native rows).
body_x={}
for key in feet:
 centers=[]
 for i in range(8):
  a=np.array(getj(f'{key}-{i}'));top=np.nonzero(a[:,:,3])[0].min();ys,xs=np.nonzero(a[top:top+26,:,3]);centers.append(float(xs.mean()))
 body_x[key]=[round(v-centers[0])for v in centers]
recipe={k:[{'frame':i,'sourceFrame':f'{k}-{i}','soleScreenLR':feet[k][i],'bodyDeltaY':tops[k][i]-20,'bodyDeltaX':body_x[k][i],'handScreenLR':hands[k][i],'phaseObservation':('flight/up'if max(p[1]for p in feet[k][i])<98 and k.startswith('run')else ('left support/down'if feet[k][i][0][1]>feet[k][i][1][1] else 'right support/passing'))}for i in range(8)]for k in feet}
(S/'juni-motion-template.json').write_text(json.dumps({'cell':[96,112],'source':'public/assets/juni/juni.png + juni.json','method':'manual native landmark tracing; screen L/R, not anatomical left/right; source irregularities preserved at matching indices','clips':recipe},indent=2)+'\n')
reports=[]
for id in ['haneul','bomi','minjun']:
 old=ROOT/'assets-src/characters/phase1b'/id;cfg=json.loads((old/'rig.json').read_text());pub=ROOT/'public/assets/characters'/id;atlas=Image.open(pub/'atlas.png').convert('RGBA');meta=json.loads((pub/'atlas.json').read_text())['frames'];outdir=S/id/'frames';outdir.mkdir(parents=True,exist_ok=True);frames={}
 baseline=Image.open(__import__('io').BytesIO(subprocess.check_output(['git','show',f'4dfa807f26a19d8602143421a9f6886cc1c08e28:public/assets/characters/{id}/atlas.png'],cwd=ROOT))).convert('RGBA')
 for key,poses in recipe.items():
  direction=key.split('-')[1];c=cfg[direction];parts={p.stem:Image.open(p).convert('RGBA')for p in (old/'layers'/direction).glob('*.png')}
  for pose in poses:
   i=pose['frame'];dy=pose['bodyDeltaY'];dx=pose['bodyDeltaX'];im=Image.new('RGBA',(96,112));legs=[]
   for side,sole in zip(['L','R'],pose['soleScreenLR']):
    h,k,a=c['joints'][side];shoe=parts[side+'shoe'];box=shoe.getbbox();sole0=[round((box[0]+box[2]-1)/2),box[3]-1];delta=[sole[0]-sole0[0],sole[1]-sole0[1]];ankle=[a[0]+delta[0],a[1]+delta[1]];hip=[h[0]+dx,h[1]+dy]
    # Projected knee follows the observed forward-lift contour, with connected joints.
    knee=[round((hip[0]+ankle[0])/2)+(-1 if side=='L'else 1),round((hip[1]+ankle[1])/2)]
    legs.append((sole[1],side,h,k,a,hip,knee,ankle,delta))
   for _,side,h,k,a,hip,knee,ankle,delta in sorted(legs):
    bone(im,parts[side+'thigh'],h,k,hip,knee);bone(im,parts[side+'shin'],k,a,knee,ankle);translate(im,parts[side+'shoe'],*delta)
   translate(im,parts['body'],dx,dy)
   for side,hand in zip(['L','R'],pose['handScreenLR']):
    a,b,w=c['arms'][side];shoulder=[a[0]+dx,a[1]+dy];wrist=hand;elbow=[round((shoulder[0]+wrist[0])/2)+(-3 if side=='L'else 3),round((shoulder[1]+wrist[1])/2)+2]
    bone(im,parts[side+'upperarm'],a,b,shoulder,elbow);bone(im,parts[side+'forearm'],b,w,elbow,wrist)
   name=f'{key}-{i}';frames[name]=im;im.save(outdir/f'{name}.png');f=meta[name]['frame'];atlas.paste(im,(f['x'],f['y']))
 atlas.save(pub/'atlas.png')
 unchanged=[name for name in meta if name not in frames];assert all(crop(atlas,meta[n]).tobytes()==crop(baseline,meta[n]).tobytes()for n in unchanged)
 report={'id':id,'correctedFrames':32,'unchangedOtherFrames':len(unchanged),'uniquePerClip':{k:len({frames[f'{k}-{i}'].tobytes()for i in range(8)})for k in feet},'sourceIdentity':'Existing own PNG parts only; face/hair/body translated without repainting; no Juni color pixels copied','mapping':list(feet),'humanMotionApproval':'PENDING'};assert all(n==8 for n in report['uniquePerClip'].values());reports.append(report)
 board=sheet(frames,D/f'{id}-corrected-native.png');board.resize((1536,1056),Image.Resampling.NEAREST).save(D/f'{id}-corrected-2x.png')
 # Same-index reference and candidate, row per clip, two columns per pair.
 compare=Image.new('RGBA',(1536,528),(29,28,36,255));dr=ImageDraw.Draw(compare)
 for row,key in enumerate(feet):
  for i in range(8):
   x=i*192;y=row*132;compare.alpha_composite(reference[f'{key}-{i}'],(x,y+20));compare.alpha_composite(frames[f'{key}-{i}'],(x+96,y+20));dr.text((x+2,y+3),f'{key} {i} J / {id}',fill='white')
 compare.save(D/f'juni-vs-{id}-native.png')
 seq=[]
 for i in range(8):
  q=Image.new('RGBA',(768,528),(29,28,36,255));dr=ImageDraw.Draw(q)
  for row,key in enumerate(feet):
   q.alpha_composite(reference[f'{key}-{i}'],(0,row*132+20));q.alpha_composite(frames[f'{key}-{i}'],(96,row*132+20));dr.text((0,row*132),key,fill='white')
  seq.append(q.crop((0,0,192,528)).resize((384,1056),Image.Resampling.NEAREST))
 seq[0].save(D/f'juni-vs-{id}-motion.png',save_all=True,append_images=seq[1:],duration=100,loop=0,disposal=0,blend=0)
(D/'source-qa.json').write_text(json.dumps(reports,indent=2)+'\n')
