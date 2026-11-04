"""Explicit current runtime closure. No directory auto-discovery of worlds."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[2]
CANONICAL='assets/gate3/palace-cleanup-world/manifest.json'
RETIRED={'ara-shell-barrette','kr-hair-ornament','kr-fashion-cap','kr-garden-hat'}
def runtime_names():
 m=json.loads((R/'public'/CANONICAL).read_text());names={CANONICAL,m['overview'],m['farmMetadata'],m['contactCollision']['physical'],'assets/juni/juni.png','assets/juni/juni.json','assets/character-studio/juni-preview.png'}
 names|={c[k]for c in m['chunks']for k in ['image','mask']};names|={o['image']for o in m['objects']}
 a=json.loads((R/'src/gate3/phase3bc-collision.json').read_text());names|={c['mask']for c in a['chunks']}
 for id in json.loads((R/'assets-src/characters/phase2c/base-bindings.json').read_text()):
  if id!='juni':names|={f'assets/characters/{id}/{n}'for n in ['atlas.png','atlas.json','preview-native.png']}
 cat=json.loads((R/'assets-src/characters/phase2c/catalog.json').read_text())
 for item in cat['items']:
  if item['id']not in RETIRED:
   for v in item['variants']:
    names|={v[k]for k in ['paint','erase','mapping','preview']}
 for item in cat.get('interactions',[]):
  if not RETIRED.intersection(item['requiresItemIds']):names|={item['patch'][k]for k in ['paint','erase','mapping','preview']}
 for source in ['phase3a/registry.json','phase3a-npc-expansion/modern-definitions.json','phase3a-final-six/definitions.json']:
  for npc in json.loads((R/'assets-src/npcs'/source).read_text())['npcs']:
   names|={npc['assets']['texture'],npc['assets']['atlas']}
 names|={'assets/farming/crops.png','assets/farming/crops.json','assets/farming/postcard.png','assets/farming/interaction-tools.png','assets/farming/interaction-tools.json'}
 return names
if __name__=='__main__':print(json.dumps(sorted(runtime_names()),indent=2))
