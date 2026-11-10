import Phaser from "phaser";
import { moveReviewPlayer } from "../gate3/ReviewMovement";
import { movementFacing } from "../gate3/MovementFacing";
import type { JuniMotion, JuniView } from "../engine/JuniMotion";
import type { RegistryMotion } from "../characters/RegistryMotion";
import type { QuestUI } from "../quests/ui";
import {
  interiors,
  roomLayouts,
  roomInteractionGround,
  type RoomLayout,
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
  private layout!: RoomLayout;
  private ground = (x: number, y: number) => roomWalkable(x, y, this.layout);
  private interactionGround = (x: number, y: number) =>
    roomInteractionGround(x, y, this.layout);
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
    this.layout = roomLayouts[data.definition.id];
    [this.x, this.y] = data.resume?.position ?? this.layout.spawn;
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
    this.cameras.main.centerOn(this.layout.width / 2, this.layout.height / 2);
    this.input.setDefaultCursor("default");
    this.add
      .image(0, 0, "room-" + r.id)
      .setOrigin(0)
      .setDepth(-10);
    const prop = (key: string, x: number, y: number) => {
      const sprite = this.add
        .image(x, y, "room-kit", key)
        .setOrigin(0.5, 1)
        .setDepth(y);
      this.objects.push(sprite);
      return sprite;
    };
    for (const [key, x, y] of this.layout.props) prop(key, x, y);
    this.fragmentSprite = prop("fragment", ...this.layout.fragment);
    this.parcelSprite = prop("parcel", ...this.layout.courier);
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
        .setDepth(800);
    addText(this.layout.width / 2, 28, r.name);
    addText(this.layout.exit[0], this.layout.exit[1] + 10, "↓ E · Ra ngoài");
    addText(
      this.layout.sign[0],
      this.layout.sign[1] - 116,
      r.id === "bookshop" ? "Hangul · 한국어" : "Bảng nét chữ",
    );
    addText(
      this.layout.service[0],
      this.layout.service[1] - 20,
      r.id === "workshop"
        ? "Dụng cụ"
        : r.id === "seed-shop"
          ? "Đóng kiện"
          : "Bảng cộng đồng",
    );
    transfer(q.player, this);
    q.player
      .setVisible(true)
      .setPosition(this.x, this.y)
      .setDepth(this.y + 0.1);
    const padX = Math.max(
        0,
        Math.ceil((this.scale.width - this.layout.width) / 2),
      ),
      padY = Math.max(
        0,
        Math.ceil((this.scale.height - this.layout.height) / 2),
      );
    this.cameras.main
      .setBounds(
        -padX,
        -padY,
        Math.max(this.layout.width, this.scale.width),
        Math.max(this.layout.height, this.scale.height),
      )
      .startFollow(q.player, true, 1, 1);
    transfer(q.npc.sprite, this);
    q.npc.sprite
      .setPosition(...this.layout.actor)
      .setVisible(true)
      .setDepth(this.layout.actor[1])
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
      ["exit", this.layout.exit],
      ["fragment", this.layout.fragment],
      ["sign", this.layout.sign],
      ["courier", this.layout.courier],
      ["npc", this.layout.actor],
      ["service", this.layout.service],
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
      ground: this.interactionGround,
      canInteract: () => !this.locked && !this.closing,
      actor: (id) => (id === r.npc ? this.layout.actor : undefined),
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
      this.ground,
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
  private event(event: string, item: string = this.inputData.definition.id) {
    const m = this.inputData.quest.manager,
      s = m.snapshot();
    return m.interiorEvent(
      event,
      item,
      `${event}:${item}:${s.economy.revision}`,
      [this.x, this.y],
      this.eventPoint(event, item),
      this.ground,
    );
  }
  private eventPoint(event: string, item: string): readonly [number, number] {
    if (event === "fragment") return this.layout.fragment;
    if (event === "repair") return this.layout.sign;
    if (event === "courier") return this.layout.courier;
    if (event === "service")
      return item.endsWith(":packing") &&
        this.inputData.definition.id === "workshop"
        ? this.layout.courier
        : this.layout.service;
    return [this.x, this.y];
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
      .image(...this.layout.sign, "room-kit", "notice-restored")
      .setOrigin(0.5, 1)
      .setDepth(this.layout.sign[1] + 1);
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
    if (target === "service") {
      const id = this.inputData.definition.id;
      this.event(
        "service",
        id +
          (id === "workshop"
            ? ":tools"
            : id === "bookshop"
              ? ":notice"
              : ":packing"),
      );
      this.status(
        id === "workshop"
          ? "Đã kiểm tra bộ dụng cụ và ghi dấu công việc."
          : id === "bookshop"
            ? "Đã đọc bảng cộng đồng; nhật ký ghi nhận khi đúng bước."
            : "Đã kiểm tra nhãn và đóng gói vật tư tại quầy.",
      );
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
      if (this.inputData.definition.id === "bookshop") {
        this.inputData.quest.openPractice();
        return;
      }
      this.renderSign();
      return;
    }
    if (target === "courier") {
      if (this.inputData.definition.id === "workshop")
        this.event("service", "workshop:packing");
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
          layoutVersion: 2,
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
        this.ground,
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
      ["exit", this.layout.exit, 40],
      ["fragment", this.layout.fragment, 48],
      ["sign", this.layout.sign, 48],
      ["courier", this.layout.courier, 48],
      ["service", this.layout.service, 48],
      ["npc", this.layout.actor, 112],
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
          service: "E · Kiểm tra / ghi nhận",
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
      layoutVersion: 2,
      layout: this.layout,
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
      footOnFloor: this.ground(this.x, this.y),
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
      layoutVersion: 2;
      layout: RoomLayout;
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
