import { describe, it, expect } from "vitest";
import {
  decodeGuest,
  defaultGuest,
  inputVector,
  facing,
  ContentLabel,
} from "../../src/domains/state";
describe("untrusted local progress", () => {
  it("recovers from corrupt and incompatible state", () => {
    for (const raw of [
      null,
      "broken",
      '{"version":9}',
      '{"version":1,"style":"<script>","visits":99999999,"metMira":true}',
    ])
      expect(decodeGuest(raw)).toEqual(defaultGuest);
  });
  it("retains verified style and greeting across reload", () => {
    expect(
      decodeGuest(
        JSON.stringify({ version: 1, style: "C", visits: 2, metMira: true }),
      ),
    ).toEqual({ version: 1, style: "C", visits: 2, metMira: true });
  });
});
describe("input and Korean text contracts", () => {
  it("diagonal input grants no speed advantage", () => {
    expect(Math.hypot(...Object.values(inputVector(1, 1)))).toBeCloseTo(1);
    expect(inputVector(0, 0)).toEqual({ x: 0, y: 0 });
  });
  it("retains orientation at rest and picks four directions", () => {
    expect(facing(0, 0, "up")).toBe("up");
    expect(facing(-1, 0, "up")).toBe("left");
    expect(facing(1, 0, "up")).toBe("right");
    expect(facing(0, -1, "down")).toBe("up");
    expect(facing(0, 1, "up")).toBe("down");
  });
  it("rejects decomposed Hangul and false certified status", () => {
    expect(
      ContentLabel.safeParse({
        id: "post-office",
        ko: "우체국",
        vi: "Bưu điện",
        provenance: "ORIGINAL",
        review: "PENDING_HUMAN_REVIEW",
      }).success,
    ).toBe(true);
    expect(
      ContentLabel.safeParse({
        id: "post-office",
        ko: "우체국".normalize("NFD"),
        vi: "Bưu điện",
        provenance: "ORIGINAL",
        review: "REVIEWED",
      }).success,
    ).toBe(false);
    expect(
      ContentLabel.safeParse({
        id: "post-office",
        ko: "우체국",
        vi: "Bưu điện",
        provenance: "ORIGINAL",
        review: "EXPERT_CERTIFIED",
      }).success,
    ).toBe(false);
  });
});
