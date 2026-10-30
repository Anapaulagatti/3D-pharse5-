import { describe, expect, it } from "vitest";
import { movementFacing } from "../../src/gate3/MovementFacing";

describe("movement cardinal continuity", () => {
  it("retains the active axis when a diagonal key is added or released", () => {
    expect(movementFacing(1, -1, "right")).toBe("right");
    expect(movementFacing(1, -1, "back")).toBe("back");
    expect(movementFacing(-1, 1, "left")).toBe("left");
    expect(movementFacing(-1, 1, "front")).toBe("front");
    expect(movementFacing(1, 0, "back")).toBe("right");
  });
  it("uses the traversed axis at walls and retains facing when blocked", () => {
    expect(movementFacing(0, -0.8, "right")).toBe("back");
    expect(movementFacing(0.8, 0, "back")).toBe("right");
    expect(movementFacing(0, 0, "left")).toBe("left");
  });
});
