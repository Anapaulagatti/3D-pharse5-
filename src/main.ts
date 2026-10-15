import Phaser from "phaser";
import { Plaza, controls } from "./game/Plaza";
import "./style.css";
const base = import.meta.env.BASE_URL;
try {
  const saved = JSON.parse(
    localStorage.getItem("living-pixel-seoul-v4") ?? "null",
  );
  if (saved && [0, 1].includes(saved.hair) && [0, 1].includes(saved.outfit)) {
    controls.hair = saved.hair;
    controls.outfit = saved.outfit;
    controls.accessory = saved.accessory !== false;
  }
} catch {
  /* Private mode/corrupt local storage still allows play. */
}
document.querySelector<HTMLDivElement>("#app")!.innerHTML = `
<header><a class="brand" href="${base}"><span class="stamp" aria-hidden="true">✉</span><span>KOREAN ARENA<small>Living Pixel Seoul</small></span></a><span class="edition">CENTRAL PLAZA · V4</span><button id="pause" aria-pressed="false">Tạm dừng</button></header>
<main><div class="intro"><p class="eyebrow">MỘT QUẢNG TRƯỜNG · NHỮNG LÁ THƯ THẤT LẠC</p><h1>Hẹn nhau <em>ở quảng trường.</em></h1><p>Dạo phố, thử trang phục và để lại một lời chào. Bản duyệt hình ảnh — chơi cục bộ.</p></div>
<div class="play-layout"><section class="stage-wrap" aria-label="Central Plaza tương tác"><div class="world-caption"><span>✦ Central Plaza</span><span id="mode-label">NPC demo · Chưa có người chơi online</span></div><div id="stage"><p id="loading" role="status">Đang mở quảng trường…</p></div><div class="game-bar"><button id="focus">Khám phá</button><span>WASD / ↑↓←→ · Shift chạy · E trò chuyện</span><button id="wave">Chào</button><button id="celebrate">Vui mừng</button><button id="pose">Tạo dáng</button><button id="interact">Trò chuyện</button></div><div class="touch-pad" aria-label="Điều khiển cảm ứng"><button data-x="0" data-y="-1" aria-label="Đi lên">↑</button><div><button data-x="-1" data-y="0" aria-label="Sang trái">←</button><button data-x="0" data-y="1" aria-label="Đi xuống">↓</button><button data-x="1" data-y="0" aria-label="Sang phải">→</button></div><button id="run" aria-pressed="false">Chạy</button></div></section>
<aside><p class="eyebrow">NGƯỜI GIỮ NHỮNG LÁ THƯ</p><h2>Một phố, một câu chuyện.</h2><p>Trạm thư, Café Dal và nhà văn hóa đang chờ. Gặp Mira hoặc chạm vào các bảng hiệu để khám phá.</p><label for="hair">Kiểu tóc</label><select id="hair"><option value="0">Tóc gợn ngắn</option><option value="1">Tóc bob buộc</option></select><label for="outfit">Trang phục</label><select id="outfit"><option value="0">Áo người đưa thư</option><option value="1">Áo khoác học viện</option></select><label class="check"><input id="accessory" type="checkbox" checked>Túi thư đeo chéo</label><label for="zoom">Tầm nhìn</label><select id="zoom"><option value="1">1× · Xem khu phố</option><option value="2" selected>2× · Dạo phố</option><option value="3">3× · Xem nhân vật</option></select><button id="night" aria-pressed="false">Ánh chiều dịu</button><label class="check"><input id="motion" type="checkbox">Giảm chuyển động</label><p class="note">Bản thử hình ảnh và trang phục. Nhiệm vụ The First Delivery, trò học, multiplayer và đấu trường chưa mở.</p><p id="offline" role="status"></p><output id="render-status">Đang tải…</output></aside></div>
<div id="dialog" class="dialog" hidden><p id="dialog-copy" role="status"></p><button id="close-dialog">Đóng lời nhắn</button></div>
<section class="directions"><p class="eyebrow">THE LOST LETTERS</p><h2>Những góc phố để trở về.</h2><p>Một bộ pixel gốc thống nhất: nhà hanok, quán café, vườn cây và quảng trường chung. Các trạm học và đấu trường hiện là địa điểm minh họa, chưa phải tính năng đã mở.</p></section>
<footer>Artwork gốc · NPC demo cục bộ · Không quảng cáo · Không tài khoản · Gate 2 chờ duyệt</footer></main>`;
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
  width: Math.min(1024, stage.clientWidth),
  height: Math.min(640, stage.clientHeight),
  backgroundColor: "#79935f",
  pixelArt: true,
  roundPixels: true,
  antialias: false,
  antialiasGL: false,
  physics: { default: "arcade", arcade: { debug: false } },
  scene: [new Plaza()],
  audio: { noAudio: true },
  banner: false,
});
const observer = new ResizeObserver(() =>
  game.scale.resize(
    Math.min(1024, stage.clientWidth),
    Math.min(640, stage.clientHeight),
  ),
);
observer.observe(stage);
const scene = () => game.scene.getScene("plaza") as Plaza;
document
  .querySelector("#focus")!
  .addEventListener("click", () => game.canvas.focus());
for (const action of ["wave", "celebrate", "pose"] as const)
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
