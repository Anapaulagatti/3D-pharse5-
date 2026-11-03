import {
  crops,
  items,
  plots,
  ready,
  SHOPKEEPER,
  ECONOMY,
  type CropId,
  type FarmAction,
} from "../economy/catalog";
import { quests, itemNames, type QuestDefinition } from "./content";
import { QuestManager } from "./manager";
import "./style.css";
interface Host {
  player(): readonly [number, number];
  ground(x: number, y: number): boolean;
  canInteract(): boolean;
  lock(): () => void;
  onWorldAction?(): void;
  actor?(id: string): readonly [number, number] | undefined;
  onOpen(id: string): void;
  onClose(id: string): void;
}
export class QuestUI {
  readonly manager: QuestManager;
  readonly root = document.createElement("section");
  private dialog = document.createElement("dialog");
  private release?: () => void;
  private npcId?: string;
  private plotId?: string;
  private cropChoice: CropId = "radish";
  private lastTradeAt = -1000;
  private lastText = "";
  private feedback = "";
  private action?: { quest: string; step: string; label: string };
  private signal = new AbortController();
  constructor(private host: Host) {
    let storage: Storage | undefined;
    try {
      storage = localStorage;
    } catch {
      /* Optional local demo persistence. */
    }
    this.manager = new QuestManager(storage);
    this.root.id = "quest-hud";
    this.root.innerHTML =
      '<button id="quest-journal" aria-label="Nhiệm vụ và túi đồ">Nhiệm vụ · Túi đồ</button><p id="quest-tracker" aria-live="polite"></p><button id="quest-world-action" hidden></button>';
    this.dialog.id = "quest-dialogue";
    this.dialog.setAttribute("aria-labelledby", "quest-heading");
    document.body.append(this.root, this.dialog);
    const signal = this.signal.signal;
    this.root
      .querySelector("#quest-journal")!
      .addEventListener("click", () => this.open(), { signal });
    this.root
      .querySelector("#quest-world-action")!
      .addEventListener("click", () => this.tryWorldAction(), { signal });
    this.dialog.addEventListener(
      "cancel",
      (e) => {
        e.preventDefault();
        this.close();
      },
      { signal },
    );
    for (const el of [this.root, this.dialog])
      for (const event of [
        "pointerdown",
        "pointermove",
        "pointerup",
        "keydown",
        "wheel",
      ])
        el.addEventListener(event, (e) => e.stopPropagation(), { signal });
    document.addEventListener(
      "keydown",
      (e) => {
        if (
          this.dialog.open &&
          !e.repeat &&
          !(e.target instanceof HTMLInputElement) &&
          !(e.target instanceof HTMLSelectElement) &&
          /^[1-4]$/.test(e.key)
        ) {
          e.preventDefault();
          this.dialog
            .querySelector<HTMLButtonElement>(
              `[data-answer="${Number(e.key) - 1}"]`,
            )
            ?.click();
        }
      },
      { signal, capture: true },
    );
    this.update();
  }
  get target() {
    return this.npcId;
  }
  hasOffer(id: string) {
    return quests.some((q) => q.giver === id || q.recipient === id);
  }
  open(npcId?: string, plotId?: string) {
    if (this.dialog.open || !this.host.canInteract()) return false;
    this.npcId = npcId;
    this.plotId = plotId;
    this.release = this.host.lock();
    if (npcId) this.host.onOpen(npcId);
    this.feedback = "";
    this.render();
    this.dialog.showModal();
    this.dialog.querySelector<HTMLButtonElement>("button")?.focus();
    return true;
  }
  private button(label: string, action: () => void) {
    const b = document.createElement("button");
    b.type = "button";
    b.textContent = label;
    b.onclick = action;
    return b;
  }
  private render() {
    const active =
      document.activeElement instanceof HTMLElement
        ? document.activeElement.dataset.answer
        : undefined;
    this.dialog.replaceChildren();
    const heading = document.createElement("h2");
    heading.id = "quest-heading";
    heading.textContent = "Chuyện nhỏ trong thị trấn · 마을의 작은 일";
    const notice = document.createElement("p");
    notice.className = "quest-demo";
    notice.textContent =
      "Học tiếng Hàn: demo cục bộ, chưa đồng bộ website. Nội dung chờ duyệt giáo dục. Quảng cáo tắt.";
    const status = document.createElement("p");
    status.setAttribute("role", "status");
    status.textContent = this.manager.storageWarning || this.feedback;
    this.dialog.append(heading, notice, status);
    const s = this.manager.snapshot();
    const inventory = document.createElement("p");
    inventory.id = "quest-inventory";
    inventory.textContent = `Town Coins: ${s.coins} · XP trò chơi: ${s.xp} · ${
      Object.entries(s.inventory)
        .filter(([, n]) => n > 0)
        .map(([id, n]) => `${items[id]?.name ?? itemNames[id] ?? id}: ${n}`)
        .join(" · ") || "Túi đồ trống"
    }`;
    this.dialog.append(inventory);
    if (this.plotId) this.renderFarm();
    if (this.npcId === SHOPKEEPER) this.renderShop();
    for (const def of quests) {
      const section = document.createElement("section");
      section.className = "quest-card";
      section.dataset.quest = def.id;
      const title = document.createElement("h3");
      title.textContent = `${def.title} · ${def.ko}`;
      const text = document.createElement("p");
      const r = s.records[def.id];
      text.textContent = this.objective(def);
      section.append(title, text);
      if (!r && this.npcId === def.giver)
        section.append(
          this.button("Nhận nhiệm vụ", () => {
            this.manager.accept(def.id, this.npcId!);
            this.render();
          }),
        );
      if (
        r?.status === "active" &&
        r.step === def.steps.length &&
        this.npcId === (def.recipient ?? def.giver)
      )
        section.append(
          this.button(
            def.recipient
              ? "Giao sách và học tiếng Hàn"
              : "Bàn giao và học tiếng Hàn",
            () => {
              this.manager.returnToNPC(def.id, this.npcId!);
              this.render();
            },
          ),
        );
      const question = this.manager.question(def.id);
      if (question) {
        const prompt = document.createElement("p");
        prompt.lang = "ko";
        prompt.textContent = question.prompt;
        prompt.dataset.question = question.id;
        section.append(prompt);
        question.options.forEach((option, i) => {
          const b = this.button(`${i + 1}. ${option}`, () => {
            const result = this.manager.answer(def.id, question.id, i);
            this.feedback =
              result.result === "correct"
                ? `Chính xác! +${def.reward.coins} Town Coins · +${def.reward.xp} XP. ${result.explanation}`
                : result.result === "incorrect"
                  ? `Chưa đúng. ${result.explanation} Thử câu khác cùng mức nhé.`
                  : this.manager.storageWarning ||
                    (result.result === "unsaved"
                      ? "Chưa cấp thưởng: kiểm tra chỗ trống trong túi hoặc bộ nhớ rồi thử lại; nhiệm vụ được giữ nguyên."
                      : result.explanation);
            this.render();
          });
          b.dataset.answer = String(i);
          section.append(b);
        });
      }
      this.dialog.append(section);
    }
    this.dialog.append(
      this.button("Trở lại thế giới / Từ chối", () => this.close()),
    );
    if (this.dialog.open)
      this.dialog
        .querySelector<HTMLButtonElement>(
          active ? `[data-answer="${active}"]` : "button",
        )
        ?.focus();
    this.update();
  }

