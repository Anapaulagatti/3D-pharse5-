import { characterRegistry, type CharacterRegistry } from "./registry";
/** One browser-session avatar choice survives Phaser scene lifetimes, including
 * when localStorage is blocked. No account/progress data is stored here. */
export class CharacterSession {
  private characterId: string;
  private confirmed: boolean;
  constructor(
    seed: { characterId: string; needsSelection: boolean },
    private readonly registry: CharacterRegistry = characterRegistry,
  ) {
    this.characterId = registry.resolve(seed.characterId).id;
    this.confirmed = !seed.needsSelection;
  }
  get selected() {
    return this.registry.resolve(this.characterId);
  }
  get needsSelection() {
    return !this.confirmed;
  }
  commit(characterId: string) {
    const def = this.registry.get(characterId);
    if (def?.availability.status !== "playable")
      throw Error("Incomplete or unknown character cannot enter session");
    this.characterId = def.id;
    this.confirmed = true;
  }
}
