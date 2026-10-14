import bpy,json,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[2];out=root/'quality-reports/v0.5';records=[]
for rel in ['assets/source-blend/arena-hero.blend','assets/source-blend/mascot-base.blend','assets/v0.3/source-blend/hanok-polish.blend','assets/v0.4/source-blend/hanok-living.blend','assets/v0.4/source-blend/mascot-living.blend']:
 p=root/rel;before=hashlib.sha256(p.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(p))
 objects=list(bpy.context.scene.objects)
 records.append({'file':rel,'sha256_before':before,'sha256_after':hashlib.sha256(p.read_bytes()).hexdigest(),'objects':len(objects),'mesh_objects':sum(o.type=='MESH' for o in objects),'armatures':[{'name':o.name,'bones':len(o.data.bones)} for o in objects if o.type=='ARMATURE'],'mesh_skin_modifiers':sum(m.type=='ARMATURE' for o in objects for m in o.modifiers),'shape_key_meshes':[o.name for o in objects if o.type=='MESH' and o.data.shape_keys],'clips':sorted({t.name for o in objects if o.animation_data for t in o.animation_data.nla_tracks}),'packed_images':[i.name for i in bpy.data.images if i.packed_file],'source_written':False})
 assert before==records[-1]['sha256_after']
(out/'blender-source-audit.json').write_text(json.dumps({'status':'READ_ONLY_INSPECTION_COMPLETE','files':records,'limitation':'No asset regeneration, deformation proof or new v0.5 render is claimed.'},indent=2)+'\n')
print('V05_BASELINE_BLEND_READ_ONLY',len(records),'files; source bytes unchanged')
