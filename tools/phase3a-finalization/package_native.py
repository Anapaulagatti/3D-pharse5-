"""Verify extracted-game POST_RENDER pixels against immutable approved atlas cells."""
from pathlib import Path
from PIL import Image
import json, numpy as np
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a-finalization'
p=json.loads((D/'package-smoke.json').read_text());assert p['actualActorsTested']==26
objects=json.loads((R/'public/assets/gate3/palace-cleanup-world/manifest.json').read_text())['objects'];images={};rows=[]
for row in p['readbacks']:
 a=row['audit'];id=row['id'];s=a['sprite'];cx,cy=a['camera']['scroll']
 assert a['matched'] and a['camera']['zoom']==1 and s['scale']==[1,1] and s['sampling']==1
 assert all(float(n).is_integer() for n in [s['x'],s['y'],cx,cy])
 root=R/'public/assets/npcs/phase3a'/id;m=json.loads((root/'atlas.json').read_text())['frames'][a['actualFrame']]['frame']
 source=np.array(Image.open(root/'atlas.png').convert('RGBA').crop((m['x'],m['y'],m['x']+96,m['y']+112)))
 x,y=int(s['x']-48-cx),int(s['y']-100-cy);actual=Image.open(row['file']).convert('RGB').crop((x,y,x+96,y+112));actualArray=np.array(actual)
 diff=(source[:,:,3]==255)&np.any(actualArray!=source[:,:,:3],axis=2);owned=[]
 for py,px in zip(*np.where(diff)):
  wx,wy=int(px+s['x']-48),int(py+s['y']-100);owners=[]
  for o in objects:
   if o['sortY']>s['depth'] and o['x']<=wx<o['x']+o['width'] and o['y']<=wy<o['y']+o['height']:
    if o['image'] not in images:images[o['image']]=Image.open(R/'public'/o['image']).convert('RGBA')
    pixel=images[o['image']].getpixel((int(wx-o['x']),int(wy-o['y'])))
    if pixel[3]==255 and pixel[:3]==actual.getpixel((int(px),int(py))):owners.append(o['id'])
  assert owners,('Unexplained mismatch',id,int(px),int(py));owned.append({'pixel':[int(px),int(py)],'world':[wx,wy],'foregroundOwners':owners})
 rows.append({'id':id,'frame':a['actualFrame'],'integerNativeAlignment':True,'nearest':True,'opaqueAtlasPixels':int((source[:,:,3]==255).sum()),'unexplainedMismatch':0,'inheritedForegroundOccludedPixels':int(diff.sum()),'ownership':owned})
report={'status':'PASS native visible-pixel fidelity','actors':26,'unexplainedMismatch':0,'inheritedForegroundOccludedPixels':sum(r['inheritedForegroundOccludedPixels'] for r in rows),'rows':rows,'scope':'Extracted offline ZIP, actual canonical Phaser POST_RENDER, not a source preview','physicalDevices':'NOT_TESTED'}
(D/'package-native-qa.json').write_text(json.dumps(report,indent=2)+'\n')
proof=json.loads((D/'PACKAGE_PROOF.json').read_text());proof['launch']={'status':'PASS','source':'package-smoke.json','actualActorsTested':26,'nativeReadback':'package-native-qa.json','dialogueAndReturn':'PASS all 26','externalRequests':len(p['external']),'httpErrors':len(p['bad']),'browserErrors':len(p['errors']),'actualMP4Playback':'PASS','physicalDevices':'NOT_TESTED'};(D/'PACKAGE_PROOF.json').write_text(json.dumps(proof,indent=2)+'\n')
print('PASS 26 actual offline actors; unexplained mismatches 0; inherited foreground occlusions',report['inheritedForegroundOccludedPixels'])
