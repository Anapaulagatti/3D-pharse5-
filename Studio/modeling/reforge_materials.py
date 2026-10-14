"""Small original PBR maps for v0.5 only. Reuses cached deterministic PNGs.
No external photos/material libraries; all pixels derive from the functions below.
"""
import bpy, math, random, json, hashlib
from math import pi
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
TEXTURES=ROOT/'assets/v0.5/textures'

def linear(v):return v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4
def original_maps(name,kind,hexcolor='FFFFFF',seed=505,size=256):
 TEXTURES.mkdir(parents=True,exist_ok=True)
 result={};paths={role:TEXTURES/f'{name}-{role}.png' for role in ['color','roughness','normal']}
 metadata=TEXTURES/f'{name}-source.json';inputs={'generator':'original-pbr-v05-1','kind':kind,'hexcolor':hexcolor,'seed':seed,'size':size}
 if all(p.exists() for p in paths.values()):
  if not metadata.exists():raise RuntimeError('Unrecorded texture cache; preserve files and use a new versioned name: '+name)
  saved=json.loads(metadata.read_text())
  if saved['inputs']!=inputs:raise RuntimeError('Texture inputs changed; choose a new versioned map name: '+name)
  for role,p in paths.items():
   if hashlib.sha256(p.read_bytes()).hexdigest()!=saved['sha256'][role]:raise RuntimeError('Texture cache checksum mismatch: '+str(p))
  for role,p in paths.items():
   image=bpy.data.images.load(str(p),check_existing=True);image.colorspace_settings.name='sRGB' if role=='color' else 'Non-Color';image.pack();result[role]=image
  return result
 rng=random.Random(seed);noise=[[rng.uniform(-1,1) for x in range(size)] for y in range(size)]
 def height(x,y):
  n=noise[y%size][x%size]
  if kind=='wood':return .50+.23*math.sin(x*.20+.9*math.sin(y*.033))+.10*math.sin(x*.68+y*.014)+.06*n
  if kind=='cloth':return .5+.13*math.sin(x*pi/2)+.13*math.sin(y*pi/2)+.04*n
  if kind=='paper':return .5+.08*math.sin(x*.36+y*.055)+.12*n
  if kind=='tile':return .5+.07*math.sin(x*.08)+.10*n
  return .5+.13*math.sin(x*.053)*math.cos(y*.071)+.13*n
 rgb=[linear(int(hexcolor[i:i+2],16)/255) for i in (0,2,4)]
 pixels={k:[] for k in paths}
 for y in range(size):
  for x in range(size):
   h=height(x,y);shade=.87+.13*h
   pixels['color'].extend([c*shade for c in rgb]+[1])
   rough=(.90+.08*h) if kind=='paper' else (.82+.12*h) if kind=='cloth' else (.64+.20*h) if kind=='wood' else (.55+.20*h) if kind=='tile' else (.78+.18*h)
   pixels['roughness'].extend([rough,rough,rough,1])
   dx=(height(x+1,y)-height(x-1,y))*.25;dy=(height(x,y+1)-height(x,y-1))*.25
   norm=math.sqrt(dx*dx+dy*dy+1)
   pixels['normal'].extend([.5-dx/norm*.5,.5-dy/norm*.5,.5+1/norm*.5,1])
 for role,p in paths.items():
  image=bpy.data.images.new(name+'_'+role,width=size,height=size,alpha=False)
  image.colorspace_settings.name='sRGB' if role=='color' else 'Non-Color';image.pixels[:]=pixels[role];image.filepath_raw=str(p);image.file_format='PNG';image.save();image.pack();result[role]=image
 metadata.write_text(json.dumps({'inputs':inputs,'source':'Studio/modeling/reforge_materials.py','license':'project-owned-original','external_source':None,'sha256':{role:hashlib.sha256(p.read_bytes()).hexdigest() for role,p in paths.items()},'color_spaces':{'color':'sRGB','roughness':'Non-Color','normal':'Non-Color'}},indent=2)+'\n')
 return result

def textured(mat,name,kind,hexcolor='FFFFFF',seed=505,vertex_color=False):
 maps=original_maps(name,kind,hexcolor,seed);nodes=mat.node_tree.nodes;links=mat.node_tree.links;p=nodes.get('Principled BSDF')
 for role,image in maps.items():
  node=nodes.new('ShaderNodeTexImage');node.image=image
  if role=='color':
   if vertex_color:
    attr=next((n for n in nodes if n.type=='VERTEX_COLOR'),None)
    if not attr:attr=nodes.new('ShaderNodeVertexColor');attr.layer_name='Color'
    mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1
    links.new(node.outputs['Color'],mix.inputs[1]);links.new(attr.outputs['Color'],mix.inputs[2]);links.new(mix.outputs[0],p.inputs['Base Color'])
   else:links.new(node.outputs['Color'],p.inputs['Base Color'])
  elif role=='roughness':links.new(node.outputs['Color'],p.inputs['Roughness'])
  else:
   normal=nodes.new('ShaderNodeNormalMap');normal.inputs['Strength'].default_value=.35;links.new(node.outputs['Color'],normal.inputs['Color']);links.new(normal.outputs[0],p.inputs['Normal'])
 return mat

def surface_uv(o,scale=.45):
 if o.type!='MESH':return
 mesh=o.data;uv=mesh.uv_layers.get('UVMap') or mesh.uv_layers.new(name='UVMap')
 bpy.context.view_layer.update()
 dims=o.dimensions;long=max(range(3),key=lambda i:dims[i])
 for face in mesh.polygons:
  normal=o.matrix_world.to_3x3()@face.normal;major=max(range(3),key=lambda i:abs(normal[i]))
  axes=[i for i in range(3) if i!=major]
  if long in axes:axes=[next(a for a in axes if a!=long),long]
  for index in face.loop_indices:
   p=o.matrix_world@mesh.vertices[mesh.loops[index].vertex_index].co
   uv.data[index].uv=(p[axes[0]]*scale,p[axes[1]]*scale)
 mesh.update()
