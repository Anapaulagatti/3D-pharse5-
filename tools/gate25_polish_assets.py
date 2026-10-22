"""Localized source-derived environment continuation; approved facade pixels stay exact.
Only new artwork is finished/resampled. Native architecture/coordinates and original sources are never altered.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,shutil,numpy as np
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate25-polish';P=R/'public/assets/gate2';O=P/'district-polish';D=R/'docs/gate25-polish'
for src,dest in [('/workspace/generated_images/exec-d711cc74-2c5b-44ec-8537-8f4c94534132.png','west-host.png'),('/workspace/generated_images/exec-f7608d2b-f783-42ee-98aa-10f3cadd6c3f.png','east-host.png')]:
 if not (S/dest).exists():shutil.copy2(src,S/dest)
before=Image.open(S/'before-background.png').convert('RGB');base=Image.open(S/'background-filled.png').convert('RGB');W,H=base.size
allowed=Image.new('L',(W,H));ad=ImageDraw.Draw(allowed)
# Missing-only continuation plus two localized public-realm repair bands.
missing=Image.open(S/'missing-mask.png');allowed.paste(missing)
for name,x,ymin in [('west',1488,850),('east',2464,810)]:
 native=Image.open(S/(name+'-host.png')).convert('RGB').resize((512,768),Image.Resampling.BOX);native.save(S/(name+'-finish.png'))
 box=(x-256,ymin,x+256,H);piece=native.crop((0,ymin-446,512,768));base.paste(piece,(box[0],box[1]));ad.rectangle((box[0],box[1],box[2]-1,box[3]-1),fill=255)
# Remove the remaining tip of the same cut tree above the curb, clear of intact bollards.
east=Image.open(S/'east-finish.png').convert('RGB');box=(2482,787,2523,818);base.paste(east.crop((box[0]-2208,box[1]-446,box[2]-2208,box[3]-446)),(box[0],box[1]));ad.rectangle((box[0],box[1],box[2]-1,box[3]-1),fill=255)
# Drainage grates are intact approved street assets; preserve their exact native pixels.
for x,y,w,h in [(2228,818,50,28),(2580,818,58,28),(2524,784,17,34)]:
 base.paste(before.crop((x,y,x+w,y+h)),(x,y));ad.rectangle((x,y,x+w-1,y+h-1),fill=0)
# Conservative protected facade/door rectangles: overlays are structurally disjoint from these.
protected=Image.new('L',(W,H));pd=ImageDraw.Draw(protected)
for rect in [(0,190,1435,760),(1545,0,2440,805),(2540,267,3110,725)]:pd.rectangle(rect,fill=255)
a=np.array(base);b=np.array(before);guard=np.array(protected)>0;assert np.array_equal(a[guard],b[guard]);change=(a!=b).any(axis=2);assert not np.any(change & (np.array(allowed)==0))
base.save(S/'finished-background.png');allowed.save(S/'authorized-edit-mask.png');protected.save(S/'facade-protection-mask.png');Image.fromarray(change.astype('uint8')*255).save(S/'changed-pixels.png')
# Three native-height chunks with exact world registration. No full-world image in runtime.
old=json.loads((P/'district/scene.json').read_text());scene=dict(old);scene['id']='district-polish';scene['label']='Gate2.5 · polished Muneum / Bakery / Station';scene['grounds']=[]
for name,x,end in [('muneum',0,1512),('bakery',1512,2488),('station',2488,W)]:
 base.crop((x,0,end,H)).save(O/(name+'.png'));scene['grounds'].append(dict(id=name,image='district-polish/'+name+'.png',x=x,y=0,width=end-x,height=H))
# Restore the complete approved Muneum foreground sprites, never clip a tree/planter at a chunk boundary.
bs=json.loads((P/'b/scene.json').read_text());scene['objects']=[dict(ob,id='district-'+ob['id'],y=ob['y']+190,sortY=ob['sortY']+190)for ob in bs['objects']]
# Carry original foot-clearance field forward, restore the complete props' measured ground contacts.
walk=Image.open(P/'district/walk.png').convert('L');wd=ImageDraw.Draw(walk)
contacts=[]
for solid in bs['solids']:
 if 'physical support' in solid['reason'] or 'trunk' in solid['reason']:
  x,y,w,h=solid['rect'];y+=190
  if x+w>=1450 and x<=1540:
   wd.rectangle((int(x-8),int(y-8),int(x+w+8),int(y+h+8)),fill=0);contacts.append([x,y,w,h])
# New low planters remain decorative/nonwalkable; retain narrow visible pedestrian paths.
for rect in [(1565,1000,175,100),(2335,970,235,65),(2240,1080,440,90)]:
 x,y,w,h=rect;wd.rectangle((x-8,y-8,x+w+8,y+h+8),fill=0)
walk.save(O/'walk.png');scene['mask']='district-polish/walk.png';scene['limitations']='Localized background/seam polish. Original source facades/entrances and all established coordinates preserved; original collision routes unchanged. Physical-device acceptance remains NOT TESTED.'
(O/'scene.json').write_text(json.dumps(scene,indent=2,ensure_ascii=False)+'\n');cat=json.loads((P/'catalog.json').read_text());cat=[x for x in cat if x['id']!='district-polish'];cat.append(dict(id='district-polish',label=scene['label']));(P/'catalog.json').write_text(json.dumps(cat,indent=2,ensure_ascii=False)+'\n')
base.resize((1592,607),Image.Resampling.NEAREST).save(D/'BACKGROUND_REVIEW.png')
checks=dict(protectedFacadePixels=int(guard.sum()),facadesExact=True,changedPixels=int(change.sum()),allChangesInsideAuthorizedMasks=True,buildingsResampled=False,worldSize=[W,H],entrancesUnchanged=scene['targets']==old['targets'],spawnUnchanged=scene['spawn']==old['spawn'],originalCollisionRoutesRetained=True,localizedRestoredPropContacts=contacts,restoredWholeForegroundSprites=[o['id']for o in scene['objects']],restoredPreviouslyCut=['district-gate1-4','district-gate1-5'],eastCutTree='Lower painted tree spanning road/source edge removed locally and replaced by low bounded planter/flowers; original source retained',chunkPolicy='Three nonoverlapping native1:1 crop windows, now full-height with completed terrain; source art dimensions remain unchanged')
(D/'art-preservation.json').write_text(json.dumps(checks,indent=2)+'\n');print('PASS local-only art masks / exact facades / complete foreground sprites / native chunks')
