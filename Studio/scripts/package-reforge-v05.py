"""Package exact self-contained v0.5; public static ZIP has only two files."""
from pathlib import Path
import hashlib,json,zipfile,re
root=Path(__file__).resolve().parents[2];d=root/'showcase-v0.5';j=json.loads((d/'build-info.json').read_text());b=(d/'index.html').read_bytes();assert hashlib.sha256(b).hexdigest()==j['checksum_sha256'] and len(b)==j['file_bytes']
text=b.decode();assert 'id="studio-dependency-licenses"' in text
for pattern in [r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',r'AKIA[0-9A-Z]{16}',r'ghp_[A-Za-z0-9]{36}',r'github_pat_[A-Za-z0-9_]{60,}',r'sk-(?:proj-)?[A-Za-z0-9_-]{40,}']:
 assert not re.search(pattern,text),'Credential-like data; inspect locally'
assert not re.search(r'<script\b[^>]*\bsrc=|<link\b[^>]*\brel="stylesheet"|sourceMappingURL=',text,re.I)
(d/'start.py').write_text((root/'showcase/start.py').read_text().replace('v0.2','v0.5'))
(d/'START_WINDOWS.cmd').write_bytes((root/'showcase/START_WINDOWS.cmd').read_bytes())
(d/'README.md').write_text('''# Korean Arena v0.5 — Joseon Fantasy Reforge

Xem ứng dụng 3D thật: giải nén toàn bộ ZIP. Windows mở START_WINDOWS.cmd; macOS/Linux chạy `python3 start.py` trong thư mục giải nén (cần Python3). Giữ cửa sổ server mở. Không cần Node, Blender, dịch vụ, tài khoản hay mạng.

Nếu index.html chỉ hiện mã nguồn trong ChatGPT/GitHub, dùng launcher HTTP trên. HTML tự chứa GLB, PNG, CSS và JavaScript; mở dưới thư mục con cũng được.

Chọn “Chơi thử cùng Nari”, chạm sân để nhận bàn phím. WASD/mũi tên di chuyển; Shift chạy; Space nhảy; E mở cửa khi đến gần. Điện thoại có phím cảm ứng. Kéo xoay, cuộn/pinch để xem gần. Vẫy chào/Ăn mừng chạy một lượt rồi trở về Idle. Chạm đèn hoặc tán hoa mận. Có 5 chế độ xem, 20 animation, 10 biểu cảm, ngày/chiều/đêm và 3 mức chất lượng. Hệ điều hành bật giảm chuyển động thì trang trí đứng yên; điều khiển chủ động vẫn hoạt động. Tạm dừng và Tắt/Ít hiệu ứng được giữ riêng. Mất WebGL chuyển sang ảnh thực v0.5.

Nari và Hanok là tài sản gốc từ Blender; Ceramic Seed Spirit được giữ làm GLB lưu trữ tùy chọn. Không có district mới/backend/audio/paid service. Kiểm tra cloud dùng SwiftShader; chưa đo FPS trên điện thoại/GPU thật và không cam kết 30/60FPS. Đây là bản hoàn tất được kiểm tra trước khi phát hành; trạng thái triển khai chính xác xem quality-reports/v0.5/pages-release/deployment.json trong repo.
''')
out=root/'downloads/v0.5';out.mkdir(parents=True,exist_ok=True);packages=[]
for name,entries in [('joseon-reforge-v0.5-view.zip',['index.html','start.py','START_WINDOWS.cmd','README.md','build-info.json']),('joseon-reforge-v0.5-static.zip',['index.html','.nojekyll'])]:
 path=out/name
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for e in entries:z.write(d/e,('Joseon-Reforge-v0.5/' if 'view.zip' in name else '')+e)
 packages.append({'file':str(path.relative_to(root)),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
(out/'package-manifest.json').write_text(json.dumps({'version':'0.5.0','html_sha256':j['checksum_sha256'],'packages':packages},indent=2)+'\n')
r=root/'quality-reports/v0.5/gate-e/artifact-audit.json';r.write_text(json.dumps({'status':'PASS', 'html_bytes':len(b),'sha256':j['checksum_sha256'],'public_allowlist':['index.html','.nojekyll'],'secret_known_pattern_scan':'PASS','external_bundle_or_sourcemap_scan':'PASS','embedded_assets':j['embedded_assets'],'notes':'Only original project-owned GLB/PNG plus bundled dependency license notices. No source .blend, private files or credentials in public artifact. Known-pattern scan is not a universal secret detector.'},indent=2)+'\n');print(json.dumps(packages,indent=2))
