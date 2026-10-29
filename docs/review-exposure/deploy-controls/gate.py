"""Exact-artifact exposure gate. Approval JSON is a human review record, not a legal license."""
import argparse,hashlib,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('site');p.add_argument('approval');a=p.parse_args();root=Path(a.site).resolve();approval=json.loads(Path(a.approval).read_text());manifest=root/'export-manifest.json';m=json.loads(manifest.read_text());errors=[]
if approval.get('decision')!='APPROVED_PUBLIC_PREVIEW':errors.append('Explicit owner PREVIEW_PUBLIC_EXPOSURE approval is PENDING')
if not approval.get('approvedBy')or not approval.get('approvedAt'):errors.append('Missing named dated human decision')
if approval.get('sourceCommit')!=json.loads(Path('review-source.json').read_text())['portalCommit']:errors.append('Unreviewed portal source SHA')
if hashlib.sha256(manifest.read_bytes()).hexdigest()!=approval.get('manifestSHA256'):errors.append('Approval does not bind the exact candidate manifest')
if m.get('portalCommit')not in json.loads(Path('review-source.json').read_text())['acceptedBuildSourceCommits']:errors.append('Unreviewed build source lineage')
actual={str(f.relative_to(root))for f in root.rglob('*')if f.is_file()and f!=manifest and '.git'not in f.parts}
if actual!={r['filename']for r in m['files']}:errors.append('Missing or unmanifested exported files')
for row in m['files']:
 f=root/row['filename']
 if f.is_symlink()or not f.resolve().is_relative_to(root)or not f.is_file()or hashlib.sha256(f.read_bytes()).hexdigest()!=row['sha256']:errors.append('Integrity failure: '+row['filename'])
ids={r.get('npcId')for r in m['files']if r.get('npcId')};reviews=approval.get('npcReviews',{});q=approval
config=json.loads(Path('review-source.json').read_text())
profile=q.get('profile');spec=config.get('releaseProfiles',{}).get(profile)
if not spec or q.get('manifestSHA256')!=spec['manifestSHA256']:errors.append('Unreviewed exact release profile/manifest')
if spec and set(q.get('npcReviews',{}))!=set(spec['npcIds']):errors.append('Exact selected roster review required')
if spec and spec.get('artworkEligibility')!='DOCUMENTED_PUBLIC_DISPLAY_TERMS':errors.append('Trusted profile terms review still PENDING')
t=q.get('creationTermsReview',{})
if t.get('status')!='REVIEWED_APPLICABLE_PUBLIC_DISPLAY'or not t.get('reviewedBy')or not t.get('reviewedAt')or not t.get('evidence')or not t.get('outputRightsSection')or not t.get('applicableService'):errors.append('Account/creation terms still UNKNOWN; no public exposure')

if not spec or ids!=set(spec['npcIds'])or ids!=set(reviews):errors.append('Exact selected NPC review coverage required')
for id in sorted(ids):
 r=reviews.get(id,{})
 if r.get('decision')!='ALLOW_PUBLIC_PREVIEW'or r.get('unresolvedSpecificConcern')is not False or not r.get('depictionReview')or not r.get('exposureJustification'):errors.append(id+': pending individual depiction/exposure decision; exclude a specifically disputed depiction before publication')
groups=approval.get('groups',{})
for group in ['world','playable-characters','cosmetics','third-party-code-fonts-audio','checkpoint-media','portal-and-metadata']:
 if group=='checkpoint-media'and profile=='contemporary20':
  if any(r['filename'].endswith('.mp4')for r in m['files'])or groups.get(group,{}).get('decision')!='NOT_DISTRIBUTED':errors.append('Excluded media unexpectedly distributed or misrepresented')
  continue
 if groups.get(group,{}).get('decision')!='ALLOW_PUBLIC_PREVIEW'or not groups[group].get('justification'):errors.append(group+': exposure review missing')
if errors:raise SystemExit('BLOCKED — NO PUBLIC UPLOAD\n'+'\n'.join(errors))
print('PASS exact-artifact owner exposure record; commercial release remains BLOCKED_PENDING_REVIEW. Environment reviewer must independently verify the record before promotion.')
