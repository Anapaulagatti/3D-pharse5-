import Phaser from "phaser";
import { KoreaTown } from "./Town";
import { NamsanPark } from "./Park";
import { setupKoreaUI } from "./ui";
import "./style.css";
const base = import.meta.env.BASE_URL;
document.querySelector<HTMLDivElement>("#app")!.innerHTML = `
<header><a href="${base}" class="brand">KOREAN ARENA <small>DI SẢN & NHỮNG CHUYẾN ĐI</small></a><span id="district-location">Quảng trường cung điện</span><button id="pause" aria-pressed="false">Tạm dừng</button><button id="settings-open" aria-label="Mở cài đặt">☰</button></header>
<main><div id="stage" aria-label="Thế giới Korean Arena"><p id="loading">Đang mở hành trình…</p></div>
<div id="mini-wrap"><img id="mini-map" src="${base}review/living-korea/north/minimap.png" alt="Bản đồ khu di sản"><span id="map-player"></span></div>
<div class="hint" id="quest-progress">WASD / ↑↓←→ · Shift chạy · E khám phá</div>
<div class="touch-controls" aria-label="Điều khiển cảm ứng"><div class="dpad"><button data-x="0" data-y="-1" aria-label="Đi lên">↑</button><button data-x="-1" data-y="0" aria-label="Sang trái">←</button><button data-x="1" data-y="0" aria-label="Sang phải">→</button><button data-x="0" data-y="1" aria-label="Đi xuống">↓</button></div><div class="actions"><button id="wave" aria-label="Chào">Chào</button><button id="celebrate" aria-label="Vui mừng">Vui</button><button id="run" aria-pressed="false">Chạy</button><button id="interact">Khám phá · E</button></div></div>
<aside id="settings" hidden aria-label="Cài đặt"><h2>Hành trình của bạn</h2><p>Thế giới du lịch giáo dục hư cấu. Các điểm đến ngoài đời nằm ở những vùng khác nhau của Hàn Quốc.</p><label>Tầm nhìn <select id="zoom"><option value="0.5">Toàn cảnh</option><option value="1">1× · Dạo phố</option><option value="2">2× · Chi tiết</option></select></label><label>Nút cảm ứng <select id="control-size"><option value="56">Vừa</option><option value="68">Lớn</option></select></label><label><input type="checkbox" id="motion"> Giảm chuyển động</label><button id="night" aria-pressed="false">Ánh chiều</button><button id="fullscreen">Toàn màn hình ngang</button><a href="?renderer=canvas">Chế độ tương thích Canvas</a><p id="orientation-status" role="status"></p><p id="storage-status" role="status"></p><p id="render-status" role="status"></p><button id="settings-close">Trở lại</button></aside>
<div id="dialog" role="dialog" aria-label="Khám phá Hàn Quốc" hidden><div id="dialog-copy"></div><button id="close-dialog">Đóng lời nhắn</button></div>
<div id="travel-veil" role="status" hidden></div><div id="rotate-screen" hidden><span class="rotate-symbol" aria-hidden="true">▯ ↻ ▭</span><h1>Xoay ngang, mở hành trình.</h1><p>Korean Arena được thiết kế để dạo phố theo chiều ngang.</p><button id="enter-landscape">Bắt đầu ở chế độ ngang</button><p id="rotate-note" role="status">Nếu trình duyệt không tự xoay, hãy xoay thiết bị và tắt khóa xoay màn hình.</p></div>
</main>`;
const stage = document.querySelector<HTMLDivElement>("#stage")!;
const overview = new URLSearchParams(location.search).has("overview");
function webgl() {
  try {
    const c = document.createElement("canvas"),
      gl = c.getContext("webgl2") || c.getContext("webgl");
    if (gl) {
      gl.getExtension("WEBGL_lose_context")?.loseContext();
      return true;
    }
  } catch {
    /* Canvas remains available. */
  }
  return false;
}
function size() {
  return {
    width: Math.min(
      overview ? 1152 : 1024,
      Math.max(320, Math.floor(stage.clientWidth)),
    ),
    height: Math.min(
      overview ? 1120 : 768,
      Math.max(180, Math.floor(stage.clientHeight)),
    ),
  };
}
const game = new Phaser.Game({
  type:
    new URLSearchParams(location.search).get("renderer") === "canvas" ||
    !webgl()
      ? Phaser.CANVAS
      : Phaser.AUTO,
  parent: stage,
  ...size(),
  backgroundColor: "#79935f",
  pixelArt: true,
  roundPixels: true,
  antialias: false,
  antialiasGL: false,
  physics: { default: "arcade", arcade: { debug: false } },
  scene: [new KoreaTown(), new KoreaTown(true), new NamsanPark()],
  input: { windowEvents: false, activePointers: 4 },
  audio: { noAudio: true },
  banner: false,
});
new ResizeObserver(() => {
  const s = size();
  game.scale.resize(s.width, s.height);
}).observe(stage);
setupKoreaUI(game);
