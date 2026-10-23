import Phaser from "phaser";
/** Phaser4 TextureSource.setFilter reuploads pixels even when the GL filter is unchanged.
 * Create nearest once and skip only identical filter changes during synchronous ownership transfer.
 * No engine/library patch persists after this call; normal context-restoration ownership is retained. */
export function addNativeTexture(
  scene: Phaser.Scene,
  key: string,
  source: HTMLImageElement,
) {
  if (scene.game.renderer.type !== Phaser.WEBGL) {
    scene.textures.addImage(key, source);
    return;
  }
  const renderer = scene.game.renderer as Phaser.Renderer.WebGL.WebGLRenderer;
  const wrapper = renderer.createTextureFromSource(
    source,
    source.width,
    source.height,
    Phaser.Textures.FilterMode.NEAREST,
  );
  if (!wrapper) throw Error("Native GL texture creation failed");
  const setFilter = renderer.setTextureFilter;
  renderer.setTextureFilter = function (texture, filter) {
    const expected =
      filter === Phaser.Textures.FilterMode.NEAREST
        ? this.gl.NEAREST
        : this.gl.LINEAR;
    if (texture.minFilter === expected && texture.magFilter === expected)
      return this;
    return setFilter.call(this, texture, filter);
  };
  try {
    if (!scene.textures.addGLTexture(key, wrapper))
      throw Error("Native GL ownership transfer failed");
  } catch (error) {
    wrapper.destroy();
    throw error;
  } finally {
    renderer.setTextureFilter = setFilter;
  }
}
