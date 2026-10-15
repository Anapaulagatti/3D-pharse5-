"""Original generated pixel-object source -> documented native-grid game sprites, not a backdrop."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,subprocess,collections,random,shutil
R=Path(__file__).resolve().parents[1];subprocess.run(['python3',str(R/'tools/export_unified.py')],check=True)
S=R/'assets-src/unified-v4';O=R/'public-unified/assets/unified-v4';source=S/'reference-source/original-atlas.png';raw=Image.open(source).convert('RGBA')
spec={'hanok':([0,0,556,354],[200,136]),'academy':([0,0,556,354],[200,136]),'cafe':([559,0,1031,357],[184,132]),'courier':([1047,0,1536,366],[184,136]),'tree':([8,358,501,748],[112,96]),'pine':([547,359,1031,748],[112,96]),'plum':([1061,358,1536,748],[112,96]),'wall':([25,751,637,1024],[120,50]),'jars':([674,773,1027,1024],[40,40]),'board':([1104,730,1449,1024],[52,48])}
# Alpha-threshold + largest8-connected component isolates each object from neighboring cells and low-alpha glow.
def isolate(im):
 im=im.copy();alpha=im.getchannel('A').point(lambda x:255 if x>=180 else 0);w,h=im.size;data=alpha.load();seen=set();best=[]
 for y in range(h):
  for x in range(w):
   if data[x,y] and (x,y) not in seen:
    q=[(x,y)];seen.add((x,y));comp=[]
    while q:
     xx,yy=q.pop();comp.append((xx,yy))
     for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)]:
      nx,ny=xx+dx,yy+dy
      if 0<=nx<w and 0<=ny<h and data[nx,ny] and (nx,ny) not in seen:seen.add((nx,ny));q.append((nx,ny))
    if len(comp)>len(best):best=comp
 mask=Image.new('L',im.size);px=mask.load()
 for x,y in best:px[x,y]=255
 im.putalpha(mask);return im.crop(mask.getbbox())
crops={k:isolate(raw.crop(tuple(v[0]))) for k,v in spec.items()}
# One shared128-color world palette learned from this single original source atlas; no dithering/soft alpha.
strip=Image.new('RGB',(1536,1024),'#e6d2ac');strip.paste(raw.convert('RGB'),mask=raw.getchannel('A'));palette=strip.quantize(colors=128,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
for k,im in crops.items():
 size=spec[k][1];im=im.resize(tuple(size),Image.Resampling.NEAREST);a=im.getchannel('A');out=im.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');out.putalpha(a.point(lambda v:255 if v>=128 else 0));out.paste((0,0,0,0),(0,0),a.point(lambda v:255 if v<128 else 0));out.save(S/(k+'.png'));out.save(O/(k+'.png'))
# Warm sand, irregular pale stepping stones and quiet grass seams, authored on the same1px grid.
rng=random.Random(4416);tile=Image.open(O/'tiles.png').convert('RGBA');d=ImageDraw.Draw(tile)
for i in list(range(4,10))+[15]:
 x=(i%8)*32;y=(i//8)*32;d.rectangle((x,y,x+31,y+31),fill='#e4cfa7' if i%2 else '#dfc9a0')
 for j in range(11):
  xx=x+rng.randrange(2,30);yy=y+rng.randrange(2,30);d.line((xx,yy,xx+1,yy),fill='#d3ba92' if j%2 else '#ead8b5')
 if i in [4,6,8]:
  d.polygon([(x+4,y+13),(x+10,y+8),(x+22,y+9),(x+27,y+14),(x+23,y+23),(x+8,y+24),(x+3,y+20)],fill='#adab98');d.polygon([(x+4,y+12),(x+10,y+7),(x+22,y+8),(x+27,y+13),(x+23,y+21),(x+8,y+22),(x+3,y+19)],fill='#d4d0b8');d.line((x+8,y+10,x+21,y+10),fill='#e8e0c5')
tile.save(S/'tiles.png');tile.save(O/'tiles.png')
# Softer low stone well instead of a floating geometric emblem.
im=Image.new('RGBA',(80,56));d=ImageDraw.Draw(im)
def poly(p,c):d.polygon(p,fill=c)
poly([(7,24),(13,17),(27,12),(53,12),(67,17),(73,24),(71,42),(59,49),(23,49),(9,42)],'#696e66');poly([(8,22),(16,16),(29,13),(52,13),(65,17),(72,23),(66,33),(54,39),(26,39),(13,33)],'#c4c2ad');poly([(17,23),(25,19),(54,19),(63,23),(59,29),(51,33),(29,33),(20,29)],'#4c7475');d.line([(22,24),(29,21),(51,21),(57,24)],fill='#8fbbb0',width=2);d.line([(17,35),(27,40),(54,40),(66,34)],fill='#959b8d',width=2)
for xx,yy in [(18,38),(34,42),(52,41),(65,35)]:d.line([(xx,yy),(xx,yy+6)],fill='#565e58')
for p in [S/'fountain.png',O/'fountain.png']:im.save(p)
# Regenerate authoritative per-file hashes after the reference refinement.
m=json.loads((S/'manifest.json').read_text());m['original']=True;m['provenance']='Original native image_gen pixel object atlas plus code-raster layered chibi/tiles/small props. User reference used for visual qualities only; no copied pixels or map. Source atlas/crops/transforms retained; not every object pixel manually placed.';m['world_palette_limit']=128;m['reference_source']={'file':'reference-source/original-atlas.png','sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_size':list(raw.size),'crop_native_sizes':spec,'transform':'Alpha180, largest8connected component, NEAREST native resize, shared128color palette, no dithering, binary alpha. Not a scene backdrop.'};m['files']=[{'path':str(p.relative_to(O)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in sorted(O.iterdir()) if p.is_file()];(S/'manifest.json').write_text(json.dumps(m,indent=2)+'\n');(S/'reference-source/provenance.json').write_text(json.dumps(m['reference_source'],indent=2)+'\n');print('Original reference-refined sprite kit exported',len(m['files']),'files')
