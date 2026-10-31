"""Assemble the final report only from verified stored evidence."""
from map_pipeline import *
Q=ROOT/'docs/v9-world';b=json.loads((SOURCE/'map/bundle.json').read_text());plan=json.loads((SOURCE/'plan/city.json').read_text());package=json.loads((Q/'package.json').read_text());video=json.loads((Q/'quality/video/encoding-verification.json').read_text());play=json.loads((Q/'quality/video/browser-playback.json').read_text());http=json.loads((Q/'quality/package/http-verification.json').read_text());clean=json.loads((Q/'quality/clean-setup.json').read_text());ci=json.loads((Q/'quality/source-ci-verified.json').read_text());assert all(j.get('status')=='PASS'for j in [video,play,http,clean,ci]);assert package['httpVerified']and video['playbackVerified'];assert video['capturedFrames']==video['encodedFrames']
commands=json.loads((SOURCE/'forge-commands.json').read_text());warn=[]
for p in (SOURCE/'art').rglob('*.json'):
 j=json.loads(p.read_text());q=j.get('qa',j)if isinstance(j,dict)else{}
 for c in q.get('checks',[]):
  if c.get('status')in['warn','fail']:warn.append({'file':str(p.relative_to(ROOT)),**c})
write(Q/'quality/art-warnings.json',warn)
site=json.loads((Q/'quality/public-site-preserved.json').read_text());perf=json.loads((Q/'quality/performance/profile.json').read_text());plots='\n'.join('| '+ ' | '.join([p['id'],str(p['site']),str(p['entrance']),p['asset']])+' |'for p in plan['plots']);warntext='\n'.join('- `'+json.dumps(w,ensure_ascii=False)+'`'for w in warn);performance='\n'.join(f"|{r['id']}|{r['renderer']}|{r['medianFrameMs']:.2f}|{r['p95FrameMs']:.2f}|{r['medianRafHz']:.2f}|"for r in perf['rows'])
text=f'''# V9 — completely new Korean city review candidate

**USER VISUAL APPROVAL PENDING.** The playable reconstruction and technical delivery are complete; the map is not locked, merged to main or publicly deployed.

## View it

Download [playable-review.zip](playable-review.zip), extract the entire **Korean-Arena-V9-World-Review** folder, run `python start.py` (Windows: `py start.py`), then open **http://localhost:8765/3D-pharse5-/v9-world-review.html** in a web browser. Alternative: `python -m http.server 8765` from the extracted root. Never file:// or a raw HTML viewer. Python3 required; no Node/account/API key for the package. Internal cloud localhost is not a public preview link.

- [Whole-world web preview](V9_WEB_OVERVIEW.png) / [actual native4352×6144 Phaser overview](quality/final/V9_FULL_WORLD_OVERVIEW.png).
- [Honest V8/V9 comparison](V8_V9_REAL_DIFFERENCE.png), [editable masterplan PNG](V9_NEW_CITY_MASTERPLAN.png), [SVG](../../assets-src/v9-world/plan/city.svg), [JSON](../../assets-src/v9-world/plan/city.json), [verified navigation](V9_NAVIGATION.png).
- Native actual-engine district crops: [city](V9_CITY_STREETS.png), [Namsan](V9_NAMSAN.png), [station](V9_STATION.png), [leisure campus](V9_ENTERTAINMENT.png), [waterfront/ferry](V9_WATERFRONT.png), [Jeju](V9_JEJU.png).
- [Actual normal-entry gameplay video](quality/video/v9-gameplay.mp4); [native1024×768 gameplay crops](quality/final), [real844×390 mobile captures](quality/mobile).

Root district images are1:1 crops of the actual engine overview. Gameplay crops are the real follow camera. Web/comparison images are labeled1:4 nearest previews, not sharpness references. V8's5312px canvas is explicitly padded to the6144px comparison frame; no stretching, tracing or fabricated old terrain.

## Recovery and preservation

Full rejected V8 recovery **0b809ee883231fcfe46af6330a93e2142c98c299**, tag `recovery/before-v9-total-southern-reset-20261021`, was pushed/remote-verified before removal of4,931obsolete tracked files (4,087,341,729bytes). Exact audit/restoration: [SOUTHERN_RESET_CLEANUP.md](../../SOUTHERN_RESET_CLEANUP.md) and [deleted-file inventory](deleted-files.json). Clean foundation07d9ce5; verified grayboxbb8c9e7 precedes new image production.

Protected north:273objects/253source solids, literal4352×2240ground and native source art. Actual matched-camera1024×768 north frame remains byte-identical to archived V8 ([proof](quality/north-preservation/actual-render-comparison.json)). Original108native art kinds/60source sheet+provenance records, Juni144frames, editable character concepts and shared gameplay/Academy/UI remain preserved. Original3D/history/main survive their recovery history; the separate learning app was untouched.

The old V8 screenshot is read only by the comparison generator from its archive after V9 authoring. No rejected southern coordinates, road masks, plots, district footprints or terrain are imported into planning/build tools.

## New urban design

Original4352×6144 world,33hierarchical public routes and25planned sites. Main civic streets/blocks came before building placements. Northeast Namsan contrasts with southwest transit; the independent southeast amusement campus connects to the coast. New southwest Jeju uses one intentional ferry connection, no mainland-island bridge.

The civic ring contains a planted meeting island and useful shop frontages. The station has its railway behind the entrance, one perpendicular crossing, a full-width forecourt, a public shelter and a gallery-facing neighborhood lane. Modern plot thresholds differ from park paths and cultural-campus paving. The continuous promenade ends in purposeful viewing/gateway spaces; the terminal/wood landing/ferry share one clear boarding sequence. Jeju arrival1984,5504 is on its route outside the112px boarding trigger.

### New site coordinates (native artwork scale1)

|Site|Artwork ground anchor|Street entrance/approach|Original asset|
|---|---|---|---|
{plots}

These positions were selected from the new plan, not retained to satisfy old tests. Public entrances, collision and source/runtime Tiled exports were updated together. Future learning/social anchors are reserved; no unrelated multiplayer, PvP, ads, backend or mass NPC production was added.

## Actual art and tool execution

Four real host image_gen calls: original16material swatches, four distinct Korean shops, a local water-material edit (only2cells adopted;14others unchanged) and two distinct park/campus fence modules. References were original project station/cafe/shop artwork only. No Pixels map/sprite/branding/texture is shipped. Host model and price are unexposed; no billable provider API was invoked and Forge paid-request budget stayed0. Public-reference access limits and interpretations are documented in [PIXELS_WORLD_DESIGN_STUDY.md](../../PIXELS_WORLD_DESIGN_STUDY.md).

Forge pinned5324342fdfab72430f4e9604f3fe427009f8596d actually executed prop extraction, terrain extraction, palette build/apply, map hash/validation, Tiled export, linked world/Academy navigation, layered composition and its unchanged browser verifier over HTTP. {len(commands)}recorded commands; {sum(c['exit']==0 for c in commands)}exit0, {sum(c['exit']!=0 for c in commands)}recorded failed diagnostics. Exact commands/stdout/stderr: [forge-commands.json](../../assets-src/v9-world/forge-commands.json). Skill reads alone are not counted. No master_still/sprite_set/video synthesis is claimed: Juni was preserved.

Four shop PNGs256×224/192colors and two fence PNGs144×48/96colors have padded binary alpha. Original approved art keeps its pixels/native scale. Ground RGB comes from original generated image textures; geometry/masks place materials. Natural-repeat reflections and32six-phase source-pixel water groups are image transforms, not a code-drawn substitute world or video synthesis. No global saturation filter, blur or approved-art resampling.

{len(b['objects'])}actual separate Phaser prop instances/{len(b['props'])}runtime kinds, over editable tile layers; {len(b['collision']['solids'])}exact source/runtime bodies. Atlas4096×1216/{json.loads((SOURCE/'map/tileset.json').read_text())['tiles'].__len__()}tiles. The engine overview is not a flattened generated background.

### Retained warnings and corrected failures

{warntext}

Native outputs were inspected with transparent padding and in-game contexts; numeric acceptance is not user art approval. The initial all-data-URI Forge diagnostic exceeded its16000000byte default (`html-size22521450`). A diagnostic-only32000000byte budget passes; all route/movement/Y-sort assertions remain unchanged and that HTML is not shipped. The Vite main chunk remains above1600kB; actual distribution/ZIP size and measured cloud behavior are reported, not hidden by increasing its warning threshold. Unused resvg-py is unavailable; no unrelated reinstall.

Actual first screenshots exposed a service building hiding the square, isolated mulch strips, curb rings at joins, a too-narrow station forecourt and false soil halos around piers. The plan/graybox/site placement and material unions were corrected. Raw earlier schema/status/size diagnostics remain in tool receipts. Source CI39540303557 had51passed/2long-route timeouts while awaiting CDP input; the CI host now uses the same CPU-compositor flag as local verification. No timeout, collision, speed or acceptance assertion was weakened.

The first V9 recording aborted with ENOSPC. Its footage was not reused. Before removing obsolete task-owned JPEG caches, the full archived V8 MP4 was rehashed to5d67b8d69eeeb1757a62543fdcbdd833164ead3b60136b0956f7370da3f9e171. Original source art/tags/encoded recovery video remain intact. The final recording started fresh with a6GiB preflight.

## Technical and visual verification

-12unit tests, full52case local browser suite plus1additional cached/reference occlusion case. Exact-source GitHub CI: [{ci['run']}](https://github.com/Anapaulagatti/3D-pharse5-/actions/runs/{ci['run']}) at `{ci['head']}`: {ci['browserPassed']}browser cases passed. No queued-run success inference.
- All33routes traversed in actual Phaser using public input. Academy lesson/return, blocked rails/designated crossing, building foundations, reciprocal ferry, basalt feedback, actual Juni walk/run/wave/celebrate/idle and mobile landscape/portrait controls work.
- Source/runtime image/collision hashes match, both linked Forge nav reports pass, upstream browser61targets/keyboard/Y-sort pass. This diagnostic reachability is separate from actual Phaser input tests.
- Actual draw-time Canvas atlas sampling has no smoothing; WebGL atlas min/mag are NEAREST. Native avatar image pixels match DPR1/3. Disabled WebGL automatically falls back to a nonblank playable Canvas view.
- Reduced-motion follows OS preference: actual water pixels/ambient clock stop; normal mode visibly animates. New-tree cue matches source-alpha reference and clears after Juni walks out. No critical browser console/network errors in final native/mobile/package captures.
- Full native engine overview and follow-camera/mobile images were actually inspected and corrected, not accepted merely because screenshots were written.

### Uncaptured cloud samples

|Case|Renderer|MedianRAF ms|p95RAF ms|MedianRAF Hz|
|---|---|---|---|---|
{performance}

Eight seconds percase after warmup; no capture/concurrent local browser suite. These are cloud browser RAF samples, not physical Android/iOS/Safari/hardware-GPU measurements or a universal60FPS guarantee.

## Video, ZIP and reproducibility

Actual normal-entry31stop walkthrough, **{video['output']['duration']:.3f}s**, {video['capturedFrames']}captured={video['encodedFrames']}encoded frames, {video['output']['bytes']:,}bytes. Original capture timestamps preserved to a maximum{video['maxTimestampErrorSeconds']:.6f}s error at1ms encoding timebase. Public joystick/run/dialog/emote/ferry controls only; no QA placement, artificial scene skip, retiming, interpolation, repeated footage or still-image replacement. Capture is JPEG78/everyNthFrame2; H264 is lossy and native PNGs remain the sharpness reference. Real Chromium play/5seeks/changing decoded pixels were verified; representative frames inspected, not every-frame visual review. [Encoding proof](quality/video/encoding-verification.json), [playback proof](quality/video/browser-playback.json).

ZIP **{package['bytes']:,}bytes/{package['files']}files**, SHA256`{package['sha256']}`, runtime/art source`{package['sourceCheckpoint']}`. Its own HTTP launcher was run. Native source/ZIP pixels match in six districts; mobile analog movement, portrait pause, both ferries, Academy and basalt wrong/correct feedback work. All packaged runtime file hashes verified. No credentials, original source masters, old reviews or unrelated3D/private files are shipped. [HTTP proof](quality/package/http-verification.json).

Independent clean checkout`{clean['head']}`: locked npm installation, no authoring-tool dependency, stored-asset/type/lint/format/unit/build/browser checks pass. {clean['browserPassed']}browser/{clean['unitPassed']}unit. Complete distribution matches the package/runtime build ([clean setup proof](quality/clean-setup.json)). This is a fresh checkout verification, not a claim that a new-task cloud snapshot has been restored.

`main` remains33360ed1989e4db9fc3fc4e3686ca385e0b00908. Public siteHTTP{site['status']}/{site['bytes']:,}bytes still SHA256`{site['sha256']}`. No Pages publication/merge/history rewrite/force push. Delivery checkpoint and observed final CI are recorded by the annotated review/recovery tag, avoiding a report pretending to know its own commit SHA.

**STOP: user visual approval is required before map lock, additional content or publication.**
'''
# Markdown list spacing is intentional; separate actual parallel verification facts.
text=text.replace('\n-12unit','\n- 12unit').replace('\n- All','\n- All').replace('\n- Source','\n- Source').replace('\n- Actual','\n- Actual').replace('\n- Reduced','\n- Reduced').replace('\n- Full','\n- Full')
(Q/'V9_CITY_REBUILD_REPORT.md').write_text(text)
print('Verified delivery report written; user visual approval remains pending')
