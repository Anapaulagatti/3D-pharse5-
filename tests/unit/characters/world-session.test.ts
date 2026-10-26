import { describe, it, expect } from "vitest";
import { WorldSessionCheckpoint } from "../../../src/platform/WorldSessionCheckpoint";
import type { Manifest } from "../../../src/gate3/types";
const world: Manifest = {
  id: "test-world",
  size: [100, 100],
  spawn: [10, 10],
  targets: [{ id: "station", x: 20, y: 20, label: "Station" }],
  chunks: [],
  objects: [],
  overview: "",
  budgetBytes: 1,
  maxConcurrent: 1,
  stops: [],
  logicalSolids: [{ id: "building", rect: [40, 40, 20, 20] }],
};
describe("per-tab reload continuity", () => {
  it("round-trips existing position and visited ids, preserving unrelated preference storage", () => {
    const data = new Map([["korean-arena-player-preferences-v1", "KEEP"]]);
    const storage = {
      getItem: (k: string) => data.get(k) ?? null,
      setItem: (k: string, v: string) => {
        data.set(k, v);
      },
    };
    const checkpoint = new WorldSessionCheckpoint(
      storage,
      "/game?entry=station",
      world,
    );
    checkpoint.save(20.125, 23.75, ["station", "unknown"]);
    expect(checkpoint.read()).toMatchObject({
      x: 20.125,
      y: 23.75,
      visited: ["station"],
    });
    expect(data.get("korean-arena-player-preferences-v1")).toBe("KEEP");
    expect(
      new WorldSessionCheckpoint(storage, "/game?entry=bridge", world).read(),
    ).toBeNull();
    checkpoint.save(45, 45, []);
    expect(checkpoint.read()).toBeNull();
    checkpoint.save(-1, 1, []);
    expect(checkpoint.read()).toBeNull();
  });
  it("corrupt, denied or unavailable session storage never interrupts play", () => {
    expect(
      new WorldSessionCheckpoint(
        { getItem: () => "{", setItem: () => {} },
        "/",
        world,
      ).read(),
    ).toBeNull();
    const denied = new WorldSessionCheckpoint(
      {
        getItem: () => {
          throw Error("denied");
        },
        setItem: () => {
          throw Error("quota");
        },
      },
      "/",
      world,
    );
    expect(denied.read()).toBeNull();
    expect(() => denied.save(10, 10, [])).not.toThrow();
    expect(new WorldSessionCheckpoint(undefined, "/", world).read()).toBeNull();
  });
});
