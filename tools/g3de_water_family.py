"""REJECTED DIAGNOSTIC TRIAL ONLY. Not imported by the production residual build. The true root is the shared native material wrap; do not expand canonical water ownership."""
from pathlib import Path
import json
import numpy as np
from PIL import Image
from scipy.ndimage import label,distance_transform_edt

def apply_offshore(g,R,S):
 # Image-frame distance is not coastline distance. Only water beyond the true
 # native land/foam/rock72px rim can join the already shared offshore family.
 c=np.array(Image.open(R/'public/assets/gate2/c/ground.png').convert('RGBA'));r,gg,b=[c[:,:,k].astype(float)for k in range(3)];water=(b>r*1.45)&(gg>r*1.3)&(b>70);structural=((r>=b*.8)&(r>=gg*.6)&(b<170))|((gg>b*1.4)&(gg>=r*.9)&(b<125)&(gg>40));labs,_=label(structural);sizes=np.bincount(labs.ravel());physical=(labs>0)&(sizes[labs]>=36);dist=distance_transform_edt(~physical);protected=(dist<=72)|~water
 yy,xx=np.indices(water.shape,dtype=np.uint32);edge=np.minimum.reduce([xx,1023-xx,yy,1535-yy]);depthWeight=np.clip((dist-72)/96,0,1);edgeWeight=np.clip((96-edge.astype(float))/96,0,1);weight=np.maximum(depthWeight,edgeWeight);weight[protected]=0
 # Native binary texel ownership, never RGB blending, sharpening or filtering.
 noise=(xx*73856093)^(yy*19349663);noise=(noise^(noise>>13))*np.uint32(1274126177);noise=(noise%65536)/65536
 current=np.array(g.crop((3180,3200,4204,4736)));r,gg,b=[current[:,:,k].astype(float)for k in range(3)];currentlyWater=(b>r*1.4)&(gg>r*1.25)&(b>70);mask=water&currentlyWater&~protected&(noise<weight)
 plate=np.array(Image.open(R/'assets-src/gate3/reconciliation-v1/ocean-authored.png').convert('RGBA'));surface=plate[yy%1024,xx%1536];change=mask&np.any(current!=surface,axis=2);after=current.copy();after[mask]=surface[mask];assert np.array_equal(after[protected],current[protected]);g.paste(Image.fromarray(after),(3180,3200))
 Image.fromarray(mask.astype('uint8')*255).save(S/'shared-water-offshore-v2-mask.png');Image.fromarray(protected.astype('uint8')*255).save(S/'jeju-physical-shore72-protection.png')
 oldKeep=np.array(Image.open(R/'assets-src/gate3/reconciliation-v1/jeju-protected-land-nearshore.png'))>0
 record={'id':'shared-offshore-ownership-v2','scope':'Shared offshore surface around canonical C, source-frame edge is not island/coast geometry. No land/foam/architecture/paths/geometry change.','worldRect':[3180,3200,1024,1536],'source':'assets-src/gate3/reconciliation-v1/ocean-authored.png','phase':[3180,3200],'sourceFileCanonical':'UNCHANGED','actualIslandAndNearshore':'EXACT versus pre-pass current composition: all non-water and72px radius from original native physical basalt/land/vegetation clusters; foam/nonwater pixels also exact. Approved turquoise shallows retained.','transition':'72..168px true coastal depth;96px frame margin only for OFFSHORE continuity. Binary native texels/world-stable ownership, no resampling/RGB interpolation/reflection or new rocks/shadows.','mask':'shared-water-offshore-v2-mask.png','physicalProtection':'jeju-physical-shore72-protection.png','changedPixels':int(change.sum()),'oldConservativeFrameGuardOffshoreExceptions':int((change&oldKeep).sum()),'versioning':'Explicit derived-water ownership revision. Historical conservative bitmap/approved source PNG/plans remain immutable. Only actual offshore water previously protected merely by image-frame coordinates is excepted under current shared-water correction authority.','humanArtAcceptance':'PENDING REVIEW'}
 (S/'shared-water-registry-v2.json').write_text(json.dumps(record,indent=2)+'\n');return g,record

if __name__=='__main__':
 R=Path(__file__).resolve().parents[1];S=R/'assets-src/gate3/residual-v1';m=json.loads((R/'public/assets/gate3/residual-world/manifest.json').read_text());g=Image.new('RGBA',m['size'])
 for c in m['chunks']:g.paste(Image.open(R/'public'/c['image']),(c['x'],c['y']))
 g,q=apply_offshore(g,R,S)
 for o in sorted(m['objects'],key=lambda o:o['sortY']):g.alpha_composite(Image.open(R/'public'/o['image']).convert('RGBA'),(o['x'],o['y']))
 g.crop((2300,3530,3580,4430)).save('/tmp/g3de-coast-water-draft.png');print(json.dumps(q,indent=2))
