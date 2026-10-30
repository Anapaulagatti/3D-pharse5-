"""Exact, versioned owner-authorized code/catalog amendments; never a wildcard.
Historical checks still inspect the old baseline; current behavioral checks inspect
these pinned revisions. No original art, source manifest or old checkpoint changes.
"""
from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[2]
def historical_bytes(name,expected=None):
 current=(R/name).read_bytes();manifest=R/'docs/phase3bb-hotfix/AUTHORIZED_AMENDMENTS.json'
 if not manifest.exists():return current
 q=json.loads(manifest.read_text());row=q['files'].get(name)
 if not row:return current
 assert hashlib.sha256(current).hexdigest()==row['afterSHA256'],('Amendment changed after review pin',name)
 old=subprocess.check_output(['git','show',q['base']+':'+name],cwd=R)
 assert hashlib.sha256(old).hexdigest()==row['beforeSHA256']
 if expected:assert row['beforeSHA256']==expected,('Unexpected predecessor',name)
 return old
