// Served preview uses repository assets. The standalone builder embeds these exact
// checksum-verified files as Blob URLs through this one adapter.
export const reforgeURL = (id: string) => '/v0.5/' + ({house:'models/hanok-reforge.glb',nari:'models/nari-messenger-art.glb',poster:'posters/hanok-day.png'} as Record<string,string>)[id]
