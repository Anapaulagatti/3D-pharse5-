import Phaser from "phaser";
import { moveReviewPlayer } from "../gate3/ReviewMovement";
import { movementFacing } from "../gate3/MovementFacing";
import type { JuniMotion, JuniView } from "../engine/JuniMotion";
import type { RegistryMotion } from "../characters/RegistryMotion";
import type { QuestUI } from "../quests/ui";
import {
  interiors,
  ROOM,
  roomWalkable,
  INTERIOR_SAVE,
  type InteriorDefinition,
  type InteriorSave,
} from "./registry";
import { quests } from "../quests/content";
interface Borrowed {
  sprite: Phaser.GameObjects.Sprite;
  restore(): void;
}
export interface InteriorInput {
  definition: InteriorDefinition;
  player: Phaser.GameObjects.Sprite;
  motion: JuniMotion | RegistryMotion;
  owner: Phaser.Scene;
  world: [number, number];
  quest: QuestUI;
  npc: Borrowed;
  analog: () => { x: number; y: number; run: boolean };
  onExit(): void;
  resume?: InteriorSave;
}
function transfer(sprite: Phaser.GameObjects.Sprite, to: Phaser.Scene) {
  sprite.removeFromUpdateList();
  sprite.scene.sys.updateList.update();
  sprite.removeFromDisplayList();
  sprite.scene = to;
  to.add.existing(sprite);
}
/** A real Phaser room. Borrows the SAME approved player/NPC objects and motion controller. No new character engine. */
export class InteriorScene extends Phaser.Scene {
  private inputData!: InteriorInput;
  private x = 320;
  private y = 414;
  private facing: JuniView = "front";
  private keys!: Record<string, Phaser.Input.Keyboard.Key>;
  private locked = false;
  private closing = false;
  private objects: Phaser.GameObjects.GameObject[] = [];
  private panel!: HTMLElement;
  private hint!: HTMLButtonElement;
  private signSlots: string[] = [];
  private carried?: string;
  private elapsed = 0;
  private currentTarget = "";
  private savedAt = 0;
  private placements = 0;
  private fragmentSprite?: Phaser.GameObjects.Image;
  private parcelSprite?: Phaser.GameObjects.Image;
  private bindings?: AbortController;
  constructor() {
    super("town-interior");
  }
  init(data: InteriorInput) {
    this.inputData = data;
    [this.x, this.y] = data.resume?.position ?? ROOM.spawn;
    this.locked = false;
    this.closing = false;
    this.signSlots = [];
    this.carried = undefined;
    this.currentTarget = "";
    this.elapsed = 0;
    this.savedAt = 0;
    this.placements = 0;
    this.objects = [];
  }
  create() {
    document.body.dataset.interior = "true";
    const q = this.inputData,
      r = q.definition;
    this.cameras.main.setBackgroundColor("#20352f");
    this.cameras.main.setZoom(1).setRoundPixels(true);
    this.cameras.main.centerOn(320, 240);
    this.input.setDefaultCursor("default");
    for (let y = 96; y < 464; y += 16)
      for (let x = 32; x < 608; x += 16)
        this.objects.push(
          this.add
            .image(
              x,
              y,
              "town-props",
              r.kind === "market" ? "floor-stone" : "floor-wood",
            )
            .setOrigin(0)
            .setCrop(0, 0, 16, 16)
            .setDepth(-5),
        );
    for (let x = 32; x < 608; x += 64)
      this.objects.push(
        this.add.image(x, 32, "town-props", "wall").setOrigin(0).setDepth(-2),
      );
    const prop = (key: string, x: number, y: number) => {
      const s = this.add
        .image(x, y, "town-props", key)
        .setOrigin(0.5, 0.95)
        .setDepth(y);
      this.objects.push(s);
      return s;
    };
    for (const x of [80, 112, 520, 552]) {
      prop(r.kind === "books" ? "bookshelf" : "seed-rack", x, 188);
    }
    prop("counter", 288, 234);
    prop("counter", 350, 234);
    prop("lamp", 220, 240);
    prop("lamp", 420, 180);
    prop("table", 114, 392);
    prop("table", 524, 392);
    prop("stool", 205, 365);
    prop("stool", 433, 365);
    this.fragmentSprite = prop("fragment", ...ROOM.fragment);
    prop(
      (q.quest.manager.snapshot().records["town-first-delivery-v2"]?.step ??
        0) > 4
        ? "restored-sign"
        : "sign",
      ...ROOM.sign,
    );
    this.parcelSprite = prop("parcel", ...ROOM.courier);
    const addText = (x: number, y: number, text: string) =>
      this.add
        .text(x, y, text, {
          fontSize: "13px",
          fontFamily: "sans-serif",
          color: "#fff0c5",
          backgroundColor: "#263c32",
          padding: { x: 5, y: 3 },
        })
        .setOrigin(0.5)
        .setDepth(-1);
    addText(320, 90, r.name);
    addText(320, 458, "↓ Ra ngoài · E / chạm");
    addText(150, 270, "Mảnh nét");
    addText(486, 268, "Bảng chữ");
    addText(320, 262, "Điểm giao");
    transfer(q.player, this);
    q.player
      .setVisible(true)
      .setPosition(this.x, this.y)
      .setDepth(this.y + 0.1);
    const padX = Math.max(0, Math.ceil((this.scale.width - 640) / 2)),
      padY = Math.max(0, Math.ceil((this.scale.height - 480) / 2));
    this.cameras.main
      .setBounds(
        -padX,
        -padY,
        Math.max(640, this.scale.width),
        Math.max(480, this.scale.height),
      )
      .startFollow(q.player, true, 1, 1);
    transfer(q.npc.sprite, this);
    q.npc.sprite
      .setPosition(...ROOM.actor)
      .setVisible(true)
      .setDepth(ROOM.actor[1])
      .setFrame("idle-front-0");
    q.npc.sprite.disableInteractive();
    this.keys = this.input.keyboard!.addKeys(
      "W,A,S,D,UP,DOWN,LEFT,RIGHT,SHIFT,E,ESC,ONE,TWO,THREE,BACKSPACE,ENTER",
    ) as typeof this.keys;
    this.input.keyboard!.on("keydown-E", (e: KeyboardEvent) => {
      if (!e.repeat) this.act();
    });
    this.input.keyboard!.on("keydown-ESC", () => {
      if (
        !this.locked &&
        !document.querySelector<HTMLDialogElement>("#quest-dialogue")?.open
      )
        this.leave();
    });
    this.input.keyboard!.on("keydown", (e: KeyboardEvent) => {
      if (this.locked || e.repeat || this.currentTarget !== "sign") return;
      if (["1", "2", "3"].includes(e.key)) this.place(Number(e.key) - 1);
      if (e.key === "Backspace") this.undo();
      if (e.key === "Enter") this.submitSign();
    });
    this.panel = document.createElement("section");
    this.panel.id = "interior-tools";
    this.panel.setAttribute("aria-label", r.name);
    this.panel.innerHTML =
      '<strong></strong><p id="interior-status" role="status"></p><div id="sign-pieces" hidden></div>';
    this.panel.querySelector("strong")!.textContent = r.name + " · Demo cục bộ";
    this.hint = document.createElement("button");
    this.hint.id = "interior-action";
    this.hint.onclick = () => this.act();
    this.panel.append(this.hint);
    document.body.append(this.panel);
    this.bindings = new AbortController();
    document
      .querySelector("#explore")!
      .addEventListener("click", () => this.act(), {
        signal: this.bindings.signal,
      });
    for (const [k, point] of [
      ["exit", ROOM.exit],
      ["fragment", ROOM.fragment],
      ["sign", ROOM.sign],
      ["courier", ROOM.courier],
      ["npc", ROOM.actor],
    ] as const) {
      const zone = this.add
        .zone(point[0], point[1], k === "npc" ? 90 : 50, 60)
        .setInteractive({ useHandCursor: true })
        .setDepth(600);
      zone.on("pointerup", (p: Phaser.Input.Pointer) => {
        if (
          p.getDistance() < 12 &&
          Math.hypot(this.x - point[0], this.y - point[1]) <
            (k === "npc" ? 112 : 48)
        )
          this.act(k);
      });
    }
    q.quest.useInterior({
      player: () => [this.x, this.y],
      ground: roomWalkable,
      canInteract: () => !this.locked && !this.closing,
      actor: (id) => (id === r.npc ? ROOM.actor : undefined),
      actorName: () => r.npc.replace("npc-", ""),
      lock: () => {
        this.locked = true;
        this.input.keyboard!.resetKeys();
        return () => {
          this.locked = false;
          this.input.keyboard!.resetKeys();
        };
      },
      onOpen: () => {},
      onClose: () => {},
    });
    // Entry is proximity checked outside before the scene starts; progression still ordered/idempotent.
    q.quest.manager.interiorEvent(
      "enter",
      r.id,
      "enter:" + r.id + ":" + q.quest.manager.snapshot().economy.revision,
      [this.x, this.y],
      [this.x, this.y],
      roomWalkable,
    );
    this.events.once("shutdown", () => {
      this.bindings?.abort();
      this.panel?.remove();
      delete document.body.dataset.interior;
      delete window.__INTERIOR__;
    });
    this.persist();
  }
  private status(text: string) {
    this.panel.querySelector("#interior-status")!.textContent = text;
  }
  private event(event: string, item = this.inputData.definition.id) {
    const m = this.inputData.quest.manager,
      s = m.snapshot();
    return m.interiorEvent(
      event,
      item,
      `${event}:${item}:${s.economy.revision}`,
      [this.x, this.y],
      [this.x, this.y],
      roomWalkable,
    );
  }
  private place(index: number) {
    if (
      this.currentTarget !== "sign" ||
      this.signSlots.includes(["ㅊ", "ㅐ", "ㄱ"][index]) ||
      this.signSlots.length >= 3
    )
      return;
    this.signSlots.push(["ㅊ", "ㅐ", "ㄱ"][index]);
    this.placements++;
    this.renderSign();
  }
  private undo() {
    this.signSlots.pop();
    this.renderSign();
  }
  private renderSign() {
    const el = this.panel.querySelector<HTMLElement>("#sign-pieces")!;
    el.hidden = false;
    el.replaceChildren();
    const p = document.createElement("p");
    p.textContent = `Ghép ‘책’ (sách): phụ âm đầu + nguyên âm + phụ âm cuối · ${this.signSlots.join(" / ") || "□ / □ / □"}`;
    el.append(p);
    ["ㅊ", "ㅐ", "ㄱ"].forEach((text, i) => {
      const b = document.createElement("button");
      b.textContent = `${i + 1} · ${text}`;
      b.dataset.piece = String(i);
      b.draggable = true;
      b.ondragstart = (e) => e.dataTransfer?.setData("text/plain", String(i));
      b.onclick = () => this.place(i);
      el.append(b);
    });
    const drop = document.createElement("button");
    drop.textContent = "Thả nét vào đây / Enter kiểm tra";
    drop.ondragover = (e) => e.preventDefault();
    drop.ondrop = (e) => {
      e.preventDefault();
      this.place(Number(e.dataTransfer?.getData("text/plain")));
    };
    drop.onclick = () => this.submitSign();
    const undo = document.createElement("button");
    undo.textContent = "Hoàn tác · Backspace";
    undo.onclick = () => this.undo();
    el.append(drop, undo);
  }
  private submitSign() {
    if (this.signSlots.join("") !== "ㅊㅐㄱ") {
      this.status("Thử lại nhẹ nhàng: ㅊ + ㅐ + ㄱ → 책. Không trừ vật phẩm.");
      return;
    }
    const q =
      this.inputData.quest.manager.snapshot().records["town-first-delivery-v2"];
    if (q?.step !== 4 || q.status !== "active") {
      this.status("Tìm đủ ba mảnh trong chuỗi giao sách trước.");
      return;
    }
    this.event("repair");
    const s = this.add
      .image(...ROOM.sign, "town-props", "restored-sign")
      .setOrigin(0.5, 0.95)
      .setDepth(ROOM.sign[1] + 1);
    this.objects.push(s);
    this.status("Bảng 책 đã sáng! Nhận tuyến giao ở giữa xưởng.");
    this.panel.querySelector<HTMLElement>("#sign-pieces")!.hidden = true;
  }
  private act(forced?: string) {
    if (this.locked || this.closing) return;
    const target = forced ?? this.currentTarget;
    if (target === "exit") {
      this.leave();
      return;
    }
    if (target === "npc") {
      this.inputData.quest.open(this.inputData.definition.npc);
      return;
    }
    if (target === "fragment") {
      const before =
        this.inputData.quest.manager.snapshot().records[
          "town-first-delivery-v2"
        ]?.step;
      this.event("fragment");
      this.status(
        this.inputData.quest.manager.snapshot().records[
          "town-first-delivery-v2"
        ]?.step !== before
          ? "Đã nhặt nét chữ!"
          : "Nhận lời Eunji ở xưởng và theo thứ tự nhật ký.",
      );
      return;
    }
    if (target === "sign") {
      this.renderSign();
      return;
    }
    if (target === "courier") {
      const before =
        this.inputData.quest.manager.snapshot().records[
          "town-first-delivery-v2"
        ]?.step;
      this.event("courier");
      this.status(
        this.inputData.quest.manager.snapshot().records[
          "town-first-delivery-v2"
        ]?.step !== before
          ? "Đã xác nhận tuyến giao. Không giới hạn thời gian bắt buộc."
          : "Theo địa chỉ trong nhật ký; gói sách vẫn an toàn.",
      );
    }
  }
  private persist() {
    try {
      localStorage.setItem(
        INTERIOR_SAVE,
        JSON.stringify({
          version: 1,
          id: this.inputData.definition.id,
          world: this.inputData.world,
          position: [this.x, this.y],
        }),
      );
    } catch {
      this.status("Chưa lưu được vị trí trong phòng.");
    }
  }
  private leave() {
    if (this.closing || this.locked) return;
    this.closing = true;
    const q = this.inputData;
    q.quest.close();
    q.quest.useInterior();
    q.npc.restore();
    transfer(q.player, q.owner);
    q.player.setPosition(...q.world).setDepth(q.world[1] + 0.1);
    try {
      localStorage.removeItem(INTERIOR_SAVE);
    } catch {
      /*optional*/
    }
    q.onExit();
    this.scene.stop();
  }
  update(_time: number, dt: number) {
    if (!this.inputData || this.closing) return;
    const q = this.inputData;
    this.elapsed += dt;
    const a = q.analog();
    let dx =
        Number(this.keys.D.isDown || this.keys.RIGHT.isDown) -
        Number(this.keys.A.isDown || this.keys.LEFT.isDown) +
        a.x,
      dy =
        Number(this.keys.S.isDown || this.keys.DOWN.isDown) -
        Number(this.keys.W.isDown || this.keys.UP.isDown) +
        a.y;
    if (this.locked || document.hidden) {
      dx = 0;
      dy = 0;
    }
    const n = Math.max(1, Math.hypot(dx, dy));
    dx /= n;
    dy /= n;
    const run = a.run || this.keys.SHIFT.isDown,
      old = [this.x, this.y],
      m = moveReviewPlayer(
        this.x,
        this.y,
        dx,
        dy,
        (Math.min(dt, 50) * (run ? 100 : 60)) / 1000,
        roomWalkable,
      );
    this.x = m.x;
    this.y = m.y;
    const distance = Math.hypot(this.x - old[0], this.y - old[1]);
    if (distance > 0.01)
      this.facing = movementFacing(
        this.x - old[0],
        this.y - old[1],
        this.facing,
      );
    const frame = q.motion.step(
      dt,
      distance,
      distance > 0.01,
      run,
      this.facing,
      matchMedia("(prefers-reduced-motion: reduce)").matches,
      this.locked,
    );
    q.player
      .setPosition(Math.round(this.x), Math.round(this.y))
      .setFrame(frame)
      .setDepth(Math.round(this.y) + 0.1);
    const storyState =
      q.quest.manager.snapshot().records["town-first-delivery-v2"];
    const fragmentIndex = (
      { workshop: 2, bookshop: 3, "seed-shop": 4 } as Record<string, number>
    )[q.definition.id];
    const fragmentDone = (storyState?.step ?? 0) >= fragmentIndex;
    this.fragmentSprite?.setVisible(!fragmentDone);
    this.parcelSprite?.setVisible(
      !!storyState && storyState.step >= 5 && storyState.step < 8,
    );
    const targets = [
      ["exit", ROOM.exit, 40],
      ["fragment", ROOM.fragment, 48],
      ["sign", ROOM.sign, 48],
      ["courier", ROOM.courier, 48],
      ["npc", ROOM.actor, 112],
    ] as const;
    this.currentTarget =
      targets
        .filter(([key]) => key !== "fragment" || !fragmentDone)
        .find(
          ([, p, r]) => Math.hypot(this.x - p[0], this.y - p[1]) <= r,
        )?.[0] ?? "";
    this.hint.hidden = !this.currentTarget;
    this.hint.textContent =
      (
        {
          exit: "E · Ra ngoài",
          fragment: "E · Nhặt nét",
          sign: "E · Ghép bảng",
          courier: "E · Xác nhận địa chỉ",
          npc: "E · Trò chuyện / giao dịch",
        } as Record<string, string>
      )[this.currentTarget] ?? "";
    if (this.currentTarget !== "sign")
      this.panel.querySelector<HTMLElement>("#sign-pieces")!.hidden = true;
    q.quest.update();
    if (this.elapsed - this.savedAt > 500) {
      this.persist();
      this.savedAt = this.elapsed;
    }
    const story = q.quest.manager.snapshot().records["town-first-delivery-v2"];
    document.querySelector("#near")!.textContent =
      `${q.definition.name} · ${story ? (quests.find((x) => x.id === "town-first-delivery-v2")!.steps[story.step]?.label ?? "Trở lại Jiho") : "WASD, E, Esc để trở ra"}`;
    window.__INTERIOR__ = {
      progress: {
        records: q.quest.manager.snapshot().records,
        coins: q.quest.manager.snapshot().coins,
        inventory: q.quest.manager.snapshot().inventory,
      },
      camera: [
        this.cameras.main.width,
        this.cameras.main.height,
        this.cameras.main.scrollX,
        this.cameras.main.scrollY,
      ],
      id: q.definition.id,
      x: this.x,
      y: this.y,
      frame,
      target: this.currentTarget,
      locked: this.locked,
      playerIdentity: q.player.getData("playerCharacter"),
      npcIdentity: q.definition.npc,
      placements: this.placements,
      footOnFloor: roomWalkable(this.x, this.y),
      scale: q.player.scaleX,
      sampling: q.player.frame.source.scaleMode,
      scene: "town-interior",
      world: q.world,
      sign: [...this.signSlots],
    };
  }
}
declare global {
  interface Window {
    __INTERIOR__?: {
      progress: {
        records: ReturnType<QuestUI["manager"]["snapshot"]>["records"];
        coins: number;
        inventory: Record<string, number>;
      };
      camera: number[];
      id: string;
      x: number;
      y: number;
      frame: string;
      target: string;
      locked: boolean;
      playerIdentity: string;
      npcIdentity: string;
      placements: number;
      footOnFloor: boolean;
      scale: number;
      sampling: number;
      scene: string;
      world: [number, number];
      sign: string[];
    };
  }
}
export { interiors };
