import type { NPCDefinition, DialogueNode } from "./types";
import { npcCatalog as npcRegistry } from "./catalog";
import "./style.css";
export interface DialogueHost {
  canOpen(): boolean;
  lock(): () => void;
  onOpen(id: string): void;
  onClose(id: string): void;
  drawPreview(canvas: HTMLCanvasElement, id: string): void;
}
export class NPCDialogueService {
  readonly dialog: HTMLDialogElement;
  private release?: () => void;
  private npc?: NPCDefinition;
  private node?: DialogueNode;
  private steps = 0;
  private bindings = new AbortController();
  constructor(private host: DialogueHost) {
    this.dialog = document.createElement("dialog");
    this.dialog.id = "npc-dialogue";
    this.dialog.setAttribute("aria-labelledby", "npc-dialogue-name");
    this.dialog.innerHTML =
      '<div class="npc-dialogue-header"><div><h2 id="npc-dialogue-name"></h2><p id="npc-dialogue-role"></p></div><button id="npc-dialogue-close" aria-label="Đóng hội thoại">×</button></div><div class="npc-conversation"><canvas id="npc-dialogue-preview" width="96" height="112" aria-label="Nhân vật đang trò chuyện"></canvas><div><p id="npc-dialogue-ko" lang="ko"></p><p id="npc-dialogue-vi" lang="vi"></p><p id="npc-dialogue-hint"></p></div></div><div id="npc-dialogue-choices"></div><div class="npc-dialogue-actions"><button id="npc-dialogue-next">Tiếp tục</button><button id="npc-dialogue-return">Tạm biệt</button></div>';
    document.body.append(this.dialog);
    const signal = this.bindings.signal;
    this.el("#npc-dialogue-close").addEventListener(
      "click",
      () => this.close(),
      { signal },
    );
    this.el("#npc-dialogue-return").addEventListener(
      "click",
      () => this.close(),
      { signal },
    );
    this.el("#npc-dialogue-next").addEventListener("click", () => this.next(), {
      signal,
    });
    this.dialog.addEventListener(
      "cancel",
      (e) => {
        e.preventDefault();
        this.close();
      },
      { signal },
    );
    this.dialog.addEventListener(
      "keydown",
      (e) => {
        e.stopPropagation();
        if (e.key === "Enter" && !(e.target instanceof HTMLButtonElement)) {
          e.preventDefault();
          this.next();
        }
      },
      { signal },
    );
    for (const event of [
      "pointerdown",
      "pointermove",
      "pointerup",
      "wheel",
    ] as const)
      this.dialog.addEventListener(event, (e) => e.stopPropagation(), {
        signal,
      });
  }
  private el<T extends HTMLElement = HTMLElement>(s: string) {
    return this.dialog.querySelector<T>(s)!;
  }
  open(npc: NPCDefinition) {
    if (this.npc || !this.host.canOpen()) return false;
    this.npc = npc;
    this.steps = 0;
    this.release = this.host.lock();
    this.host.onOpen(npc.id);
    this.show(npc.dialogueId);
    this.dialog.showModal();
    this.focusAction();
    return true;
  }
  private focusAction() {
    this.dialog
      .querySelector<HTMLButtonElement>(
        "[data-npc-choice], #npc-dialogue-next:not([hidden]), #npc-dialogue-return",
      )
      ?.focus();
  }
  private show(id: string) {
    if (++this.steps > 8) {
      this.close();
      return;
    }
    const node = npcRegistry.nodes.get(id);
    if (!node || node.npcId !== this.npc?.id) {
      this.close();
      return;
    }
    this.node = node;
    this.dialog.dataset.learningWords = String(node.hint.vi.includes(" = "));
    this.dialog.dataset.npcId = this.npc.id;
    this.dialog.dataset.nodeId = node.id;
    this.el("#npc-dialogue-name").textContent =
      this.npc.names.vi + " · " + this.npc.names.ko;
    this.el("#npc-dialogue-role").textContent = this.npc.occupation;
    this.el("#npc-dialogue-ko").textContent = node.content.ko;
    this.el("#npc-dialogue-vi").textContent = node.content.vi;
    this.el("#npc-dialogue-hint").textContent = node.hint.vi;
    this.el("#npc-dialogue-choices").replaceChildren();
    for (const choice of node.choices) {
      const b = document.createElement("button");
      b.textContent = choice.label.vi;
      b.dataset.npcChoice = choice.id;
      b.addEventListener("click", () => this.show(choice.next));
      this.el("#npc-dialogue-choices").append(b);
    }
    this.el<HTMLButtonElement>("#npc-dialogue-next").hidden = !node.next;
    this.host.drawPreview(
      this.el<HTMLCanvasElement>("#npc-dialogue-preview"),
      this.npc.id,
    );
    if (this.dialog.open) this.focusAction();
  }
  next() {
    if (this.node?.next) this.show(this.node.next);
    else if (this.node?.choices.length)
      this.el<HTMLButtonElement>("[data-npc-choice]").focus();
    else this.close();
  }
  close() {
    if (!this.npc) return;
    const id = this.npc.id;
    this.npc = undefined;
    this.node = undefined;
    this.dialog.close();
    this.host.onClose(id);
    this.release?.();
    this.release = undefined;
  }
  get target() {
    return this.npc?.id;
  }
  dispose() {
    this.close();
    this.bindings.abort();
    this.dialog.remove();
  }
}
