"""Strict old-site retention OR explicitly owner-approved immutable Git archive."""
import json,hashlib,sys,subprocess
from pathlib import Path
site=Path(sys.argv[1]).resolve();q=json.loads(Path(sys.argv[2]).read_text());paths=list(Path('approved-releases/history').glob('*.json'))+[Path(sys.argv[2])];expected={}
for receipt in paths:
 r=json.loads(receipt.read_text())
 if r.get('decision')!='APPROVED_PUBLIC_PREVIEW':continue
 for name,digest in r.get('snapshotManifests',{}).items():
  if name in expected and expected[name]!=digest:raise SystemExit('Conflicting historical manifest pin')
  expected[name]=digest
am=q.get('historyRetentionAmendment');archive=site
if q.get('profile')=='roadmap-v2-local26':
 if q.get('decision')!='APPROVED_PUBLIC_PREVIEW' or not q.get('approvedBy')or not q.get('approvedAt')or not am or am.get('decision')!='APPROVED_BY_OWNER' or am.get('policy')!='IMMUTABLE_GIT_ARCHIVE_INSTEAD_OF_DUPLICATED_SITE' or am.get('artifactCommit')!='1a6e5a58a8fb515730e553a30980d2ffb7274da6' or am.get('manifestSHA256')!='331cd300478f879bab11e9541803dd7c47ba1caaab339263f37150ae6c0d0ce4' or am.get('snapshotManifests')!=expected:raise SystemExit('BLOCKED: exact owner history amendment absent or incomplete')
 if len(sys.argv)!=4:raise SystemExit('Pinned immutable Git checkout required')
 archive=Path(sys.argv[3]).resolve()
 if subprocess.check_output(['git','rev-parse','HEAD'],cwd=archive,text=True).strip()!=am['artifactCommit']:raise SystemExit('Wrong immutable history commit')
 if hashlib.sha256((archive/'export-manifest.json').read_bytes()).hexdigest()!=am['manifestSHA256']:raise SystemExit('Wrong immutable history root manifest')
 manifest=json.loads((archive/'export-manifest.json').read_text())
 for row in manifest['files']:
  f=archive/row['filename']
  if f.is_symlink()or not f.resolve().is_relative_to(archive)or not f.is_file()or hashlib.sha256(f.read_bytes()).hexdigest()!=row['sha256']:raise SystemExit('Immutable historical asset mismatch: '+row['filename'])
for name,digest in expected.items():
 f=archive/name
 if f.is_symlink()or not f.resolve().is_relative_to(archive)or not name.startswith('phases/')or not f.is_file()or hashlib.sha256(f.read_bytes()).hexdigest()!=digest:raise SystemExit('Prior immutable snapshot missing or altered: '+name)
print('PASS retained snapshot manifests; exact immutable archive verified'if archive!=site else'PASS retained snapshot manifests in site')
