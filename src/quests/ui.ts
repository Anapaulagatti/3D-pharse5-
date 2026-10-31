import { quests, itemNames, type QuestDefinition } from "./content";
import { QuestManager } from "./manager";
import "./style.css";
interface Host {
  player(): readonly [number, number];
  ground(x: number, y: number): boolean;
  canInteract(): boolean;
  lock(): () => void;
  onWorldAction?(): void;
  onOpen(id: string): void;
  onClose(id: string): void;
}
export class QuestUI {
  readonly manager: QuestManager;
  readonly root = document.createElement("section");
  private dialog = document.createElement("dialog");
  private release?: () => void;
  private npcId?: string;
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
        if (this.dialog.open && /^[1-4]$/.test(e.key)) {
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
  open(npcId?: string) {
    if (this.dialog.open || !this.host.canInteract()) return false;
    this.npcId = npcId;
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
        .map(([id, n]) => `${itemNames[id] ?? id}: ${n}`)
        .join(" · ") || "Túi đồ trống"
    }`;
    this.dialog.append(inventory);
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
                  : this.manager.storageWarning || result.explanation;
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
  objective(def: QuestDefinition) {
    const r = this.manager.snapshot().records[def.id];
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
    b.hidden = !this.action;
    if (this.action) b.textContent = `E · ${this.action.label}`;
    const journal =
      this.root.querySelector<HTMLButtonElement>("#quest-journal")!;
    journal.disabled = !this.dialog.open && !this.host.canInteract();
  }
  tryWorldAction() {
    if (!this.action || !this.host.canInteract()) return false;
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
