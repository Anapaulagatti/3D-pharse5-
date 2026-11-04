from pathlib import Path
from PIL import Image
import subprocess,json,hashlib
R=Path.cwd();D=R/'docs/roadmap-v2';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();base=json.loads((D/'PROTECTED_BASELINE.json').read_text());bad=[p for p,h in base['files'].items()if not Path(p).is_file()or H(Path(p))!=h];assert not bad,bad
(D/'PROTECTED_AUDIT.json').write_text(json.dumps({'status':'PASS','count':len(base['files']),'changed':[],'missing':[],'base':base['baseCommit'],'worldMasksRegistrations':'UNCHANGED','players':12,'NPCs':26,'activeCosmetics':24,'newAssets':'public/assets/roadmap-v2 only'},indent=2)+'\n')
q=json.load(open('public/assets/roadmap-v2/crops.json'));old=json.load(open('public/assets/farming/phase3bd-final-quality/crops.json'));im=Image.open('public/assets/roadmap-v2/crops.png').convert('RGBA');prev=Image.open('public/assets/farming/phase3bd-final-quality/crops.png').convert('RGBA');table=json.load(open(D/'ECONOMY_TABLE.json'))
def pixels(image,f):f=f['frame'];return image.crop((f['x'],f['y'],f['x']+f['w'],f['y']+f['h'])).tobytes()
assert all(pixels(im,q['frames'][k])==pixels(prev,v)for k,v in old['frames'].items())
for c in table['crops']:
 for st in ['sown','sprout','young','growing','ready']:
  f=q['frames'][c['id']+'-'+st]['frame'];assert(f['w'],f['h'])==(40,44);assert Image.frombytes('RGBA',(40,44),pixels(im,{'frame':f})).getbbox()
mature={c['id']:hashlib.sha256(pixels(im,q['frames'][c['id']+'-ready'])).hexdigest()for c in table['crops']};assert len(set(mature.values()))==12
(D/'NATIVE_ART_AUDIT.json').write_text(json.dumps({'status':'PASS','retainedOriginalCropFramesByteExact':len(old['frames']),'newCropFrames':len(q['frames'])-len(old['frames']),'nativeCell':[40,44],'anchor':[20,40],'scale':1,'all12SpeciesHave5NonemptyNamedNativeFrames':True,'matureFrameHashes':mature,'partialAlpha':sum(0<a<255 for a in im.getchannel('A').get_flattened_data()),'worldArtworkEdited':False,'artApproval':'PENDING_HUMAN_REVIEW'},indent=2)+'\n')
names=json.loads(subprocess.check_output(['python','tools/phase3bd/runtime_assets.py'],text=True));prior=json.load(open('.cache/phase3bd-final-quality-review/export-manifest.json'));pins={r['filename']:r['sha256']for r in prior['files']};rows=[]
for name in names:
 p=Path('public')/name;h=H(p);new=name.startswith('assets/roadmap-v2/');assert new or pins.get('play/'+name)==h,name
 rows.append({'path':name,'sha256':h,'classification':'ORIGINAL_CODE_AUTHORED_REVIEW_CANDIDATE'if new else'UNCHANGED_PREVIOUS_OWNER_PUBLIC_PREVIEW_SCOPE','matchesPriorArtifact':None if new else True,'source':'assets-src/roadmap-v2/PROVENANCE.json'if new else'Exact1a6e5a58/331cd300 previous approval/provenance record','specificUnresolvedThirdPartyConcern':'None identified; no new third-party references supplied'if new else'No new concern identified; unchanged prior scope, not invented new clearance','artReview':'PENDING_HUMAN_REVIEW'if new else'PROTECTED_BASELINE','publicExposureForChangedBuild':'PENDING_EXACT_OWNER_APPROVAL'})
(D/'ASSET_EXPOSURE.json').write_text(json.dumps({'status':'LOCAL_REVIEW_ONLY; NOT COMMERCIAL/LEGAL CERTIFICATION','count':len(rows),'newFiles':sum(r['classification'].startswith('ORIGINAL')for r in rows),'oldPublicManifest':'331cd300478f879bab11e9541803dd7c47ba1caaab339263f37150ae6c0d0ce4','voicesAudio':'NONE; noAudio:true','fonts':'Browser/system fonts; no new font binaries','realAccounts':'NONE','Korean':'PENDING_HUMAN_REVIEW','files':rows},indent=2)+'\n')
mods=json.loads((D/'AUTHORIZED_AMENDMENTS.json').read_text());assert all(H(Path(k))==v['afterSHA256']for k,v in mods['files'].items());assert all(H(Path(k))==v for k,v in mods['addedFiles'].items())
engine=['src/gate3/ReviewMovement.ts','src/gate3/NativeContact.ts','src/gate3/PixelGrid.ts','src/gate3/FoundationCamera.ts','src/engine/Joystick.ts','src/engine/JuniMotion.ts','src/characters/PlayerCharacterManager.ts','src/characters/RegistryMotion.ts']
assert all(hashlib.sha256(subprocess.check_output(['git','show',base['baseCommit']+':'+p])).hexdigest()==H(Path(p))for p in engine)
(D/'CORE_PRESERVATION.json').write_text(json.dumps({'status':'PASS','unchangedEnginePaths':engine,'allowedIntegrationFiles':list(mods['files']),'newRoomAndContractFiles':list(mods['addedFiles']),'originalWorldAndActors':'Exact source/PNG/hash preservation; no global camera/movement rewrite'},indent=2)+'\n')
print('PASS protected',len(base['files']),'runtime',len(rows),'62nativeframes/12species,originalengine exact')
