// Kinematic, metre-scale courtyard controller. Independent of the renderer/frame rate.
export type V3=[number,number,number]
export interface Collider {id:string;min:number[];max:number[]}
export interface InputState {keys:Set<string>;mobileRun:boolean;jump:boolean;wake?:()=>void}
export const createInput=():InputState=>({keys:new Set(),mobileRun:false,jump:false})
export interface Player {
 position:V3;velocity:[number,number];vertical:number;yaw:number;grounded:boolean;
 crouch:number;landing:number;speed:number;blocked:number;distance:number;steps:number;
 clip:string;clipTime:number;actionId:number;resetId:number
}
export const createPlayer=():Player=>({position:[0,0,2.4],velocity:[0,0],vertical:0,yaw:0,grounded:true,crouch:0,landing:0,speed:0,blocked:0,distance:0,steps:0,clip:'Idle',clipTime:0,actionId:0,resetId:0})
export function floorHeight(x:number,z:number){
 if(Math.abs(x)<.64&&z>=.25&&z<1.21)return .45-.15*Math.min(2,Math.floor((z-.25)/.32))
 if(Math.abs(x)<3.25&&z>=-4.45&&z<.30)return .4775
 if(Math.abs(x)<3.375&&z>=-4.50&&z<.35)return .36
 return 0
}
export function intersects(x:number,y:number,z:number,c:Collider,r=.235){
 if(y+.045>=c.max[1]||y+1.40<=c.min[1]+.015)return false
 const dx=x-Math.max(c.min[0],Math.min(c.max[0],x)),dz=z-Math.max(c.min[2],Math.min(c.max[2],z))
 return dx*dx+dz*dz<r*r
}
const approach=(a:number,b:number,d:number)=>a<b?Math.min(a+d,b):Math.max(a-d,b)
export function stepPlayer(p:Player,wish:[number,number],run:boolean,jump:boolean,dt:number,colliders:Collider[],doorOpen:boolean){
 const [oldX,oldY,oldZ]=p.position
 const desired=run?2.4375:.8148,hasInput=Math.hypot(...wish)>.01
 if(jump&&p.grounded&&p.crouch===0&&p.landing===0)p.crouch=.20
 if(p.crouch>0){p.crouch=Math.max(0,p.crouch-dt);if(p.crouch===0){p.vertical=Math.sqrt(2*11*.5);p.grounded=false}}
 p.landing=Math.max(0,p.landing-dt)
 const multiplier=p.crouch>0?.10:1,accel=hasInput?9:13
 p.velocity[0]=approach(p.velocity[0],wish[0]*desired*multiplier,accel*dt);p.velocity[1]=approach(p.velocity[1],wish[1]*desired*multiplier,accel*dt)
 const dynamicDoor:Collider={id:'SlidingDoorAperture',min:[-.55,.477,-.67],max:[.55,2.48,-.46]}
 const blocks=(x:number,z:number)=>{
  if(x<-5.70||x>5.70||z<-5.42||z>4.02)return true
  if(p.grounded&&floorHeight(x,z)-p.position[1]>.18)return true
  if(!doorOpen&&intersects(x,p.position[1],z,dynamicDoor))return true
  return colliders.some(c=>intersects(x,p.position[1],z,c))
 }
 const nx=oldX+p.velocity[0]*dt,nz=oldZ+p.velocity[1]*dt
 if(!blocks(nx,oldZ))p.position[0]=nx;else{p.velocity[0]=0;p.blocked++}
 if(!blocks(p.position[0],nz))p.position[2]=nz;else{p.velocity[1]=0;p.blocked++}
 const ground=floorHeight(p.position[0],p.position[2])
 if(p.grounded&&Math.abs(ground-oldY)<=.18)p.position[1]=ground
 if(!p.grounded||p.position[1]>ground+.01){p.vertical-=11*dt;p.position[1]+=p.vertical*dt;p.grounded=false}
 if(p.position[1]<=ground){if(!p.grounded&&p.vertical<-.6)p.landing=.3333;p.position[1]=ground;p.vertical=0;p.grounded=true}
 if(p.grounded&&ground>oldY)p.position[1]=ground
 const dx=p.position[0]-oldX,dz=p.position[2]-oldZ;p.speed=Math.hypot(dx,dz)/dt;p.distance+=Math.hypot(dx,dz);p.steps++
 if(p.speed>.02){const target=Math.atan2(dx,dz),angle=Math.atan2(Math.sin(target-p.yaw),Math.cos(target-p.yaw));p.yaw+=angle*Math.min(1,dt*12)}
 return p
}
