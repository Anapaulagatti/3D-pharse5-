from pathlib import Path
p=Path('src/economy/catalog.ts');s=p.read_text().replace('export interface PlotState {','export interface PlotState {\n  lastHarvestedAt?: number;').replace('export interface EconomyState {','export interface EconomyState {\n  interactionSchema?: 2;').replace('    revision: 0,','    interactionSchema: 2,\n    revision: 0,');p.write_text(s)
p=Path('src/quests/content.ts');s=p.read_text();start=s.index('    id: "farm-first-seed-v1"');end=s.index('\n  {\n    id: "farm-radish-harvest-v1"',start);s=s[:start]+'''    id: "farm-first-seed-v1",
    title: "Hạt giống đầu tiên", ko: "첫 씨앗", giver: "npc-cheolsu", topic: "farm",
    steps: [
      {id:"plant",label:"Gieo hạt vào một luống thật",point:[470,669]},
      {id:"water",label:"Dùng bình tưới cho cây vừa gieo",point:[470,669]},
      {id:"harvest",label:"Thu hoạch cây chín rồi trở lại Cheolsu",point:[470,669]},
    ],
    economyObjectives:[{event:"plant",crop:"radish"},{event:"water",crop:"radish"},{event:"harvest",crop:"radish"}],
    reward:{coins:20,xp:20,items:{"seed-radish":2,sprout:1}},
  },'''+s[end:];p.write_text(s)
p=Path('src/quests/manager.ts');s=p.read_text().replace('  boundPlot?: string;','  boundPlot?: string;\n  collected?: string[];').replace('  storageWarning = "";','  storageWarning = "";\n  migrationNotice = "";').replace('      const v = JSON.parse(raw) as QuestSave;','      const v = JSON.parse(raw) as QuestSave;\n      const legacy = v.economy?.interactionSchema !== 2;').replace('record.step > def.steps.length','record.step > (legacy && id === "farm-first-seed-v1" ? 4 : def.steps.length)');s=s.replace('      v.economy ??= freshEconomy();','''      for (const def of quests.filter(q=>q.topic==="orchard")) {
        const r=v.records[def.id]; if(!r)continue;
        r.collected ??= def.steps.slice(0,r.step).map(s=>s.id);
        if(!Array.isArray(r.collected)||new Set(r.collected).size!==r.collected.length||r.collected.some(id=>!def.steps.some(s=>s.id===id))||r.collected.length!==r.step)throw Error("invalid collected objects");
      }
      if(legacy) {
        const n=Math.min(v.inventory.seed??0,Math.max(0,99-(v.inventory["seed-radish"]??0)));
        const slots=Object.values(v.inventory).filter(n=>n>0).length;
        if(n>0 && ((v.inventory["seed-radish"]??0)>0||slots<ECONOMY.slots||n===v.inventory.seed)) {
          v.inventory.seed-=n;v.inventory["seed-radish"]=(v.inventory["seed-radish"]??0)+n;
        }
        const r=v.records["farm-first-seed-v1"];
        if(r?.status==="completed")r.step=3;
        else if(r){r.status="active";r.step=0;delete r.boundPlot;
          if(!(v.inventory["seed-radish"]>0)&&Object.values(v.inventory).filter(n=>n>0).length<ECONOMY.slots)v.inventory["seed-radish"]=1;
          this.migrationNotice="Hướng dẫn cũ chuyển sang luống thật; xu và phần thưởng đã nhận vẫn giữ nguyên.";
        }
      }
      v.economy ??= freshEconomy();
      v.economy.interactionSchema=2;''');s=s.replace('s.inventory.seed = (s.inventory.seed ?? 0) + 1;','s.inventory["seed-radish"] = (s.inventory["seed-radish"] ?? 0) + 1;');s=s.replace('    const step = def?.steps[record?.step ?? -1];','    const step = def?.topic === "orchard" ? def.steps.find(s=>s.id===action) : def?.steps[record?.step ?? -1];').replace('      step.id !== action ||','      step.id !== action ||\n      record.collected?.includes(action) ||');s=s.replace('      if (def.topic === "orchard")\n        s.inventory.tangerine = (s.inventory.tangerine ?? 0) + 1;','''      if (def.topic === "orchard") {
        const r=s.records[id];r.collected ??= def.steps.slice(0,r.step).map(s=>s.id);
        if(r.collected.includes(action))return false;
        r.collected.push(action);
        s.inventory.tangerine = (s.inventory.tangerine ?? 0) + 1;
      }''');s=s.replace('if (p.stage !== "tilled" || !cropId || !(cropId in crops)) return false;','''if (!["empty","tilled"].includes(p.stage) || !cropId || !(cropId in crops)) return false;
        if(p.stage==="empty")this.economyEvent(s,"till",undefined,undefined,plotId);''').replace('{ stage: "empty", cycle: p.cycle };','{ stage: "empty", cycle: p.cycle, lastHarvestedAt: now };');i=s.index('  accept(id: string, npcId: string)');s=s[:i]+'''  private validContext(id:string,npcId:string,c:InteractionContext) {
    return c.npcId===npcId && nearGround(c.player,c.actor,c.ground,112) && quests.some(q=>q.id===id);
  }
  acceptInWorld(id:string,npcId:string,c:InteractionContext){return this.validContext(id,npcId,c)&&this.accept(id,npcId);}
  returnInWorld(id:string,npcId:string,c:InteractionContext){return this.validContext(id,npcId,c)&&this.returnToNPC(id,npcId);}
  answerInWorld(id:string,questionId:string,choice:number,c:InteractionContext){
    const q=quests.find(q=>q.id===id);
    return q&&this.validContext(id,q.recipient??q.giver,c) ? this.answer(id,questionId,choice) : {result:"invalid",explanation:"Hãy trở lại người bạn để trả lời."};
  }
'''+s[i:];s=s.replace('export const QUEST_STORAGE_KEY', '''export interface InteractionContext {npcId:string;player:readonly[number,number];actor:readonly[number,number];ground:(x:number,y:number)=>boolean;}
export const QUEST_STORAGE_KEY''');p.write_text(s)
