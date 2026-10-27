import source from "../../assets-src/npcs/phase3a/registry.json";
import dialogueSource from "../../assets-src/npcs/phase3a/dialogues.json";
import { characterRegistry } from "../characters/registry";
import {
  npcSchema,
  dialogueSchema,
  type NPCDefinition,
  type DialogueNode,
} from "./types";
export class NPCRegistry {
  readonly npcs: readonly NPCDefinition[];
  readonly nodes: ReadonlyMap<string, DialogueNode>;
  constructor(
    definitions: readonly unknown[] = source.npcs,
    nodes: readonly unknown[] = dialogueSource.nodes,
  ) {
    this.npcs = definitions.map((d) => npcSchema.parse(d));
    for (const npc of this.npcs)
      for (const [x, y] of [
        npc.spawn,
        npc.interactionPosition,
        npc.reviewSpawn,
        ...npc.route,
      ])
        if (x < 0 || y < 0 || x >= 4352 || y >= 4864)
          throw Error("NPC point outside canonical world");
    const ids = this.npcs.map((n) => n.id);
    if (
      new Set(ids).size !== ids.length ||
      ids.some((id) => characterRegistry.get(id))
    )
      throw Error("Duplicate/conflicting NPC ID");
    const parsed = nodes.map((n) => dialogueSchema.parse(n));
    this.nodes = new Map(parsed.map((n) => [n.id, n]));
    if (this.nodes.size !== parsed.length) throw Error("Duplicate dialogue ID");
    const reachable = new Set<string>();
    for (const npc of this.npcs) {
      const visiting = new Set<string>();
      const walk = (id: string) => {
        if (visiting.has(id)) throw Error("Dialogue cycle");
        const n = this.nodes.get(id);
        if (!n || n.npcId !== npc.id)
          throw Error("Missing/cross-owned dialogue node");
        if (reachable.has(id)) return;
        visiting.add(id);
        for (const next of [n.next, ...n.choices.map((c) => c.next)])
          if (next) walk(next);
        visiting.delete(id);
        reachable.add(id);
      };
      walk(npc.dialogueId);
    }
    if (reachable.size !== this.nodes.size)
      throw Error("Orphaned dialogue node");
  }
  get(id: string) {
    return this.npcs.find((n) => n.id === id);
  }
}
export const npcRegistry = new NPCRegistry();
