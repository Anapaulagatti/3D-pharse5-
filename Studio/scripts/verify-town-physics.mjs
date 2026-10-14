import assert from 'node:assert/strict'
import {readFile,writeFile} from 'node:fs/promises'
import {createPlayer,stepPlayer,floorHeight} from '../../preview/src/town/physics.ts'
const world=JSON.parse(await readFile(new URL('../../exports/v0.6/collision-world.json',import.meta.url))),checks=[],out=new URL('../../quality-reports/v0.6/prototype/'+(process.env.TOWN_PHYSICS_REPORT||'physics.json'),import.meta.url)
const tick=(p,n,w,run=false,open=false,jump=false)=>{for(let i=0;i<n;i++)stepPlayer(p,w,run,jump&&i===0,1/60,world.colliders,open)}
try{
 let p=createPlayer();p.position[0]=-1.2;tick(p,360,[0,-1]);assert.ok(p.position[2]>-.93&&p.position[2]<-.65);assert.ok(Math.abs(p.position[1]-.30)<.02);checks.push('Closed actual door stops entry after traversing real .1m stairs onto veranda')
 const closed=[...p.position];tick(p,180,[0,-1],false,true);assert.ok(p.position[2]<-1.6,'Open aperture must be traversable, without a central support collider');assert.ok(Math.abs(p.position[1]-.30)<.001);checks.push('Opened door enters supported interior with exact floor contact')
 tick(p,600,[0,-1],true,true);assert.ok(p.position[2]>-3.60);checks.push('Rear wall retains real collision')
 p=createPlayer();let peak=0;for(let i=0;i<100;i++){stepPlayer(p,[0,0],false,i===0,1/60,world.colliders,true);peak=Math.max(peak,p.position[1])}assert.ok(peak>.32&&peak<.40);assert.ok(p.grounded&&p.position[1]===0);checks.push('Finite .38m jump arc and grounded landing')
 tick(p,35,[1,0],true,true);tick(p,40,[0,0],false,true);assert.ok(p.speed<.001);checks.push('Input release decelerates to complete stop')
 p=createPlayer();tick(p,1000,[1,0],true,true);assert.ok(p.position[0]<=4.85);checks.push('World bounds prevent leaving plaza')
 assert.equal(floorHeight(-1.2,-.50),.30);assert.equal(floorHeight(3.1,1.35),.16);checks.push('Highest overlapping floor wins, safe jump platform matches source height')
 await writeFile(out,JSON.stringify({status:'PASS',checks,closed_position:closed,jump_peak:peak,limitation:'Actual shared controller + exported geometry checks. Browser input and visual inspection remain separate.'},null,2)+'\n');console.log('Town physics:',checks.length,'checks PASS')
}catch(e){await writeFile(out,JSON.stringify({status:'FAIL',checks,message:String(e)},null,2)+'\n');throw e}
