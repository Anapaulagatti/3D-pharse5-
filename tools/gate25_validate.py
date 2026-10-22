from pathlib import Path
from PIL import Image
import numpy as np,json,shutil
R=Path(__file__).resolve().parents[1];P=R/'public/assets/gate2';D=R/'docs/gate25';sc=json.loads((P/'district/scene.json').read_text());W,H=sc['size'];coverage=np.zeros((H,W),np.uint8);checks=[]
for chunk,original in zip(sc['grounds'],['b','original','station']):
 im=Image.open(P/chunk['image']).convert('RGBA');source=Image.open(P/original/'ground.png').convert('RGBA');assert im.size==source.size;assert im.convert('RGB').tobytes()==source.convert('RGB').tobytes();alpha=np.array(im.getchannel('A'));assert set(np.unique(alpha))<={0,255};x,y=chunk['x'],chunk['y'];h,w=alpha.shape;coverage[y:y+h,x:x+w][alpha>0]=1;checks.append(dict(chunk=chunk['id'],originalDimensions=list(source.size),nativeRGBExact=True,binaryOwnership=True))
mask=np.array(Image.open(P/'district/walk.png').convert('L'));assert np.count_nonzero((mask>127)&(coverage==0))==0
for ob in sc['objects']:
 im=Image.open(P/ob['image']).convert('RGBA');assert im.size==(ob['width'],ob['height']);assert ob['sortY']==next(o for o in json.loads((P/'b/scene.json').read_text())['objects'] if 'district-'+o['id']==ob['id'])['sortY']+190
# Conservative full-resolution route connectivity (pixel-level4-connected regions).
from scipy.ndimage import label
labels,n=label(mask>127);sx,sy=sc['spawn'];region=labels[sy,sx];assert region
for t in sc['targets']:assert labels[t['y'],t['x']]==region,t
(D/'collision-source-report.json').write_text(json.dumps(dict(chunks=checks,nativeScale=1,walkablePixelsOutsideArtworkCoverage=0,allEntrancesConnected=True,connectedComponents=int(n),objects=len(sc['objects']),sortYTranslationExact=True,sourceMaskChanges='new district only: seam clearance and station bench keepouts',noGlobalAssetResampling=True,unpaintedMarginsNonwalkable=True,productionSeamMaterials='FAIL / sidewalk grid, asphalt paint and vertical scene boundary are not a production tile kit'),indent=2)+'\n')
(D/'physical-devices.json').write_text(json.dumps(dict(androidChrome='NOT TESTED',iPhoneSafari='NOT TESTED',adbExecutable=shutil.which('adb'),usbDeviceDirectoryPresent=Path('/dev/bus/usb').exists(),deviceControlConnectorAvailable=False,reason='No connected physical device interface is exposed in this cloud session; no hardware conclusions from emulation',handoff='DEVICE_TESTING.md'),indent=2)+'\n')
print('PASS district native RGB, collision, source/occlusion metadata; physical devices NOT TESTED')
