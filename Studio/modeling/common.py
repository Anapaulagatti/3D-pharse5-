"""Original Living Hangeul District geometry and material helpers (Blender 4.3+)."""
from pathlib import Path
from math import sin, cos, pi
import random
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
PALETTE = {'jade': '72BEAC', 'jade_dark': '4C8E81', 'cream': 'F5EFE1',
           'ink': '293C55', 'navy': '15243A', 'coral': 'E57B69', 'brass': 'CFAC67',
           'wood': '8D6549', 'wood_light': 'BA9168', 'stone': 'D2CDBD',
           'haze': 'AFC7E0', 'haze_dark': '839EB5', 'amber': 'FFE1A0'}


def reset():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for item in list(bpy.data.materials):
        bpy.data.materials.remove(item)
    bpy.context.scene.render.fps = 30
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = 91
    bpy.context.scene.unit_settings.system = 'METRIC'
    bpy.context.scene.world.color = (0.22, 0.25, 0.28)


def color(hexcode):
    values = [int(hexcode[i:i+2], 16)/255 for i in (0, 2, 4)]
    return tuple(v/12.92 if v <= 0.04045 else ((v+.055)/1.055)**2.4 for v in values) + (1,)


def grain(name, base, seed, strength=.035):
    path = ROOT / 'assets/textures' / f'{name}.png'
    path.parent.mkdir(parents=True, exist_ok=True)
    rng = random.Random(seed)
    rgb = [int(base[i:i+2], 16)/255 for i in (0, 2, 4)]
    image = bpy.data.images.new(name, width=256, height=256, alpha=False)
    pixels = []
    for y in range(256):
        for x in range(256):
            noise = rng.uniform(-strength, strength) + sin(x*.48+y*.03)*strength*.25
            pixels.extend([min(1, max(0, c+noise)) for c in rgb] + [1])
    image.pixels[:] = pixels
    image.filepath_raw = str(path)
    image.file_format = 'PNG'
    image.save()
    image.pack()
    return image


def material(name, hexcode, roughness=.7, metallic=0, texture=None, emission=0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    m.diffuse_color = color(hexcode)
    p = m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value = color(hexcode)
    p.inputs['Roughness'].default_value = roughness
    p.inputs['Metallic'].default_value = metallic
    if texture:
        t = m.node_tree.nodes.new('ShaderNodeTexImage')
        t.image = texture
        m.node_tree.links.new(t.outputs['Color'], p.inputs['Base Color'])
    if emission:
        p.inputs['Emission Color'].default_value = color(hexcode)
        p.inputs['Emission Strength'].default_value = emission
    return m


def materials():
    paper = grain('hanji-grain', PALETTE['cream'], 73, .025)
    stone = grain('courtyard-stone', PALETTE['stone'], 91, .025)
    mats = {n: material(n, h, .7) for n, h in PALETTE.items()}
    mats['jade'] = material('CeladonEnamel', PALETTE['jade'], .3, .05)
    mats['jade_dark'] = material('DeepCeladon', PALETTE['jade_dark'], .38, .04)
    mats['brass'] = material('BrassInlay', PALETTE['brass'], .34, .65)
    mats['paper'] = material('HanjiPaper', PALETTE['cream'], .92, texture=paper)
    mats['stone'] = material('CourtyardStone', PALETTE['stone'], .85, texture=stone)
    mats['glow'] = material('PaperLight', PALETTE['amber'], .85, emission=.8)
    return mats


def finish(obj, name, mat, parent=None):
    obj.name = name
    if mat:
        obj.data.materials.clear()
        obj.data.materials.append(mat)
    if parent:
        obj.parent = parent
    return obj


def box(name, loc, size, mat, bevel=.03, parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object
    o.dimensions = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        mod = o.modifiers.new('CraftedEdges', 'BEVEL')
        mod.width = bevel
        mod.segments = 2
        bpy.ops.object.modifier_apply(modifier=mod.name)
        mod = o.modifiers.new('WeightedNormals', 'WEIGHTED_NORMAL')
        bpy.ops.object.modifier_apply(modifier=mod.name)
    return finish(o, name, mat, parent)


def sphere(name, loc, scale, mat, segments=24, rings=12, parent=None):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, radius=1, location=loc)
    o = bpy.context.object
    o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    for f in o.data.polygons:
        f.use_smooth = True
    return finish(o, name, mat, parent)


def cylinder(name, loc, radius, depth, mat, vertices=24, parent=None, radius2=None):
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=radius, radius2=radius if radius2 is None else radius2,
                                    depth=depth, location=loc)
    o = bpy.context.object
    for f in o.data.polygons:
        f.use_smooth = len(f.vertices) == 4
    return finish(o, name, mat, parent)


def mesh(name, verts, faces, mat, parent=None, smooth=False):
    data = bpy.data.meshes.new(name)
    data.from_pydata(verts, [], faces)
    data.update()
    uv = data.uv_layers.new(name='UVMap')
    for p in data.polygons:
        p.use_smooth = smooth
        for idx in p.loop_indices:
            co = data.vertices[data.loops[idx].vertex_index].co
            uv.data[idx].uv = (co.x*.3, co.y*.3)
    o = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(o)
    return finish(o, name, mat, parent)


