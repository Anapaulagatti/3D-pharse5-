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

// Additive store: the accepted v1 key/read format remains intact and readable.
import {
  defaultAppearance,
  normalizeAppearance,
  appearanceManifest,
} from "./appearance";
import type {
  AppearanceManifest,
  AppearancePreset,
  CharacterAppearance,
} from "./appearanceTypes";
export const APPEARANCE_PREFERENCES_KEY =
  "korean-arena-appearance-preferences-v2";
interface AppearanceStore {
  version: 2;
  selectedCharacterId: string;
  appearances: Record<string, CharacterAppearance>;
  presets: AppearancePreset[];
}
export class AppearancePreferences {
  private memory: AppearanceStore | undefined;
  constructor(
    private storage: PreferenceStorage | undefined,
    private registry: CharacterRegistry,
    private manifest: AppearanceManifest = appearanceManifest,
  ) {}
  private readStore(): AppearanceStore {
    if (this.memory) return this.memory;
    const fallback: AppearanceStore = {
      version: 2,
      selectedCharacterId: new CharacterPreferences(
        this.storage,
        this.registry,
      ).read().characterId,
      appearances: {},
      presets: [],
    };
    try {
      const value = JSON.parse(
        this.storage?.getItem(APPEARANCE_PREFERENCES_KEY) ?? "null",
      );
      if (
        !value ||
        value.version !== 2 ||
        typeof value.appearances !== "object" ||
        value.appearances === null
      )
        return fallback;
      for (const def of this.registry.all)
        if (def.availability.status === "playable")
          fallback.appearances[def.id] = normalizeAppearance(
            def.id,
            value.appearances[def.id],
            this.manifest,
          );
      fallback.selectedCharacterId = this.registry.resolve(
        value.selectedCharacterId,
      ).id;
      if (Array.isArray(value.presets))
        for (const p of value.presets.slice(0, 8)) {
          if (
            p &&
            typeof p.id === "string" &&
            p.id.length < 80 &&
            typeof p.name === "string" &&
            p.name.trim() &&
            this.registry.get(p.appearance?.characterId)?.availability
              .status === "playable"
          )
            fallback.presets.push({
              id: p.id,
              name: p.name.trim().slice(0, 32),
              appearance: normalizeAppearance(
                p.appearance.characterId,
                p.appearance,
                this.manifest,
              ),
            });
        }
    } catch {
      /* Keep v1 selection and defaults; no destructive migration. */
    }
    return fallback;
  }
  read(characterId: string) {
    const id = this.registry.resolve(characterId).id;
    return normalizeAppearance(
      id,
      this.readStore().appearances[id] ?? defaultAppearance(id),
      this.manifest,
    );
  }
  presets() {
    return [...this.manifest.presets, ...this.readStore().presets].map((p) => ({
      ...p,
      appearance: {
        ...p.appearance,
        accessoryIds: [...p.appearance.accessoryIds],
      },
    }));
  }
  save(appearance: CharacterAppearance, name?: string) {
    const def = this.registry.get(appearance.characterId);
    if (def?.availability.status !== "playable") return false;
    const next = this.readStore();
    next.appearances[def.id] = normalizeAppearance(
      def.id,
      appearance,
      this.manifest,
    );
    next.selectedCharacterId = def.id;
    if (name?.trim()) {
      const clean = name.trim().slice(0, 32),
        existing = next.presets.find((p) => p.name === clean);
      const preset = {
        id:
          existing?.id ??
          `local-${Date.now().toString(36)}-${next.presets.length}`,
        name: clean,
        appearance: next.appearances[def.id],
      };
      next.presets = [
        ...next.presets.filter((p) => p.id !== preset.id),
        preset,
      ].slice(-8);
    }
    this.memory = next;
    try {
      if (!this.storage) return false;
      this.storage.setItem(APPEARANCE_PREFERENCES_KEY, JSON.stringify(next));
      return true;
    } catch {
      return false;
    }
  }
}
