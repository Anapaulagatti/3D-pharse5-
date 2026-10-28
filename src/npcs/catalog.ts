import modern from "../../assets-src/npcs/phase3a-npc-expansion/modern-definitions.json";
import additions from "../../assets-src/npcs/phase3a-npc-expansion/dialogue-additions.json";
import metadata from "../../assets-src/npcs/phase3a-npc-expansion/encounter-metadata.json";
import { NPCRegistry, npcRegistry } from "./registry";
import type { ModernVisitorMetadata } from "./collections";
/** Original resident singleton/data remains14 for backwards compatibility.
 * Compose the actual runtime catalog through the SAME validated Registry class.
 * No archived historical figure is activated without verified facts and finished art.
 */
const roots = new Map(additions.rootExtensions.map((r) => [r.rootId, r]));
const nodes = [...npcRegistry.nodes.values()].map((n) => {
  const extension = roots.get(n.id);
  return extension
    ? { ...n, choices: [...n.choices, ...extension.choices] }
    : n;
});
export const npcCatalog = new NPCRegistry(
  [...npcRegistry.npcs, ...modern.npcs],
  [...nodes, ...additions.nodes],
);
export const modernVisitors: readonly ModernVisitorMetadata[] = metadata.map(
  (m) => {
    const npc = npcCatalog.get(m.id);
    const host = npcRegistry.get(m.hostResidentId);
    if (
      !npc ||
      !host ||
      host.homeZone !== npc.homeZone ||
      m.realPerson ||
      m.licensedCameo
    )
      throw Error("Invalid original visitor ownership/host registration");
    return {
      id: m.id,
      category: "modern-fictional",
      hostResidentId: host.id,
      homeZone: npc.homeZone,
      rights: "original-fictional",
      realPerson: false,
      licensedCameo: false,
    };
  },
);
export const npcLearningTeasers = additions.learning;
