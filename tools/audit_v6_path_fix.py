"""Read-only static delivery audit for the fixed V6 review package."""
from pathlib import Path
import json, hashlib, re

R = Path(__file__).resolve().parents[1]
D = R / 'docs/v6-path-fix'
package = json.loads((D/'package.json').read_text())
assert package['status'] == 'VERIFIED_EXACT_ZIP_OVER_HTTP'
patterns = [r'-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----',r'\bAKIA[A-Z0-9]{16}\b',r'\bgh[pousr]_[A-Za-z0-9]{20,}\b',r'\bgithub_pat_[A-Za-z0-9_]{40,}\b',r'\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{32,}\b',r'\bsk_live_[A-Za-z0-9]{20,}\b',r'\bAIza[A-Za-z0-9_-]{35}\b']
findings = []
texts = 0
for row in package['files']:
    p = R/'dist'/row['path']
    assert hashlib.sha256(p.read_bytes()).hexdigest() == row['sha256']
    assert p.suffix in {'.html','.js','.css','.png','.json','.svg','.txt'}
    assert not any(x in {'.git','.env','node_modules','assets-src','generated_images'} for x in Path(row['path']).parts)
    if p.suffix != '.png':
        texts += 1
        for index,pattern in enumerate(patterns):
            if re.search(pattern,p.read_text()):
                findings.append({'file':row['path'],'ruleIndex':index})
notices = [r['path'] for r in package['files'] if 'license' in r['path'].lower() or 'notice' in r['path'].lower()]
assert notices
ci = (R/'.github/workflows/pixel-ci.yml').read_text()
assert 'contents: read' in ci and 'deploy-pages' not in ci
result = {'status':'PASS' if not findings else 'FAIL','distFilesHashed':len(package['files']),'textFilesScanned':texts,'credentialPatternFindings':findings,'noticesRetained':notices,'sourceOrPrivateFilesIncluded':False,'newMediaGenerationCalls':0,'paidProviderCalls':0,'publication':'Source review checkpoint only; no main merge or website deployment.','limits':['Credential pattern scan is not an exhaustive certification.','Physical Android/iOS/Safari and hardware GPU not measured.']}
(D/'quality/release-audit.json').write_text(json.dumps(result,indent=2)+'\n')
assert not findings
print(json.dumps(result))
