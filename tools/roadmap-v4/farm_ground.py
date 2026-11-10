"""Derived native soil ownership only; approved source atlas/world remain immutable."""
from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json,numpy as np
R=Path.cwd();O=R/'public/assets/roadmap-v4/farm';S=R/'assets-src/roadmap-v4/farm';O.mkdir(parents=True,exist_ok=True);S.mkdir(parents=True,exist_ok=True)
meta=json.loads((R/'public/assets/farming/phase3bd-final-quality/soil-components.json').read_text());atlas=Image.open(R/'public/assets/farming/phase3bd-final-quality/soil-components.png').convert('RGBA');farm=json.loads((R/'public/assets/gate3/final-world/farm-plots.json').read_text());rows=[]
for i,p in enumerate(farm['plots']):
 x,y,w,h=p['worldRect'];left=x+12;top=y+12;rw=156;rh=104;im=Image.new('RGBA',(rw,rh));mask=Image.new('L',(rw,rh));d=ImageDraw.Draw(mask)
 # Inside the original raised bed. Stepped edge follows native earth, no alpha feather/filter.
 polygon=[(5,0),(rw-6,0),(rw-6,3),(rw-2,3),(rw-2,13),(rw-1,13),(rw-1,rh-7),(rw-6,rh-7),(rw-6,rh-2),(7,rh-2),(7,rh-4),(1,rh-4),(1,12),(3,12),(3,3),(5,3)]
 d.polygon(polygon,fill=255)
 for yy in range(0,rh,16):
  for xx in range(0,rw,16):
   k=f'loam-{((xx//16)*7+(yy//16)*11+(xx//16)*(yy//16)*5+i*3)%12}';f=meta['frames'][k]['frame'];tile=atlas.crop((f['x'],f['y'],f['x']+f['w'],f['y']+f['h']));im.paste(tile,(xx,yy))
 im.putalpha(mask);a=np.array(im);a[a[:,:,3]==0,:3]=0;im=Image.fromarray(a);name=p['id']+'.png';im.save(O/name);mask.save(S/(p['id']+'-repair-mask.png'));im.save(S/name);rows.append({'id':p['id'],'x':left,'y':top,'width':rw,'height':rh,'image':'assets/roadmap-v4/farm/'+name,'mask':'assets-src/roadmap-v4/farm/'+p['id']+'-repair-mask.png','opaquePixels':int((a[:,:,3]==255).sum()),'outsideOwnershipPixels':0,'sha256':hashlib.sha256((O/name).read_bytes()).hexdigest()})
# Recover original native rim ownership above soil, rather than hiding it under expanded ground.
source=Image.open(R/'assets-src/gate3/final-surgical-v1/farm-authored.png').convert('RGBA')
for p,row in zip(farm['plots'],rows):
 sx,sy,sw,sh=p['sourceRect'];original=source.crop((sx,sy,sx+sw,sy+sh));a=np.array(original);yy,xx=np.indices((sh,sw));inner=(xx>=17)&(xx<151)&(yy>=20)&(yy<102)
 for layer,ownership in [('rim-back',yy<20),('rim-front',(~inner)&(yy>=20))]:
  v=a.copy();v[~ownership]=0;name=p['id']+'-'+layer+'.png';Image.fromarray(v).save(O/name);Image.fromarray(v).save(S/name);row[layer]={'image':'assets/roadmap-v4/farm/'+name,'sha256':hashlib.sha256((O/name).read_bytes()).hexdigest(),'position':p['worldRect'][:2],'depth':p['worldRect'][1]+(22 if layer=='rim-back'else 128),'sourceRect':p['sourceRect'],'resampling':False,'originalNativePixels':True}
 row['visibleSoilOwnership']={'insideOriginalRim':[p['worldRect'][0]+17,p['worldRect'][1]+20,134,82],'outsideNativeBorderReplacementPixels':0}
q={'art_source' :'derived native material composition','inputs':['public/assets/farming/phase3bd-final-quality/soil-components.png','public/assets/farming/phase3bd-final-quality/soil-components.json'],'providerCalls':0,'sourcePixelScale':1,'resampling':False,'filters':False,'purpose':'Fill cultivated interior edge/gaps beneath 36 independent cells; original rail/path/world pixels untouched','humanArtApproval':'PENDING','beds':rows};(O/'ownership.json').write_text(json.dumps(q,indent=2)+'\n');(S/'PROVENANCE.json').write_text(json.dumps(q,indent=2)+'\n');print(json.dumps(q,indent=2))
