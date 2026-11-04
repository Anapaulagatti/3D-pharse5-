import { InteriorScene } from "../interiors/InteriorScene";
import { interiors, readInterior } from "../interiors/registry";
import { moveReviewPlayer } from "./ReviewMovement";
import collisionAmendments from "./phase3bc-collision.json";
import { CollisionDebug } from "./CollisionDebug";
// PHASE3A BEGIN imports
import { NPCManager } from "../npcs/manager";
import { npcReviewSpawn } from "../npcs/review";
// PHASE3A END imports
import {
  WorldSessionCheckpoint,
  browserSessionCheckpointStorage,
  checkpointGroundIsWalkable,
} from "../platform/WorldSessionCheckpoint";
import { CharacterSession } from "../characters/session";
import { characterRegistry } from "../characters/registry";
import {
  CharacterPreferences,
  AppearancePreferences,
  browserPreferenceStorage,
} from "../characters/preferences";
import { PlayerCharacterManager } from "../characters/PlayerCharacterManager";
import { PhaserCharacterAssets } from "../characters/PhaserCharacterAssets";
import { CharacterSelection } from "../characters/CharacterSelection";
import type { RegistryMotion } from "../characters/RegistryMotion";
import "../characters/selection.css";
import { appearanceIsDefault } from "../characters/appearance";
import type { CharacterAppearance } from "../characters/appearanceTypes";
import { loadNativeContact, type ContactSpec } from "./NativeContact";
import Phaser from "phaser";
import { nativeCanvasOffset } from "./PixelGrid";
import { installPixelAudit } from "./PixelAudit";
import { Diagnostics } from "./Diagnostics";
import { JuniMotion, type JuniView } from "../engine/JuniMotion";
import { attachJoystick } from "../engine/Joystick";
import "../gate2/style.css";
import "./style.css";
import { FoundationCamera } from "./FoundationCamera";
import { movementFacing } from "./MovementFacing";
import { SessionMetrics } from "../gate2/SessionMetrics";
import { WorldCache } from "./WorldCache";
import type { Manifest } from "./types";
const production = document.documentElement.dataset.phase === "1";
const preferences = new CharacterPreferences(
  browserPreferenceStorage(),
  characterRegistry,
);
const appearances = new AppearancePreferences(
  browserPreferenceStorage(),
  characterRegistry,
);
const preference = preferences.read();
const characterSession = new CharacterSession(
  production ? preference : { characterId: "juni", needsSelection: false },
);
type State = {
  characterId: string;
  appearance: CharacterAppearance;
  characterAssets: ReturnType<PhaserCharacterAssets["snapshot"]>;
  playerSprites: number;
  visited: string[];
  renderer: string;
  ready: boolean;
  scene: string;
  x: number;
  y: number;
  frame: string;
  zoom: number;
  camera: ReturnType<FoundationCamera["snapshot"]>;
  chunks: ReturnType<WorldCache["pool"]["snapshot"]>;
  session: ReturnType<SessionMetrics["snapshot"]>;
  samplingMode: number;
  behind: string[];
  paused: boolean;
  textures: { key: string; width: number; height: number }[];
};
declare global {
  interface Window {
    __GATE3_PROFILE__?: {
      reset: () => void;
      layer: (mode: string) => void;
      snapshot: () => ReturnType<Diagnostics["snapshot"]>;
    };
    __GATE3__?: State;
    __GATE3_TEST__?: { walkable: (x: number, y: number) => boolean };
  }
}
const base = import.meta.env.BASE_URL,
  query = new URLSearchParams(location.search),
  native = query.has("native"),
  overview = query.has("overview");
