import Phaser from "phaser";
import { Plaza, controls } from "../game/Plaza";
import "./characters.css";

type View = "front" | "back" | "left" | "right";
type ReviewMetrics = {
  ready: boolean;
  view: View;
  zoom: number;
  renderer: string;
  canvas: { width: number; height: number };
  candidates: { id: string; frame: string; foot: { x: number; y: number } }[];
  nativeBodyHeight: number;
  staticDesignProof: true;
  userApproval: "PENDING";
};
declare global {
  interface Window {
    __CHARACTER_REVIEW__?: ReviewMetrics;
  }
}
const choices = [
  {
    id: "A",
    name: "Bori",
    title: "Adventure Chibi",
    detail: "Tóc bồng dựng · Mắt hổ phách · Áo thám hiểm & quần ngắn",
  },
  {
    id: "B",
    name: "Juni",
    title: "Social RPG Chibi",
    detail: "Hai búi tóc · Mặt góc cạnh · Bomber, tai nghe & quần ống rộng",
  },
  {
    id: "C",
    name: "Nari",
    title: "Korean Fantasy Chibi",
    detail:
      "Tóc tết lệch · Mắt xanh trầm · Áo giao lĩnh cách điệu & quần xếp ly",
  },
];
const base = import.meta.env.BASE_URL;
document.querySelector("#character-review")!.innerHTML = `
<header><a href="${base}">KOREAN ARENA <span>Living Pixel Seoul</span></a><span>JUNI · PHƯƠNG ÁN CHÍNH TẠM THỜI</span></header>
<main><p class="eyebrow">CHARACTER REBOOT · THREE ORIGINAL DIRECTIONS</p><h1>Ba cá tính. Một thế giới.</h1>
<p class="lead">So sánh thiết kế mới trong chính quảng trường hiện tại. Cùng chiều cao pixel, cùng ánh sáng, cùng điểm đặt chân.</p>
<div class="toolbar"><fieldset><legend>Hướng nhìn</legend>${(
  [
    ["front", "Mặt trước"],
    ["back", "Mặt sau"],
    ["left", "Bên trái"],
    ["right", "Bên phải"],
  ] as const
)
  .map(
    ([id, label]) =>
      `<button data-view="${id}" aria-pressed="${id === "front"}">${label}</button>`,
  )
  .join("")}</fieldset>
<label for="review-zoom">Tỷ lệ camera <select id="review-zoom"><option value="1">1× · Pixel gốc</option><option value="2" selected>2× · Gameplay</option></select></label></div>
<section class="review-stage"><div class="caption"><span>PHASER · CENTRAL PLAZA</span><span id="review-status" role="status">Đang mở bản duyệt…</span></div><div id="review-stage"></div></section>
<div class="concepts">${choices.map((c) => `<article><span class="letter">${c.id}</span><h2>${c.name}</h2><h3>${c.title}</h3><p>${c.detail}</p><div class="native-pair"><figure><img src="${base}review/characters/${c.id}/direction-stills-atlas-00.png" class="native-atlas" alt="${c.name}, bản pixel mặt trước ở 1×"><figcaption>1× · 80 px</figcaption></figure><figure><div class="detail-crop"><img src="${base}review/characters/${c.id}/direction-stills-atlas-00.png" alt="${c.name}, chi tiết pixel phóng 3×"></div><figcaption>3× · Chi tiết pixel</figcaption></figure></div></article>`).join("")}</div>
<p class="note">Bạn đã chọn B — Juni tạm thời. A — Bori và C — Nari được giữ làm phong cách avatar tương lai. Đây là bốn hướng tĩnh, chưa phải hoạt ảnh đi bộ. Bộ hoạt ảnh và NPC mới chờ xác nhận hình ảnh; game cũ vẫn được giữ nguyên.</p>
<a class="back" href="${base}">Mở game hiện tại →</a></main>`;

