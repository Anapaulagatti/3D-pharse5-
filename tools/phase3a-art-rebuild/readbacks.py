"""Compare real POST_RENDER native Phaser pixels to actual source cells,not source previews."""
from pathlib import Path
from PIL import Image
import json,numpy as np,math
R=Path(__file__).resolve().parents[2];D=R/'docs/phase3a-art-rebuild';out=D/'native';out.mkdir(exist_ok=True);reports=[];manifest=json.loads((R/'public/assets/gate3/palace-cleanup-world/manifest.json').read_text());objects=manifest['objects'];objectImages={}
for mode in ['before','after']:
 q=json.loads((D/f'{mode}-capture.json').read_text())
 for r in q['captures']:
  a=r['audit'];id=a['npcId'];stem=R/'public/assets/npcs/phase3a'/id;atlas=D/'before-source'/(id+'-atlas.png')if mode=='before'else stem/'atlas.png';meta=json.loads((stem/'atlas.json').read_text())['frames'][a['actualFrame']]['frame'];source=Image.open(atlas).convert('RGBA').crop((meta['x'],meta['y'],meta['x']+96,meta['y']+112));s=a['sprite'];sx,sy=a['camera']['scroll'];assert a['camera']['zoom']==1 and s['scale']==[1,1]and s['sampling']==1;assert all(float(n).is_integer()for n in [s['x'],s['y'],sx,sy]);x=s['x']-48-sx;y=s['y']-100-sy;actual=Image.open(r['sourcePath']).convert('RGB').crop((x,y,x+96,y+112));b=np.array(source);diff=int(((b[:,:,3]==255)&np.any(np.array(actual)!=b[:,:,:3],axis=2)).sum());occlusions=[]
  for py,px in zip(*np.where((b[:,:,3]==255)&np.any(np.array(actual)!=b[:,:,:3],axis=2))):
   wx=int(px+s['x']-48);wy=int(py+s['y']-100);owners=[]
   for o in objects:
    if o['sortY']>s['depth']and o['x']<=wx<o['x']+o['width']and o['y']<=wy<o['y']+o['height']:
     if o['image']not in objectImages:objectImages[o['image']]=Image.open(R/'public'/o['image']).convert('RGBA')
     pixel=objectImages[o['image']].getpixel((int(wx-o['x']),int(wy-o['y'])))
     if pixel[3]==255 and pixel[:3]==actual.getpixel((int(px),int(py))):owners.append({'object':o['id'],'image':o['image'],'sortY':o['sortY'],'exactRGBA':pixel})
   assert owners,(mode,id,a['actualFrame'],'UNEXPLAINED pixel',int(px),int(py));occlusions.append({'native':[int(px),int(py)],'world':[wx,wy],'owners':owners})
  file=f'{mode}-{id}-{a["actualFrame"]}-actual-body-native.png';actual.save(out/file);reports.append({'mode':mode,'id':id,'frame':a['actualFrame'],'native':[96,112],'opaqueSourcePixelsOccludedByExistingForeground':diff,'unexplainedMismatch':0,'foregroundOwnershipProof':occlusions,'opaqueSourcePixels':int((b[:,:,3]==255).sum()),'integerPhase':True,'nearest':True,'actualWorld':'palace-cleanup-world','file':'native/'+file})
(D/'native-render-qa.json').write_text(json.dumps({'status':'PASS visible-pixel fidelity;WARN inherited foreground occlusion','actualCaptures':len(reports),'unexplainedMismatch':sum(r['unexplainedMismatch']for r in reports),'existingForegroundOccludedPixels':sum(r['opaqueSourcePixelsOccludedByExistingForeground']for r in reports),'rows':reports,'scope':'Actual canonical Phaser,not clip-inspector or source-sheet mock gameplay','humanArtApproval':'PENDING'},indent=2)+'\n');print('PASS',len(reports),'actualnative before/after Phaserbody readbacks;0UNEXPLAINED mismatch;existing foreground occlusions documented')
