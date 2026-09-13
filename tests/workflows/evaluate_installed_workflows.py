from tintprobe.context import evaluation_path, script_path, project_resource, EVALUATION
"""Capture actual installed plugin workflows with deterministic Python fixtures."""
import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import shutil
import subprocess
from tintprobe.evaluate_interactions import isolated_capture, assess
from tintprobe.compare_themes import render
from tintprobe.evaluation_checks import effective_colors
from tintprobe.context import ROOT

SCENES = {
    'python-lsp': ('Reading',), 'python-diff': ('str(total)', 'total='), 'python-search': ('values',), 'python-visual': ('values', 'total'),
    'python-diagnostic': ('Incompatible assignment',),
    'neo-tree': ('palette_workflow.py',), 'trouble': ('Incompatible assignment',),
    'which-key': ('Inspect Python',), 'grug-far': ('Search', 'Replace'),
    'fzf-lua': ('palette_workflow.py',), 'dashboard': ('Find File',), 'blink': ('summarize',),
}
PLUGIN = {'neo-tree':'neo-tree.nvim','trouble':'trouble.nvim','which-key':'which-key.nvim',
          'grug-far':'grug-far.nvim','fzf-lua':'fzf-lua','dashboard':'snacks.nvim','blink':'blink.cmp'}


WINDOW_TYPES={'neo-tree':'neo-tree','trouble':'trouble','which-key':'wk','grug-far':'grug-far','fzf-lua':'fzf','dashboard':'snacks_dashboard'}


def check(shot, palette):
    failures=[]
    if 'Lua callback:' in shot['text'] or 'Failed to run config' in shot['text']: failures.append('Rendered runtime error notification')
    for text in SCENES[shot['case']]:
        if text not in shot['text']: failures.append('Missing rendered content: '+text)
    evidence=shot['evidence']
    failures.extend('Runtime error: '+msg for msg in evidence.get('messages',[]))
    if not evidence['parser']: failures.append('Python Tree-sitter inactive')
    if shot['case']=='python-diagnostic' and not any(w.get('floating') for w in evidence['windows']): failures.append('Diagnostic float absent')
    window=WINDOW_TYPES.get(shot['case'])
    if window and not any(w['filetype']==window for w in evidence['windows']): failures.append('Plugin window absent: '+window)
    if shot['case']=='fzf-lua' and not any(w['filetype']=='fzf' and 'palette_workflow.py' in w.get('text','') for w in evidence['windows']):
        failures.append('Expected Python file absent from visible fzf result pane')
    plugin=PLUGIN.get(shot['case'])
    if plugin and plugin not in evidence['plugins']: failures.append('Plugin not loaded: '+plugin)
    if shot['case']=='python-lsp' and not evidence.get('lsp',{}).get('semantic_tokens'): failures.append('Live semantic tokens absent')
    if shot['case']=='blink' and not evidence['blink_visible']: failures.append('Blink menu not visible')
    if shot['case']=='python-visual' and evidence['mode']!='V': failures.append('Linewise Visual mode absent')
    # Require overlays on actual source cells, not merely defined highlight groups.
    colors=json.loads((ROOT/'scripts/palette/ithilien-dawn.json').read_text())['colors']
    role={'python-search':'Heather','python-visual':'Briar','python-diff':'Celandine'}.get(shot['case'])
    if role:
        expected=int(colors[role][1:],16)
        visible=[c for c in shot['cells'] if c['text'].strip() and effective_colors(shot,c)[1]==expected]
        if not visible: failures.append('Missing rendered '+role+' overlay')
    if shot['case']=='python-diff':
        # Both old and new single-digit edits must be emphasized, even at narrow width.
        for fragment in ('LIMIT = 10','LIMIT = 11'):
            found=False
            rows={}
            for c in shot['cells']: rows.setdefault(c['row'],[]).append(c)
            for cells in rows.values():
                cells=sorted(cells,key=lambda c:c['col'])
                text=''.join(c['text'] for c in cells)
                start=text.find(fragment)
                if start>=0:
                    found=True
                    target=cells[start+len(fragment)-1]
                    if effective_colors(shot,target)[1]!=int(colors['Celandine'][1:],16):
                        failures.append('Single-character edit not emphasized: '+fragment)
            if not found: failures.append('Single-character fixture missing: '+fragment)
    if shot['case']=='python-visual':
        for fragment in ('values =','total ='):
            rows={}
            for c in shot['cells']: rows.setdefault(c['row'],[]).append(c)
            found=False
            for cells in rows.values():
                cells=sorted(cells,key=lambda c:c['col'])
                text=''.join(c['text'] for c in cells)
                start=text.find(fragment)
                if start>=0:
                    found=True
                    if any(effective_colors(shot,c)[1]!=int(colors['Briar'][1:],16) for c in cells[start:] if c['text'].strip()):
                        failures.append('Partial line selection: '+fragment)
            if not found: failures.append('Selected source line missing: '+fragment)
    off=[]
    for cell in shot['cells']:
        fg,bg=effective_colors(shot,cell)
        if bg not in palette or (cell['text'].strip() and fg not in palette):
            off.append({'row':cell['row'],'col':cell['col'],'text':cell['text'],'fg':f'#{fg:06X}','bg':f'#{bg:06X}'})
    # Guides are decoration, not text: identify them by native highlight provenance.
    def decorative(cell):
        info=shot.get('attr_info',{}).get(str(cell['attr']),shot.get('attr_info',{}).get(cell['attr'],[]))
        return (any(i.get('hi_name','').startswith(('SnacksIndent','IblIndent','IblScope')) for i in info)
                or (cell['text'] in ('\ue0b0','\ue0b2') and any(i.get('hi_name','').startswith('lualine_transitional_') for i in info)))
    text_shot=dict(shot,cells=[c for c in shot['cells'] if not decorative(c)])
    contrast=assess(text_shot)
    contrast['decorative_cells']=sum(decorative(c) for c in shot['cells'])
    blocked=shot['case']=='fzf-lua' and any('fzf error 2: operation not permitted' in message for message in evidence.get('history',[]))
    return {'status':'blocked' if blocked else ('pass' if not failures and not off and not contrast['failures'] else 'fail'),
            'blocked_reason':'Terminal mode ioctl denied by execution environment' if blocked else None,
            'failures':failures,'off_palette':off,'contrast':contrast,
            'pass':not blocked and not failures and not off and not contrast['failures']}


