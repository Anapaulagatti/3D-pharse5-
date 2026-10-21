"""Read-only provenance diagnostic, never a production compiler input."""
import ast,hashlib,json,re
from pathlib import Path
R=Path(__file__).resolve().parents[1];S=R/'assets-src/v10-city';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();seen=set();edges=[];bad=[]
def scan(p):
 p=p.resolve()
 if p in seen:return
 seen.add(p)
 if p.suffix not in ['.ts','.css','.json']:return
 text=p.read_text()
 for ref in re.findall(r'(?:from\s*|import\s*)[\"\']([^\"\']+)[\"\']',text):
  if not ref.startswith('.'):continue
  dest=(p.parent/ref).resolve()
  if not dest.exists():dest=dest.with_suffix('.ts')
  edges.append([str(p.relative_to(R)),str(dest.relative_to(R))])
  if re.search(r'(?:v[1-9]-(?:world|city)|legacy)',str(dest)):bad.append(str(dest))
  if dest.is_file():scan(dest)
scan(R/'src/main.ts')
python=[]
for name in ['v10_final_build.py','v10_surfaces.py','v10_prepare_art.py','v10_plan.py']:
 p=R/'tools'/name;text=p.read_text();tree=ast.parse(text)
 refs=[n.module for n in ast.walk(tree)if isinstance(n,ast.ImportFrom)];python.append(dict(path=str(p.relative_to(R)),sha256=sha(p),imports=refs))
 assert not any(x in text for x in ['v9-world','v8-city','v7-world','v6-world','map_pipeline','v10_compare']),name
# Separate hash-only diagnostic: no bytes or coordinates from this index feed rendering.
legacy={}
for version in [f'v{i}-world'for i in range(1,10)]+[f'v{i}-city'for i in range(1,10)]:
 for p in (R/'assets-src'/version).rglob('*.png'):legacy.setdefault(sha(p),[]).append(str(p.relative_to(R)))
matches=[]
for p in list((S/'originals').glob('*.png'))+list((S/'native').glob('*.png')):
 if sha(p)in legacy:matches.append(dict(new=str(p.relative_to(R)),legacy=legacy[sha(p)]))
assert not bad and not matches,(bad,matches)
result=dict(status='PASS',scope='Active TypeScript imports and final Python entry/helpers; original/native SHA comparison only, recovery files remain inactive',references=edges,python=python,forbiddenProductionReferences=bad,newArtMatchesHistoricalHashes=matches,legacyDistinctPngHashes=len(legacy),planSha256=sha(S/'plan/city.json'),runtimeCaptureRequests=json.loads((R/'docs/v10-production/captures.json').read_text())['requests'])
(R/'docs/v10-production/final-source-audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k not in ['references','runtimeCaptureRequests','python']}))
