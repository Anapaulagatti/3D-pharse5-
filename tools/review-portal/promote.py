"""Prepare immutable private release with retained snapshots. No remote mutation."""
import argparse,json,hashlib,shutil
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('candidate');p.add_argument('destination');p.add_argument('--previous');a=p.parse_args();src=Path(a.candidate).resolve();dst=Path(a.destination).resolve();previous=Path(a.previous).resolve()if a.previous else None
if src==dst or src.is_relative_to(dst)or dst.is_relative_to(src):raise SystemExit('Candidate/destination must be separate trees')
def verify(root):
 v=json.loads((root/'version.json').read_text());m=json.loads((root/'export-manifest.json').read_text())
 if v['dirty']:raise SystemExit('Cannot promote dirty build; checkpoint source first')
 for x in m['files']:
  f=root/x['filename']
  if not f.is_file()or f.is_symlink()or not f.resolve().is_relative_to(root)or hashlib.sha256(f.read_bytes()).hexdigest()!=x['sha256']:raise SystemExit('Candidate integrity failure')
 return v,m
v,m=verify(src)
if dst.exists():raise SystemExit('Destination must be new; retain old release and switch authenticated host pointer after review')
old_manifest=None
if previous:
 if dst.is_relative_to(previous)or previous.is_relative_to(dst):raise SystemExit('Previous/destination overlap')
 _,old_manifest=verify(previous)
 # Compare immutable snapshot content before creating any release directory.
 for f in (previous/'phases').rglob('*'):
  if f.is_file()and(src/f.relative_to(previous)).exists()and f.read_bytes()!=(src/f.relative_to(previous)).read_bytes():raise SystemExit('Immutable snapshot conflict: '+str(f.relative_to(previous)))
shutil.copytree(src,dst)
if previous:
 for f in (previous/'phases').rglob('*'):
  if f.is_file():
   target=dst/f.relative_to(previous)
   if not target.exists():target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,target)
 h=json.loads((dst/'history.json').read_text());old=json.loads((previous/'history.json').read_text());seen={x['path']for x in h['snapshots']}
 for entry in old['snapshots']:
  if entry['path']not in seen:h['snapshots'].append(entry);seen.add(entry['path'])
 (dst/'history.json').write_text(json.dumps(h,indent=2)+'\n')
 records={x['filename']:x for x in (old_manifest['files']if old_manifest else [])};records.update({x['filename']:x for x in m['files']})
 for f in sorted(dst.rglob('*')):
  if not f.is_file()or f==dst/'export-manifest.json':continue
  name=str(f.relative_to(dst));row=records.get(name,{'filename':name,'origin':'retained immutable previous snapshot manifest','category':'snapshot-manifest','knownTerms':'unchanged upstream review','publicPreviewDecision':'NOT_APPROVED','commercialRelease':'BLOCKED_PENDING_REVIEW','risk':'not cleared','missingEvidence':'explicit exposure and rights review'});row.update({'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'bytes':f.stat().st_size});records[name]=row
 m['files']=sorted(records.values(),key=lambda x:x['filename']);(dst/'export-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
verify(dst)
print('PRIVATE release verified with retained immutable snapshots; no host or public deployment changed.')
