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
export const MAX_APPEARANCE_PRESETS = 12;
export interface AppearanceRepository {
  read(characterId: string): CharacterAppearance;
  presets(): AppearancePreset[];
  save(appearance: CharacterAppearance, name?: string): boolean;
  renamePreset(id: string, name: string): boolean;
  deletePreset(id: string): boolean;
}
interface AppearanceStore {
  version: 2;
  selectedCharacterId: string;
  appearances: Record<string, CharacterAppearance>;
  presets: AppearancePreset[];
}
export class AppearancePreferences implements AppearanceRepository {
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
        for (const p of value.presets.slice(0, MAX_APPEARANCE_PRESETS)) {
          if (
            p &&
            typeof p.id === "string" &&
            p.id.length < 80 &&
            typeof p.name === "string" &&
            p.name.trim() &&
            !fallback.presets.some((v) => v.id === p.id) &&
            !this.manifest.presets.some((v) => v.id === p.id) &&
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
  userPresets() {
    return this.presets().filter((p) =>
      this.readStore().presets.some((u) => u.id === p.id),
    );
  }
  isUserPreset(id: string) {
    return this.readStore().presets.some((p) => p.id === id);
  }
  canSavePreset(name: string) {
    const clean = name.trim().replace(/\s+/g, " ").slice(0, 32);
    return (
      !clean ||
      this.readStore().presets.some((p) => p.name === clean) ||
      this.readStore().presets.length < MAX_APPEARANCE_PRESETS
    );
  }
  private writeStore(next: AppearanceStore) {
    this.memory = next;
    try {
      if (!this.storage) return false;
      this.storage.setItem(APPEARANCE_PREFERENCES_KEY, JSON.stringify(next));
      return true;
    } catch {
      return false;
    }
  }
  renamePreset(id: string, name: string) {
    const clean = name.trim().replace(/\s+/g, " ").slice(0, 32),
      next = structuredClone(this.readStore());
    if (!clean || next.presets.some((p) => p.id !== id && p.name === clean))
      return false;
    const item = next.presets.find((p) => p.id === id);
    if (!item) return false;
    item.name = clean;
    return this.writeStore(next);
  }
  deletePreset(id: string) {
    const next = structuredClone(this.readStore());
    if (!next.presets.some((p) => p.id === id)) return false;
    next.presets = next.presets.filter((p) => p.id !== id);
    return this.writeStore(next);
  }
  save(appearance: CharacterAppearance, name?: string) {
    const def = this.registry.get(appearance.characterId);
    if (def?.availability.status !== "playable") return false;
    const next = structuredClone(this.readStore());
    next.appearances[def.id] = normalizeAppearance(
      def.id,
      appearance,
      this.manifest,
    );
    next.selectedCharacterId = def.id;
    if (name?.trim()) {
      const clean = name.trim().replace(/\s+/g, " ").slice(0, 32),
        existing = next.presets.find((p) => p.name === clean);
      if (!existing && next.presets.length >= MAX_APPEARANCE_PRESETS)
        return false;
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
      ].slice(-MAX_APPEARANCE_PRESETS);
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
