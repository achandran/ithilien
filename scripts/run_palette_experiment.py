import json,subprocess,sys,os,shutil,itertools
from pathlib import Path
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'scripts'))
from ithilienlib import wcag,Color
out=root.parents[1]/'outputs/palette-experiment';out.mkdir(exist_ok=True)
source=json.loads((root/'palette/ithilien-dawn.json').read_text());base=source['colors']
rows=[]
for i,(spray,amber,ash) in enumerate(itertools.product(['#E0E9EE','#D7E3EA','#D2DFE7'],['#D8B46A','#D0A859'],['#596166','#51595E'])):
 c=dict(base,Spray=spray,Celandine=amber,Ash=ash)
 metrics={'comment_contrast':wcag(ash,base['Asphodel']),'inline_text_contrast':wcag('#000000',amber),'line_delta_e':Color(spray).delta_e(base['Asphodel'],method='2000'),'inline_delta_e':Color(amber).delta_e(spray,method='2000'),'search_delta_e':Color(amber).delta_e(base['Clematis'],method='2000')}
 rows.append({'id':f'candidate-{i:02d}','changes':{k:v for k,v in c.items() if base[k]!=v},'metrics':metrics,'screen_pass':min(metrics['comment_contrast'],metrics['inline_text_contrast'])>=4.5})
# Three distinct hypotheses, not a ranking by a saturated composite.
selected=[0,4,6,10]
(out/'screening.json').write_text(json.dumps({'baseline':'5479254','candidates':rows,'native_selected':[rows[i]['id'] for i in selected],'selection':'Baseline, stronger changed-line background, then two strengths of line blue with deeper amber. Comment colors remain unchanged in native finalists. No aesthetic-score optimization.'},indent=2))
env=dict(os.environ,CARGO_HOME='/private/tmp/ithilien-cargo',RUSTUP_HOME='/private/tmp/ithilien-rustup',RUSTUP_TOOLCHAIN='1.95.0');env['PATH']='/private/tmp/ithilien-cargo/bin:'+env['PATH']
files=subprocess.check_output(['git','ls-files'],cwd=root,text=True).splitlines()
for i in selected:
 row=rows[i];dest=root.parent/('experiment-'+row['id']);dest.mkdir(exist_ok=True)
 if not (dest/'.venv').exists():(dest/'.venv').symlink_to(root/'.venv',target_is_directory=True)
 for file in files:
  target=dest/file;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(root/file,target)
 p=json.loads(json.dumps(source));p['colors'].update(row['changes']);(dest/'palette/ithilien-dawn.json').write_text(json.dumps(p,indent=2)+'\n')
 with (out/(row['id']+'.log')).open('w') as log:
  print('START',row['id'],row['changes'],flush=True)
  subprocess.run([sys.executable,'scripts/generate_themes.py'],cwd=dest,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
  result=subprocess.run([sys.executable,'scripts/evaluate_suite.py','--themes','ithilien-dawn','--codex-source',str(root.parent/'review-codex'),'--python-source',str(root.parent/'eval-tree-sitter-python'),'--output',str(out/row['id'])],cwd=dest,env=env,stdout=log,stderr=subprocess.STDOUT)
  row['native_exit']=result.returncode
  print('DONE',row['id'],result.returncode,flush=True)
 (out/'screening.json').write_text(json.dumps({'baseline':'5479254','candidates':rows,'native_selected':[rows[j]['id'] for j in selected]},indent=2))
