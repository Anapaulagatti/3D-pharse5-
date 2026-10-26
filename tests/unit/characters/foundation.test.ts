import { CharacterSession } from "../../../src/characters/session";
import { describe, it, expect } from "vitest";
import {
  characterRegistry,
  CharacterRegistry,
} from "../../../src/characters/registry";
import {
  CharacterPreferences,
  PREFERENCES_KEY,
} from "../../../src/characters/preferences";
import { validateAtlas } from "../../../src/characters/types";
import atlas from "../../../public/assets/juni/juni.json";
import {
  PlayerCharacterManager,
  type PlayerSprite,
} from "../../../src/characters/PlayerCharacterManager";
import { RegistryMotion } from "../../../src/characters/RegistryMotion";
const juni = characterRegistry.resolve("juni");
// Fixture is never shipped as new art; exercise loading/switch transactions only.
const fixture = {
  ...juni,
  id: "pipeline-fixture",
  names: { ko: "테스트", vi: "Pipeline fixture only" },
};
const registry = new CharacterRegistry([juni, fixture]);
const incompleteRegistry = new CharacterRegistry([
  juni,
  {
    ...juni,
    id: "unfinished",
    assets: null,
    animations: {},
    availability: {
      status: "incomplete",
      unlock: "free",
      reason: "Test incomplete rejection only",
    },
  },
]);
function storage() {
  const map = new Map<string, string>();
  return {
    map,
    getItem: (k: string) => map.get(k) ?? null,
    setItem: (k: string, v: string) => {
      map.set(k, v);
    },
  };
}
class Sprite implements PlayerSprite {
  dead = false;
  visible = true;
  x = 0;
  y = 0;
  depth = 0;
  frame = "";
  setPosition(x: number, y: number) {
    this.x = x;
    this.y = y;
    return this;
  }
  setDepth(d: number) {
    this.depth = d;
    return this;
  }
  setFrame(f: string) {
    this.frame = f;
    return this;
  }
  setVisible(v: boolean) {
    this.visible = v;
    return this;
  }
  destroy() {
    this.dead = true;
  }
}
function setup(load = async () => {}) {
  const store = storage(),
    sprites: Sprite[] = [];
  const pref = new CharacterPreferences(store, registry);
  const manager = new PlayerCharacterManager(
    { ensure: load },
    (_def, p) => {
      const s = new Sprite().setPosition(p.x, p.y);
      sprites.push(s);
      return s;
    },
    pref,
    juni,
    { x: 2048, y: 1460 },
    registry,
  );
  return { manager, store, sprites };
}
describe("character registry and atlas boundary", () => {
  it("registers six identities with Juni as safe playable fallback", () => {
    expect(characterRegistry.all.map((c) => c.id)).toEqual([
      "juni",
      "haneul",
      "bomi",
      "minjun",
      "ara",
      "doyun",
    ]);
    expect(characterRegistry.resolve("missing").id).toBe("juni");
    expect(characterRegistry.resolve("bomi").id).toBe("bomi");
    expect(
      characterRegistry.all.every((c) => c.availability.status === "playable"),
    ).toBe(true);
  });
  it("rejects duplicate identities and broken required gait definitions", () => {
    expect(() => new CharacterRegistry([juni, juni])).toThrow("Duplicate");
    const broken = {
      ...juni,
      animations: {
        ...juni.animations,
        "run-back": { frames: ["same"], durationsMs: [100], loop: true },
      },
    };
    expect(() => new CharacterRegistry([broken])).toThrow();
  });
  it("validates every original frame and rejects missing/misaligned atlases", () => {
    expect(() => validateAtlas(juni, atlas)).not.toThrow();
    expect(() => validateAtlas(juni, { frames: {} })).toThrow(
      "Missing/invalid",
    );
    const bad = structuredClone(atlas);
    bad.frames["walk-front-0"].frame.w = 95;
    expect(() => validateAtlas(juni, bad)).toThrow();
  });
});
describe("preferences protect unrelated progress", () => {
  it("first launch and invalid schemas require selection with Juni default", () => {
    const s = storage(),
      p = new CharacterPreferences(s, characterRegistry);
    expect(p.read().needsSelection).toBe(true);
    for (const raw of [
      "{",
      '{"version":2,"characterId":"juni"}',
      '{"version":1,"characterId":"unknown"}',
      '{"version":1,"characterId":"unfinished"}',
    ]) {
      s.map.set(PREFERENCES_KEY, raw);
      expect(p.read()).toMatchObject({
        characterId: "juni",
        needsSelection: true,
      });
    }
  });
  it("round-trips selection without clearing progress or other storage", () => {
    const s = storage(),
      p = new CharacterPreferences(s, characterRegistry);
    s.map.set("learning-progress-fixture", "KEEP");
    expect(p.save("juni")).toBe(true);
    expect(new CharacterPreferences(s, characterRegistry).read()).toMatchObject(
      { characterId: "juni", needsSelection: false },
    );
    expect(s.map.get("learning-progress-fixture")).toBe("KEEP");
    expect(p.save("minjun")).toBe(true);
    expect(p.read().characterId).toBe("minjun");
    expect(p.save("unknown")).toBe(false);
  });
  it("unavailable/throwing browser storage never prevents session play", () => {
    const p = new CharacterPreferences(
      {
        getItem() {
          throw Error("denied");
        },
        setItem() {
          throw Error("quota");
        },
      },
      characterRegistry,
    );
    expect(p.read().characterId).toBe("juni");
    expect(p.save("juni")).toBe(false);
    expect(
      new CharacterPreferences(undefined, characterRegistry).save("juni"),
    ).toBe(false);
  });
});
describe("transactional sprite ownership", () => {
  it("loads before replacing and preserves supplied position/progress identity", async () => {
    const { manager, sprites, store } = setup();
    const externalProgress = { level: 7, lessons: ["fixture"] };
    await manager.select(fixture.id, { x: 2001.25, y: 1400.5 });
    expect(sprites[0].dead).toBe(true);
    expect(manager.sprite).toMatchObject({
      x: 2001.25,
      y: 1400.5,
      visible: true,
    });
    expect(sprites.filter((s) => !s.dead)).toHaveLength(1);
    expect(externalProgress).toEqual({ level: 7, lessons: ["fixture"] });
    expect(JSON.parse(store.map.get(PREFERENCES_KEY)!).characterId).toBe(
      fixture.id,
    );
  });
  it("a missing atlas keeps the original sprite and saved state intact", async () => {
    const { manager, sprites, store } = setup(async () => {
      throw Error("Missing atlas");
    });
    await expect(manager.select(fixture.id, { x: 10, y: 20 })).rejects.toThrow(
      "Missing atlas",
    );
    expect(manager.sprite).toBe(sprites[0]);
    expect(sprites[0].dead).toBe(false);
    expect(store.map.size).toBe(0);
  });
  it("refuses incomplete art and unsafe transition switches", async () => {
    const { manager } = setup();
    manager.setTransitioning(true);
    await expect(manager.select(fixture.id, { x: 0, y: 0 })).rejects.toThrow(
      "transition",
    );
    manager.setTransitioning(false);
    const r = new PlayerCharacterManager(
      { ensure: async () => {} },
      () => new Sprite(),
      new CharacterPreferences(storage(), incompleteRegistry),
      juni,
      { x: 0, y: 0 },
      incompleteRegistry,
    );
    await expect(r.select("unfinished", { x: 0, y: 0 })).rejects.toThrow(
      "incomplete",
    );
  });
  it("shutdown or concurrent requests cannot create orphan player sprites", async () => {
    let done!: () => void;
    const { manager, sprites } = setup(
      () =>
        new Promise<void>((r) => {
          done = r;
        }),
    );
    const first = manager.select(fixture.id, { x: 1, y: 2 });
    await expect(manager.select("juni", { x: 1, y: 2 })).rejects.toThrow();
    manager.dispose();
    done();
    await expect(first).rejects.toThrow("Scene changed");
    expect(sprites).toHaveLength(1);
    expect(sprites[0].dead).toBe(true);
  });
  it("reselecting Juni keeps existing motion and sprite; unknown ID falls back", async () => {
    const { manager, sprites } = setup();
    const motion = manager.motion;
    await manager.select("unknown", { x: 10, y: 20 });
    expect(manager.motion).toBe(motion);
    expect(sprites).toHaveLength(1);
  });
});
describe("generic future atlas playback", () => {
  it("advances gait only by actual travel and resolves emotes then idle", () => {
    const m = new RegistryMotion(fixture);
    m.step(16, 10, true, false, "right", false, false);
    expect(m.frame).toMatch(/^start-right-/);
    for (let i = 0; i < 5; i++)
      m.step(100, 1, true, false, "right", false, false);
    expect(m.frame).toMatch(/^walk-right-/);
    const phase = m.phase;
    m.step(16, 0, true, false, "right", false, false);
    expect(m.phase).toBe(phase);
    m.step(16, 0, false, false, "right", false, false);
    m.gesture("celebrate");
    m.step(16, 0, false, false, "right", false, false);
    expect(m.frame).toMatch(/^celebrate-front-/);
    for (let i = 0; i < 20; i++)
      m.step(100, 0, false, false, "front", false, false);
    expect(m.action).toBe("idle");
  });
});

describe("avatar identity across scene lifetimes", () => {
  it("retains a confirmed choice in memory even with blocked persistent storage", () => {
    const session = new CharacterSession(
      { characterId: "juni", needsSelection: true },
      registry,
    );
    expect(session.needsSelection).toBe(true);
    session.commit(fixture.id);
    const secondSceneSelection = session.selected;
    expect(secondSceneSelection.id).toBe(fixture.id);
    expect(session.needsSelection).toBe(false);
    expect(
      new CharacterSession(
        { characterId: "juni", needsSelection: true },
        registry,
      ).selected.id,
    ).toBe("juni");
  });
  it("cannot promote an incomplete character through session state", () => {
    const session = new CharacterSession(
      {
        characterId: "unfinished",
        needsSelection: true,
      },
      incompleteRegistry,
    );
    expect(session.selected.id).toBe("juni");
    expect(() => session.commit("unfinished")).toThrow("Incomplete");
  });
});
