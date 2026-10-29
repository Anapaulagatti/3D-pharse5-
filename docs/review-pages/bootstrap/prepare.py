"""Stage a public-preview CANDIDATE from the existing portal; never builds game or deploys."""
from pathlib import Path
import argparse,json,hashlib,shutil,re
p=argparse.ArgumentParser();p.add_argument('candidate');p.add_argument('output');a=p.parse_args();S=Path(a.candidate).resolve();O=Path(a.output).resolve();m=json.loads((S/'export-manifest.json').read_text())
if O.exists()or O==S or O.is_relative_to(S):raise SystemExit('Use a separate fresh output directory')
actual={str(f.relative_to(S))for f in S.rglob('*')if f.is_file()and f!=S/'export-manifest.json'}
if actual!={x['filename']for x in m['files']}:raise SystemExit('Unmanifested/missing source files')
for row in m['files']:
 f=S/row['filename']
 if f.is_symlink()or not f.resolve().is_relative_to(S)or hashlib.sha256(f.read_bytes()).hexdigest()!=row['sha256']:raise SystemExit('Source integrity failure')
shutil.copytree(S,O)
# Presentation/deployment wrapper only. Compiled Phaser JS/CSS and every art file remain exact.
for f in O.rglob('*'):
 if not f.is_file():continue
 if f.name=='index.html'and f.parent.name!='play':
  t=f.read_text().replace('PRIVATE DEVELOPMENT REVIEW','DEVELOPMENT REVIEW').replace('Chỉ dùng trong staging có kiểm soát truy cập. Không phải bản phát hành thương mại.','Bản phát triển để đánh giá; không phải bản phát hành thương mại.').replace('PREVIEW_PUBLIC_EXPOSURE: NOT APPROVED.','Cho phép hiển thị công khai cần quyết định riêng của chủ dự án; không đồng nghĩa quyền thương mại.');t=re.sub(r'Chơi bình thường dùng dữ liệu\s+lưu hiện có;', 'Bản Pages review có vùng lưu riêng, không ghi save của site v0.5;',t);t=re.sub(r'Chỉ dùng trong staging có kiểm soát truy cập\.\s+Không phải bản phát hành\s+thương mại\.', 'Bản phát triển để đánh giá; không phải bản phát hành thương mại.',t);f.write_text(t)
 if f.name=='index.html'and f.parent.name=='play':
  f.write_text(f.read_text().replace('<head>','<head><script type="module" src="./pages-saves.mjs"></script>'));(f.parent/'pages-saves.mjs').write_bytes(Path(__file__).with_name('pages-saves.mjs').read_bytes())
 if f.name=='version.json':
  v=json.loads(f.read_text());v['exposure']='PUBLIC_PREVIEW_CANDIDATE';v['publicExposure']='EXPLICIT_OWNER_APPROVAL_REQUIRED_BEFORE_PUBLICATION';v['commercialRelease']='BLOCKED_PENDING_REVIEW';f.write_text(json.dumps(v,indent=2)+'\n')
# Recompute inner manifests first, then exact whole-site manifest (including inner manifests).
for f in sorted(O.rglob('export-manifest.json'),key=lambda p:len(p.parts),reverse=True):
 q=json.loads(f.read_text());root=f.parent
 for shim in root.rglob('pages-saves.mjs'):
  q['files'].append({'filename':str(shim.relative_to(root)),'sha256':hashlib.sha256(shim.read_bytes()).hexdigest(),'bytes':shim.stat().st_size,'origin':'project-authored Pages-only storage isolation wrapper','category':'portal-source','knownTerms':'project-authored tooling; original notices retained','npcId':None,'publicPreviewDecision':'EXPLICIT_OWNER_APPROVAL_REQUIRED','commercialRelease':'BLOCKED_PENDING_REVIEW','risk':'no artwork; startup namespace only','missingEvidence':'owner exposure approval for complete artifact'})
 for row in q['files']:
  asset=root/row['filename'];row['sha256']=hashlib.sha256(asset.read_bytes()).hexdigest();row['bytes']=asset.stat().st_size;row['publicPreviewDecision']='EXPLICIT_OWNER_APPROVAL_REQUIRED'
 q['scope']='PUBLIC PREVIEW CANDIDATE ONLY; exact artifact owner approval required before any upload; no legal clearance';f.write_text(json.dumps(q,indent=2)+'\n')
print('PUBLIC CANDIDATE PREPARED LOCALLY ONLY; NOT APPROVED; NOT DEPLOYED')
print('manifest SHA256:',hashlib.sha256((O/'export-manifest.json').read_bytes()).hexdigest())
