import { NPCWorldClock } from "./clock";
import { resolveActivity, validateSchedules } from "./schedules";
import { privateReviewBuild, mountRightsReport } from "../rights/runtime";
import { chooseTarget } from "./interaction";
import { installNPCAudit } from "./audit";
import Phaser from "phaser";
import { npcRegistry as residentRegistry } from "./registry";
import { modernVisitors } from "./catalog";
import {
  runtimeNPCCatalog as npcRegistry,
  HistoryArtReview,
  productionHistoryCount,
  verifiedHistoricalClaimCount,
  applyHistorySelection,
} from "./history";
import "./history.css";
import { NPCVisitPolicy } from "./visits";
import { NPCAssetPool } from "./assets";
import { NPCActorModel } from "./actor";
import { NPCStateStore } from "./state";
import { NPCDialogueService } from "./dialogue";
import { clearInteractionLine } from "./navigation";
import type { Point } from "./types";
interface Host {
  player(): Point;
  ground(x: number, y: number): boolean;
  blocked(): boolean;
  canInteract(): boolean;
  lock(): () => void;
}
interface RenderActor {
  model: NPCActorModel;
  sprite: Phaser.GameObjects.Sprite;
  shadow: Phaser.GameObjects.Ellipse;
  elapsed: number;
  lastFrame: string;
}
const zones: Record<string, number[][]> = {
  palace: [[1060, 120, 1920, 1010]],
  modern: [[420, 2090, 1450, 670]],
  station: [[2230, 2090, 1160, 690]],
  jeju: [[3280, 3240, 910, 1380]],
  farm: [[300, 230, 760, 740]],
  "nature-leisure": [
    [360, 2790, 1440, 550],
    [2160, 2790, 980, 550],
  ],
  coast: [[330, 3360, 2700, 620]],
};
function rectDistance(p: Point, r: number[]) {
  return Math.hypot(
    Math.max(r[0] - p[0], 0, p[0] - r[0] - r[2]),
    Math.max(r[1] - p[1], 0, p[1] - r[1] - r[3]),
  );
}
export class NPCManager {
  private clock: NPCWorldClock;
  private timeLabel: HTMLOutputElement;
  private qaTools?: HTMLElement;
  private rightsDispose?: () => void;
  private archiveElapsed = 0;
  private lastArchive?: string;
  private lastTimeLabel = "";
  private archive?: HistoryArtReview;
  private auditDispose?: () => void;
  private assets: NPCAssetPool;
  private store: NPCStateStore;
  private visits: NPCVisitPolicy;
  private reviewId?: string;
  private models = new Map<string, NPCActorModel>();
  private actors = new Map<string, RenderActor>();
  private wanted = new Set<string>();
  private retry = new Map<string, number>();
  private dialogue: NPCDialogueService;
  private button: HTMLButtonElement;
  private target?: string;
  private closed = false;
  private now = 0;
  private lastPopulation = -999;
  private lastSave = 0;
  private activations = 0;
  private despawns = 0;
  private animationUpdates = 0;
  private simulationUpdates = 0;
  private bindings = new AbortController();
  constructor(
    private scene: Phaser.Scene,
    base: string,
    private host: Host,
  ) {
    this.assets = new NPCAssetPool(scene, base);
    let storage: Storage | undefined;
    try {
      storage = localStorage;
    } catch {
      /* Optional NPC persistence. */
    }
    this.clock = new NPCWorldClock(storage);
    validateSchedules(npcRegistry.npcs);
    this.timeLabel = document.createElement("output");
    this.timeLabel.id = "npc-life-time";
    this.timeLabel.setAttribute("aria-label", "Giờ trong game · 게임 시간");
    this.timeLabel.title = "Giờ mô phỏng, không phải giờ thực";
    document.querySelector("footer")?.append(this.timeLabel);
    this.visits = new NPCVisitPolicy(storage);
    const query = new URLSearchParams(location.search);
    this.rightsDispose = mountRightsReport();
    this.reviewId =
      privateReviewBuild && query.has("qa")
        ? (query.get("npcReview") ?? undefined)
        : undefined;
    if (privateReviewBuild && query.has("qa")) {
      this.qaTools = document.createElement("fieldset");
      this.qaTools.id = "npc-life-controls";
      this.qaTools.innerHTML =
        '<legend>QA · giờ mô phỏng</legend><label>Phút <input id="npc-life-minute" type="number" min="0" max="1439" value="540"></label><label>Tốc độ <select id="npc-life-rate"><option value="1">1×</option><option value="10">10×</option><option value="60">60×</option></select></label><button id="npc-life-apply">Đặt giờ QA</button>';
      document.querySelector("#settings > div")?.append(this.qaTools);
      this.qaTools
        .querySelector("button")!
        .addEventListener("click", () =>
          this.setReviewTime(
            Number(
              this.qaTools!.querySelector<HTMLInputElement>("input")!.value,
            ),
            Number(
              this.qaTools!.querySelector<HTMLSelectElement>("select")!.value,
            ),
          ),
        );
      window.__NPC_LIFE_QA__ = {
        setTime: (minute, rate = 1) => this.setReviewTime(minute, rate),
      };
    }
    this.archive = new HistoryArtReview(query, host, () => {
      this.lastPopulation = -999;
    });
    this.store = new NPCStateStore(storage, npcRegistry.npcs);
    for (const d of npcRegistry.npcs)
      this.models.set(d.id, new NPCActorModel(d, this.store.get(d.id)));
    this.button = document.createElement("button");
    this.button.id = "npc-interact";
    this.button.hidden = true;
    document.body.append(this.button);
    const signal = this.bindings.signal;
    this.button.addEventListener(
      "click",
      (e) => {
        e.stopPropagation();
        this.tryInteract();
      },
      { signal },
    );
    for (const event of ["pointerdown", "pointermove", "pointerup"] as const)
      this.button.addEventListener(event, (e) => e.stopPropagation(), {
        signal,
      });
    window.addEventListener(
      "pagehide",
      () => {
        this.store.save();
        this.saveLife();
      },
      { signal },
    );
    document.addEventListener(
      "visibilitychange",
      () => {
        this.saveLife();
        for (const a of this.actors.values()) a.elapsed = 0;
      },
      { signal },
    );
    if (new URLSearchParams(location.search).has("pixelAudit"))
      this.auditDispose = installNPCAudit(
        scene,
        () => this.snapshot(),
        () => [...this.actors.values()].map((a) => a.sprite),
      );
    this.dialogue = new NPCDialogueService({
      canOpen: () => host.canInteract(),
      lock: () => host.lock(),
      onOpen: (id) => {
        this.target = id;
        this.models.get(id)!.talk(host.player());
        this.button.hidden = true;
      },
      onClose: (id) => {
        this.models.get(id)?.finishTalk();
        this.store.save();
      },
      drawPreview: (canvas, id) => this.preview(canvas, id),
    });
  }
  private preview(canvas: HTMLCanvasElement, id: string) {
    const actor = this.actors.get(id),
      asset = this.assets.loaded.get(id);
    if (!actor || !asset) return;
    const context = canvas.getContext("2d")!;
    context.imageSmoothingEnabled = false;
    context.clearRect(0, 0, 96, 112);
    const f = asset.atlas.frames["greet-front-0"].frame;
    context.drawImage(asset.image, f.x, f.y, 96, 112, 0, 0, 96, 112);
  }
  tryInteract() {
    if (this.dialogue.target) return true;
    if (!this.host.canInteract()) return false;
    this.updateTarget();
    const def = this.target && npcRegistry.get(this.target);
    return !!def && this.dialogue.open(def);
  }
  private updateTarget() {
    if (this.dialogue.target) {
      this.target = this.dialogue.target;
      this.button.hidden = true;
      return;
    }
    const p = this.host.player();
    const candidates = this.host.canInteract()
      ? [...this.actors.values()]
          .filter(
            (a) =>
              a.sprite.visible &&
              Math.hypot(
                a.model.record.position[0] - p[0],
                a.model.record.position[1] - p[1],
              ) <= a.model.def.interactionRadius &&
              clearInteractionLine(p, a.model.record.position, (x, y) =>
                this.host.ground(x, y),
              ),
          )
          .map((a) => ({
            id: a.model.def.id,
            distance: Math.hypot(
              a.model.record.position[0] - p[0],
              a.model.record.position[1] - p[1],
            ),
          }))
      : [];
    this.target = chooseTarget(candidates, this.target);
    this.button.hidden = !this.target;
    if (this.target) {
      const m = this.models.get(this.target)!;
      this.button.textContent = `Trò chuyện · ${m.def.names.vi} · E${m.activity ? " · " + m.activity.label.vi + " / " + m.activity.label.ko : ""}`;
      this.button.dataset.npcId = this.target;
      m.greet(p);
    }
  }
  private populate() {
    const p = this.host.player();
    const pinned = this.dialogue.target;
    const activeZones = new Set(
      Object.keys(zones).filter((z) =>
        zones[z].some((r) => rectDistance(p, r) < 240),
      ),
    );
    this.archive?.setContext(activeZones);
    const living = this.visits.eligible(
      activeZones,
      pinned,
      this.reviewId,
      0,
      this.clock.minute,
      { seed: this.clock.seed, day: this.clock.day },
    );
    const selected = this.archive?.selected;
    const eligible = applyHistorySelection(living, selected, modernVisitors);
    const wanted = [...this.models.values()]
      .filter(
        (m) =>
          m.def.id === pinned ||
          (eligible.has(m.def.id) &&
            zones[m.def.homeZone].some((r) => rectDistance(p, r) < 240) &&
            Math.hypot(
              p[0] - m.record.position[0],
              p[1] - m.record.position[1],
            ) < 900),
      )
      .sort(
        (a, b) =>
          Number(b.def.id === pinned) - Number(a.def.id === pinned) ||
          Math.hypot(p[0] - a.record.position[0], p[1] - a.record.position[1]) -
            Math.hypot(
              p[0] - b.record.position[0],
              p[1] - b.record.position[1],
            ) ||
          a.def.id.localeCompare(b.def.id),
      )
      .slice(0, 4);
    this.wanted.clear();
    for (const m of wanted) this.wanted.add(m.def.id);
    if (this.dialogue.target) this.wanted.add(this.dialogue.target);
    for (const [id, a] of this.actors)
      if (!this.wanted.has(id)) {
        a.sprite.destroy();
        a.shadow.destroy();
        this.actors.delete(id);
        this.despawns++;
      }
    this.assets.cancelUnwanted(this.wanted);
    for (const m of wanted) {
      const id = m.def.id;
      if (
        this.actors.has(id) ||
        this.assets.pending.has(id) ||
        (this.retry.get(id) ?? 0) > this.now
      )
        continue;
      if (
        !this.assets.loaded.has(id) &&
        this.assets.pending.size >= this.assets.concurrency
      )
        continue;
      this.retry.set(id, this.now + 5000);
      void this.assets.load(m.def, this.wanted).then((ok) => {
        if (!ok || this.closed || !this.wanted.has(id) || this.actors.has(id))
          return;
        const p = m.record.position;
        const sprite = this.scene.add
          .sprite(
            Math.round(p[0]),
            Math.round(p[1]),
            m.def.assets.key,
            m.frame(),
          )
          .setOrigin(0.5, 100 / 112)
          .setDepth(Math.round(p[1]) + 0.05)
          .setData("npcId", id);
        const shadow = this.scene.add
          .ellipse(
            Math.round(p[0]),
            Math.round(p[1]) - 1,
            20,
            5,
            0x263b37,
            0.18,
          )
          .setDepth(Math.round(p[1]) - 0.01);
        this.actors.set(id, {
          model: m,
          sprite,
          shadow,
          elapsed: 0,
          lastFrame: "",
        });
        this.activations++;
      });
    }
  }
  update(delta: number) {
    if (this.closed) return;
    const dt = Math.max(0, Math.min(delta, 200));
    this.clock.tick(delta, this.host.blocked(), document.hidden);
    const selected = this.archive?.selected;
    if (selected !== this.lastArchive) {
      this.archiveElapsed = 0;
      this.lastArchive = selected;
    }
    if (selected && !this.host.blocked()) this.archiveElapsed += dt;
    const clock = this.clock.snapshot();
    for (const m of this.models.values())
      m.setActivity(resolveActivity(m.def, clock, this.archiveElapsed));
    const time = selected
      ? "Chuyện xưa · giờ riêng / 이야기 속 시간"
      : `${String(Math.floor(clock.minute / 60)).padStart(2, "0")}:${String(Math.floor(clock.minute % 60)).padStart(2, "0")} · giờ game`;
    if (time !== this.lastTimeLabel) {
      this.timeLabel.textContent = time;
      this.lastTimeLabel = time;
    }
    this.now += dt;
    if (this.now - this.lastPopulation >= 150) {
      this.lastPopulation = this.now;
      this.populate();
    }
    const p = this.host.player(),
      camera = this.scene.cameras.main.worldView;
    for (const a of this.actors.values()) {
      const pos = a.model.record.position;
      const visible =
        pos[0] >= camera.x - 80 &&
        pos[0] <= camera.right + 80 &&
        pos[1] >= camera.y - 20 &&
        pos[1] <= camera.bottom + 112;
      a.sprite.setVisible(visible);
      a.shadow.setVisible(visible);
      a.elapsed += dt;
      const interval = visible ? 50 : 250;
      if (a.elapsed >= interval) {
        if (!this.host.blocked() || this.dialogue.target === a.model.def.id) {
          const occupied = (n: Point) =>
            Math.hypot(n[0] - p[0], n[1] - p[1]) < 24 ||
            [...this.actors.values()].some(
              (b) =>
                b !== a &&
                Math.hypot(
                  n[0] - b.model.record.position[0],
                  n[1] - b.model.record.position[1],
                ) < 26,
            );
          a.model.step(
            Math.min(a.elapsed, 300),
            (x, y) => this.host.ground(x, y),
            occupied,
          );
          this.simulationUpdates++;
        }
        a.elapsed = 0;
      }
      const q = a.model.record.position;
      const frame = a.model.frame();
      a.sprite
        .setPosition(Math.round(q[0]), Math.round(q[1]))
        .setDepth(Math.round(q[1]) + 0.05);
      a.shadow
        .setPosition(Math.round(q[0]), Math.round(q[1]) - 1)
        .setDepth(Math.round(q[1]) - 0.01);
      if (visible && frame !== a.lastFrame) {
        a.sprite.setFrame(frame);
        a.lastFrame = frame;
        this.animationUpdates++;
      }
    }
    this.updateTarget();
    if (this.now - this.lastSave > 5000) {
      this.store.save();
      this.saveLife();
      this.lastSave = this.now;
    }
    window.__NPC_WORLD__ = this.snapshot();
  }
  private saveLife() {
    this.clock.save(
      Object.fromEntries(
        [...this.models.values()]
          .filter((m) => m.activity)
          .map((m) => [m.def.id, m.activity!.id]),
      ),
    );
  }
  private setReviewTime(minute: number, rate: number) {
    this.clock.setReviewTime(minute, rate);
    this.lastPopulation = -999;
    this.saveLife();
  }
  snapshot() {
    return {
      clock: this.clock.snapshot(),
      registered: residentRegistry.npcs.length, // Legacy resident API; actual total is explicit below.
      catalogTotal: npcRegistry.npcs.length,
      residentCount: residentRegistry.npcs.length,
      modernVisitorCount: modernVisitors.length,
      historicalArchiveCount: productionHistoryCount,
      historicalArtCandidateCount: 0, // All six approved by the human owner.
      approvedNPCCount: npcRegistry.npcs.length,
      verifiedHistoricalClaimCount,
      historySourceStatus: "PENDING / unverified factual material excluded",
      historyArtSelected: this.archive?.selected ?? null,
      active: this.actors.size,
      rendered: [...this.actors.values()].filter((a) => a.sprite.visible)
        .length,
      limit: 4,
      assets: this.assets.snapshot(),
      target: this.target ?? null,
      dialogue: this.dialogue.target ?? null,
      activations: this.activations,
      despawns: this.despawns,
      animationUpdates: this.animationUpdates,
      simulationUpdates: this.simulationUpdates,
      actors: [...this.actors.values()].map((a) => ({
        ...a.model.snapshot(),
        visible: a.sprite.visible,
        texture: a.sprite.texture.key,
        nativeScale: [a.sprite.scaleX, a.sprite.scaleY],
        sampling: a.sprite.frame.source.scaleMode,
      })),
      records: [...this.models.values()].map((m) => m.snapshot()),
      playerBlockingPolicy:
        "NPCs yield with soft contact; do not alter protected player collision",
      persistenceKey: "korean-arena-npc-world-v1",
    };
  }
  dispose() {
    if (this.closed) return;
    this.archive?.dispose();
    this.auditDispose?.();
    this.dialogue.dispose();
    this.closed = true;
    this.store.save();
    this.bindings.abort();
    for (const a of this.actors.values()) {
      a.sprite.destroy();
      a.shadow.destroy();
    }
    this.actors.clear();
    this.assets.close();
    this.saveLife();
    this.qaTools?.remove();
    this.rightsDispose?.();
    this.timeLabel.remove();
    delete window.__NPC_LIFE_QA__;
    this.button.remove();
    delete window.__NPC_WORLD__;
  }
}
declare global {
  interface Window {
    __NPC_WORLD__?: ReturnType<NPCManager["snapshot"]>;
    __NPC_LIFE_QA__?: { setTime(minute: number, rate?: number): void };
  }
}
