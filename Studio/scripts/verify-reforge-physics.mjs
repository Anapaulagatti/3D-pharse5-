import assert from 'node:assert/strict'
import {readFile,writeFile} from 'node:fs/promises'
import {createPlayer,stepPlayer} from '../../preview/src/reforge/physics.ts'
const world=JSON.parse(await readFile(new URL('../../exports/v0.5/hanok-graybox-structure.json',import.meta.url),'utf8')),walls=world.colliders
const tick=(p,n,w,run,open,jump=false)=>{for(let i=0;i<n;i++)stepPlayer(p,w,run,jump&&i===0,1/60,walls,open)}
let p=createPlayer();tick(p,360,[0,-1],true,false)
assert.ok(p.position[2]>-.25,'closed sliding door blocks entry')
const closed=[...p.position];tick(p,180,[0,-1],false,true)
assert.ok(p.position[2]<-1.5,'opened door and actual staircase traversable')
assert.ok(Math.abs(p.position[1]-.4775)<.001,'raised interior has ground contact')
tick(p,600,[0,-1],true,true);assert.ok(p.position[2]>-4.11,'rear wall blocks travel')
const rear=[...p.position];p=createPlayer();let peak=0
for(let i=0;i<100;i++){stepPlayer(p,[0,0],false,i===0,1/60,walls,true);peak=Math.max(peak,p.position[1])}
assert.ok(peak>.44&&peak<.53,'physics airborne arc with finite gravity');assert.equal(p.grounded,true);assert.equal(p.position[1],0)
tick(p,60,[1,0],true,true);tick(p,40,[0,0],false,true);assert.ok(p.speed<.001,'release decelerates to stop')
const result={status:'PASS',checks:['closed-door collision','walk staircase through opened door','raised interior ground contact','rear wall collision','physics jump and landing','input release stops'],closed_position:closed,rear_position:rear,jump_height:peak,limitation:'Actual shared controller geometry/physics checks; browser input and visual acceptance remain separate.'}
await writeFile(new URL('../../quality-reports/v0.5/gate-c/physics-verification.json',import.meta.url),JSON.stringify(result,null,2)+'\n')
console.log(JSON.stringify(result,null,2))
