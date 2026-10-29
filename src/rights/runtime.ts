import source from "../../assets-src/rights/npc-inventory.json";
import { validateRightsInventory } from "./contract";
/** Controlled by Vite build configuration, never a URL or saved permission. */
export const privateReviewBuild =
  import.meta.env.VITE_RELEASE_PROFILE !== "public";
export const rightsInventory = validateRightsInventory(
  source,
  source.assets.map((a) => a.stableId),
);
export function mountRightsReport() {
  if (!privateReviewBuild) return;
  const report = document.createElement("section");
  report.id = "npc-rights-report";
  const toggle = document.createElement("button");
  toggle.type = "button";
  toggle.id = "npc-rights-toggle";
  toggle.textContent = "Private review · quyền asset chưa xác minh";
  toggle.setAttribute("aria-controls", "npc-rights-records");
  toggle.setAttribute("aria-expanded", "false");
  const records = document.createElement("div");
  records.id = "npc-rights-records";
  records.hidden = true;
  for (const asset of rightsInventory.assets) {
    const p = document.createElement("p");
    p.textContent = `${asset.publicName.vi} · ${asset.publicName.ko}: ${asset.risk} / ${asset.publication}. Không phải xác nhận pháp lý.`;
    records.append(p);
  }
  toggle.addEventListener("click", () => {
    records.hidden = !records.hidden;
    toggle.setAttribute("aria-expanded", String(!records.hidden));
  });
  report.append(toggle, records);
  document.querySelector("#settings > div")?.append(report);
  return () => report.remove();
}