def path(name, points, radius, mat, parent=None):
    c = bpy.data.curves.new(name, 'CURVE')
    c.dimensions = '3D'
    c.resolution_u = 1
    c.bevel_depth = radius
    c.bevel_resolution = 1
    spline = c.splines.new('POLY')
    spline.points.add(len(points)-1)
    for point, xyz in zip(spline.points, points):
        point.co = (*xyz, 1)
    o = bpy.data.objects.new(name, c)
    bpy.context.collection.objects.link(o)
    bpy.ops.object.select_all(action='DESELECT')
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.convert(target='MESH')
    return finish(bpy.context.object, name, mat, parent)


def ring(name, radius, z, thickness, mat, center=(0, 0), waves=0, parent=None):
    points = []
    for i in range(65):
        a = i/64*2*pi
        r = radius + waves*cos(a*8)
        points.append((center[0]+r*cos(a), center[1]+r*sin(a), z+waves*sin(a*8)*.35))
    return path(name, points, thickness, mat, parent)


def lathe(name, profile, mat, segments=48, parent=None):
    verts = [(r*cos(i/segments*2*pi), r*sin(i/segments*2*pi), z)
             for z, r in profile for i in range(segments)]
    faces = []
    for j in range(len(profile)-1):
        for i in range(segments):
            k = j*segments+i
            next_i = j*segments+(i+1)%segments
            faces.append((k, next_i, next_i+segments, k+segments))
    faces.extend([tuple(reversed(range(segments))), tuple(range((len(profile)-1)*segments, len(profile)*segments))])
    o = mesh(name, verts, faces, mat, parent, True)
    for p in o.data.polygons:
        for idx in p.loop_indices:
            v = o.data.loops[idx].vertex_index
            o.data.uv_layers.active.data[idx].uv = ((v % segments)/segments, (v//segments)/(len(profile)-1))
    return o


def empty(name, loc=(0, 0, 0), parent=None):
    o = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(o)
    o.location = loc
    o.parent = parent
    return o


def join(name, objects):
    objects = [o for o in objects if o.type == 'MESH']
    if not objects:
        return None
    bpy.ops.object.select_all(action='DESELECT')
    for o in objects:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.object.join()
    objects[0].name = name
    return objects[0]


def animation(obj, clip, frames):
    obj.animation_data_create()
    action = bpy.data.actions.new(f'{clip}_{obj.name}')
    obj.animation_data.action = action
    original = (obj.location.copy(), obj.rotation_euler.copy(), obj.scale.copy())
    for frame, values in frames:
        for prop, value in values.items():
            setattr(obj, prop, value)
            obj.keyframe_insert(data_path=prop, frame=frame, group=obj.name)
    for curve in action.fcurves:
        for point in curve.keyframe_points:
            point.interpolation = 'BEZIER'
    track = obj.animation_data.nla_tracks.new()
    track.name = clip
    strip = track.strips.new(clip, 1, action)
    strip.blend_type = 'REPLACE'
    obj.animation_data.action = None
    obj.location, obj.rotation_euler, obj.scale = original


def save_export(name):
    src = ROOT / 'assets/source-blend' / f'{name}.blend'
    out = ROOT / 'assets/models' / f'{name}.glb'
    src.parent.mkdir(parents=True, exist_ok=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    bpy.context.scene.frame_set(1)
    bpy.ops.wm.save_as_mainfile(filepath=str(src))
    bpy.ops.export_scene.gltf(filepath=str(out), export_format='GLB', export_yup=True,
                             export_animations=True, export_animation_mode='NLA_TRACKS',
                             export_nla_strips=True, export_force_sampling=True,
                             export_cameras=False, export_lights=False)
    print('PRODUCTION_ASSET_SAVED', name, out.stat().st_size)


def lighting_camera(loc=(9, -12, 10), target=(0, 0, 1), orthoscale=13):
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 32
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 1200
    scene.render.resolution_y = 1000
    scene.render.resolution_percentage = 100
    for name, position, energy, size, tint in [
        ('Key', (2, -5, 9), 1100, 7, (1, .84, .65)),
        ('Fill', (-5, -1, 6), 800, 6, (.69, .82, 1)),
        ('Rim', (1, 5, 7), 1000, 5, (.97, .85, .68))]:
        light = bpy.data.lights.new(name, 'AREA')
        light.energy = energy
        light.shape = 'DISK'
        light.size = size
        light.color = tint
        o = bpy.data.objects.new(name, light)
        bpy.context.collection.objects.link(o)
        o.location = position
        o.rotation_euler = (Vector(target)-o.location).to_track_quat('-Z', 'Y').to_euler()
    camera = bpy.data.cameras.new('StudioCamera')
    camera.type = 'ORTHO'
    camera.ortho_scale = orthoscale
    o = bpy.data.objects.new('StudioCamera', camera)
    bpy.context.collection.objects.link(o)
    o.location = loc
    o.rotation_euler = (Vector(target)-o.location).to_track_quat('-Z', 'Y').to_euler()
    scene.camera = o
    scene.view_settings.view_transform = 'AgX'
    scene.render.image_settings.file_format = 'PNG'
    scene.render.film_transparent = True
