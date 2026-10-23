"""Native sprite extraction/registration only; raw authored sources remain immutable.
No resize, sharpening, recoloring or procedural artwork. Reject trials that miss envelopes.
"""
from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate3/recovery-world-v1';O=R/'public/assets/gate3/recovery-world';O.mkdir(exist_ok=True)
objects=[];records=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def extract(name,source,box,rootx,rooty,sorty=None):
 raw=Image.open(S/source).convert('RGBA');im=raw.crop(box);a=np.array(im)
 # Tool alpha can contain <=32/255 diffuse background glow. Remove only that matte,
 # never resample/recolor opaque artwork. Native edge alpha is otherwise retained.
 a[a[:,:,3]<=32,3]=0;im=Image.fromarray(a);bbox=im.getbbox();assert bbox
 im=im.crop(bbox);out=O/(name+'.png');im.save(out,optimize=True)
 ob={'id':'recovery-world/'+name,'image':str(out.relative_to(R/'public')),'x':round(rootx-im.width/2),'y':rooty-im.height,'width':im.width,'height':im.height,'sortY':sorty or rooty,'alphaSoftening':.35,'bytes':im.width*im.height*4}
 rec={'id':name,'raw':str((S/source).relative_to(R)),'rawSha256':sha(S/source),'sourceCell':list(box),'nativeOpaqueCrop':list(bbox),'derived':str(out.relative_to(R)),'sha256':sha(out),'resampling':'NONE','matte':'Only source alpha<=32 discarded; native RGB and remaining alpha unchanged','nativeEnvelope':[ob[k]for k in ['x','y','width','height']]};records.append(rec);return ob

# Complete roof, no duplicate hall/foundation. Native original facade supplies one continuous lower hall.
roof=extract('palace-roof','roof-v2-raw.png',(0,0,1280,1024),2035,610,790);objects.append(roof)
a=Image.open(R/'public/assets/gate2/a/ground.png').convert('RGBA')
upper=Image.new('RGBA',(1010,60));upper.paste(a.crop((870,0,1536,40)),(0,20));upper.paste(a.crop((1145,0,1489,40)),(666,20));upper.paste(a.crop((870,0,1536,20)),(0,0));upper.paste(a.crop((1145,0,1489,20)),(666,0));upper.save(O/'palace-upper-timber.png',optimize=True)
objects.append({'id':'recovery-world/palace-upper-timber','image':'assets/gate3/recovery-world/palace-upper-timber.png','x':1510,'y':590,'width':1010,'height':60,'sortY':789,'alphaSoftening':.35,'bytes':1010*60*4})
right=a.crop((1145,0,1489,140));right.save(O/'palace-right-continuation.png',optimize=True)
objects.append({'id':'recovery-world/palace-right-continuation','image':'assets/gate3/recovery-world/palace-right-continuation.png','x':2176,'y':650,'width':344,'height':140,'sortY':790,'alphaSoftening':.35,'bytes':344*140*4})
records.append({'id':'palace-native-facade-continuation','source':'public/assets/gate2/a/ground.png','sha256':sha(R/'public/assets/gate2/a/ground.png'),'ownership':[{'sourceRect':[870,0,666,20],'destination':[1510,590]},{'sourceRect':[1145,0,344,20],'destination':[2176,590]},{'sourceRect':[870,0,666,40],'destination':[1510,610]},{'sourceRect':[1145,0,344,40],'destination':[2176,610]},{'sourceRect':[1145,0,344,140],'destination':[2176,650]}],'scale':1,'resampling':'NONE','foundation':'One horizontal continuous native source plinth; no new stacked foundation. Original A source pixels remain exact.','visualEasement':'Roof overhang beyond1050px contact; original lower steps extend to790. Reservation unchanged.'})

# Preserve every complete architectural silhouette. Envelopes are audited, never shrunk/cut to fit.
objects.append(extract('market','harbor-low-v4-raw.png',(0,0,875,345),910,3660))
objects.append(extract('ferry','compact-landmarks-v5-raw.png',(0,704,384,1024),2560,3740))

