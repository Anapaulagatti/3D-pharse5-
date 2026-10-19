"""Read-only release audit. Reports counts/paths, never prints a credential match."""
from pathlib import Path
import json,re,hashlib
R=Path(__file__).resolve().parents[1];D=R/'dist';Q=R/'docs/v6-restructure';j=json.loads((Q/'package.json').read_text());assert j['status']=='VERIFIED_EXACT_ZIP_OVER_HTTP'
allowed={'.html','.js','.css','.png','.json','.svg','.txt'};text_types=allowed-{'.png'};findings=[];texts=0
patterns=[r'-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----',r'\bAKIA[A-Z0-9]{16}\b',r'\bgh[pousr]_[A-Za-z0-9]{20,}\b',r'\bgithub_pat_[A-Za-z0-9_]{40,}\b',r'\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{32,}\b',r'\bsk_live_[A-Za-z0-9]{20,}\b',r'\bAIza[A-Za-z0-9_-]{35}\b']
for row in j['files']:
 p=D/row['path'];assert p.suffix in allowed and hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256']
 assert not any(q in {'.git','.env','node_modules','assets-src','generated_images'}for q in p.relative_to(D).parts)
 if p.suffix in text_types:
  texts+=1;t=p.read_text()
  for i,regex in enumerate(patterns):
   if re.search(regex,t):findings.append({'path':row['path'],'ruleIndex':i})
notices=[r['path']for r in j['files']if 'notice'in r['path'].lower() or 'license'in r['path'].lower()];assert notices
render=json.loads((Q/'quality/renderer-verification.json').read_text());assert render['status']=='PASS' and not render['errors'] and not render.get('externalRequests')
ci='\n'.join(line.split('#',1)[0]for line in (R/'.github/workflows/pixel-ci.yml').read_text().splitlines());assert 'contents: read'in ci and not re.search(r'pages\s*:\s*write',ci) and 'deploy-pages'not in ci
report={'status':'PASS'if not findings else'FAIL','filesHashed':len(j['files']),'textFilesScanned':texts,'credentialPatternFindings':findings,'privateSourcePathsIncluded':False,'authoringOr3DFilesIncluded':False,'retainedNotices':notices,'runtimeExternalRequests':render.get('externalRequests',[]),'workflow':'Existing read-only CI, no Pages deployment job. No main merge/website publication.','artProvenance':'Approved original world/native pixel assets reused; no new provider/host generation and no reference painting baked into runtime. Source provenance and user reference stay outside dist.','limitations':['Pattern scan is not exhaustive secret certification','No V6 media generation/provider request was made','No actual public deployment performed']}
(Q/'quality/release-audit.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));assert not findings
