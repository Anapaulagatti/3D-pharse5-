"""Fail-closed exact candidate eligibility. Owner approval cannot turn UNKNOWN into permission."""
from pathlib import Path
import json,hashlib,argparse,re
REQUIRED={'npc-contemporary','world','playable-characters','cosmetics'}
def validate(site,record,evidence_root):
 site=Path(site).resolve();root=Path(evidence_root).resolve();q=json.loads((site/'export-manifest.json').read_text());errors=[]
 if record.get('manifestSHA256')!=hashlib.sha256((site/'export-manifest.json').read_bytes()).hexdigest():errors.append('Exact manifest mismatch')
 if record.get('decision')!='APPROVED_PUBLIC_PREVIEW'or not record.get('approvedBy')or not record.get('approvedAt'):errors.append('Explicit named dated owner exposure decision missing')
 expected=set(q.get('npcIds',[]))or {r['npcId']for r in q['files']if r.get('npcId')}
 if len(expected)not in [20,26]:errors.append('Not a supported exact roster')
 if set(record.get('npcReviews',{}))!=expected:errors.append('Exact included-NPC review coverage missing')
 for id in expected:
  row=record.get('npcReviews',{}).get(id,{})
  if row.get('decision')!='ALLOW_PUBLIC_PREVIEW'or row.get('unresolvedSpecificConcern')is not False:errors.append('Pending or specific unresolved concern: '+id)
 groups=set(REQUIRED)
 if any(id.startswith('npc-history-')for id in expected):groups.add('npc-era')
 terms=record.get('creationTermsReview',{})
 if terms.get('status')!='REVIEWED_APPLICABLE_PUBLIC_DISPLAY':errors.append('UNKNOWN account/creation terms; eligibility not established')
 if set(terms.get('coveredGroups',[]))!=groups:errors.append('Terms evidence does not cover all included art groups')
 if not terms.get('reviewedBy')or not terms.get('reviewedAt')or not terms.get('applicableService')or not terms.get('outputRightsSection'):errors.append('Missing genuine account/terms review')
 refs=terms.get('evidence',[])
 if not refs:errors.append('No creation/account terms evidence documents')
 for ref in refs:
  rel=ref.get('path','');p=(root/rel).resolve()
  if not rel or not p.is_relative_to(root)or not p.is_file()or p.is_symlink():errors.append('Invalid evidence file');continue
  if hashlib.sha256(p.read_bytes()).hexdigest()!=ref.get('sha256'):errors.append('Evidence hash mismatch')
  if not ref.get('applicabilityReason')or not ref.get('supportingSection'):errors.append('No inspected claim-to-terms support')
 listed={r['filename']for r in q['files']};actual={str(p.relative_to(site))for p in site.rglob('*')if p.is_file()and p!=site/'export-manifest.json'and'.git'not in p.parts}
 if listed!=actual:errors.append('Unmanifested/missing public files')
 for r in q['files']:
  p=site/r['filename']
  if p.is_symlink()or not p.resolve().is_relative_to(site)or not p.is_file()or hashlib.sha256(p.read_bytes()).hexdigest()!=r['sha256']:errors.append('Asset integrity: '+r['filename'])
 return errors
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('site');p.add_argument('record');p.add_argument('--evidence-root',default='docs/review-exposure');a=p.parse_args();errors=validate(a.site,json.loads(Path(a.record).read_text()),a.evidence_root)
 if errors:raise SystemExit('BLOCKED — NO PUBLIC UPLOAD\n'+'\n'.join(errors))
 print('PASS recorded eligibility and exact owner exposure scope; not a legal opinion. Protected GitHub environment review still required.')
