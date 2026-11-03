"""Deterministic balance table, not a claim of real-economy/security certification."""
from pathlib import Path
import json
D=Path('docs/phase3bd');rows=[]
for name,buy,yield_,sell,seconds,stock in [('radish',4,2,3,45,50),('scallion',6,3,3,90,50)]:
 assert sell*yield_>buy and seconds>0
 rows.append({'crop':name,'seedCost':buy,'yield':yield_,'sellPerUnit':sell,'netPerActualCrop':sell*yield_-buy,'growthSeconds':seconds,'maximumReviewStockProfit':stock*(sell*yield_-buy),'instantBuySellSeedProfit':None,'reason':'Seeds not sellable; produce not buyable. Finite stock, actual growing/harvest/sale required, no passive offline autoharvest.'})
(D/'ECONOMY_SIMULATION.json').write_text(json.dumps({'status':'PASS CONFIGURED NO-INSTANT-ARBITRAGE / NOT ECONOMIC CERTIFICATION','rows':rows,'questRewardsOneTime':{'radish':18,'market':22},'introGrowthOneTimeSeconds':{'radish':6,'scallion':10},'allEducationAndDefaultsFree':True,'realMoney':False,'ads':'DISABLED'},indent=2)+'\n')
