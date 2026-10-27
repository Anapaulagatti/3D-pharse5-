import Phaser from "phaser";
/** Read-only actual POST_RENDER observations. Never places an actor or changes animation/collision. */
export function installNPCAudit(
  scene: Phaser.Scene,
  snapshot: () => unknown,
  sprites: () => Phaser.GameObjects.Sprite[],
) {
  const capture = (id: string, prefix = "", timeoutMs = 12000) =>
    new Promise<unknown>((resolve) => {
      const done = (result: unknown) => {
        clearTimeout(timer);
        scene.game.events.off(Phaser.Core.Events.POST_RENDER, read);
        resolve(result);
      };
      const read = () => {
        const s = sprites().find(
          (s) =>
            s.getData("npcId") === id &&
            s.visible &&
            String(s.frame.name).startsWith(prefix),
        );
        if (!s) return;
        const c = scene.cameras.main;
        done({
          matched: true,
          npcId: id,
          actualFrame: String(s.frame.name),
          npc: snapshot(),
          player: window.__GATE3__,
          sprite: {
            x: s.x,
            y: s.y,
            depth: s.depth,
            scale: [s.scaleX, s.scaleY],
            sampling: s.frame.source.scaleMode,
            origin: [s.originX, s.originY],
          },
          camera: {
            zoom: c.zoom,
            scroll: [c.scrollX, c.scrollY],
            matrix: Array.from(c.matrixCombined.matrix),
          },
          png: scene.game.canvas.toDataURL("image/png"),
        });
      };
      const timer = setTimeout(
        () => done({ matched: false, npcId: id, prefix }),
        Math.max(100, Math.min(30000, timeoutMs)),
      );
      scene.game.events.on(Phaser.Core.Events.POST_RENDER, read);
    });
  window.__NPC_CAPTURE__ = capture;
  return () => {
    if (window.__NPC_CAPTURE__ === capture) delete window.__NPC_CAPTURE__;
  };
}
declare global {
  interface Window {
    __NPC_CAPTURE__?: (
      id: string,
      prefix?: string,
      timeoutMs?: number,
    ) => Promise<unknown>;
  }
}
