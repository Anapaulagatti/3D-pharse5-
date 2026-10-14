import bpy,json,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[2];records=[]
for rel in ['assets/v0.5/source-blend/hanok-reforge.blend','assets/v0.5/source-blend/nari-messenger-art.blend']:
    p=root/rel;before=hashlib.sha256(p.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(p));objects=list(bpy.context.scene.objects)
    records.append({'file':rel,'sha256':before,'objects':len(objects),'meshes':sum(o.type=='MESH' for o in objects),'armatures':[{'name':o.name,'bones':len(o.data.bones)} for o in objects if o.type=='ARMATURE'],'morph_meshes':[{'name':o.name,'keys':list(o.data.shape_keys.key_blocks.keys())} for o in objects if o.type=='MESH' and o.data.shape_keys],'nla_tracks':sorted({t.name for o in objects if o.animation_data for t in o.animation_data.nla_tracks}),'packed_images':[i.name for i in bpy.data.images if i.packed_file],'source_written':False})
    assert hashlib.sha256(p.read_bytes()).hexdigest()==before
out=root/'quality-reports/v0.6/baseline';out.mkdir(parents=True,exist_ok=True)
(out/'blender.json').write_text(json.dumps({'status':'PASS_READ_ONLY_SOURCE_INSPECTION','files':records},indent=2)+'\n')
print('V06 current v0.5 Blender source audit complete; no file saved or asset regenerated.')
