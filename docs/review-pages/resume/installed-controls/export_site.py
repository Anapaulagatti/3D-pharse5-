"""Extract only the declared prior approved site from its Git checkout, excluding .git."""
from pathlib import Path
import sys,json,shutil,hashlib
S=Path(sys.argv[1]).resolve();O=Path(sys.argv[2]).resolve();m=json.loads((S/'export-manifest.json').read_text());O.mkdir(parents=True)
for row in m['files']:
 p=S/row['filename']
 if p.is_symlink()or not p.resolve().is_relative_to(S)or hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:raise SystemExit('Prior release integrity failure')
 q=O/row['filename'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
shutil.copy2(S/'export-manifest.json',O/'export-manifest.json')
