"""Localized extension of the existing Studio/preferences; no alternate UI engine."""
from pathlib import Path
import sys
R=Path(__file__).resolve().parents[2];OUT=R if '--apply'in sys.argv else Path('/tmp/phase2c-ui-draft')
def put(p,s):
 out=OUT/p;out.parent.mkdir(parents=True,exist_ok=True);out.write_text(s)
p='src/characters/preferences.ts';s=(R/p).read_text().replace('interface AppearanceStore {','export const MAX_APPEARANCE_PRESETS = 12;\nexport interface AppearanceRepository {\n  read(characterId:string):CharacterAppearance;\n  presets():AppearancePreset[];\n  save(appearance:CharacterAppearance,name?:string):boolean;\n  renamePreset(id:string,name:string):boolean;\n  deletePreset(id:string):boolean;\n}\ninterface AppearanceStore {').replace('export class AppearancePreferences {','export class AppearancePreferences implements AppearanceRepository {').replace('value.presets.slice(0, 8)','value.presets.slice(0, MAX_APPEARANCE_PRESETS)').replace('    const next = this.readStore();','    const next = structuredClone(this.readStore());').replace('      const clean = name.trim().slice(0, 32),','      const clean = name.trim().replace(/\\s+/g," ").slice(0, 32),').replace('      const preset = {','      if(!existing && next.presets.length >= MAX_APPEARANCE_PRESETS) return false;\n      const preset = {').replace('].slice(-8);','].slice(-MAX_APPEARANCE_PRESETS);')
ix=s.index('  save(appearance: CharacterAppearance, name?: string)')
s=s[:ix]+'''  userPresets() { return this.presets().filter(p=>this.readStore().presets.some(u=>u.id===p.id)); }
  isUserPreset(id:string) { return this.readStore().presets.some(p=>p.id===id); }
  canSavePreset(name:string) { const clean=name.trim().replace(/\\s+/g," ").slice(0,32);return !clean || this.readStore().presets.some(p=>p.name===clean) || this.readStore().presets.length<MAX_APPEARANCE_PRESETS; }
  private writeStore(next:AppearanceStore) {
    this.memory=next;
    try {if(!this.storage)return false;this.storage.setItem(APPEARANCE_PREFERENCES_KEY,JSON.stringify(next));return true;}catch{return false;}
  }
  renamePreset(id:string,name:string) {
    const clean=name.trim().replace(/\\s+/g," ").slice(0,32), next=structuredClone(this.readStore());
    if(!clean || next.presets.some(p=>p.id!==id&&p.name===clean))return false;
    const item=next.presets.find(p=>p.id===id);if(!item)return false;item.name=clean;return this.writeStore(next);
  }
  deletePreset(id:string) {
    const next=structuredClone(this.readStore());if(!next.presets.some(p=>p.id===id))return false;
    next.presets=next.presets.filter(p=>p.id!==id);return this.writeStore(next);
  }
''' +s[ix:];put(p,s)
p='src/characters/studioI18n.ts';s=(R/p).read_text();translations=[('vi',dict(renamePreset='Đổi tên bộ đã lưu',deletePreset='Xóa bộ đã lưu',presetLimit='Đã đủ12bộ. Xóa một bộ cũ hoặc để trống tên để áp dụng.',presetChanged='Đã cập nhật bộ của bạn.',presetInvalid='Chọn bộ tự lưu và nhập tên không trùng.',previewLoading='Đang thử đồ…',idle='Đứng',walk='Đi bộ',run='Chạy',wave='Chào',celebrate='Vui')),('en',dict(renamePreset='Rename saved look',deletePreset='Delete saved look',presetLimit='12saved looks reached. Delete one or clear the name to apply.',presetChanged='Your saved looks are updated.',presetInvalid='Choose a personal preset and a unique name.',previewLoading='Trying your look…',idle='Idle',walk='Walk',run='Run',wave='Wave',celebrate='Celebrate')),('ko',dict(renamePreset='저장한 코디 이름 변경',deletePreset='저장한 코디 삭제',presetLimit='코디12개가 저장되었습니다. 하나를 삭제하거나 이름을 비워 적용하세요.',presetChanged='저장한 코디를 수정했습니다.',presetInvalid='직접 저장한 코디와 다른 이름을 선택하세요.',previewLoading='코디 준비 중…',idle='대기',walk='걷기',run='달리기',wave='인사',celebrate='기쁨'))]
import json
for key,fields in translations:
 needle='  '+key+': {';assert needle in s;s=s.replace(needle,needle+'\n'+''.join('    '+k+': '+json.dumps(v,ensure_ascii=False)+',\n'for k,v in fields.items()),1)
