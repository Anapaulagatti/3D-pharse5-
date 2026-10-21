import Phaser from "phaser";
import { Street } from "./Street";
import { controls } from "../game/Plaza";
import { attachJoystick } from "../engine/Joystick";
import "./street.css";

const root = document.querySelector<HTMLDivElement>("#app")!;
root.innerHTML = `<header><div class="brand">KOREAN ARENA <span>문음길 · Phố Muneum</span></div><button id="pause" aria-pressed="false">Tạm dừng</button></header><main><div id="stage"><p id="loading" role="status">Đang mở phố…</p></div><div id="touch"><div id="joystick" aria-label="Cần di chuyển"><span class="stick-knob"></span></div><div class="actions"><button id="run">Giữ để chạy</button><button id="interact">Khám phá · E</button></div></div><div id="dialog" role="dialog" aria-modal="true" aria-label="Một góc phố" hidden><h2 id="dialog-title"></h2><p id="dialog-copy"></p><button id="close-dialog">Trở lại phố</button></div><div id="portrait" hidden>Xoay ngang để dạo phố.</div></main><footer><span id="near">Dạo theo mặt phố · qua đường để đến sân gặp gỡ</span><span>WASD / ↑↓←→ · Shift chạy · E khám phá · Space chào</span></footer>`;
const stage = document.querySelector<HTMLDivElement>("#stage")!,
  query = new URLSearchParams(location.search);
controls.zoom = 1;
controls.paused = false;
controls.x = 0;
controls.y = 0;
function software() {
  try {
    const gl = document.createElement("canvas").getContext("webgl2");
    if (!gl) return true;
    const ext = gl.getExtension("WEBGL_debug_renderer_info");
    const name = ext
      ? String(gl.getParameter(ext.UNMASKED_RENDERER_WEBGL))
      : "";
    gl.getExtension("WEBGL_lose_context")?.loseContext();
    return /swiftshader|llvmpipe|software/i.test(name);
  } catch {
    return true;
  }
}
const canvas =
  query.get("renderer") === "canvas" ||
  (query.get("renderer") !== "webgl" && software());
function size() {
  return {
    width: Math.min(
      query.has("overview") ? 1536 : 1024,
      Math.max(320, Math.floor(stage.clientWidth)),
    ),
    height: Math.min(
      query.has("overview") ? 1024 : 768,
      Math.max(240, Math.floor(stage.clientHeight)),
    ),
  };
}
const game = new Phaser.Game({
  type: canvas ? Phaser.CANVAS : Phaser.AUTO,
  parent: stage,
  ...size(),
  pixelArt: true,
  roundPixels: true,
  antialias: false,
  backgroundColor: "#56635d",
  physics: { default: "arcade", arcade: { debug: false } },
  scene: [new Street()],
  input: { windowEvents: false, activePointers: 4 },
  audio: { noAudio: true },
  banner: false,
});
new ResizeObserver(() => {
  const s = size();
  game.scale.resize(s.width, s.height);
}).observe(stage);
const scene = () => game.scene.getScene("gate1") as Street,
  dialog = document.querySelector<HTMLDivElement>("#dialog")!;
const touch =
  matchMedia("(pointer:coarse)").matches || navigator.maxTouchPoints > 0;
document.body.dataset.touch = String(touch);
const reset = attachJoystick(
  document.querySelector<HTMLElement>("#joystick")!,
  (x, y) => {
    controls.x = x;
    controls.y = y;
  },
  () => controls.paused,
);
function pause(value: boolean) {
  controls.paused = value;
  if (value) reset();
  const b = document.querySelector<HTMLButtonElement>("#pause")!;
  b.setAttribute("aria-pressed", String(value));
  b.textContent = value ? "Tiếp tục" : "Tạm dừng";
}
document
  .querySelector("#pause")!
  .addEventListener("click", () => pause(!controls.paused));
document
  .querySelector("#interact")!
  .addEventListener("click", () => scene().interact());
const run = document.querySelector<HTMLButtonElement>("#run")!;
run.onpointerdown = (e) => {
  run.setPointerCapture(e.pointerId);
  controls.run = true;
};
run.onpointerup =
  run.onpointercancel =
  run.onlostpointercapture =
    () => {
      controls.run = false;
    };
window.addEventListener("game-ready", () => {
  document.querySelector("#loading")?.remove();
  game.canvas.focus();
});
window.addEventListener("game-error", (e) => {
  const p = document.createElement("p");
  p.textContent = String((e as CustomEvent).detail);
  p.className = "error";
  stage.append(p);
});
window.addEventListener("street-near", (e) => {
  document.querySelector("#near")!.textContent = (
    e as CustomEvent<string>
  ).detail;
});
window.addEventListener("street-dialog", (e) => {
  const data = (e as CustomEvent<{ title: string; text: string }>).detail;
  document.querySelector("#dialog-title")!.textContent = data.title;
  document.querySelector("#dialog-copy")!.textContent = data.text;
  dialog.hidden = false;
  pause(true);
  document.querySelector<HTMLButtonElement>("#close-dialog")!.focus();
});
function close() {
  dialog.hidden = true;
  pause(false);
  game.canvas.focus();
}
document.querySelector("#close-dialog")!.addEventListener("click", close);
window.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && !dialog.hidden) close();
});
function orientation() {
  const portrait = touch && innerHeight > innerWidth;
  document.querySelector<HTMLElement>("#portrait")!.hidden = !portrait;
  if (portrait) pause(true);
}
window.addEventListener("resize", orientation);
orientation();