def adapter(init, lazy):
    quote=json.dumps
    setup=f'''
vim.o.loadplugins=true
vim.lsp.enable=function() end -- deterministic scenarios start their own explicit server
vim.fn.mkdir(vim.fn.stdpath('state'),'p')
vim.g.minianimate_disable=true
vim.opt.rtp:prepend({quote(str(init.parent))})
vim.opt.rtp:prepend({quote(str(lazy))})
local lazy=require('lazy');local setup=lazy.setup
lazy.setup=function(o)
 o.install={{missing=false}};o.checker={{enabled=false}};o.change_detection={{enabled=false}};o.readme={{enabled=false}}
 o.lockfile=vim.fn.getcwd()..'/lock.json';o.state=vim.fn.getcwd()..'/state.json'
 table.insert(o.spec,{{'achandran/ithilien',dir={quote(str(ROOT))}}})
 table.insert(o.spec,{{'nvim-neo-tree/neo-tree.nvim',opts={{log_to_file=vim.fn.getcwd()..'/neo-tree.log',filesystem={{use_libuv_file_watcher=false}}}}}})
 table.insert(o.spec,{{'cormacrelf/dark-notify',enabled=false}})
 return setup(o)
end
dofile({quote(str(init))})
for name,p in pairs(require('lazy.core.config').plugins) do
 if name~='catppuccin' and name~='tokyonight.nvim' and name~='dark-notify' then
  assert(vim.fn.isdirectory(p.dir)==1,'Missing plugin: '..name)
  lazy.load({{plugins={{name}}}})
 end
end
_G.ithilien_messages={{}}
local notify=vim.notify
vim.notify=function(msg,level,opts)
 if level and level>=vim.log.levels.ERROR then table.insert(_G.ithilien_messages,tostring(msg)) end
 return notify(msg,level,opts)
end
vim.cmd('colorscheme ithilien-dawn')
vim.wait(100)
'''
    return {'id':'ithilien-dawn','paths':[str(ROOT)],'setup':setup}


