from tintprobe.context import evaluation_path, script_path, project_resource, EVALUATION
"""Native pytest and debugpy plugin screens; no personal Neovim configuration is loaded."""
import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path
from tintprobe.context import ROOT
from tintprobe.evaluate_interactions import isolated_capture, assess
from evaluate_installed_workflows import write_gallery
from tintprobe.evaluation_checks import effective_colors

SCENES=('telescope','snacks','cmp')

def check(shot,colors):
    errors=[];e=shot['evidence']
    target={'telescope':'TelescopeResults','snacks':'snacks_picker_list','cmp':'cmp_menu'}[shot['case']]
    panes=[w for w in e['windows'] if w['filetype']==target]
    if not panes:errors.append('Missing native pane: '+target)
    if not any('reading' in w['text'] for w in panes):errors.append('Missing result in native pane')
    if shot['case']=='cmp' and not e.get('visible'):errors.append('Completion not visible')
    if shot['case']!='cmp' and not any('return 42' in w['text'] for w in e['windows'] if w.get('preview') or 'preview' in w['filetype'].lower()):errors.append('Missing Python preview')
    errors.extend(e.get('errors',[]))
    allowed={int(v[1:],16) for v in colors.values()}
    off=[c for c in shot['cells'] if effective_colors(shot,c)[1] not in allowed or (c['text'].strip() and effective_colors(shot,c)[0] not in allowed)]
    contrast=assess(shot)
    return {'pass':not errors and not off and not contrast['failures'],'failures':errors,'off_palette':off,'contrast':contrast}

def prepare(fetch=False):
    from tintprobe.evaluation_dependencies import plugin_dependencies
    return plugin_dependencies('tests/evaluation/pickers-dependencies.json', fetch)


def run(output,widths=(100,160)):
    output.mkdir(parents=True,exist_ok=True)
    deps=prepare()
    paths=[d['path'] for d in deps.values()]
    adapter={'id':'ithilien-dawn','paths':[str(ROOT),*paths], 'pins':{d['path']:d['revision'] for d in deps.values()}, 'setup':"""
vim.o.loadplugins=true
vim.cmd('runtime plugin/cmp.lua')
require('snacks').setup({picker={enabled=true}})
vim.cmd('syntax on')
vim.cmd('colorscheme ithilien-dawn')
"""}
    palette=(ROOT/'scripts/palette/ithilien.json').read_bytes()
    colors=json.loads(palette)['variants']['ithilien-dawn']['colors'];results=[];shots=[]
    for scene in SCENES:
        for width in widths:
            for state in ('initial','reload'):
                print(scene,width,state,flush=True)
                try:
                    shot=isolated_capture(adapter,width,scene,nvim=shutil.which('nvim'),action=state,workflow=str(evaluation_path('pickers.lua')))
                    shots.append(shot);r=check(shot,colors)
                except Exception as exc:r={'pass':False,'error':str(exc)}
                results.append(dict(scene=scene,width=width,state=state,**r))
    report={'title':'Picker and completion workflows','pass':all(r['pass'] for r in results),'results':results,'dependencies':deps,'nvim':subprocess.check_output(['nvim','--version'],text=True).splitlines()[0],'render_profile':json.loads((evaluation_path('render-profile.json')).read_text()),'palette_sha256':hashlib.sha256(palette).hexdigest(),'fixture_sha256':hashlib.sha256((evaluation_path('pickers.lua')).read_bytes()).hexdigest(),'scope':'Actual Telescope, Snacks picker and nvim-cmp renderers with deterministic Python fixtures. Native Neovim cells, not Ghostty pixels or comfort proof.'}
    (output/'report.json').write_text(json.dumps(report,indent=2));(output/'cells.json').write_text(json.dumps(shots))
    write_gallery(output,report,shots)
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=ROOT/'tests/evaluation/results/pickers')
    p.add_argument('--fetch-dependencies',action='store_true',help='Fetch missing pinned test plugins')
    args=p.parse_args();prepare(args.fetch_dependencies);raise SystemExit(0 if run(args.output)['pass'] else 1)
