import Phaser from "phaser";
import { Plaza, controls } from "../game/Plaza";
import "../style.css";
import { decodeAvatarPreferences } from "../domains/state";
import { Gwanghwamun } from "../review/Gwanghwamun";
import "../review/plaza.css";
import { LivingSeoul } from "../review/LivingSeoul";
import { RefinedTown } from "./Town";
import { setupRefinementUI } from "./ui";
import "./refinement.css";
const plazaReview = location.pathname.endsWith("/plaza-review.html");
const districtReview = location.pathname.endsWith("/district-review.html");
const productionReview = true;
const artReview = plazaReview || districtReview || productionReview;
const overview =
  (districtReview || productionReview) &&
  new URLSearchParams(location.search).has("overview");
const base = import.meta.env.BASE_URL;
try {
  Object.assign(
    controls,
    decodeAvatarPreferences(localStorage.getItem("living-pixel-seoul-v4")),
  );
} catch {
  /* Private storage mode remains playable. */
}
document.querySelector<HTMLDivElement>("#app")!.innerHTML = `
<header><a class="brand" href="${base}"><span class="stamp" aria-hidden="true">✉</span><span>KOREAN ARENA<small>Living Pixel Seoul</small></span></a><span class="edition">CENTRAL PLAZA · V4</span><button id="pause" aria-pressed="false">Tạm dừng</button></header>
<main><div class="intro"><p class="eyebrow">MỘT QUẢNG TRƯỜNG · NHỮNG LÁ THƯ THẤT LẠC</p><h1>Hẹn nhau <em>ở quảng trường.</em></h1><p>Dạo phố, thử trang phục và để lại một lời chào. Bản duyệt hình ảnh — chơi cục bộ.</p></div>
<div class="play-layout"><section class="stage-wrap" aria-label="Central Plaza tương tác"><div class="world-caption"><span>✦ Central Plaza</span><span id="mode-label">Khách lịch sử · Chơi cục bộ</span></div><div id="stage"><p id="loading" role="status">Đang mở quảng trường…</p></div><div class="game-bar"><button id="focus">Khám phá</button><span>WASD / ↑↓←→ · Shift chạy · E trò chuyện</span><button id="wave">Chào</button><button id="celebrate">Vui mừng</button><button id="pose">Tạo dáng</button><button id="think">Suy nghĩ</button><button id="interact">Trò chuyện</button></div><div class="touch-pad" aria-label="Điều khiển cảm ứng"><button data-x="0" data-y="-1" aria-label="Đi lên">↑</button><div><button data-x="-1" data-y="0" aria-label="Sang trái">←</button><button data-x="0" data-y="1" aria-label="Đi xuống">↓</button><button data-x="1" data-y="0" aria-label="Sang phải">→</button></div><button id="run" aria-pressed="false">Chạy</button></div></section>
<aside><p class="eyebrow">NGƯỜI GIỮ NHỮNG LÁ THƯ</p><h2>Một phố, một câu chuyện.</h2><p>Trạm thư, Café Dal và nhà văn hóa đang chờ. Gặp Sejong, Jang Yeong-sil, Shin Saimdang và Yi Sun-sin — những vị khách lịch sử trong thế giới hư cấu.</p><label for="hair">Kiểu tóc</label><select id="hair"><option value="0">Tóc mây · Gợn ngắn</option><option value="1">Tóc hạt dẻ · Hai búi</option></select><label for="outfit">Trang phục</label><select id="outfit"><option value="0">Đưa thư · Khăn & quần ngắn</option><option value="1">Học viện · Áo khoác & quần dài</option></select><label for="expression">Biểu cảm</label><select id="expression"><option value="neutral">Thư thái</option><option value="happy">Vui vẻ</option><option value="focused">Tập trung</option><option value="surprised">Ngạc nhiên</option></select><label class="check"><input id="accessory" type="checkbox" checked>Túi thư đeo chéo</label><label for="zoom">Tầm nhìn</label><select id="zoom"><option value="1">1× · Xem khu phố</option><option value="2" selected>2× · Dạo phố</option><option value="3">3× · Xem nhân vật</option></select><button id="night" aria-pressed="false">Ánh chiều dịu</button><label class="check"><input id="motion" type="checkbox">Giảm chuyển động</label><div class="guest-list"><p class="eyebrow">KHÁCH LỊCH SỬ</p><button data-guest="sejong">Sejong · 세종대왕</button><button data-guest="jang">Jang Yeong-sil · 장영실</button><button data-guest="saimdang">Shin Saimdang · 신사임당</button><button data-guest="yi">Yi Sun-sin · 이순신</button></div><p class="note">Các vị khách là hình chiếu giáo dục từ những thời kỳ khác nhau.</p><p class="note">Bản thử hình ảnh và trang phục. Nhiệm vụ The First Delivery, trò học, multiplayer và đấu trường chưa mở.</p><p id="offline" role="status"></p><output id="render-status">Đang tải…</output></aside></div>
<div id="dialog" class="dialog" hidden><p id="dialog-copy" role="status"></p><button id="close-dialog">Đóng lời nhắn</button></div>
<section class="directions"><p class="eyebrow">THE LOST LETTERS</p><h2>Những góc phố để trở về.</h2><p>Một bộ pixel gốc thống nhất: nhà hanok, quán café, vườn cây và quảng trường chung. Các trạm học và đấu trường hiện là địa điểm minh họa, chưa phải tính năng đã mở.</p></section>
<footer>Artwork gốc · Khách lịch sử mô phỏng · Không quảng cáo · Không tài khoản · Gate 2 chờ duyệt</footer></main>`;
const stage = document.querySelector<HTMLDivElement>("#stage")!;
function hasWebGL() {
  try {
    const c = document.createElement("canvas");
    const gl = c.getContext("webgl2") || c.getContext("webgl");
    if (gl) {
      gl.getExtension("WEBGL_lose_context")?.loseContext();
      return true;
    }
  } catch {
    /* Use Canvas. */
  }
  return false;
}
const game = new Phaser.Game({
  type:
    new URLSearchParams(location.search).get("renderer") === "canvas" ||
    !hasWebGL()
      ? Phaser.CANVAS
      : Phaser.AUTO,
  parent: stage,
  width: Math.min(overview ? 1152 : 1024, stage.clientWidth),
  height: Math.min(
    productionReview && overview ? 960 : artReview ? 768 : 640,
    stage.clientHeight,
  ),
  backgroundColor: "#79935f",
  pixelArt: true,
  roundPixels: true,
  antialias: false,
  antialiasGL: false,
  physics: { default: "arcade", arcade: { debug: false } },
  scene: productionReview
    ? [new RefinedTown(), new RefinedTown(true)]
    : districtReview
      ? [new LivingSeoul(), new LivingSeoul(true)]
      : [plazaReview ? new Gwanghwamun() : new Plaza()],
  audio: { noAudio: true },
  banner: false,
});
const observer = new ResizeObserver(() =>
  game.scale.resize(
    Math.min(overview ? 1152 : 1024, stage.clientWidth),
    Math.min(
      productionReview && overview ? 960 : artReview ? 768 : 640,
      stage.clientHeight,
    ),
  ),
);
observer.observe(stage);
const scene = () =>
  (districtReview || productionReview
    ? game.scene.getScenes(true)[0]
    : game.scene.getScene("plaza")) as Plaza;