  private renderFarm() {
    const s = this.manager.snapshot(),
      plot = plots.find((p) => p.id === this.plotId)!;
    const state = s.economy.plots[plot.id];
    const box = document.createElement("section");
    box.className = "quest-card";
    box.dataset.farmPlot = plot.id;
    const title = document.createElement("h3");
    title.textContent = `Luống ${plot.id.slice(-2)} · 내 밭`;
    const help = document.createElement("p");
    help.textContent =
      "Gieo hạt, tưới nước rồi quay lại thu hoạch. Cây vẫn lớn khi bạn tiếp tục khám phá; tiến độ được lưu trên thiết bị này.";
    box.append(title, help);
    const select = document.createElement("select");
    select.id = "farm-crop";
    select.setAttribute("aria-label", "Chọn giống cây");
    for (const [id, crop] of Object.entries(crops))
      select.add(
        new Option(`${crop.name} · hạt ${s.inventory[crop.seed] ?? 0}`, id),
      );
    select.value = this.cropChoice;
    select.onchange = () => {
      this.cropChoice = select.value as CropId;
    };
    if (state.stage === "tilled") box.append(select);
    const action: FarmAction =
      state.stage === "empty"
        ? "till"
        : state.stage === "tilled"
          ? "plant"
          : state.stage === "planted"
            ? "water"
            : "harvest";
    const labels = {
      till: "Xới hàng · 밭을 갈아요",
      plant: "Gieo hạt · 씨앗을 심어요",
      water: "Tưới cây · 물을 줘요",
      harvest: "Thu hoạch · 수확해요",
    };
    const transaction = `${plot.id}:${state.cycle}:${action}:${s.economy.revision}`;
    const b = this.button(labels[action], () => {
      const ok = this.manager.farmAction(
        plot.id,
        action,
        this.cropChoice,
        transaction,
        this.host.player(),
        (x, y) => this.host.ground(x, y),
      );
      this.feedback = ok
        ? "Đã lưu thao tác canh tác."
        : this.manager.storageWarning ||
          "Chưa thực hiện: kiểm tra hạt giống, vị trí, độ chín hoặc chỗ trống trong túi. Không mất vật phẩm.";
      if (ok) this.host.onWorldAction?.();
      this.render();
    });
    b.dataset.farmAction = action;
    b.disabled = action === "harvest" && !ready(state, Date.now());
    box.append(b);
    const note = document.createElement("p");
    note.id = "farm-ready-note";
    box.append(note);
    this.dialog.append(box);
  }
  private renderShop() {
    const s = this.manager.snapshot();
    const box = document.createElement("section");
    box.className = "quest-card";
    box.id = "town-shop";
    const h = document.createElement("h3");
    h.textContent = "Cửa hàng Minseo · 민서의 가게";
    box.append(h);
    const hint = document.createElement("p");
    hint.textContent = `Túi ${Object.values(s.inventory).filter((n) => n > 0).length}/${ECONOMY.slots}ô. Giá thử nghiệm; mặc định nhân vật/cosmetics và việc học luôn miễn phí. Không mua bằng tiền thật.`;
    box.append(hint);
    const label = document.createElement("label");
    label.textContent = "Số lượng ";
    const qty = document.createElement("input");
    qty.type = "number";
    qty.id = "shop-quantity";
    qty.min = "1";
    qty.max = "99";
    qty.value = "1";
    qty.setAttribute("aria-label", "Số lượng mua bán");
    label.append(qty);
    box.append(label);
    for (const [id, item] of Object.entries(items)) {
      const row = document.createElement("div");
      row.className = "shop-row";
      const text = document.createElement("p");
      text.textContent = `${item.name} · ${item.ko} · có ${s.inventory[id] ?? 0} · ${item.buy ? `mua ${item.buy}xu, kho ${s.economy.stock[id] ?? 0}` : `bán ${item.sell}xu`}`;
      row.append(text);
      if (id === "jeju-postcard") {
        const image = document.createElement("img");
        image.src = import.meta.env.BASE_URL + "assets/farming/postcard.png";
        image.width = 128;
        image.height = 96;
        image.alt = "Bưu thiếp cảnh cầu Jeju từ artwork được duyệt";
        image.style.imageRendering = "pixelated";
        row.append(image);
      }

      const kind = item.buy ? "buy" : "sell";
      const tx = `${kind}:${id}:${s.economy.revision}`;
      const b = this.button(
        kind === "buy" ? "Mua · 사요" : "Bán · 팔아요",
        () => {
          if (performance.now() - this.lastTradeAt < 300) return;
          this.lastTradeAt = performance.now();
          const actor = this.host.actor?.(SHOPKEEPER);
          const ok =
            !!actor &&
            this.manager.trade(kind, id, Number(qty.value), tx, {
              npcId: this.npcId!,
              player: this.host.player(),
              actor,
              ground: (x, y) => this.host.ground(x, y),
            });
          this.feedback = ok
            ? "Đã lưu giao dịch; xu và vật phẩm cập nhật cùng nhau."
            : this.manager.storageWarning ||
              "Giao dịch không đổi: kiểm tra số lượng nguyên dương, xu, hàng còn trong kho hoặc túi đồ.";
          this.render();
        },
      );
      b.dataset.trade = kind;
      b.dataset.item = id;
      row.append(b);
      box.append(row);
    }
    this.dialog.append(box);
  }
  objective(def: QuestDefinition) {
    const r = this.manager.snapshot().records[def.id];
    if (!r && def.giver === "npc-nayeon")
      return "Gặp Nayeon ở nông trại. Nhận một hạt củ cải miễn phí; lứa đầu6giây, không khóa việc học.";
    if (!r)
      return `Chưa nhận · gặp ${def.giver === "npc-harin" ? "Harin tại Jeju" : def.giver === "npc-minseo" ? "Minseo tại phố thương mại" : "Cheolsu tại nông trại"}.`;
    if (r.status === "completed")
      return "Hoàn thành · phần thưởng đã nhận một lần.";
    if (r.status === "challenge")
      return "Trả lời đúng câu hỏi tiếng Hàn để nhận phần thưởng.";
    if (def.recipient) return "Mang gói sách đến Jiho ở hiệu sách.";
    return (
      def.steps[r.step]?.label ??
      `Quay lại ${def.giver === "npc-harin" ? "Harin" : "Cheolsu"} để bàn giao và học tiếng Hàn.`
    );
  }
  update() {
    const s = this.manager.snapshot();
    const text = quests
      .filter((q) => s.records[q.id] && s.records[q.id].status !== "completed")
      .map((q) => `${q.title}: ${this.objective(q)}`)
      .join(" · ");
    if (text !== this.lastText) {
      this.root.querySelector("#quest-tracker")!.textContent = text;
      this.lastText = text;
    }
    this.action = undefined;
    if (this.host.canInteract())
      for (const def of quests) {
        const r = s.records[def.id],
          step = def.steps[r?.step ?? -1];
        if (
          r?.status === "active" &&
          !def.economyObjectives &&
          step &&
          Math.hypot(
            this.host.player()[0] - step.point[0],
            this.host.player()[1] - step.point[1],
          ) <= 30 &&
          this.host.ground(...step.point)
        ) {
          this.action = { quest: def.id, step: step.id, label: step.label };
          break;
        }
      }
    const b = this.root.querySelector<HTMLButtonElement>(
      "#quest-world-action",
    )!;
    const plot = this.host.canInteract()
      ? plots.find(
          (p) =>
            Math.hypot(
              this.host.player()[0] - p.point[0],
              this.host.player()[1] - p.point[1],
            ) <= 30 && this.host.ground(...p.point),
        )
      : undefined;
    b.hidden = !this.action && !plot;
    b.dataset.plotId = plot?.id ?? "";
    if (!this.action && plot) b.textContent = `E · Canh tác ${plot.id} · 농사`;

    if (this.action) b.textContent = `E · ${this.action.label}`;
    if (this.dialog.open && this.plotId) {
      const p = this.manager.snapshot().economy.plots[this.plotId];
      const harvest = this.dialog.querySelector<HTMLButtonElement>(
        '[data-farm-action="harvest"]',
      );
      if (harvest) harvest.disabled = !ready(p, Date.now());
      const note = this.dialog.querySelector("#farm-ready-note");
      if (note && p.wateredAt !== undefined)
        note.textContent = ready(p, Date.now())
          ? "Đã chín · 수확할 수 있어요"
          : `Còn ${Math.max(0, Math.ceil(((p.growMs ?? 0) - (Date.now() - p.wateredAt)) / 1000))}giây; có thể đóng bảng và tiếp tục khám phá.`;
    }
    const journal =
      this.root.querySelector<HTMLButtonElement>("#quest-journal")!;
    journal.disabled = !this.dialog.open && !this.host.canInteract();
  }
  tryWorldAction() {
    if (!this.host.canInteract()) return false;
    if (!this.action) {
      const plot = plots.find(
        (p) =>
          Math.hypot(
            this.host.player()[0] - p.point[0],
            this.host.player()[1] - p.point[1],
          ) <= 30 && this.host.ground(...p.point),
      );
      return plot ? this.open(undefined, plot.id) : false;
    }
    const success = this.manager.worldAction(
      this.action.quest,
      this.action.step,
      this.host.player(),
      (x, y) => this.host.ground(x, y),
    );
    if (success) this.host.onWorldAction?.();
    this.update();
    return success;
  }
  close() {
    if (!this.dialog.open) return;
    this.dialog.close();
    const id = this.npcId;
    this.npcId = undefined;
    this.plotId = undefined;
    if (id) this.host.onClose(id);
    this.release?.();
    this.release = undefined;
    this.update();
  }
  dispose() {
    this.close();
    this.signal.abort();
    this.root.remove();
    this.dialog.remove();
  }
}
