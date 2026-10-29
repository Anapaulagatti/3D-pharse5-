"""Fail before fetching compiled art unless a complete explicit owner receipt exists."""
from pathlib import Path
import sys,json,re,os
p=sys.argv[1]
if not re.fullmatch(r'(review-candidates|approved-releases)(/[A-Za-z0-9_.-]+)+\.json',p):raise SystemExit('Invalid receipt path')
q=json.loads(Path(p).read_text());errors=[]
if q.get('decision')!='APPROVED_PUBLIC_PREVIEW':errors.append('Owner public exposure approval PENDING; no asset checkout/upload/deployment allowed')
if not q.get('approvedBy')or not q.get('approvedAt'):errors.append('Named dated owner decision required')
if not re.fullmatch('[0-9a-f]{40}',q.get('artifactCommit','')):errors.append('Pinned compiled-artifact commit required')
if not re.fullmatch('[0-9a-f]{64}',q.get('manifestSHA256','')):errors.append('Exact export manifest checksum required')
if q.get('sourceCommit')!=json.loads(Path('review-source.json').read_text())['portalCommit']:errors.append('Source checkpoint does not match reviewed configuration')
reviews=q.get('npcReviews',{})
if len(reviews)!=26:errors.append('All26 NPC review records required')
for id,r in reviews.items():
 if r.get('decision')!='ALLOW_PUBLIC_PREVIEW'or r.get('unresolvedSpecificConcern')is not False or not r.get('depictionReview')or not r.get('exposureJustification'):errors.append(id+': individual review still pending')
for group in ['world','playable-characters','cosmetics','third-party-code-fonts-audio','checkpoint-media','portal-and-metadata']:
 g=q.get('groups',{}).get(group,{})
 if g.get('decision')!='ALLOW_PUBLIC_PREVIEW'or not g.get('justification'):errors.append(group+': exposure decision pending')
if not q.get('snapshotManifests'):errors.append('Snapshot retention record required')
if errors:raise SystemExit('BLOCKED BEFORE ART FETCH\n'+'\n'.join(errors))
if os.environ.get('GITHUB_OUTPUT'):
 with open(os.environ['GITHUB_OUTPUT'],'a')as f:f.write('artifact='+q['artifactCommit']+'\n')
print('Owner receipt structurally complete; not a legal clearance. Exact site gate and protected environment review still required.')