for (const b of document.querySelectorAll<HTMLButtonElement>("[data-guest]"))
  b.onclick = () => scene().interactGuest(b.dataset.guest!);
document
  .querySelector("#focus")!
  .addEventListener("click", () => game.canvas.focus());
for (const action of ["wave", "celebrate", "pose", "think"] as const)
  document
    .querySelector(`#${action}`)!
    .addEventListener("click", () => scene().emote(action));
document
  .querySelector("#interact")!
  .addEventListener("click", () => scene().interact());
document.querySelector("#pause")!.addEventListener("click", (e) => {
  controls.paused = !controls.paused;
  const b = e.currentTarget as HTMLButtonElement;
  b.textContent = controls.paused ? "Tiếp tục" : "Tạm dừng";
  b.setAttribute("aria-pressed", String(controls.paused));
});
document.querySelector("#night")!.addEventListener("click", (e) => {
  controls.night = !controls.night;
  const b = e.currentTarget as HTMLButtonElement;
  b.setAttribute("aria-pressed", String(controls.night));
  b.textContent = controls.night ? "Trở về ban ngày" : "Ánh chiều dịu";
});
document.querySelector("#zoom")!.addEventListener("change", (e) => {
  controls.zoom = Number((e.target as HTMLSelectElement).value);
});
function save() {
  try {
    localStorage.setItem(
      "living-pixel-seoul-v4",
      JSON.stringify({
        hair: controls.hair,
        outfit: controls.outfit,
        accessory: controls.accessory,
      }),
    );
  } catch {
    /* session only */
  }
}
for (const key of ["hair", "outfit"] as const) {
  const select = document.querySelector<HTMLSelectElement>(`#${key}`)!;
  select.value = String(controls[key]);
  select.onchange = () => {
    controls[key] = Number(select.value) === 1 ? 1 : 0;
    save();
  };
}
document.querySelector<HTMLSelectElement>("#expression")!.onchange = (e) => {
  const value = (e.target as HTMLSelectElement).value;
  if (["neutral", "happy", "focused", "surprised"].includes(value))
    controls.expression = value;
};
const accessory = document.querySelector<HTMLInputElement>("#accessory")!;
accessory.checked = controls.accessory;
accessory.onchange = () => {
  controls.accessory = accessory.checked;
  save();
};
const reduced = document.querySelector<HTMLInputElement>("#motion")!;
reduced.checked = controls.reduced;
reduced.onchange = () => {
  controls.reduced = reduced.checked;
};
matchMedia("(prefers-reduced-motion: reduce)").addEventListener(
  "change",
  (e) => {
    controls.reduced = e.matches;
    reduced.checked = e.matches;
  },
);
for (const b of document.querySelectorAll<HTMLButtonElement>("[data-x]")) {
  b.onpointerdown = (e) => {
    e.preventDefault();
    b.setPointerCapture(e.pointerId);
    controls.x = Number(b.dataset.x);
    controls.y = Number(b.dataset.y);
  };
  const stop = () => {
    controls.x = 0;
    controls.y = 0;
  };
  b.onpointerup = stop;
  b.onpointercancel = stop;
  b.onlostpointercapture = stop;
}
document.querySelector("#run")!.addEventListener("click", (e) => {
  controls.run = !controls.run;
  (e.currentTarget as HTMLButtonElement).setAttribute(
    "aria-pressed",
    String(controls.run),
  );
});
window.addEventListener("town-dialog", (e) => {
  document.querySelector("#dialog-copy")!.textContent = (
    e as CustomEvent<string>
  ).detail;
  document.querySelector<HTMLDivElement>("#dialog")!.hidden = false;
});
document.querySelector("#close-dialog")!.addEventListener("click", () => {
  document.querySelector<HTMLDivElement>("#dialog")!.hidden = true;
  game.canvas.focus();
});
window.addEventListener("game-ready", () => {
  document.querySelector("#loading")?.remove();
  document.querySelector("#render-status")!.textContent =
    "Một Central Plaza · Hình ảnh chờ duyệt";
});
window.addEventListener("game-error", (e) => {
  document.querySelector("#render-status")!.textContent = (
    e as CustomEvent<string>
  ).detail;
});
function network() {
  document.querySelector("#offline")!.textContent = navigator.onLine
    ? ""
    : "Đang offline · Bản đã tải vẫn chơi được; tải mới cần HTTP.";
}
window.addEventListener("online", network);
window.addEventListener("offline", network);
network();
if (artReview) {
  document.body.classList.add("plaza-review");
  controls.zoom = 1;
  document.querySelector<HTMLSelectElement>("#zoom")!.value = "1";
  document.querySelector(".edition")!.textContent = "GWANGHWAMUN · ART REVIEW";
  document.querySelector(".intro h1")!.textContent = "Dưới tán bạch quả.";
  document.querySelector(".intro .eyebrow")!.textContent =
    "B — GINKGO COMMONS · ĐỀ XUẤT, CHƯA DUYỆT";
  document.querySelector(".intro > p:last-child")!.textContent =
    "Juni đi bộ, chạy và chào bằng khung hình thật · WASD, Shift, E hoặc cảm ứng.";
  document.querySelector(".world-caption span")!.textContent =
    "광화문 · Gwanghwamun Plaza";
  document.querySelector("#mode-label")!.textContent =
    "Phaser · Chơi cục bộ · Chờ duyệt";
  document.querySelector("aside > h2")!.textContent = "Juni & Ginkgo Commons";
  document.querySelector("aside > p:not(.eyebrow)")!.textContent =
    "Cổng hai tầng, tượng Sejong, đình đọc sách, nhà trà và rãnh nước trong một quảng trường. Nhấn E gần địa điểm hoặc chạm props để xem ghi chú.";
  for (const id of ["hair", "outfit", "expression", "accessory", "think"]) {
    const el = document.getElementById(id) as
      HTMLButtonElement | HTMLSelectElement | HTMLInputElement;
    el.disabled = true;
    el.title =
      "Giữ nguyên thiết kế Juni đã chọn; chưa tạo kiểu tóc/trang phục hoặc clip suy nghĩ riêng.";
  }
  document.querySelector("#pose")!.textContent = "Biểu cảm";
  document.querySelector(".guest-list")!.setAttribute("hidden", "");
  document
    .querySelectorAll("aside .note")
    .forEach(
      (n) =>
        (n.textContent =
          "Juni được chọn tạm thời. A/Bori và C/Nari vẫn được giữ làm avatar tương lai. Hoạt ảnh Juni và bố cục mới đang chờ bạn duyệt; chưa tạo NPC mới."),
    );
  document.querySelector(".directions h2")!.textContent =
    "Một khu duy nhất để duyệt.";
  document.querySelector(".directions > p:last-child")!.textContent =
    "Đây là bản thử nghệ thuật đề xuất B. Khu phố cũ được giữ nguyên trong liên kết thương hiệu đầu trang. Bukchon, Cheonggyecheon và Namsan chưa được xây. Chưa xuất bản công khai.";
  const gallery = document.createElement("section");
  gallery.className = "plaza-concepts";
  gallery.innerHTML = `<h2>Ba hướng quảng trường</h2><p>Ảnh dưới là concept nguồn, không phải screenshot gameplay. Bản chơi Phaser phía trên là hướng B.</p><div>${[
    ["A", "Royal Stone Promenade", "Trục nghi lễ · Đá granite · Trang trọng"],
    [
      "B",
      "Ginkgo Commons",
      "Đề xuất · Sân đọc sách · Cây bạch quả & rãnh nước",
    ],
    [
      "C",
      "Hanji Lantern Court",
      "Sân lễ hội · Nhà sân khấu · Ánh hanji buổi tối",
    ],
  ]
    .map(
      ([id, name, description]) =>
        `<figure><img src="${base}review/gwanghwamun/concepts/${id}.png" alt="Concept ${id}: ${name}"><figcaption><strong>${id} — ${name}</strong><br>${description}</figcaption></figure>`,
    )
    .join("")}</div>`;
  document.querySelector("footer")!.before(gallery);
}

setupRefinementUI(overview);