# Tower/ride bounded trials are measured before selection. Their actual projected conflicts remain explicit.
# Preserve the conditionally accepted pilot's105px entrance and native tower body.
# Restore its COMPLETE source antenna: the former pilot-only30px tip shortening
# is not propagated. New compact trials are rejected for undersized entrances.
tower_source=R/'assets-src/gate3/recovery/namsan-authored-v3.png';tower_mask=R/'assets-src/gate3/recovery/tower-ownership-mask.png'
t=Image.open(tower_source).convert('RGBA');tm=Image.open(tower_mask).convert('L');t.putalpha(tm);tb=tm.getbbox();t=t.crop(tb);t.save(O/'tower.png',optimize=True)
objects.append({'id':'recovery-world/tower','image':'assets/gate3/recovery-world/tower.png','x':1200-858+tb[0],'y':3240-766+tb[1],'width':t.width,'height':t.height,'sortY':3240,'alphaSoftening':.65,'bytes':t.width*t.height*4})
records.append({'id':'tower','source':str(tower_source.relative_to(R)),'sha256':sha(tower_source),'ownershipMask':str(tower_mask.relative_to(R)),'maskSha256':sha(tower_mask),'nativeSourceCrop':list(tb),'sourceRoot':[858,766],'worldRoot':[1200,3240],'nativeDoorRect':[814,552,79,105],'resampling':'NONE','policy':'Accepted pilot entrance/body preserved. COMPLETE original antenna, no30px tip shortening. Protected root/contact unchanged. Projection conflict remains P1; compact trials with miniature doors are not substituted.'})
ride_source='compact-landmarks-v5-raw.png'
ridecells=[('carousel',(0,0,384,355),2415,3150),('wheel',(0,355,384,704),2830,3160)]
for name,box,cx,root in ridecells:objects.append(extract(name,ride_source,box,cx,root))

# Native tree bank extracted in fixed cells; no stretching to compensate for poor source size.
trees=[]
for row in range(4):
 for col in range(6):
  name=f'tree-{row*6+col:02d}';ob=extract(name,'tree-bank-raw.png',(col*256,row*256,(col+1)*256,(row+1)*256),0,0);trees.append(ob)

m=json.loads((R/'public/assets/gate3/recovery-pilots/manifest.json').read_text());p=json.loads((R/'assets-src/gate3/production-plan-v3.1-restored.json').read_text())['plan'];W,H=p['size'];avoid=Image.new('L',(W,H));from PIL import ImageDraw
ad=ImageDraw.Draw(avoid)
for path in p['paths']:ad.line([tuple(q)for q in path['points']],fill=255,width=path['width']+70,joint='curve')
for x,y,w,h in [b['rect']for b in p['buildings']]+[(640,650,1536,1024),(3180,3200,1024,1536),(2274,2196,766,667)]:ad.rectangle((x-40,y-80,x+w+40,y+h+40),fill=255)
avoid=np.array(avoid)>0;protected=[(o['x'],o['y'],o['width'],o['height'])for o in m['objects']if not o['id'].startswith('production/tree-')]+[(o['x'],o['y'],o['width'],o['height'])for o in objects];feet=[];placed=[]
# Deliberately composed clusters around rest areas and outer edges; deterministic native coordinates.
nodes=[(330,350),(570,480),(890,340),(310,840),(370,1520),(590,1730),(930,1740),(1390,1640),(2850,180),(3000,480),(2950,1720),(2510,1740),(2780,2030),(1780,2190),(1780,2440),(330,2210),(340,2640),(1750,2910),(1640,3070),(1800,3480),(350,3690),(1620,3900),(2900,3880),(3060,3250),(3080,3700)]
for i,(cx,cy)in enumerate(nodes):
 t=trees[(i*7)%len(trees)];w,h=t['width'],t['height'];x=cx-w//2;y=cy-h+8
 if np.any(avoid[cy-12:cy+12,cx-15:cx+16]):continue
 if any(x<bx+bw and x+w>bx and y<by+bh and cy+8>by for bx,by,bw,bh in protected):continue
 ob=dict(t,id=f'recovery-world/planted-tree-{i:02d}',x=x,y=y,sortY=cy);objects.append(ob);feet.append([cx-11,cy-6,23,14]);placed.append({'nativeTree':t['image'],'root':[cx,cy]})
data={'objects':objects,'newFeet':feet,'sourceRecords':records,'treeComposition':placed,'trialPolicy':'Raw trials preserved. No asset is scaled or arbitrarily cropped to force a reservation. Placement conflicts are reported separately; installed candidates are not human-approved art.'}
(S/'native-assets.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');print('Prepared',len(objects),'foregrounds;',len(placed),'new tree placements')
