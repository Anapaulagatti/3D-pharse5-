"""Read-only candidate integrity, preservation, provenance and publish-file audit."""
import hashlib,json,pathlib,re,zipfile
root=pathlib.Path(__file__).resolve().parents[2]
info=json.loads((root/'showcase-v0.4/build-info.json').read_text())
html=(root/'showcase-v0.4/index.html').read_bytes()
assert len(html)==info['file_bytes'] and hashlib.sha256(html).hexdigest()==info['checksum_sha256']
baseline=json.loads((root/'quality-reports/v0.4/preserved-v03.json').read_text())
approval_path=root/'quality-reports/v0.4/pages-release/authorization.json'
approval=json.loads(approval_path.read_text()) if approval_path.exists() else {}
deployment_changes=approval.get('deployment_file_updates',{})
assert set(deployment_changes).issubset({'.github/workflows/showcase-pages.yml','Studio/scripts/prepare-pages-site.py'})
authorized_changes=[]
for file,expected in baseline['files'].items():
    b=(root/file).read_bytes()
    if file in deployment_changes:
        change=deployment_changes[file]
        assert approval['approved_html_sha256']==info['checksum_sha256']
        assert change['before_sha256']==expected['sha256'] and change['after_sha256']==hashlib.sha256(b).hexdigest(),file
        authorized_changes.append(file)
        continue
    assert len(b)==expected['bytes'] and hashlib.sha256(b).hexdigest()==expected['sha256'],file
assets=[]
for folder in ['exports/v1','exports/v0.3','exports/v0.4']:
    manifest=json.loads((root/folder/'asset-manifest.json').read_text())
    for a in manifest['assets']:
        b=(root/folder/a['file']).read_bytes()
        assert hashlib.sha256(b).hexdigest()==a['checksum_sha256'] and len(b)==a['file_bytes'],a['id']
        assert a['license']=='project-owned-original' and a['source_url'] is None,a['id']
        if a.get('source_checksum_sha256'):
            assert hashlib.sha256((root/folder/a['source_file']).read_bytes()).hexdigest()==a['source_checksum_sha256'],a['id']
        assets.append(a['id'])
text=html.decode()
patterns=[r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',r'gh[pousr]_[A-Za-z0-9_]{30,}',r'github_pat_[A-Za-z0-9_]{30,}',r'AKIA[0-9A-Z]{16}',r'sk-[A-Za-z0-9_-]{30,}']
assert not any(re.search(p,text) for p in patterns),'Potential credential in candidate'
assert not re.search(r'<script\b[^>]*\bsrc\s*=',text,re.I),'External JavaScript'
assert not re.search(r'<link\b[^>]*(?:stylesheet|preload|modulepreload)',text,re.I),'External bundle/resource'
assert 'studio-dependency-licenses' in text
static=root/'downloads/v0.4/living-hanok-v0.4-static.zip'
if static.exists():
    with zipfile.ZipFile(static) as archive:
        assert set(archive.namelist())=={'index.html','.nojekyll'},'Unexpected static-site files'
        assert archive.read('index.html')==html,'Static ZIP does not match latest candidate; repackage first'
        assert archive.read('.nojekyll')==b''
report={'status':'PASS','candidate_sha256':info['checksum_sha256'],'candidate_bytes':len(html),'preserved_v03_files':len(baseline['files'])-len(authorized_changes),
        'authorized_deployment_file_changes':authorized_changes,
        'verified_original_assets':assets,'known_credential_patterns':0,'external_script_stylesheet_tags':0,'dependency_notices_present':True,
        'static_deployment_allowlist':['index.html','.nojekyll'],'private_source_blender_config_files_in_static_site':False,
        'public_deployment':False,'scope':'Static artifact audit; does not prove public deployment',
        'publication_authorized':bool(authorized_changes),'release_gate':'Publication explicitly authorized' if authorized_changes else 'User review and updated-publication authorization required'}
(root/'quality-reports/v0.4/candidate-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print('v0.4 candidate audit PASS:',report['preserved_v03_files'],'unchanged baseline files,',len(authorized_changes),'authorized deployment updates,',len(assets),'verified original assets; no known credential patterns/external scripts')
