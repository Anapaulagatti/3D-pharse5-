"""Exact, versioned owner-authorized code/catalog amendments; never a wildcard.
Historical checks still inspect the old baseline; current behavioral checks inspect
these pinned revisions. No original art, source manifest or old checkpoint changes.
"""
from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[2]
def historical_bytes(name,expected=None):
 cleanup=R/'docs/cleanup/REJECTED_WORLD_CLEANUP_20261103.json'
 if not (R/name).exists() and cleanup.exists():
  q=json.loads(cleanup.read_text());row=next((r for r in q['removed']if r['path']==name),None)
  if not row:
   moved=next((r for r in q.get('archiveMoves',[])if r['from']==name),None)
   if moved:
    data=(R/moved['to']).read_bytes();assert hashlib.sha256(data).hexdigest()==moved['sha256']
    if expected:assert expected==moved['sha256']
    return data
  assert row,('Unapproved missing protected file',name)
  old=subprocess.check_output(['git','show',q['base']+':'+name],cwd=R)
  assert hashlib.sha256(old).hexdigest()==row['sha256']
  if expected:assert expected==row['sha256'],('Historical removed file predecessor mismatch',name)
  return old
 current=(R/name).read_bytes()
 hotfix=R/'docs/phase3bd-farm-path/AUTHORIZED_AMENDMENTS.json'
 if hotfix.exists():
  q=json.loads(hotfix.read_text());row=q['files'].get(name)
  if row:
   assert hashlib.sha256(current).hexdigest()==row['afterSHA256'],('Farm/path hotfix drift',name)
   current=subprocess.check_output(['git','show',q['base']+':'+name],cwd=R)
   assert hashlib.sha256(current).hexdigest()==row['beforeSHA256']

 physical=R/'docs/phase3bd-in-world/AUTHORIZED_AMENDMENTS.json'
 if physical.exists():
  q=json.loads(physical.read_text());row=q['files'].get(name)
  if row:
   assert hashlib.sha256(current).hexdigest()==row['afterSHA256'],('Physical interaction source drift',name)
   current=subprocess.check_output(['git','show',q['base']+':'+name],cwd=R)
   assert hashlib.sha256(current).hexdigest()==row['beforeSHA256']

 amendment=R/'docs/phase3bd/AUTHORIZED_AMENDMENTS.json'
 if amendment.exists():
  q=json.loads(amendment.read_text());row=q['files'].get(name)
  if row:
   assert hashlib.sha256(current).hexdigest()==row['afterSHA256'],('Phase3BD amendment drift',name)
   current=subprocess.check_output(['git','show',q['base']+':'+name],cwd=R)
   assert hashlib.sha256(current).hexdigest()==row['beforeSHA256']
 latest=R/'docs/phase3bc/AUTHORIZED_AMENDMENTS.json'
 if latest.exists():
  q=json.loads(latest.read_text());row=q['files'].get(name)
  if row:
   assert hashlib.sha256(current).hexdigest()==row['afterSHA256'],('Phase3BC amendment drift',name)
   current=subprocess.check_output(['git','show',q['base']+':'+name],cwd=R)
   assert hashlib.sha256(current).hexdigest()==row['beforeSHA256']
 manifest=R/'docs/phase3bb-hotfix/AUTHORIZED_AMENDMENTS.json'
 if not manifest.exists():return current
 q=json.loads(manifest.read_text());row=q['files'].get(name)
 if not row:return current
 assert hashlib.sha256(current).hexdigest()==row['afterSHA256'],('Amendment changed after review pin',name)
 old=subprocess.check_output(['git','show',q['base']+':'+name],cwd=R)
 assert hashlib.sha256(old).hexdigest()==row['beforeSHA256']
 if expected:assert row['beforeSHA256']==expected,('Unexpected predecessor',name)
 return old
