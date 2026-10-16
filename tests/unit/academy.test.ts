import { expect, it } from "vitest";
import { parseAcademyProgress } from "../../src/domains/academy";
it("accepts only known letter completion; recovers corrupt and incompatible local progress", () => {
  for (const raw of [
    null,
    "broken",
    "null",
    '{"version":99,"mastered":["ㄱ"]}',
    '{"version":1,"mastered":"ㄱ"}',
  ])
    expect(parseAcademyProgress(raw)).toEqual({ version: 1, mastered: [] });
  expect(
    parseAcademyProgress(
      '{"version":1,"mastered":["ㅁ","ㄱ","ㄱ","<script>",null,88]}',
    ),
  ).toEqual({ version: 1, mastered: ["ㄱ", "ㅁ"] });
});
