import cropAtlas from "../../public/assets/roadmap-v2/crops.json";
import {
  crops,
  cropUnlocked,
  cropUnlockHint,
  items,
  plots,
  nearGround,
  SHOPKEEPER,
  ECONOMY,
  type CropId,
} from "../economy/catalog";
import { plotPresentation, type FarmTool } from "../economy/presentation";
import { quests, itemNames, type QuestDefinition } from "./content";
import { QuestManager, type InteractionContext } from "./manager";
import "./style.css";
export type WorldFeedback =
  | "plant"
  | "water"
  | "harvest"
  | "collect"
  | "deliver"
  | "handover"
  | "report"
  | "reward";
export interface QuestHost {
  player(): readonly [number, number];
  ground(x: number, y: number): boolean;
  canInteract(): boolean;
  lock(): () => void;
  actor?(id: string): readonly [number, number] | undefined;
  actorName?(id: string): string | undefined;
  feedback?(
    kind: WorldFeedback,
    target: readonly [number, number],
    label: string,
  ): void;
  onOpen(id: string): void;
  onClose(id: string): void;
}
type View = "journal" | "inventory" | "npc" | "shop";
const itemName = (id: string) => items[id]?.name ?? itemNames[id] ?? id;
export class QuestUI {
  readonly manager: QuestManager;
  readonly root = document.createElement("section");
  private dialog = document.createElement("dialog");
  private picker = document.createElement("div");
  private release?: () => void;
  private npcId?: string;
  private mode: View = "journal";
  private cropChoice: CropId = "radish";
  private tool: FarmTool = "seed";
  private lastTradeAt = -1000;
  private lastActionAt = -1000;
  private message = "";
  private toastUntil = 0;
  private lastHUD = "";
  private shopTab: "buy" | "sell" = "buy";
  private quantity = 1;
  private nearest?: string;
  private orchard?: {
    id: string;
    step: string;
    point: readonly [number, number];
  };
  private followup?: ReturnType<typeof setTimeout>;
  private signal = new AbortController();
  private exteriorHost: QuestHost;
  private inventoryCategory = "all";
  useInterior(host?: QuestHost) {
    this.close();
    this.host = host ?? this.exteriorHost;
    this.update();
  }
  constructor(private host: QuestHost) {
    this.exteriorHost = host;
    let storage: Storage | undefined;
    try {
      storage = localStorage;
    } catch {
      /* Optional local demo. */
    }
    this.manager = new QuestManager(storage);
    this.message = this.manager.migrationNotice;
    this.root.id = "quest-hud";
    this.root.innerHTML =
      '<div class="town-pocket"><output id="town-coins" aria-label="Town Coins"></output><button id="quest-inventory" aria-label="Mở túi đồ">Túi đồ</button><button id="quest-journal" aria-label="Xem nhiệm vụ">Nhiệm vụ</button></div><p id="quest-tracker" aria-live="polite"></p><div id="farm-toolbelt" role="toolbar" aria-label="Dụng cụ canh tác"><button data-tool="seed" aria-label="Xới đất hoặc chọn hạt giống">Đất / Hạt</button><button data-tool="water" aria-label="Trang bị bình tưới">Tưới</button><button data-tool="harvest" aria-label="Trang bị dụng cụ thu hoạch">Gặt</button></div><button id="quest-world-action" hidden></button><output id="world-feedback" role="status"></output>';
    this.picker.id = "seed-picker";
    this.picker.hidden = true;
    this.picker.setAttribute("role", "group");
    this.picker.setAttribute("aria-label", "Chọn hạt cho luống gần bạn");
    this.root.append(this.picker);
    this.dialog.id = "quest-dialogue";
    this.dialog.setAttribute("aria-labelledby", "quest-heading");
    document.body.append(this.root, this.dialog);
    const signal = this.signal.signal;
    this.root
      .querySelector("#quest-journal")!
      .addEventListener("click", () => this.open(), { signal });
    this.root
      .querySelector("#quest-inventory")!
      .addEventListener("click", () => this.openInventory(), { signal });
    this.root
      .querySelector("#quest-world-action")!
      .addEventListener("click", () => this.tryWorldAction(), { signal });
    for (const b of this.root.querySelectorAll<HTMLButtonElement>(
      "[data-tool]",
    )) {
      b.prepend(this.icon(b.dataset.tool === "seed" ? "hoe" : b.dataset.tool!));
      b.onclick = () => this.equip(b.dataset.tool as FarmTool);
    }
    this.dialog.addEventListener(
      "cancel",
      (e) => {
        e.preventDefault();
        this.close();
      },
      { signal },
    );
    for (const el of [this.root, this.dialog])
      for (const name of ["pointerdown", "pointermove", "pointerup", "wheel"])
        el.addEventListener(name, (e) => e.stopPropagation(), { signal });
    document.addEventListener(
      "keydown",
      (e) => {
        if (
          e.repeat ||
          e.isComposing ||
          e.keyCode === 229 ||
          e.ctrlKey ||
          e.metaKey ||
          e.altKey
        )
          return;
        if (this.dialog.open) {
          if (e.key === "Escape") {
            e.preventDefault();
            this.close();
          } else if (
            !(e.target instanceof HTMLInputElement) &&
            /^[1-4]$/.test(e.key)
          ) {
            e.preventDefault();
            this.dialog
              .querySelector<HTMLButtonElement>(
                `[data-answer="${Number(e.key) - 1}"]`,
              )
              ?.click();
          }
          return;
        }
        if (!this.host.canInteract()) return;
        const k = e.key.toLowerCase();
        if (k === "i") this.openInventory();
        else if (k === "j") this.open();
        else if (/^[1-3]$/.test(k))
          this.equip((["seed", "water", "harvest"] as const)[Number(k) - 1]);
        else if (k === "escape") this.picker.hidden = true;
      },
      { signal, capture: true },
    );
    for (const [selector, icon] of [
      ["#quest-inventory", "bag"],
      ["#quest-journal", "journal"],
    ] as const)
      this.root.querySelector(selector)!.prepend(this.icon(icon));
    this.update();
  }
  get target() {
    return this.npcId;
  }
  get selectedPlot() {
    return this.nearest;
  }
  get selectedTool() {
    return this.tool;
  }
  interactionNPCs() {
    const s = this.manager.snapshot(),
      ids = new Set([SHOPKEEPER]);
    for (const q of quests) {
      const r = s.records[q.id];
      if (r?.status !== "completed") ids.add(q.giver);
      if (q.recipient && r && r.status !== "completed") ids.add(q.recipient);
    }
    return ids;
  }
  hasOffer(id: string) {
    return quests.some((q) => q.giver === id || q.recipient === id);
  }
  canReport(id: string) {
    const s = this.manager.snapshot();
    return quests.some(
      (q) =>
        (q.recipient ?? q.giver) === id &&
        s.records[q.id]?.status === "active" &&
        s.records[q.id].step === q.steps.length,
    );
  }
  reportToNPC(id: string) {
    if (!this.host.canInteract()) return false;
    const c = this.context(id),
      s = this.manager.snapshot(),
      q = quests.find(
        (q) =>
          (q.recipient ?? q.giver) === id &&
          s.records[q.id]?.status === "active" &&
          s.records[q.id].step === q.steps.length,
      );
    return !!c && !!q && this.report(q, c);
  }
  private report(q: QuestDefinition, c: InteractionContext) {
    if (!this.manager.returnInWorld(q.id, c.npcId, c)) return false;
    this.host.feedback?.(
      q.recipient ? "deliver" : q.topic === "orchard" ? "handover" : "report",
      c.actor,
      q.recipient
        ? "Đã giao bưu kiện"
        : q.topic === "orchard"
          ? "Đã giao quýt"
          : "Đã báo lại",
    );
    const id = c.npcId;
    this.close();
    if (this.followup) clearTimeout(this.followup);
    this.followup = setTimeout(() => {
      this.followup = undefined;
      if (this.context(id) && this.host.canInteract()) this.open(id);
    }, 750);
    return true;
  }
  private context(id = this.npcId): InteractionContext | undefined {
    const actor = id && this.host.actor?.(id);
    if (
      !id ||
      !actor ||
      !nearGround(
        this.host.player(),
        actor,
        (x, y) => this.host.ground(x, y),
        112,
      )
    )
      return;
    return {
      npcId: id,
      player: this.host.player(),
      actor,
      ground: (x, y) => this.host.ground(x, y),
    };
  }
  open(id?: string) {
    return this.show(id ? "npc" : "journal", id);
  }
  openInventory() {
    return this.show("inventory");
  }
  openShop(id = SHOPKEEPER) {
    return id === SHOPKEEPER && this.show("shop", id);
  }
  private show(view: View, id?: string) {
    if (
      this.dialog.open ||
      !this.host.canInteract() ||
      (id && !this.context(id))
    )
      return false;
    this.mode = view;
    this.npcId = id;
    this.message = this.manager.migrationNotice;
    this.release = this.host.lock();
    if (id) this.host.onOpen(id);
    this.picker.hidden = true;
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
  private text(tag: string, value: string) {
    const e = document.createElement(tag);
    e.textContent = value;
    return e;
  }
  private icon(id: string) {
    if (["coin", "bag", "journal", "hoe"].includes(id)) {
      const img = document.createElement("img");
      img.src = import.meta.env.BASE_URL + "assets/roadmap-v2/" + id + ".png";
      img.width = 32;
      img.height = 40;
      img.alt = "";
      img.className = "hud-native-icon";
      return img;
    }
    const cropId = id.startsWith("seed-") ? id.slice(5) : id;
    if (cropId in crops) {
      const names = Object.keys(cropAtlas.frames);
      const index = names.indexOf(cropId + "-ready");
      const e = document.createElement("span");
      e.className = "crop-native-icon";
      e.style.backgroundImage = `url(${import.meta.env.BASE_URL}assets/roadmap-v2/crops.png)`;
      e.style.backgroundPosition = `-${(index % 12) * 40}px -${Math.floor(index / 12) * 44}px`;
      e.setAttribute("aria-hidden", "true");
      return e;
    }

    if (id === "jeju-postcard") {
      const img = document.createElement("img");
      img.src = import.meta.env.BASE_URL + "assets/farming/postcard.png";
      img.width = 64;
      img.height = 48;
      img.alt = "Bưu thiếp cảnh cầu Jeju được duyệt";
      img.style.imageRendering = "pixelated";
      return img;
    }
    if (id === "radish" || id === "scallion") {
      const e = document.createElement("span");
      e.className = "native-item";
      e.setAttribute("aria-hidden", "true");
      e.style.backgroundImage = `url(${import.meta.env.BASE_URL}assets/farming/crops.png)`;
      e.style.backgroundSize = "192px 40px";
      e.style.backgroundPosition = id === "radish" ? "-64px 0" : "-160px 0";
      return e;
    }

    const names = [
        "seed-pouch",
        "water-can",
        "water-can-pour",
        "sickle",
        "parcel",
        "tangerine",
        "coin",
        "basket",
      ],
      map: Record<string, string> = {
        seed: "seed-pouch",
        water: "water-can",
        harvest: "sickle",
        "seed-radish": "seed-pouch",
        "seed-scallion": "seed-pouch",
        radish: "sickle",
        scallion: "sickle",
        sprout: "seed-pouch",
      };
    const key = map[id] ?? id;
    const span = document.createElement("span");
    span.className = "native-item";
    span.setAttribute("aria-hidden", "true");
    span.style.backgroundImage = `url(${import.meta.env.BASE_URL}assets/farming/interaction-tools.png)`;
    span.style.backgroundPosition = `-${Math.max(0, names.indexOf(key)) * 32}px 0`;
    return span;
  }
  private render() {
    const answer = (document.activeElement as HTMLElement | null)?.dataset
      .answer;
    this.dialog.replaceChildren();
    this.dialog.dataset.view = this.mode;
    const heading = this.text(
      "h2",
      this.mode === "shop"
        ? "Cửa hàng Minseo · 민서의 가게"
        : this.mode === "inventory"
          ? "Túi đồ · 가방"
          : this.mode === "journal"
            ? "Nhật ký nhiệm vụ · 부탁"
            : `${(this.npcId && this.host.actorName?.(this.npcId)) || "Người bạn"} · chuyện nhỏ`,
    );
    heading.id = "quest-heading";
    const bar = document.createElement("div");
    bar.className = "quest-panel-heading";
    const close = this.button("×", () => this.close());
    close.id = "quest-close";
    close.setAttribute("aria-label", "Đóng và trở lại thế giới");
    bar.append(heading, close);
    const notice = this.text(
      "p",
      "Demo cục bộ · Nội dung tiếng Hàn chờ duyệt; không đồng bộ tiến độ website. Quảng cáo tắt.",
    );
    notice.className = "quest-demo";
    const status = this.text("p", this.manager.storageWarning || this.message);
    status.setAttribute("role", "status");
    this.dialog.append(bar, notice, status);
    if (this.manager.storageWarning) {
      this.dialog.append(
        this.button("Xuất bản lưu gốc", () => {
          const raw = this.manager.exportRawSave();
          if (!raw) return;
          const url = URL.createObjectURL(
            new Blob([raw], { type: "application/json" }),
          );
          const a = document.createElement("a");
          a.href = url;
          a.download = "pixel-town-local-recovery.json";
          a.click();
          setTimeout(() => URL.revokeObjectURL(url), 1000);
        }),
        this.button("Khôi phục backup trước nâng cấp", () => {
          this.message = this.manager.restoreMigrationBackup()
            ? "Đã phục hồi backup cục bộ; bản lỗi được lưu riêng."
            : "Không có backup hợp lệ; dữ liệu gốc vẫn nguyên.";
          this.render();
        }),
      );
    }

    const s = this.manager.snapshot();
    if (
      this.mode === "npc" &&
      this.npcId === SHOPKEEPER &&
      this.host !== this.exteriorHost
    ) {
      const b = this.button("Cửa hàng · 가게", () => {
        this.close();
        this.openShop(SHOPKEEPER);
      });
      b.dataset.interiorShop = SHOPKEEPER;
      this.dialog.append(b);
    }
    if (this.mode === "inventory") this.renderInventory();
    else if (this.mode === "shop") this.renderShop();
    else
      for (const q of quests.filter(
        (q) =>
          this.mode === "journal" ||
          q.giver === this.npcId ||
          q.recipient === this.npcId,
      )) {
        const box = document.createElement("section");
        box.className = "quest-card";
        box.dataset.quest = q.id;
        box.append(
          this.text("h3", `${q.title} · ${q.ko}`),
          this.text("p", this.objective(q)),
        );
        if (this.mode === "npc") this.renderNPC(box, q, s.records[q.id]);
        this.dialog.append(box);
      }
    if (this.dialog.open && answer !== undefined)
      this.dialog
        .querySelector<HTMLButtonElement>(`[data-answer="${answer}"]`)
        ?.focus();
    this.update();
  }
  private renderNPC(
    box: HTMLElement,
    q: QuestDefinition,
    r: ReturnType<QuestManager["snapshot"]>["records"][string] | undefined,
  ) {
    if (this.npcId === "npc-cheolsu" && q.id === "farm-first-seed-v1")
      box.append(
        this.button("Hạt dự phòng · một lần", () => {
          if (this.context()) {
            this.message = this.manager.recoverStarter()
              ? "Đã nhận một hạt dự phòng; chỉ cấp khi hết hạt và cây đang trồng."
              : "Chưa cần hoặc đã dùng hạt dự phòng.";
            this.render();
          }
        }),
      );
    if (
      q.prerequisite &&
      this.manager.snapshot().records[q.prerequisite]?.status !== "completed"
    ) {
      box.append(
        this.text(
          "p",
          "Mở sau: " + quests.find((x) => x.id === q.prerequisite)?.title,
        ),
      );
      return;
    }
    if (!r && this.npcId === q.giver)
      box.append(
        this.button("Nhận lời · 좋아요", () => {
          const c = this.context(),
            ok = c && this.manager.acceptInWorld(q.id, c.npcId, c);
          this.message = ok
            ? ["farm-first-seed-v1", "farm-radish-harvest-v1"].includes(q.id)
              ? "Hạt giống đã ở trong túi. Đến mép luống, chọn hạt và nhấn E để gieo."
              : "Đã nhận lời. Mình cùng khám phá nhé!"
            : "Túi chưa đủ chỗ hoặc cần đứng gần hơn.";
          this.render();
        }),
      );
    if (
      r?.status === "active" &&
      r.step === q.steps.length &&
      this.npcId === (q.recipient ?? q.giver)
    )
      box.append(
        this.button(
          q.recipient ? "Giao bưu kiện · 전달해요" : "Báo lại · 다 했어요",
          () => {
            const c = this.context();
            if (!c || !this.report(q, c)) {
              this.message = "Chưa đủ vật phẩm hoặc chưa gần người nhận.";
              this.render();
            }
          },
        ),
      );
    if (r?.status !== "challenge" || this.npcId !== (q.recipient ?? q.giver))
      return;
    const question = this.manager.question(q.id);
    if (!question) return;
    const prompt = this.text("p", question.prompt);
    prompt.dataset.question = question.id;
    prompt.lang = "vi";
    box.dataset.answerLanguage = "ko";
    box.dataset.learningDirection = question.direction;
    prompt.className = "korean-prompt";
    box.append(prompt);
    const answers = document.createElement("div");
    answers.className = "quest-answers";
    question.options.forEach((o, i) => {
      const b = this.button(`${i + 1}. ${o}`, () => {
        const c = this.context();
        if (!c) return;
        const result = this.manager.answerInWorld(q.id, question.id, i, c);
        this.message =
          result.result === "correct"
            ? `Đúng rồi! +${q.reward.coins} xu · +${q.reward.xp} XP trò chơi. ${result.explanation}`
            : result.result === "incorrect"
              ? `Chưa đúng. ${result.explanation} Mình thử câu khác nhé.`
              : this.manager.storageWarning ||
                "Chưa cấp thưởng. Kiểm tra chỗ trống trong túi hoặc vị trí.";
        if (result.result === "correct")
          this.host.feedback?.(
            "reward",
            this.host.player(),
            `+${q.reward.coins} xu`,
          );
        this.render();
      });
      b.dataset.answer = String(i);
      b.lang = "ko";
      answers.append(b);
    });
    box.append(answers);
    const label = this.text("label", "Hoặc nhập bằng Hangul · 한글로 답하세요");
    const input = document.createElement("input");
    input.type = "text";
    input.lang = "ko";
    input.maxLength = 160;
    input.autocomplete = "off";
    input.spellcheck = false;
    input.dataset.hangulInput = question.id;
    input.setAttribute("aria-label", "Nhập đáp án bằng tiếng Hàn");
    input.placeholder = "한글로 입력…";
    label.append(input);
    const submit = () => {
      const c = this.context();
      if (!c) return;
      const result = this.manager.answerTextInWorld(
        q.id,
        question.id,
        input.value,
        c,
      );
      this.message =
        result.result === "correct"
          ? `Đúng rồi! +${q.reward.coins} xu. ${result.explanation}`
          : result.result === "incorrect"
            ? `Chưa đúng. ${result.explanation} Thử câu Hangul cùng cấp nhé.`
            : result.explanation;
      this.render();
    };
    const typed = this.button("Trả lời bằng Hangul · 답하기", submit);
    typed.dataset.hangulSubmit = question.id;
    input.addEventListener("keydown", (e) => {
      if (e.isComposing || e.keyCode === 229) return;
      if (e.key === "Enter") {
        e.preventDefault();
        submit();
      }
    });
    box.append(label, typed);
  }
  private renderInventory() {
    const s = this.manager.snapshot(),
      grid = document.createElement("div");
    grid.className = "inventory-grid";
    grid.id = "quest-inventory-items";
    const tabs = document.createElement("div");
    tabs.className = "inventory-tabs";
    for (const [id, label] of [
      ["all", "Tất cả"],
      ["seeds", "Hạt"],
      ["crops", "Nông sản"],
      ["quest", "Nhiệm vụ"],
    ]) {
      const b = this.button(label, () => {
        this.inventoryCategory = id;
        this.render();
      });
      b.dataset.inventoryCategory = id;
      b.setAttribute("aria-pressed", String(this.inventoryCategory === id));
      tabs.append(b);
    }
    this.dialog.append(tabs);
    for (const [id, n] of Object.entries(s.inventory).filter(
      ([id, n]) =>
        n > 0 &&
        (this.inventoryCategory === "all" ||
          (this.inventoryCategory === "seeds" && id.startsWith("seed-")) ||
          (this.inventoryCategory === "crops" && id in crops) ||
          (this.inventoryCategory === "quest" &&
            !(id in crops) &&
            !id.startsWith("seed-"))),
    )) {
      const c = document.createElement("div");
      c.className = "inventory-item";
      c.append(this.icon(id), this.text("span", `${itemName(id)} × ${n}`));
      const crop = Object.entries(crops).find(([, v]) => v.seed === id);
      if (crop)
        c.append(
          this.button("Cầm hạt", () => {
            this.cropChoice = crop[0] as CropId;
            this.tool = "seed";
            this.close();
            this.toast("Đến mép luống rồi nhấn E hoặc chạm luống để gieo.");
          }),
        );
      grid.append(c);
    }
    if (!grid.children.length)
      grid.append(
        this.text("p", "Túi đang trống. Cheolsu có hạt hướng dẫn cho bạn."),
      );
    this.dialog.append(
      grid,
      this.text(
        "p",
        `${Object.values(s.inventory).filter((n) => n > 0).length}/${ECONOMY.slots} ô · ${s.coins} Town Coins`,
      ),
    );
  }
  private renderShop() {
    const s = this.manager.snapshot(),
      tabs = document.createElement("div");
    tabs.className = "shop-tabs";
    for (const tab of ["buy", "sell"] as const) {
      const b = this.button(
        tab === "buy" ? "Mua hạt / đồ lưu niệm" : "Bán nông sản",
        () => {
          this.shopTab = tab;
          this.render();
        },
      );
      b.dataset.shopTab = tab;
      b.setAttribute("aria-selected", String(this.shopTab === tab));
      tabs.append(b);
    }
    this.dialog.append(
      tabs,
      this.text(
        "p",
        `Ví: ${s.coins} Town Coins · Túi ${Object.values(s.inventory).filter((n) => n > 0).length}/${ECONOMY.slots} ô`,
      ),
    );
    const label = this.text("label", "Số lượng "),
      qty = document.createElement("input");
    qty.id = "shop-quantity";
    qty.type = "number";
    qty.min = "1";
    qty.max = "99";
    qty.value = String(this.quantity);
    qty.setAttribute("aria-label", "Số lượng mua bán");
    qty.oninput = () => {
      this.quantity = Number(qty.value);
    };
    label.append(qty);
    this.dialog.append(label);
    const list = document.createElement("div");
    list.id = "town-shop";
    for (const [id, item] of Object.entries(items).filter(([, i]) =>
      this.shopTab === "buy" ? i.buy > 0 : i.sell > 0,
    )) {
      const row = document.createElement("div");
      row.className = "shop-row";
      row.append(
        this.icon(id),
        this.text(
          "p",
          `${item.name} · ${item.ko}\n${this.shopTab === "buy" ? `${item.buy} xu · kho ${s.economy.stock[id] ?? 0}` : `${item.sell} xu mỗi món`} · đang có ${s.inventory[id] ?? 0}`,
        ),
      );
      const kind = this.shopTab,
        tx = `${kind}:${id}:${s.economy.revision}`;
      const b = this.button(kind === "buy" ? "Mua" : "Bán", () => {
        if (performance.now() - this.lastTradeAt < 300) return;
        this.lastTradeAt = performance.now();
        const c = this.context(),
          n = Number(qty.value),
          ok = c && this.manager.trade(kind, id, n, tx, c);
        this.message = ok
          ? `Đã ${kind === "buy" ? "mua" : "bán"} ${n} ${item.name}.`
          : !Number.isInteger(n) || n < 1 || n > 99
            ? "Chọn số lượng nguyên từ 1 đến 99."
            : kind === "buy" && s.coins < item.buy * n
              ? "Bạn chưa đủ Town Coins; xu và đồ vật vẫn nguyên vẹn."
              : kind === "buy" && (s.economy.stock[id] ?? 0) < n
                ? "Cửa hàng không đủ số lượng."
                : "Kiểm tra nông sản, chỗ trống trong túi hoặc khoảng cách tới cửa hàng.";
        this.render();
      });
      if (
        kind === "buy" &&
        id.startsWith("seed-") &&
        !cropUnlocked(id.slice(5), s.records)
      ) {
        b.disabled = true;
        b.textContent = "Khóa";
        row.append(this.text("small", cropUnlockHint(id.slice(5))));
      }
      b.dataset.trade = kind;
      b.dataset.item = id;
      row.append(b);
      list.append(row);
    }
    this.dialog.append(list);
  }
  objective(q: QuestDefinition) {
    const r = this.manager.snapshot().records[q.id];
    if (!r)
      return `Chưa nhận · gặp ${q.giver === "npc-harin" ? "Harin tại Jeju" : q.giver === "npc-minseo" ? "Minseo tại phố thương mại" : q.giver === "npc-nayeon" ? "Nayeon tại nông trại" : "Cheolsu tại nông trại"}.`;
    if (r.status === "completed")
      return "Hoàn thành · phần thưởng đã nhận một lần.";
    if (r.status === "challenge")
      return "Trả lời câu hỏi tiếng Hàn tại người bạn để nhận thưởng.";
    if (q.id === "town-first-delivery-v2")
      return (
        q.steps[r.step]?.label ??
        "Trở lại Jiho ở hiệu sách để giao và nhận câu hỏi."
      );
    if (q.recipient) return "Mang gói sách đến Jiho ở hiệu sách.";
    if (q.topic === "orchard") return `Thu quýt ${r.step}/3 rồi trở lại Harin.`;
    return (
      q.steps[r.step]?.label ??
      `Trở lại ${q.giver === "npc-nayeon" ? "Nayeon" : q.giver === "npc-minseo" ? "Minseo" : "Cheolsu"} để báo lại.`
    );
  }
  private equip(tool: FarmTool) {
    if (!this.host.canInteract()) return;
    this.tool = tool;
    if (tool === "seed") this.seedPicker();
    else this.picker.hidden = true;
    this.update();
  }
  private seedPicker() {
    this.picker.replaceChildren(
      this.text("p", "Chọn hạt; E / chạm luống để gieo"),
    );
    const s = this.manager.snapshot();
    for (const [id, crop] of Object.entries(crops)) {
      const b = this.button(
        `${crop.name} × ${s.inventory[crop.seed] ?? 0}`,
        () => {
          this.cropChoice = id as CropId;
          this.tool = "seed";
          this.picker.hidden = true;
          this.toast("Đã cầm hạt. E hoặc chạm luống để gieo.");
          this.update();
        },
      );
      b.dataset.seed = id;
      b.prepend(this.icon(crop.seed));
      b.disabled =
        !(s.inventory[crop.seed] > 0) || !cropUnlocked(id, s.records);
      if (!cropUnlocked(id, s.records))
        b.append(this.text("small", cropUnlockHint(id)));
      this.picker.append(b);
    }
    this.picker.hidden = false;
  }
  showHint(message: string) {
    this.toast(message);
  }
  private toast(message: string) {
    this.toastUntil = Date.now() + 3200;
    this.root.querySelector("#world-feedback")!.textContent = message;
  }
  update() {
    if (Date.now() > this.toastUntil)
      this.root.querySelector("#world-feedback")!.textContent = "";
    const s = this.manager.snapshot(),
      summary = quests
        .filter(
          (q) => s.records[q.id] && s.records[q.id].status !== "completed",
        )
        .slice(0, 2)
        .map((q) => this.objective(q))
        .join(" · "),
      key = JSON.stringify([
        s.coins,
        summary,
        this.tool,
        this.cropChoice,
        s.inventory,
      ]);
    if (key !== this.lastHUD) {
      this.lastHUD = key;
      this.root
        .querySelector("#town-coins")!
        .replaceChildren(
          this.icon("coin"),
          document.createTextNode(`${s.coins} xu`),
        );
      this.root.querySelector("#quest-tracker")!.textContent = summary;
      for (const b of this.root.querySelectorAll<HTMLButtonElement>(
        "[data-tool]",
      ))
        b.setAttribute("aria-pressed", String(b.dataset.tool === this.tool));
    }
    this.nearest = undefined;
    this.orchard = undefined;
    if (this.host.canInteract()) {
      const player = this.host.player();
      this.nearest = plots.find((p) =>
        nearGround(player, p.point, (x, y) => this.host.ground(x, y), 34),
      )?.id;
      for (const q of quests.filter((q) => q.topic === "orchard")) {
        const r = s.records[q.id];
        if (r?.status !== "active") continue;
        const collected =
            r.collected ?? q.steps.slice(0, r.step).map((s) => s.id),
          step = q.steps
            .filter((p) => !collected.includes(p.id))
            .sort(
              (a, b) =>
                Math.hypot(a.point[0] - player[0], a.point[1] - player[1]) -
                Math.hypot(b.point[0] - player[0], b.point[1] - player[1]),
            )
            .find((p) =>
              nearGround(player, p.point, (x, y) => this.host.ground(x, y), 30),
            );
        if (step) this.orchard = { id: q.id, step: step.id, point: step.point };
      }
    }
    this.root.querySelector<HTMLElement>("#farm-toolbelt")!.hidden =
      !this.nearest;
    if (!this.nearest) this.picker.hidden = true;
    const b = this.root.querySelector<HTMLButtonElement>(
      "#quest-world-action",
    )!;
    b.hidden = !this.nearest && !this.orchard;
    b.dataset.plotId = this.nearest ?? "";
    if (this.orchard) b.textContent = "E · Hái quýt · 귤 따기";
    else if (this.nearest) {
      const stage = plotPresentation(s.economy.plots[this.nearest], Date.now());
      b.textContent = `E · ${stage === "EMPTY" ? (s.economy.plots[this.nearest].stage === "empty" && s.economy.plots[this.nearest].lastHarvestedAt === undefined ? "Xới đất" : "Gieo hạt") : stage === "PLANTED" ? "Tưới cây" : stage === "READY" ? "Thu hoạch" : "Cây đang lớn"} · ${plots.find((p) => p.id === this.nearest)!.label}`;
    }
    for (const id of ["quest-journal", "quest-inventory"])
      this.root.querySelector<HTMLButtonElement>("#" + id)!.disabled =
        !this.dialog.open && !this.host.canInteract();
  }
  tapPlot(id: string) {
    const p = plots.find((p) => p.id === id);
    if (!p || !this.host.canInteract()) return false;
    if (
      !nearGround(
        this.host.player(),
        p.point,
        (x, y) => this.host.ground(x, y),
        34,
      )
    ) {
      this.toast("Đi tới mép luống để chăm cây nhé.");
      return false;
    }
    return this.performPlot(id);
  }
  tapOrchard(step: string) {
    if (!this.host.canInteract()) return false;
    const q = quests.find((q) => q.topic === "orchard")!,
      p = q.steps.find((p) => p.id === step);
    return !!p && this.collect(q.id, p.id, p.point);
  }
  tryWorldAction() {
    if (!this.host.canInteract()) return false;
    this.update();
    return this.orchard
      ? this.collect(this.orchard.id, this.orchard.step, this.orchard.point)
      : this.nearest
        ? this.performPlot(this.nearest)
        : false;
  }
  private collect(id: string, step: string, point: readonly [number, number]) {
    if (performance.now() - this.lastActionAt < 450) return true;
    const ok = this.manager.worldAction(id, step, this.host.player(), (x, y) =>
      this.host.ground(x, y),
    );
    if (ok) {
      this.lastActionAt = performance.now();
      this.host.feedback?.("collect", point, "+1 quýt");
      this.toast("Đã cho quýt vào túi.");
    }
    this.update();
    return ok;
  }
  private performPlot(id: string) {
    if (performance.now() - this.lastActionAt < 450) return true;
    const s = this.manager.snapshot(),
      p = s.economy.plots[id],
      def = plots.find((p) => p.id === id)!,
      stage = plotPresentation(p, Date.now());
    if (stage === "GROWING" || stage === "HARVESTED") {
      this.toast("Cây vẫn đang lớn. Bạn có thể khám phá rồi quay lại.");
      return true;
    }
    if (stage === "EMPTY" && !(s.inventory[crops[this.cropChoice].seed] > 0)) {
      this.seedPicker();
      this.toast("Cheolsu có hạt hướng dẫn miễn phí; chọn hạt trong túi.");
      return true;
    }
    const required: FarmTool =
      stage === "EMPTY" ? "seed" : stage === "PLANTED" ? "water" : "harvest";
    if (this.tool !== required) {
      this.tool = required;
      if (required === "seed") this.seedPicker();
      this.toast("Đã chọn dụng cụ phù hợp. E / chạm luống để thực hiện.");
      this.update();
      return true;
    }
    const action =
        stage === "EMPTY"
          ? p.stage === "empty" && p.lastHarvestedAt === undefined
            ? "till"
            : "plant"
          : stage === "PLANTED"
            ? "water"
            : "harvest",
      tx = `world:${id}:${p.cycle}:${action}:${s.economy.revision}`,
      ok = this.manager.farmAction(
        id,
        action,
        this.cropChoice,
        tx,
        this.host.player(),
        (x, y) => this.host.ground(x, y),
      );
    if (ok) {
      this.lastActionAt = performance.now();
      this.picker.hidden = true;
      this.tool =
        action === "plant" ? "water" : action === "water" ? "harvest" : "seed";
      const label =
        action === "till"
          ? "Đất đã xới · E để gieo hạt"
          : action === "plant"
            ? "Đã gieo hạt"
            : action === "water"
              ? "Đã tưới cây"
              : `+${p.crop ? crops[p.crop].yield : 0} ${p.crop ? crops[p.crop].name : "nông sản"}`;
      this.host.feedback?.(
        action === "till" ? "report" : action,
        def.root,
        label,
      );
      this.toast(label);
    } else
      this.toast(
        this.manager.storageWarning ||
          "Chưa thể thực hiện. Kiểm tra hạt, độ chín hoặc chỗ trống trong túi; không mất đồ.",
      );
    this.update();
    return true;
  }
  close() {
    if (!this.dialog.open) return;
    this.dialog.close();
    const id = this.npcId;
    this.npcId = undefined;
    if (id) this.host.onClose(id);
    this.release?.();
    this.release = undefined;
    this.update();
  }
  dispose() {
    this.close();
    if (this.followup) clearTimeout(this.followup);
    this.signal.abort();
    this.root.remove();
    this.dialog.remove();
  }
}
