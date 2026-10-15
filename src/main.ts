import Phaser from "phaser";
import { Plaza, controls, type ArtStyle } from "./game/Plaza";
import { decodeGuest, Style } from "./domains/state";
import "./style.css";
const guest = decodeGuest(safeRead());
function safeRead() {
  try {
    return localStorage.getItem("hangeul-pixel-premium-reset-v2");
  } catch {
    return null;
  }
}
function save() {
  try {
    localStorage.setItem(
      "hangeul-pixel-premium-reset-v2",
      JSON.stringify(guest),
    );
  } catch {
    /* private mode: session still playable */
  }
}
guest.visits = Math.min(100000, guest.visits + 1);
save();
const base = import.meta.env.BASE_URL;
document.querySelector<HTMLDivElement>("#app")!.innerHTML = `
<header><a class="brand" href="${base}"><span class="stamp" aria-hidden="true">✉</span><span>KOREAN ARENA<small>Hangeul Pixel Town</small></span></a><span class="edition">ART RESET · GATE 2</span><button id="pause" aria-pressed="false">Tạm dừng</button></header>
<main><div class="intro"><p class="eyebrow">BA KHU PHỐ · BA VAI NHÂN VẬT</p><h1>Một nơi bạn muốn <em>ở lại.</em></h1><p>Dạo phố ở tầm nhìn gần, gặp Mira và so sánh ba hướng mỹ thuật mới.</p></div>
<div class="play-layout"><section class="stage-wrap" aria-label="Bản đồ tương tác"><div class="world-caption"><span>✦ Bản duyệt Gate 2 · Reset</span><span id="mode-label">Chơi cục bộ · Không có người chơi online</span></div><div id="stage"><p id="loading" role="status">Đang mở cánh cửa phố…</p></div><div class="game-bar"><button id="focus">Khám phá</button><span>WASD / ↑↓←→ · Shift chạy · E trò chuyện</span><button id="wave">Biểu cảm</button><button id="interact">Trò chuyện</button></div><div class="touch-pad" aria-label="Điều khiển cảm ứng"><button data-x="0" data-y="-1" aria-label="Đi lên">↑</button><div><button data-x="-1" data-y="0" aria-label="Sang trái">←</button><button data-x="0" data-y="1" aria-label="Đi xuống">↓</button><button data-x="1" data-y="0" aria-label="Sang phải">→</button></div></div></section>
<aside><p class="eyebrow">BẢN DUYỆT MỸ THUẬT</p><h2>Những lá thư<br>không còn tên.</h2><p>Mira đang đợi bên bưu điện. Có chuyện gì vừa xảy ra ở thị trấn này?</p><p class="quest-step"><span>01</span>Đến gần Mira và nhấn E.</p><p class="note">Đây là bản thử hình ảnh và điều khiển. Nhiệm vụ học, trang phục và chơi cùng bạn bè sẽ được làm ở các gate sau.</p><label for="direction">Hướng hình ảnh</label><select id="direction"><option value="A">A · Thư quán ven hồ</option><option value="B">B · Quảng trường Ngân Hạnh</option><option value="C">C · Phố xưởng Hanji</option></select><label for="zoom">Zoom pixel nguyên</label><select id="zoom"><option value="1">1× · Toàn cảnh bản đồ</option><option value="2" selected>2× · Tầm chơi nhân vật</option><option value="3">3× · Cận cảnh nhân vật</option></select><button id="night" aria-pressed="false">Ánh chiều dịu</button><label class="check"><input id="motion" type="checkbox">Giảm chuyển động</label><p id="offline" role="status"></p><output id="render-status">Đang tải…</output></aside></div>
<div id="dialog" class="dialog" hidden><p id="dialog-copy" role="status"></p><button id="close-dialog">Đóng lời nhắn</button></div>
<section class="directions"><p class="eyebrow">BA THIẾT KẾ · BA BỐ CỤC RIÊNG</p><h2>Bạn muốn sống ở khu phố nào?</h2><p>Mỗi hướng có kiến trúc, cây, đường đi và nhân vật riêng. Đây là chính asset đang chạy trong Phaser; cả ba đều chờ duyệt.</p><div class="art-grid">${(["A", "B", "C"] as const).map((s, i) => `<article><div class="sheet-scroll"><img src="${base}assets/reset-v2/direction-${s}.png" width="448" height="448" alt="Nguồn pixel hướng ${s}: nhà hanok, cây hoa, quầy hàng và bốn hướng nhân vật"></div><h3>${s} · ${["Moonletter Garden", "Ginkgo Commons", "Hanji Afterhours"][i]}</h3><p>${["Thư quán hanok và người đưa thư áo choàng.", "Học viện seowon, sân đá và học viên đeo kính.", "Phố xưởng lệch tầng, sân khấu và người biểu diễn."][i]}</p><button data-style="${s}">Thử hướng ${s}</button></article>`).join("")}</div></section>
<footer>Pixel gốc · Không quảng cáo · Không thu thập tài khoản · Chưa thay website công khai</footer></main>`;
const stage = document.querySelector<HTMLDivElement>("#stage")!;
let game: Phaser.Game;
let observer: ResizeObserver;
function hasWebGL() {
  try {
    const c = document.createElement("canvas");
    const gl = c.getContext("webgl2") || c.getContext("webgl");
    if (gl) {
      gl.getExtension("WEBGL_lose_context")?.loseContext();
      return true;
    }
    return false;
  } catch {
    return false;
  }
}
function start(style: ArtStyle) {
  window.__PIXEL_METRICS__ = undefined;
  document.querySelector("#render-status")!.textContent = "Đang tải…";
  if (game) {
    observer.disconnect();
    game.destroy(true);
    stage.replaceChildren();
  }
  const renderer =
    new URLSearchParams(location.search).get("renderer") === "canvas" ||
    !hasWebGL()
      ? Phaser.CANVAS
      : Phaser.AUTO;
  game = new Phaser.Game({
    type: renderer,
    parent: stage,
    width: Math.min(1024, stage.clientWidth),
    height: Math.min(640, stage.clientHeight),
    backgroundColor: "#abc291",
    pixelArt: true,
    roundPixels: true,
    antialias: false,
    antialiasGL: false,
    transparent: false,
    physics: { default: "arcade", arcade: { debug: false } },
    scene: [new Plaza(style)],
    audio: { noAudio: true },
    banner: false,
  });
  observer = new ResizeObserver(() =>
    game.scale.resize(
      Math.min(1024, stage.clientWidth),
      Math.min(640, stage.clientHeight),
    ),
  );
  observer.observe(stage);
}
function select(style: ArtStyle) {
  if (style === guest.style) return;
  guest.style = style;
  save();
  (document.querySelector("#direction") as HTMLSelectElement).value = style;
  start(style);
}
document.querySelector<HTMLSelectElement>("#direction")!.value = guest.style;
document
  .querySelector("#direction")!
  .addEventListener("change", (e) =>
    select(Style.parse((e.target as HTMLSelectElement).value)),
  );
