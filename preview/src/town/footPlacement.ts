import { Bone, Object3D, Quaternion, Vector3 } from 'three'
import type { Group } from 'three'
import { floorHeight, type Player } from './physics'

// Analytic two-joint correction for known courtyard/stair surfaces. Authored gait
// remains unchanged on flat ground; only stance feet follow a different tread.
export class TerrainFeet {
 private chains:{hip:Bone;knee:Bone;foot:Bone;phase:number}[]=[]
 private h=new Vector3();private k=new Vector3();private a=new Vector3();private t=new Vector3()
 private u=new Vector3();private v=new Vector3();private goal=new Vector3();private from=new Vector3();private to=new Vector3()
 private delta=new Quaternion();private original=new Quaternion();private parent=new Quaternion();private savedFoot=new Quaternion()
 constructor(model:Object3D){
  for(const [suffix,phase] of [['L',0],['R',.5]] as const){
   const find=(name:string)=>model.getObjectByName(name+suffix)||model.getObjectByName(name+'.'+suffix)
   const hip=find('Thigh') as Bone,knee=find('Shin') as Bone,foot=find('Foot') as Bone
   if(hip&&knee&&foot)this.chains.push({hip,knee,foot,phase})
  }
 }
 private aim(bone:Bone,child:Bone,target:Vector3){
  bone.getWorldPosition(this.h);child.getWorldPosition(this.a)
  this.from.subVectors(this.a,this.h).normalize();this.to.subVectors(target,this.h).normalize()
  this.delta.setFromUnitVectors(this.from,this.to);bone.getWorldQuaternion(this.original);this.original.premultiply(this.delta)
  bone.parent!.getWorldQuaternion(this.parent);bone.quaternion.copy(this.parent.invert().multiply(this.original)).normalize();bone.updateWorldMatrix(true,true)
 }
 apply(outer:Group,player:Player,clip:string,cycle:number){
  if(!player.grounded||!['Idle','Walk','Run','WalkStart','WalkStop','RunStart','RunStop','Thinking','Sad','Curious'].includes(clip))return
  const contacts=this.chains.filter(c=>clip!=='Walk'&&clip!=='Run'||(cycle+c.phase)%1<(clip==='Run'?.32:.60))
  let lowest=player.position[1]
  for(const c of contacts){c.foot.getWorldPosition(this.a);lowest=Math.min(lowest,floorHeight(this.a.x+Math.sin(player.yaw)*.045,this.a.z+Math.cos(player.yaw)*.045))}
  // Moving onto a higher tread need not yank the hips up while the rear foot is planted.
  outer.position.y=lowest;outer.updateWorldMatrix(true,true)
  for(const c of contacts){
   c.hip.getWorldPosition(this.h);c.knee.getWorldPosition(this.k);c.foot.getWorldPosition(this.a)
   const ground=floorHeight(this.a.x+Math.sin(player.yaw)*.045,this.a.z+Math.cos(player.yaw)*.045)
   if(Math.abs(this.a.y-ground-.065)<.006)continue
   c.foot.getWorldQuaternion(this.savedFoot);this.t.copy(this.a);this.t.y=ground+.065
   const l1=this.h.distanceTo(this.k),l2=this.k.distanceTo(this.a),d=Math.max(.01,Math.min(l1+l2-.0001,this.h.distanceTo(this.t)))
   this.u.subVectors(this.t,this.h).normalize();this.v.subVectors(this.k,this.h).addScaledVector(this.u,-this.v.dot(this.u))
   if(this.v.lengthSq()<.00001)this.v.set(Math.sin(player.yaw),0,Math.cos(player.yaw)).addScaledVector(this.u,-this.v.dot(this.u))
   this.v.normalize();const along=(l1*l1-l2*l2+d*d)/(2*d)
   this.goal.copy(this.h).addScaledVector(this.u,along).addScaledVector(this.v,Math.sqrt(Math.max(0,l1*l1-along*along)))
   this.aim(c.hip,c.knee,this.goal);this.aim(c.knee,c.foot,this.t)
   c.foot.parent!.getWorldQuaternion(this.parent);c.foot.quaternion.copy(this.parent.invert().multiply(this.savedFoot)).normalize();c.foot.updateWorldMatrix(true,true)
  }
 }
}