// Approved world is explicit for normal play, reload and every legacy/direct review URL.
const id = "palace-cleanup-world";
const availableCatalog = [
  { id, label: "Korean Pixel Town · approved canonical world" },
];
const data: Manifest = await fetch(
  base + "assets/gate3/" + id + "/manifest.json",
).then((r) => {
  if (!r.ok) throw Error("Missing G3 manifest");
  return r.json();
});
if (id === "palace-cleanup-world") {
  for (const change of collisionAmendments.chunks) {
    const chunk = data.chunks.find((c) => c.id === change.id);
    if (!chunk || chunk.mask !== change.originalMask)
      throw Error("Collision amendment predecessor mismatch");
    chunk.mask = change.mask;
  }
}
const nativeContact = await loadNativeContact(
  (data as Manifest & { contactCollision?: ContactSpec }).contactCollision,
  base,
);
// Diagnostic stress profile only; normal review uses the manifest64MiB budget.
if (query.has("stress")) data.budgetBytes = 24 * 1024 * 1024;
// Versioned QA approach correction: immutable masterplan/target coordinates are retained.
const entries: Record<string, number[]> = { ...data.reviewEntries };
if (query.has("qa"))
  for (const key of [
    "palace-west",
    "jeju-arrival",
    "bridge-island",
    "jeju-landing",
  ]) {
    const aliases: Record<string, number[]> = {
      "palace-west": [1837, 1090],
      "jeju-arrival": [3500, 3633],
      "bridge-island": [3500, 3633],
      "jeju-landing": [3188, 3999],
    };
    entries[key] = aliases[key];
  }
if (entries[query.get("entry") ?? ""])
  data.spawn = entries[query.get("entry")!];
// PHASE3A BEGIN qa-entry
const npcEntry =
  production && id === "palace-cleanup-world"
    ? npcReviewSpawn(query)
    : undefined;
if (npcEntry) data.spawn = npcEntry;
// PHASE3A END qa-entry
// Resume only an actual browser reload. Explicit review-entry navigation keeps its declared spawn.
const worldCheckpoint = production
  ? new WorldSessionCheckpoint(
      browserSessionCheckpointStorage(),
      location.pathname + location.search,
      data,
    )
  : null;
let reloadState =
  (
    performance.getEntriesByType("navigation")[0] as
      PerformanceNavigationTiming | undefined
  )?.type === "reload"
    ? (worldCheckpoint?.read() ?? null)
    : null;
if (
  reloadState &&
  !(await checkpointGroundIsWalkable(data, reloadState.x, reloadState.y, base))
)
  reloadState = null;
let interiorResume =
  production &&
  (
    performance.getEntriesByType("navigation")[0] as
      PerformanceNavigationTiming | undefined
  )?.type === "reload"
    ? readInterior()
    : undefined;
if (interiorResume) {
  if (await checkpointGroundIsWalkable(data, ...interiorResume.world, base)) {
    data.spawn = interiorResume.world;
    if (reloadState)
      reloadState = {
        ...reloadState,
        x: interiorResume.world[0],
        y: interiorResume.world[1],
      };
  } else interiorResume = undefined;
}
const label = "Korean Pixel Town · canonical world / local gameplay review";
const root = document.querySelector<HTMLDivElement>("#app")!;
root.innerHTML = `<header><b>KOREAN ARENA</b><select id="scene-picker" aria-label="Review environment">${availableCatalog.map((s) => `<option value="${s.id}" ${s.id === id ? "selected" : ""}>${s.label}</option>`).join("")}</select><span id="camera-mode">Follow · native1:1</span><button id="scenic">Scenic</button><details id="settings"><summary aria-label="Options">···</summary><div>${production ? '<button id="character-open">Character Studio</button><button id="celebrate-desktop">Ăn mừng · C</button>' : ""}<label><input type="checkbox" id="showcases"> Landmark moments</label><button id="pause">Pause</button><button id="export-session">Export test report</button></div></details></header><main id="stage"></main><div id="map-labels" aria-hidden="true"></div><div id="camera-tools"><span>Drag to look · pinch to zoom</span><button id="start-tour">Start Tour</button><span id="tour-caption" role="status" aria-live="polite"></span><button id="tour-pause">Pause</button><button id="tour-next">Skip landmark</button><button id="overview-mode">Full scene</button><button id="return-juni">Return to Juni</button></div><button id="tour-controls" aria-controls="camera-tools" aria-expanded="true">Tour controls</button><footer><span id="near">${label}</span><span>WASD / arrows · Shift run · E explore · Space greet${production ? " · C celebrate" : ""}</span></footer><div id="joystick" aria-label="Movement joystick"><span class="stick-knob"></span></div><div id="touch-actions"><button id="run">Run</button><button id="explore">Explore</button>${production ? '<button id="wave-emote">Chào</button><button id="celebrate-emote">Vui</button>' : ""}</div><aside id="dialog" hidden role="dialog" aria-label="Environment detail"><h2 id="title"></h2><p id="copy"></p><button id="close">Return</button></aside>`;
if (production)
  document.querySelector<HTMLElement>("#scene-picker")!.hidden = true;
