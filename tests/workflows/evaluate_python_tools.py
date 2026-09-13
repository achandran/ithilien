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

SCENES=('neotest-summary','neotest-output','dap-scopes')

def check(shot,colors):
    failures=[];e=shot['evidence'];text=shot['text']
    if not e.get('parser'):failures.append('Python Tree-sitter absent')
    if shot['case'].startswith('neotest'):
        counts=e.get('counts',{})
        for key in ('passed','failed','skipped'):
            if counts.get(key)!=1:failures.append('Expected one '+key+' test')
        required=('test_pass','test_fail','test_skip') if shot['case']=='neotest-summary' else ('AssertionError',)
    else:
        if not e.get('stopped'):failures.append('No stopped debugger session')
        required=('total','42')
        if not any(w['filetype']=='dapui_scopes' for w in e['windows']):failures.append('DAP scopes window absent')
    target='dapui_scopes' if shot['case']=='dap-scopes' else shot['case']
    pane=next((w.get('text','') for w in e['windows'] if w['filetype']==target),'')
    for token in required:
        if token not in pane:failures.append('Missing plugin pane content: '+token)
    for token in required:
        if token not in text:failures.append('Missing rendered content: '+token)
    if shot['case']=='neotest-summary':
        for group,name in [('NeotestPassed','Ilex'),('NeotestFailed','Annun'),('NeotestSkipped','Ash')]:
            visible=[c for c in shot['cells'] if c['text'].strip() and any(i.get('hi_name')==group for i in shot.get('attr_info',{}).get(str(c['attr']),shot.get('attr_info',{}).get(c['attr'],[])))]
            if not visible or any(effective_colors(shot,c)[0]!=int(colors[name][1:],16) for c in visible):
                failures.append('Missing or incorrect rendered test status: '+group)
    failures.extend(e.get('errors',[]))
    allowed={int(v[1:],16) for v in colors.values()}
    off=[c for c in shot['cells'] if effective_colors(shot,c)[1] not in allowed or (c['text'].strip() and effective_colors(shot,c)[0] not in allowed)]
    contrast=assess(shot)
    return {'pass':not failures and not off and not contrast['failures'],'failures':failures,'off_palette':off,'contrast':contrast}

def prepare(fetch=False):
    from tintprobe.evaluation_dependencies import plugin_dependencies
    return plugin_dependencies('tests/evaluation/python-tools-dependencies.json', fetch)


def run(output,widths=(100,160)):
    import os, sys
    os.environ['ITHILIEN_TEST_PYTHON']=sys.executable
    os.environ.setdefault('ITHILIEN_PYTHON_PARSER_ROOT',str(Path.home()/'.local/share/nvim/site'))
    import importlib.metadata
    versions={name:importlib.metadata.version(name) for name in ('pytest','debugpy')}
    parser=Path(os.environ['ITHILIEN_PYTHON_PARSER_ROOT'])/'parser/python.so'
    parser_digest=hashlib.sha256(parser.read_bytes()).hexdigest()
    output.mkdir(parents=True,exist_ok=True)
    deps=prepare()
    paths=[d['path'] for d in deps.values()]
    adapter={'id':'ithilien-dawn','paths':[str(ROOT),*paths], 'pins':{d['path']:d['revision'] for d in deps.values()}, 'setup':"""
vim.o.loadplugins=true
vim.opt.rtp:append(vim.env.ITHILIEN_PYTHON_PARSER_ROOT)
vim.cmd('syntax on')
vim.cmd('colorscheme ithilien-dawn')
"""}
    palette=(ROOT/'scripts/palette/ithilien.json').read_bytes()
    colors=json.loads(palette)['colors'];results=[];shots=[]
    for scene in SCENES:
        for width in widths:
            for state in ('initial','reload'):
                print(scene,width,state,flush=True)
                try:
                    shot=isolated_capture(adapter,width,scene,nvim=shutil.which('nvim'),action=state,workflow=str(evaluation_path('python-tools.lua')))
                    shots.append(shot);r=check(shot,colors)
                except Exception as exc:r={'pass':False,'error':str(exc)}
                results.append(dict(scene=scene,width=width,state=state,**r))
    report={'title':'Python testing and debugging workflows','pass':all(r['pass'] for r in results),'results':results,'dependencies':deps,'python_packages':versions,'python_parser_sha256':parser_digest,'nvim':subprocess.check_output(['nvim','--version'],text=True).splitlines()[0],'render_profile':json.loads((evaluation_path('render-profile.json')).read_text()),'palette_sha256':hashlib.sha256(palette).hexdigest(),'fixture_sha256':hashlib.sha256((evaluation_path('python-tools.lua')).read_bytes()).hexdigest(),'scope':'Actual pytest results and debugpy stopped state through Neotest and DAP UI. Native Neovim cells, not Ghostty pixels or comfort proof.'}
    (output/'report.json').write_text(json.dumps(report,indent=2));(output/'cells.json').write_text(json.dumps(shots))
    write_gallery(output,report,shots)
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=ROOT/'tests/evaluation/results/python-tools')
    p.add_argument('--fetch-dependencies',action='store_true',help='Fetch missing pinned test plugins')
    args=p.parse_args();prepare(args.fetch_dependencies);raise SystemExit(0 if run(args.output)['pass'] else 1)
