import { characterRegistry } from "./registry";
import type { CharacterDefinition, AtlasData } from "./types";
export interface SelectionHost {
  current(): string;
  canOpen(): boolean;
  lock(): void;
  unlock(): void;
  confirm(id: string): Promise<{ saved: boolean }>;
}
/** Native modal prevents joystick/key gestures reaching the game beneath it. */
export class CharacterSelection {
  readonly dialog: HTMLDialogElement;
  private candidate = "juni";
  private first = false;
  private pending = false;
  private action = "idle";
  private previewToken = 0;
  private animation: number | undefined;
  private images = new Map<
    string,
    { image: HTMLImageElement; atlas: AtlasData }
  >();
  constructor(
    private host: SelectionHost,
    private base: string,
  ) {
    this.dialog = document.createElement("dialog");
    this.dialog.id = "character-selection";
    this.dialog.setAttribute("aria-labelledby", "character-title");
    this.dialog.innerHTML = `<section class="character-shell"><div class="character-heading"><span>KOREAN ARENA · PIXEL TOWN</span><button id="character-close" aria-label="Trở lại thế giới">✕</button></div><div class="character-intro"><h1 id="character-title">Một hành trình, nét riêng của bạn</h1><p>Chọn người bạn đồng hành giữa những con phố Hàn Quốc.</p></div><div class="character-content"><nav id="character-gallery" aria-label="Nhân vật"></nav><section class="character-detail" aria-label="Xem trước nhân vật"><div id="character-art"><canvas id="character-preview" width="192" height="224" aria-label="Hoạt ảnh nhân vật"></canvas><img id="character-master" alt="Thiết kế tham khảo — chưa phải sprite chơi được" hidden></div><div class="character-copy"><h2 id="character-name"></h2><p id="character-description"></p><p id="character-art-status"></p><div id="character-preview-actions"><button data-action="idle" aria-pressed="true">Đứng</button><button data-action="walk" aria-pressed="false">Đi bộ</button></div></div></section></div><footer class="character-footer"><p id="character-feedback" role="status" aria-live="polite"></p><button id="character-confirm">Bắt đầu hành trình</button></footer></section>`;
    document.body.append(this.dialog);
    const gallery = this.el("#character-gallery");
    for (const def of characterRegistry.all) {
      const card = document.createElement("button");
      card.type = "button";
      card.dataset.character = def.id;
      card.setAttribute("aria-pressed", "false");
      const names = document.createElement("strong");
      names.textContent = def.names.ko;
      const vi = document.createElement("span");
      vi.textContent = def.names.vi;
      const status = document.createElement("small");
      status.textContent =
        def.availability.status === "playable"
          ? "Sẵn sàng đồng hành"
          : "Đang hoàn thiện hoạt ảnh";
      card.append(names, vi, status);
      card.addEventListener("click", () => this.choose(def));
      gallery.append(card);
    }
    this.el("#character-close").addEventListener("click", () => {
      if (!this.pending) this.close();
    });
    this.dialog.addEventListener("cancel", (e) => {
      e.preventDefault();
      if (!this.first && !this.pending) this.close();
    });
    this.el("#character-confirm").addEventListener(
      "click",
      () => void this.confirm(),
    );
    for (const b of this.dialog.querySelectorAll<HTMLButtonElement>(
      "[data-action]",
    ))
      b.addEventListener("click", () => {
        this.action = b.dataset.action!;
        for (const q of this.dialog.querySelectorAll("[data-action]"))
          q.setAttribute("aria-pressed", String(q === b));
        void this.preview(characterRegistry.get(this.candidate)!);
      });
  }
  private el<T extends HTMLElement = HTMLElement>(selector: string) {
    return this.dialog.querySelector<T>(selector)!;
  }
  open(first = false) {
    if (this.pending || this.dialog.open || !this.host.canOpen()) return false;
    this.first = first;
    this.host.lock();
    this.el<HTMLButtonElement>("#character-close").hidden = first;
    this.el("#character-feedback").textContent = "";
    this.dialog.showModal();
    this.choose(characterRegistry.resolve(this.host.current()));
    return true;
  }
  private choose(def: CharacterDefinition) {
    if (this.pending) return;
    this.candidate = def.id;
    for (const b of this.dialog.querySelectorAll<HTMLButtonElement>(
      "[data-character]",
    ))
      b.setAttribute("aria-pressed", String(b.dataset.character === def.id));
    this.el("#character-name").textContent =
      `${def.names.ko} · ${def.names.vi}`;
    this.el("#character-description").textContent = def.description;
    const complete = def.availability.status === "playable";
    this.el("#character-art-status").textContent = complete
      ? "Người bạn nguyên bản của Korean Arena"
      : "Thiết kế tham khảo. Chưa đủ hoạt ảnh để vào thế giới.";
    this.el<HTMLButtonElement>("#character-confirm").disabled = !complete;
    this.el("#character-preview-actions").hidden = !complete;
    void this.preview(def);
  }
  private async preview(def: CharacterDefinition) {
    const token = ++this.previewToken;
    if (this.animation !== undefined) cancelAnimationFrame(this.animation);
    const canvas = this.el<HTMLCanvasElement>("#character-preview"),
      master = this.el<HTMLImageElement>("#character-master");
    canvas.hidden = def.availability.status !== "playable";
    master.hidden = !canvas.hidden;
    if (!def.assets) {
      master.src = this.base + def.preview;
      master.onerror = () => {
        master.hidden = true;
      };
      return;
    }
    try {
      let asset = this.images.get(def.id);
      if (!asset) {
        const response = await fetch(this.base + def.assets.atlas);
        if (!response.ok) throw Error("Missing preview atlas");
        const atlas: AtlasData = await response.json();
        const image = new Image();
        image.src = this.base + def.assets.texture;
        await image.decode();
        asset = { image, atlas };
        this.images.set(def.id, asset);
      }
      if (token !== this.previewToken || !this.dialog.open) return;
      const data = asset;
      const start = performance.now();
      const clip = def.animations[`${this.action}-front`];
      const tick = (now: number) => {
        if (token !== this.previewToken || !this.dialog.open) return;
        const scale = matchMedia("(max-height: 500px)").matches ? 1 : 2;
        canvas.width = def.native.width * scale;
        canvas.height = def.native.height * scale;
        const c = canvas.getContext("2d")!;
        c.imageSmoothingEnabled = false;
        let t = (now - start) % clip.durationsMs.reduce((a, b) => a + b, 0),
          i = 0;
        if (
          !matchMedia("(prefers-reduced-motion: reduce)").matches ||
          this.action === "walk"
        )
          while (i < clip.frames.length - 1 && t >= clip.durationsMs[i])
            t -= clip.durationsMs[i++];
        const f = data.atlas.frames[clip.frames[i]].frame;
        c.clearRect(0, 0, canvas.width, canvas.height);
        c.drawImage(
          data.image,
          f.x,
          f.y,
          f.w,
          f.h,
          0,
          0,
          canvas.width,
          canvas.height,
        );
        this.animation = requestAnimationFrame(tick);
      };
      tick(start);
    } catch {
      if (token === this.previewToken)
        this.el("#character-feedback").textContent =
          "Chưa tải được bản xem trước. Bạn vẫn có thể chọn Juni.";
    }
  }
  private async confirm() {
    if (
      this.pending ||
      characterRegistry.get(this.candidate)?.availability.status !== "playable"
    )
      return;
    this.pending = true;
    this.el<HTMLButtonElement>("#character-confirm").disabled = true;
    this.el<HTMLButtonElement>("#character-close").disabled = true;
    this.el("#character-feedback").textContent =
      "Đang chuẩn bị người bạn đồng hành…";
    try {
      const result = await this.host.confirm(this.candidate);
      this.first = false;
      this.close();
      if (!result.saved)
        document.querySelector("#near")!.textContent =
          "Đã chọn nhân vật cho phiên này · trình duyệt không lưu được tùy chọn.";
    } catch {
      this.el("#character-feedback").textContent =
        "Chưa đổi được nhân vật. Người chơi và vị trí hiện tại vẫn được giữ.";
    } finally {
      this.pending = false;
      this.el<HTMLButtonElement>("#character-close").disabled = false;
      this.el<HTMLButtonElement>("#character-confirm").disabled =
        characterRegistry.get(this.candidate)?.availability.status !==
        "playable";
    }
  }
  close() {
    if (!this.dialog.open) return;
    this.dialog.close();
    this.previewToken++;
    if (this.animation !== undefined) cancelAnimationFrame(this.animation);
    this.host.unlock();
  }
  dispose() {
    this.close();
    this.dialog.remove();
    this.images.clear();
  }
}
