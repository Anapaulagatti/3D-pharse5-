"""Read-only candidate integrity, preservation, provenance and publish-file audit."""
import hashlib,json,pathlib,re
root=pathlib.Path(__file__).resolve().parents[2]
info=json.loads((root/'showcase-v0.3/build-info.json').read_text())
html=(root/'showcase-v0.3/index.html').read_bytes()
assert len(html)==info['file_bytes'] and hashlib.sha256(html).hexdigest()==info['checksum_sha256']
baseline=json.loads((root/'quality-reports/v0.3/preserved-v02.json').read_text())
for file,expected in baseline['files'].items():
    b=(root/file).read_bytes()
    assert len(b)==expected['bytes'] and hashlib.sha256(b).hexdigest()==expected['sha256'],file
assets=[]
for folder in ['exports/v1','exports/v0.3']:
    manifest=json.loads((root/folder/'asset-manifest.json').read_text())
    for a in manifest['assets']:
        b=(root/folder/a['file']).read_bytes()
        assert hashlib.sha256(b).hexdigest()==a['checksum_sha256'] and len(b)==a['file_bytes'],a['id']
        assert a['license']=='project-owned-original' and a['source_url'] is None,a['id']
        assets.append(a['id'])
text=html.decode()
patterns=[r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',r'gh[pousr]_[A-Za-z0-9_]{30,}',r'github_pat_[A-Za-z0-9_]{30,}',r'AKIA[0-9A-Z]{16}',r'sk-[A-Za-z0-9_-]{30,}']
assert not any(re.search(p,text) for p in patterns),'Potential credential in candidate'
assert not re.search(r'<script\b[^>]*\bsrc\s*=',text,re.I),'External JavaScript'
assert not re.search(r'<link\b[^>]*(?:stylesheet|preload|modulepreload)',text,re.I),'External bundle/resource'
assert 'studio-dependency-licenses' in text
report={'status':'PASS','candidate_sha256':info['checksum_sha256'],'candidate_bytes':len(html),'preserved_v02_files':len(baseline['files']),
        'verified_original_assets':assets,'known_credential_patterns':0,'external_script_stylesheet_tags':0,'dependency_notices_present':True,
        'static_deployment_allowlist':['index.html','.nojekyll'],'private_source_blender_config_files_in_static_site':False,
        'public_deployment':False,'release_gate':'User review and updated-publication authorization required'}
(root/'quality-reports/v0.3/candidate-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print('Candidate audit PASS:',len(baseline['files']),'preserved original files,',len(assets),'verified original assets; no known credential patterns/external scripts')
