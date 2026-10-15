"""Copy editable accepted world source to runtime. Never regenerate acceptable artwork."""
from pathlib import Path
import json,hashlib,shutil
R=Path(__file__).resolve().parents[1];S=R/'assets-src/world';O=R/'public/assets/world';O.mkdir(parents=True,exist_ok=True)
m=json.loads((S/'manifest.json').read_text())
for r in m['files']:
 p=S/r['name'];assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
 if p.name!='world.json':shutil.copy2(p,O/p.name)
print('World export: exact source PNG/Tiled bytes retained, no art regenerated.')
