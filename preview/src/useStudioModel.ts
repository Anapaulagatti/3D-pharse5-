import { useEffect, useMemo } from 'react'
import { useGLTF } from '@react-three/drei'
import { Mesh, MeshStandardMaterial } from 'three'
import { assetURL } from './assets'

export function useStudioModel(id: string) {
  const gltf = useGLTF(assetURL(id))
  const scene = useMemo(() => {
    const clone = gltf.scene.clone(true)
    const materials = new Map<MeshStandardMaterial, MeshStandardMaterial>()
    clone.traverse(o => {
      if (!(o instanceof Mesh)) return
      o.castShadow = true
      o.receiveShadow = true
      const copy = (m: MeshStandardMaterial) => {
        if (!materials.has(m)) {
          const next = m.clone()
          next.envMapIntensity = .48
          if (/Celadon|Enamel/.test(m.name)) { next.roughness = .29; next.metalness = .06; next.envMapIntensity = .8 }
          if (/wood|Timber/i.test(m.name)) next.roughness = .78
          if (/navy|ink/.test(m.name)) next.roughness = .68
          materials.set(m, next)
        }
        return materials.get(m)!
      }
      o.material = Array.isArray(o.material) ? o.material.map(copy) : copy(o.material as MeshStandardMaterial)
    })
    return clone
  }, [gltf.scene])
  useEffect(() => () => {
    const materials = new Set<MeshStandardMaterial>()
    scene.traverse(o => { if (o instanceof Mesh) for (const m of Array.isArray(o.material) ? o.material : [o.material]) materials.add(m as MeshStandardMaterial) })
    for (const m of materials) m.dispose()
  }, [scene])
  return { ...gltf, scene }
}
