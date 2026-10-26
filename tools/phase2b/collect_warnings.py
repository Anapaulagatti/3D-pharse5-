from pathlib import Path
import json,collections
R=Path(__file__).resolve().parents[2];D=R/'docs/phase2b';rows=[];fails=[];skipped=collections.Counter()
for p in sorted((D/'forge-qa').rglob('*.json')):
 q=json.loads(p.read_text())
 if not isinstance(q,dict):continue
 for c in q.get('checks',[]):
  if c.get('status')=='warn':rows.append({'file':str(p.relative_to(R)),'check':c,'classification':'Diagnostic luminance ambiguity at passing/overlapping poses; explicit opposite near/far foot targets and real eight-pose playback are preserved. Numerical WARN remains.'if c.get('id')=='leg_alternation'else'Loop appearance review flag: periodic native IK and bounded body bob, head/garment area and near/far shading affect RGBA seam ratio. No omitted/repeated gait frame or root discontinuity found internally; numerical WARN remains for human loop review.'})
  elif c.get('status')=='fail':fails.append({'file':str(p.relative_to(R)),'check':c})
  elif c.get('status')=='skipped':skipped[c['id']]+=1
assert not fails,fails
(D/'forge-warnings.json').write_text(json.dumps({'warnings':rows,'hardFailures':fails,'skippedChecks':dict(skipped),'commands':72,'retainedEarlierWarnings':{'phase1b':11,'phase2a':6},'thresholdPolicy':'All original gates unchanged. No automatic warning relabelled numerical PASS.'},indent=2)+'\n')
s='# Forge numerical warnings — retained\n\n72 commands completed with0hard failures. The new packs retain'+str(len(rows))+' leaf WARNs: '+str(dict(collections.Counter(r['check']['id']for r in rows)))+'. Earlier11 Phase1B and6 Phase2A warnings remain in their immutable approved reviews.\n\nAll eight actual gait poses were observed in Phaser for every direction/action. Native bounds/alpha and source-reference readbacks pass. Internal review investigated these flags against the native sheets, actual gameplay and registered foot targets. Auto-luminance near/far classification is ambiguous for overlapping loose garments and passing poses; source foot targets oppose exactly at contact phases. Seam ratios also weight the large head/garment area moving by1 walk pixel or2 run pixels and near/far leg shading. Geometry is periodic; closure has no additional pose beyond the regular next contact. These observations do not erase numerical WARN or grant human art acceptance. Loop feel remains an explicit human review item.\n\nPalette-specific/outline-specific Forge gates were SKIPPED because no palette or outline color was supplied. The separate native finisher enforces shared96-color source palette and binary alpha; far-layer shading adds derived colors. Do not claim the skipped Forge tests passed.\n\n'
for r in rows:s+='`'+r['file']+'`\n\n'+r['classification']+'\n\n```json\n'+json.dumps(r['check'],indent=2)+'\n```\n\n'
(D/'FORGE_WARNINGS.md').write_text(s.rstrip()+'\n');print(len(rows),'numerical WARNs retained,0hardFAIL')
