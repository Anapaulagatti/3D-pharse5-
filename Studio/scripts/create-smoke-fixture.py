"""Toolchain fixture only; not a final art asset. Run with Blender --background."""
from pathlib import Path
import bpy

output = Path(__file__).resolve().parents[1] / '.cache' / 'smoke'
output.mkdir(parents=True, exist_ok=True)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, location=(0, 0, 0.6))
body = bpy.context.object
body.name = 'ToolchainFixture'
body.scale = (0.6, 0.5, 0.6)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
material = bpy.data.materials.new('Celadon')
material.use_nodes = True
principled = material.node_tree.nodes.get('Principled BSDF')
principled.inputs['Base Color'].default_value = (0.17, 0.52, 0.40, 1)
principled.inputs['Roughness'].default_value = 0.35
body.data.materials.append(material)
for face in body.data.polygons:
    face.use_smooth = True
bpy.ops.wm.save_as_mainfile(filepath=str(output / 'toolchain-fixture.blend'))
bpy.ops.export_scene.gltf(filepath=str(output / 'toolchain-fixture.glb'),
                          export_format='GLB', export_yup=True, export_animations=False)
print('FIXTURE_EXPORTED', output / 'toolchain-fixture.glb')
