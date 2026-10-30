from pathlib import Path
import subprocess,json,hashlib
R=Path.cwd();D=R/'docs/phase3bb-hotfix';proof=json.loads((D/'PUBLIC_CANDIDATE_PROOF.json').read_text());S=R/proof['candidate'];assert not(S/'.git').exists()
for cmd in [['git','init'],['git','config','user.name','Codex'],['git','config','user.email','codex@local.invalid'],['git','config','core.autocrlf','false'],['git','checkout','--orphan','candidate/phase3bb-fictional26'],['git','add','.'],['git','commit','-m','Immutable private Phase3BB fictional26 review candidate; exact public approval pending']]:subprocess.run(cmd,cwd=S,check=True,stdout=subprocess.DEVNULL)
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=S,text=True).strip();m=json.loads((S/'export-manifest.json').read_text())
for row in m['files']:
 blob=subprocess.check_output(['git','show',commit+':'+row['filename']],cwd=S);assert hashlib.sha256(blob).hexdigest()==row['sha256'],row['filename']
assert not subprocess.check_output(['git','remote'],cwd=S,text=True).strip();proof.update(artifactCommit=commit,committedPayloadVerified=len(m['files']),artifactHasPrivateAncestors=False,artifactRemotes=[],publicDecision='PENDING');(D/'PUBLIC_CANDIDATE_PROOF.json').write_text(json.dumps(proof,indent=2)+'\n');print('Pinned artifact',commit,'verified',len(m['files']),'committed blobs; NOT pushed')