for (const b of document.querySelectorAll<HTMLButtonElement>("[data-style]"))
  b.onclick = () => {
    select(Style.parse(b.dataset.style));
    stage.scrollIntoView({
      behavior: controls.reduced ? "instant" : "smooth",
      block: "center",
    });
  };
document
  .querySelector("#focus")!
  .addEventListener("click", () => game.canvas.focus());
document.querySelector("#wave")!.addEventListener("click", () => {
  (game.scene.getScene("plaza") as Plaza).wave();
});
document.querySelector("#interact")!.addEventListener("click", () => {
  (game.scene.getScene("plaza") as Plaza).interact();
});
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
for (const button of document.querySelectorAll<HTMLButtonElement>("[data-x]")) {
  button.onpointerdown = (e) => {
    e.preventDefault();
    button.setPointerCapture(e.pointerId);
    controls.x = Number(button.dataset.x);
    controls.y = Number(button.dataset.y);
  };
  const stop = () => {
    controls.x = 0;
    controls.y = 0;
  };
  button.onpointerup = stop;
  button.onpointercancel = stop;
  button.onlostpointercapture = stop;
}
window.addEventListener("town-dialog", (e) => {
  guest.metMira = true;
  save();
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
    "Camera 2× · Nhân vật 48×64 · Bản mới chưa duyệt";
});
window.addEventListener("game-error", (e) => {
  document.querySelector("#render-status")!.textContent = (
    e as CustomEvent<string>
  ).detail;
});
function network() {
  document.querySelector("#offline")!.textContent = navigator.onLine
    ? ""
    : "Đang offline · Bản đã tải vẫn chơi được. Tải mới cần máy chủ cục bộ.";
}
window.addEventListener("online", network);
window.addEventListener("offline", network);
network();
start(guest.style);
