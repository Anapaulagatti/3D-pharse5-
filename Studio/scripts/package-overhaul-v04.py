"""Package only the separate review candidate; never touches the live v0.3 files."""
import hashlib, json, pathlib, zipfile

root=pathlib.Path(__file__).resolve().parents[2]
candidate=root/'showcase-v0.4'
info=json.loads((candidate/'build-info.json').read_text())
html=(candidate/'index.html').read_bytes()
if info['asset_version']!='0.4.0' or len(html)!=info['file_bytes'] or hashlib.sha256(html).hexdigest()!=info['checksum_sha256']:
    raise SystemExit('Candidate integrity mismatch; build/verify the v0.4 artifact first')
# Reuse the already-tested local launcher, with only the version label changed.
(candidate/'start.py').write_text((root/'showcase/start.py').read_text().replace('v0.2','v0.4'))
(candidate/'START_WINDOWS.cmd').write_bytes((root/'showcase/START_WINDOWS.cmd').read_bytes())
(candidate/'README.md').write_text('''# Korean Arena 3D Studio v0.4 — Living Hanok Showcase\n\nBản ứng viên để bạn duyệt hình ảnh. Website GitHub Pages hiện vẫn là v0.3; v0.4 chưa triển khai công khai.\n\n## Xem tương tác trên máy cá nhân\n\n1. Giải nén toàn bộ ZIP vào một thư mục.\n2. Windows: mở START_WINDOWS.cmd. macOS/Linux: mở Terminal trong thư mục vừa giải nén và chạy `python3 start.py`. Cần Python 3.\n3. Trình duyệt tự mở ứng dụng thật. Giữ cửa sổ server mở trong khi xem; Ctrl+C để dừng. Không cần Node, Blender hoặc mạng.\n\nMở index.html trong ChatGPT/Codex/GitHub có thể chỉ hiện mã nguồn; dùng launcher HTTP ở trên. Launcher chỉ phục vụ thư mục ZIP trên chính máy bạn.\n\n## Điểm cần xem\n\n- Đèn lồng, lá mận, giấy hanji và chuyển động linh vật; mười hai trạng thái rõ ràng.\n- Chạm linh vật để nhảy nhỏ; các nút Đi dạo/Chạy vui/Nhảy lên/Vẫy chào/Ăn mừng chạy một lượt rồi Thả lỏng và trở về Idle; chạm đèn/cây hoặc dùng các nút tương tác.\n- Nắng dịu / Chiều ấm / Đêm đèn. Góc nhìn Mái hanok / Vườn mận / Đài gốm.\n- Kéo xoay và cuộn/pinch zoom. Góc nhìn điện ảnh là tùy chọn, dừng khi bạn kéo xoay.\n- Giảm chuyển động tuân theo hệ điều hành; bạn có thể chủ động đổi checkbox. Tạm dừng giữ yên các chuyển động.\n- Chất lượng Thấp / Vừa / Cao; điện thoại mặc định Thấp. Fallback dùng ảnh 3D gốc khi WebGL không khả dụng.\n\nNguồn v0.2/v0.3 và checkpoint được giữ nguyên; v0.4 có rig chân/tay/tai, 12 animation và biểu cảm mắt/mày/miệng thật xuất trong GLB, cùng layer Hanok phong phú hơn. Không có district mới, tài khoản, backend, âm thanh hoặc dịch vụ trả phí.\n\nThành tích FPS phần cứng/điện thoại thật chưa được đo; kiểm tra cloud dùng SwiftShader. Không có cam kết 60 FPS.\n\n## Release\n\nThe user requested stopping after the completed v0.4 upgrade for review (section 19). This ZIP is the local review candidate; the existing v0.3 site remains unchanged. Public v0.4 publication can follow a separate user request.\n''')
downloads=root/'downloads/v0.4'; downloads.mkdir(parents=True,exist_ok=True)
local=downloads/'living-hanok-v0.4-review.zip'
static=downloads/'living-hanok-v0.4-static.zip'
with zipfile.ZipFile(local,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for name in ['index.html','start.py','START_WINDOWS.cmd','README.md','build-info.json']:
        z.write(candidate/name,'Living-Hanok-v0.4/'+name)
with zipfile.ZipFile(static,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    z.write(candidate/'index.html','index.html');z.writestr('.nojekyll','')
packages=[]
for path in [local,static]:
    b=path.read_bytes();packages.append({'file':str(path.relative_to(root)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
(downloads/'package-manifest.json').write_text(json.dumps({'version':'0.4.0','status':'review-candidate-not-deployed','html_sha256':info['checksum_sha256'],'packages':packages},indent=2)+'\n')
print(json.dumps(packages,indent=2))