document.querySelector<HTMLSelectElement>("#scene-picker")!.onchange = (e) => {
  location.search =
    "?scene=" +
    (e.target as HTMLSelectElement).value +
    (query.has("worldOnly")
      ? "&worldOnly"
      : query.has("pilotsOnly")
        ? "&pilotsOnly"
        : "");
};
if (native) document.body.dataset.native = "true";
let scenicLocked = false;
let paused = false,
  heldRun = false,
  analog = { x: 0, y: 0 };
const reset = attachJoystick(
  document.querySelector<HTMLElement>("#joystick")!,
  (x, y) => {
    analog = { x, y };
  },
  () =>
    (paused && document.body.dataset.interior !== "true") ||
    scenicLocked ||
    !!document.querySelector<HTMLDialogElement>("#quest-dialogue")?.open,
);
class Slice extends Phaser.Scene {
  // PHASE3A BEGIN field
  private npcs?: NPCManager;
  private enteringInterior = false;
  private interiorReturnUntil = 0;
  private interiorRestored = false;
  private doorHint?: HTMLButtonElement;
  private collisionDebug?: CollisionDebug;
  // PHASE3A END field
  private reviewCamera!: FoundationCamera;
  private worldCache!: WorldCache;
  private overviewImage!: Phaser.GameObjects.Image;
  private diagnostics = query.has("profile") ? new Diagnostics() : undefined;
  private sessionMetrics = new SessionMetrics();
  private lastUpdateTime = performance.now();
  private lastMetrics = 0;
  private metrics = this.sessionMetrics.snapshot();
  private textureGeneration = -1;
  private textureInfo: State["textures"] = [];
  private legacy = query.has("baseline");
  private player!: Phaser.GameObjects.Sprite;
  private motion: JuniMotion | RegistryMotion = new JuniMotion();
  private characters?: PlayerCharacterManager<Phaser.GameObjects.Sprite>;
  private selection?: CharacterSelection;
  private characterAssets!: PhaserCharacterAssets;
  private selectionBindings?: AbortController;
  private x = 0;
  private y = 0;
  private facing: JuniView = "front";
  private keys!: Record<string, Phaser.Input.Keyboard.Key>;
  private visited = new Set<string>();
  preload() {
    this.load.atlas(
      "farm-crops",
      base + "assets/roadmap-v2/crops.png",
      base + "assets/roadmap-v2/crops.json",
    );
    this.load.atlas(
      "world-actions",
      base + "assets/farming/interaction-tools.png",
      base + "assets/farming/interaction-tools.json",
    );
    this.load.atlas(
      "farm-materials",
      base + "assets/farming/phase3bd-final-quality/soil-components.png",
      base + "assets/farming/phase3bd-final-quality/soil-components.json",
    );
    this.load.atlas(
      "town-props",
      base + "assets/roadmap-v2/props.png",
      base + "assets/roadmap-v2/props.json",
    );
    const selected = characterSession.selected;
    if (!this.textures.exists(selected.assets!.key))
      this.load.atlas(
        selected.assets!.key,
        base + selected.assets!.texture,
        base + selected.assets!.atlas,
      );
    this.load.image("overview", base + data.overview);
  }
  walkable(x: number, y: number) {
    return this.worldCache.walkable(x, y);
  }
  create() {
    this.worldCache = new WorldCache(this, data, base, this.diagnostics);
    if (query.has("collisionDebug"))
      this.collisionDebug = new CollisionDebug(
        this,
        nativeContact?.spec,
        [
          ...Object.values(data.reviewEntries ?? {}),
          ...data.targets.map((t) => [t.x, t.y] as const),
        ],
        data.logicalSolids ?? [],
      );
    this.events.once("shutdown", () => this.collisionDebug?.dispose());
    if (this.diagnostics) {
      this.diagnostics.attach(this);
      window.__GATE3_PROFILE__ = {
        reset: () => this.diagnostics!.reset(),
        layer: (mode) => this.diagnostics!.layer(mode),
        snapshot: () => this.diagnostics!.snapshot(),
      };
    }
    this.overviewImage = this.add
      .image(0, 0, "overview")
      .setOrigin(0)
      .setDisplaySize(data.size[0], data.size[1])
      .setDepth(-101)
      .setVisible(false);
    [this.x, this.y] = reloadState
      ? [reloadState.x, reloadState.y]
      : data.spawn;
    this.visited = new Set(reloadState?.visited ?? []);
    // Initial movement waits for native chunk + local foreground + collision readiness.
    this.characterAssets = new PhaserCharacterAssets(this, base);
    this.characters = new PlayerCharacterManager(
      this.characterAssets,
      (def, position) =>
        this.add
          .sprite(
            position.x,
            position.y,
            def.assets!.key,
            def.animations["idle-front"].frames[0],
          )
          .setOrigin(
            def.native.anchor[0] / def.native.width,
            def.native.anchor[1] / def.native.height,
          )
          .setDepth(position.y + 0.1)
          .setData("playerCharacter", def.id),
      preferences,
      characterSession.selected,
      { x: this.x, y: this.y },
      characterRegistry,
      production ? appearances : undefined,
    );
    this.player = this.characters.sprite;
    this.motion = this.characters.motion;
    this.keys = this.input.keyboard!.addKeys(
      "W,A,S,D,UP,DOWN,LEFT,RIGHT,SHIFT,E,SPACE",
    ) as typeof this.keys;
    this.input.keyboard!.addCapture(["SPACE", "UP", "DOWN", "LEFT", "RIGHT"]);
    this.input.keyboard!.on("keydown-E", (event: KeyboardEvent) => {
      if (!event.repeat) this.inspect();
    });
    this.input.keyboard!.on("keydown-SPACE", () => this.motion.gesture("wave"));
    this.input.keyboard!.on("keydown-C", () => {
      if (production && !paused) this.motion.gesture("celebrate");
    });
    this.reviewCamera = new FoundationCamera(
      this,
      data.size,
      data.targets,
      id,
      (on) => {
        scenicLocked = on;
        reset();
        heldRun = false;
      },
      native,
      overview,
      this.x,
      this.y,
      async () => {},
      data.stops,
    );
    if (native) {
      const centres: Record<string, [number, number]> = data.nativeFrames ?? {
        station: [2598.5, 2460],
        bakery: [1814, 3500],
        retail: [1128, 2360],
        convenience: [640, 2910],
      };
      const centre =
        centres[query.get("entry") ?? "station"] ?? centres.station;
      this.reviewCamera.frameNative(...centre);
    }
    if (production) {
      this.selectionBindings = new AbortController();
      const signal = this.selectionBindings.signal;
      window.addEventListener(
        "pagehide",
        () => worldCheckpoint?.save(this.x, this.y, this.visited),
        { signal },
      );
      let previousPause = false;
      this.selection = new CharacterSelection(
        {
          current: () => this.characters!.selected.id,
          appearance: () => this.characters!.appearance,
          canOpen: () =>
            !this.characters!.busy && this.reviewCamera.mode === "follow",
          lock: () => {
            previousPause = paused;
            paused = true;
            reset();
            heldRun = false;
            this.input.keyboard!.enabled = false;
            this.input.keyboard!.removeCapture([
              "SPACE",
              "UP",
              "DOWN",
              "LEFT",
              "RIGHT",
            ]);
          },
          unlock: () => {
            paused = previousPause;
            this.input.keyboard!.resetKeys();
            this.input.keyboard!.enabled = true;
            this.input.keyboard!.addCapture([
              "SPACE",
              "UP",
              "DOWN",
              "LEFT",
              "RIGHT",
            ]);
            reset();
            heldRun = false;
          },
          confirm: async (characterId, appearance, presetName) => {
            const result = await this.characters!.select(
              characterId,
              {
                x: this.x,
                y: this.y,
              },
              appearance,
              presetName,
            );
            characterSession.commit(result.characterId);
            this.player = this.characters!.sprite;
            this.motion = this.characters!.motion;
            return result;
          },
        },
        base,
        appearances,
      );
      document.querySelector("#character-open")!.addEventListener(
        "click",
        () => {
          if (!this.selection!.open())
            document.querySelector("#near")!.textContent =
              "Trở về chế độ theo nhân vật trước khi đổi người đồng hành.";
        },
        { signal },
      );
      document.querySelector("#wave-emote")!.addEventListener(
        "click",
        () => {
          if (!paused) this.motion.gesture("wave");
        },
        { signal },
      );
      document.querySelector("#celebrate-emote")!.addEventListener(
        "click",
        () => {
          if (!paused) this.motion.gesture("celebrate");
        },
        { signal },
      );
      document.querySelector("#celebrate-desktop")!.addEventListener(
        "click",
        () => {
          if (!paused) this.motion.gesture("celebrate");
        },
        { signal },
      );
      if (characterSession.needsSelection) this.selection.open(true);
      else {
        const savedAppearance = appearances.read(this.characters.selected.id);
        if (!appearanceIsDefault(savedAppearance)) {
          const beforeRestorePause = paused;
          paused = true;
          this.player.setVisible(false);
          void this.characters
            .select(
              this.characters.selected.id,
              { x: this.x, y: this.y },
              savedAppearance,
            )
            .then(() => {
              this.player = this.characters!.sprite;
              this.motion = this.characters!.motion;
            })
            .catch(() => {
              document.querySelector("#near")!.textContent =
                "Chưa tải được ngoại hình đã lưu; bản nguyên gốc vẫn sẵn sàng.";
            })
            .finally(() => {
              if (this.scene.isActive()) {
                this.player.setVisible(true);
                paused = beforeRestorePause;
              }
            });
        }
      }
    }
    // PHASE3A BEGIN create
    if (production && id === "palace-cleanup-world")
      this.npcs = new NPCManager(this, base, {
        player: () => [this.x, this.y],
        onQuestAction: (kind) => {
          if (kind === "reward") this.motion.gesture("celebrate");
        },
        view: () => this.facing,
        ground: (x, y) => this.walkable(x, y),
        blocked: () => paused || scenicLocked || document.hidden,
        canInteract: () =>
          !paused &&
          !scenicLocked &&
          !this.characters!.busy &&
          this.reviewCamera.mode === "follow",
        lock: () => {
          const wasPaused = paused;
          paused = true;
          reset();
          heldRun = false;
          this.input.keyboard!.resetKeys();
          return () => {
            paused = wasPaused;
            this.input.keyboard!.resetKeys();
            reset();
            heldRun = false;
          };
        },
      });
    this.doorHint = document.createElement("button");
    this.doorHint.id = "interior-door";
    this.doorHint.hidden = true;
    this.doorHint.onclick = () => void this.enterInterior();
    document.body.append(this.doorHint);
    this.events.once("shutdown", () => {
      this.npcs?.dispose();
      this.doorHint?.remove();
    });
    // PHASE3A END create
    this.events.once("shutdown", () => {
      this.selectionBindings?.abort();
      this.characters?.setTransitioning(true);
      this.selection?.dispose();
      this.characters?.dispose();
    });
    document
      .querySelector("#joystick")!
      .addEventListener("pointerdown", () => this.reviewCamera.interruptTour());
    window.__GATE3_TEST__ = { walkable: (x, y) => this.walkable(x, y) };
    if (query.has("pixelAudit")) installPixelAudit(this);
    document
      .querySelector("#explore")!
      .addEventListener("click", () => this.inspect());
  }
  private nearDoor() {
    return interiors.find(
      (r) =>
        Math.hypot(this.x - r.door[0], this.y - r.door[1]) < 36 &&
        this.walkable(this.x, this.y),
    );
  }
  private async enterInterior() {
    const r = this.nearDoor();
    if (
      !r ||
      !this.npcs ||
      paused ||
      scenicLocked ||
      this.enteringInterior ||
      performance.now() < this.interiorReturnUntil ||
      this.characters!.busy
    )
      return;
    this.enteringInterior = true;
    if (this.doorHint) this.doorHint.hidden = true;
    paused = true;
    reset();
    heldRun = false;
    this.input.keyboard!.resetKeys();
    this.sys.pause();
    try {
      const npc = await this.npcs.borrowInteriorActor(r.npc);
      if (!this.scene.isPaused()) throw Error("World changed");
      this.scene.launch("town-interior", {
        definition: r,
        player: this.player,
        motion: this.motion,
        owner: this,
        world: [this.x, this.y],
        quest: this.npcs.questUI,
        npc,
        analog: () => ({ ...analog, run: heldRun }),
        resume:
          interiorResume?.id === r.id && !this.interiorRestored
            ? interiorResume
            : undefined,
        onExit: () => {
          this.interiorRestored = true;
          this.interiorReturnUntil = performance.now() + 400;
          this.sys.resume();
          paused = false;
          this.enteringInterior = false;
          this.input.keyboard!.resetKeys();
          reset();
          heldRun = false;
        },
      });
    } catch (error) {
      console.warn("Interior load deferred", String(error));
      this.sys.resume();
      this.enteringInterior = false;
      paused = false;
      this.npcs.showHint(
        "Chưa tải được phòng; bạn vẫn ở cửa an toàn. Thử lại nhé.",
      );
    }
  }
  inspect() {
    if (paused || scenicLocked || performance.now() < this.interiorReturnUntil)
      return;
    if (this.nearDoor()) {
      void this.enterInterior();
      return;
    }
    // PHASE3A BEGIN interaction
    if (this.npcs?.tryInteract()) return;
    // PHASE3A END interaction
    const nearest = [...data.targets].sort(
      (a, b) =>
        Math.hypot(a.x - this.x, a.y - this.y) -
        Math.hypot(b.x - this.x, b.y - this.y),
    )[0];
    const close =
      nearest && Math.hypot(nearest.x - this.x, nearest.y - this.y) < 120;
    if (production) {
      if (close) this.visited.add(nearest.id);
      this.npcs?.showHint(
        close
          ? nearest.label
          : "Đến gần một người bạn hoặc luống cây rồi nhấn E / chạm để tương tác.",
      );
      return;
    }
    document.querySelector("#title")!.textContent = close
      ? nearest.label
      : label;
    document.querySelector("#copy")!.textContent = close
      ? "Explore the architecture, materials and routes at Juni’s original scale."
      : "Walk toward an entrance or destination, then explore.";
    if (close) this.visited.add(nearest.id);
    document.querySelector<HTMLElement>("#dialog")!.hidden = false;
    paused = true;
    reset();
  }
  update(_t: number, delta: number) {
    if (!this.player) return;
    const door = this.nearDoor();
    if (this.doorHint) {
      this.doorHint.hidden = !door || paused || scenicLocked;
      this.doorHint.textContent = door ? "E · Vào " + door.name : "";
    }
    if (
      interiorResume &&
      !this.interiorRestored &&
      !this.enteringInterior &&
      door &&
      this.walkable(this.x, this.y) &&
      !paused
    ) {
      void this.enterInterior();
      return;
    }

    const updateStarted = performance.now();
    const collisionStarted = performance.now();
    let dx =
        Number(this.keys.D.isDown || this.keys.RIGHT.isDown) -
        Number(this.keys.A.isDown || this.keys.LEFT.isDown) +
        analog.x,
      dy =
        Number(this.keys.S.isDown || this.keys.DOWN.isDown) -
        Number(this.keys.W.isDown || this.keys.UP.isDown) +
        analog.y;
    if (Math.hypot(dx, dy) > 0.01) this.reviewCamera.interruptTour();
    if (paused || scenicLocked || document.hidden) {
      dx = 0;
      dy = 0;
    }
    const n = Math.max(1, Math.hypot(dx, dy));
    dx /= n;
    dy /= n;
    const running = heldRun || this.keys.SHIFT.isDown,
      speed = running ? 100 : 60,
      step = (Math.min(delta, 50) * speed) / 1000,
      oldX = this.x,
      oldY = this.y;
    const contactFacing = movementFacing(dx, dy, this.facing);
    const contactAllows = (x: number, y: number) =>
      !nativeContact ||
      nativeContact.allows(x, y, running ? "run" : "walk", contactFacing);
    const moved = moveReviewPlayer(
      this.x,
      this.y,
      dx,
      dy,
      step,
      (x, y) => this.walkable(x, y) && contactAllows(x, y),
    );
    this.x = moved.x;
    this.y = moved.y;
    this.diagnostics?.sample(
      "update.inputCollision",
      performance.now() - collisionStarted,
    );
    const distance = Math.hypot(this.x - oldX, this.y - oldY);
    if (distance > 0.01)
      this.facing = moved.assisted
        ? contactFacing
        : movementFacing(this.x - oldX, this.y - oldY, this.facing);
    const frame = this.motion.step(
      delta,
      distance,
      distance > 0.01,
      running,
      this.facing,
      matchMedia("(prefers-reduced-motion: reduce)").matches,
      paused,
    );
    this.player
      .setPosition(Math.round(this.x), Math.round(this.y))
      .setFrame(frame)
      .setDepth(Math.round(this.y) + 0.1);
    const cameraStarted = performance.now();
    this.reviewCamera.update(
      delta,
      this.x,
      this.y,
      this.x - oldX,
      this.y - oldY,
      paused,
    );
    this.diagnostics?.sample(
      "update.camera",
      performance.now() - cameraStarted,
    );
    const cacheStarted = performance.now();
    const isOverview = this.reviewCamera.mode === "overview";
    this.overviewImage.setVisible(isOverview);
    const cameraSnapshot = this.reviewCamera.snapshot();
    this.worldCache.update(
      cameraSnapshot.worldView as [number, number, number, number],
      this.x,
      this.y,
      isOverview,
    );
    this.diagnostics?.sample("update.cache", performance.now() - cacheStarted);
    // PHASE3A BEGIN update
    this.npcs?.update(delta);
    this.collisionDebug?.update(
      delta,
      this.x,
      this.y,
      (x, y) => this.walkable(x, y),
      frame,
    );
    // PHASE3A END update
    const behind = data.objects
      .filter(
        (o) =>
          this.x > o.x - 30 &&
          this.x < o.x + o.width + 30 &&
          this.y < o.sortY &&
          this.y > o.y,
      )
      .map((o) => o.id);
    const now = performance.now();
    this.sessionMetrics.add(now - this.lastUpdateTime);
    this.diagnostics?.sample("frame.interval", now - this.lastUpdateTime);
    this.lastUpdateTime = now;
    const stats = this.worldCache.pool.snapshot(),
      generation = stats.loads + stats.evictions;
    if (this.legacy || generation !== this.textureGeneration) {
      this.textureGeneration = generation;
      this.textureInfo = this.textures.getTextureKeys().map((key) => {
        const t = this.textures.get(key).getSourceImage() as HTMLImageElement;
        return { key, width: t.width, height: t.height };
      });
    }
    if (this.legacy || now - this.lastMetrics > 100) {
      this.lastMetrics = now;
      this.metrics = this.sessionMetrics.snapshot();
    }
    window.__GATE3__ = {
      characterId: this.characters!.selected.id,
      appearance: this.characters!.appearance,
      characterAssets: this.characterAssets.snapshot(),
      playerSprites: this.children.list.filter(
        (o) =>
          o instanceof Phaser.GameObjects.Sprite &&
          !!o.getData("playerCharacter"),
      ).length,
      visited: [...this.visited],
      renderer: this.game.renderer.type === Phaser.WEBGL ? "WebGL" : "Canvas",
      ready: this.walkable(this.x, this.y) && !this.characters!.busy,
      scene: id,
      x: this.x,
      y: this.y,
      frame,
      zoom: this.cameras.main.zoom,
      camera: cameraSnapshot,
      chunks: stats,
      session: this.metrics,
      behind,
      paused,
      samplingMode: this.player.frame.source.scaleMode,
      textures: this.textureInfo,
    };
    const near = [...data.targets].sort(
      (a, b) =>
        Math.hypot(a.x - this.x, a.y - this.y) -
        Math.hypot(b.x - this.x, b.y - this.y),
    )[0];
    document.querySelector("#near")!.textContent =
      near && Math.hypot(near.x - this.x, near.y - this.y) < 120
        ? near.label
        : label;
    this.diagnostics?.sample("update.total", performance.now() - updateStarted);
  }
}
const stage = document.querySelector<HTMLElement>("#stage")!;
function dimensions() {
  return {
    width: native
      ? query.has("wideNative")
        ? 2048
        : 1280
      : Math.min(1280, stage.clientWidth),
    height: native
      ? query.has("wideNative")
        ? 1280
        : 900
      : Math.min(900, stage.clientHeight),
  };
}
const game = new Phaser.Game({
  type: query.get("renderer") === "canvas" ? Phaser.CANVAS : Phaser.AUTO,
  parent: stage,
  ...dimensions(),
  pixelArt: true,
  roundPixels: true,
  antialias: false,
  backgroundColor: "#33494a",
  scene: [Slice, InteriorScene],
  audio: { noAudio: true },
  banner: false,
  input: { activePointers: 4 },
});
function alignCanvas() {
  const s = dimensions();
  if (!native) game.scale.resize(s.width, s.height);
  game.canvas.style.left =
    nativeCanvasOffset(stage.clientWidth, s.width) + "px";
  game.canvas.style.top =
    nativeCanvasOffset(stage.clientHeight, s.height) + "px";
}
alignCanvas();
new ResizeObserver(alignCanvas).observe(stage);
document.querySelector("#pause")!.addEventListener("click", () => {
  paused = !paused;
  reset();
  document.querySelector("#pause")!.textContent = paused ? "Resume" : "Pause";
});
document.querySelector("#close")!.addEventListener("click", () => {
  document.querySelector<HTMLElement>("#dialog")!.hidden = true;
  paused = false;
});
const run = document.querySelector<HTMLButtonElement>("#run")!;
run.onpointerdown = (e) => {
  run.setPointerCapture(e.pointerId);
  heldRun = !scenicLocked;
};
run.onpointerup =
  run.onpointercancel =
  run.onlostpointercapture =
    () => {
      heldRun = false;
    };
window.addEventListener("blur", () => {
  reset();
  heldRun = false;
});

document.querySelector("#export-session")!.addEventListener("click", () => {
  const report = {
    renderer: game.renderer.type === Phaser.WEBGL ? "WebGL" : "Canvas",
    foundationStatus: label,
    physicalDeviceVerification:
      "NOT AUTOMATICALLY VERIFIED / tester must record real model, OS and browser",
    userAgent: navigator.userAgent,
    platform: navigator.platform,
    viewport: [innerWidth, innerHeight],
    screen: [screen.width, screen.height],
    dpr: devicePixelRatio,
    recordedAt: new Date().toISOString(),
    state: window.__GATE3__,
  };
  const url = URL.createObjectURL(
    new Blob([JSON.stringify(report, null, 2)], { type: "application/json" }),
  );
  const link = document.createElement("a");
  link.href = url;
  link.download = "gate3a-test-report.json";
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});
