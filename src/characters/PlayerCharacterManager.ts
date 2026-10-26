import { RegistryMotion } from "./RegistryMotion";
import { JuniMotion } from "../engine/JuniMotion";
import { characterRegistry, type CharacterRegistry } from "./registry";
import type { CharacterDefinition } from "./types";
import type { CharacterPreferences } from "./preferences";
export interface PlayerSprite {
  setPosition(x: number, y: number): this;
  setDepth(depth: number): this;
  setFrame(name: string): this;
  setVisible(visible: boolean): this;
  destroy(): void;
}
export interface CharacterAssets {
  ensure(def: CharacterDefinition): Promise<void>;
}
export interface PlayerLocation {
  x: number;
  y: number;
}
/** Avatar ownership only. Controller, camera, world collision and account progress
 * remain scene-owned and are never reset by character selection. */
export class PlayerCharacterManager<S extends PlayerSprite> {
  private active: S;
  private definition: CharacterDefinition;
  private closed = false;
  private loading = false;
  private transitioning = false;
  private pose: JuniMotion | RegistryMotion;
  constructor(
    private readonly assets: CharacterAssets,
    private readonly create: (
      def: CharacterDefinition,
      position: PlayerLocation,
    ) => S,
    private readonly preferences: CharacterPreferences,
    initial: CharacterDefinition,
    position: PlayerLocation,
    private readonly registry: CharacterRegistry = characterRegistry,
  ) {
    this.definition = initial;
    this.pose =
      initial.id === "juni" ? new JuniMotion() : new RegistryMotion(initial);
    this.active = this.create(initial, position);
  }
  get sprite() {
    return this.active;
  }
  get selected() {
    return this.definition;
  }
  get motion() {
    return this.pose;
  }
  get busy() {
    return this.loading || this.transitioning || this.closed;
  }
  setTransitioning(value: boolean) {
    this.transitioning = value;
  }
  async select(id: string, location: PlayerLocation) {
    if (this.busy)
      throw Error("Character switch unavailable during scene transition");
    const requested = this.registry.get(id);
    if (requested?.availability.status === "incomplete")
      throw Error("Character art is incomplete");
    const next = this.registry.resolve(id);
    if (next.id === this.definition.id) {
      return { characterId: next.id, saved: this.preferences.save(next.id) };
    }
    this.loading = true;
    try {
      await this.assets.ensure(next);
      if (this.closed || this.transitioning)
        throw Error("Scene changed while loading character");
      const sprite = this.create(next, location).setVisible(false);
      const old = this.active;
      this.active = sprite;
      this.definition = next;
      this.pose =
        next.id === "juni" ? new JuniMotion() : new RegistryMotion(next);
      old.destroy();
      sprite.setVisible(true);
      return { characterId: next.id, saved: this.preferences.save(next.id) };
    } finally {
      this.loading = false;
    }
  }
  dispose() {
    if (this.closed) return;
    this.closed = true;
    this.active.destroy();
  }
}
