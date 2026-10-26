import type { CharacterRegistry } from "./registry";
export const PREFERENCES_KEY = "korean-arena-player-preferences-v1";
export interface PreferenceStorage {
  getItem(key: string): string | null;
  setItem(key: string, value: string): void;
}
export class CharacterPreferences {
  constructor(
    private readonly storage: PreferenceStorage | undefined,
    private readonly registry: CharacterRegistry,
  ) {}
  read() {
    try {
      const raw = this.storage?.getItem(PREFERENCES_KEY);
      if (!raw)
        return {
          characterId: "juni",
          needsSelection: true,
          reason: this.storage ? "missing" : "unavailable",
        };
      const q: unknown = JSON.parse(raw);
      if (
        typeof q !== "object" ||
        q === null ||
        !("version" in q) ||
        q.version !== 1 ||
        !("characterId" in q) ||
        typeof q.characterId !== "string"
      )
        return { characterId: "juni", needsSelection: true, reason: "invalid" };
      const d = this.registry.get(q.characterId);
      if (d?.availability.status !== "playable")
        return {
          characterId: "juni",
          needsSelection: true,
          reason: "unknown-or-incomplete",
        };
      return { characterId: d.id, needsSelection: false, reason: "saved" };
    } catch {
      return {
        characterId: "juni",
        needsSelection: true,
        reason: "unavailable-or-corrupt",
      };
    }
  }
  save(characterId: string) {
    const def = this.registry.get(characterId);
    if (def?.availability.status !== "playable") return false;
    try {
      if (!this.storage) return false;
      this.storage.setItem(
        PREFERENCES_KEY,
        JSON.stringify({ version: 1, characterId }),
      );
      return true;
    } catch {
      return false;
    }
  }
}
export function browserPreferenceStorage() {
  try {
    return window.localStorage;
  } catch {
    return undefined;
  }
}
