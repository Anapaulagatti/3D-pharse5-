import source from "../../assets-src/npcs/phase3a-final-six/definitions.json";
import dialogue from "../../assets-src/npcs/phase3a-final-six/dialogues.json";
import metadata from "../../assets-src/npcs/phase3a-final-six/metadata.json";
import { npcCatalog } from "./catalog";
import { NPCRegistry } from "./registry";
import {
  historicalIdentities,
  presentNPCIdentity,
  presentArchiveDialogue,
} from "./identity";
import { npcSchema, dialogueSchema } from "./types";

/** Human-approved26NPC development baseline. Facts/rights release status is
 * independent from artistic approval and actor availability. Same registry/FSM.
 */
const presented = source.npcs.map((definition) => {
  const identity = historicalIdentities.find(
    (row) => row.npcId === definition.id,
  );
  if (!identity) throw Error("Missing historical public identity mapping");
  return presentNPCIdentity(npcSchema.parse(definition), identity);
});
const archiveNodes = dialogue.nodes.map((node) => {
  const identity = historicalIdentities.find((row) => row.npcId === node.npcId);
  if (!identity) throw Error("Missing historical dialogue presentation");
  return presentArchiveDialogue(dialogueSchema.parse(node), identity);
});
export const historyArtCatalog = new NPCRegistry(
  [...npcCatalog.npcs, ...presented],
  [...npcCatalog.nodes.values(), ...archiveNodes],
);
export const historyCandidates = metadata; // Legacy name; all six are human-approved.
export const productionHistoryCount = presented.length; // Registry count, NOT commercial clearance.
export const verifiedHistoricalClaimCount = 0;
export function historyArtReviewEnabled(query: URLSearchParams) {
  return query.has("qa") && query.get("historyArtReview") === "1";
}
/** Historical URL parameters remain compatible; none can disable the approved roster. */
export function selectNPCCatalog(query: URLSearchParams) {
  void query;
  return historyArtCatalog;
}
export const runtimeNPCCatalog = historyArtCatalog;

/** Pure eligibility extension: exactly one reconstruction replaces its host role
 * slot; modern visitors sharing that slot are also suppressed during the review.
 * No moving actor is added as a hard collision solid.
 */
export function applyHistorySelection(
  eligible: ReadonlySet<string>,
  selected: string | undefined,
  hostVisitors: readonly { id: string; hostResidentId: string }[],
) {
  const result = new Set(eligible);
  const figure = historyCandidates.find((h) => h.id === selected);
  if (!figure) return result;
  result.delete(figure.hostResidentId);
  for (const v of hostVisitors)
    if (v.hostResidentId === figure.hostResidentId) result.delete(v.id);
  result.add(figure.id);
  return result;
}

/** Contextual approved archive selector. No historical claim or source is marked verified.
 * Existing living-world interactions and production schedules are unchanged.
 */
export class HistoryArtReview {
  selected?: string;
  readonly button: HTMLButtonElement;
  readonly dialog: HTMLDialogElement;
  private abort = new AbortController();
  private release?: () => void;
  constructor(
    query: URLSearchParams,
    private host: { lock(): () => void; canInteract(): boolean },
    private onSelect: () => void,
  ) {
    const requested = query.get("npcReview");
    this.selected = historyCandidates.find((h) => h.id === requested)?.id;
    this.button = document.createElement("button");
    this.button.id = "history-art-review";
    this.button.textContent = "Kho chuyện xưa · 옛 문화 이야기";
    this.dialog = document.createElement("dialog");
    this.dialog.id = "history-art-dialog";
    this.dialog.setAttribute("aria-label", "Kho chuyện xưa · nhân vật hư cấu");
    const title = document.createElement("h2");
    title.textContent = "옛 문화 이야기 · Kho chuyện xưa";
    const notice = document.createElement("p");
    notice.textContent =
      "Những người bạn trong mục này đều là nhân vật hư cấu, lấy cảm hứng từ các thời kỳ và nghề nghiệp văn hóa Hàn Quốc; họ không phải nhân vật lịch sử có thật. Câu chuyện và lời thoại được sáng tác cho game. Nội dung lịch sử chi tiết đang được kiểm chứng riêng. 이곳의 인물은 모두 게임 속 가상 인물이며 실제 역사 인물이 아닙니다.";
    this.dialog.append(title, notice);
    for (const h of historyCandidates) {
      const def = historyArtCatalog.get(h.id)!;
      const item = document.createElement("button");
      item.dataset.historyId = h.id;
      const identity = historicalIdentities.find((row) => row.npcId === h.id)!;
      item.textContent = `${def.names.vi} · ${def.names.ko} · ${identity.role.vi} / ${identity.role.ko} · ${identity.eraLabel}`;
      item.setAttribute(
        "aria-label",
        `${def.names.vi} · ${def.names.ko} · nhân vật hư cấu · 가상 인물`,
      );
      item.addEventListener("click", () => {
        this.selected = h.id;
        this.close();
        this.onSelect();
      });
      this.dialog.append(item);
    }
    const exit = document.createElement("button");
    exit.id = "history-art-return";
    exit.textContent = "Trở lại cư dân hiện tại";
    exit.addEventListener("click", () => {
      this.selected = undefined;
      this.close();
      this.onSelect();
    });
    const close = document.createElement("button");
    close.id = "history-art-close";
    close.textContent = "Đóng";
    close.addEventListener("click", () => this.close());
    this.dialog.append(exit, close);
    const signal = this.abort.signal;
    this.button.addEventListener(
      "click",
      () => {
        if (!this.host.canInteract()) return;
        this.release = this.host.lock();
        this.dialog.showModal();
      },
      { signal },
    );
    this.dialog.addEventListener("cancel", (e) => {
      e.preventDefault();
      this.close();
    });
    this.dialog.addEventListener(
      "close",
      () => {
        // The protected game canvas need not be focusable. Release our own
        // button's key-isolation before handing keys back to the existing game.
        const active = document.activeElement;
        if (
          active instanceof HTMLElement &&
          (active === this.button || this.dialog.contains(active))
        )
          active.blur();
        document.querySelector<HTMLCanvasElement>("#stage canvas")?.focus();
      },
      { signal },
    );
    for (const element of [this.button, this.dialog])
      for (const event of [
        "pointerdown",
        "pointermove",
        "pointerup",
        "keydown",
      ])
        element.addEventListener(event, (e) => e.stopPropagation(), { signal });
    document.body.append(this.button, this.dialog);
  }
  setContext(zones: ReadonlySet<string>) {
    const available = historyCandidates.filter((h) =>
      zones.has(historyArtCatalog.get(h.id)!.homeZone),
    );
    this.button.hidden = available.length === 0;
    for (const item of this.dialog.querySelectorAll<HTMLButtonElement>(
      "[data-history-id]",
    ))
      item.disabled = !available.some((h) => h.id === item.dataset.historyId);
    if (this.selected && !available.some((h) => h.id === this.selected))
      this.selected = undefined;
  }
  private close() {
    this.dialog.close();
    this.release?.();
    this.release = undefined;
  }
  dispose() {
    this.close();
    this.abort.abort();
    this.button.remove();
    this.dialog.remove();
  }
}
