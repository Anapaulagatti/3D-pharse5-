"""Retain actually installed third-party notices in isolated release packages."""
from pathlib import Path
import re,hashlib,json
R=Path.cwd()
def write_notices(out):
 out=Path(out);p=out/'licenses/THIRD_PARTY_ADDITIONS.txt';p.parent.mkdir(parents=True,exist_ok=True)
 chunks=[];records=[]
 for rel in ['node_modules/eventemitter3/LICENSE','node_modules/phaser/src/physics/matter-js/lib/license.js','node_modules/phaser/src/geom/polygon/Earcut.js','node_modules/phaser/src/geom/polygon/Simplify.js','node_modules/phaser/src/math/HashSimplex.js','node_modules/phaser/src/renderer/webgl/shaders/src/NoiseSimplex2D.frag','node_modules/phaser/src/renderer/webgl/shaders/src/NoiseSimplex3D.frag']:
  b=(R/rel).read_bytes();t=b.decode();blocks=[t]if rel.endswith('/LICENSE')else [m.group()for m in re.finditer(r'/\*[\s\S]*?\*/|(?:^[ \t]*//[^\n]*\n?)+',t,re.M)if re.search(r'Copyright \(c\)|ISC License|The MIT License',m.group())]
  assert blocks,rel
  chunks.append('SOURCE: '+rel+'\n'+'\n\n'.join(blocks));records.append({'source':rel,'sha256':hashlib.sha256(b).hexdigest(),'noticeBlocks':len(blocks)})
 p.write_text('Third-party notices retained from the installed locked packages. Some components may be unused; inclusion does not assert use of every module.\n\n'+'\n\n'.join(chunks)+'\n')
 return records
if __name__=='__main__':
 import sys
 print(json.dumps(write_notices(sys.argv[1]),indent=2))