def run(output, init, lazy, scenes=None, widths=(100,160), states=('initial','reload')):
    output.mkdir(parents=True,exist_ok=True)
    os.environ.setdefault('ITHILIEN_LSP_COMMAND',str(Path(__import__('sys').executable).parent/'basedpyright-langserver'))
    revisions={}
    for folder in sorted(lazy.parent.iterdir()):
        if (folder/'.git').exists():
            revisions[folder.name]=subprocess.check_output(['git','-C',str(folder),'rev-parse','HEAD'],text=True).strip()
    palette=json.loads((ROOT/'scripts/palette/ithilien-dawn.json').read_text())
    allowed={int(v[1:],16) for v in palette['colors'].values()}
    records=[];results=[]
    for scene in scenes or SCENES:
        for width in widths:
            for state in states:
                print(f'{scene} {width} {state}',flush=True)
                try:
                    shot=isolated_capture(adapter(init,lazy),width,scene,nvim=shutil.which('nvim'),action=state,
                                          workflow=str(evaluation_path('installed-workflows.lua')))
                    records.append(shot);results.append(dict(scene=scene,width=width,state=state,**check(shot,allowed)))
                except Exception as exc:
                    results.append({'scene':scene,'width':width,'state':state,'pass':False,'error':str(exc)})
    report={'pass':all(r['pass'] for r in results) and bool(results),'results':results,
            'fixture_sha256':hashlib.sha256((evaluation_path('installed-workflows.lua')).read_bytes()).hexdigest(),
            'palette_sha256':hashlib.sha256((ROOT/'scripts/palette/ithilien-dawn.json').read_bytes()).hexdigest(),
            'plugin_revisions':revisions,
            'nvim':subprocess.check_output(['nvim','--version'],text=True).splitlines()[0],
            'scope':'Actual installed plugin renderers and Python Tree-sitter. Deterministic diagnostics plus an explicit live BasedPyright case; normal configured servers are disabled for reproducibility. Neovim RGB cell captures, not native Ghostty screenshots. No comfort proof.',
            'render_profile':json.loads((evaluation_path('render-profile.json')).read_text())}
    (output/'report.json').write_text(json.dumps(report,indent=2))
    (output/'cells.json').write_text(json.dumps(records))
    write_gallery(output,report,records)
    return report


def write_gallery(output, report, records):
    rows=[]
    for result in report['results']:
        errors=result.get('failures',[])+([result['error']] if result.get('error') else [])
        detail=f"{len(result.get('off_palette',[]))} off-palette cells; {len(result.get('contrast',{}).get('failures',[]))} low-contrast text cells"
        rows.append('<tr><td>'+html.escape(f"{result['scene']} / {result['width']} / {result['state']}")+'</td><td>'+result.get('status',('pass' if result['pass'] else 'fail')).upper()+'</td><td>'+html.escape(detail+'; '+'; '.join(errors))+'</td></tr>')
    blocks=''.join('<details><summary>'+html.escape(f"{s['case']} / {s['width']} / {s['state']}")+'</summary>'+render(s)+'</details>' for s in records)
    passed=sum(r['pass'] for r in report['results'])
    (output/'gallery.html').write_text('<!doctype html><meta charset="utf-8"><style>body{font:16px system-ui;padding:24px}pre{font:16pt/1.4 "Berkeley Mono Medium",monospace;overflow:auto}td{padding:8px;border-bottom:1px solid #ddd;max-width:65em;overflow-wrap:anywhere}</style><h1>'+html.escape(report.get('title','Installed Neovim workflows'))+'</h1><p>'+report['scope']+f'</p><h2>{passed}/{len(report["results"])} cases passed</h2><p><a href="report.json">Full evidence</a></p><table>'+''.join(rows)+'</table>'+blocks)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--init',type=Path,default=Path.home()/'.config/nvim/init.lua')
    p.add_argument('--lazy-root',type=Path,default=Path.home()/'.local/share/nvim/lazy/lazy.nvim')
    p.add_argument('--scenes',nargs='+',choices=list(SCENES))
    a=p.parse_args()
    raise SystemExit(0 if run(a.output.resolve(),a.init.resolve(),a.lazy_root.resolve(),a.scenes)['pass'] else 1)
