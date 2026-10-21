"""V10 authored roads-first study. No southern legacy files are inputs."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets-src/v10-city/plan'

def sample_points(road):
    """Smooth only landscape trails; street corners keep an urban hierarchy."""
    pts=road['points']
    if road['kind'] not in ['park','island'] or len(pts)<4:return [tuple(p)for p in pts]
    closed=pts[0]==pts[-1]
    src=([pts[-2]]+pts+[pts[1]]) if closed else ([pts[0]]+pts+[pts[-1]])
    result=[]
    for i in range(1,len(src)-2):
        a,b,c,d=src[i-1:i+3]
        for k in range(16):
            t=k/16
            result.append(tuple(round(0.5*((2*b[j])+(-a[j]+c[j])*t+(2*a[j]-5*b[j]+4*c[j]-d[j])*t*t+(-a[j]+3*b[j]-3*c[j]+d[j])*t*t*t))for j in [0,1]))
    return result+[tuple(pts[-1])]

def make_plan():
    roads = []
    def road(id, points, width=112, kind='street'):
        roads.append(dict(id=id, points=points, width=width, kind=kind))
    # A bent eastbound high street, with a pair of compact frontage loops.
    road('heritage-gateway', [[2176,2240],[2176,2416],[2016,2592],[2016,2960]], 112)
    road('station-high-street', [[1456,2960],[2016,2960],[2768,2960],[3456,2960],[4048,2960]], 160, 'primary')
    road('upper-neighborhood', [[1456,2960],[1456,2400],[2768,2400],[3456,2400],[3456,2960]], 96)
    road('market-loop', [[1456,2960],[1456,3504],[2016,3504],[2768,3504],[3456,3504],[3456,2960]], 96)
    road('book-lane', [[2768,2400],[2768,3504]], 96, 'lane')
    road('civic-lane', [[2016,2960],[2016,3504]], 96, 'lane')
    road('station-approach', [[3456,2960],[3776,2960],[3776,2832]], 112)
    road('park-to-sea', [[1456,2960],[1344,3248],[1456,3504],[1824,3760],[2320,3936],[3104,4112],[3776,4224]], 128, 'promenade')
    road('coastal-market', [[3456,3504],[3776,3712],[3776,4224]], 112)
    road('market-seafront', [[2768,3504],[2768,4032]], 112)
    road('leisure-arrival', [[1824,3760],[1456,3904],[1280,3904]], 112)
    road('leisure-circuit', [[1280,3904],[1136,3744],[624,3744],[400,3936],[464,4224],[960,4352],[1232,4176],[1280,3904]], 80, 'park')
    road('namsan-gateway', [[1456,2960],[1216,2960]], 96, 'park')
    road('namsan-loop', [[1216,2960],[1152,2672],[896,2480],[560,2528],[320,2784],[352,3104],[656,3328],[1024,3248],[1216,2960]], 72, 'park')
    road('tower-climb', [[560,2528],[608,2736],[864,2816],[896,3008],[736,3040]], 64, 'park')
    road('mainland-pier', [[3776,4224],[3968,4384],[3968,4592]], 128, 'pier')
    road('jeju-arrival', [[3296,5024],[3296,5184]], 112, 'pier')
    road('jeju-olle', [[3296,5184],[2992,5040],[2624,5168],[2464,5456],[2752,5648],[3216,5664],[3552,5488],[3568,5216],[3296,5184]], 80, 'island')
    road('village-lane', [[2624,5168],[2576,5360],[2944,5456],[3216,5664]], 72, 'island')
    plots = []
    def plot(id,label,rect,door,facing='south',district='commons',height=72):
        plots.append(dict(id=id,label=label,rect=rect,door=door,facing=facing,district=district,height=height))
    # Buildings define the four street corners; tight lots rather than isolated landmarks.
    for row,y,dy,face in [('N',2512,2816,'south'),('S',3136,3072,'north')]:
        for col,x in enumerate([1552,1736,2160,2384,2880,3104]):
            if row=='S' and col in [2,3]: continue  # civic court framed by its north and side frontages
            label = ['BOOKS','CAFE','LANGUAGE','GROCERY','DESIGN','BAKERY'][col]
            plot(f'{row}{col+1}',label,[x,y,152 if col<2 else 192,240 if row=='N' else 256],[x+(76 if col<2 else 96),dy],face,height=48+col*12)
    plot('station','STATION',[3592,2512,512,272],[3776,2832],district='transit',height=112)
    plot('station-kiosk','TRANSIT CAFE',[3576,3136,208,208],[3680,3072],'north','transit',56)
    plot('station-book','TICKETS / MARKET',[3888,3136,224,208],[4000,3072],'north','transit',80)
    plot('civic-house','COMMUNITY',[2384,3360,256,80],[2512,3312],'north',height=48)
    plot('coast-1','FISH MARKET',[2936,3696,256,192],[3064,3952],district='busan-coast')
    plot('coast-2','SEA CAFE',[3304,3792,256,192],[3432,4048],district='busan-coast',height=96)
    plot('terminal','FERRY TERMINAL',[3856,3992,288,192],[3776,4096],'west','busan-coast',88)
    plot('tower','NAMSAN TOWER',[672,2864,128,128],[736,3040],district='namsan',height=216)
    plot('wheel','FERRIS WHEEL',[512,3824,208,208],[616,4072],district='entertainment',height=136)
    plot('carousel','CAROUSEL',[864,3840,176,176],[952,4080],district='entertainment',height=72)
    plot('pavilion','CULTURE STAGE',[704,4216,192,80],[800,4168],'north','entertainment',48)
    plot('jeju-hall','VILLAGE HALL',[2720,5184,160,144],[2800,5384],district='jeju',height=48)
    plot('jeju-tea','TEA HOUSE',[3200,5376,176,128],[3288,5568],district='jeju',height=56)
    return dict(version='v10-graybox',status='AWAITING_MASTERPLAN_AND_GRAYBOX_APPROVAL',
      world=[4352,5888],protectedNorth=[0,0,4352,2240],actorFootprint=[16,8],nativeJuniFrame=[96,112],
      viewport=[1024,768],camera='top-down, y-sort, nearest, native 1x default',
      roads=roads,plots=plots,
      mainland=[[32,2240],[4320,2240],[4320,4368],[4032,4432],[3712,4368],[3296,4320],[2864,4224],[2464,4128],[2096,4000],[1744,3920],[1456,4352],[1168,4528],[688,4496],[272,4320],[128,3920],[160,3536],[64,3168]],
      island=[[2296,5184],[2512,4944],[2944,4864],[3472,4928],[3792,5168],[3760,5536],[3456,5776],[2928,5808],[2512,5664],[2320,5440]],
      civicCourt=[2112,3088,544,256],
      rail=[[3504,2448],[4208,2448]],
      regions=[dict(id='heritage',bounds=[0,0,4352,2240],ambient=[2176,1800]),dict(id='namsan',bounds=[0,2240,1392,3536],ambient=[736,2960]),dict(id='entertainment',bounds=[0,3536,1664,4640],ambient=[832,4016]),dict(id='jeju',bounds=[0,4736,4352,5888],ambient=[3008,5360]),dict(id='transit',bounds=[3504,2240,4352,3520],ambient=[3776,2960]),dict(id='busan-coast',bounds=[1664,3568,4352,4736],ambient=[3456,4096]),dict(id='commons',bounds=[1392,2240,3504,3568],ambient=[2384,3200])],
      travel=dict(enabled=True,mainlandTrigger=[3968,4560],mainlandArrival=[3968,4400],islandTrigger=[3296,5056],islandArrival=[3296,5216],seaBoundary=4736,discovery=[2464,5456]),
      reviewStops=[dict(id='gateway',point=[2176,2288]),dict(id='high-street',point=[2016,2960]),dict(id='civic-court',point=[2352,3216]),dict(id='station',point=[3776,2832]),dict(id='namsan',point=[736,3040]),dict(id='leisure',point=[1280,3904]),dict(id='coast',point=[3776,4224]),dict(id='pier',point=[3968,4560]),dict(id='jeju',point=[3296,5216])])

if __name__ == '__main__':
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'city.json').write_text(json.dumps(make_plan(),indent=2)+'\n')
    print('Authored V10 plan. Only independent literals, no previous southern inputs.')
