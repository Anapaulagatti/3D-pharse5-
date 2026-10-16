import { controls } from "../game/Plaza";
import {
  letterLesson,
  parseAcademyProgress,
  progressKey,
} from "../domains/academy";
import "./district.css";

export function setupDistrictUI(overview: boolean, production = false) {
  document.body.classList.add("district-review");
  if (overview) document.body.classList.add("district-overview");
  document.querySelector(".edition")!.textContent =
    "LIVING SEOUL · FIRST SLICE";
  document.querySelector(".intro h1")!.textContent =
    "Theo ngõ sách, đến Học viện.";
  document.querySelector(".intro .eyebrow")!.textContent =
    "GWANGHWAMUN → NGÕ SÁCH → HỌC VIỆN HANGUL";
  document.querySelector(".intro > p:last-child")!.textContent =
    "Một hành trình liền mạch cùng Juni. Qua cầu, rẽ về đông; E ở bậc cửa để mở phòng đọc.";
  document.querySelector("aside > h2")!.textContent = "Đường đến những con chữ";
  document.querySelector("aside > p:not(.eyebrow)")!.textContent =
    "Theo đường ngõ sách phía đông quảng trường. Vào Học viện, đến bàn viết và nhấn E để ghép tên chữ Hangul. Vườn đọc và quầy sách nằm bên cạnh.";
  document.querySelector("#interact")!.textContent = "Khám phá · E";
  document.querySelector("#think")!.setAttribute("hidden", "");
  document.querySelector(".game-bar span")!.textContent =
    "WASD / mũi tên · Shift chạy · E khám phá / vào / ra";
  document.querySelector(".world-caption span")!.textContent =
    "광화문 → 한글 배움터";
  document.querySelector(".plaza-concepts")?.remove();
  document.querySelector(".directions h2")!.textContent =
    "Phần mở rộng đầu tiên để duyệt.";
  document.querySelector(".directions > p:last-child")!.textContent =
    "Giữ nguyên quảng trường và Juni; nối thêm ngõ sách, sân Học viện và phòng đọc. Bốn khách lịch sử, workshop, art hanok, bảo tàng và khu chợ mới ở quy hoạch. Chưa xuất bản công khai.";
  const notes = document.querySelectorAll("aside .note");
  if (notes[0])
    notes[0].textContent =
      "Juni, Bori và Nari được giữ nguyên. Các vị khách lịch sử mới chưa sản xuất trong vòng duyệt không gian này.";
  if (notes[1])
    notes[1].textContent =
      "Bài đầu giới thiệu tên chữ, chưa dạy mọi cách phát âm. Tiến độ lưu trên thiết bị; không tài khoản, quảng cáo hay kết nối máy chủ.";
  // Hide irrelevant disabled customization controls only on this new review page.
  for (const id of ["hair", "outfit", "expression", "accessory"]) {
    const el = document.getElementById(id)!;
    el.closest("label")?.setAttribute("hidden", "");
    document.querySelector(`label[for="${id}"]`)?.setAttribute("hidden", "");
    el.setAttribute("hidden", "");
  }
  const navigation = document.createElement("section");
  navigation.className = "district-navigation";
  navigation.innerHTML =
    '<h3>Bản đồ khu đang mở</h3><svg id="district-mini" viewBox="0 0 256 96" role="img" aria-label="Bản đồ: quảng trường bên trái, Học viện phía đông; chấm vàng là Juni"><rect width="256" height="96" fill="#49664f"/><path d="M64 75H78V76H145L164 68H180L192 60H224L240 72" fill="none" stroke="#dec79b" stroke-width="9"/><rect x="40" y="14" width="46" height="30" fill="#293b46"/><rect x="163" y="20" width="58" height="31" fill="#293b46"/><text x="10" y="91" fill="#fff5da" font-size="9">Gwanghwamun</text><text x="166" y="91" fill="#fff5da" font-size="9">Học viện</text><circle id="map-player" r="3" fill="#ffe184" stroke="#253e3a"/></svg><p id="district-location" aria-live="polite">Gwanghwamun Plaza</p><p id="quest-progress">Mục tiêu: khám phá Học viện phía đông.</p><p id="storage-status" role="status"></p>';
  document.querySelector("aside > p:not(.eyebrow)")!.after(navigation);
  document.querySelector("footer")!.textContent =
    "Artwork gốc · First connected slice · Bản duyệt cục bộ · Chưa tạo NPC mới / chưa mở phần còn lại";
  if (production) {
    document.body.classList.add("seoul-production");
    document.querySelector(".edition")!.textContent =
      "LIVING SEOUL · STAGE B REVIEW";
    document.querySelector(".intro h1")!.textContent =
      "Một cánh cổng. Những điều khám phá.";
    document.querySelector(".intro .eyebrow")!.textContent =
      "CỔNG CUNG ĐIỆN · HỌC VIỆN · KHOA HỌC · LỊCH SỬ";
    document.querySelector(".intro > p:last-child")!.textContent =
      "Theo Juni qua quảng trường, sân đọc và phố danh nhân. WASD/mũi tên, Shift chạy, E khám phá.";
    document.querySelector("aside > h2")!.textContent =
      "Hẹn nhau ở Seoul thu nhỏ";
    document.querySelector("aside > p:not(.eyebrow)")!.textContent =
      "Bắc: mở cổng để thăm sân ngoài. Tây: vào phòng đọc Học viện. Đông: xưởng phát minh và hiên bảo tàng. Theo các lối lát đá và đường đất để khám phá.";
    document.querySelector(".world-caption span")!.textContent =
      "광화문 · 배움 · 과학 · 역사";
    document.querySelector(".directions > p:last-child")!.textContent =
      "Phần bắc4096×1728 dùng đúng tọa độ bản quy hoạch4096×3072. Các khu phía nam, suối, cầu và NPC mới chờ duyệt Stage B. Đây là thế giới hư cấu lấy cảm hứng Hàn Quốc, không phải tái dựng lịch sử.";
    document.querySelector("#district-mini")!.outerHTML =
      '<svg id="district-mini" viewBox="0 0 512 216" role="img" aria-label="Khu bắc: học viện phía tây, cổng phía bắc, xưởng và bảo tàng phía đông"><image href="' +
      import.meta.env.BASE_URL +
      'review/seoul-production/minimap.png" width="512" height="216"/><circle id="map-player" r="3" fill="#ffe184" stroke="#253e3a"/></svg>';
    document.querySelector("footer")!.textContent =
      "Artwork gốc · Stage A + first Stage B · Chờ duyệt hình ảnh · Không xuất bản công khai";
    if (notes[0])
      notes[0].textContent =
        "Giữ nguyên Juni144frame. Bori/Nari và bản phố cũ được bảo toàn; chưa tạo NPC mới.";
  }
  let progress = parseAcademyProgress(null);
  try {
    progress = parseAcademyProgress(localStorage.getItem(progressKey));
  } catch {
    document.querySelector("#storage-status")!.textContent =
      "Không truy cập lưu trữ; vẫn học được trong phiên này.";
  }
  const status = () => {
    document.querySelector("#quest-progress")!.textContent =
      progress.mastered.length === 3
        ? "✓ Đã ghép đúng ba tên chữ. Bạn có thể ôn lại tại bàn học."
        : `Bài đầu: ${progress.mastered.length}/3 tên chữ · Vào Học viện, đến bàn viết.`;
  };
  status();
  window.addEventListener("district-position", (e) => {
    const p = (e as CustomEvent).detail;
    document.querySelector("#district-location")!.textContent = p.location;
    document.querySelector("#mode-label")!.textContent = p.location;
    const dot = document.querySelector("#map-player")!;
    dot.setAttribute(
      "cx",
      String(p.area === "room" ? (production ? 84 : 192) : p.x / 8),
    );
    dot.setAttribute("cy", String(p.area === "room" ? 45 : p.y / 8));
    document.querySelector("#render-status")!.textContent =
      `${p.area === "room" ? "Phòng đọc768×576" : production ? "Khu bắc4096×1728" : "Khu ngoài2048×768"} · Phaser · Chơi cục bộ`;
  });
  let lessonOpen = false,
    priorPaused = false,
    index = 0;
  const close = () => {
    if (!lessonOpen) return;
    lessonOpen = false;
    controls.paused = priorPaused;
    document.querySelector<HTMLButtonElement>("#pause")!.disabled = false;
  };
  document.querySelector("#close-dialog")!.addEventListener("click", close);
  const render = () => {
    const copy = document.querySelector("#dialog-copy")!;
    copy.replaceChildren();
    const title = document.createElement("strong");
    title.textContent =
      index < 3 ? `Bàn học Hangul · ${index + 1}/3` : "Hoàn thành bài đầu!";
    copy.append(title);
    if (index === 3) {
      const p = document.createElement("p");
      p.textContent =
        "Bạn đã ghép ㄱ—giyeok, ㄴ—nieun, ㅁ—mieum. Đây là tên chữ; cách đọc trong từ sẽ học ở bước sau. Đóng lời nhắn để trở lại phòng đọc.";
      copy.append(p);
      return;
    }
    const item = letterLesson[index];
    const q = document.createElement("p");
    q.innerHTML = `<span class="hangul-letter">${item.glyph}</span> Chọn tên chữ này:`;
    copy.append(q);
    const feedback = document.createElement("p");
    feedback.setAttribute("role", "status");
    for (const name of ["mieum", "giyeok", "nieun"]) {
      const b = document.createElement("button");
      b.textContent = name;
      b.onclick = () => {
        if (name !== item.name) {
          feedback.textContent = "Chưa đúng. Hãy quan sát nét chữ và thử lại.";
          return;
        }
        progress.mastered = [...new Set([...progress.mastered, item.glyph])];
        try {
          localStorage.setItem(progressKey, JSON.stringify(progress));
        } catch {
          document.querySelector("#storage-status")!.textContent =
            "Lưu trữ không khả dụng; kết quả chỉ giữ trong phiên này.";
        }
        status();
        copy.querySelectorAll("button").forEach((b) => (b.disabled = true));
        feedback.textContent = item.vi;
        const next = document.createElement("button");
        next.textContent = index === 2 ? "Hoàn thành" : "Chữ tiếp theo";
        next.onclick = () => {
          index++;
          render();
        };
        copy.append(next);
      };
      copy.append(b);
    }
    copy.append(feedback);
  };
  window.addEventListener("academy-lesson", () => {
    if (lessonOpen) return;
    lessonOpen = true;
    priorPaused = controls.paused;
    controls.paused = true;
    document.querySelector<HTMLButtonElement>("#pause")!.disabled = true;
    index = 0;
    render();
    document.querySelector<HTMLDivElement>("#dialog")!.hidden = false;
    document.querySelector<HTMLButtonElement>("#dialog-copy button")?.focus();
  });
}