// A separate review entry reuses the approved scene's real preload/create path.
// No production art, actors, physics, UI or environment code is replaced.
class CharacterReview extends Plaza {
  private candidates: Phaser.GameObjects.Image[] = [];
  private view: View = "front";
  private reviewZoom = 2;
  private loaded = false;
  override preload() {
    super.preload();
    for (const c of choices)
      this.load.atlas(
        `concept-${c.id}`,
        `${base}review/characters/${c.id}/direction-stills-atlas-00.png`,
        `${base}review/characters/${c.id}/atlas.json`,
      );
  }
  override create() {
    controls.paused = true;
    controls.reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
    super.create();
    // Hide rejected actors only in this isolated review scene. Their original
    // game entry and authored files remain intact until explicit approval.
    for (const child of this.children.list) {
      if (
        child instanceof Phaser.GameObjects.Sprite &&
        /^(hero-|guest-)/.test(child.texture.key)
      )
        child.setVisible(false);
      if (child instanceof Phaser.GameObjects.Text) child.setVisible(false);
    }
    this.physics.world.pause();
    if (this.input.keyboard) this.input.keyboard.enabled = false;
    this.candidates = choices.map((c, i) =>
      this.add
        .image(430 + i * 105, 550, `concept-${c.id}`, this.view)
        .setOrigin(0.5, 96 / 104)
        .setDepth(550),
    );
    const reposition = () => {
      const width = this.scale.width;
      // Keep three full silhouettes visible at narrow viewport sizes too.
      const spacing = Math.min(105, (width / this.reviewZoom - 64) / 2);
      this.candidates.forEach((c, i) => c.setX(535 + (i - 1) * spacing));
      this.cameras.main.stopFollow();
      this.cameras.main.setZoom(this.reviewZoom).centerOn(535, 485);
    };
    reposition();
    this.scale.on("resize", reposition);
    for (const button of document.querySelectorAll<HTMLButtonElement>(
      "[data-view]",
    ))
      button.onclick = () => {
        this.view = button.dataset.view as View;
        this.candidates.forEach((c) => c.setFrame(this.view));
        for (const b of document.querySelectorAll("[data-view]"))
          b.setAttribute("aria-pressed", String(b === button));
        this.sample();
      };
    document.querySelector<HTMLSelectElement>("#review-zoom")!.onchange = (
      e,
    ) => {
      this.reviewZoom = Number((e.currentTarget as HTMLSelectElement).value);
      reposition();
      this.sample();
    };
    this.events.once("shutdown", () => this.scale.off("resize", reposition));
    this.loaded = true;
    document.querySelector("#review-status")!.textContent =
      "A · B · C / 80 px gốc / đang chờ lựa chọn";
    this.sample();
  }
  private sample() {
    const camera = this.cameras.main;
    window.__CHARACTER_REVIEW__ = {
      ready: this.loaded,
      view: this.view,
      zoom: this.reviewZoom,
      renderer: this.game.renderer.type === Phaser.WEBGL ? "WebGL" : "Canvas",
      canvas: { width: this.scale.width, height: this.scale.height },
      candidates: this.candidates.map((c, i) => ({
        id: choices[i].id,
        frame: String(c.frame.name),
        foot: {
          x: (c.x - camera.worldView.x) * this.reviewZoom,
          y: (c.y - camera.worldView.y) * this.reviewZoom,
        },
      })),
      nativeBodyHeight: 80,
      staticDesignProof: true,
      userApproval: "PENDING",
    };
  }
  override update() {
    if (this.loaded) this.sample();
  }
}
const stage = document.querySelector<HTMLDivElement>("#review-stage")!;
const game = new Phaser.Game({
  type:
    new URLSearchParams(location.search).get("renderer") === "canvas"
      ? Phaser.CANVAS
      : Phaser.AUTO,
  parent: stage,
  width: stage.clientWidth,
  height: 640,
  backgroundColor: "#e8d5a5",
  pixelArt: true,
  roundPixels: true,
  antialias: false,
  antialiasGL: false,
  physics: { default: "arcade", arcade: { debug: false } },
  scene: [new CharacterReview()],
  audio: { noAudio: true },
  banner: false,
});
new ResizeObserver(() =>
  game.scale.resize(
    stage.clientWidth,
    Math.min(640, Math.max(480, stage.clientWidth * 0.625)),
  ),
).observe(stage);
