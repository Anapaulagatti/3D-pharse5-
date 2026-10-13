"""Render the saved production mascot as a real transparent PNG, not concept art."""
from pathlib import Path
import bpy

root=Path(__file__).resolve().parents[2]
bpy.ops.wm.open_mainfile(filepath=str(root/'assets/source-blend/mascot-base.blend'))
# Only Idle is active for the neutral portrait; all six clips remain in the .blend.
for obj in bpy.context.scene.objects:
    if obj.animation_data:
        for track in obj.animation_data.nla_tracks:
            track.mute=track.name!='Idle'
bpy.context.scene.frame_set(1)
bpy.context.scene.render.film_transparent=True
bpy.context.scene.render.image_settings.file_format='PNG'
bpy.context.scene.render.image_settings.color_mode='RGBA'
bpy.context.scene.cycles.samples=96
bpy.context.scene.cycles.use_denoising=False
output=root/'assets/posters/mascot-transparent.png'
output.parent.mkdir(parents=True,exist_ok=True)
bpy.context.scene.render.filepath=str(output)
bpy.ops.render.render(write_still=True)
print('TRANSPARENT_MASCOT_RENDER_SAVED',output)
