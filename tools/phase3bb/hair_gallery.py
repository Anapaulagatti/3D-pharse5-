import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'phase2c'))
from compose import *
c=Composer();names=['idle-front-0','idle-back-0','idle-left-0','idle-right-0','walk-front-3','run-back-3','wave-front-4','celebrate-front-4']; cases=[('juni',['kr-classic-bob']),('minjun',['kr-fashion-cap']),('doyun',['kr-garden-hat']),('ara',['ara-braided-bun']),('juni',['kr-classic-bob','kr-hair-ornament']),('minjun',['kr-layered-cut','kr-fashion-cap'])]
board=Image.new('RGBA',(96*8,112*len(cases)),(26,29,35))
for j,(id,ids) in enumerate(cases):
 for i,n in enumerate(names):board.alpha_composite(c.render(id,ids,n),(96*i,112*j))
board.save('docs/phase3bb-hotfix/hair-after-native.png');board.resize((1536,1344),Image.Resampling.NEAREST).save('/tmp/hair-after-review.png')
