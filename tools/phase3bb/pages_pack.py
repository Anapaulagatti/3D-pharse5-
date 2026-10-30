"""Pack exactly allowlisted regular files, including prior approved .vite metadata.
The upstream Pages uploader excludes dot paths, breaking retained snapshot URLs.
Approval, hashes and history gates run before this transport-only step.
"""
from pathlib import Path
import sys,json,hashlib,tarfile
root=Path(sys.argv[1]).resolve();dest=Path(sys.argv[2]);m=json.loads((root/'export-manifest.json').read_text());names={r['filename']for r in m['files']};actual={str(p.relative_to(root))for p in root.rglob('*')if p.is_file()}
assert actual==names|{'export-manifest.json'},'Unexpected export files'
for row in m['files']:
 p=root/row['filename'];assert p.is_file()and not p.is_symlink()and p.resolve().is_relative_to(root);assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'],row['filename']
with tarfile.open(dest,'w',format=tarfile.GNU_FORMAT)as archive:
 for name in sorted(actual):
  p=root/name;assert '.git'not in p.parts and '.github'not in p.parts
  info=archive.gettarinfo(str(p),arcname=name);info.mode=0o644;info.uid=info.gid=0;info.uname=info.gname='';
  with p.open('rb')as f:archive.addfile(info,f)
with tarfile.open(dest)as archive:assert set(archive.getnames())==actual
print('PASS exact Pages tar:',len(actual),'regular files; approved dot-path metadata retained; no Git/source history')