s=s.replace('Nhân vật này đang giữ ngoại hình đã duyệt. Các mục tùy chỉnh hiện có dành cho Ara và Doyun.','Chưa có mục phù hợp trong danh mục này. Bạn vẫn có thể giữ nguyên bản.').replace('This approved appearance is preserved. Review customization currently supports Ara and Doyun.','No matching items in this category. Your original appearance is always available.');put(p,s)
p='src/characters/CharacterSelection.ts';s=(R/p).read_text();s=s.replace('<div id="character-art"><canvas','<div id="character-art"><span id="studio-preview-state" role="status" aria-live="polite" hidden></span><canvas')
s=s.replace('["idle", "Đứng"]','["idle", this.copy.idle]').replace('["walk", "Đi bộ"]','["walk", this.copy.walk]').replace('["run", "Chạy"]','["run", this.copy.run]').replace('["wave", "Chào"]','["wave", this.copy.wave]').replace('["celebrate", "Vui"]','["celebrate", this.copy.celebrate]')
s=s.replace('<select id="appearance-preset"><option value="">—</option></select></label>','<span class="studio-preset-select"><select id="appearance-preset"><option value="">—</option></select><button id="preset-rename" type="button" aria-label="${this.copy.renamePreset}" title="${this.copy.renamePreset}">✎</button><button id="preset-delete" type="button" aria-label="${this.copy.deletePreset}" title="${this.copy.deletePreset}">×</button></span></label>')
needle='        this.choose(characterRegistry.resolve(preset.appearance.characterId));';assert needle in s;s=s.replace(needle,needle+'\n        this.el<HTMLSelectElement>("#appearance-preset").value=preset.id;\n        this.el<HTMLInputElement>("#appearance-preset-name").value=preset.name;\n        this.presetButtons();')
needle='    this.presets();\n    window.addEventListener(';assert needle in s;s=s.replace(needle,'''    this.el("#preset-rename").addEventListener("click",()=>this.managePreset(false));
    this.el("#preset-delete").addEventListener("click",()=>this.managePreset(true));
    this.presets();
    window.addEventListener(''',1)
needle='  private presets() {';assert needle in s;s=s.replace(needle,'''  private presetButtons() {
    const id=this.el<HTMLSelectElement>("#appearance-preset").value;
    for(const selector of ["#preset-rename","#preset-delete"])this.el<HTMLButtonElement>(selector).disabled=this.pending||!this.appearances.isUserPreset(id);
  }
  private managePreset(remove:boolean) {
    if(this.pending)return;
    const id=this.el<HTMLSelectElement>("#appearance-preset").value;
    const ok=remove?this.appearances.deletePreset(id):this.appearances.renamePreset(id,this.el<HTMLInputElement>("#appearance-preset-name").value);
    this.feedback(ok?this.copy.presetChanged:this.copy.presetInvalid);
    this.presets();if(ok&&!remove)this.el<HTMLSelectElement>("#appearance-preset").value=id;this.presetButtons();
  }
  private presets() {''')
s=s.replace('      select.add(new Option(preset.name, preset.id));','      select.add(new Option(preset.name, preset.id));\n    this.presetButtons();')
needle='    const def = characterRegistry.resolve(this.candidate),';s=s.replace(needle,'''    const status=this.el("#studio-preview-state");status.hidden=false;status.textContent=this.copy.previewLoading;
    this.el("#character-preview").setAttribute("aria-busy","true");
    const def = characterRegistry.resolve(this.candidate),''',1)
needle='      if (token !== this.previewToken || !this.dialog.open) return;';s=s.replace(needle,needle+'\n      status.hidden=true;\n      const preview=this.el<HTMLCanvasElement>("#character-preview");preview.setAttribute("aria-busy","false");preview.dataset.character=def.id;preview.dataset.appearance=JSON.stringify(asset.appearance);preview.dataset.previewState="ready";',1)
s=s.replace('      const canvas = this.el<HTMLCanvasElement>("#character-preview");','      const canvas = this.el<HTMLCanvasElement>("#character-preview");')
s=s.replace('        const f = asset.atlas.frames[clip.frames[i]].frame;','        const f = asset.atlas.frames[clip.frames[i]].frame;\n        if(canvas.dataset.frame!==clip.frames[i])canvas.dataset.frame=clip.frames[i];')
s=s.replace('    this.pending = true;\n    for (const b', '''    if(!this.appearances.canSavePreset(this.el<HTMLInputElement>("#appearance-preset-name").value)){this.feedback(this.copy.presetLimit);return;}
    this.pending = true;
    for (const b''',1)
s=s.replace('    this.host.unlock();','    this.drafts.clear();\n    this.host.unlock();')
needle='      for (const b of this.dialog.querySelectorAll<HTMLButtonElement>(\n        "[data-character]",\n      ))\n        b.disabled =\n          characterRegistry.get(b.dataset.character!)?.availability.status !==\n          "playable";';assert needle in s;s=s.replace(needle,needle+'\n      this.presetButtons();');put(p,s)
p='src/characters/selection.css';s=(R/p).read_text();s+='''
/* Phase2C: keep existing modal/grid; native preview and touch controls. */
#character-art {position:relative;}
#studio-preview-state {position:absolute;top:6px;right:8px;padding:4px 7px;background:#f9ecca;border:1px solid #a8b28c;font-size:11px;}
.studio-preset-select {display:flex;gap:4px;align-items:center;min-width:0;}
.studio-preset-select select {flex:1;width:0;}
#preset-rename,#preset-delete {min-width:44px;min-height:44px;padding:4px;font-size:20px;}
#cosmetic-items button[aria-pressed="true"] {box-shadow:inset 0 0 0 2px #427561;background:#dce7bd;}
#cosmetic-items button img {image-rendering:pixelated;}
@media(max-height:560px){
 #character-preview-actions {grid-template-columns:repeat(5,minmax(0,1fr));gap:2px;}
 #character-preview-actions button {min-height:44px;min-width:0;padding:3px 1px;font-size:10px;}
 #character-preview-actions button[data-action="wave"],#character-preview-actions button[data-action="celebrate"]{display:block;}
 .studio-presets{gap:3px;}
 #preset-rename,#preset-delete{min-width:44px;min-height:44px;}
 .character-detail{gap:3px;}
}
''';put(p,s)
print('UI draft prepared'if OUT!=R else'Existing Studio upgraded')
