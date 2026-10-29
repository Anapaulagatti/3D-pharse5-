"""Distinguish first-release404 from authorization/network failures; never print token."""
import os,json,urllib.request,urllib.error
request=urllib.request.Request('https://api.github.com/repos/'+os.environ['GITHUB_REPOSITORY']+'/branches/pages-snapshots',headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Accept':'application/vnd.github+json'})
try:
 with urllib.request.urlopen(request,timeout=30)as response:json.load(response)
 exists=True
except urllib.error.HTTPError as error:
 if error.code!=404:raise SystemExit('Cannot inspect snapshot branch: HTTP '+str(error.code))
 exists=False
with open(os.environ['GITHUB_OUTPUT'],'a')as f:f.write('exists='+str(exists).lower()+'\n')
