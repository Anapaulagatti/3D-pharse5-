import { describe, expect, it } from "vitest";
import { NativeContact } from "../../src/gate3/NativeContact";
describe("native contact at a narrow turning landing", () => {
  const pixels = new Uint8Array(20 * 20);
  for (let y = 0; y < 20; y++)
    for (let x = 0; x < 20; x++)
      if ((x >= 9 && x <= 11) || (y >= 8 && y <= 12)) pixels[y * 20 + x] = 1;
  const contact = new NativeContact(
    {
      physical: "unused",
      rect: [100, 200, 20, 20],
      footprints: {
        "walk-front": [
          [-1, -1],
          [1, -1],
          [-1, -4],
          [1, -4],
        ],
        "walk-right": [
          [-4, -1],
          [4, -1],
          [-4, -4],
          [4, -4],
        ],
      },
    },
    pixels,
  );
  it("allows the narrow approach but requires the feet to reach the landing before turning", () => {
    expect(contact.allows(110, 207, "walk", "front")).toBe(true);
    expect(contact.allows(110, 207, "walk", "right")).toBe(false);
    expect(contact.allows(110, 212, "walk", "right")).toBe(true);
  });
  it("uses native rounded world pixels and leaves scenes outside the local guard unchanged", () => {
    expect(contact.allows(110.4, 212.4, "walk", "right")).toBe(true);
    expect(contact.allows(40, 50, "walk", "right")).toBe(true);
    expect(() => new NativeContact(contact.spec, new Uint8Array(1))).toThrow(
      "size mismatch",
    );
  });
});
