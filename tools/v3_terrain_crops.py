"""Measure periodic source crops with Forge's actual unchanged seam metric; no RGB painting."""
from v3_final_art import *
import numpy as np
sys.path.insert(0,str(F/'skills/generate2dmap/scripts'));import extract_terrain_tiles as e,forge_core
im=Image.open(S/'raw/terrain.png').convert('RGBA');n=im.width//3;names=['forest','grass','sand','basalt','paver','concrete','asphalt','deep-water','shallow-water'];stack=Image.new('RGBA',(128,128*9));recipes=[]
for i,name in enumerate(names):
 x=i%3*n;y=i//3*n;cell=im.crop((x,y,x+n,y+n));best=None
 def candidate(box):
  a=e.resize_tile(np.array(cell.crop(box)),(128,128),resampler='lanczos',opaque=True,wrap=True);q=[forge_core.edge_seam_report(a,a,gate=1.25),forge_core.edge_seam_report(a.transpose(1,0,2),a.transpose(1,0,2),gate=1.25)];return a,q
 if name not in ['paver','concrete']:box=(0,0,n,n);a,q=candidate(box)
 else:
  for size in range(n,190,-8):
   choices=list(range(0,n-size+1,8));choices+=([n-size]if n-size not in choices else[])
   for yy in choices:
    for xx in choices:
     box0=(xx,yy,xx+size,yy+size);arr,qq=candidate(box0)
     if all(z['verdict']not in ['seam','duplicate_edge']and z['seam_ratio']<=1.12 for z in qq):best=(box0,arr,qq);break
    if best:break
   if best:break
  assert best,name;box,a,q=best
 stack.paste(Image.fromarray(a),(0,i*128));recipes.append({'material':name,'sourceBox':[x+box[0],y+box[1],x+box[2],y+box[3]],'outputSize':[128,128],'method':'Actual Forge resize_tile wrap-aware Lanczos; largest measured passing periodic crop. No arbitrary painted/drawn pixels or threshold relaxation.','wrapX':q[0],'wrapY':q[1]});print(name,box,[z['seam_ratio']for z in q],flush=True)
stack.save(S/'terrain-periodic-rows.png');write(S/'terrain-crops.json',recipes)
