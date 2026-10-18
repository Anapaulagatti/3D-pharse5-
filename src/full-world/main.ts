import Phaser from "phaser";
import { FullWorld } from "./World";
import { setupFullUI } from "./ui";
import "./style.css";
const base = import.meta.env.BASE_URL;
document.querySelector<HTMLDivElement>("#app")!.innerHTML = `
<header><a href="${base}" class="brand">KOREAN ARENA <small>NHỮNG CON ĐƯỜNG HÀN QUỐC</small></a><span id="district-location">Quảng trường cung điện</span><button id="pause" aria-pressed="false">Tạm dừng</button><button id="settings-open" aria-label="Mở cài đặt">☰</button></header>
<main><div id="stage" aria-label="Thế giới Korean Arena"><p id="loading">Đang mở hành trình…</p></div>
<button id="mini-wrap" aria-label="Mở bản đồ hành trình"><img id="mini-map" src="${base}review/full-world/world/minimap.png" alt="Bản đồ khu di sản"><span id="map-player"></span></button>
<div class="hint" id="quest-progress">WASD / ↑↓←→ · Shift chạy · E khám phá</div>
<div class="touch-controls" aria-label="Điều khiển cảm ứng"><div id="joystick" role="group" aria-label="Cần di chuyển"><span class="stick-mark north">N</span><span class="stick-knob"></span></div><div class="action-cluster"><button id="interact" aria-label="Khám phá">Khám phá</button><button id="talk" aria-label="Trò chuyện hoặc xác nhận">Nói chuyện</button><button id="run" aria-label="Giữ để chạy" aria-pressed="false">Chạy</button><button id="emote" aria-label="Biểu cảm" aria-expanded="false">Biểu cảm</button><div id="emote-menu" hidden><button id="wave">Chào</button><button id="celebrate">Vui</button></div></div></div>
<aside id="settings" hidden aria-label="Cài đặt"><h2>Hành trình của bạn</h2><p>Thế giới du lịch giáo dục hư cấu. Các điểm đến ngoài đời nằm ở những vùng khác nhau của Hàn Quốc.</p><label>Tầm nhìn <select id="zoom"><option value="0.5">Toàn cảnh</option><option value="1">1× · Dạo phố</option><option value="2">2× · Chi tiết</option></select></label><label>Nút cảm ứng <select id="control-size"><option value="56">Vừa</option><option value="68">Lớn</option></select></label><label><input type="checkbox" id="motion"> Giảm chuyển động</label><button id="night" aria-pressed="false">Ánh chiều</button><button id="fullscreen">Toàn màn hình ngang</button><a href="?renderer=canvas">Chế độ tương thích Canvas</a><p id="orientation-status" role="status"></p><p id="storage-status" role="status"></p><p id="render-status" role="status"></p><button id="settings-close">Trở lại</button></aside>
<div id="dialog" role="dialog" aria-label="Khám phá Hàn Quốc" hidden><div id="dialog-copy"></div><button id="close-dialog">Đóng lời nhắn</button></div>
<div id="travel-veil" role="status" hidden></div><div id="rotate-screen" hidden><span class="rotate-symbol" aria-hidden="true">▯ ↻ ▭</span><h1>Xoay ngang, mở hành trình.</h1><p>Korean Arena được thiết kế để dạo phố theo chiều ngang.</p><button id="enter-landscape">Bắt đầu ở chế độ ngang</button><p id="rotate-note" role="status">Nếu trình duyệt không tự xoay, hãy xoay thiết bị và tắt khóa xoay màn hình.</p></div>
</main>`;
const stage = document.querySelector<HTMLDivElement>("#stage")!;
const overview = new URLSearchParams(location.search).has("overview");
function webgl(): "none" | "software" | "hardware" {
  try {
    const c = document.createElement("canvas"),
      gl = c.getContext("webgl2") || c.getContext("webgl");
    if (gl) {
      const ext = gl.getExtension("WEBGL_debug_renderer_info");
      const renderer = ext
        ? String(gl.getParameter(ext.UNMASKED_RENDERER_WEBGL))
        : "unknown";
      const software = /swiftshader|llvmpipe|software rasterizer/i.test(
        renderer,
      );
      gl.getExtension("WEBGL_lose_context")?.loseContext();
      return software ? "software" : "hardware";
    }
  } catch {
    /* Canvas remains available. */
  }
  return "none";
}
function size() {
  return {
    width: Math.min(
      overview ? 4352 : 1024,
      Math.max(320, Math.floor(stage.clientWidth)),
    ),
    height: Math.min(
      overview ? 4800 : 768,
      Math.max(180, Math.floor(stage.clientHeight)),
    ),
  };
}
if (overview) document.body.classList.add("overview");
const requested = new URLSearchParams(location.search).get("renderer");
const capability = webgl();
const useCanvas =
  requested === "canvas" ||
  (requested !== "webgl" && capability !== "hardware");
const game = new Phaser.Game({
  type: useCanvas ? Phaser.CANVAS : Phaser.AUTO,
  parent: stage,
  ...size(),
  backgroundColor: "#79935f",
  pixelArt: true,
  roundPixels: true,
  antialias: false,
  antialiasGL: false,
  physics: { default: "arcade", arcade: { debug: false } },
  scene: [new FullWorld(), new FullWorld(true)],
  input: { windowEvents: false, activePointers: 4 },
  audio: { noAudio: true },
  banner: false,
});
new ResizeObserver(() => {
  const s = size();
  game.scale.resize(s.width, s.height);
}).observe(stage);
setupFullUI(game);
document.body.dataset.renderer = useCanvas ? "canvas" : "webgl";
document.body.dataset.fallback =
  capability === "software" ? "software-gpu" : "none";
