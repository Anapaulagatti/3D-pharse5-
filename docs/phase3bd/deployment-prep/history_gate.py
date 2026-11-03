"""Prior approved snapshots must remain byte-identical when promoting or rolling back."""
import json,hashlib,sys
from pathlib import Path
site=Path(sys.argv[1]).resolve();paths=list(Path('approved-releases/history').glob('*.json'))+[Path(sys.argv[2])]
for receipt in paths:
 q=json.loads(receipt.read_text())
 if q.get('decision')!='APPROVED_PUBLIC_PREVIEW':continue
 for name,expected in q.get('snapshotManifests',{}).items():
  p=site/name
  if not p.resolve().is_relative_to(site)or not name.startswith('phases/')or not p.is_file()or hashlib.sha256(p.read_bytes()).hexdigest()!=expected:raise SystemExit('Prior immutable snapshot missing or altered: '+name)
print('PASS retained snapshot manifests')
