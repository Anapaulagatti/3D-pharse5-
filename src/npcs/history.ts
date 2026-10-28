import source from "../../assets-src/npcs/phase3a-final-six/definitions.json";
import dialogue from "../../assets-src/npcs/phase3a-final-six/dialogues.json";
import metadata from "../../assets-src/npcs/phase3a-final-six/metadata.json";
import { npcCatalog } from "./catalog";
import { NPCRegistry } from "./registry";

/** Original20 catalog and tests remain exact. Six real authored actor candidates
 * use the SAME registry/FSM/pool, but unverified history never unlocks production.
 */
export const historyArtCatalog = new NPCRegistry(
  [...npcCatalog.npcs, ...source.npcs],
  [...npcCatalog.nodes.values(), ...dialogue.nodes],
);
export const historyCandidates = metadata;
export const productionHistoryCount = 0;
export function historyArtReviewEnabled(query: URLSearchParams) {
  return query.has("qa") && query.get("historyArtReview") === "1";
}
export function selectNPCCatalog(query: URLSearchParams) {
  return historyArtReviewEnabled(query) ? historyArtCatalog : npcCatalog;
}
export const runtimeNPCCatalog = selectNPCCatalog(
  new URLSearchParams(typeof location === "undefined" ? "" : location.search),
);

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

/** QA-only art review selector. No historical claim or source is marked verified.
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
    this.button.textContent = "Lịch sử · Bản thử mỹ thuật";
    this.dialog = document.createElement("dialog");
    this.dialog.id = "history-art-dialog";
    this.dialog.setAttribute("aria-label", "Bản thử mỹ thuật lịch sử");
    const title = document.createElement("h2");
    title.textContent = "역사 이야기 · Bản thử mỹ thuật";
    const notice = document.createElement("p");
    notice.textContent =
      "Tư liệu lịch sử và trang phục chưa được kiểm chứng. Chỉ xem mỹ thuật và chuyển động; đây không phải lời nói thật của nhân vật. Các thời kỳ dưới đây là đề xuất của đề bài. Chọn nhân vật tại khu tương ứng; thư viện bằng chứng có lối vào thử cho cả sáu.";
    this.dialog.append(title, notice);
    for (const h of historyCandidates) {
      const def = historyArtCatalog.get(h.id)!;
      const item = document.createElement("button");
      item.dataset.historyId = h.id;
      item.textContent = `${def.names.vi} · ${def.names.ko} · ${h.era}`;
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
