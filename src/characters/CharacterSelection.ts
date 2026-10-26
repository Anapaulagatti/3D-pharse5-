import { characterRegistry } from "./registry";
import type { CharacterDefinition, Direction } from "./types";
import type { CharacterAppearance, CosmeticCategory } from "./appearanceTypes";
import { AppearancePreferences, browserPreferenceStorage } from "./preferences";
import {
  compatibleItems,
  defaultAppearance,
  normalizeAppearance,
} from "./appearance";
import { appearanceRenderer } from "./AppearanceRenderer";
import { studioMessages, type StudioLocale } from "./studioI18n";
export interface SelectionHost {
  current(): string;
  appearance?(): CharacterAppearance;
  canOpen(): boolean;
  lock(): void;
  unlock(): void;
  confirm(
    id: string,
    appearance?: CharacterAppearance,
    presetName?: string,
  ): Promise<{ saved: boolean; fallbackReason?: string }>;
}
/** The existing character-selection modal now owns the Studio. Gameplay input is
 * isolated by the same scene lock; all previews use the same composed native atlas. */
export class CharacterSelection {
  readonly dialog: HTMLDialogElement;
  private candidate = "juni";
  private first = false;
  private pending = false;
  private action = "idle";
  private view: Direction = "front";
  private category: CosmeticCategory = "hairstyle";
  private drafts = new Map<string, CharacterAppearance>();
  private look = defaultAppearance("juni");
  private previewToken = 0;
  private previewAbort?: AbortController;
  private lifecycle = new AbortController();
  private animation: number | undefined;
  private copy;
  constructor(
    private host: SelectionHost,
    private base: string,
    private appearances = new AppearancePreferences(
      browserPreferenceStorage(),
      characterRegistry,
    ),
    locale: StudioLocale = "vi",
  ) {
    this.copy = studioMessages[locale];
    this.dialog = document.createElement("dialog");
    this.dialog.id = "character-selection";
    this.dialog.setAttribute("aria-labelledby", "character-title");
    this.dialog.innerHTML = `<section class="character-shell"><div class="character-heading"><span>KOREAN ARENA · CHARACTER STUDIO</span><button id="character-close" aria-label="Trở lại thế giới">✕</button></div><div class="character-intro"><h1 id="character-title">${this.copy.title}</h1><p>${this.copy.subtitle}</p></div><div class="character-content"><div class="studio-gallery-column"><h2>${this.copy.characters}</h2><nav id="character-gallery" aria-label="Nhân vật"></nav><details id="future-roster"><summary>${this.copy.upcoming}</summary><p></p></details></div><section class="character-detail" aria-label="Xem trước nhân vật"><div id="character-art"><canvas id="character-preview" width="192" height="224" aria-label="Hoạt ảnh nhân vật"></canvas></div><div class="character-copy"><h2 id="character-name"></h2><p id="character-description"></p><p id="character-art-status"></p></div><div id="character-preview-actions">${[
      ["idle", "Đứng"],
      ["walk", "Đi bộ"],
      ["run", "Chạy"],
      ["wave", "Chào"],
      ["celebrate", "Vui"],
    ]
      .map(
        ([id, label]) =>
          `<button data-action="${id}" aria-pressed="${id === "idle"}">${label}</button>`,
      )
      .join(
        "",
      )}</div><label class="studio-direction">Hướng nhìn<select id="character-preview-direction"><option value="front">Trước</option><option value="back">Sau</option><option value="left">Trái</option><option value="right">Phải</option></select></label></section><section class="studio-wardrobe" aria-label="${this.copy.appearance}"><div class="studio-wardrobe-heading"><h2>${this.copy.appearance}</h2><span>${this.copy.free}</span></div><div id="cosmetic-categories" aria-label="Danh mục">${(["hairstyle", "outfit", "accessory"] as const).map((category) => `<button data-category="${category}" aria-pressed="${category === "hairstyle"}">${this.copy[category]}</button>`).join("")}</div><div id="cosmetic-items" aria-live="polite"></div><div class="studio-presets"><label>${this.copy.presets}<select id="appearance-preset"><option value="">—</option></select></label><label>${this.copy.presetName}<input id="appearance-preset-name" maxlength="32" autocomplete="off"></label></div></section></div><footer class="character-footer"><p id="character-feedback" role="status" aria-live="polite"></p><div><button id="appearance-reset">${this.copy.reset}</button><button id="appearance-save">${this.copy.save}</button><button id="character-confirm">${this.copy.enter}</button></div></footer></section>`;
    document.body.append(this.dialog);
    const gallery = this.el("#character-gallery");
    for (const def of characterRegistry.all) {
      const card = document.createElement("button");
      card.type = "button";
      card.dataset.character = def.id;
      card.setAttribute("aria-pressed", "false");
      const image = document.createElement("img");
      image.alt = "";
      image.loading = "lazy";
      image.src =
        base +
        (def.id === "juni"
          ? "assets/character-studio/juni-preview.png"
          : def.preview);
      const names = document.createElement("strong");
      names.textContent = def.names.ko;
      const vi = document.createElement("span");
      vi.textContent = def.names.vi;
      const status = document.createElement("small");
      status.textContent =
        def.availability.status === "playable"
          ? "Sẵn sàng đồng hành"
          : "Đang hoàn thiện hoạt ảnh";
      card.append(image, names, vi, status);
      card.disabled = def.availability.status !== "playable";
      card.addEventListener("click", () => this.choose(def));
      gallery.append(card);
    }
    this.el("#future-roster p").textContent = characterRegistry.planned
      .map((slot) => `${slot.names.ko} · ${slot.names.vi}`)
      .join(" / ");
    this.el("#future-roster").hidden = characterRegistry.planned.length === 0;
    this.el("#character-close").addEventListener("click", () => {
      if (!this.pending) this.close();
    });
    this.dialog.addEventListener("cancel", (e) => {
      e.preventDefault();
      if (!this.first && !this.pending) this.close();
    });
    this.el("#character-confirm").addEventListener(
      "click",
      () => void this.confirm(true),
    );
    this.el("#appearance-save").addEventListener(
      "click",
      () => void this.confirm(false),
    );
    this.el("#appearance-reset").addEventListener("click", () => {
      if (this.pending) return;
      this.look = defaultAppearance(this.candidate);
      this.drafts.set(this.candidate, this.look);
      this.el<HTMLSelectElement>("#appearance-preset").value = "";
      this.el<HTMLInputElement>("#appearance-preset-name").value = "";
      this.items();
      this.feedback(this.copy.resetHint);
      void this.preview();
    });
    for (const button of this.dialog.querySelectorAll<HTMLButtonElement>(
      "[data-action]",
    ))
      button.addEventListener("click", () => {
        this.action = button.dataset.action!;
        for (const b of this.dialog.querySelectorAll("[data-action]"))
          b.setAttribute("aria-pressed", String(b === button));
        if (["wave", "celebrate"].includes(this.action)) {
          this.view = "front";
          this.el<HTMLSelectElement>("#character-preview-direction").value =
            "front";
        }
        void this.preview();
      });
    this.el<HTMLSelectElement>("#character-preview-direction").addEventListener(
      "change",
      (e) => {
        this.view = (e.target as HTMLSelectElement).value as Direction;
        if (["wave", "celebrate"].includes(this.action)) this.action = "idle";
        for (const b of this.dialog.querySelectorAll<HTMLButtonElement>(
          "[data-action]",
        ))
          b.setAttribute(
            "aria-pressed",
            String(b.dataset.action === this.action),
          );
        void this.preview();
      },
    );
    for (const b of this.dialog.querySelectorAll<HTMLButtonElement>(
      "[data-category]",
    ))
      b.addEventListener("click", () => {
        this.category = b.dataset.category as CosmeticCategory;
        this.items();
      });
    this.el<HTMLSelectElement>("#appearance-preset").addEventListener(
      "change",
      (e) => {
        const preset = this.appearances
          .presets()
          .find((p) => p.id === (e.target as HTMLSelectElement).value);
        if (!preset) return;
        this.drafts.set(preset.appearance.characterId, preset.appearance);
        this.choose(characterRegistry.resolve(preset.appearance.characterId));
      },
    );
    this.presets();
    window.addEventListener(
      "resize",
      () => {
        if (this.dialog.open && !this.pending) void this.preview();
      },
      { signal: this.lifecycle.signal },
    );
  }
  private el<T extends HTMLElement = HTMLElement>(selector: string) {
    return this.dialog.querySelector<T>(selector)!;
  }
  private feedback(value: string) {
    this.el("#character-feedback").textContent = value;
  }
  open(first = false) {
    if (this.pending || this.dialog.open || !this.host.canOpen()) return false;
    this.first = first;
    this.host.lock();
    this.el<HTMLButtonElement>("#character-close").hidden = first;
    this.feedback("");
    this.drafts.clear();
    const current = this.host.current();
    if (this.host.appearance) this.drafts.set(current, this.host.appearance());
    this.dialog.showModal();
    this.choose(characterRegistry.resolve(current));
    return true;
  }
  private choose(def: CharacterDefinition) {
    if (this.pending) return;
    this.candidate = def.id;
    this.look = normalizeAppearance(
      def.id,
      this.drafts.get(def.id) ?? this.appearances.read(def.id),
    );
    this.drafts.set(def.id, this.look);
    for (const b of this.dialog.querySelectorAll<HTMLButtonElement>(
      "[data-character]",
    ))
      b.setAttribute("aria-pressed", String(b.dataset.character === def.id));
    this.dialog
      .querySelector(`[data-character="${def.id}"]`)
      ?.scrollIntoView({ block: "nearest", inline: "nearest" });
    this.el("#character-name").textContent =
      `${def.names.ko} · ${def.names.vi}`;
    this.el("#character-description").textContent = def.description;
    this.el("#character-art-status").textContent =
      "Người bạn nguyên bản của Korean Arena";
    this.el<HTMLButtonElement>("#character-confirm").disabled =
      def.availability.status !== "playable";
    this.el<HTMLInputElement>("#appearance-preset-name").value = "";
    this.items();
    this.presets();
    void this.preview();
  }
  private items() {
    for (const b of this.dialog.querySelectorAll<HTMLButtonElement>(
      "[data-category]",
    ))
      b.setAttribute(
        "aria-pressed",
        String(b.dataset.category === this.category),
      );
    const area = this.el("#cosmetic-items");
    area.replaceChildren();
    const options = compatibleItems(this.candidate, this.category),
      all = compatibleItems(this.candidate);
    if (!all.length) {
      const p = document.createElement("p");
      p.className = "studio-empty";
      p.textContent = characterRegistry
        .get(this.candidate)
        ?.cosmetics.tags.includes("default-only")
        ? this.copy.default
        : this.copy.unavailable;
      area.append(p);
      return;
    }
    const add = (id: string, name: string, preview?: string) => {
      const selected =
        id === "default"
          ? this.category === "accessory"
            ? this.look.accessoryIds.length === 0
            : !this.look[
                this.category === "hairstyle" ? "hairstyleId" : "outfitId"
              ]
          : this.category === "accessory"
            ? this.look.accessoryIds.includes(id)
            : this.look[
                this.category === "hairstyle" ? "hairstyleId" : "outfitId"
              ] === id;
      const b = document.createElement("button");
      b.dataset.cosmetic = id;
      b.setAttribute("aria-pressed", String(selected));
      b.type = "button";
      if (preview) {
        const image = document.createElement("img");
        image.alt = "";
        image.src = this.base + preview;
        b.append(image);
      }
      const label = document.createElement("span");
      label.textContent = `${selected ? "✓ " : ""}${name}`;
      b.append(label);
      b.addEventListener("click", () => {
        if (this.pending) return;
        const next = {
          ...this.look,
          accessoryIds: [...this.look.accessoryIds],
        };
        if (this.category === "accessory")
          next.accessoryIds =
            id === "default"
              ? []
              : selected
                ? next.accessoryIds.filter((v) => v !== id)
                : [...next.accessoryIds, id];
        else
          next[this.category === "hairstyle" ? "hairstyleId" : "outfitId"] =
            id === "default" ? null : id;
        this.look = normalizeAppearance(this.candidate, next);
        this.drafts.set(this.candidate, this.look);
        this.items();
        void this.preview();
      });
      area.append(b);
    };
    add("default", this.copy.default);
    for (const item of options)
      add(
        item.id,
        item.name.vi,
        item.variants.find((v) => v.characterId === this.candidate)?.preview,
      );
  }
  private presets() {
    const select = this.el<HTMLSelectElement>("#appearance-preset");
    select.replaceChildren(new Option("—", ""));
    for (const preset of this.appearances.presets())
      select.add(new Option(preset.name, preset.id));
  }
  private async preview() {
    const def = characterRegistry.resolve(this.candidate),
      token = ++this.previewToken;
    this.previewAbort?.abort();
    this.previewAbort = new AbortController();
    if (this.animation !== undefined) cancelAnimationFrame(this.animation);
    try {
      const asset = await appearanceRenderer.render(
        def,
        this.look,
        this.base,
        this.previewAbort.signal,
      );
      if (token !== this.previewToken || !this.dialog.open) return;
      if (asset.fallbackReason) {
        this.look = asset.appearance;
        this.drafts.set(def.id, this.look);
        this.items();
        this.feedback(
          "Mục ngoại hình chưa tải được. Đã khôi phục bản nguyên gốc.",
        );
      }
      const canvas = this.el<HTMLCanvasElement>("#character-preview");
      const scale = matchMedia("(max-height: 560px)").matches ? 1 : 2;
      canvas.width = def.native.width * scale;
      canvas.height = def.native.height * scale;
      const c = canvas.getContext("2d")!;
      c.imageSmoothingEnabled = false;
      const view = ["wave", "celebrate"].includes(this.action)
        ? "front"
        : this.view;
      const clip =
          def.animations[`${this.action}-${view}`] ??
          def.animations[`idle-${view}`],
        start = performance.now();
      const durations = ["walk", "run"].includes(this.action)
        ? clip.frames.map(
            () =>
              (1000 *
                (this.action === "walk"
                  ? def.movement.walkStride / def.movement.walkSpeed
                  : def.movement.runStride / def.movement.runSpeed)) /
              clip.frames.length,
          )
        : clip.durationsMs;
      const duration = durations.reduce((a, b) => a + b, 0);
      const tick = (now: number) => {
        if (token !== this.previewToken || !this.dialog.open) return;
        let t = clip.loop
            ? (now - start) % duration
            : Math.min(now - start, duration - 1),
          i = 0;
        if (
          !matchMedia("(prefers-reduced-motion: reduce)").matches ||
          this.action !== "idle"
        )
          while (i < clip.frames.length - 1 && t >= durations[i])
            t -= durations[i++];
        const f = asset.atlas.frames[clip.frames[i]].frame;
        c.clearRect(0, 0, canvas.width, canvas.height);
        c.drawImage(
          asset.image,
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
      if (token === this.previewToken && !this.previewAbort.signal.aborted)
        this.feedback(
          "Chưa tải được bản xem trước. Hãy thử lại hoặc chọn Juni.",
        );
    }
  }
  private async confirm(enter: boolean) {
    if (
      this.pending ||
      characterRegistry.get(this.candidate)?.availability.status !== "playable"
    )
      return;
    this.pending = true;
    for (const b of this.dialog.querySelectorAll<HTMLButtonElement>("button"))
      b.disabled = true;
    this.feedback(this.copy.loading);
    try {
      const result = await this.host.confirm(
        this.candidate,
        this.look,
        this.el<HTMLInputElement>("#appearance-preset-name").value,
      );
      this.look = this.host.appearance?.() ?? this.look;
      this.drafts.set(this.candidate, this.look);
      this.feedback(
        result.fallbackReason
          ? "Đã khôi phục ngoại hình nguyên bản vì tài sản tùy chỉnh chưa sẵn sàng."
          : result.saved
            ? this.copy.saved
            : this.copy.noSave,
      );
      this.presets();
      this.items();
      if (!enter) void this.preview();
      if (enter) {
        this.first = false;
        this.close();
        if (!result.saved)
          document.querySelector("#near")!.textContent = this.copy.noSave;
      }
    } catch {
      this.feedback(this.copy.failed);
    } finally {
      this.pending = false;
      for (const b of this.dialog.querySelectorAll<HTMLButtonElement>("button"))
        b.disabled = false;
      for (const b of this.dialog.querySelectorAll<HTMLButtonElement>(
        "[data-character]",
      ))
        b.disabled =
          characterRegistry.get(b.dataset.character!)?.availability.status !==
          "playable";
    }
  }
  close() {
    if (!this.dialog.open) return;
    this.dialog.close();
    this.previewToken++;
    this.previewAbort?.abort();
    if (this.animation !== undefined) cancelAnimationFrame(this.animation);
    this.host.unlock();
  }
  dispose() {
    this.lifecycle.abort();
    this.close();
    this.dialog.remove();
    this.drafts.clear();
  }
}
