from pathlib import Path
import json
R=Path(__file__).resolve().parents[2]
def runtime_names():
 m=json.loads((R/'public/assets/gate3/palace-cleanup-world/manifest.json').read_text());names={'assets/gate3/palace-cleanup-world/manifest.json',m['overview'],m['farmMetadata'],m['contactCollision']['physical'],'assets/juni/juni.png','assets/juni/juni.json','assets/character-studio/juni-preview.png'}|{c[k]for c in m['chunks']for k in ['image','mask']}|{o['image']for o in m['objects']}
 for id in json.loads((R/'assets-src/characters/phase2c/base-bindings.json').read_text()):
  if id!='juni':
   for n in ['atlas.png','atlas.json','preview-native.png']:names.add(f'assets/characters/{id}/{n}')
 for stem in ['assets/cosmetics/phase2c','assets/npcs/phase3a']:
  for p in(R/'public'/stem).rglob('*'):
   if p.is_file():names.add(str(p.relative_to(R/'public')))
 return names
if __name__=='__main__':
 names=runtime_names();print('Runtime assets',len(names),'MiB',sum((R/'public'/n).stat().st_size for n in names)/1048576)
 for stem in ['assets-src/npcs/phase3a-npc-expansion','docs/phase3a-npc-expansion/gameplay']:
  sizes={}
  for p in(R/stem).rglob('*'):
   if p.is_file():sizes[p.suffix]=sizes.get(p.suffix,0)+p.stat().st_size
  print(stem,{k:round(v/1048576,2)for k,v in sizes.items()})
